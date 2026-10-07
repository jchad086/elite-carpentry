#!/usr/bin/env python3
"""
Shared primitives for print artwork (business cards, job stickers, anything
else that goes to a printer).

Every contact detail comes from brand.py — print pieces must never hold their
own copy of a phone number or an address. The first business cards did, and
went stale the moment the email changed.

Two guards live here because neither is safe to judge by eye:

  check()        every text element records its bounds and must land inside the
                 artefact's safe box. Outside it is artwork trimmed through a
                 phone number.
  type_report()  nothing may print below MIN_PT. An early card cut had the
                 phone number at 5pt, which is unreadable on paper.
"""

import math
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install Pillow")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

DPI = 300
MIN_PT = 7.0

INK, INK2 = (11, 11, 12), (19, 20, 23)
CHROME1, CHROME2 = (243, 245, 248), (210, 216, 222)
CHROME3, CHROME4, CHROME5 = (154, 162, 171), (107, 115, 124), (69, 75, 83)
RED, RED_D, RED_LIFT = (224, 27, 36), (168, 15, 20), (255, 74, 82)
PAPER, WHITE = (238, 240, 243), (255, 255, 255)

DISP = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
BODY = "/System/Library/Fonts/Supplemental/Arial.ttf"
BODYB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

LOGO_SRC = os.path.join(ROOT, "assets/img/brand/elitelogo/PNG/Artboard 1 copy.png")
MARK_BOX = (685, 392, 3889, 2772)     # house + EC
WORD_BOX = (678, 2772, 3908, 3933)    # ELITE + rule + sub-line

PT_USED = []
BOUNDS = []


def inches(n):
    return round(n * DPI)


def pt(points):
    PT_USED.append(points)
    return round(points / 72 * DPI)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def tw(d, text, f):
    return d.textbbox((0, 0), text, font=f)[2]


def track_w(d, text, f, space=0):
    return sum(tw(d, c, f) + space for c in text) - space


def T(d, xy, text, f, fill, right=None, centre=None):
    x, y = xy
    if right is not None:
        x = right - tw(d, text, f)
    if centre is not None:
        x = centre - tw(d, text, f) / 2
    d.text((x, y), text, font=f, fill=fill)
    BOUNDS.append((text[:26], d.textbbox((x, y), text, font=f)))


def TT(d, xy, text, f, fill, space=0, right=None, centre=None):
    """Letter-spaced text; condensed faces need it at small sizes."""
    x, y = xy
    w = track_w(d, text, f, space)
    if right is not None:
        x = right - w
    if centre is not None:
        x = centre - w / 2
    x0 = x
    for c in text:
        d.text((x, y), c, font=f, fill=fill)
        x += tw(d, c, f) + space
    BOUNDS.append((text[:26], (x0, y, x0 + w, y + d.textbbox((0, 0), text, font=f)[3])))


def check(label, safe):
    bad = [(t, b) for t, b in BOUNDS
           if b[0] < safe[0] - 1 or b[2] > safe[2] + 1
           or b[1] < safe[1] - 1 or b[3] > safe[3] + 1]
    for t, b in bad:
        print(f"    !! {label}: '{t}' at {b} breaks safe zone {safe}")
    BOUNDS.clear()
    return not bad


def type_report():
    lo, hi = min(PT_USED), max(PT_USED)
    ok = lo >= MIN_PT
    print(f"\n  Type: {len(set(PT_USED))} sizes, {lo:.1f}pt to {hi:.1f}pt — "
          + (f"OK, nothing under the {MIN_PT:.0f}pt print floor" if ok
             else f"!! {lo:.1f}pt is BELOW the {MIN_PT:.0f}pt floor"))
    return ok


# --- Logo --------------------------------------------------------------------

def require_logo():
    if not os.path.exists(LOGO_SRC):
        sys.exit(f"missing logo master: {os.path.relpath(LOGO_SRC, ROOT)}\n"
                 "It is gitignored — restore it from the designer package backup.")


