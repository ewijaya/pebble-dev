#!/usr/bin/env python3
"""Checkpoint emulator tests using real AppMessages and native CLI screenshots."""
from pathlib import Path
import argparse, hashlib, json, os, signal, subprocess, time, zipfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('stage')
parser.add_argument('platforms', nargs='+')
parser.add_argument('--release', default='1.2.0')
args = parser.parse_args()
OUT = ROOT/'dist/verification'/args.release/args.stage
PBW = OUT/'thin-plus.pbw'
SCRATCH = Path(json.loads((OUT/'build-context.json').read_text())['scratch'])
ENV = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy', SDL_RENDER_DRIVER='software')
with zipfile.ZipFile(PBW) as z:
    INFO = json.loads(z.read('appinfo.json'))
records = json.loads((OUT/'captures.json').read_text()) if (OUT/'captures.json').exists() else []

def cli(arguments, platform):
    with (OUT/(platform+'-commands.log')).open('a') as log:
        log.write('\nCOMMAND: pebble '+' '.join(arguments)+'\n'); log.flush()
        subprocess.run(['pebble']+arguments, cwd=SCRATCH, env=ENV, stdout=log,
                       stderr=subprocess.STDOUT, check=True, timeout=100)

def settings(platform, **values):
    ints, strings = [], []
    for key, value in values.items():
        target = strings if isinstance(value, str) else ints
        target.append(str(INFO['messageKeys'][key])+'='+str(int(value) if isinstance(value, bool) else value))
    command = ['send-app-message', '--emulator', platform, '--app-uuid', INFO['uuid']]
    if ints: command += ['--int']+ints
    if strings: command += ['--string']+strings
    cli(command, platform)

