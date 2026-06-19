---
name: ppt-master
description: Create, edit, and polish professional PowerPoint (.pptx) presentations programmatically with python-pptx. Use when the user asks to build a slide deck, generate a presentation, turn an outline/markdown/report into slides, restyle or template a deck, add charts/tables/images to slides, or export/convert presentation content. Covers layout, typography, color themes, charts, tables, speaker notes, and reusable templates.
---

# PPT Master

Build clean, on-brand PowerPoint decks programmatically. This skill uses
[`python-pptx`](https://python-pptx.readthedocs.io/) so decks are reproducible,
diffable, and scriptable — no manual clicking in PowerPoint required.

## When to use this skill

- "Make a presentation / slide deck about X"
- "Turn this document / outline / markdown into slides"
- "Add a chart (or table, or image) to this deck"
- "Restyle this deck with our brand colors / a dark theme"
- "Create a reusable presentation template"

## Workflow

Follow these steps in order. Do not skip the planning step — decks built without
an outline tend to be unbalanced and verbose.

### 1. Set up the environment

Ensure `python-pptx` is installed:

```bash
python3 -c "import pptx" 2>/dev/null || pip install python-pptx
```

### 2. Plan the deck (always do this first)

Before writing any code, produce a short outline: one line per slide with the
slide type and the single key message. Keep it tight — **one idea per slide**.

```
1. Title         — "Q3 Growth Review"
2. Agenda        — 4 sections
3. Section header— "Revenue"
4. Content       — Revenue up 22% QoQ (bullets)
5. Chart         — Revenue by region (bar)
6. Table         — Top 5 accounts
7. Closing       — Next steps + contact
```

Confirm the outline with the user if the request is open-ended, then build.

### 3. Choose an approach

- **Most decks:** use `scripts/build_deck.py` as a starting point. It defines a
  `Deck` helper class wrapping python-pptx with sensible defaults for titles,
  bullet slides, section headers, images, tables, charts, and speaker notes.
- **From structured content:** if the user gives you markdown or an outline,
  use `scripts/md_to_pptx.py` which converts a simple markdown spec into a deck.
- **Editing an existing .pptx:** open it with `Presentation("existing.pptx")`
  and modify in place; do not rebuild from scratch unless asked.

### 4. Apply design discipline

Read `references/design_guidelines.md` and apply it. The non-negotiables:

- **One idea per slide.** If a slide needs a paragraph, it needs to be split.
- **≤ 6 bullets per slide, ≤ ~8 words per bullet.** Slides are not documents.
- **Consistent type scale.** Title ~32–40pt, body ~18–24pt. Never below 14pt.
- **A restrained palette.** One primary, one accent, neutrals. See the themes in
  `references/color_themes.md`.
- **High contrast.** Dark text on light, or light text on dark — never mid-grey.
- **Charts over tables** when showing trends; **tables** only for precise values.
- **Speaker notes** carry the detail that does not belong on the slide.

### 5. Build, then verify

After generating the `.pptx`:

1. Confirm the file exists and reports the expected slide count (the build
   scripts print this).
2. Optionally render thumbnails to visually check layout — see
   `references/rendering.md` for converting slides to images with LibreOffice.
3. Report the output path to the user and offer to send the file.

## Reference files

Load these as needed (progressive disclosure — don't read all of them upfront):

- `references/design_guidelines.md` — layout, typography, content density rules.
- `references/color_themes.md` — ready-to-use color palettes (hex) and fonts.
- `references/python_pptx_cookbook.md` — copy-paste recipes for common tasks
  (title slides, bullets, images, tables, native charts, notes, EMU/Inches).
- `references/rendering.md` — how to render a deck to PNG/PDF for visual review.

## Scripts

- `scripts/build_deck.py` — `Deck` helper class + a runnable example deck.
- `scripts/md_to_pptx.py` — convert a markdown outline into a `.pptx`.

Both are meant to be read and adapted, not run blindly. Copy the relevant parts
into a build script tailored to the user's content.

## Quick start

```bash
# Generate the example deck to confirm the toolchain works
python3 .claude/skills/ppt-master/scripts/build_deck.py /tmp/example.pptx
```
