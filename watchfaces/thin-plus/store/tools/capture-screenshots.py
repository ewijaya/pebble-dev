"""Capture minimal layouts, or --medium layouts, without touching the release PBW."""
from pathlib import Path
import hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile, time

def interrupted(signum, frame):
    raise KeyboardInterrupt
signal.signal(signal.SIGTERM, interrupted)
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'store/screenshots'
EVIDENCE = ROOT/'store/evidence'
assert sys.argv[1:] in ([], ['--medium']), 'Usage: capture-screenshots.py [--medium]'
mode = 'medium' if sys.argv[1:] else 'minimal'
SCRATCH = Path(tempfile.mkdtemp(prefix='thin-plus-'+mode+'-'))/'thin-plus'
shutil.copytree(ROOT, SCRATCH, ignore=shutil.ignore_patterns('build','store','screenshots','.lock-waf*'))
DATA = SCRATCH/'src/c/modules/data.c'
original = DATA.read_text()
pbw_hash = hashlib.sha256((ROOT/'build/thin-plus.pbw').read_bytes()).hexdigest()
js = (ROOT/'src/pkjs/custom-clay.js').read_text()
keys = re.findall(r"'([^']+)'", re.search(r'var COLOR_KEYS = \[(.*?)\];',js,re.S).group(1))
themes = {name: re.findall(r"'([0-9A-F]+)'", values) for name, values in re.findall(r"(\w+): \[([^\]]+)\]",js)}
env = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy', SDL_RENDER_DRIVER='software', PYTHONUNBUFFERED='1')

def run(args, log):
    with (EVIDENCE/log).open('a') as f:
        f.write('\nCOMMAND: '+' '.join(args)+'\n'); f.flush()
        subprocess.run(args,cwd=SCRATCH,env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=120)

def variant(platform,name,theme='classic',slots=('None','None','None'),date=False,seconds=False,thick=False,battery_markers=False,battery=80):
    return dict(platform=platform,name=name,theme=theme,slots=slots,date=date,seconds=seconds,thick=thick,battery_markers=battery_markers,battery=battery)

variants=[
    variant('emery','emery-01-classic-minimal'),
    variant('emery','emery-02-neon-date-only','neon',date=True),
    variant('emery','emery-03-ocean-steps-only','ocean',slots=('None','None','Steps'),seconds=True),
    variant('emery','emery-04-paper-digital-only','paper',slots=('Time','None','None')),
    variant('emery','emery-05-sunset-battery-only','sunset',slots=('None','Battery','None'),seconds=True,thick=True,battery_markers=True,battery=40),
]+[variant(p,p+'-classic-minimal') for p in ['gabbro','chalk','basalt','aplite','diorite','flint']]
if mode == 'medium':
    variants=[variant('emery','emery-03-ocean-medium','ocean',slots=('Time','None','Steps'))]+[
        variant(p,p+'-classic-medium',slots=('Time','None','None'),date=True)
        for p in ['gabbro','chalk','basalt','aplite','diorite','flint']]
records=[]
last=None
provenance=EVIDENCE/(mode+'-screenshot-provenance.json')
previous={r['file']:r for r in json.loads(provenance.read_text()).get('captures',[])} if provenance.exists() else {}
try:
    for v in variants:
        platform,name,theme=v['platform'],v['name'],v['theme']
        filename=name+'.png'
        if filename in previous and (OUT/filename).exists():
            assert hashlib.sha256((OUT/filename).read_bytes()).hexdigest()==previous[filename]['sha256']
            records.append(previous[filename]);continue
        colors='\n'.join(f'  if (key == MESSAGE_KEY_{k}) return PBL_IF_COLOR_ELSE(GColorFromHEX(0x{c}), {"GColorBlack" if k in ("ColorBackground","ColorBatteryEmpty") else "GColorWhite"}); // TEMP_TEST' for k,c in zip(keys,themes[theme]))
        slots='\n'.join(f'  if (key == MESSAGE_KEY_{k}) return SlotType{value}; // TEMP_TEST' for k,value in zip(['SlotTop','SlotLeft','SlotBottom'],v['slots']))
        enables='\n'.join(f'  if (key == MESSAGE_KEY_{k}) return {str(value).lower()}; // TEMP_TEST' for k,value in [('EnableDate',v['date']),('EnableBT',False),('EnableBattery',v['battery_markers']),('EnableSecondHand',v['seconds']),('EnableThickHands',v['thick'])])
        DATA.write_text(original.replace('GColor data_get_color(uint32_t key) {','GColor data_get_color(uint32_t key) {\n'+colors).replace('SlotType data_get_slot(uint32_t key) {','SlotType data_get_slot(uint32_t key) {\n'+slots).replace('bool data_get_enable(uint32_t key) {','bool data_get_enable(uint32_t key) {\n'+enables))
        log='capture-'+name+'.log'
        run(['pebble','build'],log)
        if last!=platform:run(['pebble','kill'],log)
        run(['pebble','install','--emulator',platform,'build/thin-plus.pbw'],log)
        if v['battery_markers'] or 'Battery' in v['slots']:
            run(['pebble','emu-battery','--emulator',platform,'--percent',str(v['battery'])],log)
        if 'Steps' in v['slots']:run(['pebble','emu-steps','--emulator',platform,'6432'],log)
        if v['seconds']:run(['pebble','emu-tap','--emulator',platform],log)
        time.sleep(2)
        run(['pebble','screenshot','--emulator',platform,'--no-open',str(OUT/filename)],log)
        records.append(dict(v,file=filename,sha256=hashlib.sha256((OUT/filename).read_bytes()).hexdigest(),capture='native, unscaled emulator PNG; scratch getter overrides; live emulator clock'))
        provenance.write_text(json.dumps({'scratch_path':str(SCRATCH),'scratch_data_restored':False,'captures':records},indent=2)+'\n')
        last=platform;print('Captured '+name,flush=True)
finally:
    DATA.write_text(original)
    assert 'TEMP_TEST' not in DATA.read_text()
    assert (ROOT/'src/c/modules/data.c').read_text()==original
    assert hashlib.sha256((ROOT/'build/thin-plus.pbw').read_bytes()).hexdigest()==pbw_hash
    subprocess.run(['pebble','kill'],cwd=SCRATCH,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    provenance.write_text(json.dumps({'scratch_path':str(SCRATCH),'scratch_data_restored':True,'production_data_unchanged':True,'production_pbw_unchanged':True,'pbw_sha256':pbw_hash,'captures':records},indent=2)+'\n')
