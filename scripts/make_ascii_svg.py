from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "data" / "source-prepped.png"
OUTPUT = ROOT / "avi-ascii.svg"

# Configuration
WIDTH = 100
RAMP = " .:-=+*#%@"

print("Generating ASCII portrait...")

if not INPUT.exists():
    raise FileNotFoundError(INPUT)

# Load image
img = Image.open(INPUT).convert("L")

# Improve contrast
img = ImageOps.autocontrast(img)
img = ImageEnhance.Contrast(img).enhance(1.8)

# Resize
height = int(img.height / img.width * WIDTH * 0.56)
img = img.resize((WIDTH, height), Image.Resampling.LANCZOS)

# Convert pixels to ASCII
pixels = img.load()

lines = []

for y in range(height):
    line = ""

    for x in range(WIDTH):
        brightness = pixels[x, y]

        # Bright pixels = dense characters
        index = int(brightness / 255 * (len(RAMP) - 1))

        line += RAMP[index]

    lines.append(line)

# SVG dimensions
CHAR_WIDTH = 8
CHAR_HEIGHT = 13

SVG_WIDTH = WIDTH * CHAR_WIDTH
SVG_HEIGHT = height * CHAR_HEIGHT

# Generate SVG
svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{SVG_WIDTH}" height="{SVG_HEIGHT}" '
    f'viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">',

    '<rect width="100%" height="100%" fill="#000000"/>',

    '<text xml:space="preserve" '
    'font-family="Courier New, monospace" '
    'font-size="12" fill="#FFFFFF">'
]

for i, line in enumerate(lines):
    svg.append(
        f'<tspan x="0" y="{(i + 1) * CHAR_HEIGHT}">'
        f'{html.escape(line)}</tspan>'
    )

svg.append('</text>')
svg.append('</svg>')

OUTPUT.write_text("\n".join(svg), encoding="utf-8")

print("SUCCESS!")
print(f"Generated: {OUTPUT}")
print(f"Dimensions: {WIDTH} x {height}")
