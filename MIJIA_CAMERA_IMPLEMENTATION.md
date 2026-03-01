# Mijia Camera V1 Implementation Summary

## What Was Added

Support for the **Xiaomi Mijia Camera V1 (mijia.camera.v1)** has been successfully added to python-miio!

## Files Created

### 1. Core Implementation
- **`miio/integrations/mijia/camera/mijia_camera.py`**
  - Main implementation with MijiaCameraV1 class
  - CameraStatus class for status reporting
  - ImageRollover and NightShot enums
  - MIoT mapping for all supported properties

- **`miio/integrations/mijia/camera/__init__.py`**
  - Export definitions for the camera module

- **`miio/integrations/mijia/camera/test_mijia_camera.py`**
  - Unit tests for the camera implementation

### 2. Integration
- **`miio/integrations/mijia/__init__.py`**
  - Updated to export camera classes

- **`miio/__init__.py`**
  - Added MijiaCameraV1 to main module exports
  - Users can now import with: `from miio import MijiaCameraV1`

### 3. Documentation & Examples
- **`README_MIJIA_CAMERA.md`**
  - Complete usage guide
  - API documentation
  - Command-line examples

- **`examples/mijia_camera_example.py`**
  - Ready-to-use example script
  - Shows all available features

## Supported Features

### Camera Control (Service 2)
✅ **Power Control**
- Turn camera on/off

✅ **Image Rollover**
- Normal orientation
- Upside-down (180° flip)

✅ **Night Shot Mode**
- Auto (based on light conditions)
- Always on
- Always off

✅ **Time Watermark**
- Show/hide timestamp overlay

✅ **WDR Mode**
- Wide Dynamic Range for better contrast

### Memory Card Management (Service 6)
✅ **SD Card Operations**
- Format SD card
- Safely eject SD card

## Quick Start

### Python API

```python
from miio import MijiaCameraV1
from miio.integrations.mijia.camera import ImageRollover, NightShot

# Connect
camera = MijiaCameraV1("192.168.1.10", "your_token_here")

# Get status
status = camera.status()
print(f"Power: {status.power}")
print(f"Night Mode: {status.night_shot.name}")

# Control
camera.on()
camera.set_night_shot(NightShot.Auto)
camera.set_time_watermark(True)
```

### Command Line

```bash
# Get status
miiocli mijiacamerav1 --ip IP --token TOKEN status

# Turn on
miiocli mijiacamerav1 --ip IP --token TOKEN on

# Set night mode
miiocli mijiacamerav1 --ip IP --token TOKEN set_night_shot Auto
```

## Testing

All tests pass successfully:

```bash
python3 test_camera_implementation.py
```

Output:
```
✓ All classes imported successfully
✓ Testing enums
✓ Testing status parsing
✓ Testing model information
✅ All tests passed!
```

## Technical Details

- **Protocol**: MIoT (Xiaomi IoT protocol)
- **Model**: mijia.camera.v1
- **Device URN**: urn:miot-spec-v2:device:camera:0000A01C:mijia-v1:1
- **Spec Source**: Automatically fetched from Xiaomi cloud via MiotCloud API

## Device Specification

The implementation is based on the official MIoT specification with the following services:

1. **Camera Control** (siid: 2)
   - on (piid: 1) - Power switch
   - image-rollover (piid: 2) - Image orientation
   - night-shot (piid: 3) - Night vision mode
   - time-watermark (piid: 5) - Timestamp overlay
   - wdr-mode (piid: 6) - Wide dynamic range

2. **Memory Card Management** (siid: 6)
   - format (aiid: 1) - Format SD card
   - pop-up (aiid: 2) - Eject SD card

## Next Steps

You can now use your camera control script! Replace the contents of `camera_control.py` with:

```python
from miio import MijiaCameraV1
from miio.integrations.mijia.camera import NightShot

IP = "192.168.1.10"
TOKEN = "364d7543663979497647704e58505749"

camera = MijiaCameraV1(IP, TOKEN)

# Get current status
status = camera.status()
print(f"Camera is {status.power}")
print(f"Night mode: {status.night_shot.name}")

# Control the camera
camera.on()
camera.set_night_shot(NightShot.Auto)
```

Or use the example script:
```bash
python3 examples/mijia_camera_example.py
```

## Notes

- The camera uses MIoT protocol, not the older miIO protocol
- Streaming features require P2P connection (not available via this API)
- All basic camera controls are now fully supported
- The implementation follows python-miio conventions and patterns

## Contributing

If you want to add more features or find issues:
1. Implement your changes
2. Add tests
3. Submit a pull request to: https://github.com/rytilahti/python-miio

---

**Status**: ✅ Ready to use!
**Date**: March 1, 2026
