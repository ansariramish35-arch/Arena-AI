"""Layout kit for the B.Tech CSE Summer Internship Report (PDF side).

Produces an A4, single-sided, spiral-binding-friendly academic report with:
  * Roman page numbers for preliminary pages, Arabic for the main report
  * Clickable table of contents, list of tables, list of figures
  * PDF outline bookmarks for every chapter / section
  * Cross-reference links between body text, tables and figures
"""
import hashlib
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image,
                                KeepTogether, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------
NAVY = colors.HexColor('#123A63')
NAVY_DARK = colors.HexColor('#0B2440')
GREEN = colors.HexColor('#1E6B4F')
GREEN_LIGHT = colors.HexColor('#E8F3EC')
GREEN_MID = colors.HexColor('#4E8F72')
GREY = colors.HexColor('#4A4A4A')
GREY_LIGHT = colors.HexColor('#EDEFF2')
RULE = colors.HexColor('#C7D2DC')

BODY_FONT = 'Times-Roman'
BOLD = 'Times-Bold'
ITAL = 'Times-Italic'
BOLDITAL = 'Times-BoldItalic'

TEXT_W = A4[0] - 30 * mm - 20 * mm          # 160 mm frame
TEXT_H = A4[1] - 23 * mm - 19 * mm

# --------------------------------------------------------------------------
# Styles
# --------------------------------------------------------------------------
S = {}
S['body'] = ParagraphStyle('body', fontName=BODY_FONT, fontSize=12, leading=12.6,
                           alignment=TA_JUSTIFY, spaceAfter=3.8, textColor=colors.black,
                           firstLineIndent=0)
S['body_first'] = ParagraphStyle('body_first', parent=S['body'], spaceBefore=0)
S['eyebrow'] = ParagraphStyle('eyebrow', fontName=BOLD, fontSize=9.5, leading=12,
                              textColor=GREEN, alignment=TA_LEFT, spaceAfter=2)
S['h1'] = ParagraphStyle('H1', fontName=BOLD, fontSize=12, leading=15,
                         textColor=NAVY_DARK, alignment=TA_LEFT, spaceBefore=2,
                         spaceAfter=3)
S['h1_front'] = ParagraphStyle('H1', fontName=BOLD, fontSize=12, leading=15,
                               textColor=NAVY_DARK, alignment=TA_CENTER, spaceBefore=0,
                               spaceAfter=3)
S['h2'] = ParagraphStyle('H2', fontName=BOLDITAL, fontSize=12, leading=14,
                         textColor=NAVY, alignment=TA_LEFT, spaceBefore=8, spaceAfter=2)
S['h3'] = ParagraphStyle('H3', fontName=BOLD, fontSize=12, leading=15,
                         textColor=NAVY, alignment=TA_LEFT, spaceBefore=9, spaceAfter=3)
S['bul'] = ParagraphStyle('bul', parent=S['body'], leftIndent=20, bulletIndent=6,
                          spaceAfter=1.9, alignment=TA_JUSTIFY)
S['bul2'] = ParagraphStyle('bul2', parent=S['bul'], leftIndent=38, bulletIndent=24)
S['num'] = ParagraphStyle('num', parent=S['body'], leftIndent=24, bulletIndent=6,
                          spaceAfter=3.5)
S['caption'] = ParagraphStyle('caption', fontName=ITAL, fontSize=10, leading=12,
                              alignment=TA_CENTER, textColor=NAVY_DARK,
                              spaceBefore=3, spaceAfter=1)
S['caption_tab'] = ParagraphStyle('caption_tab', fontName=BOLD, fontSize=10, leading=12,
                                  alignment=TA_LEFT, textColor=NAVY_DARK,
                                  spaceBefore=7, spaceAfter=3)
S['note'] = ParagraphStyle('note', fontName=ITAL, fontSize=9.5, leading=12,
                           alignment=TA_LEFT, textColor=GREY, spaceBefore=3, spaceAfter=8)
S['cell'] = ParagraphStyle('cell', fontName=BODY_FONT, fontSize=9.3, leading=10.7,
                           alignment=TA_LEFT, textColor=colors.black)
S['cellb'] = ParagraphStyle('cellb', parent=S['cell'], fontName=BOLD, textColor=NAVY_DARK)
S['cellh'] = ParagraphStyle('cellh', parent=S['cell'], fontName=BOLD,
                            textColor=colors.white)
S['cellc'] = ParagraphStyle('cellc', parent=S['cell'], alignment=TA_CENTER)
S['quote'] = ParagraphStyle('quote', fontName=ITAL, fontSize=12, leading=15,
                            alignment=TA_JUSTIFY, leftIndent=22, rightIndent=14,
                            textColor=NAVY, spaceBefore=6, spaceAfter=10)
