"""The module contains device descriptions for custom entities."""
from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
import logging
from typing import Any, Final, cast

import voluptuous as vol

from hahomematic.backport import StrEnum
import hahomematic.device as hmd
import hahomematic.entity as hme
from hahomematic.helpers import generate_unique_identifier

ED_DEFAULT_ENTITIES: Final = "default_entities"
ED_INCLUDE_DEFAULT_ENTITIES: Final = "include_default_entities"
ED_DEVICE_GROUP: Final = "device_group"
ED_DEVICE_DEFINITIONS: Final = "device_definitions"
ED_ADDITIONAL_ENTITIES: Final = "additional_entities"
ED_FIELDS: Final = "fields"
ED_REPEATABLE_FIELDS: Final = "repeatable_fields"
ED_VISIBLE_REPEATABLE_FIELDS: Final = "visible_repeatable_fields"
ED_PRIMARY_CHANNEL: Final = "primary_channel"
ED_SECONDARY_CHANNELS: Final = "secondary_channels"
ED_VISIBLE_FIELDS: Final = "visible_fields"
DEFAULT_INCLUDE_DEFAULT_ENTITIES: Final = True

FIELD_ACTIVE_PROFILE: Final = "active_profile"
FIELD_AUTO_MODE: Final = "auto_mode"
FIELD_BOOST_MODE: Final = "boost_mode"
FIELD_CHANNEL_COLOR: Final = "channel_color"
FIELD_CHANNEL_LEVEL: Final = "channel_level"
FIELD_CHANNEL_LEVEL_2: Final = "channel_level_2"
FIELD_CHANNEL_OPERATION_MODE: Final = "channel_operation_mode"
FIELD_CHANNEL_STATE: Final = "channel_state"
FIELD_COLOR: Final = "color"
FIELD_COLOR_LEVEL: Final = "color_temp"
FIELD_COMFORT_MODE: Final = "comfort_mode"
FIELD_CONTROL_MODE: Final = "control_mode"
FIELD_CURRENT: Final = "current"
FIELD_DIRECTION: Final = "direction"
FIELD_DOOR_COMMAND: Final = "door_command"
FIELD_DOOR_STATE: Final = "door_state"
FIELD_DURATION_UNIT: Final = "duration_unit"
FIELD_DURATION: Final = "duration"
FIELD_DUTY_CYCLE: Final = "duty_cycle"
FIELD_DUTYCYCLE: Final = "dutycycle"
FIELD_ERROR: Final = "error"
FIELD_ENERGY_COUNTER: Final = "energy_counter"
FIELD_FREQUENCY: Final = "frequency"
FIELD_HEATING_COOLING: Final = "heating_cooling"
FIELD_HUMIDITY: Final = "humidity"
FIELD_INHIBIT: Final = "inhibit"
FIELD_LEVEL: Final = "level"
FIELD_LEVEL_2: Final = "level_2"
FIELD_LOCK_STATE: Final = "lock_state"
FIELD_LOCK_TARGET_LEVEL: Final = "lock_target_level"
FIELD_LOW_BAT: Final = "low_bat"
FIELD_LOWBAT: Final = "lowbat"
FIELD_LOWERING_MODE: Final = "lowering_mode"
FIELD_MANU_MODE: Final = "manu_mode"
FIELD_ON_TIME_VALUE: Final = "on_time_value"
FIELD_ON_TIME_UNIT: Final = "on_time_unit"
FIELD_OPERATING_VOLTAGE: Final = "operating_voltage"
FIELD_OPEN: Final = "open"
FIELD_PARTY_MODE: Final = "party_mode"
FIELD_PROGRAM: Final = "program"
FIELD_POWER: Final = "power"
FIELD_RAMP_TIME_VALUE: Final = "ramp_time_value"
FIELD_RAMP_TIME_UNIT: Final = "ramp_time_unit"
FIELD_RSSI_DEVICE: Final = "rssi_device"
FIELD_RSSI_PEER: Final = "rssi_peer"
FIELD_SABOTAGE: Final = "sabotage"
FIELD_SECTION: Final = "section"
FIELD_SET_POINT_MODE: Final = "set_point_mode"
FIELD_SETPOINT: Final = "setpoint"
FIELD_STATE: Final = "state"
FIELD_STOP: Final = "stop"
FIELD_SWITCH_MAIN: Final = "switch_main"
FIELD_SWITCH_V1: Final = "vswitch_1"
FIELD_SWITCH_V2: Final = "vswitch_2"
FIELD_TEMPERATURE: Final = "temperature"
FIELD_TEMPERATURE_MAXIMUM: Final = "temperature_maximum"
FIELD_TEMPERATURE_MINIMUM: Final = "temperature_minimum"
FIELD_VALVE_STATE: Final = "valve_state"
FIELD_VOLTAGE: Final = "voltage"

