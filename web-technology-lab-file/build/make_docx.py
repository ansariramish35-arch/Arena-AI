"""
make_docx.py
Builds the editable Microsoft Word file  Web_Technology_Laboratory_File.docx
with exactly the same content, sizes and page numbering as the PDF produced by
make_document.py.

Word is forced to paginate like the PDF by using
  * identical page size / margins (A4, 2.0 cm sides, 2.0 cm top, 2.2 cm bottom)
  * identical fonts and sizes (Times New Roman 12, Courier New 10 for code)
  * EXACT line spacing equal to the leading used in the PDF
  * the same explicit page breaks and the same image dimensions

Run :  python build/make_docx.py 3 7 11 15 18 21 24 28 32 39 44
      (the arguments are the practical start pages measured from the PDF;
       if omitted, make_document.py is run first to measure them)
"""
import os
import sys
import subprocess

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
IMG = os.path.join(ROOT, "images")
OUT = os.path.join(ROOT, "Web_Technology_Laboratory_File.docx")

sys.path.insert(0, HERE)
from make_document import (PRACTICALS, INDEX_NAMES, read, IMG_MAX_W, IMG_MAX_H,  # noqa
                         wrap_code)  # noqa
from PIL import Image as PILImage                                             # noqa

BODY_LEAD = 15.5      # must equal ST["body"].leading  in make_document.py
CODE_LEAD = 12.6      # must equal ST["code"].leading


# ---------------------------------------------------------------- helpers
def set_cell_margins_zero(table):
    tbl = table._tbl
    mar = OxmlElement("w:tblCellMar")
    for side, val in (("top", 40), ("bottom", 40), ("left", 80), ("right", 80)):
        e = OxmlElement("w:" + side)
        e.set(qn("w:w"), str(val))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tbl.tblPr.append(mar)


def page_number_footer(section):
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    rf = OxmlElement("w:rFonts")
    rf.set(qn("w:ascii"), "Times New Roman")
    rf.set(qn("w:hAnsi"), "Times New Roman")
    rsz = OxmlElement("w:sz")
    rsz.set(qn("w:val"), "22")
    rpr.append(rf)
    rpr.append(rsz)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    p._p.append(fld)


