# -*- coding: utf-8 -*-
"""Render the same report to a fully editable .docx.

Formatting follows the department's prescription: Times New Roman 12 pt,
single line spacing, bold main headings, italic sub-headings, Roman numerals
on the preliminary pages and Arabic numerals on the main chapters.
"""
import os
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

import content_front as F
import content_body as CB

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "..", "Summer_Internship_Report_Mayank_Kumar.docx")

SERIF = "Times New Roman"
MONO = "Consolas"
BODY_W_IN = 6.0


# ------------------------------------------------------------------ helpers
def set_cell_shading(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def shade_paragraph(p, hexcolor='F2F2F2'):
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    pPr.append(shd)
    border = OxmlElement("w:pBdr")
    for edge in ("top", "left", "bottom", "right"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:space"), "4")
        e.set(qn("w:color"), "BFBFBF")
        border.append(e)
    pPr.append(border)


def add_page_field(paragraph, fmt=None):
    run = paragraph.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), " PAGE ")
    run._r.addnext(fld)
    return fld


def set_page_number_format(section, fmt, start=1):
    sectPr = section._sectPr
    pg = sectPr.find(qn("w:pgNumType"))
    if pg is None:
        pg = OxmlElement("w:pgNumType")
        sectPr.append(pg)
    pg.set(qn("w:fmt"), fmt)
    pg.set(qn("w:start"), str(start))


def style_run(run, size=12, bold=False, italic=False, font=SERIF,
              color=None):
    run.font.name = font
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), font)
    rfonts.set(qn("w:hAnsi"), font)
    rfonts.set(qn("w:eastAsia"), font)
    rfonts.set(qn("w:cs"), font)