FIELD_ACOUSTIC_ALARM_ACTIVE: Final = "acoustic_alarm_active"
FIELD_ACOUSTIC_ALARM_SELECTION: Final = "acoustic_alarm_selection"
FIELD_OPTICAL_ALARM_ACTIVE: Final = "optical_alarm_active"
FIELD_OPTICAL_ALARM_SELECTION: Final = "optical_alarm_selection"

_LOGGER = logging.getLogger(__name__)


class EntityDefinition(StrEnum):
    """Enum for entity definitions."""

    IP_COVER = "IPCover"
    IP_DIMMER = "IPDimmer"
    IP_GARAGE = "IPGarage"
    IP_SWITCH = "IPSwitch"
    IP_FIXED_COLOR_LIGHT = "IPFixedColorLight"
    IP_SIMPLE_FIXED_COLOR_LIGHT = "IPSimpleFixedColorLight"
    IP_LOCK = "IPLock"
    IP_THERMOSTAT = "IPThermostat"
    IP_THERMOSTAT_GROUP = "IPThermostatGroup"
    IP_SIREN = "IPSiren"
    RF_COVER = "RfCover"
    RF_DIMMER = "RfDimmer"
    RF_DIMMER_COLOR = "RfDimmer_Color"
    RF_DIMMER_COLOR_TEMP = "RfDimmer_Color_Temp"
    RF_DIMMER_WITH_VIRT_CHANNEL = "RfDimmerWithVirtChannel"
    RF_LOCK = "RfLock"
    RF_THERMOSTAT = "RfThermostat"
    RF_THERMOSTAT_GROUP = "RfThermostatGroup"
    RF_SIREN = "RfSiren"
    RF_SWITCH = "RfSwitch"
    SIMPLE_RF_THERMOSTAT = "SimpleRfThermostat"


SCHEMA_ED_ADDITIONAL_ENTITIES = vol.Schema(
    {vol.Required(vol.Any(int, tuple[int, ...])): vol.Schema((vol.Optional(str),))}
)

SCHEMA_ED_FIELD_DETAILS = vol.Schema({vol.Required(str): str})

SCHEMA_ED_FIELD = vol.Schema({vol.Required(int): SCHEMA_ED_FIELD_DETAILS})

SCHEMA_ED_DEVICE_GROUP = vol.Schema(
    {
        vol.Required(ED_PRIMARY_CHANNEL): int,
        vol.Optional(ED_SECONDARY_CHANNELS): (int,),
        vol.Optional(ED_REPEATABLE_FIELDS): SCHEMA_ED_FIELD_DETAILS,
        vol.Optional(ED_VISIBLE_REPEATABLE_FIELDS): SCHEMA_ED_FIELD_DETAILS,
        vol.Optional(ED_FIELDS): SCHEMA_ED_FIELD,
        vol.Optional(ED_VISIBLE_FIELDS): SCHEMA_ED_FIELD,
    }
)

SCHEMA_ED_DEVICE_GROUPS = vol.Schema(
    {
        vol.Required(ED_DEVICE_GROUP): SCHEMA_ED_DEVICE_GROUP,
        vol.Optional(ED_ADDITIONAL_ENTITIES): SCHEMA_ED_ADDITIONAL_ENTITIES,
        vol.Optional(ED_INCLUDE_DEFAULT_ENTITIES, DEFAULT_INCLUDE_DEFAULT_ENTITIES): bool,
    }
)

