from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_URL
from homeassistant.core import HomeAssistant, CALLBACK_TYPE
from homeassistant.helpers import device_registry as registry
import unfoldedcircle.device as uc

import logging

from .const import DOMAIN, PLATFORMS, DEVICE_MODEL, DEVICE_MANUFACTURER

_LOGGER = logging.getLogger(__name__)


class UnfoldedCircleDevice:
    def __init__(self, hass, config):
        self.hass: HomeAssistant = hass
        self.config = config
        self.device_name: str = None
        self.api: uc.Device = None
        self.reset_jobs: list[CALLBACK_TYPE] = []

    @property
    def name(self):
        return self.api.name

    @property
    def unique_id(self):
        return self.config.unique_id

    @property
    def serial(self):
        # @fixme
        return self.config.unique_id

    @property
    def endpoint(self) -> str:
        return self.api.endpoint

    @property
    def model_type(self):
        # @fixme
        return DEVICE_MODEL

    @staticmethod
    async def async_update(hass: HomeAssistant, config: ConfigEntry) -> None:
        """Update the device and related entities.

        Triggered when the device is renamed on the frontend.
        """
        device_registry = registry.async_get(hass)
        assert config.unique_id
        device_entry = device_registry.async_get_device(
            identifiers={(DOMAIN, config.unique_id)}
        )
        assert device_entry
        device_registry.async_update_device(device_entry.id, name=config.title)
        await hass.config_entries.async_reload(config.entry_id)

    def _get_device_name(self) -> int | None:
        """Fetch device name."""
        return self.api.info()["device_name"]

    async def async_setup(self) -> bool:
        """Set up the device and related entities."""
        config = self.config
        hass = self.hass
        endpoint = config.data.get(CONF_URL)
        apikey = config.data.get(CONF_API_KEY)
        self.api = uc.Device(endpoint, apikey)

        try:
            self.device_name = await hass.async_add_executor_job(
                self._get_device_name
            )
        except uc.HTTPError:
            await self._async_handle_http_error()
            return False

        hass.data[DOMAIN].devices[config.entry_id] = self
        self.reset_jobs.append(config.add_update_listener(self.async_update))

        # Forward entry setup to entity platforms
        for platform in PLATFORMS:
            hass.async_add_job(
                self.hass.config_entries.async_forward_entry_setup(
                    config, platform
                )
            )

        return True

    async def async_unload(self) -> bool:
        """Unload the device and related entities."""

        while self.reset_jobs:
            self.reset_jobs.pop()()

        return await self.hass.config_entries.async_unload_platforms(
            self.config, PLATFORMS
        )

    async def _async_handle_http_error(self) -> None:
        """Handle a HTTP error."""

        _LOGGER.error("Unable to connect to %s.", self.name)

    def device_info(self) -> registry.DeviceInfo:
        """Return the device info."""
        return registry.DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self.unique_id)
            },
            name=self.name,
            manufacturer=DEVICE_MANUFACTURER,
            model=DEVICE_MODEL,
            sw_version=self.api.info().get("api"),
        )
