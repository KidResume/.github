"""Render exact, monochrome organization-profile art for KidResume."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(parents=True, exist_ok=True)
REGULAR = next(path for path in ("C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf") if Path(path).exists())
BOLD = next(path for path in ("C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") if Path(path).exists())


def face(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


def one_bit(image, name):
    image.convert("1", dither=Image.Dither.FLOYDSTEINBERG).save(OUT / name, optimize=True)


def hero():
    im = Image.new("L", (2400, 760), 255)
    d = ImageDraw.Draw(im)
    for y in range(0, 760, 12):
        shade = 232 if (y // 12) % 2 == 0 else 250
        d.rectangle((0, y, 2400, y + 5), fill=shade)
    d.rectangle((0, 0, 44, 760), fill=0)
    d.rectangle((1970, 0, 2400, 760), fill=0)
    d.text((130, 110), "K", font=face(180, True), fill=0)
    d.text((130, 300), "KIDRESUME", font=face(132, True), fill=0)
    d.text((140, 470), "TRUTHFUL CVS. BETTER FIRST STEPS.", font=face(43, True), fill=0)
    d.text((140, 550), "SOUTH AFRICAN YOUTH  /  GUIDED EVIDENCE  /  PDF + PNG", font=face(28), fill=40)
    d.text((2035, 220), "01", font=face(58, True), fill=255)
    d.text((2035, 300), "LEARN", font=face(32, True), fill=255)
    d.text((2035, 350), "BUILD", font=face(32, True), fill=255)
    d.text((2035, 400), "APPLY", font=face(32, True), fill=255)
    one_bit(im, "kidresume-hero-1bit.png")


def path():
    im = Image.new("L", (2400, 650), 255)
    d = ImageDraw.Draw(im)
    d.text((80, 55), "ONE LEARNER. ONE VERIFIED STORY. ONE OWNED RESULT.", font=face(44, True), fill=0)
    labels = [("01", "LEARNER INPUT", "School • skills • activity • photo"), ("02", "EVIDENCE", "Supported facts only"), ("03", "CONTROLLED DESIGN", "Selected template • A4 layout"), ("04", "DELIVERY", "PDF • PNG • approved revision")]
    x = 80
    for i, (num, title, note) in enumerate(labels):
        d.rectangle((x, 180, x + 480, 490), outline=0, width=5)
        d.rectangle((x, 180, x + 480, 230), fill=0)
        d.text((x + 22, 188), num, font=face(26, True), fill=255)
        d.text((x + 24, 275), title, font=face(30, True), fill=0)
        words = note.split(" • ")
        for j, word in enumerate(words):
            d.text((x + 24, 345 + j * 42), word, font=face(23), fill=0)
        if i < 3:
            d.line((x + 480, 335, x + 560, 335), fill=0, width=6)
            d.polygon([(x + 560, 335), (x + 535, 320), (x + 535, 350)], fill=0)
        x += 580
    one_bit(im, "kidresume-path-1bit.png")


def principles():
    im = Image.new("L", (2400, 560), 255)
    d = ImageDraw.Draw(im)
    labels = [("TRUTH", "No invented claims"), ("OWNERSHIP", "Downloadable files"), ("PRIVACY", "Strict data boundaries"), ("ACCESS", "Phone to large screen")]
    for i, (title, note) in enumerate(labels):
        x = 80 + i * 580
        for row in range(18):
            for col in range(18):
                if (row + col + i) % 3 == 0:
                    d.rectangle((x + col * 16, 80 + row * 16, x + col * 16 + 8, 88 + row * 16), fill=0)
        d.rectangle((x + 315, 80, x + 500, 265), fill=0)
        d.text((x, 380), title, font=face(31, True), fill=0)
        d.text((x, 430), note, font=face(24), fill=0)
    one_bit(im, "kidresume-principles-1bit.png")


if __name__ == "__main__":
    hero(); path(); principles()
    print(f"Rendered public profile assets in {OUT}")
