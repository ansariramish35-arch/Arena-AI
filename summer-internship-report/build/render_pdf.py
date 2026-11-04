"""Render the report to PDF (print-ready, single-sided, A4, spiral-bound)."""
import os
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (CondPageBreak, Flowable, Image, KeepTogether,
                                NextPageTemplate, PageBreak, Paragraph, Spacer,
                                Table, TableStyle)

import reportkit as rk
from reportkit import (BOLD, GREEN, GREEN_LIGHT, GREY, ITAL, NAVY, NAVY_DARK, RULE,
                       S, TEXT_W, Callout, Caption, ChapterHead)
import model
from model import K

from content_front import FRONT
from content_main import CH1, CH2, CH3, CH4, CH5
from content_main2 import CH6, CH7
from content_main3 import CH8, CH9, CH10, APPENDIX, EVIDENCE, REFERENCES

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'B.Tech_CSE_Summer_Internship_Report_SwachhAI.pdf')


# --------------------------------------------------------------------------
# Extra flowables
# --------------------------------------------------------------------------
class FrontHead(Paragraph):
    """Centred preliminary-page heading; bookmarked but kept out of the TOC."""

    def __init__(self, text):
        self.anchor_dest = K(text)
        self.skip_toc = True
        Paragraph.__init__(self, text, S['h1_front'])


class Spacer2(Spacer):
    pass


class SignatureBlock(Flowable):
    def __init__(self, rows, width=TEXT_W):
        Flowable.__init__(self)
        self.rows = rows
        self._w = width

    def wrap(self, aw, ah):
        self._w = aw
        self._h = 14 * len(self.rows) + 6
        return aw, self._h

    def draw(self):
        c = self.canv
        y = self._h - 12
        for left, right in self.rows:
            c.setFont('Times-Roman', 12)
            if left:
                c.drawString(0, y, left)
            if right:
                c.drawRightString(self._w, y, right)
            y -= 14


class RefItem(Paragraph):
    """A numbered reference; anchors #refN for in-text citation links."""

    def __init__(self, num, text):
        self.num = num
        self.anchor_dest = 'ref%d' % num
        self.skip_toc = True
        Paragraph.__init__(self, '<b>[%d]</b>&nbsp;&nbsp;%s' % (num, text), S['ref'])


class LinkRow(Paragraph):
    def __init__(self, url, style=None):
        Paragraph.__init__(self, '<link href="%s" color="#123A63">%s</link>' % (url, url),
                           style or S['reflink'])


