#!/usr/bin/env python3
"""Arrange the six native R11 date-style captures without altering face pixels."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--stage', default='r11-centered')
args = parser.parse_args()
OUT = ROOT / 'dist/verification/1.3.0' / args.stage
font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font = ImageFont.truetype(font_path, 24)
title = ImageFont.truetype(font_path, 32)
board = Image.new('RGB', (1680, 1320), '#17191d')
draw = ImageDraw.Draw(board)
draw.text((30, 20), 'Thin+ 1.3.0 — Date style', font=title, fill='white')
draw.text((30, 68), 'Native emulator captures at 10:35, enlarged 2x. Full preserves the existing layout.', font=font, fill='#bbbbbb')
for row, (platform, name) in enumerate([('emery', 'Pebble Time 2'), ('gabbro', 'Round')]):
    for col, (case, label) in enumerate([('full', 'Full (default)'), ('day-only', 'Day only'), ('weekday-day', 'Weekday and day')]):
        capture = Image.open(OUT / (platform + '-date-' + case + '.png')).convert('RGB')
        capture = capture.resize((capture.width * 2, capture.height * 2), Image.Resampling.NEAREST)
        x, y = col * 560, 125 + row * 580
        draw.text((x + 25, y), name + ' · ' + label, font=font, fill='white')
        board.paste(capture, (x + (560 - capture.width) // 2, y + 44))
draw.text((30, 1280), 'Date style appears in settings only while Show current date is on.', font=font, fill='#bbbbbb')
board.save(OUT / 'date-style-review.png')
print(OUT / 'date-style-review.png')
