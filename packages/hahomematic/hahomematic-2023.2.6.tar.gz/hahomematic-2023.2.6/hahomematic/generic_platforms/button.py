"""
Module for entities implemented using the button platform.

See https://www.home-assistant.io/integrations/boton/.
"""
from __future__ import annotations

from typing import Final

import hahomematic.central_unit as hmcu
from hahomematic.const import PROGRAM_ADDRESS, HmPlatform
from hahomematic.decorators import value_property
from hahomematic.entity import GenericEntity, GenericHubEntity
from hahomematic.helpers import HubData, ProgramData


class HmButton(GenericEntity[None]):
    """
    Implementation of a button.

    This is a default platform that gets automatically generated.
    """

    _attr_platform = HmPlatform.BUTTON

    async def press(self) -> None:
        """Handle the button press."""
        await self.send_value(value=True)


class HmProgramButton(GenericHubEntity):
    """Class for a HomeMatic program button."""

    _attr_platform = HmPlatform.HUB_BUTTON

    def __init__(
        self,
        central: hmcu.CentralUnit,
        data: ProgramData,
    ) -> None:
        """Initialize the entity."""
        super().__init__(
            central=central,
            address=PROGRAM_ADDRESS,
            data=data,
        )
        self.pid: Final[str] = data.pid
        self.ccu_program_name: Final[str] = data.name
        self.is_active: bool = data.is_active
        self.is_internal: bool = data.is_internal
        self.last_execute_time: str = data.last_execute_time

    @value_property
    def available(self) -> bool:
        """Return the availability of the device."""
        return self.is_active

    def get_name(self, data: HubData) -> str:
        """Return the name of the program button entity."""
        if data.name.lower().startswith(tuple({"p_", "prg_"})):
            return data.name.title()
        return f"P_{data.name}".title()

    def update_data(self, data: ProgramData) -> None:
        """Set variable value on CCU/Homegear."""
        do_update: bool = False
        if self.is_active != data.is_active:
            self.is_active = data.is_active
            do_update = True
        if self.is_internal != data.is_internal:
            self.is_internal = data.is_internal
            do_update = True
        if self.last_execute_time != data.last_execute_time:
            self.last_execute_time = data.last_execute_time
            do_update = True
        if do_update:
            self.update_entity()

    async def press(self) -> None:
        """Handle the button press."""
        await self.central.execute_program(pid=self.pid)
