#!/usr/bin/env python3
"""Example script for controlling Mijia Camera V1 (mijia.camera.v1)."""

from miio import MijiaCameraV1
from miio.integrations.mijia.camera import ImageRollover, NightShot

# Your device details
IP = "192.168.1.10"
TOKEN = "364d7543663979497647704e58505749"

try:
    # Create camera instance
    camera = MijiaCameraV1(IP, TOKEN)

    print("=" * 60)
    print("Mijia Camera V1 Control Example")
    print("=" * 60)

    # Get status
    print("\n📷 Current Status:")
    status = camera.status()
    print(f"  Power: {status.power}")
    print(f"  Image Rollover: {status.image_rollover.name}")
    print(f"  Night Shot: {status.night_shot.name}")
    print(f"  Time Watermark: {status.time_watermark}")
    print(f"  WDR Mode: {status.wdr_mode}")

    print("\n" + "=" * 60)
    print("Available Commands:")
    print("=" * 60)

    # Example commands (commented out - uncomment to use)

    # Power control
    # camera.on()   # Turn camera on
    # camera.off()  # Turn camera off

    # Image orientation
    # camera.set_image_rollover(ImageRollover.Normal)      # Normal orientation
    # camera.set_image_rollover(ImageRollover.UpsideDown)  # Flip 180 degrees

    # Night vision mode
    # camera.set_night_shot(NightShot.Auto)  # Auto night vision
    # camera.set_night_shot(NightShot.On)    # Always on
    # camera.set_night_shot(NightShot.Off)   # Always off

    # Time watermark
    # camera.set_time_watermark(True)   # Show timestamp
    # camera.set_time_watermark(False)  # Hide timestamp

    # WDR (Wide Dynamic Range)
    # camera.set_wdr_mode(True)   # Enable WDR
    # camera.set_wdr_mode(False)  # Disable WDR

    # SD card management
    # camera.format_sd_card()  # Format SD card (WARNING: Deletes all data!)
    # camera.eject_sd_card()   # Safely eject SD card

    print("\n✅ Connection successful!")
    print("\nUncomment the commands in the script to control your camera.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("  1. Check if the IP address is correct")
    print("  2. Verify the token (32 hex characters)")
    print("  3. Make sure the camera is on the same network")
    print("  4. Ensure the camera is powered on")
