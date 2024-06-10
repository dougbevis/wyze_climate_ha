import logging
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_OFF, HVAC_MODE_HEAT, HVAC_MODE_COOL, HVAC_MODE_HEAT_COOL,
    SUPPORT_TARGET_TEMPERATURE)
from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE
import wyzeapy

_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Wyze Thermostat platform."""
    client = wyzeapy.Client()
    thermostat = WyzeThermostat(client)
    async_add_entities([thermostat])

class WyzeThermostat(ClimateEntity):
    """Representation of a Wyze Thermostat."""

    def __init__(self, client):
        """Initialize the thermostat."""
        self._client = client
        self._name = "Wyze Thermostat"
        self._hvac_mode = HVAC_MODE_OFF
        self._target_temperature = None
        self._current_temperature = None
        self._min_temp = 7  # Minimum temperature setpoint
        self._max_temp = 35  # Maximum temperature setpoint
        self.update()

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def name(self):
        """Return the name of the thermostat."""
        return self._name

    @property
    def hvac_mode(self):
        """Return the current HVAC mode."""
        return self._hvac_mode

    @property
    def hvac_modes(self):
        """Return the list of available HVAC modes."""
        return [HVAC_MODE_OFF, HVAC_MODE_HEAT, HVAC_MODE_COOL, HVAC_MODE_HEAT_COOL]

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return self._min_temp

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return self._max_temp

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        if ATTR_TEMPERATURE in kwargs:
            self._target_temperature = kwargs[ATTR_TEMPERATURE]
            self._client.set_temperature(self._target_temperature)
            self.schedule_update_ha_state()

    def update(self):
        """Fetch new state data for the thermostat."""
        self._current_temperature = self._client.get_current_temperature()
        self._target_temperature = self._client.get_target_temperature()
        self._hvac_mode = self._client.get_hvac_mode()
