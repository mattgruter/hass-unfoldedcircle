"""Config flow for Unfolded Circle integration."""
import logging
from typing import Dict

from homeassistant import config_entries
from homeassistant.components.zeroconf import ZeroconfServiceInfo
from homeassistant.const import (
    CONF_API_KEY,
    CONF_NAME,
    CONF_PIN,
    CONF_TYPE,
    CONF_URL,
)
import unfoldedcircle.device as uc
import voluptuous as vol

from .const import AUTH_APIKEY_NAME, AUTH_APIKEY_SCOPES, DEVICE_MODEL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class UnfoldedCircleConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Gardena."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        self.api: uc.Device = None

    async def async_setup_api(self, endpoint, unique_id):
        await self.async_set_unique_id(unique_id, raise_on_progress=True)
        self._abort_if_unique_id_configured(updates={CONF_URL: endpoint})

        self.api = uc.Device(endpoint)
        device_info = await self.hass.async_add_executor_job(self.api.info)
        if not device_info:
            raise uc.HTTPError("can't fetch device info")

    async def async_login(self):
        apikey = await self.hass.async_add_executor_job(
            self.api.add_apikey,
            AUTH_APIKEY_NAME,
            AUTH_APIKEY_SCOPES,
        )

        if not apikey:
            raise uc.HTTPError("can't create API key")
        return apikey

    async def async_step_zeroconf(self, discovery_info: ZeroconfServiceInfo):
        """Handle zeroconf discovery."""
        host = discovery_info.ip_address
        port = discovery_info.port
        endpoint = f"http://{host}:{port}/api/"
        unique_id = endpoint

        try:
            await self.async_setup_api(endpoint, unique_id)
        except uc.HTTPError:
            return self.async_abort(reason="cannot_connect")
        else:
            _LOGGER.debug("Unfolded Circle Device discovered: %s", endpoint)

        return await self.async_step_auth()

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            endpoint = user_input[CONF_URL]
            unique_id = endpoint
            try:
                await self.async_setup_api(endpoint, unique_id)
            except uc.HTTPError:
                errors["base"] = "connection"
            else:
                return await self.async_step_auth()

        endpoint_schema = vol.Schema({vol.Required(CONF_URL): str})
        return self.async_show_form(
            step_id="user",
            data_schema=endpoint_schema,
            errors=errors,
        )

    async def async_step_auth(self, user_input=None):
        """Provide PIN code in order to authenticate and create an API key."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            pin = user_input[CONF_PIN]
            self.api.pin = pin
            try:
                apikey = await self.async_login()
            except uc.HTTPError:
                errors["base"] = "connection"
            except uc.AuthenticationError:
                errors["base"] = "auth"
            else:
                self.api.apikey = apikey
                return await self.async_step_finish()

        auth_schema = vol.Schema({vol.Required(CONF_PIN): str})
        return self.async_show_form(
            step_id="auth",
            data_schema=auth_schema,
            errors=errors,
        )

    async def async_step_finish(self, user_input=None):
        """Choose a name for the device and create config entry."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={
                    CONF_URL: self.api.endpoint,
                    CONF_API_KEY: self.api.apikey,
                    CONF_TYPE: DEVICE_MODEL[0],  # @fixme
                },
            )

        name_schema = vol.Schema(
            {vol.Required(CONF_NAME, default=self.api.name): str}
        )
        return self.async_show_form(
            step_id="finish",
            data_schema=name_schema,
            errors=errors,
        )


# async def try_connection(client_url, client_apikey):
#     _LOGGER.debug("Trying to connect to Unfolded Circle device during setup")
#     uc_device = uc.Device(endpoint=client_url, apikey=client_apikey)
#     await uc_device.info()
#     await uc_device.fetch_remotes()
#     _LOGGER.debug(
#         "Successfully connected to Unfolded Circle device during setup"
#     )
