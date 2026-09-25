"""Raster previews of the existing SVGs; kill Chrome once the PNG exists."""
from pathlib import Path
import math, subprocess, time, tempfile
import xml.etree.ElementTree as ET
source = Path('/Users/leonardoTornabene/Projects/hormathos/results/hexis31/v3-seed0-v3006')
output = Path('/tmp/hormathos-v5-review/visual')
chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
for svg in sorted(source.glob('figure__*.svg')):
    _, _, w, h = map(float, ET.fromstring(svg.read_bytes()).attrib['viewBox'].split())
    W = 2400; H = math.ceil(W*h/w)
    page = output/(svg.stem+'.html'); png = output/(svg.stem+'.png')
    png.unlink(missing_ok=True)
    page.write_text(f'<html><body style="margin:0;background:white"><img src="{svg.as_uri()}" style="width:{W}px;height:{H}px"></body></html>')
    p = subprocess.Popen([chrome,'--headless','--disable-gpu','--no-first-run',
        f'--user-data-dir={tempfile.mkdtemp()}','--hide-scrollbars','--force-device-scale-factor=1',
        f'--screenshot={png}',f'--window-size={W},{H}',page.as_uri()],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(120):
        time.sleep(0.5)
        if png.exists() and png.stat().st_size > 1000: time.sleep(1); break
    p.kill()
    print(svg.name, W, H, png.exists() and png.stat().st_size, flush=True)
