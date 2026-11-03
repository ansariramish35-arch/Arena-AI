"""
make_assets.py
Generates the picture files that the HTML programs of Practical 4, 5 and 6
need :  shapes.png , hardware.png , grid.png

Each picture is drawn at 2x size (crisp for the screenshots in the lab file)
and a 1x copy is saved next to the source code, because the HTML files show
them at their natural size (width / height attributes).
"""
from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
FONTDIR = "/usr/share/fonts/truetype/dejavu"
OUT_HI = os.path.join(os.path.dirname(__file__), "..", "images")   # 2x, for screenshots
OUT_LO = os.path.join(os.path.dirname(__file__), "..", "source")   # 1x, shipped with code
OUT_HI = os.path.abspath(OUT_HI)
OUT_LO = os.path.abspath(OUT_LO)


def F(size, bold=False, serif=False, mono=False):
    if mono:
        name = "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"
    elif serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONTDIR, name), size * SCALE)


def centre_text(d, cx, cy, txt, font, fill):
    b = d.textbbox((0, 0), txt, font=font)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]),
           txt, font=font, fill=fill)


def save(img, folder, name):
    os.makedirs(folder, exist_ok=True)
    img.save(os.path.join(folder, name))


# =====================================================================
# 1. shapes.png  (Practical 4 : image map with rect / circle / poly)
#    hot spots : rect 20,90,180,250 | circle 265,170,80 | poly 430,90 510,250 350,250
# =====================================================================
def make_shapes():
    W, H = 520, 320
    img = Image.new("RGB", (W * SCALE, H * SCALE), "#FFFFFF")
    d = ImageDraw.Draw(img)
    s = SCALE

    d.rectangle([2 * s, 2 * s, (W - 3) * s, (H - 3) * s], outline="#1F4E79", width=2 * s)
    d.rectangle([6 * s, 6 * s, (W - 7) * s, 44 * s], fill="#1F4E79")
    centre_text(d, W / 2 * s, 25 * s, "SHAPES  -  CLICK ANY SHAPE", F(16, True), "#FFFFFF")

    # RECTANGLE  (20,90) - (180,250)
    d.rectangle([20 * s, 90 * s, 180 * s, 250 * s], fill="#4A86E8", outline="#0B3D91", width=3 * s)
    centre_text(d, 100 * s, 162 * s, "RECTANGLE", F(15, True), "#FFFFFF")
    centre_text(d, 100 * s, 184 * s, "rect", F(12, mono=True), "#DCE9FF")

    # CIRCLE  centre (265,170) radius 80
    d.ellipse([185 * s, 90 * s, 345 * s, 250 * s], fill="#34A853", outline="#0B6623", width=3 * s)
    centre_text(d, 265 * s, 162 * s, "CIRCLE", F(15, True), "#FFFFFF")
    centre_text(d, 265 * s, 184 * s, "circle", F(12, mono=True), "#DFF5E4")

    # TRIANGLE (polygon)  430,90  510,250  350,250
    d.polygon([(430 * s, 90 * s), (510 * s, 250 * s), (350 * s, 250 * s)],
              fill="#EA4335", outline="#8B0000")
    d.line([(430 * s, 90 * s), (510 * s, 250 * s)], fill="#8B0000", width=3 * s)
    d.line([(510 * s, 250 * s), (350 * s, 250 * s)], fill="#8B0000", width=3 * s)
    d.line([(350 * s, 250 * s), (430 * s, 90 * s)], fill="#8B0000", width=3 * s)
    centre_text(d, 430 * s, 214 * s, "TRIANGLE", F(14, True), "#FFFFFF")
    centre_text(d, 430 * s, 234 * s, "poly", F(11, mono=True), "#FFDDDD")

    centre_text(d, W / 2 * s, 288 * s, "Each shape is one hot spot (<area>) of the image map",
                F(12), "#333333")
    return img


