# Design Guidelines

Apply these rules when building any deck. They are ordered by impact.

## Content density

- **One idea per slide.** The slide title should be the takeaway, written as a
  full assertion ("Revenue grew 22% QoQ"), not a topic label ("Revenue").
- **6×8 rule:** at most ~6 bullets, at most ~8 words each. If you exceed it,
  split the slide or move detail into speaker notes.
- **No paragraphs on slides.** Prose belongs in notes or a handout.
- **Cut filler.** Remove "In this slide we will…", redundant adjectives, and
  obvious labels.

## Typography

| Element        | Size      | Weight  |
|----------------|-----------|---------|
| Slide title    | 32–40 pt  | Bold    |
| Section header | 36–44 pt  | Bold    |
| Body / bullets | 18–24 pt  | Regular |
| Captions/notes | 12–14 pt  | Regular |

- Never go below 14pt on a slide (back-row legibility).
- Use **one** font family for the whole deck (two at most: one display, one body).
- Left-align body text. Center only titles on title/section slides.
- Avoid ALL CAPS for long strings; fine for short labels.

## Layout & spacing

- Standard widescreen is 13.333 in × 7.5 in (16:9). Default to this.
- Keep a consistent margin (~0.5–0.7 in) on all edges; don't let text touch.
- Align elements to a grid. Reuse the same X/Y for repeated elements.
- Embrace whitespace. A sparse slide reads as confident; a crammed one reads as
  anxious.
- One focal point per slide. Size and color draw the eye — use them on the one
  thing that matters.

## Color

- One primary, one accent, plus neutrals (near-black text, off-white bg).
- Maintain high contrast (WCAG AA ≈ 4.5:1 for body text).
- Use color to encode meaning consistently (e.g., accent = "the number that
  matters"), not for decoration.
- See `color_themes.md` for ready-made palettes.

## Data: charts vs tables

- **Trends / comparisons / proportions → chart.** Bar for comparison, line for
  time series, pie/donut only for ≤4 parts of a whole.
- **Exact values that must be read precisely → table**, kept small (≤5 cols).
- Label data directly when possible instead of relying on a legend.
- Never use 3-D charts; they distort perception.
- Sort categories meaningfully (by value, not alphabetically) unless order has
  inherent meaning.

## Consistency

- Repeat the same layout for the same kind of slide. Surprise is friction.
- Use the slide master / layouts rather than free-floating text boxes when you
  want global consistency.
- Number slides (except the title) for easy reference in discussion.

## Accessibility

- Don't rely on color alone to convey information (add labels/patterns).
- Provide `alt text` on images for screen readers.
- Keep contrast high; test light-on-dark combos especially.
