"""Compose the Emery banner with the untouched, native-size emulator capture."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--face',type=Path,default=ROOT/'store/screenshots/emery-01-classic-minimal.png')
parser.add_argument('--output',type=Path,default=ROOT/'store/banner-emery-720x320.png')
args=parser.parse_args()
im=Image.new('RGB',(720,320),'#080B10')
d=ImageDraw.Draw(im)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',76)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
d.text((48,86),'Thin',font=font,fill='#F5F3EC')
x=48+d.textlength('Thin',font=font)
d.text((x,86),'+',font=font,fill='#FFAA00')
tagline_lines=['The Thin you love.', 'More ways to make it yours.']
for i,line in enumerate(tagline_lines):
    assert d.textlength(line,font=small)<350
    d.text((52,184+i*28),line,font=small,fill='#B5BBC4')
d.line((52,255,112,255),fill='#FFAA00',width=2)
face=Image.open(args.face).convert('RGB')
assert face.size==(200,228)
d.rounded_rectangle((451,35,673,285),radius=16,fill='#161B22',outline='#303844',width=1)
im.paste(face,(462,46))
im.save(args.output)
