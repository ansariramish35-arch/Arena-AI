"""
browsermock.py
Small drawing library used to produce the "Output / Result" screenshots of
the Web Technology Lab File.  Every picture shows a realistic browser window
(chrome + address bar + page content) drawn with Pillow, because the pages
are plain HTML/CSS/JS whose rendering can be reproduced faithfully.

All coordinates passed to the helper methods are LOGICAL pixels; the class
internally multiplies everything by SCALE so the saved PNG is sharp.
"""
from PIL import Image, ImageDraw, ImageFont
import os

FONTDIR = "/usr/share/fonts/truetype/dejavu"
SCALE = 2

# --- palette ---------------------------------------------------------------
CHROME_TOP   = "#DEE1E6"
CHROME_TAB   = "#FFFFFF"
CHROME_BAR   = "#F1F3F4"
CHROME_LINE  = "#B0B4BA"
TEXT         = "#1A1A1A"
GREY         = "#5F6368"
LINK         = "#1155CC"
BORDER       = "#767676"
INPUT_BG     = "#FFFFFF"
DISABLED_BG  = "#EFEFEF"

_cache = {}


def font(size, bold=False, sans=False, mono=False, italic=False):
    key = (size, bold, sans, mono, italic)
    if key not in _cache:
        if mono:
            name = "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"
        elif sans:
            name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        else:
            name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
        _cache[key] = ImageFont.truetype(os.path.join(FONTDIR, name), int(size * SCALE))
    return _cache[key]


