"""Render exact, monochrome organization-profile art for KidResume."""

from pathlib import Path
import math
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


def contour_path(cx, cy, rx, ry, phase, lobes=5, points=180):
    coords = []
    for index in range(points + 1):
        angle = 2 * math.pi * index / points
        modulation = 1 + 0.075 * math.sin(lobes * angle + phase) + 0.035 * math.cos(3 * angle - phase)
        x = cx + rx * modulation * math.cos(angle)
        y = cy + ry * modulation * math.sin(angle)
        coords.append((x, y))
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in coords) + " Z"


def svg_header(title, subtitle, height):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{height}" viewBox="0 0 1600 {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{subtitle}</desc>
<defs>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#111" stroke-opacity=".10" stroke-width="1"/></pattern>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0 0L9 3L0 6Z" fill="#111"/></marker>
  <style>text{{font-family:Arial,Helvetica,sans-serif;fill:#111}} .mono{{font-family:'Courier New',monospace}} .label{{font-size:18px;font-weight:700;letter-spacing:2px}} .small{{font-size:16px}} .contour{{fill:none;stroke:#111;stroke-width:1.5}} .vector{{fill:none;stroke:#111;stroke-width:2;marker-end:url(#arrow)}}</style>
</defs><rect width="1600" height="{height}" fill="#f8f8f5"/><rect width="1600" height="{height}" fill="url(#grid)"/>'''


def math_hero_svg():
    contours = "".join(
        f'<path class="contour" opacity="{0.25 + i * 0.055:.2f}" d="{contour_path(1265, 326, 285-i*18, 245-i*15, i*.37, 5)}"/>'
        for i in range(13)
    )
    arrows = []
    for row in range(5):
        for col in range(6):
            x, y = 1020 + col * 92, 145 + row * 88
            dx, dy = 46 + row * 4, (-18 + col * 7)
            arrows.append(f'<path class="vector" opacity=".46" d="M{x} {y}l{dx} {dy}"/>')
    svg = svg_header("KidResume mathematical editorial hero", "A coordinate grid, contour field and evidence-to-resume vector equation", 640)
    svg += f'''<rect x="0" y="0" width="26" height="640" fill="#d0f000"/>
<text x="80" y="78" class="label">KIDRESUME / SYSTEM 01</text>
<text x="80" y="205" font-size="92" font-weight="700">TRUTH,</text>
<text x="80" y="300" font-size="92" font-weight="700">BY DESIGN.</text>
<text x="84" y="362" class="mono" font-size="24">CV = Σ(verified evidence × clear language) + controlled design</text>
<path d="M84 405H850" stroke="#111" stroke-width="3" marker-end="url(#arrow)"/>
<text x="84" y="451" class="small">INPUT VECTOR</text><text x="350" y="451" class="small">FACTUALITY GATE</text><text x="650" y="451" class="small">OWNED OUTPUT</text>
<text x="84" y="535" class="mono" font-size="17">v₀ = [school, subjects, activities, tools, portrait]</text>
<text x="84" y="568" class="mono" font-size="17">T(v₀) → [PDF, PNG, JSON]  where unsupported claims = 0</text>
{contours}{''.join(arrows)}
<circle cx="1265" cy="326" r="9" fill="#d0f000" stroke="#111" stroke-width="3"/>
<text x="1150" y="600" class="label">EVIDENCE FIELD</text></svg>'''
    (OUT / "kidresume-math-hero.svg").write_text(svg, encoding="utf-8")


def proof_vector_svg():
    svg = svg_header("KidResume proof vector", "A formal visual proof of the product path from user facts to downloadable files", 620)
    nodes = [
        (95, "x₀", "LEARNER FACTS", "closed-world input"),
        (415, "E(x)", "EVIDENCE", "source-linked claims"),
        (735, "Q(E)", "QUALITY GATES", "truth + language + layout"),
        (1055, "R(Q)", "RENDER", "deterministic HTML/CSS"),
        (1375, "y", "OWNED FILES", "PDF + PNG + JSON"),
    ]
    svg += '<text x="70" y="75" class="label">THE RESUME TRANSFORMATION</text><text x="70" y="120" class="mono" font-size="21">y = R(Q(E(x₀)))   subject to: fabrication = 0, payment verified = 1, owner(session) = true</text>'
    for i, (x, symbol, title, note) in enumerate(nodes):
        svg += f'<circle cx="{x}" cy="300" r="78" fill="#f8f8f5" stroke="#111" stroke-width="3"/><circle cx="{x}" cy="300" r="60" fill="none" stroke="#111" stroke-width="1" stroke-dasharray="4 7"/><text x="{x}" y="312" text-anchor="middle" class="mono" font-size="31" font-weight="700">{symbol}</text><text x="{x}" y="420" text-anchor="middle" class="label">{title}</text><text x="{x}" y="455" text-anchor="middle" class="small">{note}</text>'
        if i < len(nodes)-1:
            nx = nodes[i+1][0]
            svg += f'<path d="M{x+82} 300H{nx-86}" class="vector"/><text x="{(x+nx)/2}" y="278" text-anchor="middle" class="mono" font-size="16">T{i+1}</text>'
    svg += '<path d="M70 520H1530" stroke="#111" stroke-width="2"/><text x="70" y="566" class="mono" font-size="18">Invariant: design changes arrangement, never biography.  ∂content/∂whitespace = 0</text></svg>'
    (OUT / "kidresume-proof-vector.svg").write_text(svg, encoding="utf-8")


def contour_manifesto_svg():
    svg = svg_header("KidResume contour manifesto", "Four product principles set against mathematical contours and vector annotations", 520)
    contours = "".join(f'<path class="contour" opacity=".55" d="{contour_path(800, 260, 720-i*33, 205-i*10, i*.23, 7)}"/>' for i in range(15))
    svg += contours
    items = [(160, "01", "TRUTH", "claims ∈ verified evidence"), (530, "02", "OWNERSHIP", "files → learner"), (900, "03", "PRIVACY", "PII exposure → minimum"), (1270, "04", "ACCESS", "phone ≤ viewport ≤ TV")]
    for x, num, title, note in items:
        svg += f'<rect x="{x-85}" y="160" width="270" height="210" fill="#f8f8f5" stroke="#111" stroke-width="3"/><rect x="{x-85}" y="160" width="270" height="18" fill="#d0f000"/><text x="{x-55}" y="225" class="mono" font-size="22">{num}</text><text x="{x-55}" y="282" class="label">{title}</text><text x="{x-55}" y="328" class="mono" font-size="15">{note}</text>'
    svg += '<text x="80" y="470" class="mono" font-size="17">Quality is a constrained system: useful output = verified facts + legible structure + accountable delivery.</text></svg>'
    (OUT / "kidresume-contour-manifesto.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    hero(); path(); principles(); math_hero_svg(); proof_vector_svg(); contour_manifesto_svg()
    print(f"Rendered public profile assets in {OUT}")
