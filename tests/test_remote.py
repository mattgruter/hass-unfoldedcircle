from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import Mock
import unfoldedcircle.device as uc

from custom_components.unfoldedcircle.remote import UCRemoteTwoRemote


async def test_state_always_on():
    """Tests a failed async_update."""
    device = Mock()
    device.unique_id = "foo"
    api = Mock()
    api.endpoint = "bar"

    remote = UCRemoteTwoRemote(device, api)
    assert remote.state == "on"
    assert remote.activity_list is None


async def test_async_update(hass: HomeAssistant):
    """Tests an async_update."""
    test_activities = ["Watch TV", "Listen to Spotify"]
    device = Mock()
    device.unique_id = "foo"
    api = Mock()
    api.endpoint = "bar"
    api.fetch_activities = Mock(
        return_value=[{"name": {"en": a}} for a in test_activities]
    )
    remote = UCRemoteTwoRemote(device, api)
    remote.hass = hass

    await remote.async_update()
    assert remote.activity_list == test_activities


async def test_async_update_failed(hass: HomeAssistant):
    """Tests a failed async_update."""
    device = Mock()
    device.unique_id = "foo"
    api = Mock()
    api.endpoint = "bar"
    api.fetch_activities = Mock(side_effect=uc.HTTPError("mock error"))
    remote = UCRemoteTwoRemote(device, api)
    remote.hass = hass

    await remote.async_update()
    assert remote.available is False
