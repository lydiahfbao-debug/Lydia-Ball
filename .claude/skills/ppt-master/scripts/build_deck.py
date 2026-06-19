#!/usr/bin/env python3
"""Deck builder helper for the ppt-master skill.

A thin, opinionated wrapper around python-pptx that produces clean 16:9 slides
from a theme dict. Read it, then adapt the example at the bottom to the user's
content — or import `Deck` into a tailored build script.

Usage:
    python3 build_deck.py [output.pptx]

Requires: pip install python-pptx
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION


# Default theme. Swap for any palette in references/color_themes.md, or build a
# custom dict in the same shape from the user's brand colors.
DEFAULT_THEME = {
    "bg": "FFFFFF",
    "text": "1A1A2E",
    "primary": "0B5394",
    "accent": "F39C12",
    "muted": "7F8C9A",
    "title_font": "Calibri",
    "body_font": "Calibri",
}

EMU_W = Inches(13.333)  # 16:9 widescreen
EMU_H = Inches(7.5)
MARGIN = 0.7  # inches


@dataclass
class Deck:
    """Build a presentation slide by slide."""

    theme: dict = field(default_factory=lambda: dict(DEFAULT_THEME))

    def __post_init__(self):
        self.prs = Presentation()
        self.prs.slide_width = EMU_W
        self.prs.slide_height = EMU_H
        self._blank = self.prs.slide_layouts[6]

    # --- internals -------------------------------------------------------
    def _rgb(self, key):
        return RGBColor.from_string(self.theme[key])

    def _new_slide(self, bg=None):
        slide = self.prs.slides.add_slide(self._blank)
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor.from_string(bg or self.theme["bg"])
        return slide

    def _text(self, slide, text, left, top, width, height, *, size, bold=False,
              color=None, align=PP_ALIGN.LEFT, font=None):
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
        run.font.name = font or self.theme["body_font"]
        run.font.color.rgb = (RGBColor.from_string(color) if color
                              else self._rgb("text"))
        return box

    def _notes(self, slide, notes):
        if notes:
            slide.notes_slide.notes_text_frame.text = notes

    # --- public slide types ---------------------------------------------
    def title(self, title, subtitle=None, *, notes=None):
        slide = self._new_slide()
        self._text(slide, title, MARGIN, 2.6, 13.333 - 2 * MARGIN, 1.6,
                   size=40, bold=True, color=self.theme["primary"],
                   align=PP_ALIGN.CENTER, font=self.theme["title_font"])
        if subtitle:
            self._text(slide, subtitle, MARGIN, 4.2, 13.333 - 2 * MARGIN, 1.0,
                       size=22, color=self.theme["muted"], align=PP_ALIGN.CENTER)
        self._notes(slide, notes)
        return slide

    def section(self, title, *, notes=None):
        slide = self._new_slide(bg=self.theme["primary"])
        self._text(slide, title, MARGIN, 3.0, 13.333 - 2 * MARGIN, 1.5,
                   size=40, bold=True, color=self.theme["bg"],
                   align=PP_ALIGN.LEFT, font=self.theme["title_font"])
        self._notes(slide, notes)
        return slide

    def _title_band(self, slide, title):
        self._text(slide, title, MARGIN, 0.5, 13.333 - 2 * MARGIN, 1.0,
                   size=32, bold=True, color=self.theme["primary"],
                   font=self.theme["title_font"])

    def bullets(self, title, items, *, notes=None):
        slide = self._new_slide()
        self._title_band(slide, title)
        box = slide.shapes.add_textbox(Inches(MARGIN), Inches(1.7),
                                       Inches(13.333 - 2 * MARGIN), Inches(5.2))
        tf = box.text_frame
        tf.word_wrap = True
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = f"•  {item}"
            p.space_after = Pt(10)
            for run in p.runs:
                run.font.size = Pt(22)
                run.font.name = self.theme["body_font"]
                run.font.color.rgb = self._rgb("text")
        self._notes(slide, notes)
        return slide

    def image(self, title, image_path, *, notes=None, alt=None):
        slide = self._new_slide()
        self._title_band(slide, title)
        pic = slide.shapes.add_picture(image_path, Inches(MARGIN), Inches(1.7),
                                       width=Inches(13.333 - 2 * MARGIN))
        if alt:
            pic._element._nvXxPr.cNvPr.set("descr", alt)
        self._notes(slide, notes)
        return slide

    def table(self, title, data, *, notes=None):
        slide = self._new_slide()
        self._title_band(slide, title)
        rows, cols = len(data), len(data[0])
        tbl = slide.shapes.add_table(rows, cols, Inches(MARGIN), Inches(1.8),
                                     Inches(13.333 - 2 * MARGIN),
                                     Inches(0.5 * rows)).table
        for r in range(rows):
            for c in range(cols):
                cell = tbl.cell(r, c)
                cell.text = str(data[r][c])
                for p in cell.text_frame.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(14)
                        run.font.name = self.theme["body_font"]
                        if r == 0:
                            run.font.bold = True
                            run.font.color.rgb = self._rgb("bg")
                        else:
                            run.font.color.rgb = self._rgb("text")
                if r == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = self._rgb("primary")
        self._notes(slide, notes)
        return slide

    def bar_chart(self, title, categories, series, *, notes=None,
                  chart_title=None):
        """series: dict of {series_name: [values...]}"""
        slide = self._new_slide()
        self._title_band(slide, title)
        cd = CategoryChartData()
        cd.categories = categories
        for name, values in series.items():
            cd.add_series(name, values)
        gframe = slide.shapes.add_chart(
            XL_CHART_TYPE.COLUMN_CLUSTERED,
            Inches(MARGIN), Inches(1.7),
            Inches(13.333 - 2 * MARGIN), Inches(5.0), cd)
        chart = gframe.chart
        if chart_title:
            chart.has_title = True
            chart.chart_title.text_frame.text = chart_title
        else:
            chart.has_title = False
        chart.has_legend = len(series) > 1
        if chart.has_legend:
            chart.legend.position = XL_LEGEND_POSITION.BOTTOM
            chart.legend.include_in_layout = False
        self._notes(slide, notes)
        return slide

    def closing(self, title, items=None, *, notes=None):
        slide = self._new_slide(bg=self.theme["primary"])
        self._text(slide, title, MARGIN, 1.5, 13.333 - 2 * MARGIN, 1.2,
                   size=36, bold=True, color=self.theme["bg"],
                   font=self.theme["title_font"])
        if items:
            box = slide.shapes.add_textbox(Inches(MARGIN), Inches(3.0),
                                           Inches(13.333 - 2 * MARGIN), Inches(3.5))
            tf = box.text_frame
            tf.word_wrap = True
            for i, item in enumerate(items):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.text = f"•  {item}"
                p.space_after = Pt(10)
                for run in p.runs:
                    run.font.size = Pt(22)
                    run.font.name = self.theme["body_font"]
                    run.font.color.rgb = self._rgb("bg")
        self._notes(slide, notes)
        return slide

    def save(self, path):
        self.prs.save(path)
        print(f"Saved {len(self.prs.slides._sldIdLst)} slides -> {path}")
        return path


def _example(path):
    deck = Deck()
    deck.title("Q3 Growth Review", "Prepared for the Leadership Team · 2026",
               notes="Welcome everyone. Today: how Q3 went and what's next.")
    deck.bullets("Agenda", [
        "Revenue performance",
        "Regional breakdown",
        "Top accounts",
        "Next steps",
    ])
    deck.section("Revenue")
    deck.bullets("Revenue grew 22% QoQ", [
        "Total revenue: $4.8M, up from $3.9M",
        "Net new ARR: $1.1M",
        "Gross margin held at 78%",
        "Churn down to 1.9% monthly",
    ], notes="Lead with the headline number, then the supporting metrics.")
    deck.bar_chart("Revenue by region ($K)",
                   ["North", "EMEA", "APAC", "LATAM"],
                   {"Q2": [1200, 900, 600, 300],
                    "Q3": [1500, 1100, 800, 400]})
    deck.table("Top 5 accounts", [
        ["Account", "ARR ($K)", "Growth"],
        ["Acme Corp", "420", "+18%"],
        ["Globex", "310", "+9%"],
        ["Initech", "260", "+31%"],
        ["Umbrella", "240", "+4%"],
        ["Soylent", "190", "+22%"],
    ])
    deck.closing("Next steps", [
        "Double down on APAC expansion",
        "Launch tiered pricing in Q4",
        "Hire 3 enterprise AEs",
    ], notes="Close with a clear ask and contact info.")
    deck.save(path)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "deck.pptx"
    _example(out)
