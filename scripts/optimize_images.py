"""Resize portfolio images for display and lightbox delivery."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "public" / "images"
PROJECTS = IMAGES / "projects"
THUMBS = PROJECTS / "thumbs"


def save_webp(im: Image.Image, path: Path, quality: int = 78) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, format="WEBP", quality=quality, method=6)


def fit_width(im: Image.Image, width: int) -> Image.Image:
    if im.width <= width:
        return im.convert("RGB")
    ratio = width / im.width
    size = (width, max(1, round(im.height * ratio)))
    return im.convert("RGB").resize(size, Image.Resampling.LANCZOS)


def crop_cover(im: Image.Image, width: int, height: int) -> Image.Image:
    src = im.convert("RGB")
    target_ratio = width / height
    src_ratio = src.width / src.height
    if src_ratio > target_ratio:
        new_w = round(src.height * target_ratio)
        left = (src.width - new_w) // 2
        src = src.crop((left, 0, left + new_w, src.height))
    else:
        new_h = round(src.width / target_ratio)
        top = (src.height - new_h) // 2
        src = src.crop((0, top, src.width, top + new_h))
    return src.resize((width, height), Image.Resampling.LANCZOS)


def main() -> None:
    THUMBS.mkdir(parents=True, exist_ok=True)

    # Hero portrait variants (4:5)
    headshot = Image.open(IMAGES / "headshot.webp")
    save_webp(crop_cover(headshot, 320, 400), IMAGES / "headshot-320.webp", quality=80)
    save_webp(crop_cover(headshot, 640, 800), IMAGES / "headshot-640.webp", quality=80)

    for path in sorted(PROJECTS.glob("*.webp")):
        im = Image.open(path)
        # Grid thumbnails: enough for ~850px display at 1x and sharp enough at 1.5x
        thumb = fit_width(im, 860)
        save_webp(thumb, THUMBS / path.name, quality=76)
        # Lightbox / full: cap oversized sources
        full = fit_width(im, 1280)
        if full.size != im.size:
            save_webp(full, path, quality=80)
        else:
            # recompress in place if still large on disk
            if path.stat().st_size > 90_000:
                save_webp(full, path, quality=78)

        print(
            f"{path.name}: full={Image.open(path).size} "
            f"{path.stat().st_size // 1024}KB | "
            f"thumb={Image.open(THUMBS / path.name).size} "
            f"{(THUMBS / path.name).stat().st_size // 1024}KB"
        )

    print("headshots:", list((IMAGES).glob("headshot-*.webp")))


if __name__ == "__main__":
    main()
