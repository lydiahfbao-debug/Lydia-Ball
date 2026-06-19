# ppt-master skill

A Claude Code [Skill](https://code.claude.com/docs) for building professional
PowerPoint (`.pptx`) decks programmatically with
[`python-pptx`](https://python-pptx.readthedocs.io/).

## Layout

```
ppt-master/
├── SKILL.md                         # entry point: when/how to use, workflow
├── references/
│   ├── design_guidelines.md         # layout, typography, content density
│   ├── color_themes.md              # ready-made palettes + fonts
│   ├── python_pptx_cookbook.md      # copy-paste recipes
│   └── rendering.md                 # render to PNG/PDF for visual review
└── scripts/
    ├── build_deck.py                # Deck helper class + example deck
    └── md_to_pptx.py                # markdown outline -> .pptx
```

## Try it

```bash
pip install python-pptx
python3 scripts/build_deck.py /tmp/example.pptx
```

The skill activates automatically when you ask Claude Code to build, edit, or
restyle a slide deck. See `SKILL.md` for the full workflow.
