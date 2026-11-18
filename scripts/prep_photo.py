import cv2
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "data" / "source-photo.png"
OUTPUT = ROOT / "data" / "source-prepped.png"

print("Preparing image...")

img = cv2.imread(str(INPUT))

if img is None:
    raise FileNotFoundError(INPUT)

h, w = img.shape[:2]

# Crop around the monkey
img = img[
    int(h * 0.02):int(h * 0.90),
    int(w * 0.05):int(w * 0.95)
]

# Grayscale
gray = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2GRAY
)

# Contrast enhancement
clahe = cv2.createCLAHE(
    clipLimit=2.5,
    tileGridSize=(8, 8)
)

gray = clahe.apply(gray)

# Reduce image noise
gray = cv2.GaussianBlur(
    gray,
    (3, 3),
    0
)

cv2.imwrite(str(OUTPUT), gray)

print("Image preprocessing complete!")