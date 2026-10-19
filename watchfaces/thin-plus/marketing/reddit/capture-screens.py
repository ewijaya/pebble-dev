"""Capture the released Thin+ app on Emery using one connection and a fixed demo time."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,subprocess,tempfile,time,uuid,zipfile,threading
import png
from pebble_tool.sdk.emulator import ManagedEmulatorTransport
from pebble_tool.commands.screenshot import ScreenshotCommand
from pebble_tool.commands.emucontrol import send_data_to_qemu
from libpebble2.communication import PebbleConnection
from libpebble2.services.appmessage import AppMessageService,Int32,CString
from libpebble2.communication.transports.qemu.protocol import QemuTap,QemuBattery
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent/'screens';PBW=ROOT/'dist/releases/1.1.0/thin-plus.pbw';OUT.mkdir(exist_ok=True)
assert subprocess.run(['pgrep','-x','qemu-pebble'],capture_output=True).returncode==1,'Another emulator is running'
expected=hashlib.sha256(PBW.read_bytes()).hexdigest();env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',SDL_RENDER_DRIVER='software');os.environ.update({k:env[k] for k in ['SDL_VIDEODRIVER','SDL_AUDIODRIVER','SDL_RENDER_DRIVER']})
work=Path(tempfile.mkdtemp(prefix='thin-plus-promo-'));log=(OUT/'capture.log').open('a')
def cli(args):subprocess.run(['pebble']+args,cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=120)
with zipfile.ZipFile(PBW) as z:info=json.loads(z.read('appinfo.json'))
config=json.loads(subprocess.check_output(['node','-e','process.stdout.write(JSON.stringify(require("./src/pkjs/config")))'],cwd=ROOT,text=True));items={}
def walk(xs):
 for x in xs:
  if 'messageKey' in x:items[x['messageKey']]=x
  walk(x.get('items',[]))
walk(config)
js=(ROOT/'src/pkjs/custom-clay.js').read_text();color_keys=re.findall(r"'([^']+)'",re.search(r'var COLOR_KEYS = \[(.*?)\];',js,re.S).group(1));themes={n:re.findall(r"'([0-9A-F]+)'",v) for n,v in re.findall(r'(\w+): \[([^\]]+)\]',js)}
pebble=None;service=None;records=[]
try:
 cli(['install','--emulator','emery',str(PBW)]);cli(['emu-steps','--emulator','emery','6432'])
 pebble=PebbleConnection(ManagedEmulatorTransport('emery'));pebble.connect();pebble.run_async();service=AppMessageService(pebble);command=ScreenshotCommand();command.pebble=pebble
 variants=[(n,n,'minimal') for n in ['classic','neon','ocean','sunset','lime','mono','paper']]+[('classic-medium','classic','medium'),('classic-rich','classic','rich')]
 for name,theme,density in variants:
  settings=dict(zip(color_keys,themes[theme]));settings.update(Theme='custom',EnableDate=density!='minimal',EnableBT=False,EnableBattery=False,EnableSecondHand=True,EnableThickHands=False,BatteryOnlyWhenLow=False,SlotTop='4' if density=='rich' else '0',SlotLeft='3' if density=='rich' else '0',SlotBottom='1' if density!='minimal' else '0')
  if theme=='classic':settings['ColorCenterDot']='AA0000'
  values={}
  for key,item in items.items():
   value=settings.get(key,item['defaultValue'])
   if item['type']=='color':value=int(value,16)
   values[info['messageKeys'][key]]=CString(value) if isinstance(value,str) else Int32(int(value))
  service.send_message(uuid.UUID(info['uuid']),values);time.sleep(.7)
  send_data_to_qemu(pebble.transport,QemuBattery(percent=80,charging=False))
  target=datetime.datetime(2026,10,19,10,10,35)
  command._set_time(pebble,target);time.sleep(.35)
  send_data_to_qemu(pebble.transport,QemuTap(axis=QemuTap.Axis.X,direction=1));time.sleep(.3)
  command._set_time(pebble,target);time.sleep(.2)
  pixels=command._grab_processed_image(argparse.Namespace(no_correction=False,scale=1),show_progress=False)
  path=OUT/(name+'.png');png.from_array(pixels,mode='RGBA;8').save(str(path))
  records.append({'file':path.name,'theme':theme,'density':density,'settings':settings,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()});print('Captured '+name,flush=True)
finally:
 if service:service.shutdown()
 if pebble:
  try:pebble.transport.disconnect()
  except Exception:pass
 cli(['kill']);log.close();assert hashlib.sha256(PBW.read_bytes()).hexdigest()==expected
 (OUT/'provenance.json').write_text(json.dumps({'pbw_sha256':expected,'version':'1.1.0','platform':'emery','capture':'Native SDK screenshots using the same ScreenshotCommand processing as pebble screenshot; persistent emulator connection; simulated 10:10 time, 80% battery and 6432 steps; no physical watch touched','captures':records},indent=2)+'\n')
