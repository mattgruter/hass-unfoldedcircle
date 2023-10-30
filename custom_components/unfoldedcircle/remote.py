"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.components.remote import RemoteEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import unfoldedcircle.device as uc

from .const import DOMAIN
from .device import UnfoldedCircleDevice

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the RemoteTwo remote."""
    device = hass.data[DOMAIN].devices[config.entry_id]
    remotes = [UCRemoteTwoRemote(device, api=device.api)]
    async_add_entities(remotes, update_before_add=True)


class UCRemoteTwoRemote(RemoteEntity):
    """Representation of an Unfolded Circle Remote Two remote."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device: UnfoldedCircleDevice, api: uc.Device):
        """Initialize the sensor."""
        super().__init__()
        self.device = device
        self.api = api
        self.endpoint = self.api.endpoint
        self._available = True
        self._attr_is_on = True
        self._attr_unique_id = self.device.unique_id

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the remote."""
        # @fixme: return serial number instead
        return self.endpoint

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    async def async_update(self) -> None:
        try:
            activities = await self.hass.async_add_executor_job(
                self.api.fetch_activities
            )
        except uc.HTTPError:
            _LOGGER.exception(
                "Error retrieving data from UnfoldedCircle device %s", self.name
            )
        self._attr_activity_list = [a["name"]["en"] for a in activities]

    async def async_turn_on(self, activity: str = None, **kwargs):
        """Send the power on command."""
        _LOGGER.error("Remote turned on activity %s", activity)
        self._attr_current_activity = activity

    async def async_toggle(self, activity: str = None, **kwargs):
        """Toggle a device."""
        _LOGGER.error("Remote toggled activity %s", activity)

    async def async_turn_off(self, activity: str = None, **kwargs):
        """Send the power off command."""
        _LOGGER.error("Remote turned off activity %s", activity)
        self._attr_current_activity = None

    async def async_send_command(self, command, **kwargs):
        """Send commands to a device."""
        _LOGGER.error("Remote sent command %s", command)

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return self.device.device_info()
