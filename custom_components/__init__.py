import logging
from homeassistant.helpers import discovery

_LOGGER = logging.getLogger(__name__)

DOMAIN = "wyze_thermostat"

def setup(hass, config):
    """Set up the Wyze Thermostat component."""
    _LOGGER.info("Setting up Wyze Thermostat component")

    # Discover and load platforms
    hass.helpers.discovery.load_platform('climate', DOMAIN, {}, config)
    return True
