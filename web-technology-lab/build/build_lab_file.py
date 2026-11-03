#!/usr/bin/env python3
"""Build the Web Technology Laboratory File (.docx + .pdf) for B.Tech CSE.

The document contains: front page, index, and 11 practicals (source code
read from ../programs). Page numbers in the index are computed with a
two-pass PDF build so they match the final pagination. The .docx is built
with identical fonts/spacings so its pagination matches the PDF.
"""
import os
import sys
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROG = os.path.join(ROOT, "programs")
OUT_DOCX = os.path.join(ROOT, "Web_Technology_Lab_File.docx")
OUT_PDF = os.path.join(ROOT, "Web_Technology_Lab_File.pdf")

MAX_CODE_LINE = 72  # keeps Courier 10pt lines inside the text frame

# ---------------------------------------------------------------- content --
PRACTICALS = [
    dict(no=1,
         title="HTML program to create resume preparation using tables.",
         files=[("resume.html", "p01-resume-table/resume.html")],
         output=[
            ("p", "Opening resume.html in a browser displays a one-page "
                  "resume built entirely with HTML tables: a bordered top "
                  "table holding the photo cell and the candidate's name, "
                  "address, phone and email, followed by Career Objective, "
                  "an Educational Qualification table, a Technical Skills "
                  "table, and a Declaration with a signature line."),
            ("code",
             "+-------+-------------------------------------+\n"
             "| PHOTO |  Ananya Sharma                      |\n"
             "|       |  B.Tech CSE | Phone | Email         |\n"
             "+-------+-------------------------------------+\n"
             "Career Objective\n"
             "Educational Qualification\n"
             "+---------------+--------------+------+-----+\n"
             "| Qualification | Board/Univ.  | Year |  %  |\n"
             "+---------------+--------------+------+-----+\n"
             "| B.Tech CSE    | ... University| 20XX | ..  |\n"
             "+---------------+--------------+------+-----+\n"
             "Technical Skills ... Declaration ... Signature"),
         ]),
    dict(no=2,
         title="HTML program for home page creation using frames.",
         files=[("index.html (frameset)", "p02-homepage-frames/index.html"),
                ("header.html", "p02-homepage-frames/header.html"),
                ("menu.html", "p02-homepage-frames/menu.html"),
                ("welcome.html", "p02-homepage-frames/welcome.html"),
                ("about.html", "p02-homepage-frames/about.html"),
                ("education.html", "p02-homepage-frames/education.html"),
                ("contact.html", "p02-homepage-frames/contact.html"),
                ("footer.html", "p02-homepage-frames/footer.html")],
         output=[
            ("p", "Opening index.html divides the browser window into "
                  "frames (traditional HTML 4.01 frameset): a dark-blue "
                  "header (15%), a middle row with the menu (25%) and the "
                  "main content frame, and a footer (12%). Clicking a menu "
                  "link loads that page inside the main frame because of "
                  "target=\"main\"."),
            ("code",
             "+------------------------------------------+\n"
             "|      MY PERSONAL HOME PAGE (header)      | 15%\n"
             "+---------+--------------------------------+\n"
             "| Menu    |  Welcome to my home page!      |\n"
             "| - Home  |  (main frame content)          |\n"
             "| - About |                                |\n"
             "+---------+--------------------------------+\n"
             "|     (c) 2026 My Home Page (footer)       | 12%\n"
             "+------------------------------------------+"),
         ]),
    dict(no=3,
         title="HTML program for form creation.",
         files=[("form.html", "p03-form/form.html")],
         output=[
            ("p", "Opening form.html shows a centered, bordered Student "
                  "Registration Form with text, password, radio, checkbox, "
                  "dropdown, textarea and file fields, plus Submit and "
                  "Reset buttons."),
            ("code",
             "+--------------------------------------+\n"
             "|      Student Registration Form       |\n"
             "|  Full Name:  [....................]  |\n"
             "|  Password:   [....................]  |\n"
             "|  Gender: (.) Male  ( ) Female        |\n"
             "|  Hobbies: [x] Reading [ ] Sports     |\n"
             "|  Course:  [ B.Tech CSE          v ]  |\n"
             "|  Address: [........................] |\n"
             "|           [Submit]   [Reset]         |\n"
             "+--------------------------------------+"),
         ]),
    dict(no=4,
         title="Create a web page to embed an image map in a web page "
               "using HTML.",
         files=[("image-map.html", "p04-image-map/image-map.html"),
                ("campus-map.jpg (image used by the map)",
                 "p04-image-map/campus-map.jpg")],
         output=[
            ("p", "Opening image-map.html displays the campus map image "
                  "with an embedded client-side image map (<img usemap> + "
                  "<map>/<area>). The mouse pointer changes over each "
                  "rectangular area, and clicking an area jumps to its "
                  "description below the image."),
            ("code",
             "Campus Map - Image Map\n"
             "[ campus-map.jpg 600x400 with clickable blocks ]\n"
             "  Library | Computer Labs | Canteen\n"
             "  Auditorium      |  Sports Ground\n"
             "---\n"
             "Library: Central library with reading halls ..."),
         ]),
    dict(no=5,
         title="Create a web page to fix the hot spots and to show all the "
               "related information when the hot spots are clicked using "
               "HTML.",
         files=[("hotspots.html", "p05-hotspots/hotspots.html"),
                ("campus-map.jpg (image with the hot spots)",
                 "p05-hotspots/campus-map.jpg")],
         output=[
            ("p", "Opening hotspots.html shows the same campus map with "
                  "fixed hot spots. Clicking any hot spot runs the "
                  "JavaScript showInfo() function, which displays that "
                  "building's related information in the panel below the "
                  "image - without reloading the page."),
            ("code",
             "Campus Map - Hot Spots\n"
             "[ campus map; click a building ]\n"
             "+--------------------------------------------+\n"
             "| Library                                    |\n"
             "| Central library: 10,000+ books, reading   |\n"
             "| halls, Wi-Fi.                              |\n"
             "+--------------------------------------------+"),
         ]),
    dict(no=6,
         title="Create a web page to get the coordinates from an image "
               "using JavaScript.",
         files=[("coordinates.html", "p06-image-coordinates/coordinates.html"),
                ("lab-map.jpg (image clicked for coordinates)",
                 "p06-image-coordinates/lab-map.jpg")],
         output=[
            ("p", "Opening coordinates.html shows a gridded map. Clicking "
                  "anywhere on the image calls getCoords(event); JavaScript "
                  "reads offsetX/offsetY and fills the X and Y text boxes "
                  "and prints the message below."),
            ("code",
             "Click on the image to get its coordinates\n"
             "[ gridded map 500x350 - click anywhere ]\n"
             "X coordinate: [237]   Y coordinate: [148]\n"
             "You clicked at coordinates (237, 148)"),
         ]),
    dict(no=7,
         title="Create a web page with all types of cascading style sheets.",
         files=[("css-types.html", "p07-css-types/css-types.html"),
                ("styles.css (external style sheet)",
                 "p07-css-types/styles.css")],
         output=[
            ("p", "Opening css-types.html shows the same heading/paragraph "
                  "styled three times: blue (inline style attribute), red "
                  "(internal <style> in the head) and green (external "
                  "styles.css linked with <link>)."),
            ("code",
             "Three Ways of Using CSS\n"
             "+------------------------------------------+\n"
             "| 1. Inline CSS (style attribute)  [blue] |\n"
             "+------------------------------------------+\n"
             "+------------------------------------------+\n"
             "| 2. Internal CSS (<style> in head) [red]  |\n"
             "+------------------------------------------+\n"
             "+------------------------------------------+\n"
             "| 3. External CSS (styles.css)    [green]  |\n"
             "+------------------------------------------+"),
         ]),
    dict(no=8,
         title="Write HTML/JavaScript to display your CV in navigator, your "
               "institute website, Department website and tutorial "
               "website for specific subject.",
         files=[("links.html", "p08-cv-links/links.html"),
                ("cv.html (CV page opened in the navigator)",
                 "p08-cv-links/cv.html")],
         output=[
            ("p", "Opening links.html shows four buttons. Each button "
                  "calls a JavaScript function that uses window.open() to "
                  "display the page in the browser: the local CV page, the "
                  "institute website, the department website, and an HTML "
                  "tutorial site (replace the example URLs with your own)."),
            ("code",
             "Quick Links\n"
             "Click a button to open the page in the browser:\n"
             "[ My CV ]  -> opens cv.html\n"
             "[ Institute Website ]  -> opens institute site\n"
             "[ Department Website ] -> opens CSE department site\n"
             "[ Tutorial Website (HTML - W3Schools) ]"),
         ]),
    dict(no=9,
         title="Design HTML form for keeping student record and validate it "
               "using JavaScript.",
         files=[("student-record.html",
                 "p09-student-record-validation/student-record.html")],
         output=[
            ("p", "Opening student-record.html shows the Student Record "
                  "form. On submit, JavaScript validateForm() checks every "
                  "field (name letters-only, alphanumeric roll no., email "
                  "pattern, 10-digit phone, marks 0-100). Invalid input "
                  "shows the errors in red; valid input shows a success "
                  "message."),
            ("code",
             "Student Record\n"
             "Name: [abc]  Roll No.: [12!]  Marks: [120]\n"
             "Errors:\n"
             "Name must contain letters only (min 3).\n"
             "Roll No. must be alphanumeric.\n"
             "Marks must be a number between 0 and 100.\n"
             "--- valid input ---\n"
             "Record saved successfully for Ananya Sharma!"),
         ]),
    dict(no=10,
         title="Writing program in XML for creation of DTD, which specifies "
               "set of rules.",
         files=[("students.xml (XML with internal DTD)",
                 "p10-xml-dtd/students.xml"),
                ("students-external.dtd (external DTD)",
                 "p10-xml-dtd/students-external.dtd"),
                ("students-external.xml (XML using external DTD)",
                 "p10-xml-dtd/students-external.xml")],
         output=[
            ("p", "Opening students.xml in a browser displays the XML "
                  "document as a collapsible tree. The internal DTD subset "
                  "declares the rules: students contains one or more "
                  "student elements; each student has name, roll, course, "
                  "marks and a required id attribute. students-external.xml "
                  "follows the same rules kept in the external file "
                  "students-external.dtd."),
            ("code",
             "- <students>\n"
             "  - <student id=\"S101\">\n"
             "      <name>Ananya Sharma</name>\n"
             "      <roll>2301234</roll>\n"
             "      <course>B.Tech CSE</course>\n"
             "      <marks>88</marks>\n"
             "  + <student id=\"S102\"> ...\n"
             "  + <student id=\"S103\"> ..."),
         ]),
    dict(no=11,
         title="Create a style sheet in CSS/XSL and display the document "
               "in Internet Explorer.",
         files=[("students.xml (with xml-stylesheet instruction)",
                 "p11-xml-xsl/students.xml"),
                ("students.xsl (XSL style sheet)",
                 "p11-xml-xsl/students.xsl")],
         output=[
            ("p", "Opening students.xml in a browser applies students.xsl "
                  "automatically (through the <?xml-stylesheet?> "
                  "instruction) and renders a styled HTML table of the "
                  "student records. Browser compatibility: XSLT 1.0 is "
                  "supported by Internet Explorer 5.5+ and by all modern "
                  "browsers (Chrome, Edge, Firefox), so the XML file can be "
                  "opened directly - no web server is needed."),
            ("code",
             "Student Records\n"
             "+------+---------------+---------+------------+-------+\n"
             "| ID   | Name          | Roll No.| Course     | Marks |\n"
             "+------+---------------+---------+------------+-------+\n"
             "| S101 | Ananya Sharma | 2301234 | B.Tech CSE |   88  |\n"
             "| S102 | Rahul Verma   | 2301235 | B.Tech CSE |   76  |\n"
             "| S103 | Priya Singh   | 2301236 | B.Tech CSE |   91  |\n"
             "+------+---------------+---------+------------+-------+"),
         ]),
]

