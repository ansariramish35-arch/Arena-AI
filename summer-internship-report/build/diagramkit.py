"""Vector diagram and mock-up generator for the internship report.

Every diagram is drawn with reportlab's graphics toolkit (crisp, type-set in
Times) and rasterised at 300 dpi into images/ for embedding in both the PDF and
the DOCX edition.
"""
import os

from reportlab.graphics.shapes import (Drawing, Group, Line, Polygon, Rect,
                                       String, Circle, Wedge, Ellipse)
from reportlab.graphics.shapes import Line as _Line
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase.pdfmetrics import stringWidth
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(os.path.dirname(HERE), 'images')
os.makedirs(IMGDIR, exist_ok=True)

NAVY = HexColor('#123A63')
NAVY_D = HexColor('#0B2440')
GREEN = HexColor('#1E6B4F')
GREEN_L = HexColor('#E8F3EC')
GREEN_M = HexColor('#4E8F72')
SAND = HexColor('#F4EEE2')
BLUE_L = HexColor('#E7EEF7')
GREY = HexColor('#5A5A5A')
GREY_L = HexColor('#F1F3F5')
RULE = HexColor('#B9C6D2')
ORANGE = HexColor('#B5651D')
RED = HexColor('#9B2C2C')

F = 'Times-Roman'
FB = 'Times-Bold'
FI = 'Times-Italic'