# =====================================================================
# 2. hardware.png  (Practical 5 : hot spots showing related information)
#    hot spots : monitor 15,20,205,150 | cpu 215,20,375,190 | keyboard poly
# =====================================================================
def make_hardware():
    W, H = 520, 300
    img = Image.new("RGB", (W * SCALE, H * SCALE), "#F4F6F9")
    d = ImageDraw.Draw(img)
    s = SCALE

    d.rectangle([0, 0, W * s - 1, H * s - 1], outline="#1F4E79", width=2 * s)

    # ---- MONITOR : body 15,20 -> 205,140 , stand below ----
    d.rounded_rectangle([15 * s, 20 * s, 205 * s, 140 * s], radius=6 * s,
                        fill="#3B3F46", outline="#111111", width=2 * s)
    d.rectangle([24 * s, 29 * s, 196 * s, 122 * s], fill="#BBD8F5", outline="#0B3D91", width=2 * s)
    d.rectangle([95 * s, 140 * s, 125 * s, 156 * s], fill="#8A8F98")
    d.rounded_rectangle([72 * s, 156 * s, 148 * s, 164 * s], radius=3 * s, fill="#5B6068")
    # fake screen content
    d.rectangle([30 * s, 35 * s, 110 * s, 44 * s], fill="#1F4E79")
    for i in range(5):
        d.rectangle([30 * s, (54 + i * 12) * s, (190 - (i % 3) * 25) * s, (59 + i * 12) * s],
                    fill="#7FA8D9")
    centre_text(d, 110 * s, 112 * s, "MONITOR", F(13, True), "#0B3D91")

    # ---- CPU (system unit) : 215,20 -> 375,190 ----
    d.rounded_rectangle([215 * s, 20 * s, 375 * s, 190 * s], radius=6 * s,
                        fill="#C9CDD4", outline="#111111", width=2 * s)
    d.rectangle([228 * s, 32 * s, 362 * s, 46 * s], fill="#6B7280")          # DVD drive
    d.rectangle([228 * s, 52 * s, 362 * s, 62 * s], fill="#8A8F98")          # 2nd bay
    for i in range(6):
        d.rectangle([(232 + i * 20) * s, 70 * s, (244 + i * 20) * s, 76 * s], fill="#9AA0A8")
    d.ellipse([283 * s, 88 * s, 307 * s, 112 * s], fill="#1F4E79", outline="#0B3D91", width=2 * s)
    d.rectangle([228 * s, 124 * s, 362 * s, 176 * s], fill="#AEB4BC", outline="#7A8089", width=2 * s)
    for i in range(4):
        d.rectangle([236 * s, (131 + i * 11) * s, 354 * s, (136 + i * 11) * s], fill="#878D96")
    # (no text inside the picture - the labels are shown by the page itself)

    # ---- KEYBOARD : polygon 90,215 430,215 455,285 65,285 ----
    poly = [(90 * s, 215 * s), (430 * s, 215 * s), (455 * s, 285 * s), (65 * s, 285 * s)]
    d.polygon(poly, fill="#E3E6EA", outline="#111111")
    d.line([poly[0], poly[1]], fill="#111111", width=2 * s)
    d.line([poly[1], poly[2]], fill="#111111", width=2 * s)
    d.line([poly[2], poly[3]], fill="#111111", width=2 * s)
    d.line([poly[3], poly[0]], fill="#111111", width=2 * s)
    # keys (4 rows, tapered to follow the trapezoid)
    for row in range(4):
        t = row / 3.0
        xl = (90 - 25 * t) + 6
        xr = (430 + 25 * t) - 6
        y = 222 + row * 15
        n = 14
        gap = (xr - xl) / n
        for k in range(n):
            x0 = xl + k * gap + 1.5
            x1 = x0 + gap - 3
            d.rounded_rectangle([x0 * s, y * s, x1 * s, (y + 10) * s],
                                radius=1.5 * s, fill="#FFFFFF", outline="#9AA0A8")
    return img


