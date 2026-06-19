# python-pptx Cookbook

Copy-paste recipes. Import surface:

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
```

## Units

- `Inches(1)`, `Pt(18)`, `Emu(914400)` — 1 inch = 914400 EMU = 72 pt.
- Widescreen 16:9 canvas: width `Inches(13.333)`, height `Inches(7.5)`.

## Create a 16:9 presentation

```python
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
```

## Blank slide (full manual control)

Layout index 6 is the blank layout in the default template.

```python
blank = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank)
```

## Full-bleed background color

```python
def set_bg(slide, hex_color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(hex_color)
```

## Text box with styling

```python
def add_text(slide, text, left, top, width, height,
             size=18, bold=False, color="111111", align=PP_ALIGN.LEFT,
             font="Calibri"):
    box = slide.shapes.add_textbox(Inches(left), Inches(top),
                                   Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = font
    run.font.color.rgb = RGBColor.from_string(color)
    return box
```

## Bulleted list

```python
def add_bullets(slide, items, left, top, width, height,
                size=20, color="111111", font="Calibri"):
    box = slide.shapes.add_textbox(Inches(left), Inches(top),
                                   Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {item}"
        p.level = 0
        p.space_after = Pt(8)
        for run in p.runs:
            run.font.size = Pt(size)
            run.font.name = font
            run.font.color.rgb = RGBColor.from_string(color)
    return box
```

## Image (fit within a box, preserve aspect)

```python
slide.shapes.add_picture("logo.png", Inches(0.5), Inches(0.5),
                         height=Inches(1.0))   # set ONE of width/height
```

Add alt text for accessibility:

```python
pic = slide.shapes.add_picture("chart.png", Inches(1), Inches(1.5), width=Inches(6))
pic._element._nvXxPr.cNvPr.set("descr", "Bar chart of revenue by region")
```

## Table

```python
def add_table(slide, rows, cols, data, left, top, width, height,
              header_fill="0B5394", header_text="FFFFFF"):
    table = slide.shapes.add_table(rows, cols, Inches(left), Inches(top),
                                   Inches(width), Inches(height)).table
    for r in range(rows):
        for c in range(cols):
            cell = table.cell(r, c)
            cell.text = str(data[r][c])
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(14)
                    if r == 0:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor.from_string(header_text)
            if r == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor.from_string(header_fill)
    return table
```

## Native (editable) chart

Native charts stay editable in PowerPoint and inherit theme colors.

```python
def add_bar_chart(slide, categories, series, left, top, width, height,
                  title=None):
    chart_data = CategoryChartData()
    chart_data.categories = categories
    for name, values in series.items():        # series: {"2023": [..], "2024": [..]}
        chart_data.add_series(name, values)
    gframe = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(left), Inches(top), Inches(width), Inches(height),
        chart_data)
    chart = gframe.chart
    if title:
        chart.has_title = True
        chart.chart_title.text_frame.text = title
    chart.has_legend = len(series) > 1
    if chart.has_legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
    return chart
```

Common `XL_CHART_TYPE` values: `COLUMN_CLUSTERED`, `BAR_CLUSTERED`,
`LINE`, `LINE_MARKERS`, `PIE`, `DOUGHNUT`, `XY_SCATTER`, `AREA`.

## Speaker notes

```python
slide.notes_slide.notes_text_frame.text = "Detail the presenter says aloud."
```

## Using built-in layouts (title & content)

```python
slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content
slide.shapes.title.text = "Slide title"
body = slide.placeholders[1].text_frame
body.text = "First bullet"
body.add_paragraph().text = "Second bullet"
```

Default template layout indices: 0 Title, 1 Title+Content, 2 Section Header,
5 Title Only, 6 Blank.

## Save

```python
prs.save("out.pptx")
print(f"Saved {len(prs.slides.slides) if hasattr(prs.slides,'slides') else len(prs.slides._sldIdLst)} slides")
# simplest: print(f"Saved {len(prs.slides)} slides -> out.pptx")
```
