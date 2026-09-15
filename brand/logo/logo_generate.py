from pathlib import Path
import re, subprocess, sys
ROOT=Path('brand/logo')
primary=ROOT/'primary'/'qiuheting-logo.svg'
s=primary.read_text(encoding='utf-8')
if '<image' in s.lower(): raise SystemExit('primary SVG still contains <image>')
if '<path' not in s.lower(): raise SystemExit('primary SVG has no <path>')
for folder,color in [('black','#111111'),('white','#ffffff')]:
    t=re.sub(r'fill="#[0-9a-fA-F]{6}"',f'fill="{color}"',s)
    (ROOT/folder/f'qiuheting-logo-{folder}.svg').write_text(t,encoding='utf-8')
for color in ['primary','black','white']:
    src=primary if color=='primary' else ROOT/color/f'qiuheting-logo-{color}.svg'
    t=src.read_text(encoding='utf-8')
    t=re.sub(r'viewBox="[^"]+"','viewBox="120 20 1010 655"',t,count=1)
    out=ROOT/'icon'/f'qiuheting-icon.svg' if color=='primary' else ROOT/'icon'/f'qiuheting-icon-{color}.svg'
    out.write_text(t,encoding='utf-8')
subprocess.check_call([sys.executable,'-m','pip','install','cairosvg','pillow','-q'])
import cairosvg
from PIL import Image
items=[
 (ROOT/'primary'/'qiuheting-logo.svg', ROOT/'primary'/'qiuheting-logo.png', ROOT/'primary'/'qiuheting-logo.jpg'),
 (ROOT/'black'/'qiuheting-logo-black.svg', ROOT/'black'/'qiuheting-logo-black.png', ROOT/'black'/'qiuheting-logo-black.jpg'),
 (ROOT/'white'/'qiuheting-logo-white.svg', ROOT/'white'/'qiuheting-logo-white.png', ROOT/'white'/'qiuheting-logo-white.jpg'),
 (ROOT/'icon'/'qiuheting-icon.svg', ROOT/'icon'/'qiuheting-icon.png', ROOT/'icon'/'qiuheting-icon.jpg'),
]
for svg,png,jpg in items:
    data=cairosvg.svg2png(url=str(svg),output_width=2000,output_height=2000)
    png.write_bytes(data)
    im=Image.open(png).convert('RGBA')
    bg=Image.new('RGB',im.size,'white'); bg.paste(im,mask=im.getchannel('A'))
    bg.save(jpg,quality=95,subsampling=0,optimize=True)
print('generated logo assets')
