#!/usr/bin/env python3
"""
Publish the supplied brand package to the sizes the site needs.

    python3 tools/brand-assets.py

Source of truth is the designer's package in assets/img/brand/elitelogo/. The
only operations performed on it are RESIZE and, for the header lockup, CROP.
There is no redrawing, no recolouring, no re-typesetting, no shadow work and no
change to spacing inside any piece. Every pixel published is the designer's.

Two lockups, both cut from the same file:

  STACKED  the artwork whole, exactly as supplied, clear space intact. Used in
           the footer, the social card, and everywhere print/signage is needed.

  HORIZONTAL  the house+EC mark and the ELITE / CARPENTRY & RENOVATIONS block
           cropped apart and set side by side, for the header. APPROVED BY THE
           OWNER 2026-08-16 — see the note on the crop boxes below. Nothing
           else about the logo may change without asking him first.

Favicons are the supplied favicon_io set, copied verbatim — they are not
re-rendered from the PNG.

Outputs (assets/img/brand/):
  logo-1200, logo-480   .png and .webp   stacked, resize-only
  mark-192              .png and .webp   house + EC          (header, 64px)
  word-144              .png and .webp   ELITE + rule + sub  (header, 46px)
Outputs (assets/img/):
  favicon.ico, favicon-16x16.png, favicon-32x32.png,
  apple-touch-icon.png, android-chrome-192x192.png, android-chrome-512x512.png
"""

import os
import shutil
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install Pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "assets", "img", "brand", "elitelogo")
SRC = os.path.join(PKG, "PNG", "Artboard 1 copy.png")   # the transparent one
FAVDIR = os.path.join(PKG, "favicon_io")
BRAND = os.path.join(ROOT, "assets", "img", "brand")
IMG = os.path.join(ROOT, "assets", "img")

# The stacked lockup is painted at 200px (footer); 480 covers that past 2x, and
# 1200 is the copy the social card is composed around.
SIZES = (1200, 480)

FAVICONS = ("favicon.ico", "favicon-16x16.png", "favicon-32x32.png",
            "apple-touch-icon.png",
            "android-chrome-192x192.png", "android-chrome-512x512.png")

# --- The header crops -------------------------------------------------------
# These boxes are the ALPHA BOUNDING BOXES of the artwork's own bands, not
# hand-placed rectangles. The supplied 4501x4500 PNG separates into horizontal
# strips — house+EC, ELITE, red rule, sub-line — and rows 2759-2784 between the
# mark and the wordmark carry nothing but the mark's soft drop shadow (peak
# alpha 58, against 168-203 the moment real artwork starts). The split is taken
# at 2772, the middle of that shadow-only band, so each crop keeps its own half
# of the shadow and no letterform or keyline is touched.
#
# Verified by _assert_crops() on every run: if the artwork is ever re-exported
# at different proportions the build stops rather than shipping a silently
# mis-cut logo.
MARK_BOX = (685, 392, 3889, 2772)     # house + EC          3204 x 2380
WORD_BOX = (678, 2772, 3908, 3933)    # ELITE + rule + sub  3230 x 1161
SEAM = (2759, 2785)                   # shadow-only rows the split sits inside
SEAM_MAX_ALPHA = 96                   # observed 58; real artwork starts at 168

# Painted at 64px (mark) and 46px (word) in the header, so 3x covers retina.
# The word block is deliberately NOT at its stacked proportion (~31px against a
# 64px mark). A horizontal lockup gives the wordmark width, so it can carry the
# extra height — and it has to: 46px is where the sub-line's capitals reach
# ~8.5px and start reading as words instead of texture. At the stacked ratio it
# lands at 6.3px, which is the legibility problem this lockup exists to fix.
CROPS = (("mark", MARK_BOX, 192),
         ("word", WORD_BOX, 144))

# The header pair is the only brand image above the fold, so it is the only one
# whose bytes are on the critical path. WebP q86 rather than q92: measured
# against the uncompressed resize, mean channel error goes 2.89 -> 3.24 on the
# mark and 4.19 -> 4.78 on the wordmark — invisible on a chrome gradient — and
# it buys back ~4.5 KB. Spending that on resolution instead keeps the full 3x
# sampling, which the sub-line actually needs. The stacked lockup stays at q92:
# it is lazy-loaded in the footer and painted at 200px, so its bytes are free.
Q_HEADER = 86
Q_STACKED = 92


