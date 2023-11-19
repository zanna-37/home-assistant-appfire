"""Platform for number integration."""
from __future__ import annotations

from homeassistant.components.number import (
    NumberEntity,
)

import logging

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .coordinator import MyCoordinator

from .const import DOMAIN
from .const import API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number entity."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([DesiredAmbientTemperature(coordinator)])


class DesiredAmbientTemperature(CoordinatorEntity, NumberEntity):
    _attr_icon = "mdi:thermometer"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator: MyCoordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(
            coordinator, context=API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE
        )
        self._idx = API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE

        self._attr_name = (
            self.coordinator.getStoveNameOrSerial() + " desired ambient temperature"
        )
        self._attr_unique_id = (
            self.coordinator.stoveSerial + "_number" + "_desired_ambient_temperature"
        )

    @property
    def native_min_value(self) -> float:
        """Return the minimum value."""
        return 10

    @property
    def native_max_value(self) -> float:
        """Return the maximum value."""
        return 50

    @property
    def native_step(self) -> float:
        """Return the increment/decrement step."""
        return 0.1

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data[self._idx]
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Set the characteristic to this value."""
        await self.hass.async_add_executor_job(
            self.coordinator.appFireApi.setDesiredAmbientTemperature, value
        )
        await self.coordinator.async_request_refresh()
