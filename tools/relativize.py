#!/usr/bin/env python3
"""
Rewrite root-absolute href/src values ("/assets/...") to depth-correct relative
paths ("../assets/...").

Why: root-absolute paths only resolve when the site is served from a domain
root. Relative paths let the exact same files work locally, at a GitHub Pages
project URL (username.github.io/topreno/), and at the custom domain — which
means the deploy can be verified before DNS is cut over.

Only `href="..."` and `src="..."` are touched. Absolute production URLs in
canonical tags, Open Graph metadata, and JSON-LD are left alone on purpose.

Idempotent: values that are already relative are skipped, so re-running is safe.

Run from the repo root:  python3 tools/relativize.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Attribute values starting with a single "/" (not "//", which is protocol-relative)
PATTERN = re.compile(r'((?:href|src)=")/(?!/)([^"]*)"')

# srcset needs its own pass: it holds a comma-separated candidate list, each
# entry optionally followed by a width or density descriptor ("a.webp 2x"), so
# the single-value regex above cannot handle it. Missing this left every
# <source srcset="/assets/..."> root-absolute, which works on the custom domain
# but 404s at the GitHub Pages project URL — the staging preview this whole
# module exists to make possible.
SRCSET = re.compile(r'(srcset=")([^"]*)"')


def prefix_for(depth):
    """'' at the root, '../' one level down, '../../' two levels down."""
    return "../" * depth


def _rewrite_url(url, pre):
    if url == "/":
        return pre or "./"
    if url.startswith("/") and not url.startswith("//"):
        return pre + url[1:]
    return url                      # already relative, or absolute/protocol-relative


def relativize(html, depth):
    """Rewrite root-absolute href/src/srcset for a page nested `depth` dirs deep."""
    pre = prefix_for(depth)

    def sub(m):
        attr, path = m.group(1), m.group(2)
        # href="/" -> "./" at root, "../" below it
        if path == "":
            return f'{attr}{pre or "./"}"'
        return f'{attr}{pre}{path}"'

    def sub_srcset(m):
        cands = []
        for cand in m.group(2).split(","):
            cand = cand.strip()
            if not cand:
                continue
            parts = cand.split(None, 1)
            rest = f" {parts[1]}" if len(parts) > 1 else ""
            cands.append(_rewrite_url(parts[0], pre) + rest)
        return f'{m.group(1)}{", ".join(cands)}"'

    return SRCSET.sub(sub_srcset, PATTERN.sub(sub, html))


def depth_of(rel_path):
    """Directory depth of a file relative to the site root."""
    return rel_path.count(os.sep)


def main():
    changed = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "tools"}]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            with open(full, encoding="utf-8") as f:
                src = f.read()
            out = relativize(src, depth_of(rel))
            if out != src:
                with open(full, "w", encoding="utf-8") as f:
                    f.write(out)
                changed += 1
                print("rewrote", rel)
    print(f"\n{changed} file(s) updated." if changed else "\nNothing to do — already relative.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
