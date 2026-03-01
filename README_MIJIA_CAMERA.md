# Mijia Camera V1 Support

This document describes the support for Xiaomi Mijia Camera V1 (mijia.camera.v1) in python-miio.

## Installation

Make sure you have python-miio installed:

```bash
pip install python-miio
```

## Basic Usage

```python
from miio import MijiaCameraV1
from miio.integrations.mijia.camera import ImageRollover, NightShot

# Connect to the camera
camera = MijiaCameraV1("192.168.1.10", "your_token_here")

# Get status
status = camera.status()
print(f"Power: {status.power}")
print(f"Night Shot: {status.night_shot}")
print(f"Time Watermark: {status.time_watermark}")
```

## Supported Features

### Power Control

```python
# Turn camera on/off
camera.on()
camera.off()
```

### Image Orientation

Control the image orientation (useful if camera is mounted upside down):

```python
from miio.integrations.mijia.camera import ImageRollover

# Normal orientation
camera.set_image_rollover(ImageRollover.Normal)

# Flip 180 degrees
camera.set_image_rollover(ImageRollover.UpsideDown)
```

### Night Vision Mode

Control infrared night vision:

```python
from miio.integrations.mijia.camera import NightShot

# Auto mode (switches based on light conditions)
camera.set_night_shot(NightShot.Auto)

# Always on
camera.set_night_shot(NightShot.On)

# Always off
camera.set_night_shot(NightShot.Off)
```

### Time Watermark

Show or hide timestamp overlay on the video:

```python
# Show timestamp
camera.set_time_watermark(True)

# Hide timestamp
camera.set_time_watermark(False)
```

### WDR (Wide Dynamic Range)

Improve image quality in high-contrast lighting conditions:

```python
# Enable WDR
camera.set_wdr_mode(True)

# Disable WDR
camera.set_wdr_mode(False)
```

### SD Card Management

```python
# Format SD card (WARNING: This will delete all data!)
camera.format_sd_card()

# Safely eject SD card
camera.eject_sd_card()
```

### Video Streaming

The camera supports multiple streaming protocols:

#### P2P Stream (Peer-to-Peer)

```python
# Start P2P stream (direct connection without cloud)
camera.start_p2p_stream()

# Stop P2P stream
camera.stop_p2p_stream()
```

#### RTSP Stream (for Amazon Alexa)

```python
# Start RTSP stream with default quality
result = camera.start_rtsp_stream()
# Returns: stream address, snapshot URL, and expiration time

# Start with specific video quality (0 = default)
result = camera.start_rtsp_stream(video_attribute=0)

# Stop RTSP stream
camera.stop_alexa_stream()

# Get current stream configuration
config = camera.get_stream_configuration()
```

#### HLS Stream (for Google Home)

```python
# Start HLS stream
result = camera.start_hls_stream()
# Returns: stream address

# Start with specific video quality
result = camera.start_hls_stream(video_attribute=0)

# Stop HLS stream
camera.stop_google_stream()
```

**Note**: Actual video playback requires additional client software that supports the respective protocols (P2P client, RTSP player, or HLS player).

## Status Properties

The `status()` method returns a `CameraStatus` object with the following properties:

- `is_on`: Boolean indicating if camera is powered on
- `power`: String "on" or "off"
- `image_rollover`: ImageRollover enum (Normal or UpsideDown)
- `night_shot`: NightShot enum (Auto, On, or Off)
- `time_watermark`: Boolean indicating if timestamp is displayed
- `wdr_mode`: Boolean indicating if WDR is enabled

## Command Line Usage

You can also control the camera from the command line using miiocli:

```bash
# Get status
miiocli mijiacamerav1 --ip 192.168.1.10 --token YOUR_TOKEN status

# Turn on
miiocli mijiacamerav1 --ip 192.168.1.10 --token YOUR_TOKEN on

# Set night shot mode
miiocli mijiacamerav1 --ip 192.168.1.10 --token YOUR_TOKEN set_night_shot Auto
```

## Getting Your Token

To control the camera, you need its token. You can extract it using:

1. The Mi Home app (using various methods)
2. python-miio's discovery feature:
   ```bash
   miiocli discover
   ```

## Device Specification

This implementation is based on the official MIoT specification:
- Model: mijia.camera.v1
- URN: urn:miot-spec-v2:device:camera:0000A01C:mijia-v1:1
- Spec URL: https://home.miot-spec.com/spec/mijia.camera.v1

## Example Script

See `examples/mijia_camera_example.py` for a complete example.

## Contributing

If you find issues or want to add more features, please contribute at:
https://github.com/rytilahti/python-miio

## Notes

- This camera uses the MIoT protocol (not the older miIO protocol)
- P2P streaming is supported but requires a P2P client to view the stream
- RTSP and HLS streaming are available for integration with Alexa and Google Home
- Stream URLs returned by the API typically include authentication tokens with expiration times
