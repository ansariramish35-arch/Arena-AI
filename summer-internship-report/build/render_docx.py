"""Render the report to an editable .docx with the same content and formatting."""
import copy
import os
import re

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor, Emu

import model
from model import K
from figures_list import FIG, TAB

from content_front import FRONT
from content_main import CH1, CH2, CH3, CH4, CH5
from content_main2 import CH6, CH7
from content_main3 import CH8, CH9, CH10, APPENDIX, REFERENCES

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'B.Tech_CSE_Summer_Internship_Report_SwachhAI.docx')

NAVY = RGBColor(0x12, 0x3A, 0x63)
NAVY_DARK = RGBColor(0x0B, 0x24, 0x40)
GREEN = RGBColor(0x1E, 0x6B, 0x4F)
GREY = RGBColor(0x4A, 0x4A, 0x4A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BODY = 'Times New Roman'
TEXT_W_CM = 16.0

# --------------------------------------------------------------------------
# low level XML helpers
# --------------------------------------------------------------------------
def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(k), v)
    return e


def style_run(run, size=12, bold=False, italic=False, color=None, font=BODY,
              sub=False, caps=False):
    run.font.name = font
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    if sub:
        run.font.subscript = True
    if caps:
        run.font.all_caps = True
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.insert(0, rfonts)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rfonts.set(qn(a), font)


def para_border(p, color='C7D2DC', size=6, space=2, position='bottom'):
    pPr = p._p.get_or_add_pPr()
    bdr = pPr.find(qn('w:pBdr'))
    if bdr is None:
        bdr = OxmlElement('w:pBdr')
        pPr.append(bdr)
    e = OxmlElement('w:%s' % position)
    e.set(qn('w:val'), 'single')
    e.set(qn('w:sz'), str(size))
    e.set(qn('w:space'), str(space))
    e.set(qn('w:color'), color)
    bdr.append(e)


def para_shading(p, fill):
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    pPr.append(shd)


def cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    tcPr.append(shd)


def add_bookmark(paragraph, name, bid):
    start = OxmlElement('w:bookmarkStart')
    start.set(qn('w:id'), str(bid))
    start.set(qn('w:name'), name)
    end = OxmlElement('w:bookmarkEnd')
    end.set(qn('w:id'), str(bid))
    paragraph._p.insert(0, start)
    paragraph._p.append(end)


def add_internal_link(paragraph, anchor, text, bold=False, size=12, color=NAVY):
    h = OxmlElement('w:hyperlink')
    h.set(qn('w:anchor'), anchor)
    h.set(qn('w:history'), '1')
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rfonts = OxmlElement('w:rFonts')
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rfonts.set(qn(a), BODY)
    rPr.append(rfonts)
    if bold:
        rPr.append(OxmlElement('w:b'))
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), str(int(size * 2)))
    rPr.append(sz)
    col = OxmlElement('w:color')
    col.set(qn('w:val'), '%02X%02X%02X' % (color[0], color[1], color[2])
            if isinstance(color, tuple) else str(color))
    rPr.append(col)
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)
    r.append(rPr)
    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    r.append(t)
    h.append(r)
    paragraph._p.append(h)


def add_external_link(paragraph, url, text, size=12):
    part = paragraph.part
    r_id = part.relate_to(
        url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',
        is_external=True)
    h = OxmlElement('w:hyperlink')
    h.set(qn('r:id'), r_id)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rfonts = OxmlElement('w:rFonts')
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rfonts.set(qn(a), BODY)
    rPr.append(rfonts)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), str(int(size * 2)))
    rPr.append(sz)
    col = OxmlElement('w:color')
    col.set(qn('w:val'), '123A63')
    rPr.append(col)
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)
    r.append(rPr)
    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    r.append(t)
    h.append(r)
    paragraph._p.append(h)


