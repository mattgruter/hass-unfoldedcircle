from dataclasses import dataclass, field
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, PLATFORMS
from .device import UnfoldedCircleDevice


_LOGGER = logging.getLogger(__name__)


@dataclass
class UnfoldedCircleData:
    """Class to hold shared data to be used by the UC integration."""

    devices: dict[str, UnfoldedCircleDevice] = field(default_factory=dict)
    platforms: dict = field(default_factory=dict)


async def async_setup(hass: HomeAssistant, config: ConfigEntry) -> bool:
    """Set up the Unfolded Circle integration."""
    hass.data[DOMAIN] = UnfoldedCircleData()
    return True


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry) -> bool:
    """Set up a Broadlink device from a config entry."""
    data: UnfoldedCircleData = hass.data[DOMAIN]
    device = UnfoldedCircleDevice(hass, config)

    if config.entry_id in data.devices:
        _LOGGER.error("Device %s already setup.", device.endpoint)
        return False
    if not await device.async_setup():
        return False
    return True


async def async_unload_entry(hass: HomeAssistant, config: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        config, PLATFORMS
    ):
        hass.data[DOMAIN].devices.pop(config.entry_id)

    return unload_ok
