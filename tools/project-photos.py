#!/usr/bin/env python3
"""
Optimise the owner's real job photos for the web.

    python3 tools/project-photos.py

Full-resolution masters live in assets/img/photos/originals/ and are never
referenced by the site. This writes web-sized JPEG + WebP derivatives to
assets/img/projects/, which is what the pages load. Drop a new photo in
originals/, add it to PROJECTS in tools/content_projects.py, and re-run.

These are the company's OWN work, unlike everything in assets/img/photos/,
which is licensed stock. That distinction is why they live in a separate
folder: real work may be captioned as theirs, stock may never be. See the
"Content and honesty rules" section of README.md.

TWO derivatives per photo, because the site paints them in two shapes:

  {slug}.jpg/.webp        800x1067   3:4 portrait, the home page carousel
  {slug}-wide.jpg/.webp  1400x875   16:10, the figure on a service page

Almost every master is a portrait phone photo, so the 16:10 cut throws away
more than half the frame. Which half is a judgement call that differs per
photo — on a deck shot the structure sits low and the sky is expendable; on an
interior the ceiling detail may be the point. So each PROJECTS entry carries a
`focus` (0 = top of frame, 1 = bottom, 0.5 = centre) and the crops are checked
by eye, not assumed. `focus_x` does the same for the horizontal cut when a
landscape master is squeezed into the portrait card.

HEIC: iPhone masters arrive as .heic, which Pillow cannot read on its own.
pillow-heif is an optional dependency — without it the HEIC photos are skipped
with a clear message and the JPEG/PNG ones still build.
"""

import os
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install Pillow")

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC = True
except ImportError:
    HEIC = False

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content_projects import PROJECTS  # noqa: E402

SRC = os.path.join(ROOT, "assets", "img", "photos", "originals")
OUT = os.path.join(ROOT, "assets", "img", "projects")

CARD = (800, 1067)     # 3:4 portrait — carousel
WIDE = (1400, 875)     # 16:10        — service page figure

# These frames are grass, foliage and wood grain, so they compress badly: even
# at q60 the heaviest card only drops from 220 KB to 176 KB. Chasing quality
# down buys almost nothing and starts to show, so it sits at 72. The weight is
# affordable because every carousel image is lazy — the section is well below
# the fold, so nothing here is fetched until a visitor scrolls to it.
QUALITY_JPG = 78
QUALITY_WEBP = 72

# --- The owner's photograph --------------------------------------------------
# Square, painted at 240px on /about/, so 480 covers 2x.
OWNER_SRC = "jake.jpg"
OWNER_OUT = os.path.join(ROOT, "assets", "img", "team")
OWNER_SIZE = 480

# The owner's photo is published AS SUPPLIED. An alternative crop is kept here
# so switching is one line rather than a re-crop from scratch: set OWNER_CROP to
# CROP_JAKE_ONLY and re-run. Both frames were checked by eye.
#
# If the crop is ever adopted, the `alt` text in build.build_about() has to
# change with it — it describes the frame as supplied.
#
# The reason the option exists at all is recorded in NOTES.local.md, which is
# not in the public repo.
CROP_JAKE_ONLY = (330, 250, 890, 810)
OWNER_CROP = None          # None = as supplied.  CROP_JAKE_ONLY = Jake alone.

EXTS = (".jpg", ".jpeg", ".png", ".heic", ".HEIC")


def find_master(slug):
    for ext in EXTS:
        p = os.path.join(SRC, slug + ext)
        if os.path.exists(p):
            return p
    return None


def trim_letterbox(img, tol=18):
    """Strip solid black bars from a screenshot.

    One master (bathroom-tub) is a phone screenshot rather than a camera file,
    so the photograph sits letterboxed inside a taller frame. Cropping to 3:4
    without removing the bars would bake black margins into the card.
    """
    g = img.convert("L")
    w, h = g.size
    px = g.load()

    def dark_row(y):
        return max(px[x, y] for x in range(0, w, 7)) <= tol

    top, bottom = 0, h - 1
    while top < bottom and dark_row(top):
        top += 1
    while bottom > top and dark_row(bottom):
        bottom -= 1
    return img.crop((0, top, w, bottom + 1)) if (top or bottom < h - 1) else img