def add_field(paragraph, instr, placeholder='1', size=10, bold=False):
    r = paragraph.add_run()
    style_run(r, size=size, bold=bold, color=GREY)
    fld = OxmlElement('w:fldChar')
    fld.set(qn('w:fldCharType'), 'begin')
    r._r.append(fld)
    r2 = paragraph.add_run()
    style_run(r2, size=size, bold=bold, color=GREY)
    it = OxmlElement('w:instrText')
    it.set(qn('xml:space'), 'preserve')
    it.text = instr
    r2._r.append(it)
    r3 = paragraph.add_run()
    style_run(r3, size=size, bold=bold, color=GREY)
    sep = OxmlElement('w:fldChar')
    sep.set(qn('w:fldCharType'), 'separate')
    r3._r.append(sep)
    r4 = paragraph.add_run(placeholder)
    style_run(r4, size=size, bold=bold, color=GREY)
    r5 = paragraph.add_run()
    style_run(r5, size=size, bold=bold, color=GREY)
    end = OxmlElement('w:fldChar')
    end.set(qn('w:fldCharType'), 'end')
    r5._r.append(end)


# --------------------------------------------------------------------------
# inline markup parser
# --------------------------------------------------------------------------
TAG_RE = re.compile(r'(<b>|</b>|<i>|</i>|<sub>|</sub>|<a\s+href="[^"]*">|</a>)')


def parse_inline(text):
    tokens = []
    bold = italic = sub = False
    link = None
    pos = 0
    for m in TAG_RE.finditer(text):
        if m.start() > pos:
            tokens.append((text[pos:m.start()], bold, italic, sub, link))
        tag = m.group(0)
        if tag == '<b>':
            bold = True
        elif tag == '</b>':
            bold = False
        elif tag == '<i>':
            italic = True
        elif tag == '</i>':
            italic = False
        elif tag == '<sub>':
            sub = True
        elif tag == '</sub>':
            sub = False
        elif tag.startswith('<a'):
            link = re.search(r'href="([^"]*)"', tag).group(1)
        else:
            link = None
        pos = m.end()
    if pos < len(text):
        tokens.append((text[pos:], bold, italic, sub, link))
    return tokens


def unescape(s):
    return (s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
             .replace('&nbsp;', '\u00a0'))