class Canvas:
    """Tiny drawing helper: top-left origin, points, wrapped text boxes."""

    def __init__(self, w, h, bg=white):
        self.d = Drawing(w, h)
        self.w, self.h = w, h
        if bg is not None:
            self.d.add(Rect(0, 0, w, h, fillColor=bg, strokeColor=None))

    def _y(self, y):
        """Convert top-based y to reportlab bottom-based y."""
        return self.h - y

    # -- primitives ---------------------------------------------------------
    def rect(self, x, y, w, h, fill=None, stroke=NAVY, lw=0.9, radius=None, dash=None):
        kwargs = dict(fillColor=fill, strokeColor=stroke, strokeWidth=lw)
        if dash:
            kwargs['strokeDashArray'] = dash
        if radius:
            self.d.add(Rect(x, self._y(y + h), w, h, rx=radius, ry=radius, **kwargs))
        else:
            self.d.add(Rect(x, self._y(y + h), w, h, **kwargs))

    def line(self, x1, y1, x2, y2, color=NAVY, lw=0.9, dash=None):
        ln = Line(x1, self._y(y1), x2, self._y(y2),
                  strokeColor=color, strokeWidth=lw)
        if dash:
            ln.strokeDashArray = dash
        self.d.add(ln)

    def arrow(self, x1, y1, x2, y2, color=NAVY, lw=1.0, head=5.2, both=False,
              dash=None):
        import math
        self.line(x1, y1, x2, y2, color, lw, dash)
        ang = math.atan2(y2 - y1, x2 - x1)
        self._head(x2, y2, ang, color, head)
        if both:
            self._head(x1, y1, ang + math.pi, color, head)

    def _head(self, x, y, ang, color, size):
        import math
        a1, a2 = ang + 2.6, ang - 2.6
        p = [x, self._y(y),
             x - size * math.cos(a1) * 1.05, self._y(y - size * math.sin(a1) * 1.05) - 0,
             x - size * math.cos(a2) * 1.05, self._y(y - size * math.sin(a2) * 1.05)]
        # build in screen coords then flip
        pts = []
        pts += [x, self._y(y)]
        for a in (a1, a2):
            pts += [x - size * math.cos(a), self._y(y - size * math.sin(a))]
        self.d.add(Polygon(pts, fillColor=color, strokeColor=color, strokeWidth=0.4))

    FS = 1.12

    def text(self, x, y, s, size=9, font=F, color=NAVY_D, align='left'):
        size = size * self.FS
        if align == 'center':
            tw = stringWidth(s, font, size)
            self.d.add(String(x - tw / 2, self._y(y), s, fontName=font,
                              fontSize=size, fillColor=color))
        elif align == 'right':
            tw = stringWidth(s, font, size)
            self.d.add(String(x - tw, self._y(y), s, fontName=font,
                              fontSize=size, fillColor=color))
        else:
            self.d.add(String(x, self._y(y), s, fontName=font,
                              fontSize=size, fillColor=color))

    def wrap(self, x, y, w, text, size=9, font=F, color=NAVY_D, leading=11.4,
             align='left', max_lines=None):
        """Draw wrapped text; y is the top of the first baseline block."""
        size = size * self.FS
        leading = leading * self.FS
        words = text.split()
        lines, cur = [], ''
        for word in words:
            trial = (cur + ' ' + word).strip()
            if stringWidth(trial, font, size) <= w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        if max_lines:
            lines = lines[:max_lines]
        for i, ln in enumerate(lines):
            ty = y + size * 0.82 + i * leading
            if align == 'center':
                self.text(x + w / 2, ty, ln, size, font, color, 'center')
            elif align == 'right':
                self.text(x + w, ty, ln, size, font, color, 'right')
            else:
                self.text(x, ty, ln, size, font, color)
        return len(lines) * leading

    def para_size(self, w, text, size=9, font=F, leading=11.4):
        size = size * self.FS
        leading = leading * self.FS
        words = text.split()
        lines, cur = [], ''
        for word in words:
            trial = (cur + ' ' + word).strip()
            if stringWidth(trial, font, size) <= w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return len(lines) * leading

    def card(self, x, y, w, h, title, body='', fill=BLUE_L, stroke=NAVY,
             title_size=9.5, body_size=8.4, pad=7, tcolor=NAVY_D, dash=None):
        self.rect(x, y, w, h, fill=fill, stroke=stroke, lw=1.0, radius=3, dash=dash)
        th = self.wrap(x + pad, y + pad - 2, w - 2 * pad, title, title_size, FB,
                       tcolor, leading=title_size * 1.25)
        if body:
            self.wrap(x + pad, y + pad + th + 1, w - 2 * pad, body, body_size, F,
                      GREY, leading=body_size * 1.3)

    def band(self, x, y, w, h, label, sub='', fill=NAVY, tcolor=white):
        self.rect(x, y, w, h, fill=fill, stroke=None, radius=3)
        self.text(x + 8, y + h / 2 - 1, label, 9.5, FB, tcolor)
        if sub:
            self.text(x + 8, y + h / 2 + 10, sub, 7.6, F, HexColor('#DCE6F0'))

    def diamond(self, cx, cy, w, h, text, fill=SAND, stroke=ORANGE, size=8.2):
        pts = [cx, self._y(cy - h / 2), cx + w / 2, self._y(cy),
               cx, self._y(cy + h / 2), cx - w / 2, self._y(cy)]
        self.d.add(Polygon(pts, fillColor=fill, strokeColor=stroke, strokeWidth=0.9))
        self.wrap(cx - w / 2 + 6, cy - h / 2 + 4, w - 12, text, size, F, NAVY_D,
                  leading=size * 1.25, align='center')

    def save(self, name):
        pdf = os.path.join(IMGDIR, '_tmp.pdf')
        renderPDF.drawToFile(self.d, pdf, showBoundary=0)
        doc = pymupdf.open(pdf)
        pix = doc[0].get_pixmap(dpi=300)
        out = os.path.join(IMGDIR, name)
        pix.save(out)
        doc.close()
        os.remove(pdf)
        return out


def _strip_alpha(png):
    """Keep figures tiny & safe for Word: flatten to RGB."""
    from PIL import Image
    im = Image.open(png)
    if im.mode in ('RGBA', 'LA', 'P'):
        bg = Image.new('RGB', im.size, (255, 255, 255))
        im = im.convert('RGBA')
        bg.paste(im, mask=im.split()[-1])
        bg.save(png, optimize=True)
    return png


def finish(c, name):
    p = c.save(name)
    _strip_alpha(p)
    print('  drawn', name)
    return p