SCHEMA_DEVICE_DESCRIPTION = vol.Schema(
    {
        vol.Required(ED_DEFAULT_ENTITIES): SCHEMA_ED_ADDITIONAL_ENTITIES,
        vol.Required(ED_DEVICE_DEFINITIONS): vol.Schema(
            {
                vol.Required(EntityDefinition): SCHEMA_ED_DEVICE_GROUPS,
            }
        ),
    }
)

entity_definition: dict[str, dict[int | str | EntityDefinition, vol.Any]] = {
    ED_DEFAULT_ENTITIES: {
        0: (
            "DUTY_CYCLE",
            "DUTYCYCLE",
            "LOW_BAT",
            "LOWBAT",
            "OPERATING_VOLTAGE",
            "RSSI_DEVICE",
            "RSSI_PEER",
            "SABOTAGE",
        ),
        2: ("BATTERY_STATE",),
        4: ("BATTERY_STATE",),
    },
    ED_DEVICE_DEFINITIONS: {
        EntityDefinition.IP_COVER: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 1,
                ED_SECONDARY_CHANNELS: (2, 3),
                ED_REPEATABLE_FIELDS: {
                    FIELD_LEVEL: "LEVEL",
                    FIELD_LEVEL_2: "LEVEL_2",
                    FIELD_STOP: "STOP",
                },
                ED_FIELDS: {
                    0: {
                        FIELD_DIRECTION: "ACTIVITY_STATE",
                        FIELD_CHANNEL_LEVEL: "LEVEL",
                        FIELD_CHANNEL_LEVEL_2: "LEVEL_2",
                        FIELD_CHANNEL_OPERATION_MODE: "CHANNEL_OPERATION_MODE",
                    },
                },
            },
        },
        EntityDefinition.IP_DIMMER: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 1,
                ED_SECONDARY_CHANNELS: (2, 3),
                ED_REPEATABLE_FIELDS: {
                    FIELD_LEVEL: "LEVEL",
                    FIELD_ON_TIME_VALUE: "ON_TIME",
                    FIELD_RAMP_TIME_VALUE: "RAMP_TIME",
                },
                ED_VISIBLE_FIELDS: {
                    0: {
                        FIELD_CHANNEL_LEVEL: "LEVEL",
                    },
                },
            },
        },
        EntityDefinition.IP_GARAGE: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_DOOR_COMMAND: "DOOR_COMMAND",
                    FIELD_SECTION: "SECTION",
                },
                ED_VISIBLE_REPEATABLE_FIELDS: {
                    FIELD_DOOR_STATE: "DOOR_STATE",
                },
            },
            ED_ADDITIONAL_ENTITIES: {
                1: ("STATE",),
            },
        },
        EntityDefinition.IP_FIXED_COLOR_LIGHT: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 1,
                ED_SECONDARY_CHANNELS: (2, 3),
                ED_REPEATABLE_FIELDS: {
                    FIELD_COLOR: "COLOR",
                    FIELD_LEVEL: "LEVEL",
                    FIELD_ON_TIME_UNIT: "DURATION_UNIT",
                    FIELD_ON_TIME_VALUE: "DURATION_VALUE",
                    FIELD_RAMP_TIME_UNIT: "RAMP_TIME_UNIT",
                    FIELD_RAMP_TIME_VALUE: "RAMP_TIME_VALUE",
                },
                ED_VISIBLE_FIELDS: {
                    0: {
                        FIELD_CHANNEL_COLOR: "COLOR",
                        FIELD_CHANNEL_LEVEL: "LEVEL",
                    },
                },
            },
        },
        EntityDefinition.IP_SIMPLE_FIXED_COLOR_LIGHT: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_COLOR: "COLOR",
                    FIELD_LEVEL: "LEVEL",
                    FIELD_ON_TIME_UNIT: "DURATION_UNIT",
                    FIELD_ON_TIME_VALUE: "DURATION_VALUE",
                    FIELD_RAMP_TIME_UNIT: "RAMP_TIME_UNIT",
                    FIELD_RAMP_TIME_VALUE: "RAMP_TIME_VALUE",
                },
            },
        },
        EntityDefinition.IP_SWITCH: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 1,
                ED_SECONDARY_CHANNELS: (2, 3),
                ED_REPEATABLE_FIELDS: {
                    FIELD_STATE: "STATE",
                    FIELD_ON_TIME_VALUE: "ON_TIME",
                },
                ED_VISIBLE_FIELDS: {
                    0: {
                        FIELD_CHANNEL_STATE: "STATE",
                    },
                },
            },
            ED_ADDITIONAL_ENTITIES: {
                4: (
                    "CURRENT",
                    "ENERGY_COUNTER",
                    "FREQUENCY",
                    "POWER",
                    "ACTUAL_TEMPERATURE",
                    "VOLTAGE",
                ),
            },
        },
        EntityDefinition.IP_LOCK: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 1,
                ED_REPEATABLE_FIELDS: {
                    FIELD_DIRECTION: "ACTIVITY_STATE",
                    FIELD_LOCK_STATE: "LOCK_STATE",
                    FIELD_LOCK_TARGET_LEVEL: "LOCK_TARGET_LEVEL",
                },
                ED_FIELDS: {
                    0: {
                        FIELD_ERROR: "ERROR_JAMMED",
                    },
                },
            },
        },
        EntityDefinition.IP_SIREN: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 3,
                ED_REPEATABLE_FIELDS: {
                    FIELD_ACOUSTIC_ALARM_ACTIVE: "ACOUSTIC_ALARM_ACTIVE",
                    FIELD_OPTICAL_ALARM_ACTIVE: "OPTICAL_ALARM_ACTIVE",
                    FIELD_ACOUSTIC_ALARM_SELECTION: "ACOUSTIC_ALARM_SELECTION",
                    FIELD_OPTICAL_ALARM_SELECTION: "OPTICAL_ALARM_SELECTION",
                    FIELD_DURATION: "DURATION_VALUE",
                    FIELD_DURATION_UNIT: "DURATION_UNIT",
                },
            },
        },
        EntityDefinition.IP_THERMOSTAT: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_ACTIVE_PROFILE: "ACTIVE_PROFILE",
                    FIELD_BOOST_MODE: "BOOST_MODE",
                    FIELD_CONTROL_MODE: "CONTROL_MODE",
                    FIELD_HEATING_COOLING: "HEATING_COOLING",
                    FIELD_PARTY_MODE: "PARTY_MODE",
                    FIELD_SETPOINT: "SET_POINT_TEMPERATURE",
                    FIELD_SET_POINT_MODE: "SET_POINT_MODE",
                    FIELD_TEMPERATURE_MAXIMUM: "TEMPERATURE_MAXIMUM",
                    FIELD_TEMPERATURE_MINIMUM: "TEMPERATURE_MINIMUM",
                },
                ED_VISIBLE_REPEATABLE_FIELDS: {
                    FIELD_HUMIDITY: "HUMIDITY",
                    FIELD_TEMPERATURE: "ACTUAL_TEMPERATURE",
                },
                ED_VISIBLE_FIELDS: {
                    0: {
                        FIELD_LEVEL: "LEVEL",
                    },
                    8: {
                        FIELD_STATE: "STATE",
                    },
                },
            },
        },
        EntityDefinition.IP_THERMOSTAT_GROUP: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_ACTIVE_PROFILE: "ACTIVE_PROFILE",
                    FIELD_BOOST_MODE: "BOOST_MODE",
                    FIELD_CONTROL_MODE: "CONTROL_MODE",
                    FIELD_HEATING_COOLING: "HEATING_COOLING",
                    FIELD_PARTY_MODE: "PARTY_MODE",
                    FIELD_SETPOINT: "SET_POINT_TEMPERATURE",
                    FIELD_SET_POINT_MODE: "SET_POINT_MODE",
                    FIELD_TEMPERATURE_MAXIMUM: "TEMPERATURE_MAXIMUM",
                    FIELD_TEMPERATURE_MINIMUM: "TEMPERATURE_MINIMUM",
                },
                ED_VISIBLE_REPEATABLE_FIELDS: {
                    FIELD_HUMIDITY: "HUMIDITY",
                    FIELD_TEMPERATURE: "ACTUAL_TEMPERATURE",
                },
                ED_FIELDS: {
                    0: {
                        FIELD_LEVEL: "LEVEL",
                    },
                    3: {
                        FIELD_STATE: "STATE",
                    },
                },
            },
            ED_INCLUDE_DEFAULT_ENTITIES: False,
        },
        EntityDefinition.RF_COVER: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_DIRECTION: "DIRECTION",
                    FIELD_LEVEL: "LEVEL",
                    FIELD_LEVEL_2: "LEVEL_SLATS",
                    FIELD_STOP: "STOP",
                },
            },
        },
        EntityDefinition.RF_DIMMER: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_LEVEL: "LEVEL",
                    FIELD_ON_TIME_VALUE: "ON_TIME",
                    FIELD_RAMP_TIME_VALUE: "RAMP_TIME",
                },
            },
        },
        EntityDefinition.RF_DIMMER_COLOR: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_LEVEL: "LEVEL",
                    FIELD_ON_TIME_VALUE: "ON_TIME",
                    FIELD_RAMP_TIME_VALUE: "RAMP_TIME",
                },
                ED_FIELDS: {
                    1: {
                        FIELD_COLOR: "COLOR",
                    },
                    2: {
                        FIELD_PROGRAM: "PROGRAM",
                    },
                },
            },
        },
        EntityDefinition.RF_DIMMER_COLOR_TEMP: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_LEVEL: "LEVEL",
                    FIELD_ON_TIME_VALUE: "ON_TIME",
                    FIELD_RAMP_TIME_VALUE: "RAMP_TIME",
                },
                ED_FIELDS: {
                    1: {
                        FIELD_COLOR_LEVEL: "LEVEL",
                    },
                },
            },
        },
        EntityDefinition.RF_DIMMER_WITH_VIRT_CHANNEL: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_SECONDARY_CHANNELS: (1, 2),
                ED_REPEATABLE_FIELDS: {
                    FIELD_LEVEL: "LEVEL",
                    FIELD_ON_TIME_VALUE: "ON_TIME",
                    FIELD_RAMP_TIME_VALUE: "RAMP_TIME",
                },
            },
        },
        EntityDefinition.RF_LOCK: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_DIRECTION: "DIRECTION",
                    FIELD_OPEN: "OPEN",
                    FIELD_STATE: "STATE",
                    FIELD_ERROR: "ERROR",
                },
            },
        },
        EntityDefinition.RF_SWITCH: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_STATE: "STATE",
                    FIELD_ON_TIME_VALUE: "ON_TIME",
                },
            },
            ED_ADDITIONAL_ENTITIES: {
                1: (
                    "CURRENT",
                    "ENERGY_COUNTER",
                    "FREQUENCY",
                    "POWER",
                    "VOLTAGE",
                ),
            },
        },
        EntityDefinition.RF_THERMOSTAT: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_AUTO_MODE: "AUTO_MODE",
                    FIELD_BOOST_MODE: "BOOST_MODE",
                    FIELD_COMFORT_MODE: "COMFORT_MODE",
                    FIELD_CONTROL_MODE: "CONTROL_MODE",
                    FIELD_LOWERING_MODE: "LOWERING_MODE",
                    FIELD_MANU_MODE: "MANU_MODE",
                    FIELD_SETPOINT: "SET_TEMPERATURE",
                    FIELD_TEMPERATURE_MAXIMUM: "TEMPERATURE_MAXIMUM",
                    FIELD_TEMPERATURE_MINIMUM: "TEMPERATURE_MINIMUM",
                },
                ED_VISIBLE_REPEATABLE_FIELDS: {
                    FIELD_HUMIDITY: "ACTUAL_HUMIDITY",
                    FIELD_TEMPERATURE: "ACTUAL_TEMPERATURE",
                },
                ED_VISIBLE_FIELDS: {
                    0: {
                        FIELD_VALVE_STATE: "VALVE_STATE",
                    },
                },
            },
        },
        EntityDefinition.RF_THERMOSTAT_GROUP: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_REPEATABLE_FIELDS: {
                    FIELD_AUTO_MODE: "AUTO_MODE",
                    FIELD_BOOST_MODE: "BOOST_MODE",
                    FIELD_COMFORT_MODE: "COMFORT_MODE",
                    FIELD_CONTROL_MODE: "CONTROL_MODE",
                    FIELD_LOWERING_MODE: "LOWERING_MODE",
                    FIELD_MANU_MODE: "MANU_MODE",
                    FIELD_SETPOINT: "SET_TEMPERATURE",
                    FIELD_TEMPERATURE_MAXIMUM: "TEMPERATURE_MAXIMUM",
                    FIELD_TEMPERATURE_MINIMUM: "TEMPERATURE_MINIMUM",
                },
                ED_VISIBLE_REPEATABLE_FIELDS: {
                    FIELD_HUMIDITY: "ACTUAL_HUMIDITY",
                    FIELD_TEMPERATURE: "ACTUAL_TEMPERATURE",
                },
                ED_FIELDS: {
                    0: {
                        FIELD_VALVE_STATE: "VALVE_STATE",
                    },
                },
            },
            ED_INCLUDE_DEFAULT_ENTITIES: False,
        },
        EntityDefinition.SIMPLE_RF_THERMOSTAT: {
            ED_DEVICE_GROUP: {
                ED_PRIMARY_CHANNEL: 0,
                ED_VISIBLE_REPEATABLE_FIELDS: {
                    FIELD_HUMIDITY: "HUMIDITY",
                    FIELD_TEMPERATURE: "TEMPERATURE",
                },
                ED_FIELDS: {
                    1: {
                        FIELD_SETPOINT: "SETPOINT",
                    },
                },
            },
        },
    },
}


