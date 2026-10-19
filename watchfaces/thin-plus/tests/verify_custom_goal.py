#!/usr/bin/env python3
"""Custom goal checks over one SDK connection; native screenshot pixels, no fixture overrides.
Run with Pebble Tool's Python after installing the candidate on the emulator.
"""
import argparse, datetime, hashlib, json, queue, time, uuid, zipfile
from pathlib import Path
import png
from libpebble2.communication import PebbleConnection
from libpebble2.protocol.apps import AppRunState, AppRunStateStart, AppRunStateStop
from libpebble2.services.appmessage import AppMessageService, Int32, CString
from pebble_tool.commands.emucontrol import send_health_metric, HEALTH_METRIC_STEPS
from pebble_tool.commands.screenshot import ScreenshotCommand
from pebble_tool.sdk.emulator import ManagedEmulatorTransport
from pebble_tool.sdk import add_tools_to_path
from pebble_tool.util.logs import PebbleLogPrinter
parser=argparse.ArgumentParser()
parser.add_argument('platform');parser.add_argument('stage')
args=parser.parse_args()
add_tools_to_path()
root=Path(__file__).resolve().parents[1]
out=root/'dist/verification/1.3.0'/args.stage
with zipfile.ZipFile(out/'thin-plus.pbw') as bundle:info=json.loads(bundle.read('appinfo.json'))
app=uuid.UUID(info['uuid']);keys=info['messageKeys']
pebble=PebbleConnection(ManagedEmulatorTransport(args.platform));pebble.connect();pebble.run_async()
log=PebbleLogPrinter(pebble,force_colour=False)
messages=AppMessageService(pebble);acks=queue.Queue()
messages.register_handler('ack',lambda tid,target:acks.put((tid,True)) if target==app else None)
messages.register_handler('nack',lambda tid,target:acks.put((tid,False)) if target==app else None)
screenshot=ScreenshotCommand();screenshot.pebble=pebble
records=[];pixels={}
def settings(**values):
 print('Settings:',json.dumps(values),flush=True)
 tid=messages.send_message(app,{keys[k]:(CString(v) if isinstance(v,str) else Int32(int(v))) for k,v in values.items()})
 ack,ok=acks.get(timeout=15);assert ack==tid and ok, 'AppMessage was not acknowledged by Thin+: '+str((tid,ack,ok))
 time.sleep(.3)
def reopen():
 pebble.send_packet(AppRunState(data=AppRunStateStop(uuid=app)));time.sleep(1)
 pebble.send_packet(AppRunState(data=AppRunStateStart(uuid=app)));time.sleep(2)
def steps(value):
 send_health_metric(pebble.transport,HEALTH_METRIC_STEPS,value);time.sleep(1)
def capture(label):
 target=datetime.datetime(2026,10,19,10,35)
 screenshot._set_time(pebble,target);time.sleep(.35)
 screenshot._set_time(pebble,target);time.sleep(1.2)
 image=screenshot._grab_processed_image(argparse.Namespace(no_correction=False,scale=1),show_progress=False)
 path=out/(args.platform+'-'+label+'.png');png.from_array(image,mode='RGBA;8').save(str(path))
 pixels[label]=[list(row) for row in image]
 records.append({'case':label,'path':str(path.relative_to(root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 print('Captured '+str(path.relative_to(root)),flush=True)
def mask(label):
 # SDK screenshot correction maps GColorDarkCyan to this display RGB.
 return {(x//4,y) for y,row in enumerate(pixels[label]) for x in range(0,len(row),4) if row[x:x+3]==[87,165,162]}
try:
 time.sleep(2)
 settings(EnableDate=True,DateStyle='0',EnableBT=True,EnableBattery=False,EnableSecondHand=False,
  EnableThickHands=False,EnableStartupAnim=False,EnableStepRing=True,EnableEnhancedBT=False,
  EnableChargingColor=False,TapForSeconds=False,SlotTop='0',SlotLeft='0',SlotBottom='1',
  ColorBackground=0,ColorHourMinutes=0xAAAAAA,ColorNotches=0xFFFFFF,ColorHandTips=0xFFFFFF,
  ColorCenterDot=0xAA0000,ColorMonthDay=0xFFAA00,ColorDate=0xFFFFFF,ColorStepRing=0x00AAAA,
  StepGoalMode='1',CustomStepGoal=10000)
 for count,label in [(5000,'half'),(10000,'at-target'),(15000,'above-target')]:
  steps(count);capture('custom-10000-'+label)
 assert mask('custom-10000-at-target')==mask('custom-10000-above-target')
 assert 0 < len(mask('custom-10000-half')) < len(mask('custom-10000-at-target'))
 steps(5000);settings(StepGoalMode='0');capture('automatic')
 settings(StepGoalMode='1');capture('custom-restored')
 assert pixels['custom-10000-half']==pixels['custom-restored']
 settings(StepGoalMode='0',CustomStepGoal='1000.5',EnableDate=False);capture('invalid-rejected')
 assert pixels['custom-10000-half']==pixels['invalid-rejected']
 reopen();capture('custom-reopened')
 assert pixels['custom-10000-half']==pixels['custom-reopened']
 settings(EnableStepRing=False);capture('custom-ring-off');assert not mask('custom-ring-off')
 report={'platform':args.platform,'pbw_sha256':hashlib.sha256((out/'thin-plus.pbw').read_bytes()).hexdigest(),
  'method':'Production settings over SDK AppMessage with ACK, native SDK framebuffer captures, one connection; real close/open persistence.',
  'custom_target':10000,'half_steps':5000,'at_and_above_target_ring_pixels_identical':True,
  'restored_invalid_and_reopened_pixels_identical':True,'captures':records}
 (out/(args.platform+'-custom-goal-result.json')).write_text(json.dumps(report,indent=2)+'\n')
 print('PASS: custom goal, capped progress, mode switching, invalid packet rejection, persistence and ring off.',flush=True)
finally:
 messages.shutdown();log.stop()