S['callout'] = ParagraphStyle('callout', fontName=BODY_FONT, fontSize=11, leading=14.5,
                              alignment=TA_JUSTIFY, leftIndent=10, rightIndent=8,
                              textColor=NAVY_DARK)
S['toch0'] = ParagraphStyle('toch0', fontName=BOLD, fontSize=10.8, leading=14.2,
                            textColor=NAVY_DARK, spaceBefore=4)
S['toch1'] = ParagraphStyle('toch1', fontName=BODY_FONT, fontSize=10.4, leading=13,
                            leftIndent=15, textColor=colors.black)
S['toch2'] = ParagraphStyle('toch2', fontName=BODY_FONT, fontSize=9.8, leading=12.2,
                            leftIndent=30, textColor=GREY)


def key(text):
    """Deterministic destination name for a heading/caption string."""
    norm = ' '.join(text.split())
    return 'S' + hashlib.md5(norm.encode('utf-8')).hexdigest()[:12]


def xref(text, label=None):
    """Inline clickable cross-reference to a heading or caption."""
    return ('<a href="#%s" color="#123A63"><b>%s</b></a>'
            % (key(text), label or text))


def extlink(url, label=None):
    return '<a href="%s" color="#123A63"><u>%s</u></a>' % (url, label or url)


def _strip_tags(s):
    out, skip = [], False
    for ch in s:
        if ch == '<':
            skip = True
        elif ch == '>':
            skip = False
        elif not skip:
            out.append(ch)
    return ''.join(out)


# --------------------------------------------------------------------------
# Flowables
# --------------------------------------------------------------------------
class Rule(Flowable):
    """Thin coloured horizontal rule."""

    def __init__(self, width=None, thickness=1.1, color=GREEN, space_before=2,
                 space_after=6):
        Flowable.__init__(self)
        self.width_ = width
        self.thickness = thickness
        self.color = color
        self.sb = space_before
        self.sa = space_after

    def wrap(self, aw, ah):
        self._w = self.width_ or aw
        return self._w, self.thickness + self.sb + self.sa

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.color)
        c.setLineWidth(self.thickness)
        y = self.sa
        c.line(0, y, self._w, y)


class ChapterHead(Flowable):
    """Chapter banner: eyebrow number + 12 pt bold title + double rule."""

    def __init__(self, number, title, width=TEXT_W):
        Flowable.__init__(self)
        self.number = number
        self.title = title
        self._w = width
        self.register = True

    def wrap(self, aw, ah):
        self._w = aw
        tstyle = S['h1']
        tw = stringWidth(self.title.upper(), BOLD, 12)
        lines = 1
        if tw > aw:
            lines = 1 + int(tw // aw)
        self._h = 13 + 17 * lines + 16
        return aw, self._h

    def draw(self):
        c = self.canv
        h = self._h
        if self.number:
            c.setFillColor(GREEN)
            c.setFont(BOLD, 9.5)
            c.drawString(0, h - 10, 'CHAPTER %s' % self.number)
        c.setFillColor(NAVY_DARK)
        c.setFont(BOLD, 12)
        text = self.title.upper()
        lines, cur = [], ''
        for word in text.split():
            trial = (cur + ' ' + word).strip()
            if stringWidth(trial, BOLD, 12) <= self._w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
        y = h - 10 - 17
        for ln in lines:
            c.drawString(0, y, ln)
            y -= 16
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.4)
        c.line(0, 12, self._w, 12)
        c.setStrokeColor(GREEN)
        c.setLineWidth(0.8)
        c.line(0, 7.5, self._w * 0.34, 7.5)


class Caption(Paragraph):
    """Figure/table caption that registers itself for the LOF/LOT."""
    is_caption = True

    def __init__(self, text, kind, style, number_label=None):
        self.caption_text = text
        self.kind = kind                     # 'FIG' or 'TAB'
        self.dest = key(text)
        Paragraph.__init__(self, text, style)


class Callout(Flowable):
    """Tinted note box with a green left bar."""

    def __init__(self, para, width=TEXT_W):
        Flowable.__init__(self)
        self.para = para
        self._w = width

    def wrap(self, aw, ah):
        self._w = aw
        pw = aw - 22
        w, h = self.para.wrap(pw, ah)
        self._ph = h
        return aw, h + 10

    def draw(self):
        c = self.canv
        h = self._ph + 10
        c.setFillColor(GREEN_LIGHT)
        c.setStrokeColor(colors.HexColor('#CFE3D6'))
        c.setLineWidth(0.6)
        c.roundRect(0, 0, self._w, h, 4, stroke=1, fill=1)
        c.setFillColor(GREEN)
        c.rect(0, 0, 3.2, h, stroke=0, fill=1)
        self.para.drawOn(c, 14, 5)