def para(doc, text="", size=12, bold=False, italic=False, align="justify",
         space_after=6, space_before=0, indent=None, hanging=None,
         font=SERIF, line=1.0, keep_with_next=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
                    "center": WD_ALIGN_PARAGRAPH.CENTER,
                    "left": WD_ALIGN_PARAGRAPH.LEFT,
                    "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = line
    if indent is not None:
        pf.left_indent = Cm(indent)
    if hanging is not None:
        pf.first_line_indent = Cm(-hanging)
    pf.keep_with_next = keep_with_next
    if text:
        r = p.add_run(text)
        style_run(r, size=size, bold=bold, italic=italic, font=font)
    return p


def bullet(doc, text, size=12, marker="\u2022"):
    p = para(doc, "", size=size, align="justify", space_after=4, indent=0.85,
             hanging=0.6)
    r = p.add_run(marker + "\t")
    style_run(r, size=size)
    r2 = p.add_run(text)
    style_run(r2, size=size)
    p.paragraph_format.tab_stops.add_tab_stop(Cm(0.85))
    return p


def heading_page_break(doc):
    from docx.enum.text import WD_BREAK
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    p.add_run().add_break(WD_BREAK.PAGE)


# ----------------------------------------------------------------- document
def build():
    doc = Document()

    st = doc.styles["Normal"]
    st.font.name = SERIF
    st.font.size = Pt(12)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), SERIF)
    pf = st.paragraph_format
    pf.line_spacing = 1.0
    pf.space_after = Pt(6)
    pf.space_before = Pt(0)

    # ---- section 1: cover page (no page number)
    s1 = doc.sections[0]
    s1.page_height, s1.page_width = Cm(29.7), Cm(21.0)
    s1.left_margin, s1.right_margin = Cm(3.2), Cm(2.4)
    s1.top_margin, s1.bottom_margin = Cm(3.0), Cm(2.5)
    s1.header_distance, s1.footer_distance = Cm(1.2), Cm(1.2)

    def centred(text, size, bold=True, italic=False, after=6, before=0):
        return para(doc, text, size=size, bold=bold, italic=italic,
                    align="center", space_after=after, space_before=before)

    centred("INDUSTRIAL TRAINING REPORT", 17, after=14)
    centred("on", 13, bold=False, italic=True, after=12)
    centred("\u201c" + F.TITLE_COVER + "\u201d", 14, after=20)
    centred("by", 13, bold=False, italic=True, after=8)
    centred(F.STUDENT, 14, after=2)
    centred("Roll No. " + F.ROLL, 12, bold=False, after=24)
    centred("Submitted on Partial Fulfilment of the Requirements for the "
            "award of the Degree", 12, bold=False, after=8)
    centred("of", 12, bold=False, italic=True, after=8)
    centred("BACHELOR OF TECHNOLOGY", 15, after=6)
    centred("in", 12, bold=False, italic=True, after=6)
    centred("COMPUTER SCIENCE & ENGINEERING", 15, after=18)
    centred("from", 12, bold=False, italic=True, after=8)
    centred(F.ORG, 13, after=30)
    centred("Submitted to", 12, bold=False, italic=True, after=10)
    centred("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", 13, after=6)
    centred(F.FACULTY, 12, bold=False, after=6)
    centred(F.UNIV, 12, bold=False, after=26)
    centred(F.MONTH_YEAR, 12, after=0)

    # ---- section 2: preliminary pages, lower roman
    s2 = doc.add_section(WD_SECTION.NEW_PAGE)
    s2.left_margin, s2.right_margin = Cm(3.2), Cm(2.4)
    s2.top_margin, s2.bottom_margin = Cm(3.0), Cm(2.5)
    s2.footer.is_linked_to_previous = False
    s2.header.is_linked_to_previous = False
    set_page_number_format(s2, "lowerRoman", 1)
    # remove footer link of section 1
    s1.footer.is_linked_to_previous = False
    for f in (s1.footer, s1.header):
        for p in f.paragraphs:
            p.text = ""

    foot = s2.footer.paragraphs[0]
    foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_field(foot, "lowerRoman")
    hdr = s2.header.paragraphs[0]
    hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = hdr.add_run("Summer Internship Report  |  " + F.STUDENT)
    style_run(r, size=8.5)

    # declaration
    para(doc, "DECLARATION", size=14, bold=True, align="center",
         space_after=16)
    for t in F.DECLARATION:
        para(doc, t)
    para(doc, "", space_after=0)
    para(doc, "Date: ....................            Place: Lucknow",
         align="left", space_before=24, space_after=0)
    para(doc, "", space_after=0)
    para(doc, "( " + F.STUDENT + " )", bold=True, align="right",
         space_before=30, space_after=0)
    para(doc, "B.Tech CSE, 3rd Year", align="right", space_after=0)
    para(doc, "Roll No. " + F.ROLL, align="right", space_after=0)

    # certificate
    heading_page_break(doc)
    para(doc, "INTERNSHIP COMPLETION CERTIFICATE", size=14, bold=True,
         align="center", space_after=10)
    para(doc, F.CERT_NOTE)
    doc.add_picture(os.path.join(ASSETS, "certificate.png"),
                    width=Cm(15.4))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # abstract
    heading_page_break(doc)
    para(doc, "ABSTRACT", size=14, bold=True, align="center", space_after=14)
    for t in F.ABSTRACT:
        para(doc, t)

    # acknowledgement
    heading_page_break(doc)
    para(doc, "ACKNOWLEDGEMENT", size=14, bold=True, align="center",
         space_after=14)
    for t in F.ACK:
        para(doc, t)

    # TOC / LOT / LOF -----------------------------------------------------
    pages = load_pages()

    def leader_row(label, page, indent=0.0, bold=False, size=10.5,
                   space_before=0):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.left_indent = Cm(indent)
        p.paragraph_format.line_spacing = 1.0
        ts = p.paragraph_format.tab_stops
        ts.add_tab_stop(Cm(15.2), WD_TAB_ALIGNMENT.RIGHT, 2)  # 2 = dots
        r = p.add_run(label)
        style_run(r, size=size, bold=bold)
        r2 = p.add_run("\t" + str(page))
        style_run(r2, size=size, bold=bold)
        return p

    heading_page_break(doc)
    para(doc, "TABLE OF CONTENTS", size=14, bold=True, align="center",
         space_after=12)
    for kind, text, page in CB.toc_entries(pages):
        if kind == "h1":
            leader_row(text, page, bold=True, size=11, space_before=5)
        elif kind == "h2":
            leader_row(text, page, indent=0.6)
        else:
            leader_row(text, page, indent=1.2)

    heading_page_break(doc)
    para(doc, "LIST OF TABLES", size=14, bold=True, align="center",
         space_after=12)
    for text, page in CB.tables_list(pages):
        leader_row(text, page)

    heading_page_break(doc)
    para(doc, "LIST OF FIGURES", size=14, bold=True, align="center",
         space_after=12)
    for text, page in CB.figures_list(pages):
        leader_row(text, page)

    # ---- section 3: main body, arabic
    s3 = doc.add_section(WD_SECTION.NEW_PAGE)
    s3.left_margin, s3.right_margin = Cm(3.2), Cm(2.4)
    s3.top_margin, s3.bottom_margin = Cm(3.0), Cm(2.5)
    s3.footer.is_linked_to_previous = False
    s3.header.is_linked_to_previous = False
    set_page_number_format(s3, "decimal", 1)
    foot3 = s3.footer.paragraphs[0]
    foot3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_field(foot3, "decimal")
    hdr3 = s3.header.paragraphs[0]
    hdr3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = hdr3.add_run("Summer Internship Report  |  " + F.STUDENT)
    style_run(r, size=8.5)

    prev = [None]
    first_h1 = [True]
    for b in CB.B:
        k = b[0]
        if k == "pagebreak":
            heading_page_break(doc)
        elif k == "h1":
            if not (first_h1[0] or prev[0] == "pagebreak"):
                heading_page_break(doc)
            first_h1[0] = False
            para(doc, b[1], size=12, bold=True, align="left", space_before=6,
                 space_after=10, keep_with_next=True)
        elif k == "h2":
            para(doc, b[1], size=12, italic=True, align="left",
                 space_before=10, space_after=6, keep_with_next=True)
        elif k == "h3":
            para(doc, b[1], size=12, bold=True, italic=True, align="left",
                 space_before=8, space_after=4, keep_with_next=True)
        elif k == "p":
            para(doc, b[1])
        elif k == "pc":
            para(doc, b[1], align="center")
        elif k == "bullet":
            bullet(doc, b[1], marker="\u2022")
        elif k == "num":
            bullet(doc, b[1], marker="\u2013")
        elif k == "code":
            p = para(doc, "", align="left", space_before=4, space_after=10,
                     indent=0.3)
            lines = b[1].split("\n")
            for i, line in enumerate(lines):
                r = p.add_run(line)
                style_run(r, size=8.5, font=MONO)
                if i < len(lines) - 1:
                    r.add_break()
            shade_paragraph(p)
        elif k == "fig":
            path = os.path.join(FIGDIR, b[1])
            from PIL import Image as PILImage
            iw, ih = PILImage.open(path).size
            w = min(b[3], BODY_W_IN)
            doc.add_picture(path, width=Inches(w))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.paragraphs[-1].paragraph_format.space_before = Pt(6)
            doc.paragraphs[-1].paragraph_format.space_after = Pt(3)
            doc.paragraphs[-1].paragraph_format.keep_with_next = True
            para(doc, b[2], size=10, align="center", space_after=12)
        elif k == "table":
            para(doc, b[1], size=10, align="center", space_before=4,
                 space_after=4, keep_with_next=True)
            add_table(doc, b[2], b[3], b[4], b[5], b[6])
            para(doc, "", space_after=8)
        elif k == "ref":
            p = para(doc, "", align="justify", space_after=7, indent=1.0,
                     hanging=1.0)
            r = p.add_run(b[1] + "  ")
            style_run(r, size=11, bold=True)
            r2 = p.add_run(b[2])
            style_run(r2, size=11)
        else:
            raise ValueError(k)
        prev[0] = k

    doc.save(OUT)
    print("DOCX written:", os.path.abspath(OUT))


def add_table(doc, header, rows, widths, align, fontsize):
    size = fontsize or 9
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    amap = {"l": WD_ALIGN_PARAGRAPH.LEFT, "c": WD_ALIGN_PARAGRAPH.CENTER,
            "r": WD_ALIGN_PARAGRAPH.RIGHT}
    if widths:
        total = sum(widths)
        cmw = [Cm(15.4 * w / total) for w in widths]
    else:
        cmw = [Cm(15.4 / len(header))] * len(header)

    hdr = t.rows[0].cells
    for i, h in enumerate(header):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(h)
        style_run(r, size=size, bold=True)
        set_cell_shading(hdr[i], "DCE6F1")
        hdr[i].width = cmw[i]
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.alignment = amap[(align[i] if align and i < len(align)
                                else "l")]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            r = p.add_run(val)
            style_run(r, size=size)
            cells[i].width = cmw[i]
    # repeat header row across pages
    trPr = t.rows[0]._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)
    return t


def load_pages():
    """Read the page numbers produced by the PDF build (if available)."""
    import json
    path = os.path.join(HERE, "pages.json")
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    return {}


if __name__ == "__main__":
    build()