FRONT_LINES = [
    # (text, size, bold, space_after, leading)
    ("", 12, False, 30, 14),
    ("University Name : ______________________________", 12, False, 10, 14),
    ("College Name    : ______________________________", 12, False, 28, 14),
    ("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", 14, True, 34, 17),
    ("WEB TECHNOLOGY LABORATORY FILE", 16, True, 34, 19),
    ("Name             : ______________________", 12, False, 8, 14),
    ("Roll Number      : ______________________", 12, False, 8, 14),
    ("Enrollment No.   : ______________________", 12, False, 8, 14),
    ("Course           : B.Tech CSE", 12, False, 8, 14),
    ("Semester         : ______________", 12, False, 8, 14),
    ("Academic Session : ______________", 12, False, 28, 14),
    ("Submitted To     : ______________________", 12, False, 2, 14),
    ("(Faculty Name)", 12, False, 0, 14),
]


def read_code(rel):
    path = os.path.join(PROG, rel)
    if rel.endswith((".jpg", ".jpeg", ".png")):
        return "[binary image file - see the programs folder]"
    with open(path, "r", encoding="utf-8") as f:
        code = f.read().rstrip("\n")
    for i, line in enumerate(code.split("\n"), 1):
        if len(line) > MAX_CODE_LINE:
            raise SystemExit(f"line too long ({len(line)}): {rel}:{i}")
    return code


