#!/usr/bin/env python3
"""
Print-ready business cards for Elite Carpentry & Renovations.

    python3 tools/business-cards.py      (needs Pillow)

North American standard: 3.5 x 2 in trim, 0.125 in bleed, 300 DPI -> 1125x675.
Writes PNG (what most online printers want) and PDF (what a commercial printer
usually prefers) into assets/print/cards/.

EVERY contact detail comes from brand.py. The first cut of this hard-coded the
address and went stale the moment the email changed — which is the same failure
the whole site is built to avoid. Change brand.py, re-run this, done.

Two checks run on every build, because neither is safe to eyeball:

  SAFE ZONE  every piece of text records its bounds and must land inside the
             safe box. Outside it is a card guillotined through a phone number.

  TYPE SIZE  nothing may print below MIN_PT. The first cut had the phone number
             and email at 5-6.5pt, which is unreadable on paper.
"""

import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install Pillow")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import brand as S  # noqa: E402

OUT = os.path.join(ROOT, "assets", "print", "cards")

DPI = 300
BLEED = 38                       # 0.125 in
W, H = 1125, 675                 # 3.75 x 2.25 in including bleed
SAFE = (BLEED * 2, BLEED * 2, W - BLEED * 2, H - BLEED * 2)

INK, INK2 = (11, 11, 12), (19, 20, 23)
CHROME1, CHROME2 = (243, 245, 248), (210, 216, 222)
CHROME3, CHROME4, CHROME5 = (154, 162, 171), (107, 115, 124), (69, 75, 83)
RED, RED_LIFT, PAPER = (224, 27, 36), (255, 74, 82), (238, 240, 243)

DISP = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
BODY = "/System/Library/Fonts/Supplemental/Arial.ttf"
BODYB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

LOGO_SRC = os.path.join(ROOT, "assets/img/brand/elitelogo/PNG/Artboard 1 copy.png")
MARK_BOX = (685, 392, 3889, 2772)     # house + EC
WORD_BOX = (678, 2772, 3908, 3933)    # ELITE + rule + sub-line

# --- Copy, all of it derived -------------------------------------------------
NAME = S.OWNER_NAME.upper()
ROLE = S.OWNER_ROLE.upper()
PHONE = S.PHONE_DISPLAY
EMAIL = S.EMAIL
WEB = S.BASE.replace("https://", "")
AREA = "Cornwall  ·  Akwesasne  ·  SD&G"
TRUST = "Licensed & fully insured  ·  WSIB covered"
SERVICES = [s[1].upper() for s in S.SERVICES]
TAGLINE = "BUILT RIGHT, THE FIRST TIME."

MIN_PT = 7.0
PT_USED = []
BOUNDS = []


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
    w = tw(d, text, f)
    if right is not None:
        x = right - w
    if centre is not None:
        x = centre - w / 2
    d.text((x, y), text, font=f, fill=fill)
    BOUNDS.append((text[:26], d.textbbox((x, y), text, font=f)))


def TT(d, xy, text, f, fill, space=0, right=None, centre=None):
    """Letter-spaced: condensed faces need it at small sizes."""
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
    h = d.textbbox((0, 0), text, font=f)[3]
    BOUNDS.append((text[:26], (x0, y, x0 + w, y + h)))


def check(label):
    bad = [(t, b) for t, b in BOUNDS if b[0] < SAFE[0] - 1 or b[2] > SAFE[2] + 1
           or b[1] < SAFE[1] - 1 or b[3] > SAFE[3] + 1]
    for t, b in bad:
        print(f"    !! {label}: '{t}' at {b} breaks safe zone {SAFE}")
    BOUNDS.clear()
    return not bad


# --- Drawing helpers ---------------------------------------------------------

def logo_part(box, height):
    im = Image.open(LOGO_SRC).convert("RGBA").crop(box)
    return im.resize((round(im.width * height / im.height), height), Image.LANCZOS)


def logo_full(height):
    im = Image.open(LOGO_SRC).convert("RGBA")
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * height / im.height), height), Image.LANCZOS)


def grid(img, y0=0, y1=None, step=46, colour=(24, 26, 30)):
    y1 = H if y1 is None else y1
    d = ImageDraw.Draw(img)
    for x in range(0, W, step):
        d.line([(x, y0), (x, y1)], fill=colour, width=1)
    for y in range(y0, y1, step):
        d.line([(0, y), (W, y)], fill=colour, width=1)


