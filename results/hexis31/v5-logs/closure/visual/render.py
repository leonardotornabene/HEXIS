"""Raster previews of the existing SVGs, for visual inspection only."""
from pathlib import Path
import math
import subprocess
import xml.etree.ElementTree as ET

source = Path('/Users/leonardoTornabene/Projects/hormathos/results/hexis31/v3-seed0-v3006')
output = Path('/tmp/hormathos-v5-review/visual')
chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
for svg in sorted(source.glob('figure__*.svg')):
    node = ET.fromstring(svg.read_bytes())
    _, _, width, height = map(float, node.attrib['viewBox'].split())
    image_width = 1800
    image_height = math.ceil(image_width * height / width)
    preview = output/(svg.stem+'.html')
    preview.write_text('<html><body style="margin:0;background:white">'
        f'<img src="{svg.as_uri()}" style="width:{image_width}px;height:{image_height}px">'
        '</body></html>')
    result = subprocess.run([chrome, '--headless', '--disable-gpu',
        '--disable-background-networking', '--disable-sync', '--no-first-run',
        '--no-default-browser-check', '--user-data-dir=/tmp/hormathos-v5-review/chrome-preview',
        '--hide-scrollbars', '--force-device-scale-factor=1',
        f'--screenshot={output/(svg.stem+".png")}',
        f'--window-size={image_width},{image_height+30}', preview.as_uri()],
        capture_output=True, text=True, timeout=45)
    assert result.returncode==0, (svg.name,result.stderr)
    assert (output/(svg.stem+'.png')).stat().st_size>1000
    print(svg.name,'rendered',flush=True)
