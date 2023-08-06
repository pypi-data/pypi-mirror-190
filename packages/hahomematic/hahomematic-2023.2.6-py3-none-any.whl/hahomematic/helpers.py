"""Helper functions used within hahomematic."""
from __future__ import annotations

import base64
from collections.abc import Collection
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime
import logging
import os
import re
import socket
import ssl
from typing import Any

import hahomematic.central_unit as hmcu
from hahomematic.const import (
    BINARY_SENSOR_TRUE_VALUE_DICT_FOR_VALUE_LIST,
    CCU_PASSWORD_PATTERN,
    HM_TYPE,
    HM_VIRTUAL_REMOTE_ADDRESSES,
    INIT_DATETIME,
    MAX_CACHE_AGE,
    PROGRAM_ADDRESS,
    SYSVAR_ADDRESS,
    SYSVAR_HM_TYPE_FLOAT,
    SYSVAR_HM_TYPE_INTEGER,
    SYSVAR_TYPE_ALARM,
    SYSVAR_TYPE_LIST,
    SYSVAR_TYPE_LOGIC,
    TYPE_BOOL,
    TYPE_FLOAT,
    TYPE_INTEGER,
    TYPE_STRING,
    HmEntityUsage,
)
import hahomematic.custom_platforms.entity_definition as hmed
import hahomematic.device as hmd
from hahomematic.exceptions import HaHomematicException

_LOGGER = logging.getLogger(__name__)


def generate_unique_identifier(
    central: hmcu.CentralUnit,
    address: str,
    parameter: str | None = None,
    prefix: str | None = None,
) -> str:
    """
    Build unique identifier from address and parameter.

    Central id is additionally used for heating groups.
    Prefix is used for events and buttons.
    """
    unique_identifier = address.replace(":", "_").replace("-", "_")
    if parameter:
        unique_identifier = f"{unique_identifier}_{parameter}"

    if prefix:
        unique_identifier = f"{prefix}_{unique_identifier}"
    if (
        address in (PROGRAM_ADDRESS, SYSVAR_ADDRESS)
        or address.startswith("INT000")
        or address.split(":")[0] in HM_VIRTUAL_REMOTE_ADDRESSES
    ):
        return f"{central.config.central_id}_{unique_identifier}".lower()
    return f"{unique_identifier}".lower()


def build_xml_rpc_uri(
    host: str,
    port: int,
    path: str | None,
    tls: bool = False,
) -> str:
    """Build XML-RPC API URL from components."""
    scheme = "http"
    if not path:
        path = ""
    if path and not path.startswith("/"):
        path = f"/{path}"
    if tls:
        scheme += "s"
    return f"{scheme}://{host}:{port}{path}"


def build_headers(
    username: str,
    password: str,
) -> list[tuple[str, str]]:
    """Build XML-RPC API header."""
    cred_bytes = f"{username}:{password}".encode()
    base64_message = base64.b64encode(cred_bytes).decode("utf-8")
    return [("Authorization", f"Basic {base64_message}")]


def check_or_create_directory(directory: str) -> bool:
    """Check / create directory."""
    if not directory:
        return False
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as ose:
            _LOGGER.error(
                "CHECK_OR_CREATE_DIRECTORY failed: Unable to create directory %s ('%s')",
                directory,
                ose.strerror,
            )
            raise HaHomematicException from ose

    return True


def parse_sys_var(data_type: str | None, raw_value: Any) -> Any:
    """Parse system variables to fix type."""
    # pylint: disable=no-else-return
    if not data_type:
        return raw_value
    if data_type in (SYSVAR_TYPE_ALARM, SYSVAR_TYPE_LOGIC):
        return to_bool(raw_value)
    if data_type == SYSVAR_HM_TYPE_FLOAT:
        return float(raw_value)
    if data_type in (SYSVAR_HM_TYPE_INTEGER, SYSVAR_TYPE_LIST):
        return int(raw_value)
    return raw_value


def to_bool(value: Any) -> bool:
    """Convert defined string values to bool."""
    if isinstance(value, bool):
        return value

    if not isinstance(value, str):
        raise TypeError("invalid literal for boolean. Not a string.")

    lower_value = value.lower()
    return lower_value in ["y", "yes", "t", "true", "on", "1"]


def get_entity_name(
    central: hmcu.CentralUnit,
    device: hmd.HmDevice,
    channel_no: int,
    parameter: str,
) -> EntityNameData:
    """Get name for entity."""
    channel_address = f"{device.device_address}:{channel_no}"
    if channel_name := _get_base_name_from_channel_or_device(
        central=central,
        device=device,
        channel_no=channel_no,
    ):
        p_name = parameter.title().replace("_", " ")

        if _check_channel_name_with_channel_no(name=channel_name):
            c_name = channel_name.split(":")[0]
            c_postfix = ""
            if central.paramset_descriptions.has_multiple_channels(
                channel_address=channel_address, parameter=parameter
            ):
                c_postfix = "" if channel_no == 0 else f" ch{channel_no}"
            entity_name = EntityNameData(
                device_name=device.name,
                channel_name=c_name,
                parameter_name=f"{p_name}{c_postfix}",
            )
        else:
            entity_name = EntityNameData(
                device_name=device.name,
                channel_name=channel_name,
                parameter_name=p_name,
            )
        return entity_name

    _LOGGER.debug(
        "GET_ENTITY_NAME: Using unique_identifier for %s %s %s",
        device.device_type,
        channel_address,
        parameter,
    )
    return EntityNameData.empty()


