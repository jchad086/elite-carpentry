#!/usr/bin/env python3
"""
Job-completion sticker — 2 x 2 in square, applied to finished work.

    python3 tools/job-sticker.py      (needs Pillow)

This is NOT a business card shrunk down. It gets stuck on a deck joist, inside
a cabinet door, on a panel cover — read at arm's length, in bad light, and
quite possibly years later by somebody who is not the customer: a home
inspector, a buyer, the next trade in. That drives the design:

  * The PHONE NUMBER is the payload. A stranger finding this in 2032 has to be
    able to call. It is the largest thing after the mark.
  * It must read as a SEAL, not an advert. The visual language of certification
    is what says "this work was signed off", and that is the whole point.
  * No fine print. At 2 inches there is no room, and nothing on a sticker is
    read closely enough to justify it.

Corners: square stickers are die-cut with a radius (1/8 in is typical) and the
cut wanders more than a guillotine. So the safe zone here is a generous 1/4 in
inside trim, and the seal designs keep their content circular, which sidesteps
corner loss entirely.
"""

import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import brand as S          # noqa: E402
import printkit as K       # noqa: E402

OUT = os.path.join(ROOT, "assets", "print", "stickers")

TRIM = K.inches(2)                  # 600
BLEED = K.inches(0.125)             # 38
W = H = TRIM + BLEED * 2            # 676
CX = CY = W // 2
SAFE_IN = K.inches(0.25)            # die cut wanders; be generous
SAFE = (BLEED + SAFE_IN, BLEED + SAFE_IN, W - BLEED - SAFE_IN, H - BLEED - SAFE_IN)
R_TRIM = TRIM // 2                  # radius of the trimmed square's inscribed circle

NAME_RING = "ELITE CARPENTRY & RENOVATIONS"
PHONE = S.PHONE_DISPLAY
WEB = S.BASE.replace("https://", "").replace("www.", "")
TAGLINE = "BUILT RIGHT, THE FIRST TIME"
AREA = "CORNWALL · AKWESASNE"


def ring(d, r, colour, thick):
    d.ellipse([CX - r, CY - r, CX + r, CY + r], outline=colour, width=thick)


def chrome_ring(img, r, thick=10):
    """An annulus filled with the chrome gradient, lit from the top left."""
    ring_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring_img)
    for i in range(thick):
        t = i / max(1, thick - 1)
        k = t / 0.5 if t < 0.5 else (t - 0.5) / 0.5
        a, b = (K.CHROME5, K.CHROME1) if t < 0.5 else (K.CHROME1, K.CHROME4)
        c = tuple(round(a[j] + (b[j] - a[j]) * k) for j in range(3))
        rr = r - i
        rd.ellipse([CX - rr, CY - rr, CX + rr, CY + rr], outline=c + (255,), width=1)
    img.alpha_composite(ring_img)


def base(dark=True):
    img = Image.new("RGBA", (W, H), (K.INK if dark else K.PAPER) + (255,))
    if dark:
        K.grid(img, W, H, step=46, colour=(23, 25, 29))
    return img


# --- A: the seal -------------------------------------------------------------
# A certification mark. Company name curved over the top, phone curved under,
# the house mark in the middle. Nothing square-aligned, so the die cut cannot
# clip anything that matters.

