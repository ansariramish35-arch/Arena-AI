#!/usr/bin/env python3
"""Build the SwachhAI internship project presentation as an editable PowerPoint.

All diagrams and layouts are native PowerPoint shapes/text. The three certificate
slides use raster copies of the certificates supplied with the project materials.

Run from anywhere:
    python3 summer-internship-report/build/build_presentation.py
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "SwachhAI_Project_Presentation.pptx"
CERT_DIR = ROOT / "certificates"

# 16:9 wide canvas.
SW = 13.333
SH = 7.5
FONT = "Arial"

# A calm, high-contrast palette inspired by urban greenery and circularity.
C = {
    "ink": "173330",
    "ink2": "244641",
    "navy": "102C2A",
    "green": "278160",
    "green2": "43A47A",
    "mint": "DDF1E6",
    "lime": "B9DB69",
    "teal": "2C9292",
    "aqua": "58C7B5",
    "blue": "477DC0",
    "orange": "E28A48",
    "amber": "F1C562",
    "coral": "D96C5C",
    "purple": "8A6BB2",
    "brown": "9B755D",
    "slate": "6F7D7A",
    "grey": "AEBBB6",
    "line": "DEE7E1",
    "paper": "F5F8F4",
    "white": "FFFFFF",
    "soft": "EAF1EC",
    "soft2": "EDF4F1",
    "darkline": "31534D",
    "black": "151D1B",
}

STREAMS = [
    ("WET", "Peels · food scraps", "278160"),
    ("DRY", "Clean paper · plastics", "2C9292"),
    ("E-WASTE", "Phones · chargers", "477DC0"),
    ("HAZARD", "Batteries · CFLs", "E28A48"),
    ("SANITARY", "Pads · masks", "D96C5C"),
    ("TEXTILE", "Clothes · footwear", "8A6BB2"),
    ("DEBRIS", "Tiles · rubble", "9B755D"),
    ("REJECT", "Laminates · soiled film", "6F7D7A"),
]


def rgb(value: str) -> RGBColor:
    value = value.lstrip("#")
    return RGBColor(int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def add_bg(slide, color: str = "paper"):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(C[color] if color in C else color)


def shape(slide, x, y, w, h, fill: str, line: Optional[str] = None,
          kind=MSO_SHAPE.ROUNDED_RECTANGLE, radius=True):
    if isinstance(fill, str) and fill in C:
        fill = C[fill]
    if isinstance(line, str) and line in C:
        line = C[line]
    shp = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb(fill)
    if line:
        shp.line.color.rgb = rgb(line)
        shp.line.width = Pt(1)
    else:
        shp.line.fill.background()
    return shp


def line(slide, x1, y1, x2, y2, color="line", width=1.0):
    # Native straight-line connector (kept behind text and cards by creation order).
    ln = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2)
    )
    ln.line.color.rgb = rgb(C[color] if color in C else color)
    ln.line.width = Pt(width)
    return ln


def text(slide, x, y, w, h, value: str, size=14, color="ink", bold=False,
         align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, margin=0.02,
         font=FONT, italic=False, char_spacing=None):
    if isinstance(color, str) and color in C:
        color = C[color]
    # Long-form body boxes are deliberately larger than metadata/eyebrows so the deck
    # remains readable when projected. Small labels and footnotes retain their set size.
    if size <= 12 and h >= 0.40 and w >= 1.70:
        size = min(size * 1.22, 14.2)
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    p.line_spacing = 1.05
    run = p.add_run()
    run.text = value
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = rgb(color)
    if char_spacing is not None:
        run._r.get_or_add_rPr().set("spc", str(char_spacing))
    return tb


def rich_text(slide, x, y, w, h, runs, size=14, color="ink", align=PP_ALIGN.LEFT,
              valign=MSO_ANCHOR.TOP, margin=0.02, line_spacing=1.05):
    """Add one paragraph from (text, bold, color, italic, hyperlink) tuples."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    p.line_spacing = line_spacing
    for value, bold, run_color, italic, hyperlink in runs:
        r = p.add_run()
        r.text = value
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = rgb(C[run_color] if run_color in C else run_color)
        if hyperlink:
            r.hyperlink.address = hyperlink
    return tb


def bullet(slide, x, y, w, body, size=13, color="ink", dot="green", h=0.5,
           dot_size=0.085):
    shape(slide, x, y + 0.10, dot_size, dot_size, dot, kind=MSO_SHAPE.OVAL)
    return text(slide, x + 0.20, y, w - 0.20, h, body, size=size, color=color, margin=0)


def pill(slide, x, y, w, label, fill="mint", color="green", size=10.5, h=0.31,
         line_color=None):
    shape(slide, x, y, w, h, fill, line=line_color)
    text(slide, x + 0.05, y + 0.005, w - 0.10, h - 0.01, label, size=size,
         color=color, bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE,
         margin=0)


def card(slide, x, y, w, h, fill="white", border="line"):
    return shape(slide, x, y, w, h, fill, line=border)


def add_header(slide, section: str, title_text: str, subtitle: Optional[str] = None):
    add_bg(slide)
    text(slide, 0.66, 0.30, 11.95, 0.23, section.upper(), 9.5, "green", True, margin=0)
    text(slide, 0.66, 0.59, 12.0, 0.55, title_text, 27, "ink", True, margin=0)
    if subtitle:
        text(slide, 0.68, 1.16, 12.0, 0.32, subtitle, 12.5, "slate", margin=0)
        line(slide, 0.66, 1.58, 12.66, 1.58, "line", 0.8)
    else:
        line(slide, 0.66, 1.30, 12.66, 1.30, "line", 0.8)


def add_footer(slide, number: int, total: int, dark=False):
    fg = "grey" if dark else "slate"
    stroke = "darkline" if dark else "line"
    line(slide, 0.66, 7.05, 12.66, 7.05, stroke, 0.7)
    text(slide, 0.68, 7.13, 8.5, 0.18,
         "MOHAMMAD RAMISH ANSARI  ·  SWACHHAI  ·  AI FOR SUSTAINABILITY",
         8.2, fg, True, margin=0)
    text(slide, 11.55, 7.11, 1.10, 0.20, f"{number:02d} / {total:02d}",
         9.0, fg, True, align=PP_ALIGN.RIGHT, margin=0)


def add_arrow(slide, x, y, w=0.34, h=0.28, color="green", direction="right"):
    kind = {
        "right": MSO_SHAPE.CHEVRON,
        "down": MSO_SHAPE.DOWN_ARROW,
        "left": MSO_SHAPE.LEFT_ARROW,
        "up": MSO_SHAPE.UP_ARROW,
    }[direction]
    shp = shape(slide, x, y, w, h, color, kind=kind)
    return shp


def add_card_heading(slide, x, y, w, title_text, kicker=None, color="green"):
    if kicker:
        text(slide, x, y, w, 0.18, kicker.upper(), 8.7, color, True, margin=0)
        y += 0.23
    text(slide, x, y, w, 0.36, title_text, 15.5, "ink", True, margin=0)


def add_icon_badge(slide, x, y, d, label, fill="green", txt="white", size=13):
    shape(slide, x, y, d, d, fill, kind=MSO_SHAPE.OVAL)
    text(slide, x, y + 0.005, d, d - 0.01, label, size=size, color=txt, bold=True,
         align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0)


def contain_picture(slide, path: Path, x, y, w, h):
    with Image.open(path) as im:
        iw, ih = im.size
    ratio = iw / ih
    box_ratio = w / h
    if ratio >= box_ratio:
        pw, ph = w, w / ratio
        px, py = x, y + (h - ph) / 2
    else:
        ph, pw = h, h * ratio
        px, py = x + (w - pw) / 2, y
    return slide.shapes.add_picture(str(path), Inches(px), Inches(py),
                                    width=Inches(pw), height=Inches(ph))