class CoverPage(Flowable):
    """Full-page institutional cover in the prescribed B.Tech format."""

    def wrap(self, aw, ah):
        return aw, ah

    def draw(self):
        c = self.canv
        w, h = A4
        lm = 26 * mm
        rm = w - 22 * mm
        top = h - 24 * mm

        c.setStrokeColor(NAVY)
        c.setLineWidth(1.6)
        c.rect(12 * mm, 12 * mm, w - 24 * mm, h - 24 * mm)
        c.setStrokeColor(GREEN)
        c.setLineWidth(0.7)
        c.rect(15 * mm, 15 * mm, w - 30 * mm, h - 30 * mm)

        cx = w / 2
        y = top

        c.setFillColor(NAVY_DARK)
        c.setFont(BOLD, 16)
        c.drawCentredString(cx, y, 'UNIVERSITY OF LUCKNOW')
        y -= 19
        c.setFont(BOLD, 11.5)
        c.drawCentredString(cx, y, 'LUCKNOW \u2014 226 021, UTTAR PRADESH')
        y -= 17
        c.setFont(BOLD, 10.5)
        c.setFillColor(GREEN)
        c.drawCentredString(cx, y, 'DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING')
        y -= 13
        c.setStrokeColor(GREEN)
        c.setLineWidth(0.8)
        c.line(lm + 6, y, rm - 6, y)

        y -= 40
        c.setFillColor(GREY)
        c.setFont(BOLD, 10.5)
        c.drawCentredString(cx, y, 'A REPORT ON SUMMER INTERNSHIP')
        y -= 15
        c.setFont(ITAL, 10.5)
        c.drawCentredString(cx, y, '(Session 2025\u201326)')

        y -= 34
        c.setFillColor(NAVY_DARK)
        c.setFont(BOLD, 22)
        c.drawCentredString(cx, y, 'SwachhAI')
        y -= 22
        c.setFont(ITAL, 12.5)
        c.setFillColor(GREEN)
        c.drawCentredString(cx, y, 'AI-Guided Waste Segregation and Circularity Assistant')
        y -= 16
        c.drawCentredString(cx, y, 'for India\u2019s Households')

        y -= 30
        c.setFillColor(GREY)
        c.setFont(BOLD, 9.8)
        c.drawCentredString(cx, y, 'Submitted in partial fulfilment of the requirements for the '
                                   'award of the degree of')
        y -= 19
        c.setFillColor(NAVY_DARK)
        c.setFont(BOLD, 13)
        c.drawCentredString(cx, y, 'BACHELOR OF TECHNOLOGY')
        y -= 16
        c.setFont(ITAL, 11)
        c.drawCentredString(cx, y, 'in')
        y -= 16
        c.setFont(BOLD, 13)
        c.drawCentredString(cx, y, 'COMPUTER SCIENCE AND ENGINEERING')

        y -= 38
        c.setFillColor(GREY)
        c.setFont(BOLD, 9.8)
        c.drawCentredString(cx, y, 'SUBMITTED BY')
        y -= 18
        c.setFillColor(NAVY_DARK)
        c.setFont(BOLD, 13.5)
        c.drawCentredString(cx, y, 'MOHAMMAD RAMISH ANSARI')
        y -= 15
        c.setFont('Times-Roman', 10.5)
        c.drawCentredString(cx, y, 'B.Tech. Computer Science and Engineering')
        y -= 13.5
        c.drawCentredString(cx, y, 'Third Year, Semester V')
        y -= 13.5
        c.drawCentredString(cx, y, 'University Roll No.: ____________________')

        y -= 30
        c.setFillColor(GREY)
        c.setFont(BOLD, 9.8)
        c.drawCentredString(cx, y, 'UNDER THE SUPERVISION OF')
        y -= 16
        c.setFillColor(NAVY_DARK)
        c.setFont('Times-Roman', 10.5)
        c.drawCentredString(cx, y, '____________________  (Faculty Supervisor)')
        y -= 13.5
        c.drawCentredString(cx, y, 'Department of Computer Science and Engineering')

        # internship band
        bh = 54
        by = y - 28 - bh
        c.setFillColor(GREEN_LIGHT)
        c.setStrokeColor(GREEN)
        c.setLineWidth(0.7)
        c.roundRect(lm + 2, by, rm - lm - 4, bh, 3, stroke=1, fill=1)
        c.setFillColor(GREEN)
        c.setFont(BOLD, 8.6)
        c.drawCentredString(cx, by + bh - 14, 'INTERNSHIP COMPLETED AT')
        c.setFillColor(NAVY_DARK)
        c.setFont(BOLD, 11)
        c.drawCentredString(cx, by + bh - 27, '1M1B (One Million for One Billion)')
        c.setFont('Times-Roman', 8.8)
        c.setFillColor(GREY)
        c.drawCentredString(cx, by + bh - 38, 'AI for Sustainability Virtual Internship  \u00b7  '
                                              'supported by AICTE  \u00b7  in collaboration with '
                                              'IBM SkillsBuild')
        c.drawCentredString(cx, by + 9, 'Certified completion period: July 2026 \u2013 September '
                                        '2026  \u00b7  Certificate issued 22 September 2026')

        # footer
        c.setFillColor(NAVY_DARK)
        c.setFont(BOLD, 10)
        c.drawCentredString(cx, 26 * mm, 'SESSION 2025\u201326')
        c.setFont('Times-Roman', 8.4)
        c.setFillColor(GREY)
        c.drawCentredString(cx, 20 * mm, 'Spiral bound  \u00b7  single-sided printing  \u00b7  '
                                         'submitted for university evaluation')


# --------------------------------------------------------------------------
# Story assembly
# --------------------------------------------------------------------------
def numbered_figure(path, caption, width_frac=1.0):
    if os.path.isabs(path):
        full = path
    else:
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            full = os.path.join(ROOT, 'images', path)
    imgs = rk.figure(full, caption, width=TEXT_W * width_frac, max_h=86 * mm)
    return [CondPageBreak(imgs[1].drawHeight + 26 * mm)] + imgs


