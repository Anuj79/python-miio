"""Test for Mijia Camera V1."""

import pytest

from miio import MijiaCameraV1
from miio.integrations.mijia.camera import CameraStatus, ImageRollover, NightShot

from .mijia_camera import MIOT_MAPPING, MODEL_CAMERA_MJSXJ02HL


class DummyMijiaCameraV1(MijiaCameraV1):
    """Dummy camera for testing."""

    def __init__(self, *args, **kwargs):
        self.model = MODEL_CAMERA_MJSXJ02HL
        self.state = {
            "on": True,
            "image_rollover": 0,
            "night_shot": 0,
            "time_watermark": True,
            "wdr_mode": False,
        }

    def get_properties_for_mapping(self, *, max_properties=15):
        """Return dummy properties."""
        return [
            {"did": "on", "siid": 2, "piid": 1, "code": 0, "value": self.state["on"]},
            {
                "did": "image_rollover",
                "siid": 2,
                "piid": 2,
                "code": 0,
                "value": self.state["image_rollover"],
            },
            {
                "did": "night_shot",
                "siid": 2,
                "piid": 3,
                "code": 0,
                "value": self.state["night_shot"],
            },
            {
                "did": "time_watermark",
                "siid": 2,
                "piid": 5,
                "code": 0,
                "value": self.state["time_watermark"],
            },
            {
                "did": "wdr_mode",
                "siid": 2,
                "piid": 6,
                "code": 0,
                "value": self.state["wdr_mode"],
            },
        ]

    def set_property(self, property_name, value):
        """Set property value."""
        self.state[property_name] = value
        return [{"code": 0}]


@pytest.fixture
def camera():
    """Fixture for camera."""
    return DummyMijiaCameraV1()


def test_status(camera):
    """Test status retrieval."""
    status = camera.status()
    assert isinstance(status, CameraStatus)
    assert status.is_on is True
    assert status.power == "on"
    assert status.image_rollover == ImageRollover.Normal
    assert status.night_shot == NightShot.Auto
    assert status.time_watermark is True
    assert status.wdr_mode is False


def test_on_off(camera):
    """Test power on/off."""
    camera.off()
    assert camera.state["on"] is False

    camera.on()
    assert camera.state["on"] is True


def test_set_image_rollover(camera):
    """Test setting image rollover."""
    camera.set_image_rollover(ImageRollover.UpsideDown)
    assert camera.state["image_rollover"] == 1


def test_set_night_shot(camera):
    """Test setting night shot mode."""
    camera.set_night_shot(NightShot.On)
    assert camera.state["night_shot"] == 1

    camera.set_night_shot(NightShot.Off)
    assert camera.state["night_shot"] == 2


def test_set_time_watermark(camera):
    """Test enabling/disabling time watermark."""
    camera.set_time_watermark(False)
    assert camera.state["time_watermark"] is False

    camera.set_time_watermark(True)
    assert camera.state["time_watermark"] is True


def test_set_wdr_mode(camera):
    """Test enabling/disabling WDR mode."""
    camera.set_wdr_mode(True)
    assert camera.state["wdr_mode"] is True

    camera.set_wdr_mode(False)
    assert camera.state["wdr_mode"] is False


def test_mapping():
    """Test that mapping is correct."""
    mapping = MIOT_MAPPING[MODEL_CAMERA_MJSXJ02HL]
    assert mapping["on"] == {"siid": 2, "piid": 1}
    assert mapping["image_rollover"] == {"siid": 2, "piid": 2}
    assert mapping["night_shot"] == {"siid": 2, "piid": 3}
    assert mapping["time_watermark"] == {"siid": 2, "piid": 5}
    assert mapping["wdr_mode"] == {"siid": 2, "piid": 6}