def get_event_name(
    central: hmcu.CentralUnit,
    device: hmd.HmDevice,
    channel_no: int,
    parameter: str,
) -> EntityNameData:
    """Get name for event."""
    channel_address = f"{device.device_address}:{channel_no}"
    if channel_name := _get_base_name_from_channel_or_device(
        central=central,
        device=device,
        channel_no=channel_no,
    ):
        p_name = parameter.title().replace("_", " ")
        if _check_channel_name_with_channel_no(name=channel_name):
            d_name = channel_name.split(":")[0]
            c_name = "" if channel_no == 0 else f" Channel {channel_no}"
            event_name = EntityNameData(
                device_name=device.name,
                channel_name=d_name,
                parameter_name=f"{c_name} {p_name}",
            )
        else:
            event_name = EntityNameData(
                device_name=device.name,
                channel_name=channel_name,
                parameter_name=p_name,
            )
        return event_name

    _LOGGER.debug(
        "GET_EVENT_NAME: Using unique_identifier for %s %s %s",
        device.device_type,
        channel_address,
        parameter,
    )
    return EntityNameData.empty()


def get_custom_entity_name(
    central: hmcu.CentralUnit,
    device: hmd.HmDevice,
    channel_no: int,
    is_only_primary_channel: bool,
    usage: HmEntityUsage,
) -> EntityNameData:
    """Get name for custom entity."""
    if channel_name := _get_base_name_from_channel_or_device(
        central=central,
        device=device,
        channel_no=channel_no,
    ):
        if is_only_primary_channel and _check_channel_name_with_channel_no(name=channel_name):
            return EntityNameData(device_name=device.name, channel_name=channel_name.split(":")[0])
        if _check_channel_name_with_channel_no(name=channel_name):
            c_name = channel_name.split(":")[0]
            p_name = channel_name.split(":")[1]
            marker = "ch" if usage == HmEntityUsage.CE_PRIMARY else "vch"
            p_name = f"{marker}{p_name}"
            return EntityNameData(
                device_name=device.name, channel_name=c_name, parameter_name=p_name
            )
        return EntityNameData(device_name=device.name, channel_name=channel_name)

    _LOGGER.debug(
        "GET_CUSTOM_ENTITY_NAME: Using unique_identifier for %s %s %s",
        device.device_type,
        device.device_address,
        channel_no,
    )
    return EntityNameData.empty()


def _check_channel_name_with_channel_no(name: str) -> bool:
    """Check if name contains channel and this is an int."""
    if name.count(":") == 1:
        channel_part = name.split(":")[1]
        try:
            int(channel_part)
            return True
        except ValueError:
            return False
    return False


def get_device_name(central: hmcu.CentralUnit, device_address: str, device_type: str) -> str:
    """Return the cached name for a device, or an auto-generated."""
    if name := central.device_details.get_name(address=device_address):
        return name

    _LOGGER.debug(
        "GET_DEVICE_NAME: Using auto-generated name for %s %s",
        device_type,
        device_address,
    )
    return get_generic_device_name(device_address=device_address, device_type=device_type)


def get_generic_device_name(device_address: str, device_type: str) -> str:
    """Return auto-generated device name."""
    return f"{device_type}_{device_address}"


def check_channel_is_the_only_primary_channel(
    current_channel: int, device_def: dict[str, Any], device_has_multiple_channels: bool
) -> bool:
    """Check if this channel is the only primary channel."""
    primary_channel: int = device_def[hmed.ED_PRIMARY_CHANNEL]
    if primary_channel == current_channel and device_has_multiple_channels is False:
        return True
    return False


def check_password(password: str | None) -> bool:
    """Check password."""
    if password is None:
        return False
    return re.fullmatch(CCU_PASSWORD_PATTERN, password) is not None


def _get_base_name_from_channel_or_device(
    central: hmcu.CentralUnit,
    device: hmd.HmDevice,
    channel_no: int,
) -> str | None:
    """Get the name from channel if it's not default, otherwise from device."""
    channel_address = f"{device.device_address}:{channel_no}"
    default_channel_name = f"{device.device_type} {channel_address}"
    name = central.device_details.get_name(channel_address)
    if name is None or name == default_channel_name:
        return f"{device.name}:{channel_no}"
    return name


def get_tls_context(verify_tls: bool) -> ssl.SSLContext:
    """Return tls verified/unverified ssl/tls context."""
    if verify_tls:
        ssl_context = ssl.create_default_context()
    else:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
    return ssl_context


