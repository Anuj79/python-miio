"""Xiaomi Mijia Camera v1 (mijia.camera.v1) support."""

import enum
import logging
from typing import Any

import click

from miio import DeviceStatus, MiotDevice
from miio.click_common import EnumType, command, format_output

_LOGGER = logging.getLogger(__name__)

MODEL_CAMERA_MJSXJ02HL = "mijia.camera.v1"

MIOT_MAPPING = {
    MODEL_CAMERA_MJSXJ02HL: {
        # Camera Control Service (siid=2)
        "on": {"siid": 2, "piid": 1},
        "image_rollover": {"siid": 2, "piid": 2},
        "night_shot": {"siid": 2, "piid": 3},
        "time_watermark": {"siid": 2, "piid": 5},
        "wdr_mode": {"siid": 2, "piid": 6},
        # P2P Stream Service (siid=5)
        "start_p2p_stream": {"siid": 5, "aiid": 1},
        "stop_p2p_stream": {"siid": 5, "aiid": 2},
        # Camera Stream for Alexa (siid=3)
        "start_rtsp_stream": {"siid": 3, "aiid": 1},
        "stop_alexa_stream": {"siid": 3, "aiid": 2},
        "get_stream_config": {"siid": 3, "aiid": 3},
        # Camera Stream for Google Home (siid=4)
        "start_hls_stream": {"siid": 4, "aiid": 1},
        "stop_google_stream": {"siid": 4, "aiid": 2},
        # Memory Card Management Service (siid=6)
        "format_sd": {"siid": 6, "aiid": 1},
        "eject_sd": {"siid": 6, "aiid": 2},
    }
}


class ImageRollover(enum.IntEnum):
    """Image rollover mode."""

    Normal = 0
    UpsideDown = 1


class NightShot(enum.IntEnum):
    """Night shot mode."""

    Auto = 0
    On = 1
    Off = 2


class CameraStatus(DeviceStatus):
    """Container for status reports from the Xiaomi Mijia Camera V1."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Response from a MijiaCameraV1 (mijia.camera.v1):

        {
          'id': 1,
          'result': [
            {'did': 'on', 'siid': 2, 'piid': 1, 'code': 0, 'value': True},
            {'did': 'image_rollover', 'siid': 2, 'piid': 2, 'code': 0, 'value': 0},
            {'did': 'night_shot', 'siid': 2, 'piid': 3, 'code': 0, 'value': 0},
            {'did': 'time_watermark', 'siid': 2, 'piid': 5, 'code': 0, 'value': True},
            {'did': 'wdr_mode', 'siid': 2, 'piid': 6, 'code': 0, 'value': False}
          ]
        }
        """
        self.data = data

    @property
    def is_on(self) -> bool:
        """True if the camera is on."""
        return self.data["on"]

    @property
    def power(self) -> str:
        """Power state."""
        return "on" if self.is_on else "off"

    @property
    def image_rollover(self) -> ImageRollover:
        """Image rollover mode (normal or upside down)."""
        return ImageRollover(self.data["image_rollover"])

    @property
    def night_shot(self) -> NightShot:
        """Night shot mode (auto, on, or off)."""
        return NightShot(self.data["night_shot"])

    @property
    def time_watermark(self) -> bool:
        """True if time watermark is enabled."""
        return self.data["time_watermark"]

    @property
    def wdr_mode(self) -> bool:
        """True if WDR (Wide Dynamic Range) mode is enabled."""
        return self.data["wdr_mode"]