def capture(platform, label, disconnected=False):
    path = OUT/(platform+'-'+label+'.png')
    if disconnected:
        # The CLI screenshot opens another connection, which re-enables BT on
        # Emery and times out on Chalk. Read the unchanged native framebuffer.
        # PebbleOS debounces phone disconnection for 25 seconds.
        time.sleep(27)
        pebble_python = Path(subprocess.check_output(['which','pebble'],text=True).strip()).read_text().splitlines()[0][2:]
        subprocess.run([pebble_python, str(ROOT/'tests/capture_disconnected.py'), platform, str(path)], check=True)
    else:
        cli(['screenshot', '--emulator', platform, '--no-open', str(path)], platform)
    records.append({'platform':platform, 'case':label, 'path':str(path.relative_to(ROOT)),
                    'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    print('Captured '+platform+' '+label, flush=True)

def baseline(platform):
    settings(platform, EnableDate=True, EnableBT=True, EnableBattery=False,
             EnableSecondHand=False, EnableThickHands=False, BatteryOnlyWhenLow=False,
             SlotTop='4', SlotLeft='3', SlotBottom='1', ColorBackground=0,
             ColorHourMinutes=0xAAAAAA, ColorSeconds=0xAA0000, ColorNotches=0xFFFFFF,
             ColorMonthDay=0xFFAA00, ColorDate=0xFFFFFF, ColorHandTips=0xFFFFFF,
             ColorCenterDot=0xAA0000, ColorSecondTip=0xFFAA00, ColorBatteryEmpty=0x555555)
    if platform != 'aplite':
        cli(['emu-steps', '--emulator', platform, '6432'], platform)
    cli(['emu-battery', '--emulator', platform, '--percent', '60'], platform)

assert subprocess.run(['pgrep', '-x', 'qemu-pebble'], capture_output=True).returncode == 1, 'An emulator is already running'

try:
    for platform in args.platforms:
        cli(['install', '--emulator', platform, str(PBW)], platform)
        log = (OUT/(platform+'-runtime.log')).open('w')
        proc = subprocess.Popen(['pebble','logs','--emulator',platform,'--no-color'],
                                cwd=SCRATCH, env=ENV, stdout=log, stderr=subprocess.STDOUT)
        try:
            baseline(platform)
            if args.stage.startswith('final'):
                settings(platform, EnableEnhancedBT=False, EnableChargingColor=False,
                         TapForSeconds=False, EnableStartupAnim=False, VibrateOnDisconnect=True,
                         ColorDisconnected=0xFF0000, ColorCharging=0x00FF00)
                if 'EnableStepRing' in INFO['messageKeys']:
                    settings(platform, EnableStepRing=False)
                if 'DateStyle' in INFO['messageKeys']:
                    settings(platform, DateStyle='0')
                time.sleep(20)
                capture(platform, 'smoke')
            elif args.stage.startswith('r2'):
                settings(platform, SlotTop='2')
                capture(platform, 'heart-rate-unavailable')
                settings(platform, SlotTop='4')
                capture(platform, 'partial-before')
                settings(platform, EnableDate=False)
                capture(platform, 'partial-date-off')
                settings(platform, EnableDate=True)
                capture(platform, 'partial-restored')
            elif args.stage == 'r1':
                for state in ['off', 'on', 'off']:
                    cli(['emu-set-timeline-quick-view', '--emulator', platform, state], platform)
                    time.sleep(1)
                    capture(platform, 'quick-view-'+state+('-restored' if len([r for r in records if r['platform']==platform])==2 else ''))
            elif args.stage.startswith('r3'):
                cli(['emu-bt-connection', '--emulator', platform, '--connected', 'yes'], platform)
                settings(platform, EnableEnhancedBT=True, VibrateOnDisconnect=False, ColorDisconnected=0xFF0000)
                capture(platform, 'connected')
                cli(['emu-bt-connection', '--emulator', platform, '--connected', 'no'], platform)
                capture(platform, 'disconnected-enhanced', disconnected=True)
                cli(['emu-bt-connection', '--emulator', platform, '--connected', 'yes'], platform)
            elif args.stage == 'r5':
                settings(platform, TapForSeconds=True, EnableSecondHand=False)
                cli(['emu-tap','--emulator',platform], platform)
                capture(platform, 'seconds-disabled')
                settings(platform, EnableSecondHand=True)
                cli(['emu-tap','--emulator',platform], platform)
                capture(platform, 'wrist-seconds-visible')
                time.sleep(16)
                capture(platform, 'seconds-expired')
            elif args.stage == 'r9':
                settings(platform, EnableBattery=True, EnableChargingColor=True, ColorCharging=0x00FF00)
                cli(['emu-battery','--emulator',platform,'--percent','60'], platform)
                capture(platform, 'normal-60')
                cli(['emu-battery','--emulator',platform,'--percent','60','--charging'], platform)
                capture(platform, 'charging-60')
                settings(platform, EnableChargingColor=False)
                capture(platform, 'charging-opt-out')
                settings(platform, EnableChargingColor=True, EnableBattery=False)
                capture(platform, 'hour-markers-off')
                settings(platform, EnableBattery=True, ColorBackground=0xFFFFFF, ColorHourMinutes=0x555555,
                         ColorNotches=0,ColorDate=0, ColorMonthDay=0x0000FF,ColorHandTips=0,
                         ColorCenterDot=0,ColorBatteryEmpty=0xAAAAAA,ColorCharging=0x005500)
                capture(platform, 'paper-charging-60')
                cli(['emu-battery','--emulator',platform,'--percent','60'], platform)
            elif args.stage == 'r10':
                for enabled in [False, True]:
                    settings(platform, EnableStartupAnim=enabled)
                    cli(['install','--emulator',platform,str(PBW)],platform)
                    capture(platform, 'startup-'+('on' if enabled else 'off'))
            if proc.poll() is not None:
                raise RuntimeError('Runtime log stream exited early')
        finally:
            proc.send_signal(signal.SIGINT)
            try: proc.wait(timeout=5)
            except subprocess.TimeoutExpired: proc.kill(); proc.wait()
            log.close()
            cli(['kill'], platform)
finally:
    (OUT/'captures.json').write_text(json.dumps(records, indent=2)+'\n')
    cli(['kill'], 'cleanup')