# =====================================================================
# 3. grid.png  (Practical 6 : get coordinates from an image)
# =====================================================================
def make_grid():
    W, H = 500, 300
    img = Image.new("RGB", (W * SCALE, H * SCALE), "#FFFFFF")
    d = ImageDraw.Draw(img)
    s = SCALE

    # sky + ground
    d.rectangle([0, 0, W * s, 210 * s], fill="#EAF4FF")
    d.rectangle([0, 210 * s, W * s, H * s], fill="#DFF0D8")

    # grid every 25 px
    for x in range(0, W + 1, 25):
        w = 2 if x % 100 == 0 else 1
        d.line([x * s, 0, x * s, H * s], fill="#B9C4D0" if x % 100 else "#D8DEE6", width=w * s)
    for y in range(0, H + 1, 25):
        w = 2 if y % 100 == 0 else 1
        d.line([0, y * s, W * s, y * s], fill="#B9C4D0" if y % 100 else "#D8DEE6", width=w * s)

    # sun
    d.ellipse([400 * s, 25 * s, 460 * s, 85 * s], fill="#FFD34D", outline="#E8A400", width=2 * s)
    # simple house
    d.rectangle([80 * s, 130 * s, 200 * s, 220 * s], fill="#F2C9A0", outline="#8B5A2B", width=2 * s)
    d.polygon([(70 * s, 130 * s), (210 * s, 130 * s), (140 * s, 80 * s)],
              fill="#B0413E", outline="#7A2020")
    d.rectangle([125 * s, 170 * s, 155 * s, 220 * s], fill="#8B5A2B")
    d.rectangle([92 * s, 145 * s, 116 * s, 165 * s], fill="#BBD8F5", outline="#8B5A2B", width=2 * s)
    # tree
    d.rectangle([320 * s, 170 * s, 334 * s, 220 * s], fill="#8B5A2B")
    d.ellipse([290 * s, 120 * s, 364 * s, 190 * s], fill="#3E8E41", outline="#1F5F22", width=2 * s)

    # axis labels
    for x in range(0, W + 1, 50):
        d.text((x * s + 2 * s, 2 * s), str(x), font=F(9, mono=True), fill="#33566E")
    for y in range(50, H + 1, 50):
        d.text((2 * s, (y - 12) * s), str(y), font=F(9, mono=True), fill="#33566E")

    # two sample points already marked
    for (px, py) in ((250, 100), (375, 250)):
        d.line([(px - 7) * s, py * s, (px + 7) * s, py * s], fill="#CC0000", width=2 * s)
        d.line([px * s, (py - 7) * s, px * s, (py + 7) * s], fill="#CC0000", width=2 * s)
        d.text(((px + 9) * s, (py - 8) * s), f"({px},{py})", font=F(10, True, mono=True), fill="#CC0000")

    d.rectangle([0, 0, W * s - 1, H * s - 1], outline="#1F4E79", width=2 * s)
    d.rectangle([150 * s, 268 * s, 460 * s, 296 * s], fill="#FFFFFF", outline="#1F4E79", width=2 * s)
    centre_text(d, 305 * s, 282 * s, "grid.png   500 x 300 pixels", F(11, True), "#1F4E79")
    return img


if __name__ == "__main__":
    jobs = [
        ("shapes.png",   make_shapes(),   "practical_04"),
        ("hardware.png", make_hardware(), "practical_05"),
        ("grid.png",     make_grid(),     "practical_06"),
    ]
    for name, img, folder in jobs:
        save(img, OUT_HI, name)                                     # 2x for screenshots
        small = img.resize((img.width // SCALE, img.height // SCALE), Image.LANCZOS)
        save(small, os.path.join(OUT_LO, folder), name)             # 1x next to the code
        print(f"{folder}/{name}  ->  {small.width}x{small.height}  (2x master {img.width}x{img.height})")
