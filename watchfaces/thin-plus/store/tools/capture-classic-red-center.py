"""Prepare a native Emery screenshot and banner using the frozen 1.0.0 PBW.

Only local artwork is produced. Does not build, install on a physical watch,
upload, or modify the active gallery. Run with no other emulator in use.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'store/revisions/classic-red-center'
PBW = ROOT / 'dist/releases/1.0.0/thin-plus.pbw'
EXPECTED = 'b5fe248bf60447b144b71ee5078db23933780916a865271d3a924967e1cae517'
assert hashlib.sha256(PBW.read_bytes()).hexdigest() == EXPECTED
assert subprocess.run(['pgrep', '-x', 'qemu-pebble'], capture_output=True).returncode == 1, 'Another emulator is running'
OUT.mkdir(parents=True, exist_ok=True)
SCRATCH = Path(tempfile.mkdtemp(prefix='thin-plus-classic-red-center-'))
env = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy', SDL_RENDER_DRIVER='software')
with zipfile.ZipFile(PBW) as archive:
    info = json.loads(archive.read('appinfo.json'))
keys = info['messageKeys']
config = json.loads(subprocess.check_output(['node', '-e', 'process.stdout.write(JSON.stringify(require("./src/pkjs/config")))'], cwd=ROOT, text=True))
items = {}
def walk(values):
    for item in values:
        if 'messageKey' in item and item['messageKey'] in keys:
            items[item['messageKey']] = item
        walk(item.get('items', []))
walk(config)
js = (ROOT / 'src/pkjs/custom-clay.js').read_text()
color_keys = re.findall(r"'([^']+)'", re.search(r'var COLOR_KEYS = \[(.*?)\];', js, re.S).group(1))
colors = re.findall(r"'([0-9A-F]+)'", re.search(r'classic: \[([^\]]+)\]', js).group(1))
override = dict(zip(color_keys, colors))
override.update(ColorCenterDot='AA0000', Theme='custom', EnableDate=False, EnableBT=False,
                EnableBattery=False, EnableSecondHand=True, EnableThickHands=False,
                SlotTop='0', SlotLeft='0', SlotBottom='0')
ints, strings = [], []
for key, item in items.items():
    value = override.get(key, item['defaultValue'])
    if item['type'] == 'color':
        value = int(value, 16)
    target = strings if isinstance(value, str) else ints
    target.append(str(keys[key]) + '=' + str(int(value) if isinstance(value, bool) else value))
def run(args):
    with (OUT / 'capture.log').open('a') as log:
        log.write('\nCOMMAND: ' + ' '.join(args) + '\n')
        log.flush()
        subprocess.run(args, cwd=SCRATCH, env=env, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=120)
face = OUT / 'emery-01-classic-red-center.png'
try:
    run(['pebble', 'install', '--emulator', 'emery', str(PBW)])
    run(['pebble', 'send-app-message', '--emulator', 'emery', '--app-uuid', info['uuid'], '--int'] + ints + ['--string'] + strings)
    run(['pebble', 'emu-tap', '--emulator', 'emery'])
    time.sleep(1)
    run(['pebble', 'screenshot', '--emulator', 'emery', '--no-open', str(face)])
finally:
    run(['pebble', 'kill'])
    assert hashlib.sha256(PBW.read_bytes()).hexdigest() == EXPECTED
subprocess.run(['python3', str(ROOT/'store/tools/draw-banner.py'), '--face', str(face), '--output', str(OUT/'banner-emery-720x320.png')], check=True)
record = {'status': 'Prepared locally; store upload pending approval', 'platform': 'emery',
          'source_pbw_sha256': EXPECTED, 'source_pbw_version': info['versionLabel'],
          'capture': 'Native unscaled emulator PNG; released PBW; real AppMessage settings; wrist-tap input; live clock',
          'settings': override, 'physical_watch_test': 'Not performed for this artwork revision',
          'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.png')}}
(OUT/'provenance.json').write_text(json.dumps(record, indent=2)+'\n')
print('Prepared screenshot and banner in ' + str(OUT))
