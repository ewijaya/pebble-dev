#!/usr/bin/env python3
"""Install over a released PBW and compare an unchanged saved face."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, zipfile
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--stage', default='design-gate')
parser.add_argument('--release', default='1.2.0')
parser.add_argument('--from-version', default='1.1.0')
args = parser.parse_args()
OUT = ROOT/'dist/verification'/args.release/('upgrade-'+args.stage)
OUT.mkdir(parents=True, exist_ok=True)
OLD = ROOT/'dist/releases'/args.from_version/'thin-plus.pbw'
NEW = ROOT/'dist/verification'/args.release/args.stage/'thin-plus.pbw'
env = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy', SDL_RENDER_DRIVER='software')
python = Path(subprocess.check_output(['which','pebble'],text=True).strip()).read_text().splitlines()[0][2:]
def metadata(path):
    with zipfile.ZipFile(path) as z: return json.loads(z.read('appinfo.json'))
old, new = metadata(OLD), metadata(NEW)
assert all(new['messageKeys'][key] == value for key, value in old['messageKeys'].items())
assert old['uuid'] == new['uuid']
settings = dict(EnableDate=True, EnableBT=True, EnableBattery=True, EnableSecondHand=False,
                EnableThickHands=True, BatteryOnlyWhenLow=False, SlotTop='4',SlotLeft='3',SlotBottom='4',
                ColorBackground=0x0000AA,ColorHourMinutes=0x55FFFF,ColorSeconds=0xAA0000,
                ColorNotches=0xFFFFFF,ColorMonthDay=0xFFAA00,ColorDate=0xFFFFFF,
                ColorHandTips=0xFFFFFF,ColorCenterDot=0xAA0000,ColorSecondTip=0xFFAA00,
                ColorBatteryEmpty=0x555555,Theme='custom')
def run(args):
    with (OUT/'commands.log').open('a') as log:
        log.write('\n'+' '.join(args)+'\n');log.flush()
        subprocess.run(args,cwd=OUT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=100)
assert subprocess.run(['pgrep','-x','qemu-pebble'],capture_output=True).returncode==1
try:
    run(['pebble','install','--emulator','emery',str(OLD)])
    run(['pebble','emu-battery','--emulator','emery','--percent','60'])
    ints, strings = [], []
    for key,value in settings.items():
        (strings if isinstance(value,str) else ints).append(str(old['messageKeys'][key])+'='+str(int(value) if isinstance(value,bool) else value))
    run(['pebble','send-app-message','--emulator','emery','--app-uuid',old['uuid'],'--int']+ints+['--string']+strings)
    run([python,str(ROOT/'tests/capture_fixed_time.py'),'emery',str(OUT/('before-'+args.from_version+'.png'))])
    run(['pebble','install','--emulator','emery',str(NEW)])
    run([python,str(ROOT/'tests/capture_fixed_time.py'),'emery',str(OUT/'after-candidate.png')])
    difference = ImageChops.difference(Image.open(OUT/('before-'+args.from_version+'.png')).convert('RGB'),
                                     Image.open(OUT/'after-candidate.png').convert('RGB'))
    identical = difference.getbbox() is None
    report = {'identical_pixels':identical,'old_pbw_sha256':hashlib.sha256(OLD.read_bytes()).hexdigest(),
              'candidate_sha256':hashlib.sha256(NEW.read_bytes()).hexdigest(),
              'old_message_key_ids_unchanged':True,'settings':settings,
              'method':'Install released '+args.from_version+', save custom settings, install candidate over it; native screenshots at identical emulator time.'}
    (OUT/'result.json').write_text(json.dumps(report,indent=2)+'\n')
    assert identical, 'Upgrade changed the saved face; inspect screenshots'
    print('PASS: real '+args.from_version+' upgrade, original message-key IDs retained, identical face pixels.')
finally:
    run(['pebble','kill'])
