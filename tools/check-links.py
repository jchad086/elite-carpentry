#!/usr/bin/env python3
"""
Verify every internal href/src in the built site resolves on disk, and that
every same-page #anchor points at an element that exists.

    python3 tools/check-links.py

This is the guard for the relativize.py approach: root-absolute paths get
rewritten to '../' chains based on directory depth, so a page written at the
wrong depth produces links that look fine in the source and 404 in a browser.
Exit code is non-zero when anything is broken, so it can gate a deploy.
"""

import os
import re
import sys
from urllib.parse import unquote, urldefrag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LINK = re.compile(r'(?:href|src)="([^"]+)"')
# srcset holds a comma-separated candidate list with optional descriptors.
# Checking it matters: it is easy for these to stay root-absolute and 404 only
# at the GitHub Pages project URL, which is exactly what happened once already.
SRCSET = re.compile(r'srcset="([^"]+)"')
ID = re.compile(r'\sid="([^"]+)"')
EXTERNAL = ("http://", "https://", "mailto:", "tel:", "data:", "//")


def urls_in(src):
    """Every internal URL referenced by the document, srcset candidates included."""
    for u in LINK.findall(src):
        yield u
    for value in SRCSET.findall(src):
        for cand in value.split(","):
            cand = cand.strip()
            if cand:
                yield cand.split()[0]


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "tools", "__pycache__"}]
        for fn in sorted(filenames):
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def main():
    problems = []
    checked = 0

    for path in html_files():
        rel = os.path.relpath(path, ROOT)
        with open(path, encoding="utf-8") as f:
            src = f.read()
        ids = set(ID.findall(src))
        base = os.path.dirname(path)

        for raw in urls_in(src):
            if raw.startswith(EXTERNAL):
                continue
            if raw.startswith("/"):
                problems.append(f"{rel}: {raw} is root-absolute — relativize.py "
                                f"missed it; will 404 at the Pages project URL")
                continue
            checked += 1
            target, frag = urldefrag(unquote(raw))

            if not target:                       # pure "#anchor" on this page
                if frag and frag not in ids:
                    problems.append(f"{rel}: #{frag} — no element with that id")
                continue

            resolved = os.path.normpath(os.path.join(base, target))
            if target.endswith("/"):
                resolved = os.path.join(resolved, "index.html")

            if not os.path.exists(resolved):
                problems.append(f"{rel}: {raw} -> {os.path.relpath(resolved, ROOT)} (missing)")
                continue

            # Cross-page fragments: confirm the id exists in the target page.
            if frag and resolved.endswith(".html"):
                with open(resolved, encoding="utf-8") as tf:
                    if frag not in set(ID.findall(tf.read())):
                        problems.append(f"{rel}: {raw} — #{frag} not in target page")

    print(f"Checked {checked} internal links across "
          f"{len(list(html_files()))} pages.")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print("  ✗", p)
        return 1
    print("All internal links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
