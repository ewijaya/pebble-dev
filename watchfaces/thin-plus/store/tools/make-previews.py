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

sheet([('emery-01-classic-signature.png','1 · Signature / Classic + teal ring'),('emery-02-classic-minimal.png','2 · Minimal / Classic'),('emery-03-ocean-weather.png','3 · Weather / Ocean'),('emery-04-paper-second-time.png','4 · Second time zone / Paper'),('emery-05-sunset-fitness.png','5 · Fitness / Sunset')],'Thin+ 1.3.0 · Your face, your information','preview-emery.png')
sheet([(p+'-classic-'+level+'.png',p.title()+' / '+level.title()) for p in ['gabbro','chalk','basalt','aplite','diorite','flint'] for level in ['minimal','medium','rich']],'Thin+ · Minimal, medium and rich on every platform','preview-platforms.png')
