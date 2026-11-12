# -*- coding: utf-8 -*-
"""Render the internship report to PDF with ReportLab.

Layout: A4, Times-compatible serif at 12 pt, single spacing, justified body
text, Roman numerals on preliminary pages and Arabic numerals on the main
report, 40 mm top margin for spiral binding clearance.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                Paragraph, Spacer, Image, Table, TableStyle,
                                PageBreak, KeepTogether, NextPageTemplate)
from reportlab.pdfgen import canvas as pdfcanvas

import content_front as F
import content_body as CB

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figures")
ASSETS = os.path.join(HERE, "assets")
OUTPDF = os.path.join(HERE, "..", "Summer_Internship_Report_Mayank_Kumar.pdf")

# ------------------------------------------------------------------ fonts
FONT, FONT_B, FONT_I, FONT_BI = "Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic"
try:
    base = os.path.join(HERE, "assets", "fonts")
    pdfmetrics.registerFont(TTFont("TNR", f"{base}/Tinos-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("TNR-B", f"{base}/Tinos-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("TNR-I", f"{base}/Tinos-Italic.ttf"))
    pdfmetrics.registerFont(TTFont("TNR-BI", f"{base}/Tinos-BoldItalic.ttf"))
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    registerFontFamily("TNR", normal="TNR", bold="TNR-B",
                       italic="TNR-I", boldItalic="TNR-BI")
    FONT, FONT_B, FONT_I, FONT_BI = "TNR", "TNR-B", "TNR-I", "TNR-BI"
except Exception as exc:      # pragma: no cover
    print("Liberation fonts unavailable, falling back to base-14:", exc)

MONO = "Courier"
try:
    pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
    MONO = "Mono"
except Exception:
    pass

PAGE_W, PAGE_H = A4
LM, RM, TM, BM = 32 * mm, 24 * mm, 32 * mm, 25 * mm
BODY_W = PAGE_W - LM - RM

# ----------------------------------------------------------------- styles
S = {}
S["body"] = ParagraphStyle("body", fontName=FONT, fontSize=12, leading=14.4,
                           alignment=TA_JUSTIFY, spaceAfter=6, spaceBefore=0,
                           firstLineIndent=0)
S["body_c"] = ParagraphStyle("body_c", parent=S["body"], alignment=TA_CENTER)
S["h1"] = ParagraphStyle("h1", fontName=FONT_B, fontSize=12, leading=14.4,
                         spaceBefore=10, spaceAfter=12, alignment=TA_LEFT)
S["h2"] = ParagraphStyle("h2", fontName=FONT_I, fontSize=12, leading=14.4,
                         spaceBefore=12, spaceAfter=7, alignment=TA_LEFT)
S["h3"] = ParagraphStyle("h3", fontName=FONT_BI, fontSize=12, leading=14.4,
                         spaceBefore=9, spaceAfter=5)
S["caption"] = ParagraphStyle("caption", fontName=FONT, fontSize=10,
                              leading=12, alignment=TA_CENTER,
                              spaceBefore=5, spaceAfter=12)
S["tcaption"] = ParagraphStyle("tcaption", fontName=FONT, fontSize=10,
                               leading=12, alignment=TA_CENTER,
                               spaceBefore=4, spaceAfter=5)
S["bullet"] = ParagraphStyle("bullet", parent=S["body"], leftIndent=16,
                             bulletIndent=4, spaceAfter=4)
S["code"] = ParagraphStyle("code", fontName=MONO, fontSize=8.4, leading=11,
                           alignment=TA_LEFT, spaceBefore=4, spaceAfter=10,
                           leftIndent=8, rightIndent=4)
S["ref"] = ParagraphStyle("ref", fontName=FONT, fontSize=11, leading=13.6,
                          alignment=TA_JUSTIFY, leftIndent=26,
                          firstLineIndent=-26, spaceAfter=7)
S["small"] = ParagraphStyle("small", fontName=FONT, fontSize=10, leading=12.5,
                            alignment=TA_JUSTIFY, spaceAfter=4)


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --------------------------------------------------------------- document
class Report(BaseDocTemplate):
    def __init__(self, fn):
        BaseDocTemplate.__init__(self, fn, pagesize=A4,
                                 leftMargin=LM, rightMargin=RM,
                                 topMargin=TM, bottomMargin=BM,
                                 title=F.TITLE, author=F.STUDENT,
                                 subject="B.Tech CSE Summer Internship Report")
        frame = Frame(LM, BM, BODY_W, PAGE_H - TM - BM, id="normal",
                      leftPadding=0, rightPadding=0, topPadding=0,
                      bottomPadding=0)
        roman = PageTemplate(id="roman", frames=[frame],
                             onPage=lambda c, d: self._deco(c, d, "roman"))
        arabic = PageTemplate(id="arabic", frames=[frame],
                              onPage=lambda c, d: self._deco(c, d, "arabic"))
        plain = PageTemplate(id="plain", frames=[frame],
                             onPage=lambda c, d: self._deco(c, d, "none"))
        self.addPageTemplates([plain, roman, arabic])
        self.anchors = {}
        self.coverpages = 1

    def _deco(self, canv, doc, kind):
        canv.saveState()
        canv.setFont(FONT, 10.5)
        tail = "Summer Internship Report  |  " + F.STUDENT
        if kind == "roman":
            canv.drawCentredString(PAGE_W / 2, 15 * mm, doc.roman(doc.page))
            canv.setFont(FONT, 8.5)
            canv.drawCentredString(PAGE_W / 2, PAGE_H - 18 * mm, tail)
        elif kind == "arabic":
            canv.drawCentredString(PAGE_W / 2, 15 * mm, str(doc.mainpage))
            canv.setFont(FONT, 8.5)
            canv.drawCentredString(PAGE_W / 2, PAGE_H - 18 * mm, tail)
        canv.restoreState()

    # page counters -------------------------------------------------------
    def afterFlowable(self, flowable):
        key = getattr(flowable, "_anchor_key", None)
        if key is not None:
            self.anchors.setdefault(key, self.page)


def _roman(n):
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"),
            (90, "xc"), (50, "l"), (40, "xl"), (10, "x"), (9, "ix"),
            (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


class Report2(Report):
    def roman(self, p):
        return _roman(p)

    def _deco(self, canv, doc, kind):
        mp = getattr(doc, "mainpage", None)
        if kind == "arabic" and mp is None:
            kind = "roman"
        if kind == "roman" and mp is not None and self.page >= mp:
            kind = "arabic"
        Report._deco(self, canv, doc, kind)
        return

    def _deco_orig(self, *a, **k):
        pass


def arabic_number(doc, page):
    mp = getattr(doc, "mainpage", 10 ** 6)
    if page >= mp:
        return str(page - mp + 1)
    return _roman(page - doc.coverpages)


# patch numbering helpers
def _fix_deco(self, canv, doc, kind):
    canv.saveState()
    canv.setFont(FONT, 10.5)
    if doc.page > doc.coverpages:
        canv.drawCentredString(PAGE_W / 2, 15 * mm,
                              arabic_number(doc, doc.page))
    canv.setFont(FONT, 8.5)
    if doc.page > doc.coverpages:
        canv.drawCentredString(PAGE_W / 2, PAGE_H - 18 * mm,
                              "Summer Internship Report  |  " + F.STUDENT)
    canv.restoreState()


# ------------------------------------------------------------- builders
def cover_page():
    """Cover page exactly in the format prescribed by the department."""
    el = []
    st = lambda **kw: ParagraphStyle("c", fontName=kw.get("f", FONT_B),
                                     fontSize=kw.get("s", 14),
                                     leading=kw.get("s", 14) * 1.35,
                                     alignment=TA_CENTER)
    el.append(Spacer(1, 4 * mm))
    el.append(Paragraph("INDUSTRIAL TRAINING REPORT", st(s=17)))
    el.append(Spacer(1, 5 * mm))
    el.append(Paragraph("on", st(f=FONT_I, s=13)))
    el.append(Spacer(1, 4 * mm))
    el.append(Paragraph("\u201c" + esc(F.TITLE_COVER) + "\u201d", st(s=14)))
    el.append(Spacer(1, 7 * mm))
    el.append(Paragraph("by", st(f=FONT_I, s=13)))
    el.append(Spacer(1, 3 * mm))
    el.append(Paragraph(esc(F.STUDENT), st(f=FONT_B, s=14)))
    el.append(Spacer(1, 1.5 * mm))
    el.append(Paragraph("Roll No. " + esc(F.ROLL), st(f=FONT, s=12)))
    el.append(Spacer(1, 9 * mm))
    el.append(Paragraph("Submitted on Partial Fulfilment of the Requirements "
                        "for the award of the Degree", st(f=FONT, s=12)))
    el.append(Spacer(1, 3 * mm))
    el.append(Paragraph("of", st(f=FONT_I, s=12)))
    el.append(Spacer(1, 3 * mm))
    el.append(Paragraph("BACHELOR OF TECHNOLOGY", st(s=15)))
    el.append(Spacer(1, 2 * mm))
    el.append(Paragraph("in", st(f=FONT_I, s=12)))
    el.append(Spacer(1, 2 * mm))
    el.append(Paragraph("COMPUTER SCIENCE &amp; ENGINEERING", st(s=15)))
    el.append(Spacer(1, 6 * mm))
    el.append(Paragraph("from", st(f=FONT_I, s=12)))
    el.append(Spacer(1, 3 * mm))
    el.append(Paragraph(esc(F.ORG), st(s=13)))
    el.append(Spacer(1, 12 * mm))
    el.append(Paragraph("Submitted to", st(f=FONT_I, s=12)))
    el.append(Spacer(1, 4 * mm))
    el.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING",
                        st(s=13)))
    el.append(Spacer(1, 2 * mm))
    el.append(Paragraph(F.FACULTY, st(s=12)))
    el.append(Spacer(1, 2 * mm))
    el.append(Paragraph(F.UNIV, st(s=12)))
    el.append(Spacer(1, 10 * mm))
    el.append(Paragraph(F.MONTH_YEAR, st(f=FONT_B, s=12)))
    return el


def declaration():
    el = [Paragraph("DECLARATION", ParagraphStyle(
        "d", fontName=FONT_B, fontSize=14, alignment=TA_CENTER,
        spaceAfter=18))]
    for t in F.DECLARATION:
        el.append(Paragraph(esc(t), S["body"]))
    el.append(Spacer(1, 26 * mm))
    el.append(Paragraph("Date: ....................            "
                        "Place: Lucknow", S["body"]))
    el.append(Spacer(1, 20 * mm))
    el.append(Paragraph("( " + esc(F.STUDENT) + " )", ParagraphStyle(
        "sg", fontName=FONT_B, fontSize=12, alignment=TA_RIGHT)))
    el.append(Paragraph("B.Tech CSE, 3rd Year", ParagraphStyle(
        "sg2", fontName=FONT, fontSize=12, alignment=TA_RIGHT)))
    el.append(Paragraph("Roll No. " + esc(F.ROLL), ParagraphStyle(
        "sg3", fontName=FONT, fontSize=12, alignment=TA_RIGHT)))
    return el


def certificate_page():
    el = [Paragraph("INTERNSHIP COMPLETION CERTIFICATE",
                    ParagraphStyle("cc", fontName=FONT_B, fontSize=14,
                                   alignment=TA_CENTER, spaceAfter=10))]
    el.append(Paragraph(esc(F.CERT_NOTE), S["body"]))
    el.append(Spacer(1, 4 * mm))
    path = os.path.join(ASSETS, "certificate.png")
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    w = BODY_W
    h = w * ih / iw
    el.append(Image(path, width=w, height=h))
    return el


def render_toc(entries):
    el = [Paragraph("TABLE OF CONTENTS", ParagraphStyle(
        "t", fontName=FONT_B, fontSize=14, alignment=TA_CENTER,
        spaceAfter=14))]
    rows = []
    for kind, text, page in entries:
        if kind == "h1":
            style = ParagraphStyle("toc1", fontName=FONT_B, fontSize=11,
                                   leading=13.5, spaceBefore=7)
            rows.append([Paragraph(esc(text), style),
                         Paragraph(str(page), ParagraphStyle(
                             "tocp", fontName=FONT_B, fontSize=11,
                             alignment=TA_RIGHT))])
        elif kind == "h2":
            style = ParagraphStyle("toc2", fontName=FONT, fontSize=10.5,
                                   leading=12.8, leftIndent=14)
            rows.append([Paragraph(esc(text), style),
                         Paragraph(str(page), ParagraphStyle(
                             "tocp2", fontName=FONT, fontSize=10.5,
                             alignment=TA_RIGHT))])
        else:
            style = ParagraphStyle("toc3", fontName=FONT_I, fontSize=10.5,
                                   leading=12.8, leftIndent=26)
            rows.append([Paragraph(esc(text), style),
                         Paragraph(str(page), ParagraphStyle(
                             "tocp3", fontName=FONT_I, fontSize=10.5,
                             alignment=TA_RIGHT))])
    t = Table(rows, colWidths=[BODY_W - 22 * mm, 22 * mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 1),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    el.append(t)
    return el


def render_list(title, entries):
    el = [Paragraph(title, ParagraphStyle(
        "l", fontName=FONT_B, fontSize=14, alignment=TA_CENTER,
        spaceAfter=14))]
    rows = []
    for text, page in entries:
        rows.append([Paragraph(esc(text), ParagraphStyle(
            "li", fontName=FONT, fontSize=10.5, leading=13)),
            Paragraph(str(page), ParagraphStyle(
                "lip", fontName=FONT, fontSize=10.5, alignment=TA_RIGHT))])
    t = Table(rows, colWidths=[BODY_W - 18 * mm, 18 * mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                           ("LINEBELOW", (0, 0), (-1, -2), 0.25,
                            colors.HexColor("#D9D9D9"))]))
    el.append(t)
    return el


def figure_block(fname, caption, width_in):
    path = os.path.join(FIGDIR, fname)
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    w = min(width_in * inch, BODY_W)
    h = w * ih / iw
    maxh = PAGE_H - TM - BM - 40 * mm
    if h > maxh:
        h = maxh
        w = h * iw / ih
    return KeepTogether([Image(path, width=w, height=h),
                         Paragraph(esc(caption), S["caption"])])


def table_block(caption, header, rows, widths, align, fontsize):
    csz = fontsize or 9
    cell = ParagraphStyle("tc", fontName=FONT, fontSize=csz,
                          leading=csz * 1.22)
    cellb = ParagraphStyle("tcb", fontName=FONT_B, fontSize=csz,
                           leading=csz * 1.22, alignment=TA_CENTER)
    hdr_b = ParagraphStyle("th", fontName=FONT_B, fontSize=csz,
                           leading=csz * 1.22, alignment=TA_CENTER)
    amap = {"l": TA_LEFT, "c": TA_CENTER, "r": TA_RIGHT}
    data = [[Paragraph(esc(h), hdr_b) for h in header]]
    for r in rows:
        line = []
        for i, c in enumerate(r):
            a = amap[(align[i] if align and i < len(align) else "l")]
            line.append(Paragraph(esc(c), ParagraphStyle(
                "tcc", parent=cell, alignment=a)))
        data.append(line)
    if widths:
        cw = [w * inch for w in widths]
        scale = BODY_W / sum(cw)
        cw = [w * scale for w in cw]
    else:
        cw = [BODY_W / len(header)] * len(header)
    t = Table(data, colWidths=cw, repeatRows=1, hAlign="CENTER")
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#7F7F7F")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return [Paragraph(esc(caption), S["tcaption"]), t]


def build(pages=None, outfile=None, main_start=None):
    pages = pages or {}
    doc = Report2(outfile or OUTPDF)
    doc.mainpage = main_start if main_start else 10 ** 6
    story = []

    # ---- cover (no number)
    story += cover_page()
    story.append(NextPageTemplate("roman"))
    story.append(PageBreak())

    # ---- preliminary pages
    story += declaration()
    story.append(PageBreak())
    story += certificate_page()
    story.append(PageBreak())

    story.append(Paragraph("ABSTRACT", ParagraphStyle(
        "a", fontName=FONT_B, fontSize=14, alignment=TA_CENTER,
        spaceAfter=14)))
    for t in F.ABSTRACT:
        story.append(Paragraph(esc(t), S["body"]))
    story.append(PageBreak())

    story.append(Paragraph("ACKNOWLEDGEMENT", ParagraphStyle(
        "ak", fontName=FONT_B, fontSize=14, alignment=TA_CENTER,
        spaceAfter=14)))
    for t in F.ACK:
        story.append(Paragraph(esc(t), S["body"]))
    story.append(PageBreak())

    story += render_toc(CB.toc_entries(pages))
    story.append(PageBreak())
    story += render_list("LIST OF TABLES", CB.tables_list(pages))
    story.append(PageBreak())
    story += render_list("LIST OF FIGURES", CB.figures_list(pages))
    story.append(PageBreak())
    story.append(NextPageTemplate("arabic"))

    # ---- main body
    first_h1_done = [False]
    body = CB.B
    prev = [None]
    for b in body:
        k = b[0]
        if k == "pagebreak":
            story.append(PageBreak())
        elif k == "h1":
            if first_h1_done[0] and prev[0] != "pagebreak":
                story.append(PageBreak())
            first_h1_done[0] = True
            para = Paragraph(esc(b[1]), S["h1"])
            para._anchor_key = b[1]
            story.append(para)
        elif k in ("h2", "h3"):
            para = Paragraph(esc(b[1]), S[k])
            para._anchor_key = b[1]
            story.append(para)
        elif k == "p":
            story.append(Paragraph(esc(b[1]), S["body"]))
        elif k == "pc":
            story.append(Paragraph(esc(b[1]), S["body_c"]))
        elif k == "bullet":
            story.append(Paragraph("&bull;", S["bullet"]) if False else
                         Paragraph(esc(b[1]), S["bullet"],
                                   bulletText="\u2022"))
        elif k == "num":
            story.append(Paragraph(esc(b[1]), S["bullet"], bulletText="\u2013"))
        elif k == "code":
            lines = b[1].split("\n")
            pre = Paragraph("<br/>".join(
                esc(l).replace(" ", "&nbsp;") for l in lines), S["code"])
            box = Table([[pre]], colWidths=[BODY_W])
            box.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F2F2")),
                ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
            story.append(box)
            story.append(Spacer(1, 8))
        elif k == "fig":
            blk = figure_block(b[1], b[2], b[3])
            blk._anchor_key = b[2]
            story.append(blk)
        elif k == "table":
            blk = table_block(b[1], b[2], b[3], b[4], b[5], b[6])
            blk[0]._anchor_key = b[1]
            story += blk
            story.append(Spacer(1, 6))
        elif k == "ref":
            story.append(Paragraph(
                "<b>" + esc(b[1]) + "</b>&nbsp;&nbsp;" + esc(b[2]),
                S["ref"]))
        else:
            raise ValueError(k)
        prev[0] = k

    # patch decorative numbering
    Report2._deco = _fix_deco
    doc.build(story)
    return doc


def _label(doc, phys_page):
    """Page label printed on a physical page (1-based)."""
    mp = getattr(doc, "mainpage", 10 ** 6)
    if mp > 10 ** 5:
        mp = doc.page
    if phys_page >= mp:
        return str(phys_page - mp + 1)
    return _roman(phys_page - doc.coverpages)


def _start_page(doc, key):
    p = doc.anchors.get(key)
    if p is None:
        return ""
    return _label(doc, p)


def _norm(t):
    return " ".join(t.split())


def _page_labels(n_pages, main_start):
    """Physical page number -> printed label."""
    out = {}
    for p in range(1, n_pages + 1):
        if p >= main_start:
            out[p] = str(p - main_start + 1)
        else:
            out[p] = _roman(p - 1)
    return out


def _detect_main_start(path):
    import pymupdf
    d = pymupdf.open(path)
    texts = [_norm(d[i].get_text()) for i in range(len(d))]
    first_h1 = next(b[1] for b in CB.B if b[0] == "h1")
    target = _norm(first_h1)
    for i, t in enumerate(texts):
        if target in t and "TABLE OF CONTENTS" not in t:
            return i + 1, len(d)
    return 20, len(d)


def _page_map(path, main_start):
    """Maplabel text -> printed page label, by searching the built PDF."""
    import pymupdf
    d = pymupdf.open(path)
    texts = [_norm(d[i].get_text()) for i in range(len(d))]
    labels = _page_labels(len(texts), main_start)

    def find(key):
        k = _norm(key)
        for i in range(main_start - 1, len(texts)):
            if k in texts[i]:
                return labels[i + 1]
        return ""

    pages = {}
    for b in CB.B:
        if b[0] in ("h1", "h2"):
            pages[b[1]] = find(b[1])
        elif b[0] == "fig":
            pages[b[2]] = find(b[2])
        elif b[0] == "table":
            pages[b[1]] = find(b[1])
    return pages, len(texts)


def build_all():
    tmp = OUTPDF + ".pass1.pdf"
    build({}, tmp)
    main_start, _n = _detect_main_start(tmp)
    os.remove(tmp)

    pages = {}
    prev_ms = None
    for attempt in range(5):
        build(pages, OUTPDF, main_start=main_start)
        ms, _n = _detect_main_start(OUTPDF)
        newpages, npages = _page_map(OUTPDF, ms)
        if ms == prev_ms and newpages == pages:
            break
        prev_ms, main_start, pages = ms, ms, newpages
    import json
    with open(os.path.join(HERE, "pages.json"), "w") as fh:
        json.dump(pages, fh, indent=1, ensure_ascii=False)
    print("PDF written:", os.path.abspath(OUTPDF),
          "| pages:", npages, "| body starts at physical page", main_start)


if __name__ == "__main__":
    build_all()