def set_slide_title_meta(prs: Presentation, title: str, subject: str):
    prs.core_properties.title = title
    prs.core_properties.subject = subject
    prs.core_properties.author = "Mohammad Ramish Ansari"
    prs.core_properties.keywords = "SwachhAI, waste segregation, agentic AI, IBM Granite, RAG"
    prs.core_properties.comments = (
        "Concept-stage presentation. Architecture and demo walkthrough are illustrative; "
        "no deployment, model accuracy, field-test, or measured-impact claim is made."
    )


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    blank = prs.slide_layouts[6]
    total = 22
    set_slide_title_meta(
        prs,
        "SwachhAI — AI-Guided Waste Segregation and Circularity Assistant",
        "IBM University Engagement / AICTE 2026 project submission",
    )

    # 1 — Cover
    s = prs.slides.add_slide(blank)
    add_bg(s, "navy")
    # Low-contrast concentric rings and leaf-like geometry create a circularity motif.
    for x, y, d, col in [(8.8, 1.05, 3.6, "darkline"), (9.45, 1.70, 2.3, "green"),
                         (10.0, 2.25, 1.2, "teal")]:
        ring = shape(s, x, y, d, d, "navy", line=col, kind=MSO_SHAPE.OVAL)
        ring.fill.transparency = 100
        ring.line.width = Pt(2.0)
    shape(s, 10.16, 2.42, 0.90, 0.90, "lime", kind=MSO_SHAPE.OVAL)
    text(s, 10.18, 2.60, 0.86, 0.32, "AI", 20, "navy", True,
         align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0)
    # Small output cards to signal the user journey.
    shape(s, 8.10, 5.03, 1.38, 0.60, "ink2")
    text(s, 8.20, 5.12, 1.18, 0.18, "IDENTIFY", 8.5, "lime", True, margin=0)
    text(s, 8.20, 5.33, 1.18, 0.19, "item → stream", 10, "white", True, margin=0)
    add_arrow(s, 9.57, 5.20, 0.35, 0.22, "lime")
    shape(s, 9.98, 5.03, 1.38, 0.60, "ink2")
    text(s, 10.08, 5.12, 1.18, 0.18, "ACT SAFELY", 8.5, "aqua", True, margin=0)
    text(s, 10.08, 5.33, 1.18, 0.19, "short protocol", 10, "white", True, margin=0)
    add_arrow(s, 11.45, 5.20, 0.35, 0.22, "lime")
    shape(s, 11.86, 5.03, 0.90, 0.60, "ink2")
    text(s, 11.93, 5.12, 0.76, 0.18, "SEE", 8.5, "amber", True, margin=0)
    text(s, 11.93, 5.33, 0.76, 0.19, "impact", 10, "white", True, margin=0)

    pill(s, 0.78, 0.67, 3.34, "IBM UNIVERSITY ENGAGEMENT  ·  AICTE 2026",
         fill="ink2", color="aqua", size=9.3, h=0.34)
    text(s, 0.84, 1.20, 6.20, 0.22,
         "Exploring Agentic AI with IBM Granite & LangFlow",
         10.8, "aqua", True, margin=0)
    text(s, 0.78, 1.72, 6.75, 1.10, "SwachhAI", 54, "white", True, margin=0)
    text(s, 0.82, 2.98, 6.30, 0.84,
         "AI-guided waste segregation\nfor India’s households",
         26, "white", True, margin=0)
    text(s, 0.84, 4.05, 6.10, 0.78,
         "A proposed circularity assistant that helps people identify an item, act safely, and see a transparent impact estimate.",
         15.5, "grey", margin=0)
    line(s, 0.84, 5.14, 6.60, 5.14, "darkline", 1.0)
    text(s, 0.84, 5.39, 6.40, 0.28, "MOHAMMAD RAMISH ANSARI", 14, "white", True, margin=0)
    text(s, 0.84, 5.73, 6.40, 0.25,
         "B.Tech. Computer Science & Engineering  ·  University of Lucknow",
         11.5, "grey", margin=0)
    text(s, 0.84, 6.41, 6.20, 0.22,
         "1M1B AI for Sustainability  ·  1M1B / AICTE / IBM SkillsBuild",
         9.6, "aqua", True, margin=0)
    text(s, 0.84, 6.77, 3.2, 0.18, "04 NOVEMBER 2026", 8.5, "grey", True, margin=0)
    add_footer(s, 1, total, dark=True)

    # 2 — Project tile and presenter profile
    s = prs.slides.add_slide(blank)
    add_header(s, "Project tile", "Project tile & presenter",
               "A sustainability concept by a Computer Science student at the University of Lucknow")
    card(s, 0.66, 1.78, 5.74, 4.98, "white", "line")
    card(s, 6.62, 1.78, 6.04, 4.98, "white", "line")
    text(s, 0.95, 2.02, 4.9, 0.19, "PROJECT TITLE", 9, "green", True, margin=0)
    text(s, 0.95, 2.28, 5.02, 0.48, "SwachhAI", 28, "ink", True, margin=0)
    text(s, 0.96, 2.78, 4.98, 0.58,
         "AI-Guided Waste Segregation and Circularity Assistant",
         15, "ink2", True, margin=0)
    pill(s, 0.96, 3.45, 2.45, "ENVIRONMENT", "mint", "green", 9.5)
    pill(s, 3.53, 3.45, 2.38, "CIRCULAR ECONOMY", "soft2", "teal", 9.2)
    add_icon_badge(s, 0.98, 4.02, 0.79, "MA", "green", "white", 18)
    text(s, 1.95, 4.00, 3.95, 0.34, "Mohammad Ramish Ansari", 17, "ink", True, margin=0)
    text(s, 1.96, 4.38, 3.94, 0.25, "B.Tech. CSE  ·  University of Lucknow", 11.3, "slate", margin=0)
    text(s, 1.96, 4.68, 3.94, 0.22, "2024–2028  ·  Year 3, Semester V*", 10.6, "slate", margin=0)
    line(s, 0.96, 5.10, 5.95, 5.10, "line", 0.8)
    text(s, 0.98, 5.30, 0.64, 0.18, "EMAIL", 8.5, "green", True, margin=0)
    text(s, 1.70, 5.27, 4.10, 0.22, "ansariramish35@gmail.com", 11.2, "ink", margin=0)
    text(s, 0.98, 5.64, 0.64, 0.18, "MOBILE", 8.5, "green", True, margin=0)
    text(s, 1.70, 5.61, 4.10, 0.22, "+91 7007043871", 11.2, "ink", margin=0)
    text(s, 0.98, 6.10, 4.98, 0.44,
         "Project submitted 14 Sep 2026  ·  AI for Sustainability virtual internship",
         9.8, "slate", margin=0)

    text(s, 6.93, 2.02, 5.35, 0.20, "DOMAIN & PROGRAMME", 9, "green", True, margin=0)
    text(s, 6.93, 2.30, 5.30, 0.46,
         "Sustainability  ·  household waste  ·  Agentic AI",
         15, "ink", True, margin=0)
    text(s, 6.95, 2.79, 5.26, 0.58,
         "Built as a proposed solution for the 1M1B AI for Sustainability Virtual Internship, supported by AICTE and delivered in collaboration with IBM SkillsBuild.",
         12.2, "slate", margin=0)
    line(s, 6.94, 3.49, 12.30, 3.49, "line", 0.8)
    text(s, 6.94, 3.66, 5.30, 0.20, "EDUCATION", 9, "green", True, margin=0)
    text(s, 6.94, 3.93, 5.30, 0.65,
         "B.Tech. CSE  ·  University of Lucknow\nClass X & XII: First Division  ·  St. Francis School, Gomti Nagar",
         11.4, "ink", margin=0)
    line(s, 6.94, 4.63, 12.30, 4.63, "line", 0.8)
    text(s, 6.94, 4.80, 5.30, 0.20, "PROJECT INTENT", 9, "green", True, margin=0)
    text(s, 6.94, 5.08, 5.28, 0.62,
         "Make the correct action easier at the moment of disposal—without replacing local collection services or municipal rules.",
         12.8, "ink", True, margin=0)
    pill(s, 6.94, 5.96, 2.12, "DESIGN CONCEPT", "soft2", "teal", 9.1)
    pill(s, 9.20, 5.96, 2.93, "NOT A DEPLOYED PRODUCT", "soft2", "slate", 8.9)
    text(s, 6.95, 6.40, 5.22, 0.20,
         "*Year / semester follows the current AICTE résumé.",
         8.6, "slate", italic=True, margin=0)
    add_footer(s, 2, total)

    # 3 — Presenter snapshot from the supplied resumes
    s = prs.slides.add_slide(blank)
    add_header(s, "Presenter", "A technical foundation for applied AI",
               "Experience, skills and interests summarized from the supplied résumés")
    cols = [(0.66, 3.88), (4.73, 3.88), (8.80, 3.87)]
    for x, w in cols:
        card(s, x, 1.83, w, 3.76, "white", "line")
    # Experience card
    add_icon_badge(s, 0.93, 2.08, 0.48, "01", "green", "white", 10)
    text(s, 1.53, 2.14, 2.68, 0.25, "INTERNSHIP EXPERIENCE", 9.3, "green", True, margin=0)
    text(s, 0.96, 2.77, 3.25, 0.46, "Softpro India", 17, "ink", True, margin=0)
    text(s, 0.97, 3.23, 3.25, 0.76,
         "Python with Machine Learning & Data Science\n45 days  ·  Jun–Jul 2026  ·  A++ grade",
         11.2, "slate", margin=0)
    line(s, 0.96, 4.06, 4.22, 4.06, "line", 0.8)
    text(s, 0.97, 4.23, 3.25, 0.35, "1M1B · AI for Sustainability", 13.3, "ink", True, margin=0)
    text(s, 0.97, 4.63, 3.24, 0.70,
         "Exposure to AI/ML, LLMs, RAG, IBM Granite and Agentic AI through the virtual internship.",
         11.1, "slate", margin=0)
    # Skills card
    add_icon_badge(s, 5.00, 2.08, 0.48, "02", "teal", "white", 10)
    text(s, 5.60, 2.14, 2.72, 0.25, "TECHNICAL FOUNDATIONS", 9.3, "teal", True, margin=0)
    text(s, 5.02, 2.78, 3.20, 0.31, "Languages & tools", 14.3, "ink", True, margin=0)
    text(s, 5.02, 3.12, 3.20, 0.48, "C · Java · Python · SQL", 12.2, "ink2", True, margin=0)
    text(s, 5.02, 3.69, 3.22, 0.82,
         "ML · Data Science · NumPy · Pandas\nDSA · OOP · OS · relational databases / data handling",
         11.2, "slate", margin=0)
    pill(s, 5.02, 4.78, 1.40, "FOUNDATIONS", "soft2", "teal", 8.8)
    pill(s, 6.55, 4.78, 1.55, "ACADEMIC LEVEL", "soft2", "slate", 8.5)
    text(s, 5.02, 5.12, 3.20, 0.38,
         "Earlier CV: beginner C/Java programs in logic, control flow and OOP.",
         8.9, "slate", italic=True, margin=0)
    # Direction card
    add_icon_badge(s, 9.08, 2.08, 0.48, "03", "orange", "white", 10)
    text(s, 9.67, 2.14, 2.70, 0.25, "DIRECTION & STRENGTHS", 9.3, "orange", True, margin=0)
    text(s, 9.10, 2.78, 3.20, 0.33, "Career objective", 14.3, "ink", True, margin=0)
    text(s, 9.10, 3.13, 3.20, 0.60,
         "Build a professional career in Data Engineering.", 12.0, "ink2", margin=0)
    text(s, 9.10, 3.90, 3.20, 0.25, "Interests", 12.3, "ink", True, margin=0)
    text(s, 9.10, 4.20, 3.20, 0.53,
         "Data infrastructure · databases & optimization · large-scale data processing",
         10.7, "slate", margin=0)
    text(s, 9.10, 4.86, 3.20, 0.22, "Strengths", 12.3, "ink", True, margin=0)
    text(s, 9.10, 5.15, 3.20, 0.34,
         "Analytical · disciplined · patient · consistent\nProblem-solving · independent learning",
         10.2, "slate", margin=0)
    # Certifications strip
    card(s, 0.66, 5.83, 12.01, 0.91, "soft2", "line")
    text(s, 0.91, 6.02, 1.45, 0.20, "CERTIFICATIONS", 8.8, "green", True, margin=0)
    text(s, 2.38, 5.97, 9.96, 0.58,
         "IBM/Coursera: Python for Data Science, AI & Development  ·  Google/Coursera: Crash Course on Python  ·  Imperial College London/Coursera: Linear Algebra, Multivariate Calculus & PCA for ML  ·  AI for Sustainability",
         9.7, "ink", margin=0)
    add_footer(s, 3, total)

    # 4 — Problem statement
    s = prs.slides.add_slide(blank)
    add_header(s, "Problem statement", "At the bin, a few seconds decide what happens next", 
               "SwachhAI adapts AICTE-2026 Problem Statement No. 6: Eco Lifestyle Agent to household waste segregation")
    # National-scale evidence card
    card(s, 0.66, 1.83, 3.10, 3.75, "navy", "navy")
    text(s, 0.94, 2.08, 2.50, 0.20, "INDIA · CPCB 2020–21", 9.1, "aqua", True, margin=0)
    text(s, 0.94, 2.47, 2.55, 0.65, "160,039", 35, "white", True, margin=0)
    text(s, 0.97, 3.12, 2.42, 0.35, "tonnes of municipal solid waste generated per day", 11.1, "grey", margin=0)
    line(s, 0.95, 3.64, 3.45, 3.64, "darkline", 0.8)
    text(s, 0.95, 3.86, 2.55, 0.45, "152,750 t/day", 20, "lime", True, margin=0)
    text(s, 0.97, 4.33, 2.42, 0.40, "reported as collected", 10.6, "grey", margin=0)
    text(s, 0.96, 4.96, 2.45, 0.39, "National aggregate—not a current city estimate.", 9.2, "grey", italic=True, margin=0)

    # Five-second challenge
    card(s, 4.02, 1.83, 5.20, 3.75, "white", "line")
    text(s, 4.34, 2.09, 4.52, 0.26, "AT THE BIN, THE ITEM IS SPECIFIC", 9.2, "orange", True, margin=0)
    text(s, 4.34, 2.45, 4.50, 0.52,
         "A poster says ‘recycle’. A resident still has to know what to do with…",
         16, "ink", True, margin=0)
    # Three examples
    examples = [
        ("MILK POUCH", "Residue can contaminate dry recyclables.", "teal"),
        ("OLD BATTERY", "A separate, safer take-back route is needed.", "orange"),
        ("CHIPS PACKET", "A laminate may belong in reject, not clean plastics.", "slate"),
    ]
    y = 3.20
    for label, desc, col in examples:
        add_icon_badge(s, 4.35, y + 0.02, 0.30, "•", col, "white", 12)
        text(s, 4.78, y, 1.30, 0.23, label, 9.3, col, True, margin=0)
        text(s, 6.08, y - 0.01, 2.75, 0.43, desc, 10.6, "ink2", margin=0)
        y += 0.68
    # Why it matters card
    card(s, 9.48, 1.83, 3.18, 3.75, "mint", "mint")
    text(s, 9.80, 2.09, 2.55, 0.22, "WHY IT MATTERS", 9.2, "green", True, margin=0)
    bullet(s, 9.80, 2.50, 2.50, "Mixed waste contaminates recyclable streams.", 11.2, h=0.58)
    bullet(s, 9.80, 3.31, 2.50, "Unmarked hazards can put handlers at risk.", 11.2, dot="orange", h=0.58)
    bullet(s, 9.80, 4.12, 2.50, "Landfilled organics can generate methane.", 11.2, dot="teal", h=0.58)
    text(s, 9.80, 5.00, 2.45, 0.38,
         "A real-world problem with household-level action points.",
         9.6, "slate", italic=True, margin=0)

    card(s, 0.66, 5.83, 12.00, 0.83, "soft2", "line")
    text(s, 0.95, 6.02, 2.20, 0.21, "POLICY CONTEXT", 8.8, "green", True, margin=0)
    text(s, 3.12, 5.97, 9.10, 0.41,
         "Source segregation is a duty under India’s Solid Waste Management Rules, 2016. The Eco Lifestyle Agent problem statement calls for trusted, practical sustainability and local recycling guidance.",
         10.4, "ink", margin=0)
    text(s, 0.70, 6.73, 11.9, 0.17,
         "Sources: CPCB Annual Report 2020–21; Solid Waste Management Rules, 2016; supplied AICTE-2026 Problem Statements, No. 6.",
         8.0, "slate", italic=True, margin=0)
    add_footer(s, 4, total)

    # 5 — Target users / pain points / alternatives
    s = prs.slides.add_slide(blank)
    add_header(s, "Users & pain points", "Four stakeholders. One decision point.",
               "Target users, pain points and downstream beneficiaries shape the design")
    user_cards = [
        (0.66, 1.83, "HOUSEHOLD", "Urban household head / homemaker",
         "No time at the bin; item-specific rules are hard to remember.", "Per-item answer in ordinary language, in seconds.", "green"),
        (6.78, 1.83, "STUDENT / HOSTELLER", "Shared rooms and shared bins",
         "Limited storage; chargers, food cups and packaging are easy to mis-sort.", "Compact steps and campus-relevant quick picks.", "teal"),
        (0.66, 3.74, "SANITATION WORKER", "Formal and informal handlers",
         "Mixed bags can hide sharps, batteries and mercury-bearing lamps.", "Wrap / mark / separate instructions before handover.", "orange"),
        (6.78, 3.74, "WARD / LOCAL BODY", "Urban local-body operations",
         "Contaminated loads reduce recovery value; stream-level data may be limited.", "Cleaner inputs; aggregate analytics only in a later phase.", "blue"),
    ]
    for x, y, label, persona, pain, response, col in user_cards:
        card(s, x, y, 5.88, 1.68, "white", "line")
        pill(s, x + 0.22, y + 0.18, 1.82, label, fill="soft2", color=col, size=8.5, h=0.27)
        text(s, x + 0.23, y + 0.54, 5.34, 0.27, persona, 13.1, "ink", True, margin=0)
        text(s, x + 0.23, y + 0.87, 2.50, 0.75, pain, 10.5, "slate", margin=0)
        line(s, x + 2.96, y + 0.88, x + 2.96, y + 1.48, "line", 1.0)
        text(s, x + 3.16, y + 0.87, 2.42, 0.75, response, 10.5, "ink2", True, margin=0)
    card(s, 0.66, 5.75, 12.00, 0.93, "navy", "navy")
    text(s, 0.96, 5.95, 2.50, 0.20, "WHY CURRENT OPTIONS MISS", 9.0, "aqua", True, margin=0)
    text(s, 3.35, 5.91, 8.95, 0.53,
         "Posters and municipal pages can be accurate but often remain general, formal and slow to search. SwachhAI proposes an item-level interface with source citations, Hinglish/typo tolerance, and an honest refusal path.",
         10.4, "white", margin=0)
    add_footer(s, 5, total)

    # 6 — Solution overview
    s = prs.slides.add_slide(blank)
    add_header(s, "Solution overview", "Make the right bin the easy bin",
               "Three cooperating modules share one taxonomy, one request pipeline and one privacy contract")
    modules = [
        (0.66, "01", "WASTE CLASSIFIER", "Item → stream + confidence",
         "Maps an item description to one of eight streams. Returns a short protocol; below 75% confidence, it says ‘unknown’.", "IDENTIFY", "green"),
        (4.76, "02", "RULE ASSISTANT · RAG", "Question → cited guidance",
         "Retrieves public rules, composes only from evidence, lists sources, and refuses when support is weak.", "GROUND", "teal"),
        (8.86, "03", "IMPACT FORECASTER", "Habits → transparent estimate",
         "Uses household quantities and published factors to estimate 12-month diversion and CO₂e avoided.", "EXPLAIN", "orange"),
    ]
    for x, num, label, subtitle, desc, verb, col in modules:
        card(s, x, 1.90, 3.82, 3.55, "white", "line")
        add_icon_badge(s, x + 0.25, 2.18, 0.56, num, col, "white", 13)
        text(s, x + 0.96, 2.24, 2.55, 0.20, label, 9.3, col, True, margin=0)
        text(s, x + 0.27, 2.96, 3.28, 0.43, subtitle, 14, "ink", True, margin=0)
        text(s, x + 0.27, 3.52, 3.25, 1.06, desc, 11.4, "slate", margin=0)
        line(s, x + 0.27, 4.79, x + 3.50, 4.79, "line", 0.8)
        text(s, x + 0.28, 4.98, 3.10, 0.20, verb, 9.0, col, True, margin=0)
    card(s, 0.66, 5.78, 12.00, 0.87, "mint", "mint")
    text(s, 0.96, 5.97, 2.22, 0.20, "VALUE DELIVERED", 9.0, "green", True, margin=0)
    text(s, 3.10, 5.94, 9.20, 0.40,
         "Faster household decisions  ·  safer handover  ·  cleaner dry streams  ·  visible, auditable progress",
         12.0, "ink", True, margin=0)
    text(s, 0.70, 6.75, 11.9, 0.16,
         "Decision support only: SwachhAI does not collect waste, enforce rules or replace the local municipal body.",
         8.2, "slate", italic=True, margin=0)
    add_footer(s, 6, total)

    # 7 — Taxonomy
    s = prs.slides.add_slide(blank)
    add_header(s, "Design foundation", "Eight streams make household guidance actionable",
               "A practical collection taxonomy—not a complete materials-science classification")
    x0, y0, w, h, gx, gy = 0.66, 1.82, 2.88, 1.36, 0.20, 0.20
    for i, (name, examples_text, col) in enumerate(STREAMS):
        r, cidx = divmod(i, 4)
        x = x0 + cidx * (w + gx)
        y = y0 + r * (h + gy)
        card(s, x, y, w, h, "white", "line")
        add_icon_badge(s, x + 0.19, y + 0.22, 0.42, name[:1], col, "white", 11)
        text(s, x + 0.73, y + 0.20, 1.98, 0.26, name, 11.0, col, True, margin=0)
        text(s, x + 0.73, y + 0.55, 1.98, 0.50, examples_text, 10.6, "ink2", margin=0)
    text(s, 0.72, 5.10, 11.8, 0.22, "PREFERENCE ORDER: KEEP MATERIAL USEFUL BEFORE DISPOSAL", 8.7, "green", True, margin=0)
    # Waste hierarchy, shown as a progressive bar.
    hier = [
        ("1  PREVENT", "buy less · refill", "green"),
        ("2  REUSE", "repair · donate", "teal"),
        ("3  RECYCLE", "clean & dry", "blue"),
        ("4  RECOVER", "compost", "orange"),
        ("5  SAFE DISPOSAL", "reject / hazard", "slate"),
    ]
    hx, hy, hw, gap = 0.70, 5.48, 2.31, 0.10
    for i, (lbl, desc, col) in enumerate(hier):
        x = hx + i * (hw + gap)
        shape(s, x, hy, hw, 0.78, col)
        text(s, x + 0.13, hy + 0.13, hw - 0.25, 0.20, lbl, 8.8, "white", True, margin=0)
        text(s, x + 0.13, hy + 0.39, hw - 0.25, 0.25, desc, 9.6, "white", margin=0)
    text(s, 0.71, 6.45, 11.8, 0.29,
         "Concept knowledge base: about 95 items. The roadmap proposes expansion toward ~250 items using real pilot queries; local rules vary.",
         9.4, "slate", italic=True, margin=0)
    add_footer(s, 7, total)

    # 8 — Technology and LangFlow components
    s = prs.slides.add_slide(blank)
    add_header(s, "Technology plan", "IBM technology mapped to the solution",
               "Proposed component map for the Eco Lifestyle challenge; this presentation does not claim a deployed stack")
    card(s, 0.66, 1.82, 6.04, 4.93, "white", "line")
    text(s, 0.96, 2.06, 5.45, 0.22, "PROPOSED TECHNOLOGY STACK", 9.2, "green", True, margin=0)
    tech_rows = [
        ("IBM Granite", "Small instruction-tuned model for classification and constrained answers.", "green"),
        ("IBM Cloud Lite", "Proposed hosting / governance; watsonx.ai is not configured or deployed.", "teal"),
        ("LangFlow", "Proposed visual orchestration for routing inputs and tools.", "blue"),
        ("RAG knowledge layer", "Curated public rules; retrieve and cite passages; refuse if weak.", "orange"),
        ("Deterministic logic", "Alias cleanup, schema checks, confidence gate and arithmetic.", "slate"),
    ]
    yy = 2.43
    for name, desc, col in tech_rows:
        shape(s, 0.96, yy + 0.02, 0.08, 0.52, col, kind=MSO_SHAPE.RECTANGLE)
        text(s, 1.17, yy, 2.08, 0.23, name, 11.3, col, True, margin=0)
        text(s, 3.25, yy - 0.01, 3.10, 0.53, desc, 9.9, "ink2", margin=0)
        yy += 0.78
    card(s, 6.92, 1.82, 5.74, 4.93, "navy", "navy")
    text(s, 7.22, 2.06, 5.10, 0.22, "LANGFLOW NODE MAP · PROPOSED", 9.2, "aqua", True, margin=0)
    nodes = [
        ("01", "Chat Input", "typed query / item / review", "green"),
        ("02", "Normalize", "aliases · Hinglish · typos", "teal"),
        ("03", "Router", "classify / ask / estimate", "blue"),
        ("04", "File / Retriever", "public corpus · ranked passages", "orange"),
        ("05", "Granite Agent", "classify · answer · calculate", "amber"),
        ("06", "Guard & Format", "confidence · citations · safety", "lime"),
        ("07", "Chat Output", "action card + evidence", "aqua"),
    ]
    yy = 2.41
    for num, name, desc, col in nodes:
        add_icon_badge(s, 7.25, yy, 0.34, num, col, "navy", 8.0)
        text(s, 7.78, yy + 0.02, 1.78, 0.23, name, 10.5, "white", True, margin=0)
        text(s, 9.60, yy + 0.02, 2.63, 0.26, desc, 9.2, "grey", margin=0)
        if num != "07":
            add_arrow(s, 7.36, yy + 0.39, 0.12, 0.15, "darkline", "down")
        yy += 0.58
    text(s, 0.70, 6.81, 11.9, 0.16,
         "The project report describes a 20-document public corpus and TF–IDF-style demo retrieval; embeddings/vector store are a production option, not a deployed claim.",
         8.1, "slate", italic=True, margin=0)
    add_footer(s, 8, total)

    # 9 — Workflow
    s = prs.slides.add_slide(blank)
    add_header(s, "Workflow", "One request pipeline, three possible paths",
               "LangFlow-style orchestration shown as a conceptual flow—not an exported or running flow")
    # Top row: intake, normalization, router
    top = [
        (0.80, 1.98, 2.30, "USER INPUT", "‘Where does this go?’", "soft2", "ink"),
        (4.08, 1.98, 2.30, "NORMALIZE", "alias · language · clues", "mint", "green"),
        (7.36, 1.98, 2.30, "INTENT ROUTER", "classify / rule / impact", "soft2", "teal"),
    ]
    for x, y, w, label, detail, fill, col in top:
        card(s, x, y, w, 0.94, fill, "line")
        text(s, x + 0.18, y + 0.17, w - 0.36, 0.20, label, 9.1, col, True, margin=0)
        text(s, x + 0.18, y + 0.48, w - 0.36, 0.27, detail, 10.7, "ink", True, margin=0)
    add_arrow(s, 3.38, 2.31, 0.36, 0.23, "green")
    add_arrow(s, 6.66, 2.31, 0.36, 0.23, "green")
    # The intent router fans out to three interchangeable functions.
    text(s, 0.85, 3.18, 11.3, 0.22, "ROUTED TASK", 8.9, "slate", True, margin=0)
    line(s, 2.60, 3.34, 10.73, 3.34, "line", 1.0)
    line(s, 8.51, 3.02, 8.51, 3.34, "line", 1.0)
    branch_cards = [
        (0.78, "M1 · CLASSIFY", "One stream + confidence\nshort protocol", "green"),
        (4.84, "M2 · RETRIEVE + ANSWER", "Search public rules\nanswer with citations", "teal"),
        (8.90, "M3 · FORECAST", "Apply published factors\nshow assumptions", "orange"),
    ]
    branch_centres = [2.605, 6.665, 10.725]
    for (x, head, desc, col), cx in zip(branch_cards, branch_centres):
        line(s, cx, 3.34, cx, 3.54, col, 1.0)
        add_arrow(s, cx - 0.10, 3.42, 0.20, 0.16, col, "down")
        card(s, x, 3.57, 3.65, 1.30, "white", "line")
        pill(s, x + 0.22, 3.77, 2.65, head, "soft2", col, 8.5, 0.28)
        text(s, x + 0.23, 4.18, 3.15, 0.52, desc, 10.8, "ink2", True, margin=0)
    # Module outputs converge at one shared validation gate.
    gate_y = 5.22
    for cx, col in zip(branch_centres, ["green", "teal", "orange"]):
        line(s, cx, 4.87, cx, gate_y, col, 1.0)
    line(s, branch_centres[0], gate_y, branch_centres[-1], gate_y, "slate", 1.0)
    add_arrow(s, 6.56, gate_y, 0.22, 0.14, "slate", "down")
    card(s, 2.22, 5.43, 8.89, 0.57, "navy", "navy")
    text(s, 2.48, 5.60, 1.80, 0.19, "VALIDATE & GUARD", 8.9, "aqua", True, margin=0)
    text(s, 4.44, 5.60, 6.25, 0.19, "confidence  ·  evidence  ·  hazard safety  →  render action card", 9.6, "white", True, margin=0)
    text(s, 0.82, 6.42, 11.4, 0.24,
         "A failed confidence / retrieval check does not guess: it returns ‘unknown’ or an explicit refusal and points to local guidance.",
         9.3, "slate", italic=True, margin=0)
    add_footer(s, 9, total)

    # 10 — Architecture
    s = prs.slides.add_slide(blank)
    add_header(s, "Architecture blueprint", "Layered architecture. Clear safety boundaries.", 
               "Conceptual responsibilities and data flow; deployment choices are not fixed")
    layers = [
        (1.77, 0.58, "PRESENTATION", "Household resident  ·  student / hosteller  ·  accessible text interface", "mint", "green"),
        (2.47, 0.63, "ORCHESTRATION", "Normalize → extract → route → compose → validate → render", "soft2", "teal"),
        (3.21, 1.08, "THREE MODULES", "M1  Waste classifier + confidence gate       M2  RAG rule assistant + citations       M3  Impact calculator", "white", "orange"),
        (4.42, 0.72, "KNOWLEDGE & MODEL", "~95-item taxonomy  ·  public rule corpus  ·  Granite-class model  ·  published coefficients", "soft2", "blue"),
        (5.28, 0.78, "DATA & GOVERNANCE", "Client-side by default  ·  no names/addresses  ·  human-reviewed corpus  ·  aggregate-only later", "navy", "aqua"),
    ]
    for y, h, label, desc, fill, col in layers:
        card(s, 0.72, y, 11.88, h, fill, "line" if fill != "navy" else "navy")
        text(s, 0.98, y + 0.14, 2.10, 0.20, label, 9.0, col, True, margin=0)
        text(s, 3.14, y + 0.11, 9.05, h - 0.18, desc,
             11.1 if h > 0.7 else 10.6, "white" if fill == "navy" else "ink", True, margin=0)
    # Vertical connectors between layers.
    for yy in [2.36, 3.11, 4.32, 5.20]:
        add_arrow(s, 6.41, yy, 0.25, 0.16, "green", "down")
    card(s, 0.72, 6.23, 11.88, 0.49, "mint", "mint")
    text(s, 0.98, 6.36, 11.35, 0.20,
         "No autonomous action on the world: no collection order, household monitoring, enforcement or worker scoring.",
         9.8, "green", True, margin=0)
    add_footer(s, 10, total)

    # 11 — Simulation and token usage
    s = prs.slides.add_slide(blank)
    add_header(s, "Demo / simulation", "A quick item query becomes a safe action card",
               "Worked interaction from the project narrative; shown as a simulation, not a live app screen")
    card(s, 0.66, 1.83, 8.08, 4.91, "white", "line")
    text(s, 0.98, 2.07, 7.30, 0.20, "SIMULATED INTERACTION", 9.2, "green", True, margin=0)
    # User input strip
    card(s, 0.98, 2.42, 7.39, 0.73, "soft2", "soft2")
    add_icon_badge(s, 1.18, 2.59, 0.34, "U", "teal", "white", 10)
    text(s, 1.70, 2.49, 6.25, 0.18, "USER ASKS", 8.6, "teal", True, margin=0)
    text(s, 1.70, 2.73, 6.22, 0.26, "“doodh ka packet”", 15.0, "ink", True, margin=0)
    # Normalized step
    text(s, 1.03, 3.38, 1.30, 0.19, "NORMALIZE", 8.5, "slate", True, margin=0)
    text(s, 2.48, 3.34, 5.60, 0.28,
         "milk pouch  ·  LDPE film  ·  residue / liquid contact",
         11.1, "ink2", margin=0)
    add_arrow(s, 4.52, 3.72, 0.22, 0.24, "green", "down")
    # Output card
    card(s, 0.98, 4.04, 7.39, 2.16, "mint", "mint")
    pill(s, 1.20, 4.25, 1.13, "DRY", "green", "white", 10.8, 0.32)
    text(s, 2.55, 4.25, 2.45, 0.21, "Confidence field shown", 10.0, "green", True, margin=0)
    text(s, 5.63, 4.25, 2.38, 0.21, "Illustrative: 92%*", 9.0, "slate", True,
         align=PP_ALIGN.RIGHT, margin=0)
    line(s, 1.20, 4.72, 8.12, 4.72, "line", 0.8)
    bullet(s, 1.22, 4.91, 6.56, "Cut fully open and rinse; sun-dry to prevent residue and odour.", 10.7, dot="teal", h=0.38)
    bullet(s, 1.22, 5.37, 6.56, "Bundle and hand over with dry waste or to a local kabadiwala.", 10.7, dot="green", h=0.38)
    text(s, 1.23, 5.83, 6.60, 0.19,
         "If confidence is below 75, return ‘unknown’ and offer the rule assistant instead of guessing.",
         9.2, "ink2", True, margin=0)
    # Token status panel
    card(s, 9.02, 1.83, 3.64, 4.91, "navy", "navy")
    text(s, 9.31, 2.09, 3.03, 0.20, "TOKEN USAGE / RUNTIME EVIDENCE", 8.5, "aqua", True, margin=0)
    text(s, 9.30, 2.51, 3.00, 0.63, "No token count\nwas supplied", 18.0, "white", True, margin=0)
    line(s, 9.31, 3.30, 12.33, 3.30, "darkline", 0.9)
    bullet(s, 9.32, 3.54, 2.89, "No live LangFlow or Granite session is documented.", 10.2, "white", "lime", 0.62)
    bullet(s, 9.32, 4.43, 2.89, "No deployed app or working URL is supplied.", 10.2, "white", "aqua", 0.62)
    text(s, 9.32, 5.40, 2.88, 0.72,
         "Simulation demonstrates intended user experience only—not runtime, accuracy or field results.",
         10.1, "grey", italic=True, margin=0)
    text(s, 0.70, 6.80, 11.9, 0.16,
         "*The project report includes this illustrative example; it is not an independently verified accuracy measurement.",
         8.1, "slate", italic=True, margin=0)
    add_footer(s, 11, total)

    # 12 — Role of Agentic AI and responsible use
    s = prs.slides.add_slide(blank)
    add_header(s, "Agentic AI & responsibility", "Agentic does not mean unchecked autonomy",
               "The system automates a narrow information task and keeps consequential decisions under human control")
    card(s, 0.66, 1.83, 5.42, 4.86, "navy", "navy")
    text(s, 0.97, 2.08, 4.75, 0.20, "NARROW AGENT LOOP", 9.1, "aqua", True, margin=0)
    loop = [
        (1.00, 2.55, "PERCEIVE", "resident input", "green"),
        (3.33, 2.55, "DECIDE", "route to a module", "teal"),
        (1.00, 3.66, "ACT", "retrieve / classify / calculate", "orange"),
        (3.33, 3.66, "VALIDATE", "check evidence & safety", "lime"),
    ]
    for x, y, lbl, desc, col in loop:
        card(s, x, y, 2.05, 0.82, "ink2", "darkline")
        pill(s, x + 0.13, y + 0.12, 1.55, lbl, col, "navy", 8.5, 0.24)
        text(s, x + 0.14, y + 0.47, 1.78, 0.24, desc, 9.3, "white", margin=0)
    add_arrow(s, 3.05, 2.83, 0.20, 0.22, "aqua")
    add_arrow(s, 4.17, 3.43, 0.22, 0.22, "aqua", "down")
    add_arrow(s, 3.04, 3.95, 0.20, 0.22, "aqua", "left")
    add_arrow(s, 1.92, 3.43, 0.22, 0.22, "aqua", "up")
    text(s, 1.00, 4.76, 4.72, 0.82,
         "It can return advice and log an anonymised pattern. It cannot contact a recycler, order collection, enforce a rule or change its own knowledge base.",
         11.1, "white", margin=0)
    pill(s, 1.00, 5.73, 4.40, "HUMAN REVIEW FOR CORPUS / TAXONOMY CHANGES", "ink2", "lime", 8.2, 0.30)

    # Five observable guardrails on right
    card(s, 6.38, 1.83, 6.28, 4.86, "white", "line")
    text(s, 6.70, 2.08, 5.54, 0.20, "RESPONSIBLE-AI BEHAVIOURS", 9.1, "green", True, margin=0)
    guards = [
        ("TRANSPARENCY", "Show confidence, assumptions and source citations.", "green"),
        ("FAIRNESS", "Accept Hinglish, transliteration and misspellings; avoid income-coded assumptions.", "teal"),
        ("PRIVACY", "No account, names, addresses or uploaded item photos in the proposed design.", "blue"),
        ("SAFETY", "Hazard protocols start with safe wrapping / marking / separate handover.", "orange"),
        ("OVERSIGHT", "Local bylaws take precedence; people review corpus and taxonomy updates.", "slate"),
    ]
    yy = 2.47
    for label, desc, col in guards:
        add_icon_badge(s, 6.72, yy, 0.32, "✓", col, "white", 11)
        text(s, 7.18, yy + 0.01, 1.43, 0.21, label, 8.7, col, True, margin=0)
        text(s, 8.69, yy - 0.01, 3.58, 0.60, desc, 9.9, "ink2", margin=0)
        yy += 0.76
    text(s, 6.72, 6.31, 5.55, 0.22,
         "Human safety outranks recycling purity—always.",
         10.3, "green", True, margin=0)
    add_footer(s, 12, total)

    # 13 — Impact model example
    s = prs.slides.add_slide(blank)
    add_header(s, "Impact model", "Make the estimate visible—and checkable",
               "A worked household example using the project’s disclosed assumptions")
    card(s, 0.66, 1.84, 3.25, 4.82, "white", "line")
    text(s, 0.96, 2.10, 2.62, 0.21, "HOUSEHOLD INPUTS", 9.1, "green", True, margin=0)
    text(s, 0.96, 2.52, 2.60, 0.40, "Family of four", 16, "ink", True, margin=0)
    bullet(s, 0.97, 3.12, 2.55, "13 kg household waste per week", 10.7, h=0.46)
    bullet(s, 0.97, 3.74, 2.55, "About 30% currently segregated", 10.7, dot="teal", h=0.46)
    bullet(s, 0.97, 4.36, 2.55, "No home composting at baseline", 10.7, dot="orange", h=0.46)
    line(s, 0.96, 5.03, 3.57, 5.03, "line", 0.8)
    text(s, 0.97, 5.24, 2.55, 0.93,
         "Adopts home composting, daily dry separation and a take-back point.",
         11.0, "ink2", True, margin=0)
    # Formula card
    card(s, 4.17, 1.84, 3.54, 4.82, "soft2", "line")
    text(s, 4.48, 2.10, 2.91, 0.21, "TRANSPARENT CALCULATION", 9.0, "teal", True, margin=0)
    text(s, 4.48, 2.57, 2.91, 0.48, "55% organic\n25% dry · 20% reject", 14, "ink", True, margin=0)
    text(s, 4.48, 3.40, 2.90, 0.30, "Organic composted × 0.47", 11.0, "green", True, margin=0)
    text(s, 4.48, 3.71, 2.90, 0.23, "kg CO₂e avoided / kg", 9.1, "slate", margin=0)
    text(s, 4.48, 4.16, 2.90, 0.30, "Dry recycled × 1.1", 11.0, "teal", True, margin=0)
    text(s, 4.48, 4.48, 2.90, 0.23, "kg CO₂e avoided / kg", 9.1, "slate", margin=0)
    line(s, 4.48, 4.93, 7.37, 4.93, "line", 0.8)
    text(s, 4.48, 5.15, 2.88, 0.91,
         "Annual waste = 13 × 52 = 676 kg. Coefficients are directional, published factors—not measured project results.",
         9.7, "ink2", margin=0)
    # Outputs
    card(s, 7.97, 1.84, 4.69, 4.82, "navy", "navy")
    pill(s, 8.28, 2.10, 1.57, "MODELLED ONLY", "ink2", "lime", 8.8)
    text(s, 8.29, 2.58, 3.94, 0.20, "POTENTIAL NEW DIVERSION", 8.8, "aqua", True, margin=0)
    text(s, 8.27, 2.88, 3.96, 0.56, "≈435 kg / year", 26, "white", True, margin=0)
    line(s, 8.28, 3.58, 12.30, 3.58, "darkline", 0.8)
    text(s, 8.29, 3.83, 3.96, 0.20, "DIRECTIONAL CO₂e AVOIDED", 8.8, "aqua", True, margin=0)
    text(s, 8.27, 4.12, 3.96, 0.53, "≈245 kg / year", 24, "white", True, margin=0)
    text(s, 8.29, 4.85, 3.96, 0.22, "≈12 tree-years  ·  ≈1,275 km petrol driving", 9.8, "lime", True, margin=0)
    text(s, 8.29, 5.42, 3.96, 0.72,
         "Illustrative equivalents only. Actual local waste composition and collection routes vary.",
         9.6, "grey", italic=True, margin=0)
    text(s, 0.70, 6.80, 11.9, 0.16,
         "Report notes that a project document also quotes ≈268 kg CO₂e under slightly different assumptions; neither value is a measured offset.",
         8.0, "slate", italic=True, margin=0)
    add_footer(s, 13, total)

    # 14 — SDGs and evaluation plan
    s = prs.slides.add_slide(blank)
    add_header(s, "Impact & evaluation", "Contribution is a hypothesis; measurement comes next",
               "SDG mapping and pilot metrics are proposed—not reported results")
    sdgs = [
        (0.66, "12", "RESPONSIBLE CONSUMPTION", "Target 12.5", "Primary", "Prevention, reuse and recycling at the point waste is generated.", "green"),
        (4.76, "11", "SUSTAINABLE CITIES", "Target 11.6", "Secondary", "Cleaner separated streams support better municipal waste management.", "teal"),
        (8.86, "13", "CLIMATE ACTION", "Target 13.3", "Secondary", "Explain mitigation through understandable, transparent estimates.", "blue"),
    ]
    for x, num, label, target, role, desc, col in sdgs:
        card(s, x, 1.86, 3.82, 1.70, "white", "line")
        add_icon_badge(s, x + 0.22, 2.11, 0.58, num, col, "white", 17)
        text(s, x + 0.94, 2.12, 2.56, 0.18, label, 8.3, col, True, margin=0)
        text(s, x + 0.94, 2.38, 2.56, 0.22, f"{target}  ·  {role}", 10.0, "ink", True, margin=0)
        text(s, x + 0.23, 2.79, 3.33, 0.53, desc, 9.5, "slate", margin=0)
    card(s, 0.66, 3.86, 12.00, 2.80, "navy", "navy")
    text(s, 0.98, 4.12, 4.10, 0.22, "HOW A PILOT WOULD BE EVALUATED", 9.2, "aqua", True, margin=0)
    measures = [
        ("Correct-sort rate", "waste audits"),
        ("Dry-stream purity", "MRF checks"),
        ("Weekly active use", "adoption"),
        ("Handler incidents", "per 1,000 shifts"),
    ]
    x = 0.98
    for name, detail in measures:
        card(s, x, 4.60, 2.70, 0.92, "ink2", "darkline")
        text(s, x + 0.15, 4.77, 2.41, 0.25, name, 10.5, "white", True, margin=0)
        text(s, x + 0.15, 5.10, 2.41, 0.20, detail, 9.1, "grey", margin=0)
        x += 2.87
    text(s, 0.99, 5.81, 11.30, 0.68,
         "No pilot, accuracy study, field deployment, user feedback or measured diversion is claimed; results need independent audit. SDG 8 (safer work) and SDG 3 (reduced exposure) are indirect potential benefits, not delivered outcomes.",
         9.8, "white", True, margin=0)
    add_footer(s, 14, total)

    # 15 — Novelty and rubric mapping
    s = prs.slides.add_slide(blank)
    add_header(s, "Novelty & fit", "More than a generic sustainability chatbot",
               "Design decisions are mapped to the four project-judging dimensions")
    card(s, 0.66, 1.83, 5.42, 4.91, "white", "line")
    text(s, 0.97, 2.08, 4.75, 0.20, "WHAT IS DISTINCTIVE", 9.2, "green", True, margin=0)
    diffs = [
        "Item-level answer at the point of disposal—not a general eco tip.",
        "One of eight streams, with a visible confidence and an ‘unknown’ route.",
        "Public-rule answers include citations or a clear refusal.",
        "Safety instructions are written for the handler as well as the resident.",
        "Impact uses inspectable arithmetic instead of a black-box score.",
    ]
    yy = 2.48
    for i, d in enumerate(diffs, 1):
        add_icon_badge(s, 0.98, yy, 0.32, str(i), "green" if i < 4 else "teal", "white", 9)
        text(s, 1.47, yy - 0.01, 4.16, 0.50, d, 10.7, "ink2", margin=0)
        yy += 0.75
    card(s, 6.38, 1.83, 6.28, 4.91, "soft2", "line")
    text(s, 6.70, 2.08, 5.56, 0.20, "PROJECT GUIDELINE RUBRIC · 5 POINTS EACH", 9.1, "teal", True, margin=0)
    rubric = [
        ("COMPLETENESS & FEASIBILITY", "Three defined modules; explicit assumptions and measurement gates.", "green"),
        ("CREATIVITY & INNOVATION", "Combines item classification, grounded rules and impact arithmetic.", "teal"),
        ("DESIGN & USABILITY", "Short action cards; Hinglish/typo tolerance; one-hand, at-the-bin use.", "blue"),
        ("EFFECTIVENESS & EFFICIENCY", "Targets household segregation; impact and adoption metrics are specified.", "orange"),
    ]
    yy = 2.50
    for label, desc, col in rubric:
        card(s, 6.71, yy, 5.61, 0.80, "white", "line")
        text(s, 6.91, yy + 0.12, 2.24, 0.18, label, 8.0, col, True, margin=0)
        text(s, 9.18, yy + 0.11, 2.90, 0.52, desc, 9.2, "ink2", margin=0)
        yy += 0.91
    text(s, 6.72, 6.31, 5.50, 0.22,
         "Alignment only—not a self-awarded score or a claim of tested effectiveness.",
         9.1, "slate", italic=True, margin=0)
    add_footer(s, 15, total)

    # 16 — Future scope / roadmap
    s = prs.slides.add_slide(blank)
    add_header(s, "Future scope", "A phased roadmap earns scale with field evidence",
               "Proposals in the report—not commitments or completed work")
    phases = [
        (0.66, "PHASE 1", "CAMPUS PILOT", "0–3 months", "• ~500 students / 2 hostels\n• one-week baseline waste audit\n• expand taxonomy ~95 → ~250 items", "Gate: target ≥60% weekly active; measure mixed-waste reduction", "green"),
        (4.76, "PHASE 2", "WARD PARTNERSHIP", "3–9 months", "• align with local collection routes\n• multilingual voice, calendar & nudges\n• verify dry-stream purity at MRF", "Gate: ward and MRF evidence", "teal"),
        (8.86, "PHASE 3", "AGGREGATE DATA LAYER", "9–18 months", "• anonymised dashboard / housing API\n• recycler / take-back integration\n• quarterly audited diversion", "Gate: verifiable tonnes diverted", "blue"),
    ]
    for x, tag, title_text, months, body, gate, col in phases:
        card(s, x, 1.91, 3.82, 3.98, "white", "line")
        pill(s, x + 0.24, 2.15, 1.20, tag, "soft2", col, 8.5, 0.28)
        text(s, x + 0.24, 2.58, 3.32, 0.26, title_text, 12.5, "ink", True, margin=0)
        text(s, x + 0.24, 2.95, 3.26, 0.22, months, 10.2, col, True, margin=0)
        text(s, x + 0.24, 3.35, 3.30, 1.31, body, 10.4, "ink2", margin=0)
        line(s, x + 0.24, 4.91, x + 3.54, 4.91, "line", 0.8)
        text(s, x + 0.24, 5.11, 3.30, 0.62, gate, 9.4, col, True, margin=0)
    card(s, 0.66, 6.10, 12.00, 0.56, "mint", "mint")
    text(s, 0.94, 6.28, 11.34, 0.20,
         "Later: image input only after accuracy testing; local voice and city rules need review. No household ranking.",
         9.1, "green", True, margin=0)
    add_footer(s, 16, total)

    # 17 — Status, GitHub, sources and date reconciliation
    s = prs.slides.add_slide(blank)
    add_header(s, "Evidence & submission", "What is included—and what is not claimed",
               "The presentation is complete as a design submission; missing runtime evidence is stated openly")
    card(s, 0.66, 1.83, 5.50, 4.93, "navy", "navy")
    text(s, 0.98, 2.09, 4.82, 0.20, "PROJECT STATUS", 9.1, "aqua", True, margin=0)
    status_rows = [
        ("INCLUDED", "Problem framing, users, solution, architecture and a labelled simulation.", "lime"),
        ("NOT DEPLOYED", "No working app, model training, field test or accuracy result is claimed.", "aqua"),
        ("NO TOKEN LOG", "No Granite / LangFlow runtime token count or run screenshot was supplied.", "amber"),
        ("GITHUB LINK", "No public repository, app.json or deployed URL was supplied.", "orange"),
    ]
    yy = 2.51
    for label, desc, col in status_rows:
        pill(s, 0.99, yy, 1.24, label, "ink2", col, 7.8, 0.26)
        text(s, 2.40, yy - 0.01, 3.24, 0.50, desc, 9.7, "white", margin=0)
        yy += 0.83
    text(s, 0.99, 5.96, 4.79, 0.48,
         "Repository URL is intentionally omitted rather than invented; a public repo can be added if code is supplied.",
         9.5, "grey", italic=True, margin=0)

    card(s, 6.46, 1.83, 6.20, 4.93, "white", "line")
    text(s, 6.78, 2.09, 5.52, 0.20, "SOURCE BASIS", 9.1, "green", True, margin=0)
    bullet(s, 6.80, 2.49, 5.46, "AICTE-2026 Problem Statements — closest match: No. 6, Eco Lifestyle Agent.", 10.2, h=0.54)
    bullet(s, 6.80, 3.15, 5.46, "Project Guidelines and Template — required sections and judging rubric.", 10.2, dot="teal", h=0.48)
    bullet(s, 6.80, 3.77, 5.46, "SwachhAI internship report — project design, examples, estimates, limits and references.", 10.2, dot="orange", h=0.54)
    bullet(s, 6.80, 4.44, 5.46, "CPCB 2020–21; SWM Rules 2016; Battery / E-Waste Rules 2022; UN SDGs; IBM Granite / RAG references.", 10.0, dot="blue", h=0.56)
    line(s, 6.80, 5.18, 12.28, 5.18, "line", 0.8)
    text(s, 6.81, 5.39, 5.44, 0.90,
         "Date note: the current AICTE résumé lists Jul–Aug 2026; the internship completion certificate records July–September 2026 and was issued 22 Sep 2026. Project submission: 14 Sep 2026. The deck follows the certificate for the certified period.",
         9.3, "ink2", margin=0)
    add_footer(s, 17, total)

    # 18 — Selected references and source files
    s = prs.slides.add_slide(blank)
    add_header(s, "References", "Selected sources behind the project claims",
               "Clickable public references are included; the complete project bibliography appears in the internship report")
    refs_left = [
        ("CPCB · Annual Report 2020–21", "National municipal solid-waste figures cited on slide 4.",
         "https://cpcb.nic.in/uploads/MSW/MSW_AnnualReport_2020-21.pdf", "cpcb.nic.in/.../MSW_AnnualReport_2020-21.pdf"),
        ("MoEFCC · Solid Waste Management Rules, 2016", "Source-segregation obligations and local-body context.",
         "https://cpcb.nic.in/uploads/MSW/SWM_2016.pdf", "cpcb.nic.in/.../SWM_2016.pdf"),
        ("MoEFCC / PIB · Battery Waste Rules, 2022", "Battery collection and take-back context.",
         "https://www.pib.gov.in/PressReleasePage.aspx?PRID=1854433", "pib.gov.in · PRID 1854433"),
        ("MoEFCC / CPCB · E-Waste Rules, 2022", "Authorised route for electronic waste.",
         "https://cpcb.nic.in/uploads/Projects/E-Waste/e-waste_rules_2022.pdf", "cpcb.nic.in/.../e-waste_rules_2022.pdf"),
    ]
    refs_right = [
        ("United Nations · 2030 Agenda / SDGs", "Targets 11.6, 12.5 and 13.3.",
         "https://sdgs.un.org/2030agenda", "sdgs.un.org/2030agenda"),
        ("IBM · Granite 3.0 overview", "IBM Granite model-family background.",
         "https://www.ibm.com/new/announcements/ibm-granite-3-0-open-state-of-the-art-enterprise-models", "ibm.com · Granite 3.0"),
        ("Lewis et al. · Retrieval-Augmented Generation (2020)", "Grounding pattern referenced in the technical report.",
         "https://arxiv.org/abs/2005.11401", "arxiv.org/abs/2005.11401"),
        ("Supplied project source set", "AICTE PS #6 · Guidelines · Template · CVs · project report.",
         None, "Source documents supplied for this presentation"),
    ]
    for col_x, items in [(0.66, refs_left), (6.78, refs_right)]:
        for i, (title_text, desc, url, display_url) in enumerate(items):
            y = 1.83 + i * 1.16
            card(s, col_x, y, 5.88, 1.00, "white", "line")
            text(s, col_x + 0.22, y + 0.13, 5.40, 0.22, title_text, 10.9, "ink", True, margin=0)
            text(s, col_x + 0.22, y + 0.40, 5.40, 0.22, desc, 9.2, "slate", margin=0)
            if url:
                rich_text(s, col_x + 0.22, y + 0.68, 5.40, 0.18,
                          [(display_url, False, "teal", False, url)], size=8.9, color="teal", margin=0)
            else:
                text(s, col_x + 0.22, y + 0.68, 5.40, 0.18, display_url, 8.9, "green", True, margin=0)
    card(s, 0.66, 6.55, 12.00, 0.36, "mint", "mint")
    text(s, 0.90, 6.64, 11.48, 0.18,
         "Project-specific technical details and limitations are cited to the supplied SwachhAI internship report; links open in a browser.",
         8.8, "green", True, margin=0)
    add_footer(s, 18, total)

    # 19 — 1M1B internship completion certificate
    s = prs.slides.add_slide(blank)
    add_header(s, "Certificate", "AI for Sustainability Virtual Internship",
               "Completion certificate · 1M1B, supported by AICTE, in collaboration with IBM SkillsBuild")
    card(s, 0.66, 1.83, 3.48, 4.98, "white", "line")
    text(s, 0.96, 2.12, 2.88, 0.22, "INTERNSHIP COMPLETION", 9.0, "green", True, margin=0)
    text(s, 0.96, 2.60, 2.85, 0.78, "1M1B\nAI for Sustainability", 18, "ink", True, margin=0)
    line(s, 0.96, 3.58, 3.78, 3.58, "line", 0.8)
    text(s, 0.96, 3.82, 2.86, 0.25, "Mohammad Ramish Ansari", 12.2, "ink", True, margin=0)
    text(s, 0.96, 4.22, 2.86, 0.80,
         "Certified period: July–September 2026\nIssued: 22 September 2026",
         10.5, "slate", margin=0)
    text(s, 0.96, 5.24, 2.88, 0.76,
         "AICTE Internship ID\nINTERNSHIP_17828984086a44dee80acf6",
         9.2, "ink2", True, margin=0)
    card(s, 4.40, 1.83, 8.26, 4.98, "white", "line")
    contain_picture(s, CERT_DIR / "cert_main.png", 4.58, 2.00, 7.90, 4.64)
    add_footer(s, 19, total)

    # 20 — IBM Getting Started certificate
    s = prs.slides.add_slide(blank)
    add_header(s, "Certificate", "Getting Started with Artificial Intelligence",
               "IBM SkillsBuild · issued 04 November 2026 · Credly verification included on certificate")
    card(s, 0.66, 1.83, 3.48, 4.98, "white", "line")
    text(s, 0.96, 2.13, 2.86, 0.22, "IBM SKILLSBUILD", 9.0, "teal", True, margin=0)
    text(s, 0.96, 2.57, 2.87, 0.92, "Getting Started\nwith Artificial Intelligence", 19.0, "ink", True, margin=0)
    line(s, 0.96, 3.63, 3.78, 3.63, "line", 0.8)
    text(s, 0.96, 3.88, 2.86, 0.25, "Mohammad Ramish Ansari", 12.0, "ink", True, margin=0)
    text(s, 0.96, 4.26, 2.86, 0.52, "Issued 04 Nov 2026", 10.8, "slate", margin=0)
    link = "https://www.credly.com/badges/2432d2be-6ecf-4e66-903e-bef52cecaaa1"
    rich_text(s, 0.96, 4.94, 2.85, 0.56,
              [("Verify on Credly", True, "green", False, link)], size=10.3, color="green")
    text(s, 0.96, 5.70, 2.86, 0.60,
         "The certificate QR code and credential record are visible in the scan.",
         9.6, "slate", italic=True, margin=0)
    card(s, 4.40, 1.83, 8.26, 4.98, "white", "line")
    contain_picture(s, CERT_DIR / "cert_ibm_getting_started.png", 4.58, 2.00, 7.90, 4.64)
    add_footer(s, 20, total)

    # 21 — IBM Bob certificate
    s = prs.slides.add_slide(blank)
    add_header(s, "Certificate", "Troubleshoot Your Code Using IBM Bob",
               "IBM SkillsBuild completion certificate · 30 minutes")
    card(s, 0.66, 1.83, 3.48, 4.98, "white", "line")
    text(s, 0.96, 2.13, 2.86, 0.22, "IBM SKILLSBUILD", 9.0, "teal", True, margin=0)
    text(s, 0.96, 2.59, 2.88, 0.88, "Troubleshoot Your Code\nUsing IBM Bob", 18.8, "ink", True, margin=0)
    line(s, 0.96, 3.61, 3.78, 3.61, "line", 0.8)
    text(s, 0.96, 3.85, 2.86, 0.25, "Mohammad Ramish Ansari", 12.0, "ink", True, margin=0)
    text(s, 0.96, 4.23, 2.86, 0.54,
         "Completion: 04 Nov 2026 (GMT)\nLearning time: 30 minutes",
         10.1, "slate", margin=0)
    text(s, 0.96, 4.98, 2.86, 0.68,
         "Course ID\nALM-COURSE_4071307",
         9.8, "ink2", True, margin=0)
    text(s, 0.96, 5.88, 2.84, 0.42,
         "Certificate reproduced from the supplied PDF.",
         9.0, "slate", italic=True, margin=0)
    card(s, 4.40, 1.83, 8.26, 4.98, "white", "line")
    contain_picture(s, CERT_DIR / "cert_ibm_bob.png", 4.58, 2.00, 7.90, 4.64)
    add_footer(s, 21, total)

    # 22 — Thank you
    s = prs.slides.add_slide(blank)
    add_bg(s, "navy")
    # Decorative rings are intentionally subtle and behind the content.
    for x, y, d, col in [(8.85, 0.95, 3.72, "darkline"), (9.63, 1.73, 2.16, "green"),
                         (10.22, 2.31, 0.98, "teal")]:
        ring = shape(s, x, y, d, d, "navy", line=col, kind=MSO_SHAPE.OVAL)
        ring.fill.transparency = 100
        ring.line.width = Pt(2.0)
    shape(s, 10.30, 2.39, 0.82, 0.82, "lime", kind=MSO_SHAPE.OVAL)
    text(s, 10.31, 2.56, 0.80, 0.29, "✓", 22, "navy", True,
         align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin=0)
    pill(s, 0.82, 0.75, 1.60, "THANK YOU", "ink2", "aqua", 9.5, 0.34)
    text(s, 0.82, 1.73, 6.90, 1.24, "Make the right bin\nthe easy bin.", 34, "white", True, margin=0)
    text(s, 0.84, 3.78, 6.55, 0.42,
         "SwachhAI  ·  AI-Guided Waste Segregation and Circularity Assistant",
         14.3, "grey", margin=0)
    line(s, 0.84, 4.49, 6.75, 4.49, "darkline", 1.0)
    text(s, 0.84, 4.79, 5.8, 0.27, "MOHAMMAD RAMISH ANSARI", 14, "white", True, margin=0)
    text(s, 0.84, 5.18, 5.8, 0.25, "B.Tech. CSE  ·  University of Lucknow", 11.2, "grey", margin=0)
    text(s, 0.84, 5.65, 5.8, 0.23, "ansariramish35@gmail.com", 10.6, "aqua", margin=0)
    text(s, 0.84, 5.98, 5.8, 0.23, "+91 7007043871", 10.6, "aqua", margin=0)
    text(s, 0.84, 6.53, 6.4, 0.25, "QUESTIONS?", 10.2, "lime", True, margin=0)
    add_footer(s, 22, total, dark=True)

    # Check all image assets before saving.
    required = [
        CERT_DIR / "cert_main.png",
        CERT_DIR / "cert_ibm_getting_started.png",
        CERT_DIR / "cert_ibm_bob.png",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing certificate images: " + ", ".join(missing))

    prs.save(OUT)
    print(f"Wrote {OUT}")
    print(f"Slides: {len(prs.slides)} | Size: {OUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    build_deck()