class Doc(BaseDocTemplate):
    """Doc template with running headers, split page numbering, TOC + outlines."""

    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, pagesize=A4,
                                 leftMargin=30 * mm, rightMargin=20 * mm,
                                 topMargin=23 * mm, bottomMargin=19 * mm,
                                 title='B.Tech CSE Summer Internship Report - SwachhAI',
                                 author='Mohammad Ramish Ansari',
                                 subject='1M1B AI for Sustainability Virtual Internship (AICTE / IBM SkillsBuild)',
                                 creator='University of Lucknow, Department of CSE', **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, TEXT_W, TEXT_H,
                      id='body', leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0)
        cover_frame = Frame(0, 0, A4[0], A4[1], id='cover',
                            leftPadding=0, rightPadding=0, topPadding=0,
                            bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[cover_frame], onPageEnd=self._page_end),
            PageTemplate(id='body', frames=[frame], onPage=self._page_start,
                         onPageEnd=self._page_end),
        ])
        self.chapter_of_page = {}
        self.current_chapter = None
        self.main_start_page = None      # absolute page where Chapter 1 begins
        self.show_numbers_from = 2       # cover page carries no number
        self._hb = 0

    # -- numbering helpers --------------------------------------------------
    @staticmethod
    def roman(n):
        vals = [(1000, 'm'), (900, 'cm'), (500, 'd'), (400, 'cd'), (100, 'c'),
                (90, 'xc'), (50, 'l'), (40, 'xl'), (10, 'x'), (9, 'ix'),
                (5, 'v'), (4, 'iv'), (1, 'i')]
        out = ''
        for v, s in vals:
            while n >= v:
                out += s
                n -= v
        return out

    def display_number(self, page):
        """Roman for preliminary pages, Arabic for the main report."""
        if self.main_start_page and page >= self.main_start_page:
            return str(page - self.main_start_page + 1)
        return self.roman(page)

    def toc_number(self, page):
        return self.display_number(page)

    # -- page furniture -----------------------------------------------------
    def _startBuild(self, *args, **kw):
        self.chapter_of_page = {}
        self.main_start_page = None
        self.current_chapter = None
        self._hb = 0
        return BaseDocTemplate._startBuild(self, *args, **kw)

    def _page_start(self, canvas, doc_t):
        pass

    def _header_title(self, page):
        if self.main_start_page and page < self.main_start_page:
            return 'Preliminary pages'
        best = None
        for p in sorted(self.chapter_of_page):
            if p <= page:
                best = self.chapter_of_page[p]
        return best or 'SwachhAI \u2014 AI-Guided Waste Segregation'

    def _page_end(self, canvas, doc_t):
        page = canvas.getPageNumber()
        if page < self.show_numbers_from:
            return
        canvas.saveState()
        w, h = A4
        # header
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.6)
        canvas.line(30 * mm, h - 16.6 * mm, w - 20 * mm, h - 16.6 * mm)
        canvas.setFont(BOLD, 8.5)
        canvas.setFillColor(GREEN)
        canvas.drawString(30 * mm, h - 15.1 * mm,
                          'SUMMER INTERNSHIP REPORT  \u00b7  2026')
        canvas.setFont(ITAL, 8.5)
        canvas.setFillColor(GREY)
        right = self._header_title(page)
        right = right[:1].upper() + right[1:]
        if stringWidth(right, ITAL, 8.5) > 92 * mm:
            right = right[:56].rstrip() + '\u2026'
        canvas.drawRightString(w - 20 * mm, h - 15.1 * mm, right)
        # footer
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.6)
        canvas.line(30 * mm, 14 * mm, w - 20 * mm, 14 * mm)
        canvas.setFont(BODY_FONT, 10)
        canvas.setFillColor(GREY)
        canvas.drawString(30 * mm, 9.6 * mm,
                          'Dept. of Computer Science & Engineering, University of Lucknow')
        canvas.setFont(BOLD, 10)
        canvas.setFillColor(NAVY)
        canvas.drawRightString(w - 20 * mm, 9.6 * mm, self.display_number(page))
        canvas.restoreState()

    # -- outline + TOC registration ----------------------------------------
    def afterFlowable(self, flowable):
        if isinstance(flowable, ChapterHead):
            self.current_chapter = flowable.title
            dest = key(flowable.title)
            self.canv.bookmarkPage(dest)
            self.canv.addOutlineEntry(flowable.title, dest, level=0, closed=False)
            if not flowable.number:
                label = flowable.title
            elif flowable.title.lower().startswith('appendix'):
                label = flowable.title
            else:
                label = 'Chapter %s  %s' % (flowable.number, flowable.title)
            self.notify('TOCEntry', (0, label, self.page, dest))
            self.chapter_of_page[self.page] = flowable.title
            if flowable.number == '1':
                self.main_start_page = self.page
            return
        if getattr(flowable, 'anchor_dest', None):
            self.canv.bookmarkPage(flowable.anchor_dest)
            if not getattr(flowable, 'skip_toc', False):
                text = _strip_tags(flowable.getPlainText())
                self.canv.addOutlineEntry(text, flowable.anchor_dest, level=1, closed=True)
                self.notify('TOCEntry', (0, text, self.page, flowable.anchor_dest))
            return
        if isinstance(flowable, Paragraph) and flowable.style.name in ('H1', 'H2', 'H3'):
            text = _strip_tags(flowable.getPlainText())
            level = {'H1': 0, 'H2': 1, 'H3': 2}[flowable.style.name]
            dest = key(text)
            self.canv.bookmarkPage(dest)
            self.canv.addOutlineEntry(text, dest, level=level + 1, closed=True)
            if level < 2:
                self.notify('TOCEntry', (level, text, self.page, dest))
            if flowable.style.name == 'H1':
                self.current_chapter = text
            return
        if isinstance(flowable, (Caption,)) or getattr(flowable, 'is_caption', False):
            self.canv.bookmarkPage(flowable.dest)
            self.notify(flowable.kind, (0, flowable.caption_text, self.page,
                                        flowable.dest))