class Builder:
    def __init__(self):
        self.doc = Document()
        self.bid = 1000
        self.setup_styles()
        self.sections_ready = False

    # -- document defaults ------------------------------------------------
    def setup_styles(self):
        st = self.doc.styles['Normal']
        st.font.name = BODY
        st.font.size = Pt(12)
        rpr = st.element.get_or_add_rPr()
        rfonts = rpr.find(qn('w:rFonts'))
        if rfonts is None:
            rfonts = OxmlElement('w:rFonts')
            rpr.insert(0, rfonts)
        for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
            rfonts.set(qn(a), BODY)
        pf = st.paragraph_format
        pf.line_spacing = 1.0
        pf.space_before = Pt(0)
        pf.space_after = Pt(4)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        sec = self.doc.sections[0]
        sec.page_width = Mm(210)
        sec.page_height = Mm(297)
        sec.left_margin = Mm(30)
        sec.right_margin = Mm(20)
        sec.top_margin = Mm(23)
        sec.bottom_margin = Mm(19)
        sec.header_distance = Mm(11)
        sec.footer_distance = Mm(9)

        # update fields (TOC) on open
        settings = self.doc.settings.element
        uf = OxmlElement('w:updateFields')
        uf.set(qn('w:val'), 'true')
        settings.append(uf)

    # -- text helpers -----------------------------------------------------
    def para(self, text='', size=12, bold=False, italic=False, color=None,
             align='justify', space_before=0, space_after=4, indent=None,
             first_line=None, hanging=False, left=None, keep_next=False,
             line=1.0, caps=False, style=None):
        p = self.doc.add_paragraph(style=style)
        pf = p.paragraph_format
        pf.alignment = {'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
                        'left': WD_ALIGN_PARAGRAPH.LEFT,
                        'center': WD_ALIGN_PARAGRAPH.CENTER,
                        'right': WD_ALIGN_PARAGRAPH.RIGHT}[align]
        pf.space_before = Pt(space_before)
        pf.space_after = Pt(space_after)
        pf.line_spacing = line
        if left is not None:
            pf.left_indent = Cm(left)
        if indent is not None:
            pf.first_line_indent = Cm(indent)
        if hanging:
            pf.first_line_indent = Cm(-0.6)
        if keep_next:
            pf.keep_with_next = True
        if text:
            for chunk, b, i, sub, link in parse_inline(text):
                chunk = unescape(chunk)
                if not chunk:
                    continue
                if link and link.startswith('#'):
                    add_internal_link(p, link[1:], chunk, bold=b or bold,
                                      size=size, color=NAVY)
                    continue
                if link and link.startswith('http'):
                    add_external_link(p, link, chunk, size=size)
                    continue
                r = p.add_run(chunk)
                style_run(r, size=size, bold=b or bold, italic=i or italic,
                          color=color, sub=sub, caps=caps)
        return p

    def bullet(self, text, size=12, indent=0.7):
        p = self.para(text, size=size, left=indent, hanging=True, space_after=2)
        p.paragraph_format.first_line_indent = Cm(-0.45)
        # move the bullet glyph into the text via a numbered prefix is avoided:
        # insert a bullet run at the start
        r = p.runs[0] if p.runs else None
        bullet_p = self.doc.paragraphs[-1]
        return p

    def heading(self, text, level=1, number=None, bookmark=True):
        """Chapter banner (level 0), section (1) or sub-section (2)."""
        if level == 0:
            if number:
                eye = self.para('', size=9.5, bold=True, color=GREEN, align='left',
                                space_before=0, space_after=1, keep_next=True)
                r = eye.add_run('CHAPTER %s' % number)
                style_run(r, size=9.5, bold=True, color=GREEN)
            p = self.para(text.upper(), size=12, bold=True, color=NAVY_DARK,
                          align='left', space_before=0, space_after=10,
                          keep_next=True)
            para_border(p, color='123A63', size=12, space=3)
            name = K(text)
            add_bookmark(p, name, self.next_id())
            p.style = self.doc.styles['Heading 1']
            self._heading_style(p, 12, True, NAVY_DARK)
            return p
        if level == 1:
            p = self.para(text, size=12, bold=True, color=NAVY_DARK, align='left',
                          space_before=11, space_after=4, keep_next=True)
            p.style = self.doc.styles['Heading 2']
            self._heading_style(p, 12, True, NAVY_DARK)
            if bookmark:
                add_bookmark(p, K(text), self.next_id())
            return p
        p = self.para(text, size=12, bold=True, italic=True, color=NAVY,
                      align='left', space_before=8, space_after=3, keep_next=True)
        p.style = self.doc.styles['Heading 3']
        self._heading_style(p, 12, True, NAVY)
        if bookmark:
            add_bookmark(p, K(text), self.next_id())
        return p

    @staticmethod
    def _heading_style(p, size, bold, color):
        for r in p.runs:
            style_run(r, size=size, bold=bold, color=color)

    def next_id(self):
        self.bid += 1
        return self.bid

    # -- tables -----------------------------------------------------------
    def table(self, spec):
        cap_text = TAB[spec['key']]
        p = self.para(cap_text, size=10, bold=True, color=NAVY_DARK, align='left',
                      space_before=7, space_after=3, keep_next=True)
        add_bookmark(p, K(cap_text), self.next_id())
        header = spec['header']
        rows = spec['rows']
        widths = spec.get('widths')
        t = self.doc.add_table(rows=1, cols=len(header))
        t.style = 'Table Grid'
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        hdr = t.rows[0].cells
        for i, h in enumerate(header):
            hdr[i].text = ''
            para = hdr[i].paragraphs[0]
            para.paragraph_format.space_after = Pt(1)
            para.paragraph_format.space_before = Pt(1)
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for chunk, b, it, sub, link in parse_inline(h):
                r = para.add_run(unescape(chunk))
                style_run(r, size=9.4, bold=True, color=WHITE)
            cell_shading(hdr[i], '123A63')
        for i, row in enumerate(rows):
            cells = t.add_row().cells
            for j, val in enumerate(row):
                cells[j].text = ''
                para = cells[j].paragraphs[0]
                para.paragraph_format.space_after = Pt(1)
                para.paragraph_format.space_before = Pt(1)
                para.paragraph_format.line_spacing = 1.0
                para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for chunk, b, it, sub, link in parse_inline(val):
                    if link and link.startswith('#'):
                        add_internal_link(para, link[1:], unescape(chunk),
                                          bold=b, size=9.4, color=NAVY)
                        continue
                    r = para.add_run(unescape(chunk))
                    style_run(r, size=9.4, bold=b, italic=it, sub=sub)
                if i % 2 == 1:
                    cell_shading(cells[j], 'F4F6F8')
        # column widths
        if widths:
            total = Mm(160)
            for row in t.rows:
                for i, w in enumerate(widths):
                    row.cells[i].width = Emu(int(total * w))
        # repeat header row
        trPr = t.rows[0]._tr.get_or_add_trPr()
        trPr.append(_el('w:tblHeader', **{'w:val': 'true'}))
        if spec.get('note'):
            self.para(spec['note'], size=9, italic=True, color=GREY, align='left',
                      space_before=2, space_after=8)
        else:
            self.para('', size=4, space_after=4)
        return t

    # -- figures ----------------------------------------------------------
    def figure(self, path, caption, width_cm=None, max_h_cm=8.2):
        if not os.path.isabs(path):
            cand = os.path.join(ROOT, path)
            if not os.path.exists(cand):
                cand = os.path.join(ROOT, 'images', path)
            path = cand
        from PIL import Image as PILImage
        iw, ih = PILImage.open(path).size
        w_cm = width_cm or TEXT_W_CM
        h_cm = w_cm * ih / iw
        if h_cm > max_h_cm:
            h_cm = max_h_cm
            w_cm = h_cm * iw / ih
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run()
        run.add_picture(path, width=Cm(w_cm))
        cp = self.para(caption, size=10, italic=True, color=NAVY_DARK, align='center',
                       space_before=2, space_after=8)
        add_bookmark(cp, K(caption), self.next_id())
        return cp

    # -- rules, callouts, quotes -----------------------------------------
    def rule(self, color='1E6B4F', size=8):
        p = self.para('', size=2, space_after=6)
        para_border(p, color=color, size=size, space=1)

    def callout(self, text):
        p = self.para('', size=11, space_before=6, space_after=8)
        para_shading(p, 'E8F3EC')
        para_border(p, color='1E6B4F', size=18, space=4, position='left')
        pPr = p._p.get_or_add_pPr()
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'), '170')
        ind.set(qn('w:right'), '114')
        pPr.append(ind)
        for chunk, b, i, sub, link in parse_inline(text):
            if link and link.startswith('#'):
                add_internal_link(p, link[1:], unescape(chunk), bold=b, size=11,
                                  color=NAVY)
                continue
            r = p.add_run(unescape(chunk))
            style_run(r, size=11, bold=b, italic=i, sub=sub)
        return p

    def bullets(self, items):
        for it in items:
            p = self.para('\u2022\u2003' + '', size=12, left=0.75, space_after=2)
            p.paragraph_format.first_line_indent = Cm(-0.45)
            for chunk, b, i, sub, link in parse_inline(it):
                if link and link.startswith('#'):
                    add_internal_link(p, link[1:], unescape(chunk), bold=b)
                    continue
                r = p.add_run(unescape(chunk))
                style_run(r, size=12, bold=b, italic=i, sub=sub)
        self.para('', size=4, space_after=3)

    def numbered(self, items):
        for n, it in enumerate(items, 1):
            p = self.para('%d.\u2003' % n, size=12, left=0.9, space_after=2)
            p.paragraph_format.first_line_indent = Cm(-0.5)
            for chunk, b, i, sub, link in parse_inline(it):
                if link and link.startswith('#'):
                    add_internal_link(p, link[1:], unescape(chunk), bold=b)
                    continue
                r = p.add_run(unescape(chunk))
                style_run(r, size=12, bold=b, italic=i, sub=sub)
        self.para('', size=4, space_after=3)