class MijiaCameraV1(MiotDevice):
    """Main class representing the Xiaomi Mijia Camera V1 (mijia.camera.v1)."""

    _mappings = MIOT_MAPPING
    _supported_models = [MODEL_CAMERA_MJSXJ02HL]

    @command(
        default_output=format_output(
            "",
            "Power: {result.power}\n"
            "Image Rollover: {result.image_rollover}\n"
            "Night Shot: {result.night_shot}\n"
            "Time Watermark: {result.time_watermark}\n"
            "WDR Mode: {result.wdr_mode}\n",
        )
    )
    def status(self) -> CameraStatus:
        """Retrieve properties."""
        return CameraStatus(
            {
                prop["did"]: prop["value"] if prop["code"] == 0 else None
                for prop in self.get_properties_for_mapping()
            }
        )

    @command(default_output=format_output("Powering on"))
    def on(self):
        """Power on."""
        return self.set_property("on", True)

    @command(default_output=format_output("Powering off"))
    def off(self):
        """Power off."""
        return self.set_property("on", False)

    @command(
        click.argument("mode", type=EnumType(ImageRollover)),
        default_output=format_output("Setting image rollover to '{mode.name}'"),
    )
    def set_image_rollover(self, mode: ImageRollover):
        """Set image rollover mode (Normal or UpsideDown)."""
        return self.set_property("image_rollover", mode.value)

    @command(
        click.argument("mode", type=EnumType(NightShot)),
        default_output=format_output("Setting night shot to '{mode.name}'"),
    )
    def set_night_shot(self, mode: NightShot):
        """Set night shot mode (Auto, On, or Off)."""
        return self.set_property("night_shot", mode.value)

    @command(
        click.argument("enabled", type=bool),
        default_output=format_output(
            lambda enabled: (
                "Enabling time watermark" if enabled else "Disabling time watermark"
            )
        ),
    )
    def set_time_watermark(self, enabled: bool):
        """Enable or disable time watermark."""
        return self.set_property("time_watermark", enabled)

    @command(
        click.argument("enabled", type=bool),
        default_output=format_output(
            lambda enabled: "Enabling WDR mode" if enabled else "Disabling WDR mode"
        ),
    )
    def set_wdr_mode(self, enabled: bool):
        """Enable or disable WDR (Wide Dynamic Range) mode."""
        return self.set_property("wdr_mode", enabled)

    @command(default_output=format_output("Formatting SD card"))
    def format_sd_card(self):
        """Format the SD card."""
        return self.call_action_from_mapping("format_sd")

    @command(default_output=format_output("Ejecting SD card"))
    def eject_sd_card(self):
        """Eject the SD card."""
        return self.call_action_from_mapping("eject_sd")

    @command(default_output=format_output("Starting P2P stream"))
    def start_p2p_stream(self):
        """Start P2P (peer-to-peer) stream.

        This starts the camera's P2P streaming capability which allows
        direct connection to the camera without going through cloud servers.
        """
        return self.call_action_from_mapping("start_p2p_stream")

    @command(default_output=format_output("Stopping P2P stream"))
    def stop_p2p_stream(self):
        """Stop P2P stream."""
        return self.call_action_from_mapping("stop_p2p_stream")

    @command(
        click.argument("video_attribute", type=int, default=0),
        default_output=format_output("Starting RTSP stream"),
    )
    def start_rtsp_stream(self, video_attribute: int = 0):
        """Start RTSP stream for Amazon Alexa.

        Returns stream address, snapshot URL, and expiration time.

        Args:
            video_attribute: Video quality attribute (default: 0)
        """
        return self.call_action_by(3, 1, [video_attribute])

    @command(default_output=format_output("Stopping Alexa stream"))
    def stop_alexa_stream(self):
        """Stop RTSP stream for Alexa."""
        return self.call_action_from_mapping("stop_alexa_stream")

    @command(default_output=format_output("Getting stream configuration"))
    def get_stream_configuration(self):
        """Get current stream configuration.

        Returns stream status and video attribute settings.
        """
        return self.call_action_from_mapping("get_stream_config")

    @command(
        click.argument("video_attribute", type=int, default=0),
        default_output=format_output("Starting HLS stream"),
    )
    def start_hls_stream(self, video_attribute: int = 0):
        """Start HLS stream for Google Home.

        Returns stream address for HLS playback.

        Args:
            video_attribute: Video quality attribute (default: 0)
        """
        return self.call_action_by(4, 1, [video_attribute])

    @command(default_output=format_output("Stopping Google stream"))
    def stop_google_stream(self):
        """Stop HLS stream for Google Home."""
        return self.call_action_from_mapping("stop_google_stream")
