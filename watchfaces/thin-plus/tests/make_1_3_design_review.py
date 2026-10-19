#!/usr/bin/env python3
"""Arrange native emulator pixels for the weather and step-ring design gate."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist/verification/1.3.0/design-options'
font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font = ImageFont.truetype(font_path, 22)
title = ImageFont.truetype(font_path, 30)
board = Image.new('RGB', (1120, 1370), '#17191d')
draw = ImageDraw.Draw(board)
draw.text((30, 20), 'Thin+ 1.3.0 — weather and step-goal ring', font=title, fill='white')
draw.text((30, 66), 'Native emulator captures, enlarged 2x without changing pixels.', font=font, fill='#bbbbbb')
draw.text((30, 100), 'Simulated weather 18°C · simulated goal 7,500 · ring color customizable', font=font, fill='#bbbbbb')
for row, (count, label) in enumerate([(3750, '50% of goal'), (7500, 'Goal reached')]):
    for col, (platform, name) in enumerate([('emery', 'Pebble Time 2'), ('gabbro', 'Round')]):
        capture = Image.open(OUT / (platform + '-weather-ring-' + str(count) + '.png')).convert('RGB')
        capture = capture.resize((capture.width * 2, capture.height * 2), Image.Resampling.NEAREST)
        x, y = col * 560, 155 + row * 590
        draw.text((x + 30, y), name + ' · ' + label, font=font, fill='white')
        board.paste(capture, (x + (560 - capture.width) // 2, y + 45))
draw.text((30, 1335), 'Proposal: weather stays blank when unavailable or over 3 hours old.', font=font, fill='#bbbbbb')
board.save(OUT / 'design-review.png')
print(OUT / 'design-review.png')