def hazard(d, y0, y1, pitch=34):
    """The site's diagonal stripe, bled off both edges."""
    d.rectangle([0, y0, W, y1], fill=INK2)
    h = y1 - y0
    for x in range(-h * 2, W + h * 2, pitch):
        d.polygon([(x, y1), (x + pitch // 2, y1),
                   (x + pitch // 2 + h, y0), (x + h, y0)], fill=RED)


def chrome_rule(d, x0, y, x1, thick=3):
    """Chrome gradient rule — dark, bright at centre, dark again."""
    span = max(1, x1 - x0 - 1)
    for i in range(x1 - x0):
        t = i / span
        k = t / 0.5 if t < 0.5 else (t - 0.5) / 0.5
        a, b = (CHROME5, CHROME1) if t < 0.5 else (CHROME1, CHROME5)
        c = tuple(round(a[j] + (b[j] - a[j]) * k) for j in range(3))
        d.rectangle([x0 + i, y, x0 + i, y + thick], fill=c)


# --- Option A: site dark -----------------------------------------------------

def a_front():
    img = Image.new("RGB", (W, H), INK); grid(img)
    d = ImageDraw.Draw(img)
    logo = logo_full(392)
    img.paste(logo, ((W - logo.width) // 2, (H - 392) // 2 - 16), logo)
    hazard(d, H - 26, H)
    check("A-front")
    return img


def a_back():
    img = Image.new("RGB", (W, H), INK); grid(img)
    d = ImageDraw.Draw(img)
    L, R = SAFE[0], SAFE[2] - 12

    mark = logo_part(MARK_BOX, 132)
    img.paste(mark, (L, 78), mark)

    x = L + mark.width + 30
    T(d, (x, 84), NAME, font(DISP, pt(15)), CHROME1)
    TT(d, (x + 3, 152), ROLE, font(BODY, pt(7.5)), RED, space=5)

    chrome_rule(d, L, 250, SAFE[2], 3)

    T(d, (L, 284), PHONE, font(BODYB, pt(10)), CHROME1)
    T(d, (L + 4, 340), EMAIL, font(BODY, pt(8)), CHROME2)
    T(d, (L, 388), WEB, font(BODY, pt(8)), RED_LIFT)

    f_svc = font(DISP, pt(7.5))
    TT(d, (0, 288), " · ".join(SERVICES[:3]), f_svc, CHROME2, space=1, right=R)
    TT(d, (0, 328), " · ".join(SERVICES[3:]), f_svc, CHROME2, space=1, right=R)
    TT(d, (0, 386), AREA.upper(), font(DISP, pt(7)), CHROME4, space=1, right=R)

    d.rectangle([0, 486, W, H - 26], fill=INK2)
    T(d, (0, 512), TRUST, font(BODY, pt(7.5)), CHROME3, centre=W / 2)
    hazard(d, H - 26, H)
    check("A-back")
    return img


# --- Option B: chrome band ---------------------------------------------------
# The logo sits in a dark band because its sub-line is white with a dark
# keyline: drawn for dark grounds, it goes muddy straight onto pale card.

def b_front():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    for y in range(H):
        c = round(255 + (224 - 255) * (y / H))
        d.rectangle([0, y, W, y], fill=(c, c, c))

    band_bot = 462
    d.rectangle([0, 0, W, band_bot], fill=INK)
    grid(img, 0, band_bot)
    d.rectangle([0, band_bot + 1, W, band_bot + 5], fill=RED)

    logo = logo_full(322)
    img.paste(logo, ((W - logo.width) // 2, (band_bot - 322) // 2 + 14), logo)

    TT(d, (0, 524), TAGLINE, font(DISP, pt(8.5)), CHROME5, space=3, centre=W / 2)
    check("B-front")
    return img


def b_back():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 9], fill=RED)
    L, R = SAFE[0], SAFE[2] - 12

    word = logo_part(WORD_BOX, 88)
    img.paste(word, (L, 80), word)

    T(d, (0, 82), NAME, font(DISP, pt(13)), CHROME1, right=R)
    TT(d, (0, 140), ROLE, font(BODY, pt(7.5)), RED, space=5, right=R)

    chrome_rule(d, L, 232, SAFE[2], 2)

    f_lab = font(DISP, pt(7.5))
    rows = [("PHONE", PHONE, font(BODYB, pt(10)), CHROME1),
            ("EMAIL", EMAIL, font(BODY, pt(8)), CHROME2),
            ("ONLINE", WEB, font(BODY, pt(8)), RED_LIFT)]
    for i, (lab, val, f_v, col) in enumerate(rows):
        y = 266 + i * 56
        TT(d, (L, y + 8), lab, f_lab, CHROME4, space=2)
        T(d, (L + 140, y), val, f_v, col)

    TT(d, (0, 452), " · ".join(SERVICES), font(DISP, pt(7.5)), CHROME2, space=1, centre=W / 2)
    TT(d, (0, 500), AREA.upper(), font(DISP, pt(7)), CHROME4, space=1, centre=W / 2)
    T(d, (0, 548), TRUST, font(BODY, pt(7.5)), CHROME3, centre=W / 2)
    hazard(d, H - 26, H)
    check("B-back")
    return img


# --- Output ------------------------------------------------------------------

def proof(pairs, name, title):
    """Contact sheet with trim and safe guides — judged the way a printer cuts."""
    sc = 0.60
    cw, ch = round(W * sc), round(H * sc)
    pad, gap, head = 34, 26, 56
    cvs = Image.new("RGB", (pad * 2 + 2 * cw + gap,
                            head + pad + len(pairs) * (ch + 48)), (245, 246, 248))
    d = ImageDraw.Draw(cvs)
    d.text((pad, 18), title, font=font(BODYB, 26), fill=(28, 32, 38))
    f_c = font(BODY, 17)
    for r, (label, imgs) in enumerate(pairs):
        for c, im in enumerate(imgs):
            x, y = pad + c * (cw + gap), head + r * (ch + 48)
            cvs.paste(im.resize((cw, ch), Image.LANCZOS), (x, y))
            g = ImageDraw.Draw(cvs)
            g.rectangle([x + BLEED * sc, y + BLEED * sc,
                         x + cw - BLEED * sc, y + ch - BLEED * sc],
                        outline=(0, 190, 255), width=1)
            g.rectangle([x + BLEED * 2 * sc, y + BLEED * 2 * sc,
                         x + cw - BLEED * 2 * sc, y + ch - BLEED * 2 * sc],
                        outline=(255, 0, 160), width=1)
            d.text((x, y + ch + 9), f"{label} — {'FRONT' if c == 0 else 'BACK'}",
                   font=f_c, fill=(70, 78, 88))
    d.text((pad, cvs.height - 26),
           'cyan = trim   ·   magenta = safe zone   ·   art bleeds 0.125" past trim',
           font=f_c, fill=(120, 128, 138))
    cvs.save(os.path.join(OUT, name + ".png"))


def actual_size(items, name):
    """Trimmed, at the size it sits in a hand — the real legibility test."""
    tw_, th_ = 385, 220
    pad, gap = 26, 20
    cvs = Image.new("RGB", (pad * 2 + 2 * tw_ + gap, pad * 2 + 2 * th_ + gap + 40),
                    (250, 250, 251))
    d = ImageDraw.Draw(cvs)
    d.text((pad, 8), "Actual size (3.5 x 2 in), trimmed", font=font(BODY, 14),
           fill=(60, 66, 74))
    for i, (lab, im) in enumerate(items):
        im = im.crop((BLEED, BLEED, W - BLEED, H - BLEED)).resize((tw_, th_), Image.LANCZOS)
        x, y = pad + (i % 2) * (tw_ + gap), 34 + pad + (i // 2) * (th_ + gap)
        cvs.paste(im, (x, y))
        d.rectangle([x, y, x + tw_, y + th_], outline=(200, 205, 212))
    cvs.save(os.path.join(OUT, name + ".png"))


def main():
    os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(LOGO_SRC):
        sys.exit(f"missing logo master: {os.path.relpath(LOGO_SRC, ROOT)}\n"
                 "It is gitignored — restore it from the designer package backup.")

    print(f'Business cards — 3.5x2" trim + 0.125" bleed @ {DPI} DPI ({W}x{H} px)')
    print(f'  email on the card: {EMAIL}   (from brand.EMAIL)\n')

    cards = [("A-dark-front", a_front()), ("A-dark-back", a_back()),
             ("B-chrome-front", b_front()), ("B-chrome-back", b_back())]

    for n, im in cards:
        im.save(os.path.join(OUT, n + ".png"), dpi=(DPI, DPI))
        im.save(os.path.join(OUT, n + ".pdf"), "PDF", resolution=DPI)
        kb = os.path.getsize(os.path.join(OUT, n + ".png")) // 1024
        print(f"  {n:16} {W}x{H}  {kb:4} KB png  +  pdf")

    d = {n: im for n, im in cards}
    proof([("Option A · Site dark", (d["A-dark-front"], d["A-dark-back"])),
           ("Option B · Chrome band", (d["B-chrome-front"], d["B-chrome-back"]))],
          "PROOF-both-options",
          "Elite Carpentry & Renovations — business cards")
    actual_size([("A front", d["A-dark-front"]), ("A back", d["A-dark-back"]),
                 ("B front", d["B-chrome-front"]), ("B back", d["B-chrome-back"])],
                "PROOF-actual-size")
    print("  PROOF-both-options.png  +  PROOF-actual-size.png")

    lo, hi = min(PT_USED), max(PT_USED)
    ok = lo >= MIN_PT
    print(f"\n  Type: {len(set(PT_USED))} sizes, {lo:.1f}pt to {hi:.1f}pt — "
          + (f"OK, nothing under the {MIN_PT:.0f}pt print floor" if ok
             else f"!! {lo:.1f}pt is BELOW the {MIN_PT:.0f}pt floor"))
    print(f"  Written to {os.path.relpath(OUT, ROOT)}/")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
