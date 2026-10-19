"""Select a native minimal-to-rich gallery, reusing verified emulator captures."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[2];STORE=ROOT/'store';EVIDENCE=STORE/'evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
minimal=json.loads((EVIDENCE/'minimal-screenshot-provenance.json').read_text())
medium=json.loads((EVIDENCE/'medium-screenshot-provenance.json').read_text())
assert minimal['scratch_data_restored'] and medium['scratch_data_restored']
assert len(medium['captures'])==7
approval=json.loads((EVIDENCE/'gate-a-approval.json').read_text())
records=[]
def existing(platform,filename,level,provenance):
 rec=next(c for c in provenance['captures'] if c['file']==filename)
 p=STORE/'screenshots'/filename;assert sha(p)==rec['sha256']
 records.append({'platform':platform,'file':filename,'level':level,'sha256':sha(p),'configuration':rec,'capture_source':('medium' if provenance is medium else 'minimal')+'-screenshot-provenance.json'})
def rich(platform,oldname,newname):
 p=EVIDENCE/'previous-screenshots'/oldname
 assert sha(p)==approval['approved_asset_sha256']['screenshots/'+oldname]
 shutil.copyfile(p,STORE/'screenshots'/newname)
 records.append({'platform':platform,'file':newname,'level':'rich','sha256':sha(p),'capture_source':'screenshot-provenance.json','original_file':oldname,'configuration':'Top digital time, left battery, bottom steps where supported, date and battery markers; Sunset also has thick hands and 40% battery. Native emulator image, copied without edits.'})
existing('emery','emery-01-classic-minimal.png','minimal',minimal)
existing('emery','emery-02-neon-date-only.png','light',minimal)
existing('emery','emery-03-ocean-medium.png','medium',medium)
rich('emery','emery-04-paper.png','emery-04-paper-rich.png')
rich('emery','emery-06-sunset-thick-40.png','emery-05-sunset-rich.png')
for p in ['gabbro','chalk','basalt','aplite','diorite','flint']:
 existing(p,p+'-classic-minimal.png','minimal',minimal)
 existing(p,p+'-classic-medium.png','medium',medium)
 rich(p,p+'-classic.png',p+'-classic-rich.png')
active={x['file'] for x in records};archive=EVIDENCE/'previous-screenshots/minimal-only';archive.mkdir(exist_ok=True)
for p in (STORE/'screenshots').glob('*.png'):
 if p.name not in active:shutil.move(p,archive/p.name)
(STORE/'screenshot-selection.json').write_text(json.dumps({'instruction':'An assortment of minimalistic, medium-richness and super-rich screenshots.','captures':records,'count':len(records),'emery_count':5,'other_platform_count_each':3,'screenshots_native_unscaled':True,'pbw_sha256':sha(ROOT/'build/thin-plus.pbw')},indent=2)+'\n')
for src,dst in [('emery-03-ocean-medium.png','emery-medium.png'),('emery-05-sunset-rich.png','emery-rich.png')]:shutil.copyfile(STORE/'screenshots'/src,ROOT/'screenshots'/dst)
print('Selected',len(records),'native images; five Emery, three each on six other platforms.')
