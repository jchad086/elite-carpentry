#!/usr/bin/env python3
"""
Download the site's photography from Unsplash and write a credits file.

    python3 tools/fetch-photos.py

Unsplash photos are free for commercial use without permission and without
attribution; attribution is requested but not required, so CREDITS.md records
photographer and source URL for every file regardless.

IMPORTANT — these are stock photographs, NOT this company's work. They are used
as section imagery only, with descriptive alt text ("a cedar deck with glass
railing"), never attributive ("a deck we built in Cornwall"), and they are never
captioned. Captioning stock as the company's own work would defeat the entire
purpose of a trust-led site — do not do it.

STOCK IS A PLACEHOLDER, AND IT IS RETREATING. Decks, bathrooms and kitchens now
run on the owner's own photographs; those three entries were deleted from this
file and the files removed. Only fencing, siding and windows are left. When a
real photo arrives for one of them, add it to tools/content_projects.py with a
`service` key, then delete the entry here and the file it fetched.

Every entry's `alt` was written after looking at the downloaded file, not from
the search-result description. If you add an entry, look at the image first.
"""

import os
import subprocess
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  python3 -m pip install Pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "photos")

# Rendered at 16:10 in a half-width column, so anything past ~1400px wide is
# bytes the visitor pays for and never sees. Originals arrive at 500-950 KB.
TARGET_W = 1400
TARGET_RATIO = 16 / 10

# (filename, unsplash id, photographer, alt text, where it is used)
PHOTOS = [
    ("fence.jpg", "EE2R5Mh9Dro", "Unsplash contributor",
     "A wooden privacy fence with a lattice topper and a diagonally braced gate",
     "services/fencing"),
    ("siding.jpg", "CO052Aw0Z54", "Unsplash contributor",
     "A two-storey house clad in grey lap siding with white trim and a cedar-shingled gable",
     "services/siding"),
    ("windows.jpg", "dsu9V4MsRVw", "Clay Banks",
     "A dark green clapboard house with white-trimmed double-hung windows, a covered "
     "front porch and a magnolia in bloom",
     "services/windows"),
]

# Rejected after visual review — kept here so nobody re-picks them:
#   WSjAqAe46hI  deck, but subtropical (palms, agave). Wrong region for Cornwall.
#   hFsGUB0Fu30  fence, but dark, rain-soaked and weathered. Reads as neglect.
#   OqGJHtHHr-4  "bathroom" is a 3D render, not a photograph.
#   j6QSUeiW6vo  luxury kitchen; sets an unrepresentative price expectation.
#   NaCPcQBsECo  SHIPPED AND THEN PULLED 2026-08-17. It was the windows photo:
#                peeling sashes, flaking paint,
#                dead vines across the frame. A page selling window replacement
#                must show the RESULT, not the problem — a homeowner scanning it
#                sees decay and associates it with the contractor, not with the
#                windows they are replacing.
#   HckCpdBDeDk  clean modern house with black windows, and plainly Australian:
#                eucalyptus, a magpie in the road, tile roof, rendered walls.
#                Same failure as WSjAqAe46hI. LOOK AT THE BACKGROUND, not just
#                the subject.
#   6mZT8lxpZSA  architect-designed white house; wrong region and wrong budget.
#   Jds2filzouA  European townhouse with shutters. Not North American stock.
# Always LOOK at a downloaded file before shipping it. Search-result alt text
# is frequently wrong — one of the above was described as a window and is a kitchen.

URL = "https://unsplash.com/photos/{id}/download?w=1600"


def fetch(name, photo_id):
    dest = os.path.join(OUT, name)
    cmd = ["curl", "-sS", "-L", "--max-time", "45", "-o", dest,
           "-w", "%{http_code} %{size_download}", URL.format(id=photo_id)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return None, res.stderr.strip()
    code, size = res.stdout.split()
    if code != "200" or int(size) < 20000:
        return None, f"HTTP {code}, {size} bytes"
    return optimise(dest), None


def optimise(path):
    """Centre-crop to 16:10, cap the width, and write matching JPEG + WebP.

    The page renders these in a fixed 16:10 box, so cropping here rather than
    with object-fit means the bytes downloaded are the bytes displayed.
    """
    img = Image.open(path).convert("RGB")
    w, h = img.size
    if w / h > TARGET_RATIO:                       # too wide — trim the sides
        new_w = int(h * TARGET_RATIO)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:                                          # too tall — trim top/bottom,
        new_h = int(w / TARGET_RATIO)              # biased upward so horizons
        top = int((h - new_h) * 0.35)              # and rooflines survive
        img = img.crop((0, top, w, top + new_h))

    if img.width > TARGET_W:
        img = img.resize((TARGET_W, int(TARGET_W / TARGET_RATIO)), Image.LANCZOS)

    img.save(path, "JPEG", quality=78, optimize=True, progressive=True)
    img.save(os.path.splitext(path)[0] + ".webp", "WEBP", quality=76, method=6)
    return os.path.getsize(path)


def main():
    os.makedirs(OUT, exist_ok=True)
    print("Fetching photos:")
    rows, failed = [], 0
    for name, pid, who, alt, used in PHOTOS:
        size, err = fetch(name, pid)
        if err:
            print(f"  ✗ {name}: {err}")
            failed += 1
            continue
        print(f"  {name}  {size // 1024} KB")
        rows.append((name, pid, who, alt, used))

    lines = [
        "# Photo credits",
        "",
        "All photographs below are from [Unsplash](https://unsplash.com) under the",
        "[Unsplash License](https://unsplash.com/license): free for commercial use, no",
        "permission needed, attribution appreciated but not required.",
        "",
        "**These are stock photographs, not Elite Carpentry & Renovations' own work.**",
        "They are used as section imagery with descriptive alt text only. Replace them",
        "with real project photos as soon as the owner supplies them — real work beats",
        "stock on a trust-led site every time.",
        "",
        "Regenerate with `python3 tools/fetch-photos.py`.",
        "",
        "| File | Source | Photographer | Alt text | Used on |",
        "| --- | --- | --- | --- | --- |",
    ]
    for name, pid, who, alt, used in rows:
        lines.append(f"| `{name}` | https://unsplash.com/photos/{pid} | {who} | {alt} | /{used}/ |")
    lines.append("")

    with open(os.path.join(OUT, "CREDITS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n{len(rows)} photo(s) written, CREDITS.md updated.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