def validate_entity_definition() -> Any:
    """Validate the entity_definition."""
    try:
        return SCHEMA_DEVICE_DESCRIPTION(entity_definition)
    except vol.Invalid as err:  # pragma: no cover
        _LOGGER.error("The entity definition could not be validated. %s, %s", err.path, err.msg)
        return None


def make_custom_entity(
    device: hmd.HmDevice,
    custom_entity_class: type,
    device_enum: EntityDefinition,
    group_base_channels: tuple[int, ...],
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """
    Create custom_entities.

    We use a helper-function to avoid raising exceptions during object-init.
    """
    entities: list[hme.BaseEntity] = []

    entity_def = _get_device_entities(device_enum, group_base_channels[0])

    for base_channel in group_base_channels:
        device_def = _get_device_group(device_enum, base_channel)
        channels = [device_def[ED_PRIMARY_CHANNEL]]
        if secondary_channels := device_def.get(ED_SECONDARY_CHANNELS):
            channels.extend(secondary_channels)
        for channel_no in set(channels):
            entities.extend(
                _create_entities(
                    device=device,
                    custom_entity_class=custom_entity_class,
                    device_enum=device_enum,
                    device_def=device_def,
                    entity_def=entity_def,
                    channel_no=channel_no,
                    extended=extended,
                )
            )

    return tuple(entities)


def _create_entities(
    device: hmd.HmDevice,
    custom_entity_class: type,
    device_enum: EntityDefinition,
    device_def: dict[str, vol.Any],
    entity_def: dict[int, tuple[str, ...]],
    channel_no: int | None = None,
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """Create custom entities."""
    entities: list[hme.BaseEntity] = []
    unique_identifier = generate_unique_identifier(
        central=device.central, address=f"{device.device_address}:{channel_no}"
    )
    if f"{device.device_address}:{channel_no}" not in device.channels:
        return tuple(entities)
    entity = custom_entity_class(
        device=device,
        unique_identifier=unique_identifier,
        device_enum=device_enum,
        device_def=device_def,
        entity_def=entity_def,
        channel_no=channel_no,
        extended=extended,
    )
    if len(entity.data_entities) > 0:
        device.add_entity(entity)
        entities.append(entity)
    return tuple(entities)


def get_default_entities() -> dict[int | tuple[int, ...], tuple[str, ...]]:
    """Return the default entities."""
    return deepcopy(entity_definition[ED_DEFAULT_ENTITIES])  # type: ignore[arg-type]


def get_include_default_entities(device_enum: EntityDefinition) -> bool:
    """Return if default entities should be included."""
    device = _get_device_definition(device_enum)
    return device.get(ED_INCLUDE_DEFAULT_ENTITIES, DEFAULT_INCLUDE_DEFAULT_ENTITIES)


def _get_device_definition(device_enum: EntityDefinition) -> dict[str, vol.Any]:
    """Return device from entity definitions."""
    return cast(
        dict[str, vol.Any], deepcopy(entity_definition[ED_DEVICE_DEFINITIONS][device_enum])
    )


def _get_device_group(device_enum: EntityDefinition, base_channel_no: int) -> dict[str, vol.Any]:
    """Return the device group."""
    device = _get_device_definition(device_enum)
    group = cast(dict[str, vol.Any], deepcopy(device[ED_DEVICE_GROUP]))
    if group and base_channel_no == 0:
        return group

    # Add base_channel_no to the primary_channel to get the real primary_channel number
    primary_channel = group[ED_PRIMARY_CHANNEL]
    group[ED_PRIMARY_CHANNEL] = primary_channel + base_channel_no

    # Add base_channel_no to the secondary_channels
    # to get the real secondary_channel numbers
    if secondary_channel := group.get(ED_SECONDARY_CHANNELS):
        group[ED_SECONDARY_CHANNELS] = [x + base_channel_no for x in secondary_channel]

    group[ED_VISIBLE_FIELDS] = _rebase_entity_dict(
        entity_dict=ED_VISIBLE_FIELDS, group=group, base_channel_no=base_channel_no
    )
    group[ED_FIELDS] = _rebase_entity_dict(
        entity_dict=ED_FIELDS, group=group, base_channel_no=base_channel_no
    )
    return group


def _rebase_entity_dict(
    entity_dict: str, group: dict[str, vol.Any], base_channel_no: int
) -> dict[int, vol.Any]:
    """Rebase entity_dict with base_channel_no."""
    new_fields = {}
    if fields := group.get(entity_dict):
        for channel_no, field in fields.items():
            new_fields[channel_no + base_channel_no] = field
    return new_fields


def _get_device_entities(
    device_enum: EntityDefinition, base_channel_no: int
) -> dict[int, tuple[str, ...]]:
    """Return the device entities."""
    additional_entities = (
        entity_definition[ED_DEVICE_DEFINITIONS]
        .get(device_enum, {})
        .get(ED_ADDITIONAL_ENTITIES, {})
    )
    new_entities: dict[int, tuple[str, ...]] = {}
    if additional_entities:
        for channel_no, field in deepcopy(additional_entities).items():
            new_entities[channel_no + base_channel_no] = field
    return new_entities


@dataclass
class CustomConfig:
    """Data for custom entity creation."""

    func: Callable
    channels: tuple[int, ...]
    extended: ExtendedConfig | None = None


@dataclass
class ExtendedConfig:
    """Extended data for custom entity creation."""

    fixed_channels: dict[int, dict[str, str]] | None = None
    additional_entities: dict[int | tuple[int, ...], tuple[str, ...]] | None = None

    @property
    def required_parameters(self) -> tuple[str, ...]:
        """Return vol.Required parameters from extended config."""
        required_parameters: list[str] = []
        if fixed_channels := self.fixed_channels:
            for mapping in fixed_channels.values():
                required_parameters.extend(mapping.values())

        if additional_entities := self.additional_entities:
            for parameters in additional_entities.values():
                required_parameters.extend(parameters)

        return tuple(required_parameters)
