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
- Not all camera features are exposed via the API (e.g., live streaming requires P2P connection)
- Some advanced features like Alexa/Google Home integration require additional setup
