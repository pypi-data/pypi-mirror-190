"""
Module for entities implemented using the sensor platform.

See https://www.home-assistant.io/integrations/sensor/.
"""
from __future__ import annotations

import logging
from typing import Any

from hahomematic.const import SYSVAR_TYPE_LIST, HmPlatform
from hahomematic.decorators import value_property
from hahomematic.entity import GenericEntity, GenericSystemVariable

_LOGGER = logging.getLogger(__name__)


class HmSensor(GenericEntity[Any]):
    """
    Implementation of a sensor.

    This is a default platform that gets automatically generated.
    """

    _attr_platform = HmPlatform.SENSOR

    @value_property
    def value(self) -> Any | None:
        """Return the value."""
        if self._attr_value is not None and self._attr_value_list is not None:
            return self._attr_value_list[int(self._attr_value)]
        if convert_func := self._get_converter_func():
            return convert_func(self._attr_value)
        return self._attr_value

    def _get_converter_func(self) -> Any:
        """Return a converter based on sensor."""
        if convert_func := CONVERTERS_BY_PARAM.get(self.parameter):
            return convert_func
        return None


def _fix_rssi(value: Any) -> int | None:
    """
    Fix rssi value.

    See https://github.com/danielperna84/hahomematic/blob/devel/docs/rssi_fix.md.
    """
    if value is None or not isinstance(value, int):
        return None
    if -127 < value < 0:
        return value
    if 1 < value < 127:
        return value * -1
    if -256 < value < -129:
        return (value * -1) - 256
    if 129 < value < 256:
        return value - 256
    return None


class HmSysvarSensor(GenericSystemVariable):
    """Implementation of a sysvar sensor."""

    _attr_platform = HmPlatform.HUB_SENSOR

    @value_property
    def value(self) -> Any | None:
        """Return the value."""
        if (
            self.data_type == SYSVAR_TYPE_LIST
            and self._attr_value is not None
            and self.value_list is not None
        ):
            return self.value_list[int(self._attr_value)]
        return _check_length_and_warn(name=self.ccu_var_name, value=self._attr_value)


CONVERTERS_BY_PARAM: dict[str, Any] = {
    "RSSI_PEER": _fix_rssi,
    "RSSI_DEVICE": _fix_rssi,
}


def _check_length_and_warn(name: str | None, value: Any) -> Any:
    """Check the length of a variable and warn if too long."""
    if isinstance(value, str) and len(value) > 255:
        _LOGGER.warning(
            "Value of sysvar %s exceedes maximum allowed length of "
            "255 chars by Home Assistant. Value will be limited to 255 chars",
            name,
        )
        return value[0:255:1]
    return value
