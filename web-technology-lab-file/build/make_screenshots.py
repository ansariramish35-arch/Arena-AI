"""
make_screenshots.py
Builds every "Output / Result" screenshot of the lab file by drawing a
faithful browser rendering of the pages written in ../source.
Run :  python build/make_screenshots.py
"""
import os
import math
from PIL import Image, ImageDraw
from browsermock import Browser, font, TEXT, GREY, LINK, BORDER

HERE = os.path.abspath(os.path.dirname(__file__))
IMG = os.path.abspath(os.path.join(HERE, "..", "images"))
BIG = 1300  # generous canvas; each page is trimmed to its real content height


def load(name):
    return Image.open(os.path.join(IMG, name))


def dash(b, x1, y1, x2, y2, color="#CC0000", w=2):
    L = math.hypot(x2 - x1, y2 - y1)
    n = max(1, int(L // 8))
    for i in range(n):
        t1, t2 = i / n, (i + 0.5) / n
        b.line(x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1,
               x1 + (x2 - x1) * t2, y1 + (y2 - y1) * t2, color, w)


def dash_rect(b, x1, y1, x2, y2):
    dash(b, x1, y1, x2, y1); dash(b, x2, y1, x2, y2)
    dash(b, x2, y2, x1, y2); dash(b, x1, y2, x1, y1)


def warn_triangle(b, x, y, size=18):
    b.d.polygon([b.P(x + size / 2, y), b.P(x + size, y + size), b.P(x, y + size)],
                fill="#F5BD4F", outline="#B8860B")
    b.text(x + size / 2 - 3, y + 3, "!", font(size * 0.7, bold=True, sans=True), "#3B2F00")


# =====================================================================
# Practical 1 : resume made with tables
# =====================================================================
def out01():
    b = Browser("Resume - Table Layout", "file:///C:/webtech/practical_01/resume.html",
                w=780, h=BIG)
    x, w = 40, 700
    lblw = 160
    y = 20

    def label(row_y, row_h, txt):
        b.rect(x, row_y, lblw, row_h, fill="#F2F2F2")
        yy = row_y + 6
        for ln in txt.split("\n"):
            b.text(x + 6, yy, ln, font(10, bold=True))
            yy += 14

    def rowstart(row_h):
        nonlocal y
        b.rect(x, y, w, row_h, outline="#000000")
        b.line(x + lblw, y, x + lblw, y + row_h, "#000000")
        return y

    hh = 74
    ry = rowstart(hh)
    b.rect(x, ry, w, hh, fill="#D9E1F2")
    b.centre(x, ry + 10, w, "YOUR NAME", font(22, bold=True, sans=True))
    b.centre(x, ry + 42, w, "123, Street Name, City, State - 226001", font(9, sans=True))
    b.centre(x, ry + 56, w, "Mobile : +91-98XXXXXXXX   |   Email : yourname@email.com",
             font(9, sans=True))
    y += hh

    body = ("To work in a challenging environment where I can use my technical skills "
            "and knowledge for the growth of the organisation, and to keep learning "
            "new web technologies.")
    rh = 62
    ry = rowstart(rh)
    label(ry, rh, "CAREER OBJECTIVE")
    b.para(x + lblw + 8, ry + 6, body, font(10), maxw=w - lblw - 16)
    y += rh

    rh = 118
    ry = rowstart(rh)
    label(ry, rh, "EDUCATIONAL\nQUALIFICATION")
    b.table(x + lblw + 8, ry + 6, [150, 210, 70, 100],
            [["Course / Degree", "School / University", "Year", "Percentage"],
             ["B.Tech (CSE)", "Name of University", "20XX", "XX.X %"],
             ["Intermediate (12th)", "Name of Board / College", "20XX", "XX.X %"],
             ["High School (10th)", "Name of Board / School", "20XX", "XX.X %"]],
            fsize=9.5, aligns=["l", "l", "c", "c"], rowh=26)
    y += rh

    rh = 108
    ry = rowstart(rh)
    label(ry, rh, "TECHNICAL SKILLS")
    b.table(x + lblw + 8, ry + 6, [150, 380],
            [["Languages", "C, C++, Java, Python"],
             ["Web Technologies", "HTML, CSS, JavaScript, XML"],
             ["Databases", "MySQL, Oracle"],
             ["Operating Systems", "Windows, Linux (Ubuntu)"]],
            fsize=9.5, rowh=25)
    y += rh

    rh = 52
    ry = rowstart(rh)
    label(ry, rh, "PROJECTS")
    b.text(x + lblw + 12, ry + 6, "1.", font(10))
    b.text(x + lblw + 26, ry + 6,
           "Student Record System - HTML form with JavaScript validation.", font(10))
    b.text(x + lblw + 12, ry + 26, "2.", font(10))
    b.text(x + lblw + 26, ry + 26,
           "College Home Page - designed using HTML frames and CSS.", font(10))
    y += rh

    rh = 92
    ry = rowstart(rh)
    label(ry, rh, "PERSONAL DETAILS")
    yy = ry + 6
    for k, v in [("Father's Name", ": ____________________"),
                 ("Date of Birth", ": ____________________"),
                 ("Languages Known", ": English, Hindi"),
                 ("Hobbies", ": Reading, Cricket, Music")]:
        b.text(x + lblw + 8, yy, k, font(10, bold=True))
        b.text(x + lblw + 150, yy, v, font(10))
        yy += 21
    y += rh

    rh = 46
    ry = rowstart(rh)
    label(ry, rh, "DECLARATION")
    b.para(x + lblw + 8, ry + 6,
           "I hereby declare that the information given above is true to the best of my "
           "knowledge and belief.", font(10), maxw=w - lblw - 16)
    y += rh

    rh = 70
    ry = rowstart(rh)
    label(ry, rh, "PLACE / DATE")
    b.right(x + lblw + 8, ry + 8, w - lblw - 24, "Place : ____________", font(10))
    b.right(x + lblw + 8, ry + 26, w - lblw - 24, "Date  : ____________", font(10))
    b.right(x + lblw + 8, ry + 48, w - lblw - 24, "(YOUR NAME)", font(10, bold=True))
    y += rh

    b.auto_trim()
    b.save(os.path.join(IMG, "out01_resume.png"))


# =====================================================================
# Practical 2 : frames
# =====================================================================
def out02():
    b = Browser("College Home Page - Frames",
                "file:///C:/webtech/practical_02/index.html", w=780, h=BIG)
    y = 14
    bh = 66
    b.rect(6, y, 768, bh, fill="#1F4E79", outline="#808080", width=2)
    b.centre(6, y + 14, 768, "NAME OF THE COLLEGE", font(18, bold=True, sans=True), "#FFFFFF")
    b.centre(6, y + 42, 768,
             "Department of Computer Science & Engineering  |  Affiliated to Name of University",
             font(9.5, sans=True), "#DCE6F5")
    y += bh
    mw = int(768 * 0.20)
    mh = 400
    b.rect(6, y, mw, mh, fill="#F2F2F2", outline="#808080", width=2)
    b.rect(6, y, mw, 26, fill="#1F4E79")
    b.centre(6, y + 6, mw, "MAIN MENU", font(10, bold=True, sans=True), "#FFFFFF")
    items = ["Home", "About Us", "Courses", "Contact Us"]
    yy = y + 26
    for i, it in enumerate(items):
        if i == 0:
            b.rect(6, yy, mw - 16, 27, fill="#D9E1F2")
        b.text(16, yy + 7, it, font(9.5, sans=True), "#1F4E79" if i == 0 else "#000000")
        b.hline(6, yy + 27, mw - 16, "#CCCCCC")
        yy += 27
    b.vscrollbar(6 + mw - 16, y + 26, mh - 26, thumb=0.9)
    cx = 6 + mw
    b.rect(cx, y, 768 - mw, mh, fill="#FFFFFF", outline="#808080", width=2)
    tx, ty = cx + 16, y + 16
    ty = b.heading(tx, ty, "Welcome to the College Website", 15, "#1F4E79")
    ty = b.para(tx, ty + 4,
                "This home page is created using HTML frames. The browser window is "
                "divided into three parts:", font(10.5), maxw=768 - mw - 40)
    ty += 6
    for li in ["Top frame  - college banner (banner.html)",
               "Left frame - navigation menu (menu.html)",
               'Right frame - content pages, opened with target="main"']:
        b.text(tx + 6, ty, "\u2022", font(10))
        b.text(tx + 18, ty, li, font(10.5))
        ty += 18
    ty += 6
    ty = b.para(tx, ty,
                "Click any menu item on the left. Only this frame changes; the banner "
                "and the menu stay fixed on the screen.", font(10.5), maxw=768 - mw - 40)
    b.vscrollbar(cx + 768 - mw - 18, y + 2, mh - 4, thumb=0.85)
    y += mh + 8
    b.text(8, y, 'frameset rows="15%, 85%"   /   cols="20%, 80%"   -   the three frames '
                 'share ONE browser window', font(8.5, mono=True), "#9AA0A6")
    b.auto_trim()
    b.save(os.path.join(IMG, "out02_frames.png"))


# =====================================================================
# Practical 3 : form creation
# =====================================================================
def out03():
    b = Browser("Student Registration Form",
                "file:///C:/webtech/practical_03/form.html", w=780, h=BIG)
    y = 18
    b.centre(0, y, 780, "STUDENT REGISTRATION FORM", font(17, bold=True))
    y += 34

    def fs(y, h, legend):
        b.fieldset(40, y, 700, h, legend)
        return y + 12

    h1 = 216
    y = fs(y, h1, "Personal Details")
    rows = [
        ("Full Name :", "text", "Enter your full name"),
        ("Password :", "pass", ""),
        ("Gender :", "radio", ""),
        ("Date of Birth :", "date", ""),
        ("E-Mail :", "text", "name@email.com"),
        ("Mobile No. :", "text", "10 digit number"),
    ]
    yy = y + 4
    for lab, kind, val in rows:
        b.right(60, yy + 3, 150, lab, font(10))
        xx = 220
        if kind == "text":
            b.inputbox(xx, yy, 250, 20, val, placeholder=True)
        elif kind == "pass":
            b.inputbox(xx, yy, 250, 20, "")
            b.text(xx + 5, yy + 4, "\u2022" * 8, font(10, mono=True))
        elif kind == "date":
            b.inputbox(xx, yy, 150, 20, "dd/mm/yyyy", placeholder=True)
            b.rect(xx + 156, yy + 2, 16, 16, fill="#F1F3F4", outline=BORDER)
            b.line(xx + 156, yy + 7, xx + 172, yy + 7, BORDER)
            b.rect(xx + 159, yy + 10, 4, 4, fill="#1A73E8")
        elif kind == "radio":
            xx = b.radio(xx, yy + 4, checked=True)
            b.text(xx + 2, yy + 3, "Male", font(10))
            xx = b.radio(xx + 48, yy + 4)
            b.text(xx + 2, yy + 3, "Female", font(10))
            xx = b.radio(xx + 60, yy + 4)
            b.text(xx + 2, yy + 3, "Other", font(10))
        yy += 32
    y += h1 + 14

    h2 = 272
    y = fs(y, h2, "Academic Details")
    yy = y + 4
    b.right(60, yy + 3, 150, "Course :", font(10))
    b.select(220, yy, 200, 20, "B.Tech (CSE)")
    yy += 30
    b.right(60, yy + 3, 150, "Semester :", font(10))
    b.select(220, yy, 90, 20, "I")
    yy += 30
    b.right(60, yy + 3, 150, "Hobbies :", font(10))
    xx = 220
    for name, chk in [("Reading", True), ("Sports", False), ("Music", True), ("Coding", False)]:
        xx = b.checkbox(xx, yy + 4, chk)
        b.text(xx + 2, yy + 3, name, font(10))
        xx += 12 + b.measure(name, font(10))[0] + 14
    yy += 30
    b.right(60, yy + 3, 150, "Address :", font(10))
    b.textarea(220, yy, 300, 62, ["Enter your complete address"])
    yy += 72
    b.right(60, yy + 3, 150, "Upload Photo :", font(10))
    b.button(220, yy, 90, 22, "Choose File")
    b.text(318, yy + 5, "No file chosen", font(9.5, sans=True), GREY)
    yy += 32
    b.right(60, yy + 3, 150, "Marks Obtained :", font(10))
    b.inputbox(220, yy, 70, 20, "")
    b.text(300, yy + 4, "Percentage :", font(10))
    b.line(370, yy + 10, 470, yy + 10, "#B0B4BA", 3)
    b.d.ellipse([b.P(424, yy + 4), b.P(436, yy + 16)], fill="#1A73E8")
    yy += 30
    b.right(60, yy + 3, 150, "Favourite Colour :", font(10))
    b.rect(220, yy, 34, 20, fill="#1F4E79", outline=BORDER)
    b.text(260, yy + 4, "#1F4E79", font(9.5, mono=True))
    y += h2 + 16

    bw = 110
    x0 = 390 - (3 * bw + 40) // 2
    b.button(x0, y, bw, 24, "Submit Form")
    b.button(x0 + bw + 20, y, bw, 24, "Reset Form")
    b.button(x0 + 2 * (bw + 20), y, bw, 24, "Cancel")
    b.auto_trim()
    b.save(os.path.join(IMG, "out03_form.png"))


# =====================================================================
# Practical 4 : image map
# =====================================================================
def out04():
    b = Browser("HTML Image Map",
                "file:///C:/webtech/practical_04/image_map.html", w=780, h=BIG)
    y = 16
    y = b.heading(0, y, "IMAGE MAP : Click on a Shape", 16, "#1F4E79", centre=True, width=780)
    y += 6
    ix = (780 - 520) // 2
    b.paste(load("shapes.png"), ix, y, 520, 320)
    cxp, cyp = ix + 265, y + 170
    b.d.polygon([b.P(cxp, cyp), b.P(cxp + 12, cyp + 12), b.P(cxp + 5, cyp + 12),
                 b.P(cxp + 5, cyp + 18), b.P(cxp + 1, cyp + 18), b.P(cxp + 1, cyp + 12),
                 b.P(cxp - 3, cyp + 12)], fill="#FFFFFF", outline="#000000")
    b.rrect(cxp + 14, cyp - 26, 236, 20, 3, fill="#FFFFE1", outline="#000000")
    b.text(cxp + 20, cyp - 22, "Circle - all points at equal distance", font(9, sans=True))
    y += 330
    y = b.heading(0, y, "Coordinates used in this image map", 13, centre=True, width=780)
    y = b.table(60, y + 4, [120, 140, 400],
                [["Shape", "shape attribute", "coords attribute"],
                 ["Rectangle", "rect", "left,top,right,bottom = 20,90,180,250"],
                 ["Circle", "circle", "centre-x,centre-y,radius = 265,170,80"],
                 ["Triangle", "poly", "x1,y1,x2,y2,x3,y3 = 430,90,510,250,350,250"]],
                fsize=10, aligns=["c", "c", "l"], rowh=24)
    b.auto_trim()
    b.save(os.path.join(IMG, "out04_imagemap.png"))


# =====================================================================
# Practical 5 : hot spots -> related information
# =====================================================================
def out05():
    b = Browser("Image Hot Spots - Show Related Information",
                "file:///C:/webtech/practical_05/hotspots.html", w=780, h=BIG)
    y = 14
    y = b.heading(0, y, "COMPUTER HARDWARE - CLICK A HOT SPOT", 16, "#1F4E79",
                  centre=True, width=780)
    y += 4
    ix = (780 - 520) // 2
    b.paste(load("hardware.png"), ix, y, 520, 300)
    dash_rect(b, ix + 15, y + 20, ix + 205, y + 150)
    dash_rect(b, ix + 215, y + 20, ix + 375, y + 190)
    pts = [(ix + 90, y + 215), (ix + 430, y + 215), (ix + 455, y + 285), (ix + 65, y + 285)]
    for i in range(4):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % 4]
        dash(b, x1, y1, x2, y2)
    for (bx, by, lab) in [(ix + 24, y + 24, "1"), (ix + 224, y + 24, "2 (clicked)"),
                          (ix + 74, y + 250, "3")]:
        wlab = 26 if lab == "1" else (74 if lab == "3" else 84)
        b.rrect(bx, by, wlab, 16, 3, fill="#CC0000")
        b.centre(bx, by + 3, wlab, lab, font(8.5, bold=True, sans=True), "#FFFFFF")
    b.d.polygon([b.P(ix + 292, y + 100), b.P(ix + 304, y + 112), b.P(ix + 297, y + 112),
                 b.P(ix + 297, y + 118), b.P(ix + 293, y + 118), b.P(ix + 293, y + 112),
                 b.P(ix + 289, y + 112)], fill="#FFFFFF", outline="#000000")
    y += 312
    b.rect(130, y, 520, 176, fill="#F7F9FC", outline="#1F4E79", width=2)
    b.heading(142, y + 10, "CPU (Central Processing Unit)", 13, "#1F4E79")
    yy = b.para(142, y + 34,
                "The CPU is called the brain of the computer. It performs all "
                "arithmetic and logical operations on the data.", font(10.5), maxw=496)
    yy = b.table(142, yy + 6, [130, 366],
                 [["Property", "Detail"],
                  ["Type", "Processing device"],
                  ["Main parts", "ALU, Control Unit, Memory Unit"],
                  ["Examples", "Intel Core i5, AMD Ryzen 5"]],
                 fsize=9.5, rowh=22)
    b.auto_trim()
    b.save(os.path.join(IMG, "out05_hotspots.png"))


# =====================================================================
# Practical 6 : coordinates from an image
# =====================================================================
def out06():
    b = Browser("Get Image Coordinates using JavaScript",
                "file:///C:/webtech/practical_06/coordinates.html", w=780, h=BIG)
    y = 14
    y = b.heading(0, y, "GET COORDINATES FROM AN IMAGE USING JAVASCRIPT", 15,
                  "#1F4E79", centre=True, width=780)
    b.centre(0, y + 4, 780, "Move the mouse over the image or click anywhere on it. "
                            "The X and Y coordinates are shown below.", font(10.5))
    y += 26
    ix = (780 - 500) // 2
    b.rect(ix - 3, y - 3, 506, 306, outline="#1F4E79", width=2)
    b.paste(load("grid.png"), ix, y, 500, 300)
    mx, my = ix + 250, y + 100
    b.line(mx - 10, my, mx + 10, my, "#CC0000", 1)
    b.line(mx, my - 10, mx, my + 10, "#CC0000", 1)
    b.d.polygon([b.P(mx + 4, my + 4), b.P(mx + 16, my + 16), b.P(mx + 9, my + 16),
                 b.P(mx + 9, my + 22), b.P(mx + 5, my + 22), b.P(mx + 5, my + 16),
                 b.P(mx + 1, my + 16)], fill="#FFFFFF", outline="#000000")
    y += 312
    b.centre(0, y, 780,
             "CLICKED at  X = 250 ,  Y = 100   ( image size = 500 x 300 pixels )",
             font(11, bold=True), "#990000")
    y += 26
    y = b.table(140, y, [240, 130, 130],
                [["Event", "X coordinate", "Y coordinate"],
                 ["Mouse Move (offset)", "250", "100"],
                 ["Mouse Click (offset)", "250", "100"],
                 ["Mouse Click (client - window)", "408", "351"],
                 ["Mouse Click (page - document)", "408", "351"]],
                fsize=10, aligns=["l", "c", "c"], rowh=25)
    b.auto_trim()
    b.save(os.path.join(IMG, "out06_coords.png"))


# =====================================================================
# Practical 7 : all types of CSS
# =====================================================================
def out07():
    b = Browser("All Types of Cascading Style Sheets",
                "file:///C:/webtech/practical_07/css_all_types.html", w=780, h=BIG)
    y = 16
    b.centre(0, y, 780, "THREE TYPES OF CASCADING STYLE SHEETS",
             font(17, bold=True, sans=True), "#1F4E79")
    b.line(90, y + 28, 690, y + 28, "#1F4E79", 1)
    b.line(90, y + 31, 690, y + 31, "#1F4E79", 1)
    y += 44

    b.rect(40, y, 700, 34, fill="#990000")
    b.centre(40, y + 8, 700, "1. INLINE STYLE SHEET", font(13, bold=True, sans=True), "#FFFFFF")
    y += 46
    yy = b.para(40, y, "This paragraph is styled with the style attribute written "
                       "directly inside the tag. Inline CSS has the highest priority.",
                font(11, bold=True), "#990000", maxw=700)
    yy += 8
    b.rect(40, yy, 700, 40, fill="#FFEBEE", outline="#990000", width=2)
    b.text(52, yy + 12, "Inline CSS is used to style only ONE single element.",
           font(11), "#990000")
    y = yy + 56

    b.rect(40, y, 700, 32, fill="#E8F5E9")
    b.rect(40, y, 8, 32, fill="#0B6623")
    b.text(58, y + 7, "2. internal (embedded) style sheet", font(13, bold=True), "#0B6623")
    y += 42
    yy = b.para(40, y, "This paragraph and the heading above are styled by the <style> block "
                       "written inside the <head> section of this same page. Internal CSS "
                       "applies to the whole page.", font(11), "#333333", maxw=700, lh=19)
    yy += 8
    yy = b.table(60, yy, [140, 260, 140],
                 [["Type of CSS", "Where it is written", "Applies to"],
                  ["Inline", "style attribute of the tag", "One element"],
                  ["Internal", "<style> block in <head>", "One page"],
                  ["External", "separate .css file + <link>", "Many pages"]],
                 fsize=10, rowh=24, head_bg="#C8E6C9", zebra="#F1F8E9")
    y = yy + 18

    b.rect(40, y, 700, 32, fill="#D9E1F2", outline="#1F4E79", width=2)
    b.centre(40, y + 7, 700, "3. EXTERNAL STYLE SHEET", font(13, bold=True, sans=True), "#1F4E79")
    y += 42
    yy = b.para(70, y, "This heading and paragraph are styled by the separate file "
                       "external_style.css, which is attached to this page with the <link> "
                       "tag. The same file can be attached to any number of pages of a "
                       "website, so the design stays common everywhere.",
                font(11), "#191970", maxw=670, lh=19)
    yy += 10
    b.rrect(40, yy, 700, 44, 8, fill="#EAF1FA", outline="#1F4E79", width=2)
    b.centre(40, yy + 14, 700, 'This DIV also uses the external style sheet (class = "box").',
             font(11), "#1F4E79")
    b.auto_trim()
    b.save(os.path.join(IMG, "out07_css.png"))


# =====================================================================
# Practical 8 : navigator
# =====================================================================
def out08():
    b = Browser("Web Navigator - CV, Institute, Department, Tutorial",
                "file:///C:/webtech/practical_08/navigator.html", w=780, h=BIG)
    y = 8
    b.rect(0, y, 780, 32, fill="#1F4E79")
    b.centre(0, y + 7, 780, "WEB NAVIGATOR", font(15, bold=True), "#FFFFFF")
    y += 38
    b.rect(0, y, 780, 34, fill="#D9E1F2")
    b.select(10, y + 7, 210, 20, "My CV (Resume)")
    b.button(228, y + 6, 46, 22, "GO")
    for i, lab in enumerate(["My CV", "Institute", "Department", "Tutorial"]):
        b.button(286 + i * 78, y + 6, 72, 22, lab)
    b.button(600, y + 6, 90, 22, "Open NEW Tab")
    b.button(696, y + 6, 40, 22, "Back")
    y += 40
    b.centre(0, y + 2, 780, "Now showing : cv.html", font(10, sans=True), "#990000")
    y += 20
    fh = 500
    b.rect(4, y, 772, fh, outline="#1F4E79", width=2)
    ty = y + 14
    b.centre(4, ty, 772, "CURRICULUM VITAE", font(18, bold=True), "#1F4E79")
    ty += 30
    b.centre(4, ty, 772,
             "YOUR NAME  |  B.Tech (CSE)  |  Roll No. ________  |  yourname@email.com  |  "
             "+91-98XXXXXXXX", font(9.5))
    ty += 22

    def sec(title, body_lines):
        nonlocal ty
        b.rect(20, ty, 740, 20, fill="#D9E1F2")
        b.rect(20, ty, 6, 20, fill="#1F4E79")
        b.text(32, ty + 3, title, font(11, bold=True))
        ty += 24
        for ln in body_lines:
            ty = b.para(24, ty, ln, font(10), maxw=720, lh=15)
        ty += 8

    sec("Career Objective",
        ["To obtain a position where I can apply my knowledge of web technologies and grow "
         "along with the organisation."])
    sec("Educational Qualification", [])
    ty = b.table(24, ty, [180, 260, 80, 60],
                 [["Course", "Institute / Board", "Year", "%"],
                  ["B.Tech (CSE)", "Name of College", "20XX", "XX.X"],
                  ["12th", "Name of Board", "20XX", "XX.X"],
                  ["10th", "Name of Board", "20XX", "XX.X"]],
                 fsize=9.5, rowh=21, head_bg="#F2F2F2")
    ty += 10
    sec("Technical Skills", ["HTML, CSS, JavaScript, XML, C, C++, MySQL, Windows / Linux."])
    sec("Project",
        ["Web Navigator - a JavaScript based page to display the CV, institute website, "
         "department website and tutorial website in one window."])
    sec("Personal Details", ["Date of Birth : __________    Languages : English, Hindi"])
    sec("Declaration", ["The information given above is true to the best of my knowledge."])
    b.right(30, ty, 720, "(YOUR NAME)", font(10, bold=True))
    b.vscrollbar(760, y + 2, fh - 4, thumb=0.62)
    b.auto_trim()
    b.save(os.path.join(IMG, "out08_navigator.png"))


# =====================================================================
# Practical 9 : validation with errors + alert
# =====================================================================
def out09():
    b = Browser("Student Record - JavaScript Validation",
                "file:///C:/webtech/practical_09/student_record.html", w=780, h=BIG)
    y = 14
    b.centre(0, y, 780, "STUDENT RECORD FORM (with JavaScript Validation)",
             font(15, bold=True), "#1F4E79")
    y += 30
    fx, fw, fheight = 90, 600, 560
    b.rect(fx, y, fw, fheight, fill="#F7F9FC", outline="#1F4E79", width=2)
    yy = y + 14

    def field(label, widget, err=None):
        nonlocal yy
        b.right(fx + 14, yy + 3, 170, label, font(10, bold=True))
        widget(fx + 190, yy)
        if err:
            b.text(fx + 436, yy + 5, err, font(9, bold=True, sans=True), "#CC0000")
        yy += 34

    def t(value="", ph=False, w=230, err=False):
        def w_(x, y):
            b.inputbox(x, y, w, 20, value, placeholder=ph, error=err)
        return w_

    field("Student Name * :", t("", True, err=True), "Name is required.")
    field("Roll Number * :", t("CSE21", err=True), "4-12 letters/digits only.")
    field("Enrollment Number * :", t("12345", err=True), "Must be exactly 12 digits.")
    field("E-Mail * :", t("abc@college", err=True), "Invalid e-mail address.")
    field("Mobile Number * :", t("9812", err=True), "10 digits, start with 6-9.")
    field("Password * :", t("", err=True), "Minimum 6 characters.")
    field("Confirm Password * :", t("", err=True), "Passwords do not match.")
    field("Date of Birth * :", t("31/02/2005", err=True), "This date does not exist.")

    def gender(x, y):
        b.radio(x, y + 4); b.text(x + 16, y + 3, "Male", font(10))
        b.radio(x + 62, y + 4); b.text(x + 78, y + 3, "Female", font(10))
    field("Gender * :", gender, "Please select gender.")

    field("Course * :", lambda x, y: b.select(x, y, 180, 20, "-- Select --"), "Select a course.")
    field("Semester * :", lambda x, y: b.select(x, y, 90, 20, "-- Select --"), "Select a semester.")

    b.right(fx + 14, yy + 3, 170, "Address :", font(10, bold=True))
    b.textarea(fx + 190, yy, 230, 50)
    yy += 58

    def hob(x, y):
        xx = b.checkbox(x, y + 4); b.text(xx + 2, y + 3, "Reading", font(10))
        xx = b.checkbox(xx + 62, y + 4); b.text(xx + 2, y + 3, "Sports", font(10))
        xx = b.checkbox(xx + 58, y + 4); b.text(xx + 2, y + 3, "Music", font(10))
    b.right(fx + 14, yy + 3, 170, "Hobbies :", font(10, bold=True))
    hob(fx + 190, yy)
    yy += 34
    field("I accept the rules * :", lambda x, y: b.checkbox(x, y + 4),
          "You must accept the rules.")
    yy += 6
    b.button(fx + 190, yy, 110, 24, "Save Record")
    b.button(fx + 316, yy, 90, 24, "Reset")
    form_bottom = yy + 30

    # ---------- alert dialog overlay ----------
    ov = Image.new("RGBA", b.img.size, (25, 25, 25, 95))
    b.img = Image.alpha_composite(b.img.convert("RGBA"), ov).convert("RGB")
    b.d = ImageDraw.Draw(b.img)
    ax, ay, aw, ah = 210, 250, 360, 132
    b.rect(ax, ay, aw, ah, fill="#F1F3F4", outline="#9AA0A6", width=1)
    b.rect(ax, ay, aw, 26, fill="#DEE1E6")
    b.text(ax + 10, ay + 6, "localhost says", font(10, sans=True, bold=True))
    b.text(ax + aw - 22, ay + 5, "\u00D7", font(11, sans=True), GREY)
    warn_triangle(b, ax + 16, ay + 42, 18)
    b.text(ax + 44, ay + 46, "Please correct the highlighted fields.", font(10.5, sans=True))
    b.text(ax + 44, ay + 64, "11 error message(s) found.", font(9.5, sans=True), GREY)
    b.button(ax + aw // 2 - 35, ay + ah - 38, 70, 24, "OK")
    b.trim(form_bottom)
    b.save(os.path.join(IMG, "out09_validation.png"))


# =====================================================================
# Practical 10 : XML tree view + validator errors
# =====================================================================
def out10():
    b = Browser("students.xml", "file:///C:/webtech/practical_10/students.xml",
                w=780, h=BIG)
    TAG, ATT, VAL, TXTc = "#881280", "#FF0000", "#0000FF", "#000000"
    mf = font(10, mono=True)

    def el(x, yy, tag, attrs=None, value=None, kids=None):
        b.text(x, yy, "<", mf, TAG)
        xx = x + 7
        b.text(xx, yy, tag, mf, ATT)
        xx += b.measure(tag, mf)[0]
        for k, v in (attrs or []):
            s1 = " " + k + "="
            b.text(xx, yy, s1, mf, ATT); xx += b.measure(s1, mf)[0]
            s2 = '"' + v + '"'
            b.text(xx, yy, s2, mf, VAL); xx += b.measure(s2, mf)[0]
        b.text(xx, yy, ">", mf, TAG)
        xx += 7
        if kids is None:
            b.text(xx, yy, value, mf, TXTc)
            xx += b.measure(value, mf)[0]
            b.text(xx, yy, "</", mf, TAG); xx += 14
            b.text(xx, yy, tag + ">", mf, ATT)
        else:
            for kid in kids:
                yy += 16
                yy = el(x + 22, yy, **kid)
            yy += 16
            b.text(x, yy, "</", mf, TAG)
            b.text(x + 14, yy, tag + ">", mf, ATT)
        return yy

    y = 16
    b.text(24, y, "<?", mf, TAG)
    s = 'xml version="1.0" encoding="UTF-8"'
    b.text(38, y, s, mf, ATT)
    b.text(38 + b.measure(s, mf)[0], y, "?>", mf, TAG)
    y += 16
    b.text(24, y, "<!-- Practical 10 : XML document with an INTERNAL DTD -->", mf, "#236E25")
    y += 16
    b.text(24, y, "<!", mf, TAG)
    b.text(38, y, "DOCTYPE", mf, ATT)
    b.text(38 + b.measure("DOCTYPE", mf)[0], y, " students [", mf, TAG)
    y += 16
    b.text(46, y, "<!ELEMENT students (student+)>  ... the DTD rules ...", mf, "#236E25")
    y += 16
    b.text(24, y, "]>", mf, TAG)
    y += 24
    y = el(24, y, "students", kids=[
        dict(tag="student", attrs=[("id", "S01"), ("type", "regular"), ("active", "yes")],
             kids=[dict(tag="name", value="Student Name One"),
                   dict(tag="rollno", value="CSE2101"),
                   dict(tag="course", value="B.Tech (Computer Science & Engineering)"),
                   dict(tag="semester", value="V"),
                   dict(tag="email", value="student1@college.ac.in"),
                   dict(tag="address", kids=[dict(tag="city", value="Lucknow"),
                                              dict(tag="state", value="Uttar Pradesh"),
                                              dict(tag="pin", value="226001")])]),
        dict(tag="student", attrs=[("id", "S02"), ("type", "regular"), ("active", "yes")],
             kids=[dict(tag="name", value="Student Name Two"),
                   dict(tag="rollno", value="CSE2102"),
                   dict(tag="course", value="B.Tech (Computer Science & Engineering)"),
                   dict(tag="semester", value="V"),
                   dict(tag="email", value="student2@college.ac.in"),
                   dict(tag="address", kids=[dict(tag="city", value="Kanpur"),
                                              dict(tag="state", value="Uttar Pradesh"),
                                              dict(tag="pin", value="208001")])]),
        dict(tag="student", attrs=[("id", "S03"), ("type", "lateral")],
             kids=[dict(tag="name", value="Student Name Three"),
                   dict(tag="rollno", value="CSE2103"),
                   dict(tag="course", value="B.Tech (Information Technology)"),
                   dict(tag="semester", value="V"),
                   dict(tag="email", value="student3@college.ac.in"),
                   dict(tag="remarks", value="Lateral entry student. Marks & grades pending.")]),
    ])
    b.vscrollbar(760, 2, min(740, y + 40), thumb=0.75)
    b.auto_trim()
    b.save(os.path.join(IMG, "out10_xmltree.png"))


def out10b():
    b = Browser("invalid_example.xml - DTD validation",
                "file:///C:/webtech/practical_10/invalid_example.xml", w=780, h=BIG)
    y = 16
    b.rect(20, y, 740, 30, fill="#FDECEA", outline="#CC0000", width=2)
    b.text(32, y + 8, "X   DTD VALIDATION FAILED - invalid_example.xml is NOT valid",
           font(11.5, bold=True, sans=True), "#990000")
    y += 44
    b.text(24, y, "Output of a validating XML parser (rules applied from rules.dtd) :",
           font(10.5, bold=True))
    y += 24
    msgs = [
        "Element student content does not follow the DTD: expecting "
        "(name , rollno , course , semester , email , address?) , "
        "got (name rollno email course semester)",
        "Element student does not carry attribute id  "
        "(declared as  <!ATTLIST student id ID #REQUIRED>)",
    ]
    for m in msgs:
        b.rect(24, y, 62, 18, fill="#CC0000")
        b.centre(24, y + 3, 62, "ERROR", font(9, bold=True, sans=True), "#FFFFFF")
        yy = b.para(96, y + 2, m, font(9.5, mono=True), "#333333", maxw=660, lh=14)
        y = yy + 12
    y += 6
    b.rect(20, y, 740, 66, fill="#E8F5E9", outline="#0B6623", width=2)
    b.text(32, y + 8, "OK   students.xml  and  students_external.xml  follow every rule "
                      "of the DTD :", font(10.5, bold=True, sans=True), "#0B6623")
    b.text(44, y + 28, "students.xml          ->  document is VALID", font(10, mono=True), "#0B6623")
    b.text(44, y + 44, "students_external.xml ->  document is VALID", font(10, mono=True), "#0B6623")
    b.auto_trim()
    b.save(os.path.join(IMG, "out10b_dtd_error.png"))


# =====================================================================
# Practical 11 : XSL output + CSS output
# =====================================================================
def out11():
    b = Browser("Book Catalogue (XML + XSL)",
                "file:///C:/webtech/practical_11/books.xml", w=780, h=BIG)
    y = 16
    b.centre(0, y, 780, "BOOK CATALOGUE - DISPLAYED THROUGH XSL", font(15, bold=True), "#1F4E79")
    y += 34
    rows = [["S. No.", "Title", "Author", "Category", "Year", "Price (Rs.)"],
            ["1", "Computer Networks", "P. Singh", "Network", "2018", "520"],
            ["2", "JavaScript for Beginners", "S. Gupta", "Programming", "2022", "199"],
            ["3", "Learning XML", "Erik Ray", "Programming", "2005", "290"],
            ["4", "SQL Complete Reference", "R. K. Verma", "Database", "2019", "480"],
            ["5", "Web Technology", "A. K. Sharma", "Programming", "2021", "350"]]
    colw = [60, 220, 140, 120, 70, 90]
    yy = y
    rh = 26
    for ri, row in enumerate(rows):
        bg = "#1F4E79" if ri == 0 else ("#EAF1FA" if ri % 2 == 0 else "#FFFFFF")
        b.rect(40, yy, sum(colw), rh, fill=bg)
        xx = 40
        for ci, cell in enumerate(row):
            if ri == 0:
                f, col = font(10, bold=True, sans=True), "#FFFFFF"
            elif ci == 5:
                f = font(10, bold=True)
                col = "#0B6623" if int(cell) < 300 else "#990000"
            else:
                f, col = font(10), "#000000"
            cw, ch = b.measure(cell, f)
            if ci == 1:
                b.text(xx + 6, yy + 6, cell, f, col)
            else:
                b.text(xx + (colw[ci] - cw) / 2, yy + 6, cell, f, col)
            if ci:
                b.line(xx, yy, xx, yy + rh, "#999999")
            xx += colw[ci]
        b.hline(40, yy + rh, sum(colw), "#999999")
        yy += rh
    for ci in range(len(colw) + 1):
        xx = 40 + sum(colw[:ci])
        b.line(xx, y, xx, yy, "#999999")
    yy += 12
    b.centre(0, yy, 780, "Total books : 5  |  Generated from books.xml by books.xsl",
             font(9.5, sans=True), "#666666")
    yy += 16
    b.centre(0, yy, 780, "(rows sorted by <title> with <xsl:sort>; price < Rs. 300 in green, "
                         "otherwise red)", font(9.5, sans=True), "#666666")
    b.auto_trim()
    b.save(os.path.join(IMG, "out11_xsl.png"))


def out11b():
    b = Browser("books_css.xml", "file:///C:/webtech/practical_11/books_css.xml",
                w=780, h=BIG)
    y = 16
    data = [("Web Technology", "A. K. Sharma", "2021", "350"),
            ("Learning XML", "Erik Ray", "2005", "290"),
            ("SQL Complete Reference", "R. K. Verma", "2019", "480"),
            ("JavaScript for Beginners", "S. Gupta", "2022", "199"),
            ("Computer Networks", "P. Singh", "2018", "520")]
    for title, author, year, price in data:
        b.rrect(40, y, 700, 96, 6, fill="#F7F9FC", outline="#1F4E79", width=2)
        b.text(52, y + 10, title, font(14, bold=True), "#1F4E79")
        for dy, pre, val in [(34, "Author : ", author), (52, "Year : ", year),
                             (70, "Price (Rs.) : ", price)]:
            b.text(66, y + dy, pre, font(10.5, bold=True), "#333333")
            b.text(66 + b.measure(pre, font(10.5, bold=True))[0], y + dy, val,
                   font(10.5), "#333333")
        y += 108
    b.auto_trim()
    b.save(os.path.join(IMG, "out11b_cssxml.png"))


if __name__ == "__main__":
    import traceback
    fns = [out01, out02, out03, out04, out05, out06, out07, out08, out09,
           out10, out10b, out11, out11b]
    for fn in fns:
        try:
            fn()
            print("ok  ", fn.__name__)
        except Exception:
            print("FAIL", fn.__name__)
            traceback.print_exc()