def get_device_address(address: str) -> str:
    """Return the device part of an address."""
    if ":" in address:
        return address.split(":")[0]
    return address


def get_device_channel(address: str) -> int:
    """Return the channel part of an address."""
    if ":" not in address:
        raise HaHomematicException("Address has no channel part.")
    return int(address.split(":")[1])


def get_channel_no(address: str) -> int | None:
    """Return the channel part of an address."""
    if ":" not in address:
        return None
    return int(address.split(":")[1])


def updated_within_seconds(last_update: datetime, max_age_seconds: int = MAX_CACHE_AGE) -> bool:
    """Entity has been updated within X minutes."""
    if last_update == INIT_DATETIME:
        return False
    delta = datetime.now() - last_update
    if delta.seconds < max_age_seconds:
        return True
    return False


def convert_value(value: Any, target_type: str, value_list: tuple[str, ...] | None) -> Any:
    """Convert a value to target_type."""
    if value is None:
        return None
    if target_type == TYPE_BOOL:
        if value_list:
            # relevant for ENUMs retyped to a BOOL
            return _get_binary_sensor_value(value=value, value_list=value_list)
        if isinstance(value, str):
            return to_bool(value)
        return bool(value)
    if target_type == TYPE_FLOAT:
        return float(value)
    if target_type == TYPE_INTEGER:
        return int(float(value))
    if target_type == TYPE_STRING:
        return str(value)
    return value


def is_binary_sensor(parameter_data: dict[str, Any]) -> bool:
    """Check, if the sensor is a binary_sensor."""
    if parameter_data[HM_TYPE] == TYPE_BOOL:
        return True
    if value_list := parameter_data.get("VALUE_LIST"):
        return tuple(value_list) in BINARY_SENSOR_TRUE_VALUE_DICT_FOR_VALUE_LIST
    return False


def _get_binary_sensor_value(value: int, value_list: tuple[str, ...]) -> bool:
    """Return, the value of a binary_sensor."""
    try:
        str_value = value_list[value]
        if true_value := BINARY_SENSOR_TRUE_VALUE_DICT_FOR_VALUE_LIST.get(value_list):
            return str_value == true_value
    except IndexError:
        pass
    return False


def find_free_port() -> int:
    """Find a free port for XmlRpc server default port."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("", 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return int(sock.getsockname()[1])


def element_matches_key(
    search_elements: str | Collection[str],
    compare_with: str | None,
    do_wildcard_search: bool = True,
) -> bool:
    """Return if collection element is key."""
    if compare_with is None:
        return False

    if isinstance(search_elements, str):
        if do_wildcard_search:
            return compare_with.lower().startswith(search_elements.lower())
        return compare_with.lower() == search_elements.lower()
    if isinstance(search_elements, Collection):
        for element in search_elements:
            if do_wildcard_search:
                if compare_with.lower().startswith(element.lower()):
                    return True
            else:
                if compare_with.lower() == element.lower():
                    return True
    return False


def get_value_from_dict_by_wildcard_key(
    search_elements: dict[str, Any],
    compare_with: str | None,
    do_wildcard_search: bool = True,
) -> Any | None:
    """Return the dict value by wildcard type."""
    if compare_with is None:
        return None

    for key, value in search_elements.items():
        if do_wildcard_search:
            if key.lower().startswith(compare_with.lower()):
                return value
        else:
            if key.lower() == compare_with.lower():
                return value
    return None


@dataclass
class HubData:
    """Dataclass for hub entities."""

    name: str


@dataclass
class ProgramData(HubData):
    """Dataclass for programs."""

    pid: str
    is_active: bool
    is_internal: bool
    last_execute_time: str


@dataclass
class SystemVariableData(HubData):
    """Dataclass for system variables."""

    data_type: str | None = None
    unit: str | None = None
    value: bool | float | int | str | None = None
    value_list: list[str] | None = None
    max_value: float | int | None = None
    min_value: float | int | None = None
    extended_sysvar: bool = False


class EntityNameData:
    """Dataclass for entity name parts."""

    def __init__(
        self, device_name: str, channel_name: str, parameter_name: str | None = None
    ) -> None:
        """Init the EntityNameData class."""
        self._device_name = device_name
        self._channel_name = channel_name
        self._parameter_name = parameter_name

    @staticmethod
    def empty() -> EntityNameData:
        """Return an empty EntityNameData."""
        return EntityNameData(device_name="", channel_name="")

    @property
    def entity_name(self) -> str | None:
        """Return the name of the entity only name."""
        if self._device_name and self._name and self._name.startswith(self._device_name):
            return self._name.replace(self._device_name, "").strip()
        return self._name

    @property
    def full_name(self) -> str:
        """Return the full name of the entity."""
        if self.entity_name:
            return f"{self._device_name} {self.entity_name}".strip()
        return self._device_name

    @property
    def _name(self) -> str | None:
        """Return the name of the entity."""
        if self._channel_name and self._parameter_name:
            return f"{self._channel_name} {self._parameter_name}".strip()
        if self._channel_name:
            return self._channel_name.strip()
        return None
