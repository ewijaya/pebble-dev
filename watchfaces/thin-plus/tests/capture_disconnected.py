#!/usr/bin/env python3
"""Use QEMU's framebuffer when Bluetooth-off prevents a CLI screenshot.

Run with the Pebble tool's Python environment. No new watch connection is made:
that would reconnect Bluetooth and erase the very state being tested.
"""
import sys, tempfile
from pathlib import Path
from pebble_tool.sdk.emulator import ManagedEmulatorTransport
from pebble_tool.commands.emucontrol import send_data_to_qemu
from libpebble2.communication.transports.qemu.protocol import QemuBluetoothConnection
from pebble_tool.commands.screenshot import ScreenshotCommand

platform, filename = sys.argv[1:]
transport = ManagedEmulatorTransport(platform)
port = transport.qemu_monitor_port
with tempfile.TemporaryDirectory(prefix='thin-disconnect-frame-') as temp:
    image = ScreenshotCommand._grab_qemu_monitor_image_fast(port, temp, 0)
    path = Path(filename)
    image.save(path.with_suffix('.raw.png'))
    # QEMU dims the entire panel when the backlight sleeps. Normalize this
    # uniform brightness, as the SDK's GIF capture does; retain the raw evidence.
    rgb = image.convert('RGB')
    peak = max(high for low, high in rgb.getextrema())
    if peak:
        rgb = rgb.point([min(255, round(i * 255 / peak)) for i in range(256)] * 3)
    rgb.save(path)
    print('Native framebuffer:', image.size, 'brightness scale:', 255/peak if peak else 1)

# Restore through the emulator control channel, without a watch-info handshake.
transport.connect()
send_data_to_qemu(transport, QemuBluetoothConnection(connected=True))
import time
time.sleep(.3)
transport.ws.close()