# --------------------------------------------------------------------------
# page furniture (headers, footers, sections)
# --------------------------------------------------------------------------
def set_page_numbering(section, fmt=None, start=None):
    sectPr = section._sectPr
    pg = sectPr.find(qn('w:pgNumType'))
    if pg is None:
        pg = OxmlElement('w:pgNumType')
        sectPr.append(pg)
    if fmt:
        pg.set(qn('w:fmt'), fmt)
    if start is not None:
        pg.set(qn('w:start'), str(start))


def footer_with_number(section, fmt='decimal', start=None, bold=True):
    section.footer.is_linked_to_previous = False
    f = section.footer
    p = f.paragraphs[0]
    p.text = ''
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    para_border(p, color='C7D2DC', size=6, space=2, position='top')
    add_field(p, ' PAGE ', placeholder='1', size=10, bold=bold)
    set_page_numbering(section, fmt=fmt, start=start)


def header_text(section, left, right):
    section.header.is_linked_to_previous = False
    h = section.header
    p = h.paragraphs[0]
    p.text = ''
    p.paragraph_format.space_after = Pt(0)
    para_border(p, color='C7D2DC', size=6, space=3, position='bottom')
    p.paragraph_format.tab_stops.add_tab_stop(Mm(160), WD_TAB_ALIGNMENT.RIGHT)
    r = p.add_run(left)
    style_run(r, size=8.5, bold=True, color=GREEN)
    r2 = p.add_run('\t')
    style_run(r2, size=8.5)
    r3 = p.add_run(right)
    style_run(r3, size=8.5, italic=True, color=GREY)


