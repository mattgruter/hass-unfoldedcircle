"""Constants for the Unfolded Circle integration."""

from homeassistant.const import Platform

DOMAIN = "unfoldedcircle"

DEVICE_MANUFACTURER = "Unfolded Circle"
DEVICE_MODEL = "ucr2"

AUTH_APIKEY_NAME = "hass-unfoldedcircle"
AUTH_APIKEY_SCOPES = ["admin"]

PLATFORMS = [
    Platform.REMOTE,
]