def build_story():
    story = []
    nfig = 0
    ntab = 0

    def emit(block):
        nonlocal nfig, ntab
        kind = block[0]
        if kind == 'cover':
            story.append(NextPageTemplate('body'))
            story.append(CoverPage())
            return
        if kind == 'pagebreak':
            story.append(PageBreak())
            return
        if kind == 'spacer':
            story.append(Spacer(1, block[1]))
            return
        if kind == 'h1_front':
            story.append(Spacer(1, 4))
            story.append(FrontHead(block[1]))
            story.append(rk.Rule(color=GREEN, space_after=12))
            return
        if kind == 'h1':
            story.append(CondPageBreak(90))
            story.append(Paragraph(block[1], S['h1']))
            story.append(rk.Rule(thickness=0.6, color=colors.HexColor('#C7D2DC'),
                                 space_before=0, space_after=7))
            return
        if kind == 'h2':
            story.append(CondPageBreak(80))
            story.append(Paragraph(block[1], S['h2']))
            return
        if kind == 'p':
            story.append(Paragraph(block[1], S['body']))
            return
        if kind == 'quote':
            story.append(Paragraph(block[1], S['quote']))
            return
        if kind == 'bullets':
            story.extend(rk.bullets(block[1]))
            story.append(Spacer(1, 5))
            return
        if kind == 'numbered':
            story.extend(rk.numbered(block[1]))
            story.append(Spacer(1, 5))
            return
        if kind == 'callout':
            story.append(Callout(Paragraph(block[1], S['callout'])))
            story.append(Spacer(1, 9))
            return
        if kind == 'sigblock':
            story.append(SignatureBlock(block[1]))
            return
        if kind == 'toc':
            story.append(rk.make_toc())
            return
        if kind == 'lot':
            story.append(rk.make_index('TAB'))
            return
        if kind == 'lof':
            story.append(rk.make_index('FIG'))
            return
        if kind == 'certpage':
            for path, caption in block[1]:
                story.extend(numbered_figure(path, caption, 0.66))
            return
        if kind == 'figure':
            path, caption = block[1], block[2]
            frac = block[3] / 100.0 if len(block) > 3 else 1.0
            story.extend(numbered_figure(path, caption, frac))
            return
        if kind == 'table':
            spec = dict(block[1])
            key = spec.pop('key')
            spec['caption'] = model.TABSPEC(None, key)
            story.extend(rk.table(spec))
            story.append(Spacer(1, 4))
            return
        if kind == 'chapter':
            story.extend(rk.chapter(block[1], block[2]))
            return
        if kind == 'refs':
            for num, text, url in block[1]:
                story.append(RefItem(num, text))
                if url:
                    story.append(LinkRow(url))
                story.append(Spacer(1, 3))
            return
        raise ValueError('unknown block %r' % (kind,))

    for block in FRONT:
        emit(block)

    for chapter in (CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10):
        for block in chapter:
            emit(block)

    # references
    story.append(PageBreak())
    story.append(ChapterHead('', 'References and Bibliography'))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        'The list below contains only sources that were actually consulted and that support '
        'statements made in this report. Publication details and web addresses were verified before '
        'inclusion. Where a document has been amended since notification, the principal notification '
        'is cited and the amendment is named in the text.', S['body']))
    story.append(Paragraph(
        'Items [1] to [9] are the primary sources for the published statistics and rules used in '
        'Chapters 5 to 8. Items [10] to [16] support the technology and programme descriptions. '
        'Item [17] and [18] are the standard references for retrieval-augmented generation and the '
        'transformer architecture. Item [19] is the university guideline followed for formatting. '
        'Item [20] is the project document submitted during the internship; it is not publicly '
        'available and is cited for internal traceability only.', S['body']))
    story.append(Spacer(1, 6))
    emit(('refs', REFERENCES))
    story.append(Spacer(1, 10))
    story.append(Paragraph('<b>A note on citation practice.</b> Numerical citations in the text '
                           'refer to this list and are clickable in the digital edition. Statistics '
                           'are given with their reporting year, because several of the figures in '
                           'this area change annually. No source has been cited that was not '
                           'consulted, and no reference has been included to lengthen the list.',
                           S['body']))

    for block in APPENDIX:
        if block[0] == 'chapter':
            story.append(PageBreak())
            story.append(ChapterHead(block[1], block[2]))
            story.append(Spacer(1, 12))
        else:
            emit(block)

    return story


def main():
    doc = rk.Doc(OUT)
    # preliminary-page numbering and TOC formatting
    story = build_story()

    def fmt(page):
        return doc.display_number(page)

    for flow in story:
        if hasattr(flow, 'formatter'):
            flow.formatter = fmt

    doc.multiBuild(story)
    print('written', OUT)


if __name__ == '__main__':
    main()