def seal(dark=True):
    img = base(dark)
    d = ImageDraw.Draw(img)
    ink = K.CHROME1 if dark else K.INK
    sub = K.CHROME3 if dark else K.CHROME5
    red = K.RED_LIFT if dark else K.RED

    chrome_ring(img, R_TRIM - 34, thick=9)
    ring(d, R_TRIM - 54, K.RED, 4)

    # The ring carries identity. The phone does NOT go on it: curving the one
    # element a stranger has to read, and running it across a rule, costs more
    # legibility than the badge look is worth.
    K.arc_text(img, NAME_RING, CX, CY, R_TRIM - 82, K.font(K.DISP, K.pt(10.5)),
               ink + (255,), mid_deg=90, space=2)
    arc_sub = K.CHROME4 if dark else K.CHROME5
    K.arc_text(img, AREA, CX, CY, R_TRIM - 80, K.font(K.DISP, K.pt(8)),
               arc_sub + (255,), mid_deg=270, space=3, inward=True)

    mark = K.logo_part(K.MARK_BOX, 146)
    img.alpha_composite(mark, (CX - mark.width // 2, CY - 160))

    K.chrome_rule(d, CX - 96, CY + 4, CX + 96, 3)
    K.T(d, (0, CY + 26), PHONE, K.font(K.BODYB, K.pt(12.5)), ink, centre=CX)
    K.TT(d, (0, CY + 86), TAGLINE, K.font(K.DISP, K.pt(8)), sub, space=2, centre=CX)

    K.check("seal-dark" if dark else "seal-light", SAFE)
    return img


# --- B: the completion plate -------------------------------------------------
# An inspection tag, not a badge. Hazard stripes top and bottom tie it to the
# site, and the date line is the point: a dated plate is evidence of when the
# work was signed off, which is what a buyer's inspector actually wants.

def plate():
    img = base(dark=True)
    d = ImageDraw.Draw(img)
    L, R = SAFE[0], SAFE[2]

    K.hazard(d, W, BLEED, BLEED + 26)
    K.hazard(d, W, H - BLEED - 26, H - BLEED)

    K.TT(d, (0, 112), "WORK COMPLETED", K.font(K.DISP, K.pt(11.5)), K.RED_LIFT,
         space=4, centre=CX)

    mark = K.logo_part(K.MARK_BOX, 140)
    img.alpha_composite(mark, (CX - mark.width // 2, 158))

    word = K.logo_part(K.WORD_BOX, 52)
    img.alpha_composite(word, (CX - word.width // 2, 314))

    K.chrome_rule(d, L, 396, R, 2)

    # The date line is the reason this option exists — a dated plate is what a
    # buyer's inspector actually wants years later. Label is CHROME2, not a
    # murky grey, because somebody has to write on it in a dim crawlspace.
    K.TT(d, (L, 420), "DATE", K.font(K.DISP, K.pt(8.5)), K.CHROME2, space=2)
    d.line([(L + 86, 452), (R, 452)], fill=K.CHROME4, width=2)

    K.T(d, (0, 486), PHONE, K.font(K.BODYB, K.pt(12.5)), K.CHROME1, centre=CX)

    K.check("plate", SAFE)
    return img


# --- C: the mark -------------------------------------------------------------
# The quietest option. The whole lockup, a rule, the number. Works anywhere,
# including places a badge would look fussy — inside a cabinet, on a panel.

def mark_only():
    img = base(dark=True)
    d = ImageDraw.Draw(img)
    L, R = SAFE[0], SAFE[2]

    logo = K.logo_full(286)
    img.alpha_composite(logo, (CX - logo.width // 2, 104))

    K.chrome_rule(d, L + 40, 432, R - 40, 3)
    K.T(d, (0, 456), PHONE, K.font(K.BODYB, K.pt(12.5)), K.CHROME1, centre=CX)
    K.TT(d, (0, 514), WEB.upper(), K.font(K.DISP, K.pt(8)), K.CHROME3, space=2, centre=CX)

    K.hazard(d, W, H - BLEED - 24, H - BLEED)
    K.check("mark", SAFE)
    return img


# --- Output ------------------------------------------------------------------

def rounded_preview(img, radius=38):
    """Show it as it will be die-cut: trimmed square with rounded corners."""
    trim = img.crop((BLEED, BLEED, W - BLEED, H - BLEED)).convert("RGBA")
    mask = Image.new("L", trim.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, trim.width - 1, trim.height - 1],
                                           radius=radius, fill=255)
    out = Image.new("RGBA", trim.size, (0, 0, 0, 0))
    out.paste(trim, (0, 0), mask)
    return out


def proof(items, name):
    sc = 0.46
    s = round(TRIM * sc)
    pad, gap, head = 30, 24, 54
    cols = len(items)
    cvs = Image.new("RGB", (pad * 2 + cols * s + (cols - 1) * gap, head + pad + s + 86),
                    (244, 245, 247))
    d = ImageDraw.Draw(cvs)
    d.text((pad, 16), "Elite Carpentry — job-completion sticker, 2 x 2 in",
           font=K.font(K.BODYB, 23), fill=(28, 32, 38))
    f_c = K.font(K.BODY, 15)
    for i, (lab, im) in enumerate(items):
        x, y = pad + i * (s + gap), head
        chk = Image.new("RGB", (s, s), (255, 255, 255))
        cd = ImageDraw.Draw(chk)
        for yy in range(0, s, 16):
            for xx in range(0, s, 16):
                if (xx // 16 + yy // 16) % 2:
                    cd.rectangle([xx, yy, xx + 15, yy + 15], fill=(232, 234, 238))
        r = rounded_preview(im).resize((s, s), Image.LANCZOS)
        chk.paste(r, (0, 0), r)
        cvs.paste(chk, (x, y))
        d.rectangle([x, y, x + s, y + s], outline=(205, 210, 216))
        for j, line in enumerate(lab.split("|")):
            d.text((x, y + s + 10 + j * 19), line.strip(), font=f_c, fill=(68, 76, 86))
    d.text((pad, cvs.height - 24),
           "shown die-cut with a 1/8 in corner radius, at roughly half actual size",
           font=f_c, fill=(122, 130, 140))
    cvs.save(os.path.join(OUT, name + ".png"))


def actual_size(items, name):
    """2 inches is about 200 px on a typical screen — the real legibility test."""
    s, pad, gap = 200, 24, 18
    cvs = Image.new("RGB", (pad * 2 + len(items) * s + (len(items) - 1) * gap,
                            pad * 2 + s + 42), (250, 250, 251))
    d = ImageDraw.Draw(cvs)
    d.text((pad, 8), "Actual size (2 x 2 in)", font=K.font(K.BODY, 14), fill=(60, 66, 74))
    for i, (lab, im) in enumerate(items):
        r = rounded_preview(im).resize((s, s), Image.LANCZOS)
        x, y = pad + i * (s + gap), 30 + pad
        bg = Image.new("RGB", (s, s), (255, 255, 255))
        bg.paste(r, (0, 0), r)
        cvs.paste(bg, (x, y))
        d.rectangle([x, y, x + s, y + s], outline=(206, 211, 218))
    cvs.save(os.path.join(OUT, name + ".png"))


def main():
    K.require_logo()
    os.makedirs(OUT, exist_ok=True)
    print(f'Job sticker — 2x2" trim + 0.125" bleed @ {K.DPI} DPI ({W}x{H} px)')
    print(f'  phone on the sticker: {PHONE}   (from brand.PHONE_DISPLAY)\n')

    items = [("A-seal-dark", seal(True)), ("A-seal-light", seal(False)),
             ("B-completion-plate", plate()), ("C-mark", mark_only())]

    for n, im in items:
        kb = K.save(im.convert("RGB"), OUT, n) // 1024
        print(f"  {n:20} {W}x{H}  {kb:4} KB png + pdf")

    proof([("Option A · Seal (dark) | the certification read", items[0][1]),
           ("A · Seal (light) | cheaper print, more visible", items[1][1]),
           ("Option B · Completion plate | dated, inspection-tag feel", items[2][1]),
           ("Option C · Mark | quietest, goes anywhere", items[3][1])],
          "PROOF-sticker-options")
    actual_size(items, "PROOF-sticker-actual-size")
    print("  PROOF-sticker-options.png + PROOF-sticker-actual-size.png")

    ok = K.type_report()
    print(f"  Written to {os.path.relpath(OUT, ROOT)}/")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