def empty_section_furniture(section):
    section.header.is_linked_to_previous = False
    section.footer.is_linked_to_previous = False


# --------------------------------------------------------------------------
# cover, TOC, front matter
# --------------------------------------------------------------------------
def build_cover(b):
    d = b.doc
    sec = d.sections[0]
    empty_section_furniture(sec)
    set_page_numbering(sec, fmt='lowerRoman', start=1)

    b.para('', size=8, space_after=2)
    p = b.para('UNIVERSITY OF LUCKNOW', size=16, bold=True, color=NAVY_DARK,
               align='center', space_after=2)
    b.para('LUCKNOW \u2014 226 021, UTTAR PRADESH', size=11.5, bold=True,
           color=NAVY_DARK, align='center', space_after=2)
    p = b.para('DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING', size=10.5,
               bold=True, color=GREEN, align='center', space_after=10)
    para_border(p, color='1E6B4F', size=8, space=6)

    b.para('A REPORT ON SUMMER INTERNSHIP', size=10.5, bold=True, color=GREY,
           align='center', space_before=18, space_after=1)
    b.para('(Session 2025\u201326)', size=10.5, italic=True, color=GREY,
           align='center', space_after=16)
    b.para('SwachhAI', size=22, bold=True, color=NAVY_DARK, align='center',
           space_after=4)
    b.para('AI-Guided Waste Segregation and Circularity Assistant',
           size=12.5, italic=True, color=GREEN, align='center', space_after=0)
    b.para('for India\u2019s Households', size=12.5, italic=True, color=GREEN,
           align='center', space_after=18)
    b.para('Submitted in partial fulfilment of the requirements for the award of '
           'the degree of', size=9.8, bold=True, color=GREY, align='center',
           space_after=4)
    b.para('BACHELOR OF TECHNOLOGY', size=13, bold=True, color=NAVY_DARK,
           align='center', space_after=2)
    b.para('in', size=11, italic=True, color=NAVY_DARK, align='center', space_after=2)
    b.para('COMPUTER SCIENCE AND ENGINEERING', size=13, bold=True,
           color=NAVY_DARK, align='center', space_after=20)
    b.para('SUBMITTED BY', size=9.8, bold=True, color=GREY, align='center',
           space_after=3)
    b.para('MOHAMMAD RAMISH ANSARI', size=13.5, bold=True, color=NAVY_DARK,
           align='center', space_after=2)
    b.para('B.Tech. Computer Science and Engineering', size=10.5, align='center',
           space_after=1)
    b.para('Third Year, Semester V', size=10.5, align='center', space_after=1)
    b.para('University Roll No.: ____________________', size=10.5, align='center',
           space_after=16)
    b.para('UNDER THE SUPERVISION OF', size=9.8, bold=True, color=GREY,
           align='center', space_after=3)
    b.para('____________________  (Faculty Supervisor)', size=10.5, align='center',
           space_after=1)
    b.para('Department of Computer Science and Engineering', size=10.5,
           align='center', space_after=18)

    # internship band as a shaded paragraph
    band = b.para('', size=9, align='center', space_before=4, space_after=14)
    para_shading(band, 'E8F3EC')
    para_border(band, color='1E6B4F', size=8, space=6, position='top')
    para_border(band, color='1E6B4F', size=8, space=6, position='bottom')
    r = band.add_run('INTERNSHIP COMPLETED AT\n')
    style_run(r, size=8.6, bold=True, color=GREEN)
    r = band.add_run('1M1B (One Million for One Billion)\n')
    style_run(r, size=11, bold=True, color=NAVY_DARK)
    r = band.add_run('AI for Sustainability Virtual Internship \u00b7 supported by AICTE '
                     '\u00b7 in collaboration with IBM SkillsBuild\n')
    style_run(r, size=8.8, color=GREY)
    r = band.add_run('Certified completion period: July 2026 \u2013 September 2026 '
                     '\u00b7 Certificate issued 22 September 2026')
    style_run(r, size=8.8, color=GREY)

    b.para('SESSION 2025\u201326', size=10, bold=True, color=NAVY_DARK,
           align='center', space_before=26, space_after=1)
    b.para('Spiral bound \u00b7 single-sided printing \u00b7 submitted for university '
           'evaluation', size=8.4, color=GREY, align='center')


