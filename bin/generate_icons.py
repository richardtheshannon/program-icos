#!/usr/bin/env python
"""One-shot PWA icon generator. Idempotent — safe to re-run.

Produces icon-192.png, icon-512.png, icon-maskable.png in
static/icons/. Solid forest-green background (V003 --accent token,
sRGB approx #2C5F3F of oklch(0.38 0.07 145)), white "P" letterform
centered. Mirrors ritual's bin/generate_icons.php approach.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ACCENT_RGB = (0x2C, 0x5F, 0x3F)
GLYPH = "P"
ROOT = Path(__file__).resolve().parent.parent
DEST_DIR = ROOT / "static" / "icons"

FONT_CANDIDATES = [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]


def pick_font_path() -> str | None:
    for c in FONT_CANDIDATES:
        if Path(c).is_file():
            return c
    return None


def make_icon(size: int, dest: Path, content_inset_pct: int, font_path: str | None) -> None:
    img = Image.new("RGB", (size, size), ACCENT_RGB)
    draw = ImageDraw.Draw(img)
    content_box = int(size * content_inset_pct / 100)
    target = int(content_box * 0.7)

    if font_path is not None:
        font_px = max(8, target)
        for _ in range(8):
            font = ImageFont.truetype(font_path, font_px)
            bbox = draw.textbbox((0, 0), GLYPH, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            max_dim = max(text_w, text_h)
            if max_dim == 0:
                break
            if abs(max_dim - target) <= 1:
                break
            font_px = int(font_px * (target / max_dim))
            if font_px < 8:
                font_px = 8
                break
        font = ImageFont.truetype(font_path, font_px)
        bbox = draw.textbbox((0, 0), GLYPH, font=font)
        x = (size - (bbox[2] + bbox[0])) // 2
        y = (size - (bbox[3] + bbox[1])) // 2
        draw.text((x, y), GLYPH, fill=(255, 255, 255), font=font)
    else:
        # Pillow's default bitmap font — rough fallback.
        font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), GLYPH, font=font)
        x = (size - (bbox[2] + bbox[0])) // 2
        y = (size - (bbox[3] + bbox[1])) // 2
        draw.text((x, y), GLYPH, fill=(255, 255, 255), font=font)

    img.save(dest, "PNG")


def main() -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    font_path = pick_font_path()
    targets = [
        (192, 100, "icon-192.png"),
        (512, 100, "icon-512.png"),
        (512, 80, "icon-maskable.png"),
    ]
    for size, inset, name in targets:
        path = DEST_DIR / name
        make_icon(size, path, inset, font_path)
        print(f"wrote {name} ({path.stat().st_size} bytes)")
    print(f"Font: {font_path or '[built-in bitmap]'}")


if __name__ == "__main__":
    main()
