"""Review sheets only; the upload screenshots remain native and unmodified."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def sheet(names,title,path,cols=3):
    cell_w,cell_h=300,315
    rows=(len(names)+cols-1)//cols
    im=Image.new('RGB',(cols*cell_w,rows*cell_h+65),'#10151C')
    d=ImageDraw.Draw(im)
    d.text((24,20),title,font=ImageFont.truetype(FONT,24),fill='#F5F3EC')
    for i,(name,label) in enumerate(names):
        x=(i%cols)*cell_w; y=(i//cols)*cell_h+65
        face=Image.open(ROOT/'store/screenshots'/name).convert('RGBA')
        im.paste(face,(x+(cell_w-face.width)//2,y+10),face)
        d.text((x+16,y+278),label,font=ImageFont.truetype(FONT,15),fill='#D5DBE4')
    im.save(ROOT/'store'/path)

sheet([(f'emery-{i:02d}-{name}.png',label) for i,name,label in [(1,'classic-minimal','1 · Minimal / Classic'),(2,'neon-date-only','2 · Light / Neon'),(3,'ocean-medium','3 · Medium / Ocean'),(4,'paper-rich','4 · Rich / Paper'),(5,'sunset-rich','5 · Rich / Sunset / thick hands')]],'Thin+ · From minimal to fully loaded','preview-emery.png')
sheet([(p+'-classic-'+level+'.png',p.title()+' / '+level.title()) for p in ['gabbro','chalk','basalt','aplite','diorite','flint'] for level in ['minimal','medium','rich']],'Thin+ · Minimal, medium and rich on every platform','preview-platforms.png')
