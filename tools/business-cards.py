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

Shared machinery — colours, fonts, the logo crops, the safe-zone check and the
type-size floor — lives in printkit.py so the cards and the job stickers cannot
drift apart.
"""

import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import brand as S          # noqa: E402
import printkit as K       # noqa: E402

from printkit import (     # noqa: E402  — the design code reads better unprefixed
    INK, INK2, CHROME1, CHROME2, CHROME3, CHROME4, CHROME5,
    RED, RED_LIFT, PAPER, DISP, BODY, BODYB, MARK_BOX, WORD_BOX,
    DPI, MIN_PT, pt, font, tw, track_w, T, TT, logo_part, logo_full,
    chrome_rule,
)

OUT = os.path.join(ROOT, "assets", "print", "cards")

BLEED = K.inches(0.125)          # 38
W, H = K.inches(3.75), K.inches(2.25)        # 1125 x 675, trim + bleed
SAFE = (BLEED * 2, BLEED * 2, W - BLEED * 2, H - BLEED * 2)

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


def check(label):
    return K.check(label, SAFE)


def grid(img, y0=0, y1=None, step=46, colour=(24, 26, 30)):
    K.grid(img, W, H, y0, y1, step, colour)


def hazard(d, y0, y1, pitch=34):
    K.hazard(d, W, y0, y1, pitch)


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
    K.require_logo()

    print(f'Business cards — 3.5x2" trim + 0.125" bleed @ {DPI} DPI ({W}x{H} px)')
    print(f'  email on the card: {EMAIL}   (from brand.EMAIL)\n')

    cards = [("A-dark-front", a_front()), ("A-dark-back", a_back()),
             ("B-chrome-front", b_front()), ("B-chrome-back", b_back())]

    for n, im in cards:
        kb = K.save(im, OUT, n) // 1024
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

    ok = K.type_report()
    print(f"  Written to {os.path.relpath(OUT, ROOT)}/")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