def _assert_crops(master):
    """Prove the crop boxes still match the artwork before cutting anything.

    The boxes were measured off the file as supplied. If the logo is ever
    re-exported at a different size or with the bands spaced differently, these
    coordinates would quietly slice through the middle of a letter and nobody
    would notice until it was live. So: check that each box is still exactly
    the alpha bounding box of its own band, and that the split between them
    still lands in rows carrying nothing but the mark's soft drop shadow. Fail
    loudly instead.
    """
    alpha = master.split()[3]
    if master.size != (4501, 4500):
        sys.exit(f"artwork is {master.width}x{master.height}, expected 4501x4500 — "
                 f"the header crop boxes in CROPS were measured off the original "
                 f"and must be re-measured. Do not guess; ask before changing them.")

    for name, box in (("mark", MARK_BOX), ("word", WORD_BOX)):
        strip = alpha.crop((0, box[1], master.width, box[3]))
        got = strip.getbbox()
        if got is None:
            sys.exit(f"{name} crop is empty — artwork has changed")
        got = (got[0], got[1] + box[1], got[2], got[3] + box[1])
        if got != box:
            sys.exit(f"{name} crop {box} is no longer the artwork's bounding box "
                     f"(now {got}) — re-measure before building")

    # The split must land in the shadow-only band. If real artwork has moved
    # into these rows, the crop would be slicing a letterform.
    seam = alpha.crop((0, SEAM[0], master.width, SEAM[1]))
    peak = max(seam.getdata())
    if peak > SEAM_MAX_ALPHA:
        sys.exit(f"rows {SEAM[0]}-{SEAM[1] - 1} peak at alpha {peak} (limit "
                 f"{SEAM_MAX_ALPHA}) — artwork now sits where the mark/word "
                 f"split is taken; re-measure before building")
    if not MARK_BOX[3] == WORD_BOX[1] or not SEAM[0] < MARK_BOX[3] < SEAM[1]:
        sys.exit("mark/word split is not inside the shadow-only band")


def build():
    if not os.path.exists(SRC):
        sys.exit(f"missing source: {os.path.relpath(SRC, ROOT)}")

    master = Image.open(SRC).convert("RGBA")
    print(f"Source: {os.path.relpath(SRC, ROOT)}  {master.width}x{master.height}")
    _assert_crops(master)
    print("  crop boxes verified against the artwork's alpha channel")

    dims = {}
    for size in SIZES:
        img = master.copy()
        img.thumbnail((size, size), Image.LANCZOS)
        base = os.path.join(BRAND, f"logo-{size}")
        img.save(base + ".png")
        img.save(base + ".webp", "WEBP", quality=Q_STACKED, method=6)
        dims[size] = img.size
        kb = os.path.getsize(base + ".webp") // 1024
        print(f"  logo-{size}.png/.webp   {img.width}x{img.height}  {kb} KB webp")

    crop_dims = {}
    for name, box, height in CROPS:
        img = master.crop(box)
        img = img.resize((round(img.width * height / img.height), height), Image.LANCZOS)
        base = os.path.join(BRAND, f"{name}-{height}")
        img.save(base + ".png")
        img.save(base + ".webp", "WEBP", quality=Q_HEADER, method=6)
        crop_dims[name] = img.size
        kb = os.path.getsize(base + ".webp") // 1024
        print(f"  {name}-{height}.png/.webp   {img.width}x{img.height}  {kb} KB webp")

    copied = 0
    for name in FAVICONS:
        src = os.path.join(FAVDIR, name)
        if not os.path.exists(src):
            print(f"  ! missing {name} in favicon_io")
            continue
        shutil.copy2(src, os.path.join(IMG, name))
        copied += 1
    print(f"  {copied} favicon file(s) copied verbatim from favicon_io/")

    # Real dimensions, so pages can set width/height without hardcoding a ratio
    # that goes stale if the artwork is re-exported at a different aspect.
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_dims.py")
    with open(out, "w", encoding="utf-8") as f:
        f.write('"""GENERATED by tools/brand-assets.py — do not edit."""\n\n')
        for size in SIZES:
            f.write(f"LOGO_{size} = {dims[size]}\n")
        for name, _box, height in CROPS:
            f.write(f"{name.upper()}_{height} = {crop_dims[name]}\n")
    print("  tools/logo_dims.py written")


if __name__ == "__main__":
    build()
