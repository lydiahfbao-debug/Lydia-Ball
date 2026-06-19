# Color Themes & Fonts

Ready-to-use palettes. Each gives a background, primary text, primary brand
color, accent, and a muted/secondary. Hex values are RGB; in python-pptx use
`RGBColor(0x11, 0x22, 0x33)` or `RGBColor.from_string("112233")`.

The `Deck` helper in `scripts/build_deck.py` accepts a `theme` dict with these
keys: `bg`, `text`, `primary`, `accent`, `muted`, `title_font`, `body_font`.

## Corporate Blue (default, safe for business)

```python
THEME = {
    "bg":      "FFFFFF",
    "text":    "1A1A2E",
    "primary": "0B5394",
    "accent":  "F39C12",
    "muted":   "7F8C9A",
    "title_font": "Calibri",
    "body_font":  "Calibri",
}
```

## Midnight (dark, modern, good for keynotes)

```python
THEME = {
    "bg":      "0E1117",
    "text":    "E6EDF3",
    "primary": "58A6FF",
    "accent":  "F778BA",
    "muted":   "8B949E",
    "title_font": "Arial",
    "body_font":  "Arial",
}
```

## Slate & Teal (clean, technical)

```python
THEME = {
    "bg":      "F7F9FB",
    "text":    "22303C",
    "primary": "0E7C86",
    "accent":  "E07A5F",
    "muted":   "94A3B8",
    "title_font": "Helvetica",
    "body_font":  "Helvetica",
}
```

## Warm Editorial (reports, narrative decks)

```python
THEME = {
    "bg":      "FBF7F0",
    "text":    "2B2118",
    "primary": "9A3B3B",
    "accent":  "C08552",
    "muted":   "8C7B6B",
    "title_font": "Georgia",
    "body_font":  "Georgia",
}
```

## Mono Minimal (high-contrast, content-first)

```python
THEME = {
    "bg":      "FFFFFF",
    "text":    "111111",
    "primary": "111111",
    "accent":  "E63946",
    "muted":   "999999",
    "title_font": "Inter",
    "body_font":  "Inter",
}
```

## Font notes

- Fonts must be installed on the machine that *opens* the deck for them to render
  as intended; otherwise PowerPoint substitutes. Stick to widely available
  families (Calibri, Arial, Helvetica, Georgia, Times New Roman) unless the user
  controls the target machines.
- Pair at most one display font (titles) with one body font.
- If the user gives brand hex colors, build a custom theme dict in the same shape
  and pass it through.