def logo_part(box, height):
    im = Image.open(LOGO_SRC).convert("RGBA").crop(box)
    return im.resize((round(im.width * height / im.height), height), Image.LANCZOS)


def logo_full(height):
    im = Image.open(LOGO_SRC).convert("RGBA")
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * height / im.height), height), Image.LANCZOS)


# --- Brand furniture ---------------------------------------------------------

def grid(img, W, H, y0=0, y1=None, step=46, colour=(24, 26, 30)):
    y1 = H if y1 is None else y1
    d = ImageDraw.Draw(img)
    for x in range(0, W, step):
        d.line([(x, y0), (x, y1)], fill=colour, width=1)
    for y in range(y0, y1, step):
        d.line([(0, y), (W, y)], fill=colour, width=1)


def hazard(d, W, y0, y1, pitch=34):
    """The site's diagonal stripe, bled off both edges."""
    d.rectangle([0, y0, W, y1], fill=INK2)
    h = y1 - y0
    for x in range(-h * 2, W + h * 2, pitch):
        d.polygon([(x, y1), (x + pitch // 2, y1),
                   (x + pitch // 2 + h, y0), (x + h, y0)], fill=RED)


def chrome_rule(d, x0, y, x1, thick=3):
    """Chrome gradient rule — dark, bright at the centre, dark again."""
    span = max(1, x1 - x0 - 1)
    for i in range(x1 - x0):
        t = i / span
        k = t / 0.5 if t < 0.5 else (t - 0.5) / 0.5
        a, b = (CHROME5, CHROME1) if t < 0.5 else (CHROME1, CHROME5)
        d.rectangle([x0 + i, y, x0 + i, y + thick],
                    fill=tuple(round(a[j] + (b[j] - a[j]) * k) for j in range(3)))


def arc_text(img, text, cx, cy, radius, f, fill, mid_deg=90, space=0, inward=False):
    """Set text around a circle — the seal look a straight line cannot give.

    mid_deg is measured counter-clockwise from 3 o'clock, so 90 is the top of
    the ring and 270 the bottom. Glyphs on the bottom arc are flipped so the
    text still reads left to right rather than upside down.

    Each glyph is drawn with anchor="mm" so its OPTICAL centre lands on the
    radius. Drawing from the top-left instead leaves the glyph sitting high in
    its tile, which after rotation throws it outward off the circle — that is
    how the first cut ended up with the phone number lying across the ring.
    """
    d = ImageDraw.Draw(img)
    widths = [tw(d, c, f) + space for c in text]
    total = sum(widths) - space
    ang = math.degrees(total / radius)
    a = mid_deg + ang / 2 if not inward else mid_deg - ang / 2
    tile = f.size * 2 + 32

    for c, w in zip(text, widths):
        step = math.degrees(w / radius)
        mid = a - step / 2 if not inward else a + step / 2
        glyph = Image.new("RGBA", (tile, tile), (0, 0, 0, 0))
        ImageDraw.Draw(glyph).text((tile / 2, tile / 2), c, font=f, fill=fill,
                                   anchor="mm")
        rot = glyph.rotate(mid - 90 if not inward else mid + 90,
                           resample=Image.BICUBIC)
        x = cx + radius * math.cos(math.radians(mid))
        y = cy - radius * math.sin(math.radians(mid))
        img.alpha_composite(rot, (round(x - tile / 2), round(y - tile / 2)))
        a = a - step if not inward else a + step


def save(img, out_dir, name, also_pdf=True):
    os.makedirs(out_dir, exist_ok=True)
    png = os.path.join(out_dir, name + ".png")
    img.save(png, dpi=(DPI, DPI))
    if also_pdf:
        img.convert("RGB").save(os.path.join(out_dir, name + ".pdf"),
                                "PDF", resolution=DPI)
    return os.path.getsize(png)
