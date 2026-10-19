#!/usr/bin/env python3
"""Native SDK screenshot at a stable demo time, with one emulator connection."""
import argparse, datetime, sys, time
import png
from libpebble2.communication import PebbleConnection
from pebble_tool.commands.screenshot import ScreenshotCommand
from pebble_tool.sdk.emulator import ManagedEmulatorTransport

platform, filename = sys.argv[1:3]
hour, minute = map(int, sys.argv[3].split(':')) if len(sys.argv) > 3 else (10, 10)
pebble = PebbleConnection(ManagedEmulatorTransport(platform))
pebble.connect(); pebble.run_async()
command = ScreenshotCommand(); command.pebble = pebble
# Let launch animation and phone simulator time sync finish, then use the SDK's
# double-set/settle pattern. Otherwise one frame can still show the host clock.
time.sleep(2)
target = datetime.datetime(2026, 10, 19, hour, minute, 0)
command._set_time(pebble, target)
time.sleep(.35)
command._set_time(pebble, target)
time.sleep(1.2)
pixels = command._grab_processed_image(argparse.Namespace(no_correction=False, scale=1), show_progress=False)
png.from_array(pixels, mode='RGBA;8').save(filename)
