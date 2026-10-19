"""Exercise the frozen 1.1.0 PBW; no rebuilds, store writes or physical installs."""
from pathlib import Path
import hashlib,json,os,signal,subprocess,time,zipfile
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent;SCRATCH=Path(json.loads((OUT/'build-context.json').read_text())['scratch']);PBW=ROOT/'dist/releases/1.1.0/thin-plus.pbw';OLD=ROOT/'dist/releases/1.0.0/thin-plus.pbw';UUID='0e83e240-01b8-469b-a51b-b2a0e767fefb'
assert subprocess.run(['pgrep','-x','qemu-pebble'],capture_output=True).returncode==1,'Another emulator is running'
with zipfile.ZipFile(PBW) as z:keys=json.loads(z.read('appinfo.json'))['messageKeys']
env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',SDL_RENDER_DRIVER='software')
config=json.loads(subprocess.check_output(['node','-e','process.stdout.write(JSON.stringify(require("./src/pkjs/config")))'],cwd=ROOT,text=True));items={}
def walk(xs):
 for x in xs:
  if 'messageKey' in x:items[x['messageKey']]=x
  walk(x.get('items',[]))
walk(config);records=[]
def run(args,p):
 with (OUT/(p+'-commands.log')).open('a') as f:
  f.write('\nCOMMAND: '+' '.join(args)+'\n');f.flush();subprocess.run(args,cwd=SCRATCH,env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=120)
def configure(p,overrides=None,old=False):
 ints=[];strings=[]
 for k,item in items.items():
  if old and k=='BatteryOnlyWhenLow':continue
  value=(overrides or {}).get(k,item['defaultValue'])
  if item['type']=='color':value=int(value,16)
  target=strings if isinstance(value,str) else ints;target.append(str(keys[k])+'='+str(int(value) if isinstance(value,bool) else value))
 run(['pebble','send-app-message','--emulator',p,'--app-uuid',UUID,'--int']+ints+['--string']+strings,p)
def capture(p,label):
 path=OUT/(p+'-'+label+'.png');run(['pebble','screenshot','--emulator',p,'--no-open',str(path)],p)
 records.append({'platform':p,'case':label,'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()});(OUT/'emulator-captures.json').write_text(json.dumps(records,indent=2)+'\n')
settings={'EnableBattery':False,'EnableSecondHand':False,'EnableDate':False,'EnableBT':False,'SlotTop':'3','SlotLeft':'3','SlotBottom':'3'}
try:
 for p in ['emery','aplite','basalt','chalk','diorite','flint','gabbro']:
  run(['pebble','kill'],p)
  if p=='emery':
   run(['pebble','install','--emulator',p,str(OLD)],p);configure(p,settings,old=True)
   run(['pebble','emu-battery','--emulator',p,'--percent','20'],p)
  run(['pebble','install','--emulator',p,str(PBW)],p)
  if p=='emery':capture(p,'migration-option-off-20')
  configure(p)
  # Inspect default settings with a bounded crash-log observation.
  with (OUT/(p+'-runtime.log')).open('w') as f:
   proc=subprocess.Popen(['pebble','logs','--emulator',p,'--no-color'],cwd=SCRATCH,env=env,stdout=f,stderr=subprocess.STDOUT)
   try:
    time.sleep(22)
    if proc.poll() is not None:raise RuntimeError('Log stream exited early: '+p)
   finally:
    proc.send_signal(signal.SIGINT)
    try:proc.wait(timeout=5)
    except subprocess.TimeoutExpired:proc.kill();proc.wait()
  capture(p,'defaults')
  configure(p,dict(settings,BatteryOnlyWhenLow=True))
  low=10 if p in ['aplite','basalt','chalk','diorite'] else 19
  for percent,label in [(20,'20-hidden'),(low,str(low)+'-visible'),(20,'20-hidden-again')]:
   run(['pebble','emu-battery','--emulator',p,'--percent',str(percent)],p);capture(p,label)
  if p=='emery':
   run(['pebble','install','--emulator',p,str(PBW)],p);capture(p,'persisted-low-only-20')
   configure(p,dict(settings,BatteryOnlyWhenLow=False));capture(p,'option-off-20')
  print(p+': defaults, 22-second log observation and battery transitions captured',flush=True)
finally:
 run(['pebble','kill'],'cleanup')
 assert hashlib.sha256(PBW.read_bytes()).hexdigest()==json.loads((OUT/'pbw-validation.json').read_text())['sha256']