def build_toc(b):
    """A real Word TOC field (updates on open) plus a note."""
    b.para('', size=6, space_after=4)
    b.para('TABLE OF CONTENTS', size=12, bold=True, color=NAVY_DARK, align='center',
           space_after=4)
    b.rule()
    p = b.para('', size=12, align='left', space_before=4)
    add_field(p, ' TOC \\o "1-2" \\h \\z \\u ',
              placeholder='Right-click and choose \u201cUpdate Field\u201d to build the '
                          'table of contents.', size=11)
    b.para('', size=8, space_before=8)
    b.para('The table of contents is a live Word field: all entries are clickable and '
           'page numbers follow the pagination of this document. It is configured to '
           'update automatically when the file is opened; if it does not, select the '
           'field and press F9.', size=9, italic=True, color=GREY, align='left')


def build_lot(b):
    b.para('', size=6, space_after=4)
    b.para('LIST OF TABLES', size=12, bold=True, color=NAVY_DARK, align='center',
           space_after=4)
    b.rule()
    b.para('', size=6)
    for key, text in [(k, v) for k, v in TAB.items()]:
        p = b.para('', size=11, space_after=3)
        add_internal_link(p, K(text), text, size=11)

def build_lof(b):
    b.para('', size=6, space_after=4)
    b.para('LIST OF FIGURES', size=12, bold=True, color=NAVY_DARK, align='center',
           space_after=4)
    b.rule()
    b.para('', size=6)
    for fname, text in FIG.items():
        p = b.para('', size=11, space_after=3)
        add_internal_link(p, K(text), text, size=11)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def build():
    b = Builder()
    d = b.doc

    # cover is emitted from the FRONT block list
    # ---- section break: preliminary pages (roman, numbering shown) ----
    sec2 = d.add_section(WD_SECTION.NEW_PAGE)
    sec2.left_margin = Mm(30); sec2.right_margin = Mm(20)
    sec2.top_margin = Mm(23); sec2.bottom_margin = Mm(19)
    sec2.header_distance = Mm(11); sec2.footer_distance = Mm(9)
    header_text(sec2, 'SUMMER INTERNSHIP REPORT  \u00b7  2026', 'Preliminary pages')
    footer_with_number(sec2, fmt='lowerRoman', start=None)

    state = {'skip_toc': False}

    def emit(block):
        kind = block[0]
        if kind == 'cover':
            build_cover(b)
        elif kind == 'pagebreak':
            b.doc.add_page_break()
        elif kind == 'spacer':
            b.para('', size=block[1] / 3.0, space_after=0)
        elif kind == 'h1_front':
            if block[1] in ('TABLE OF CONTENTS', 'LIST OF TABLES', 'LIST OF FIGURES'):
                state['skip_toc'] = True
                return
            b.para('', size=6, space_after=2)
            p = b.para(block[1], size=12, bold=True, color=NAVY_DARK,
                       align='center', space_after=6, keep_next=True)
            add_bookmark(p, K(block[1]), b.next_id())
            b.rule(color='1E6B4F')
            b.para('', size=4, space_after=2)
        elif kind == 'h1':
            b.heading(block[1], level=1)
        elif kind == 'h2':
            b.heading(block[1], level=2)
        elif kind == 'p':
            b.para(block[1], size=12, space_after=5)
        elif kind == 'quote':
            b.para(block[1], size=12, italic=True, color=NAVY, left=1.2,
                   space_before=4, space_after=8)
        elif kind == 'bullets':
            b.bullets(block[1])
        elif kind == 'numbered':
            b.numbered(block[1])
        elif kind == 'callout':
            b.callout(block[1])
        elif kind == 'sigblock':
            b.para('', size=16, space_after=4)
            for left, right in block[1]:
                p = b.para('', size=12, align='left', space_after=2)
                p.paragraph_format.tab_stops.add_tab_stop(Mm(160), WD_TAB_ALIGNMENT.RIGHT)
                if left:
                    r = p.add_run(left)
                    style_run(r, size=12)
                if right:
                    r = p.add_run('\t' + right)
                    style_run(r, size=12)
        elif kind == 'certpage':
            for path, caption in block[1]:
                b.figure(path, caption, width_cm=15.6, max_h_cm=11.5)
        elif kind == 'figure':
            path, caption = block[1], block[2]
            wcm = 16.0 * (block[3] / 100.0) if len(block) > 3 else 16.0
            b.figure(path, caption, width_cm=wcm)
        elif kind == 'table':
            b.table(dict(block[1]))
        elif kind == 'chapter':
            b.doc.add_page_break()
            b.heading(block[2], level=0, number=block[1])
            b.para('', size=4, space_after=2)
        elif kind == 'toc':
            build_toc(b)
        elif kind == 'lot':
            build_lot(b)
        elif kind == 'lof':
            build_lof(b)
        elif kind == 'refs':
            for num, text, url in block[1]:
                p = b.para('', size=11, space_after=2, left=0.9, hanging=True)
                p.paragraph_format.first_line_indent = Cm(-0.9)
                name = 'ref%d' % num
                add_bookmark(p, name, b.next_id())
                r = p.add_run('[%d]  ' % num)
                style_run(r, size=11, bold=True)
                for chunk, bo, it, sub, link in parse_inline(text):
                    r = p.add_run(unescape(chunk))
                    style_run(r, size=11, bold=bo, italic=it, sub=sub)
                if url:
                    q = b.para('', size=9.5, space_after=6, left=0.9)
                    add_external_link(q, url, url, size=9.5)
        else:
            raise ValueError(kind)

    started_main = {'done': False}

    for block in FRONT:
        emit(block)

    def start_main():
        nonlocal started_main
        if started_main['done']:
            return
        sec = d.add_section(WD_SECTION.NEW_PAGE)
        sec.left_margin = Mm(30); sec.right_margin = Mm(20)
        sec.top_margin = Mm(23); sec.bottom_margin = Mm(19)
        sec.header_distance = Mm(11); sec.footer_distance = Mm(9)
        header_text(sec, 'SUMMER INTERNSHIP REPORT  \u00b7  2026',
                    'SwachhAI \u2014 AI-Guided Waste Segregation')
        footer_with_number(sec, fmt='decimal', start=1)
        started_main['done'] = True

    for chapter in (CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10):
        start_main()
        for block in chapter:
            emit(block)

    # references
    b.doc.add_page_break()
    b.heading('References and Bibliography', level=0, number='')
    b.para('The list below contains only sources that were actually consulted and that '
           'support statements made in this report. Publication details and web addresses '
           'were verified before inclusion. Where a document has been amended since '
           'notification, the principal notification is cited and the amendment is named '
           'in the text.', size=12, space_after=5)
    b.para('Items [1] to [9] are the primary sources for the published statistics and rules '
           'used in Chapters 5 to 8. Items [10] to [16] support the technology and '
           'programme descriptions. Items [17] and [18] are the standard references for '
           'retrieval-augmented generation and the transformer architecture. Item [19] is '
           'the university guideline followed for formatting. Item [20] is the project '
           'document submitted during the internship; it is not publicly available and is '
           'cited for internal traceability only.', size=12, space_after=8)
    emit(('refs', REFERENCES))
    b.para('A note on citation practice. Numerical citations in the text refer to this list '
           'and are clickable in the digital edition. Statistics are given with their '
           'reporting year, because several figures in this area change annually. No source '
           'has been cited that was not consulted, and no reference has been included to '
           'lengthen the list.', size=12, space_before=6)

    for block in APPENDIX:
        if block[0] == 'chapter':
            b.doc.add_page_break()
            b.heading(block[2], level=0, number=block[1])
            b.para('', size=4, space_after=2)
        else:
            emit(block)

    d.save(OUT)
    print('written', OUT)


if __name__ == '__main__':
    build()
