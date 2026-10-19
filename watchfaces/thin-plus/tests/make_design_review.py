#!/usr/bin/env python3
"""Label and enlarge native emulator captures for the owner's design gate."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT/'dist/verification/1.2.0'
OUT = EVIDENCE/'design-gate'
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)

def board(filename, title, columns):
    scale, width, cell_height = 3, 660, 780
    image = Image.new('RGB', (width*len(columns), 110+cell_height*2), '#17191d')
    draw = ImageDraw.Draw(image)
    draw.text((24,22), title, font=title_font, fill='white')
    draw.text((24,65), 'Emulator captures enlarged 3x; layout pixels unchanged.', font=font, fill='#bbbbbb')
    for row, platform in enumerate(['emery','chalk']):
        for col, (label, stage, case) in enumerate(columns):
            path = EVIDENCE/stage/(platform+'-'+case+'.png')
            capture = Image.open(path).convert('RGB')
            capture = capture.resize((capture.width*scale,capture.height*scale), Image.Resampling.NEAREST)
            x, y = col*width, 110+row*cell_height
            draw.text((x+24,y+12), label+' · '+platform, font=font, fill='white')
            image.paste(capture, (x+(width-capture.width)//2,y+60))
    image.save(OUT/filename)

board('disconnect-options.png', 'Disconnect indicator — choose A or B', [
    ('A: Larger ring', 'r3-final-ring', 'disconnected-enhanced'),
    ('B: Ring + Bluetooth-off glyph', 'r3-final-glyph', 'disconnected-enhanced')])
board('charging-review.png', 'Charging at 60% — filled markers change color', [
    ('Classic', 'r9', 'charging-60'),
    ('Paper', 'r9', 'paper-charging-60')])
print(OUT/'disconnect-options.png')
print(OUT/'charging-review.png')
