"""Constants for the Unfolded Circle integration."""

from homeassistant.const import Platform

DOMAIN = "unfoldedcircle"

DEVICE_MANUFACTURER = "Unfolded Circle"
DEVICE_MODEL = "ucr2"

CONF_API_KEY_NAME = "api_key_name"

AUTH_APIKEY_NAME_PREFIX = "hass-unfoldedcircle"
AUTH_APIKEY_SCOPES = ["admin"]

PLATFORMS = [
    Platform.REMOTE,
]
