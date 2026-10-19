#!/usr/bin/env python3
"""Real AppMessage and emulator evidence for the 1.3 design gate."""
from pathlib import Path
import argparse,json,os,subprocess,signal,time,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('platforms', nargs='+')
parser.add_argument('--stage', default='design-gate')
parser.add_argument('--design-only', action='store_true')
parser.add_argument('--date-styles', action='store_true')
args=parser.parse_args()
OUT=ROOT/'dist/verification/1.3.0'/args.stage
PBW=OUT/'thin-plus.pbw'
SCRATCH=Path(json.loads((OUT/'build-context.json').read_text())['scratch'])
ENV=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',SDL_RENDER_DRIVER='software')
with zipfile.ZipFile(PBW) as z: info=json.loads(z.read('appinfo.json'))
records=json.loads((OUT/'captures.json').read_text()) if (OUT/'captures.json').exists() else []
def cli(p,args):
 with (OUT/(p+'-commands.log')).open('a') as log:
  log.write('\npebble '+' '.join(args)+'\n');log.flush()
  subprocess.run(['pebble']+args,cwd=SCRATCH,env=ENV,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=90)
def settings(p,**values):
 ints=[];strings=[]
 for k,v in values.items():(strings if isinstance(v,str) else ints).append(str(info['messageKeys'][k])+'='+str(int(v) if isinstance(v,bool) else v))
 args=['send-app-message','--emulator',p,'--app-uuid',info['uuid']]
 if ints:args+=['--int']+ints
 if strings:args+=['--string']+strings
 cli(p,args)
def capture(p,label):
 time.sleep(1)
 path=OUT/(p+'-'+label+'.png');cli(p,['screenshot','--emulator',p,'--no-open',str(path)])
 records.append({'platform':p,'case':label,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 (OUT/'captures.json').write_text(json.dumps(records,indent=2)+'\n')
 print('Captured '+p+' '+label,flush=True)
def capture_fixed(p,label):
 py=Path(subprocess.check_output(['which','pebble'],text=True).strip()).read_text().splitlines()[0][2:]
 path=OUT/(p+'-'+label+'.png')
 subprocess.run([py,str(ROOT/'tests/capture_fixed_time.py'),p,str(path),'10:35'],check=True)
 records.append({'platform':p,'case':label,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 (OUT/'captures.json').write_text(json.dumps(records,indent=2)+'\n')
 print('Captured '+p+' '+label,flush=True)
assert subprocess.run(['pgrep','-x','qemu-pebble'],capture_output=True).returncode==1
try:
 for p in args.platforms:
  try:
   cli(p,['install','--emulator',p,str(PBW)])
   log=(OUT/(p+'-runtime.log')).open('w')
   proc=subprocess.Popen(['pebble','logs','--emulator',p,'--no-color'],cwd=SCRATCH,env=ENV,stdout=log,stderr=subprocess.STDOUT)
   try:
    settings(p,EnableDate=True,EnableBT=True,EnableBattery=False,EnableSecondHand=False,EnableThickHands=False,EnableStartupAnim=False,
     EnableStepRing=False,EnableEnhancedBT=False,EnableChargingColor=False,TapForSeconds=False,SlotTop='0',SlotLeft='0',SlotBottom='0',
     ColorBackground=0,ColorHourMinutes=0xAAAAAA,ColorNotches=0xFFFFFF,ColorHandTips=0xFFFFFF,ColorCenterDot=0xAA0000,ColorMonthDay=0xFFAA00,ColorDate=0xFFFFFF,ColorStepRing=0x00AAAA,WeatherUnits=0)
    if args.date_styles:
     for style,label in [(0,'full'),(1,'day-only'),(2,'weekday-day')]:
      settings(p,DateStyle=str(style))
      capture_fixed(p,'date-'+label)
     settings(p,EnableDate=False)
     capture_fixed(p,'date-hidden')
     settings(p,EnableDate=True,DateStyle='0')
     capture_fixed(p,'date-full-restored')
     from PIL import Image,ImageChops
     assert ImageChops.difference(Image.open(OUT/(p+'-date-full.png')).convert('RGB'),Image.open(OUT/(p+'-date-full-restored.png')).convert('RGB')).getbbox() is None
     continue
    cli(p,['emu-steps','--emulator',p,'3750'])
    cli(p,['emu-distance','--emulator',p,'16900'])
    cli(p,['emu-calories','--emulator',p,'1234'])
    settings(p,SlotTop='7',SlotLeft='5',SlotBottom='6')
    capture(p,'new-complications')
    # Store fixture weather before selecting its slot: a fresh cache avoids a network refresh.
    settings(p,WeatherTemp=18,WeatherCode=3,WeatherUnits=0)
    settings(p,SlotTop='9',SlotLeft='0',SlotBottom='1',EnableStepRing=True)
    capture(p,'weather-ring-3750')
    cli(p,['emu-steps','--emulator',p,'7500'])
    settings(p,EnableStepRing=True)
    capture(p,'weather-ring-7500')
    if args.design_only: continue
    settings(p,EnableStepRing=False)
    capture(p,'ring-off')
    settings(p,WeatherTemp=-8,WeatherCode=71,WeatherUnits=0)
    capture(p,'weather-negative')
    settings(p,WeatherUnits=1)
    capture(p,'weather-unit-change')
    settings(p,WeatherTemp=72,WeatherCode=0,WeatherUnits=1)
    capture(p,'weather-fahrenheit')
    settings(p,SlotTop='8',SlotLeft='7',SlotBottom='4',TzOffsetMinutes=540)
    capture(p,'timezone-week')
    if p=='flint':
     for kind,label in [('5','distance-10-5'),('6','calories-1234'),('7','week')]:
      settings(p,SlotTop='0',SlotBottom='0',SlotLeft=kind)
      capture(p,'left-'+label)
     settings(p,SlotLeft='4')
     py=Path(subprocess.check_output(['which','pebble'],text=True).strip()).read_text().splitlines()[0][2:]
     path=OUT/(p+'-left-12-59.png')
     subprocess.run([py,str(ROOT/'tests/capture_fixed_time.py'),p,str(path),'12:59'],check=True)
     records.append({'platform':p,'case':'left-12-59','path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    # Leave the emulator without a weather selection; no background requests.
    settings(p,SlotTop='0',SlotLeft='0',SlotBottom='0',EnableStepRing=False)
   finally:
    proc.send_signal(signal.SIGINT)
    try:proc.wait(timeout=5)
    except subprocess.TimeoutExpired:proc.kill();proc.wait()
    log.close()
  finally:cli(p,['kill'])
finally:
 (OUT/'captures.json').write_text(json.dumps(records,indent=2)+'\n')
