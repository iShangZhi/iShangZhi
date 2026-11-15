"""Animate existing cyan highlights; retain the original composition and lettering."""
from pathlib import Path
from PIL import Image, ImageChops, ImageEnhance
import math

root = Path(__file__).resolve().parents[1]
source = Image.open(root / 'assets/human-ai-horizon.jpg').convert('RGB')
source.thumbnail((720, 405), Image.Resampling.LANCZOS)
w, h = source.size
# Restrict animation to existing cyan highlights above the mountain horizon.
mask = Image.new('L', source.size)
mask.putdata([int(min(255, max(0, min(g,b)-r-12)*5) * max(0, min(1, (h*.72-y)/(h*.10))))
    for y in range(h) for r,g,b in [*list(source.crop((0,y,w,y+1)).getdata())]])
bright = ImageEnhance.Brightness(source).enhance(1.65)
# A shared palette prevents frame-to-frame color flicker.
palette = Image.blend(source, bright, .12).quantize(colors=256)
frames=[]
for i in range(48):
    phase=i/48
    breath=.12+.22*(.5-.5*math.cos(phase*2*math.pi))
    center=(phase*1.5-.25)*w
    scan=Image.new('L',(w,1))
    scan.putdata([int(255*min(.8,breath+.45*math.exp(-((x-center)/(w*.065))**2))) for x in range(w)])
    alpha=ImageChops.multiply(mask,scan.resize((w,h)))
    frame=Image.composite(bright,source,alpha)
    frames.append(frame.quantize(palette=palette,dither=Image.Dither.FLOYDSTEINBERG))
frames[0].save(root/'assets/human-ai-horizon.gif',save_all=True,append_images=frames[1:],duration=120,loop=0,optimize=True,disposal=1)
print('GIF:', source.size, len(frames), 'frames; 5.76 second loop')