# ------------------------------------------------------------------- PDF ---
def build_pdf(path, page_numbers):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
                                    Paragraph, PageBreak, Table, TableStyle)

    W, H = A4
    M = 72  # 1 inch margins

    BODY = ParagraphStyle("body", fontName="Times-Roman", fontSize=12,
                          leading=14, spaceBefore=0, spaceAfter=6)
    H1 = ParagraphStyle("h1", fontName="Times-Bold", fontSize=16,
                        leading=19, spaceBefore=0, spaceAfter=6)
    H2 = ParagraphStyle("h2", fontName="Times-Bold", fontSize=14,
                        leading=17, spaceBefore=10, spaceAfter=4)
    LBL = ParagraphStyle("lbl", fontName="Times-BoldItalic", fontSize=12,
                         leading=14, spaceBefore=6, spaceAfter=2)
    CODE = ParagraphStyle("code", fontName="Courier", fontSize=10,
                          leading=12, spaceBefore=2, spaceAfter=8,
                          backColor=colors.HexColor("#F2F2F2"),
                          borderPadding=3)
    CTR = ParagraphStyle("ctr", parent=BODY, alignment=TA_CENTER)
    CELL = ParagraphStyle("cell", fontName="Times-Roman", fontSize=12,
                          leading=14)

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Roman", 10)
        canvas.drawCentredString(W / 2, 45, str(canvas.getPageNumber()))
        canvas.restoreState()

    class LabDoc(BaseDocTemplate):
        def __init__(self, fn, **kw):
            super().__init__(fn, pagesize=A4, **kw)
            frame = Frame(M, M, W - 2 * M, H - 2 * M, id="main")
            self.addPageTemplates(
                [PageTemplate(id="page", frames=[frame], onPage=footer)])
            self.practical_pages = {}

        def afterFlowable(self, fl):
            pno = getattr(fl, "_pno", None)
            if pno is not None:
                self.practical_pages[pno] = self.page

    doc = LabDoc(path, leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M)
    story = []

    # ---- front page ----
    for text, size, bold, after, lead in FRONT_LINES:
        st = ParagraphStyle("f", parent=CTR, fontName="Times-Bold" if bold
                            else "Times-Roman", fontSize=size, leading=lead,
                            spaceAfter=after)
        story.append(Paragraph(escape(text), st))

    # ---- index ----
    story.append(PageBreak())
    idx = ParagraphStyle("idx", parent=H1, alignment=TA_CENTER, spaceAfter=12)
    story.append(Paragraph("INDEX", idx))
    header = ["S.No.", "Name of Program", "Date", "Page No."]
    rows = [[Paragraph(f"<b>{h}</b>", CELL) for h in header]]
    for pr in PRACTICALS:
        rows.append([
            Paragraph(str(pr["no"]), CELL),
            Paragraph(escape(pr["title"]), CELL),
            Paragraph("", CELL),
            Paragraph(str(page_numbers.get(pr["no"], "")), CELL),
        ])
    t = Table(rows, colWidths=[39.6, 264.0, 72.0, 75.6])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)

    # ---- practicals ----
    for pr in PRACTICALS:
        story.append(PageBreak())
        h = Paragraph(escape(f"Practical No. {pr['no']}"), H1)
        h._pno = pr["no"]
        story.append(h)
        story.append(Paragraph(
            f"<b>Program:</b> {escape(pr['title'])}", H2))
        story.append(Paragraph("Source Code:", H2))
        for disp, rel in pr["files"]:
            story.append(Paragraph(escape(f"File: {disp}"), LBL))
            story.append(Paragraph(
                escape(read_code(rel)).replace("\n", "<br/>"), CODE))
        story.append(Paragraph("Output/Result:", H2))
        story.append(Paragraph(
            "Representative browser output (open the program file in a "
            "browser to see the actual page):", BODY))
        for kind, text in pr["output"]:
            if kind == "p":
                story.append(Paragraph(escape(text), BODY))
            else:
                story.append(Paragraph(
                    escape(text).replace("\n", "<br/>"), CODE))

    doc.build(story)
    return doc.practical_pages


