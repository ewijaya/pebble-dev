"""Draw Thin+'s original geometric icon; no upstream artwork is used."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]

def icon(size, menu=False):
    scale = 1 if menu else 4
    im = Image.new('RGBA' if menu else 'RGB', (size*scale, size*scale), (0,0,0,0) if menu else '#080B10')
    d = ImageDraw.Draw(im)
    s = size*scale/100
    def xy(values): return tuple(round(v*s) for v in values)
    white = '#FFFFFF' if menu else '#F5F3EC'
    width = max(1,round(2.6*s))
    if menu:
        # Keep the embedded icon identical to the approved release candidate.
        d.arc(xy((10,10,90,90)), 65, 355, fill=white, width=width)
    else:
        # Rectangular PT2 face, open at the lower right for the orange plus.
        d.line(xy((58,91,15,91,15,9,83,9,83,57)), fill=white, width=width)
        for marker in [(49,9,49,16),(15,49,22,49),(83,49,76,49),(49,91,49,84)]:
            d.line(xy(marker), fill=white, width=width)
    d.line(xy((31,35,50,50,68,25)), fill=white, width=width)
    d.ellipse(xy((47,47,53,53)), fill=white)
    plus = white if menu else '#FFAA00'
    d.line(xy((77,64,77,90)), fill=plus, width=max(1,round(4*s)))
    d.line(xy((64,77,90,77)), fill=plus, width=max(1,round(4*s)))
    if scale > 1: im = im.resize((size,size), Image.Resampling.LANCZOS)
    return im

for size in (80,144): icon(size).save(ROOT / f'store/icons/thin-plus-{size}.png')
menu = icon(25, True)
menu.save(ROOT/'resources/images/menu_icon.png')
menu.save(ROOT/'store/icons/menu-icon-25.png')
