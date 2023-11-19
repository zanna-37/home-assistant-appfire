"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .const import API_DATA_LOOKUP_POWER_PERCENTAGE
from .const import API_DATA_LOOKUP_AMBIENT_TEMPERATURE
from .const import API_DATA_LOOKUP_STOVE_STATUS


from .lib.appfire_client.status.stove_status import StoveStatus as StoveStatusApi
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor entity."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            StoveStatus(coordinator),
            PowerPercentage(coordinator),
            AmbientTemperature(coordinator),
        ]
    )


class StoveStatus(CoordinatorEntity, SensorEntity):
    _attr_native_unit_of_measurement = None
    _attr_device_class = SensorDeviceClass.ENUM

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=API_DATA_LOOKUP_STOVE_STATUS)
        self._idx = API_DATA_LOOKUP_STOVE_STATUS

        self._attr_name = self.coordinator.getStoveNameOrSerial() + " status"
        self._attr_unique_id = self.coordinator.stoveSerial + "_sensor" + "_status"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        status_code = self.coordinator.data[self._idx]
        self._attr_native_value = StoveStatusApi.statusToText(status_code)
        self.async_write_ha_state()


class PowerPercentage(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:percent"
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=API_DATA_LOOKUP_POWER_PERCENTAGE)
        self._idx = API_DATA_LOOKUP_POWER_PERCENTAGE

        self._attr_name = self.coordinator.getStoveNameOrSerial() + " power level"
        self._attr_unique_id = self.coordinator.stoveSerial + "_sensor" + "_power_level"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data[self._idx]
        self.async_write_ha_state()


class AmbientTemperature(CoordinatorEntity, SensorEntity):
    _attr_icon = "mdi:home-thermometer"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=API_DATA_LOOKUP_AMBIENT_TEMPERATURE)
        self._idx = API_DATA_LOOKUP_AMBIENT_TEMPERATURE

        self._attr_name = (
            self.coordinator.getStoveNameOrSerial() + " ambient temperature"
        )
        self._attr_unique_id = (
            self.coordinator.stoveSerial + "_sensor" + "_ambient_temperature"
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data[self._idx]
        self.async_write_ha_state()