# ------------------------------------------------------------------ DOCX ---
def build_docx(path, page_numbers):
    from docx import Document
    from docx.shared import Pt, Inches, Mm
    from docx.enum.text import (WD_ALIGN_PARAGRAPH, WD_BREAK,
                                WD_LINE_SPACING)
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    TNR = "Times New Roman"
    doc = Document()

    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)      # A4
    sec.left_margin = sec.right_margin = Inches(1)
    sec.top_margin = sec.bottom_margin = Inches(1)

    normal = doc.styles["Normal"]
    normal.font.name = TNR
    normal.font.size = Pt(12)

    # footer with page number field
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.paragraph_format.space_before = Pt(0)
    fp.paragraph_format.space_after = Pt(0)
    run = fp.add_run()
    run.font.name = TNR
    run.font.size = Pt(10)
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve")
    it.text = "PAGE"
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
    run._r.append(f1); run._r.append(it); run._r.append(f2)

    def para(text="", size=12, bold=False, italic=False, font=TNR,
             align=None, before=0, after=6, lead=14, page_break=False,
             shade=None):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(before)
        pf.space_after = Pt(after)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.line_spacing = Pt(lead)
        if align is not None:
            pf.alignment = align
        if page_break:
            br = p.add_run()
            br.add_break(WD_BREAK.PAGE)
        if text:
            r = p.add_run(text)
            r.font.name = font
            r.font.size = Pt(size)
            r.bold = bold
            r.italic = italic
            r._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), font)
        if shade:
            pPr = p._p.get_or_add_pPr()
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"), "clear")
            shd.set(qn("w:fill"), shade)
            pPr.append(shd)
        return p

    C = WD_ALIGN_PARAGRAPH.CENTER

    # ---- front page ----
    for text, size, bold, after, lead in FRONT_LINES:
        para(text, size=size, bold=bold, align=C, after=after, lead=lead)

    # ---- index ----
    para("INDEX", size=16, bold=True, align=C, after=12, lead=19,
         page_break=True)
    t = doc.add_table(rows=1 + len(PRACTICALS), cols=4)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    layout = OxmlElement("w:tblLayout"); layout.set(qn("w:type"), "fixed")
    t._tbl.tblPr.append(layout)
    widths = [Inches(0.55), Inches(3.67), Inches(1.0), Inches(1.05)]
    headers = ["S.No.", "Name of Program", "Date", "Page No."]
    for ri, row in enumerate(t.rows):
        for ci, cell in enumerate(row.cells):
            cell.width = widths[ci]
            p = cell.paragraphs[0]
            pf = p.paragraph_format
            pf.space_before = Pt(2); pf.space_after = Pt(2)
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pf.line_spacing = Pt(14)
            if ri == 0:
                r = p.add_run(headers[ci]); r.bold = True
            elif ci == 0:
                r = p.add_run(str(PRACTICALS[ri - 1]["no"]))
            elif ci == 1:
                r = p.add_run(PRACTICALS[ri - 1]["title"])
            elif ci == 3:
                r = p.add_run(str(page_numbers.get(
                    PRACTICALS[ri - 1]["no"], "")))
            else:
                r = p.add_run("")
            r.font.name = TNR
            r.font.size = Pt(12)

    # ---- practicals ----
    for pr in PRACTICALS:
        para(f"Practical No. {pr['no']}", size=16, bold=True,
             after=6, lead=19, page_break=True)
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(10); pf.space_after = Pt(4)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.line_spacing = Pt(17)
        r1 = p.add_run("Program: "); r1.bold = True; r1.font.size = Pt(14)
        r1.font.name = TNR
        r2 = p.add_run(pr["title"]); r2.font.size = Pt(14); r2.font.name = TNR
        para("Source Code:", size=14, bold=True, before=10, after=4, lead=17)
        for disp, rel in pr["files"]:
            para(f"File: {disp}", size=12, bold=True, italic=True,
                 before=6, after=2, lead=14)
            para(read_code(rel), size=10, font="Consolas",
                 before=2, after=8, lead=12, shade="F2F2F2")
        para("Output/Result:", size=14, bold=True, before=10, after=4, lead=17)
        para("Representative browser output (open the program file in a "
             "browser to see the actual page):", after=6)
        for kind, text in pr["output"]:
            if kind == "p":
                para(text, after=6)
            else:
                para(text, size=10, font="Consolas", before=2, after=8,
                     lead=12, shade="F2F2F2")

    doc.save(path)


def main():
    # pass 1: compute real page numbers; pass 2: write the final PDF
    tmp = os.path.join(ROOT, "build", "_pass1.pdf")
    pages = build_pdf(tmp, {})
    build_pdf(OUT_PDF, pages)
    os.remove(tmp)
    build_docx(OUT_DOCX, pages)
    print("practical start pages:", pages)
    print("wrote:", OUT_PDF)
    print("wrote:", OUT_DOCX)


if __name__ == "__main__":
    sys.exit(main())
