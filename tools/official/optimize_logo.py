from pathlib import Path
from PIL import Image
import sys

src = Path(sys.argv[1])
out = Path(sys.argv[2])
max_size = int(sys.argv[3]) if len(sys.argv) > 3 else 256
img = Image.open(src).convert('RGBA')
img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
out.parent.mkdir(parents=True, exist_ok=True)
img.save(out, format='PNG', optimize=True, compress_level=9)
print(f'input={src} bytes={src.stat().st_size} dimensions={Image.open(src).size}')
print(f'output={out} bytes={out.stat().st_size} dimensions={img.size}')
