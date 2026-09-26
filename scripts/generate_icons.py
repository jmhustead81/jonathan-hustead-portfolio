"""Generate JH brand icons for favicon, Apple touch, and PWA."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ICONS = PUBLIC / "icons"

BG = (16, 19, 24, 255)
FG = (155, 196, 191, 255)


def load_font(size: int) -> ImageFont.ImageFont:
    for path in (
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\seguisb.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_mark(size: int) -> Image.Image:
    """Draw a JH monogram on a rounded dark square."""
    scale = 4
    canvas = size * scale
    im = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    radius = int(canvas * 0.18)
    draw.rounded_rectangle([0, 0, canvas - 1, canvas - 1], radius=radius, fill=BG)

    font = load_font(int(canvas * 0.42))
    text = "JH"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (canvas - tw) / 2 - bbox[0]
    y = (canvas - th) / 2 - bbox[1] - canvas * 0.03
    draw.text((x, y), text, font=font, fill=FG)

    return im.resize((size, size), Image.Resampling.LANCZOS)


def write_svg() -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Jonathan Hustead">
  <rect width="64" height="64" rx="12" fill="#101318"/>
  <text x="32" y="43" text-anchor="middle" font-family="Arial Black, Arial, Helvetica, sans-serif" font-size="26" font-weight="700" letter-spacing="-1.2" fill="#9BC4BF">JH</text>
</svg>
"""
    (PUBLIC / "favicon.svg").write_text(svg, encoding="utf-8")


def main() -> None:
    ICONS.mkdir(parents=True, exist_ok=True)

    write_svg()

    sizes = {
        16: ICONS / "favicon-16x16.png",
        32: ICONS / "favicon-32x32.png",
        48: ICONS / "favicon-48x48.png",
        180: PUBLIC / "apple-touch-icon.png",
        192: ICONS / "icon-192.png",
        512: ICONS / "icon-512.png",
    }

    rendered = {size: draw_mark(size) for size in sizes}
    for size, path in sizes.items():
        rendered[size].save(path, format="PNG", optimize=True)

    # Multi-resolution ICO for browsers that ignore SVG
    ico = draw_mark(48)
    ico.save(
        PUBLIC / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )

    # Cleanup temp check file if present
    check = PUBLIC / "favicon-check.png"
    if check.exists():
        check.unlink()

    print("Generated icons:")
    for path in [
        PUBLIC / "favicon.svg",
        PUBLIC / "favicon.ico",
        PUBLIC / "apple-touch-icon.png",
        *sizes.values(),
    ]:
        print(f"  {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
