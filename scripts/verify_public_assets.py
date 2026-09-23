"""Validate the public profile images without platform-specific font hashes."""

from pathlib import Path
from PIL import Image

EXPECTED = {
    "kidresume-hero-1bit.png": (2400, 760),
    "kidresume-path-1bit.png": (2400, 650),
    "kidresume-principles-1bit.png": (2400, 560),
}
EXPECTED_SVG = {
    "kidresume-math-hero.svg": "TRUTH,",
    "kidresume-proof-vector.svg": "THE RESUME TRANSFORMATION",
    "kidresume-contour-manifesto.svg": "Quality is a constrained system",
}

root = Path(__file__).resolve().parents[1] / "assets"
for name, size in EXPECTED.items():
    path = root / name
    if not path.is_file():
        raise SystemExit(f"Missing profile asset: {path}")
    with Image.open(path) as image:
        if image.size != size:
            raise SystemExit(f"Wrong dimensions for {name}: {image.size}, expected {size}")
        if image.mode != "1":
            raise SystemExit(f"{name} is {image.mode}, expected true 1-bit mode")
for name, marker in EXPECTED_SVG.items():
    path = root / name
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    if "<svg" not in text or marker not in text:
        raise SystemExit(f"Missing or invalid vector profile asset: {path}")
print("Public profile assets are present, correctly sized and true 1-bit images")