def para(doc, text="", size=12, bold=False, italic=False, align=None, font="Times New Roman",
         lead=BODY_LEAD, space_after=6, space_before=0, colour=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(lead)
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    if align is not None:
        p.alignment = align
    if text:
        r = p.add_run(text)
        r.font.name = font
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic
        r._element.rPr.rFonts.set(qn("w:hAnsi"), font)
        r._element.rPr.rFonts.set(qn("w:cs"), font)
        if colour:
            r.font.color.rgb = RGBColor(*colour)
    return p


def rich(doc, parts, align=None, lead=BODY_LEAD, space_after=6, space_before=0):
    """parts = list of (text, dict(size,bold,italic,font))"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(lead)
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    if align is not None:
        p.alignment = align
    for text, opt in parts:
        r = p.add_run(text)
        r.font.name = opt.get("font", "Times New Roman")
        r.font.size = Pt(opt.get("size", 12))
        r.bold = opt.get("bold", False)
        r.italic = opt.get("italic", False)
        r._element.rPr.rFonts.set(qn("w:hAnsi"), opt.get("font", "Times New Roman"))
        r._element.rPr.rFonts.set(qn("w:cs"), opt.get("font", "Times New Roman"))
    return p


def code_paragraph(doc, code):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(CODE_LEAD)
    pf.space_after = Pt(0)
    pf.space_before = Pt(0)
    pf.left_indent = Cm(0)
    lines = wrap_code(code).split("\n")
    for i, ln in enumerate(lines):
        r = p.add_run(ln if ln else "")
        r.font.name = "Courier New"
        r.font.size = Pt(10)
        r._element.rPr.rFonts.set(qn("w:hAnsi"), "Courier New")
        r._element.rPr.rFonts.set(qn("w:cs"), "Courier New")
        if i != len(lines) - 1:
            r.add_break(WD_BREAK.LINE)
    return p


def image_size(path):
    """same box rules as make_document.img_flowable, returned as docx Lengths"""
    with PILImage.open(path) as im:
        pw, ph = im.size
    ratio = ph / float(pw)
    w = float(IMG_MAX_W)          # reportlab points
    h = w * ratio
    if h > float(IMG_MAX_H):
        h = float(IMG_MAX_H)
        w = h / ratio
    return Pt(w), Pt(h)


def page_break_before(paragraph):
    paragraph.paragraph_format.page_break_before = True


# ---------------------------------------------------------------- document
def build(starts):
    doc = Document()

    # ---- page setup : A4 + margins + default font
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.2)
    sec.footer_distance = Cm(1.1)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    normal._element.rPr.rFonts.set(qn("w:cs"), "Times New Roman")
    page_number_footer(sec)

    # ================= FRONT PAGE =================
    para(doc, "______________________________________________", align=WD_ALIGN_PARAGRAPH.CENTER,
         lead=26, space_after=0)
    para(doc, "(Name of the University)", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    para(doc, "______________________________________________", align=WD_ALIGN_PARAGRAPH.CENTER,
         lead=26, space_after=0)
    para(doc, "(Name of the College)", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    para(doc, "Department of Computer Science & Engineering", bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)
    para(doc, "WEB TECHNOLOGY LABORATORY FILE", size=22, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    para(doc, "(A practical report of the Web Technology Laboratory course)",
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=44)

    rows = [("Student Name", ""), ("Roll Number", ""), ("Enrollment Number", ""),
            ("Course", "B.Tech - Computer Science & Engineering"),
            ("Semester", ""), ("Academic Session", "")]
    t = doc.add_table(rows=len(rows), cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, (k, v) in enumerate(rows):
        c0, c1 = t.rows[i].cells
        c0.width = Cm(5.2)
        c1.width = Cm(9.5)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        p0.paragraph_format.line_spacing = Pt(26)
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k + "  :")
        r0.bold = True
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(12)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        p1.paragraph_format.line_spacing = Pt(26)
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v if v else "______________________________")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12)
    para(doc, "", lead=26, space_after=0)
    para(doc, "Submitted To", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_before=30, space_after=0)
    para(doc, "______________________________", align=WD_ALIGN_PARAGRAPH.CENTER,
         lead=26, space_after=0)
    para(doc, "(Faculty Name)", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)

    # ================= INDEX =================
    p = para(doc, "INDEX", size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
             lead=20, space_before=4, space_after=10)
    page_break_before(p)
    t = doc.add_table(rows=1 + len(INDEX_NAMES), cols=4)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    widths = [Cm(1.5), Cm(10.2), Cm(2.6), Cm(2.2)]
    hdr = ["S. No.", "Name of Program", "Date", "Page No."]
    for j, h in enumerate(hdr):
        cell = t.rows[0].cells[j]
        cell.width = widths[j]
        cp = cell.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        cp.paragraph_format.line_spacing = Pt(16)
        cp.paragraph_format.space_after = Pt(0)
        r = cp.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
    for i, name in enumerate(INDEX_NAMES, start=1):
        vals = [str(i), name, "", str(starts.get(i, ""))]
        for j, v in enumerate(vals):
            cell = t.rows[i].cells[j]
            cell.width = widths[j]
            cp = cell.paragraphs[0]
            cp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            cp.paragraph_format.line_spacing = Pt(15.5)
            cp.paragraph_format.space_after = Pt(0)
            cp.paragraph_format.space_before = Pt(4)
            if j != 1:
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = cp.add_run(v)
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
    set_cell_margins_zero(t)

    # ================= PRACTICALS =================
    for pr in PRACTICALS:
        h = para(doc, "PRACTICAL No. %d" % pr["no"], size=16, bold=True,
                 align=WD_ALIGN_PARAGRAPH.CENTER, lead=20, space_before=4, space_after=10)
        page_break_before(h)
        rich(doc, [("Program : ", {"bold": True}), (pr["title"], {})], space_after=6)
        para(doc, "Source Code :", size=14, bold=True, lead=18,
             space_before=10, space_after=6)
        for fname, parts in pr["files"]:
            para(doc, fname, size=10.5, bold=True, font="Courier New", lead=16,
                 space_before=8, space_after=4)
            code_paragraph(doc, read(*parts))
            para(doc, "", lead=7, space_after=0)
        para(doc, "Output / Result :", size=14, bold=True, lead=18,
             space_before=10, space_after=6)
        para(doc, pr["note"], space_after=6)
        for i, (imgname, caption) in enumerate(pr["images"]):
            if i > 0:
                para(doc, "", lead=8.5, space_after=0)
            path = os.path.join(IMG, imgname)
            w, hh = image_size(path)
            pic = doc.add_paragraph()
            pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pic.paragraph_format.space_after = Pt(0)
            pic.paragraph_format.space_before = Pt(0)
            pic.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pic.paragraph_format.line_spacing = Pt(hh.pt)
            pic.add_run().add_picture(path, width=w, height=hh)
            para(doc, caption, size=10.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                 lead=13, space_before=4, space_after=10)

    doc.core_properties.title = "Web Technology Laboratory File"
    doc.core_properties.subject = "B.Tech Computer Science & Engineering"
    doc.core_properties.comments = "Web Technology Laboratory - 11 practicals"
    doc.save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        nums = [int(x) for x in sys.argv[1:]]
        starts = {i + 1: nums[i] for i in range(len(nums))}
    else:
        import re
        out = subprocess.run([sys.executable, os.path.join(HERE, "make_document.py")],
                             capture_output=True, text=True).stdout
        m = re.search(r"final start pages: \{([^}]*)\}", out)
        starts = {}
        for pair in m.group(1).split(","):
            k, v = pair.split(":")
            starts[int(k)] = int(v)
        print("measured start pages:", starts)
    build(starts)
