from pathlib import Path
script=Path('/home/ubuntu/projects/pebble-dev/watchfaces/thin-plus/store/releases/1.1.0/verify-emulators.py')
ns={'__file__':str(script)};exec(script.read_text().split('\ntry:\n')[0],ns)
ns['records']=ns['json'].loads((ns['OUT']/'emulator-captures.json').read_text())
run=ns['run'];configure=ns['configure'];capture=ns['capture'];p='emery'
try:
 run(['pebble','install','--emulator',p,str(ns['PBW'])],p)
 configure(p,dict(ns['settings'],BatteryOnlyWhenLow=True))
 run(['pebble','emu-battery','--emulator',p,'--percent','20'],p)
 run(['pebble','install','--emulator',p,str(ns['PBW'])],p)
 ns['time'].sleep(3)
 capture(p,'persisted-low-only-20-settled')
 run(['pebble','emu-battery','--emulator',p,'--percent','19'],p)
 capture(p,'persisted-low-only-19-settled')
 print('Persisted option rechecked after startup animation: 20 hidden, 19 visible.',flush=True)
finally:run(['pebble','kill'],'cleanup')
