#!/usr/bin/env python3
"""
Build the 1200x630 Open Graph card.

    python3 tools/make-images.py     (needs Pillow: python3 -m pip install Pillow)

Favicons and app icons are NOT generated here any more — they are the
designer's favicon_io set, copied verbatim by tools/brand-assets.py. This
module only composes the social card, and it places the supplied logo whole and
unmodified (resized only) beside the service list.

Run tools/brand-assets.py first; this reads assets/img/brand/logo-1200.png.
"""

import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install Pillow")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "img")
LOGO = os.path.join(ROOT, "assets", "img", "brand", "logo-1200.png")

INK = (11, 11, 12)
RED = (224, 27, 36)
CHROME = (243, 245, 248)
MUTED = (154, 162, 171)

DISPLAY = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
BODY_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
BODY = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def fit(d, text, path, start_size, max_w):
    """Largest size at or below `start_size` that keeps `text` inside `max_w`.
    The service list is long and the card is a fixed width, so this is measured
    rather than guessed."""
    size = start_size
    while size > 12:
        f = font(path, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 12)


def make_og():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    for x in range(0, W, 68):
        d.line([(x, 0), (x, H)], fill=(24, 26, 30), width=1)
    for y in range(0, H, 68):
        d.line([(0, y), (W, y)], fill=(24, 26, 30), width=1)

    if not os.path.exists(LOGO):
        sys.exit("run tools/brand-assets.py first — assets/img/brand/logo-1200.png missing")

    # The logo goes on whole. It is square with the designer's clear space
    # already around it, so it needs no padding of its own.
    logo = Image.open(LOGO).convert("RGBA")
    target = 470
    logo = logo.resize((target, target), Image.LANCZOS)
    img.paste(logo, (60, (H - target) // 2), logo)

    col_x = 60 + target + 20
    col_w = W - col_x - 70

    d.rectangle([col_x, 186, col_x + 150, 190], fill=RED)

    f_head = fit(d, "WINDOWS  ·  BATHS  ·  KITCHENS", DISPLAY, 54, col_w)
    for i, line in enumerate(["DECKS  ·  FENCING  ·  SIDING",
                              "WINDOWS  ·  BATHS  ·  KITCHENS"]):
        d.text((col_x, 218 + i * 64), line, font=f_head, fill=CHROME)

    f_foot = fit(d, "Licensed & fully insured  ·  Free written quotes", BODY, 22, col_w)
    d.text((col_x, 372), "Cornwall & Akwesasne, Ontario", font=f_foot, fill=MUTED)
    d.text((col_x, 404), "Licensed & fully insured  ·  Free written quotes",
           font=f_foot, fill=MUTED)
    d.text((col_x, 450), "elite-carpentry.ca", font=font(BODY_B, 24), fill=(255, 74, 82))

    d.rectangle([0, H - 16, W, H], fill=(19, 20, 23))
    for x in range(-40, W + 40, 24):
        d.polygon([(x, H), (x + 12, H), (x + 28, H - 16), (x + 16, H - 16)], fill=RED)

    img.save(os.path.join(OUT, "og-image.png"))
    kb = os.path.getsize(os.path.join(OUT, "og-image.png")) // 1024
    print(f"   og-image.png  1200x630  {kb} KB  (supplied logo, unmodified)")


def main():
    os.makedirs(OUT, exist_ok=True)
    print("Building the social card:")
    make_og()


if __name__ == "__main__":
    main()
