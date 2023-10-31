# hass-unfoldedcircle

Home Assistant integration for the [Unfolde Circle Remote Two](https://www.unfoldedcircle.com/).

Use this component to send IR commands with the Remote Two.

## Installation

1. Install this component by copying it to the `custom_components` directory of your Home Assistant's confg directory.
1. Restart Home Assistant.
1. Your remote will be auto-discovered. Go to `Settings` > `Devices & services` to configure it. It will ask for the PIN shown on your remote during setup.

   Note: If you're device wasn't discovered you can manually enter the endpoint URL of your remote, e.g. `http://192.168.1.17/api/`

## Usage

Once configured, the integration creates a device and a `remote` entry that can be used with the `remote.send_command` service.

## Development

The component uses the [python-unfoldedcircle](https://github.com/mattgruter/python-unfoldedcircle) library to communicate with the remote. The library is wrapper over the remote's [REST API](https://github.com/unfoldedcircle/core-api).

## Ideas for the future

- **RF & Bluetooth commands**

  The Remote Two's roadmap includes sending RF and Bluetooth commands. Once this feature has been rolled out and is available through its API, this component's `remote.send_command` could include sending commands over IR, RF and Bluetooth.

- **Activities**

  The Remote Two supports activities that combine IR, RF, Bluetooth and other integrations. Once its API supports turning on and off activities, we can add support for them in this component.

- **Firmware update**

  The Remote Two's firmware can be updated throught its API. This component could expose the remote's firmware through a `update` entity.

- **Remote UI control**

  If the Remote Two's API were to support controlling what's shown on the remote's UI, this component could be used to make the remote more context-aware: automatically switch to the correct music device when a stream starts or switch to a different UI page when the remote is moved to another room, etc. We'll follow the progress of this [feature request](https://github.com/unfoldedcircle/feature-and-bug-tracker/issues/108) to understand if this might be possible in the future.