class Browser:
    """A fake browser window.  `page` callbacks draw inside the content area."""

    def __init__(self, title, url, w=780, h=600):
        self.S = SCALE
        self.W, self.H = w, h
        self.TITLEBAR = 30
        self.TOOLBAR = 34
        self.img = Image.new("RGB", (w * self.S, h * self.S), "#FFFFFF")
        self.d = ImageDraw.Draw(self.img)
        self.title = title
        self.url = url
        # content origin
        self.ox = 0
        self.oy = self.TITLEBAR + self.TOOLBAR
        self._chrome()

    # ------------------------------------------------------------------ chrome
    def _chrome(self):
        S, d = self.S, self.d
        w, h = self.W, self.H
        # title / tab strip
        d.rectangle([0, 0, w * S, self.TITLEBAR * S], fill=CHROME_TOP)
        for i, c in enumerate(("#F26B5E", "#F5BD4F", "#61C554")):
            d.ellipse([(12 + i * 16) * S, 10 * S, (22 + i * 16) * S, 20 * S], fill=c)
        # active tab
        d.rounded_rectangle([70 * S, 6 * S, 300 * S, self.TITLEBAR * S],
                            radius=6 * S, fill=CHROME_TAB)
        self.text_abs(82, 10, self.title[:40], font(10, sans=True), TEXT)
        d.text((286 * S, 9 * S), "+", font=font(11, sans=True), fill=GREY)
        # toolbar with address bar
        y0 = self.TITLEBAR
        d.rectangle([0, y0 * S, w * S, (y0 + self.TOOLBAR) * S], fill=CHROME_BAR)
        d.line([0, (y0 + self.TOOLBAR) * S, w * S, (y0 + self.TOOLBAR) * S],
               fill=CHROME_LINE, width=S)
        # back / forward / reload glyphs
        cx = 20
        for glyph, col in (("\u2190", GREY), ("\u2192", "#B7BBC1"), ("\u21BB", GREY)):
            d.text(((cx - 6) * S, (y0 + 8) * S), glyph, font=font(13, sans=True), fill=col)
            cx += 24
        # address bar
        ax, ay, aw = 90, y0 + 7, w - 120
        d.rounded_rectangle([ax * S, ay * S, (ax + aw) * S, (ay + 20) * S],
                            radius=10 * S, fill="#FFFFFF", outline=CHROME_LINE)
        d.text(((ax + 10) * S, (ay + 4) * S), self.url, font=font(10, sans=True), fill=GREY)
        # content background
        d.rectangle([0, self.oy * S, w * S, h * S], fill="#FFFFFF")

    # ------------------------------------------------------------------ basics
    def P(self, x, y):
        return (int(x * self.S), int(y * self.S))

    def trim(self, bottom):
        """crop the canvas so the page ends just after `bottom`"""
        self.img = self.img.crop((0, 0, self.W * self.S, int((bottom + 8) * self.S)))
        self.H = bottom + 8

    def auto_trim(self, margin=12):
        """crop vertically to the last non-white pixel of the page content"""
        g = self.img.convert("L")
        px = g.load()
        w, h = g.size
        start = int(self.oy * self.S)
        last = start
        for yy in range(h - 1, start, -1):
            row_has = False
            for xx in range(0, w, 4):
                if px[xx, yy] < 250:
                    row_has = True
                    break
            if row_has:
                last = yy
                break
        bottom = min(h, last + int(margin * self.S))
        self.img = self.img.crop((0, 0, w, bottom))
        self.H = bottom / self.S
        return self.H

    def text_abs(self, x, y, s, f, fill=TEXT):
        self.d.text((x * self.S, y * self.S), s, font=f, fill=fill)

    def text(self, x, y, s, f, fill=TEXT):
        self.text_abs(self.ox + x, self.oy + y, s, f, fill)

    def measure(self, s, f):
        b = self.d.textbbox((0, 0), s, font=f)
        return ((b[2] - b[0]) / self.S, (b[3] - b[1]) / self.S)

    def centre(self, x, y, w, s, f, fill=TEXT):
        tw, th = self.measure(s, f)
        self.text(x + (w - tw) / 2, y, s, f, fill)

    def right(self, x, y, w, s, f, fill=TEXT):
        tw, th = self.measure(s, f)
        self.text(x + w - tw, y, s, f, fill)

    def wrap(self, s, f, maxw):
        words, lines, cur = s.split(), [], ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if self.measure(t, f)[0] <= maxw:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, f, fill=TEXT, maxw=None, lh=None):
        maxw = maxw or (self.W - x - 20)
        lh = lh or (self.measure("Ag", f)[1] + 5)
        for line in self.wrap(s, f, maxw):
            self.text(x, y, line, f, fill)
            y += lh
        return y

    def rect(self, x, y, w, h, fill=None, outline=None, width=1):
        self.d.rectangle([self.P(self.ox + x, self.oy + y),
                          self.P(self.ox + x + w, self.oy + y + h)],
                         fill=fill, outline=outline, width=width * self.S)

    def rrect(self, x, y, w, h, r, fill=None, outline=None, width=1):
        self.d.rounded_rectangle([self.P(self.ox + x, self.oy + y),
                                  self.P(self.ox + x + w, self.oy + y + h)],
                                 radius=r * self.S, fill=fill, outline=outline,
                                 width=width * self.S)

    def line(self, x1, y1, x2, y2, fill=TEXT, width=1):
        self.d.line([self.P(self.ox + x1, self.oy + y1),
                     self.P(self.ox + x2, self.oy + y2)], fill=fill, width=width * self.S)

    def hline(self, x, y, w, fill=CHROME_LINE, width=1):
        self.line(x, y, x + w, y, fill, width)

    def heading(self, x, y, s, size=18, color="#1F4E79", bold=True, centre=False, width=None):
        f = font(size, bold)
        if centre and width:
            self.centre(x, y, width, s, f, color)
        else:
            self.text(x, y, s, f, color)
        return y + self.measure(s, f)[1] + 6

    def hrule(self, x, y, w, color="#1F4E79", width=2):
        self.line(x, y, x + w, y, color, width)
        return y + 6

    # ------------------------------------------------------------- form widgets
    def inputbox(self, x, y, w, h=20, value="", placeholder=False, error=False, focus=False):
        self.rect(x, y, w, h, fill=INPUT_BG,
                  outline="#CC0000" if error else BORDER)
        if value:
            self.text(x + 4, y + 3, value, font(10, mono=True),
                      "#9AA0A6" if placeholder else TEXT)
        if focus:
            self.line(x + 2, y + h - 2, x + 2, y + 3, "#1A73E8", 1)
        return y + h

    def radio(self, x, y, checked=False):
        self.d.ellipse([self.P(self.ox + x, self.oy + y),
                        self.P(self.ox + x + 12, self.oy + y + 12)],
                       outline=BORDER, fill="#FFFFFF", width=self.S)
        if checked:
            self.d.ellipse([self.P(self.ox + x + 3, self.oy + y + 3),
                            self.P(self.ox + x + 9, self.oy + y + 9)], fill="#1A73E8")
        return x + 16

    def checkbox(self, x, y, checked=False):
        self.rect(x, y, 12, 12, fill="#FFFFFF", outline=BORDER)
        if checked:
            self.text(x + 1, y - 2, "\u2713", font(10, bold=True, sans=True), "#1A73E8")
        return x + 16

    def button(self, x, y, w, h=22, label="Button"):
        self.rrect(x, y, w, h, 3, fill="#EFEFEF", outline=BORDER)
        self.centre(x, y + 4, w, label, font(10, sans=True), TEXT)
        return x + w

    def select(self, x, y, w, h=20, label="-- select --"):
        self.rect(x, y, w, h, fill="#FFFFFF", outline=BORDER)
        self.text(x + 4, y + 3, label, font(10, sans=True))
        self.line(x + w - 18, y, x + w - 18, y + h, BORDER)
        cx = x + w - 10
        self.d.polygon([self.P(cx - 4, y + 8), self.P(cx + 4, y + 8), self.P(cx, y + 13)],
                       fill="#333333")
        return y + h

    def textarea(self, x, y, w, h=60, lines=None):
        self.rect(x, y, w, h, fill="#FFFFFF", outline=BORDER)
        if lines:
            yy = y + 3
            for ln in lines:
                self.text(x + 4, yy, ln, font(10, mono=True))
                yy += 13
        return y + h

    def fieldset(self, x, y, w, h, legend):
        self.rect(x, y, w, h, outline="#767676")
        f = font(11, bold=True)
        tw, th = self.measure(legend, f)
        self.rect(x + 8, y - 7, tw + 8, 14, fill="#FFFFFF")
        self.text(x + 12, y - 7, legend, f, TEXT)

    def table(self, x, y, colw, rows, header=True, fsize=10, aligns=None,
              head_bg="#D9E1F2", zebra="#F2F6FC", rowh=None):
        f = font(fsize)
        fb = font(fsize, bold=True)
        rh = rowh or (self.measure("Ag", f)[1] + 8)
        total = sum(colw)
        yy = y
        for ri, row in enumerate(rows):
            bg = head_bg if (header and ri == 0) else (zebra if ri % 2 == 0 else "#FFFFFF")
            self.rect(x, yy, total, rh, fill=bg)
            xx = x
            for ci, cell in enumerate(row):
                cf = fb if (header and ri == 0) else f
                al = (aligns[ci] if aligns else "l")
                cw, ch = self.measure(cell, cf)
                if al == "c":
                    self.text(xx + (colw[ci] - cw) / 2, yy + 4, cell, cf)
                elif al == "r":
                    self.text(xx + colw[ci] - cw - 4, yy + 4, cell, cf)
                else:
                    self.text(xx + 4, yy + 4, cell, cf)
                if ci:
                    self.line(xx, yy, xx, yy + rh, "#999999")
                xx += colw[ci]
            self.hline(x, yy + rh, total, "#999999")
            yy += rh
        for ci in range(len(colw) + 1):
            xx = x + sum(colw[:ci])
            self.line(xx, y, xx, yy, "#999999")
        return yy

    def vscrollbar(self, x, y, h, thumb=0.25, at=0.0):
        self.rect(x, y, 14, h, fill="#F1F3F4", outline=CHROME_LINE)
        th = max(24, h * thumb)
        ty = y + (h - th) * at
        self.rrect(x + 2, ty, 10, th, 5, fill="#B0B4BA")
        self.text(x + 3, y + 2, "\u25B2", font(7, sans=True), GREY)
        self.text(x + 3, y + h - 12, "\u25BC", font(7, sans=True), GREY)

    def paste(self, img, x, y, w=None, h=None):
        """paste a 2x master image (from images/) scaled to logical w x h"""
        tw = w or img.width // self.S
        th = h or img.height // self.S
        resized = img.resize((tw * self.S, th * self.S), Image.LANCZOS)
        self.img.paste(resized, self.P(self.ox + x, self.oy + y))
        return y + th

    def save(self, path):
        self.img.save(path)
        return path