def cover(img, size, focus, focus_x):
    """Crop to `size`'s aspect around the focus point, then resize."""
    ratio = size[0] / size[1]
    w, h = img.size
    if w / h > ratio:                       # too wide — cut the sides
        new_w = int(round(h * ratio))
        left = int(round((w - new_w) * focus_x))
        img = img.crop((left, 0, left + new_w, h))
    else:                                   # too tall — cut top/bottom
        new_h = int(round(w / ratio))
        top = int(round((h - new_h) * focus))
        img = img.crop((0, top, w, top + new_h))
    return img.resize(size, Image.LANCZOS)


def optimise(p):
    slug = p["slug"]
    src = find_master(slug)
    if src is None:
        return None, f"no master for {slug} in assets/img/photos/originals/"
    if src.lower().endswith(".heic") and not HEIC:
        return None, f"{slug}: .heic master needs pillow-heif (python3 -m pip install pillow-heif)"

    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if p.get("letterboxed"):
        img = trim_letterbox(img)

    focus = p.get("focus", 0.35)
    focus_x = p.get("focus_x", 0.5)

    # The 16:10 cut is only made for photos that actually head a service page.
    # Generating one for every project produced six files nothing referenced.
    jobs = [("", CARD, focus)]
    if p.get("service"):
        jobs.append(("-wide", WIDE, p.get("focus_wide", focus)))

    written = {}
    for suffix, size, f in jobs:
        out = cover(img, size, f, focus_x)
        jpg = os.path.join(OUT, f"{slug}{suffix}.jpg")
        out.save(jpg, "JPEG", quality=QUALITY_JPG, optimize=True, progressive=True)
        out.save(os.path.join(OUT, f"{slug}{suffix}.webp"),
                 "WEBP", quality=QUALITY_WEBP, method=6)
        written[suffix] = os.path.getsize(
            os.path.join(OUT, f"{slug}{suffix}.webp"))
    return written, None


def build_owner():
    """The owner's portrait for /about/. Square in, square out."""
    src = os.path.join(SRC, OWNER_SRC)
    if not os.path.exists(src):
        print(f"  ! no owner photo at photos/originals/{OWNER_SRC} — /about/ will "
              f"render without one")
        return
    os.makedirs(OWNER_OUT, exist_ok=True)
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if OWNER_CROP:
        img = img.crop(OWNER_CROP)
    img = cover(img, (OWNER_SIZE, OWNER_SIZE), 0.5, 0.5)
    base = os.path.join(OWNER_OUT, "jake-480")
    img.save(base + ".jpg", "JPEG", quality=82, optimize=True, progressive=True)
    img.save(base + ".webp", "WEBP", quality=80, method=6)
    kb = os.path.getsize(base + ".webp") // 1024
    which = "Jake alone" if OWNER_CROP else "as supplied"
    print(f"\nOwner photo: team/jake-480.jpg/.webp  {OWNER_SIZE}x{OWNER_SIZE}  "
          f"{kb} KB webp  ({which})")


def main():
    os.makedirs(OUT, exist_ok=True)
    if not HEIC:
        print("  ! pillow-heif not installed — .heic masters will be skipped\n")
    print("Optimising project photos (card 800x1067; wide 1400x875 where used):")
    failed = card_total = 0
    for p in PROJECTS:
        written, err = optimise(p)
        if err:
            print(f"  ✗ {err}")
            failed += 1
            continue
        card_total += written[""]
        wide = f"   wide {written['-wide'] // 1024:4} KB" if "-wide" in written else ""
        print(f"  {p['slug']:16} card {written[''] // 1024:4} KB webp{wide}")
    print(f"\n{len(PROJECTS) - failed} photo(s) written to assets/img/projects/.")
    print(f"Carousel weight if every slide is scrolled: {card_total // 1024} KB "
          f"(only the first is fetched on load — the rest are lazy).")
    build_owner()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
