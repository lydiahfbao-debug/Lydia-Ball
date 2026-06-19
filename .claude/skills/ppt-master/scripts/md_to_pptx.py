#!/usr/bin/env python3
"""Convert a simple markdown outline into a .pptx using the Deck helper.

Markdown spec (one slide per H1/H2 block):

    # Deck Title
    ## Subtitle line            -> becomes the title slide's subtitle

    # Section: Revenue          -> a section divider slide

    # Revenue grew 22% QoQ      -> a content slide; bullets follow
    - Total revenue $4.8M
    - Net new ARR $1.1M
    > Speaker note text          -> lines starting with '> ' become notes

    # Closing: Next steps        -> a closing slide (bullets follow)

Rules:
- `# Section: X`  -> section slide titled X
- `# Closing: X`  -> closing slide titled X
- first `#` in the file -> title slide; the following `## ...` is its subtitle
- any other `#`  -> bullet slide; `- ` lines are bullets
- `> ` lines attach as speaker notes to the current slide

Usage:
    python3 md_to_pptx.py input.md output.pptx
"""
from __future__ import annotations

import sys
from pathlib import Path

# Import the Deck class from the sibling script.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_deck import Deck  # noqa: E402


def parse(md_text):
    """Yield (kind, title, bullets, subtitle, notes) tuples."""
    slides = []
    cur = None
    first_h1_seen = False

    def flush():
        if cur is not None:
            slides.append(cur)

    for raw in md_text.splitlines():
        line = raw.rstrip()
        if line.startswith("# "):
            flush()
            title = line[2:].strip()
            if title.lower().startswith("section:"):
                cur = {"kind": "section", "title": title.split(":", 1)[1].strip(),
                       "bullets": [], "subtitle": None, "notes": []}
            elif title.lower().startswith("closing:"):
                cur = {"kind": "closing", "title": title.split(":", 1)[1].strip(),
                       "bullets": [], "subtitle": None, "notes": []}
            elif not first_h1_seen:
                cur = {"kind": "title", "title": title, "bullets": [],
                       "subtitle": None, "notes": []}
                first_h1_seen = True
            else:
                cur = {"kind": "bullets", "title": title, "bullets": [],
                       "subtitle": None, "notes": []}
        elif line.startswith("## ") and cur and cur["kind"] == "title":
            cur["subtitle"] = line[3:].strip()
        elif line.startswith("- ") and cur:
            cur["bullets"].append(line[2:].strip())
        elif line.startswith("> ") and cur:
            cur["notes"].append(line[2:].strip())
    flush()
    return slides


def build(slides, out_path):
    deck = Deck()
    for s in slides:
        notes = "\n".join(s["notes"]) or None
        if s["kind"] == "title":
            deck.title(s["title"], s["subtitle"], notes=notes)
        elif s["kind"] == "section":
            deck.section(s["title"], notes=notes)
        elif s["kind"] == "closing":
            deck.closing(s["title"], s["bullets"] or None, notes=notes)
        else:
            deck.bullets(s["title"], s["bullets"], notes=notes)
    return deck.save(out_path)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    md = Path(sys.argv[1]).read_text(encoding="utf-8")
    build(parse(md), sys.argv[2])


if __name__ == "__main__":
    main()