# --------------------------------------------------------------------------
# Block builders
# --------------------------------------------------------------------------
def para(text, style='body'):
    return Paragraph(text, S[style])


def bullets(items, style='bul', bullet='\u2022'):
    return [Paragraph(t, S[style], bulletText=bullet) for t in items]


def numbered(items, style='num'):
    return [Paragraph(t, S[style], bulletText='%d.' % (i + 1))
            for i, t in enumerate(items)]


def chapter(number, title):
    return [PageBreak(), Spacer(1, 6), ChapterHead(number, title), Spacer(1, 12)]


def h2(text):
    return Paragraph(text, S['h2'])


def h3(text):
    return Paragraph(text, S['h3'])


def h1(text):
    return Paragraph(text, S['h1'])


def figure(path, caption, width=None, max_h=88 * mm):
    """Centred vector/raster figure with numbered caption."""
    from PIL import Image as PILImage
    img = PILImage.open(path)
    iw, ih = img.size
    w = width or TEXT_W
    h = w * ih / iw
    if h > max_h:
        h = max_h
        w = h * iw / ih
    flow = Image(path, width=w, height=h)
    flow.hAlign = 'CENTER'
    return [Spacer(1, 3), flow,
            Caption(caption, 'FIG', S['caption'])]


def table(spec):
    """spec: {caption, header, rows, widths (fractions), note, align}"""
    widths = [f * TEXT_W for f in spec['widths']]
    data = []
    head = [Paragraph(c, S['cellh']) for c in spec['header']]
    data.append(head)
    for row in spec['rows']:
        data.append([Paragraph(c, S['cell']) for c in row])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='CENTER')
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.45, RULE),
        ('LINEBELOW', (0, 0), (-1, 0), 0.8, NAVY),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F6F8FA')))
    if spec.get('firstbold'):
        style.append(('FONTNAME', (0, 1), (0, -1), BOLD))
    t.setStyle(TableStyle(style))
    out = [Caption(spec['caption'], 'TAB', S['caption_tab']), t]
    if spec.get('note'):
        out.append(Paragraph(spec['note'], S['note']))
    else:
        out.append(Spacer(1, 8))
    return out


def callout(text):
    return [Spacer(1, 4), Callout(Paragraph(text, S['callout'])), Spacer(1, 8)]


def make_toc():
    toc = TableOfContents()
    toc.levelStyles = [S['toch0'], S['toch1']]
    toc.dotsMinLevel = 0
    toc.tableStyle = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0.6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0.6),
    ])
    return toc


def make_index(kind, style=None):
    idx = TableOfContents(notifyKind=kind)
    idx.levelStyles = [style or S['toch1']]
    idx.dotsMinLevel = 0
    idx.tableStyle = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0.9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0.9),
    ])
    return idx


S['ref'] = ParagraphStyle('ref', fontName=BODY_FONT, fontSize=11, leading=14,
                          alignment=TA_JUSTIFY, leftIndent=26, firstLineIndent=-26,
                          spaceAfter=2, textColor=colors.black)
S['reflink'] = ParagraphStyle('reflink', fontName=BODY_FONT, fontSize=9.5, leading=12,
                              alignment=TA_LEFT, leftIndent=26, textColor=NAVY,
                              spaceAfter=5)
