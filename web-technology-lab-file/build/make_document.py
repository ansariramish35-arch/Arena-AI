"""
make_document.py
Builds  Web_Technology_Laboratory_File.docx  and  Web_Technology_Laboratory_File.pdf
from ONE content model, so both files always match.

Layout rules implemented
  * A4 paper, Times New Roman 12 pt body, 14-16 pt bold headings
  * code in Courier New 10 pt
  * front page, index page, then every practical starting on a new page
  * page numbers centred at the bottom of every page
  * index page numbers are the REAL page numbers of the final document
    (two-pass build: pass 1 measures, pass 2 prints the numbers)

Run :  python build/make_document.py
"""
import os
import glob
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, PageBreak, Image, XPreformatted, Table,
                                TableStyle, Flowable, KeepTogether)

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "source")
IMG = os.path.join(ROOT, "images")
OUT = ROOT

PAGE_W, PAGE_H = A4                       # 21.0 x 29.7 cm
M_L = M_R = 2.0 * cm
M_T = 2.0 * cm
M_B = 2.2 * cm
TEXT_W = PAGE_W - M_L - M_R
TEXT_H = PAGE_H - M_T - M_B

IMG_MAX_W = 16.5 * cm
IMG_MAX_H = 14.5 * cm


# ======================================================================
# styles
# ======================================================================
ST = {
    "body":  ParagraphStyle("body", fontName="Times-Roman", fontSize=12, leading=15.5,
                            alignment=TA_LEFT, spaceAfter=6),
    "bodyc": ParagraphStyle("bodyc", fontName="Times-Roman", fontSize=12, leading=15.5,
                            alignment=TA_CENTER, spaceAfter=6),
    "h1":    ParagraphStyle("h1", fontName="Times-Bold", fontSize=16, leading=20,
                            alignment=TA_CENTER, spaceBefore=4, spaceAfter=10),
    "h2":    ParagraphStyle("h2", fontName="Times-Bold", fontSize=14, leading=18,
                            spaceBefore=10, spaceAfter=6),
    "h3":    ParagraphStyle("h3", fontName="Times-Bold", fontSize=12.5, leading=16,
                            spaceBefore=8, spaceAfter=4),
    "code":  ParagraphStyle("code", fontName="Courier", fontSize=10, leading=12.6,
                            spaceAfter=0, spaceBefore=0),
    "cap":   ParagraphStyle("cap", fontName="Times-Italic", fontSize=10.5, leading=13,
                            alignment=TA_CENTER, spaceBefore=4, spaceAfter=10),
    "small": ParagraphStyle("small", fontName="Times-Roman", fontSize=10.5, leading=13.5,
                            spaceAfter=4),
    "blank": ParagraphStyle("blank", fontName="Times-Roman", fontSize=12, leading=26,
                            alignment=TA_CENTER),
}


CODE_CHARS = 78      # Courier 10 pt -> 6.0 pt/char ; text width 17 cm = 481.9 pt


def wrap_code(code, width=CODE_CHARS):
    """hard-wrap source lines so that neither Word nor the PDF has to wrap them
    (both renderers then show exactly the same lines).
    Continuation lines keep the indentation of their own line plus 4 spaces."""
    out = []
    for line in code.split("\n"):
        line = line.rstrip()
        if len(line) <= width:
            out.append(line)
            continue
        indent = len(line) - len(line.lstrip(" "))
        base = line[:indent]
        cont = base + "    "
        words = line.strip().split(" ")
        cur = ""
        first = True
        for w in words:
            prefix = base if first else cont
            limit = width - len(prefix)
            if cur and len(cur) + 1 + len(w) > limit:
                out.append((base if first else cont) + cur)
                cur = w
                first = False
            else:
                cur = (cur + " " + w) if cur else w
            if not first and cur == w and len(w) > width - len(cont):
                # single token longer than the line : hard cut
                while len(cont + cur) > width:
                    out.append(cont + cur[:width - len(cont)])
                    cur = cur[width - len(cont):]
                first = False
        if cur:
            out.append((base if first else cont) + cur)
    return "\n".join(out)


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Marker(Flowable):
    """invisible flowable used to record the page number of a practical"""
    def __init__(self, key):
        Flowable.__init__(self)
        self.key = key
        self.width = 0
        self.height = 0

    def draw(self):
        pass


class Doc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, pagesize=A4,
                                 leftMargin=M_L, rightMargin=M_R,
                                 topMargin=M_T, bottomMargin=M_B,
                                 title="Web Technology Laboratory File",
                                 author="Department of Computer Science & Engineering")
        frame = Frame(M_L, M_B, TEXT_W, TEXT_H, id="main",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="all", frames=[frame],
                                            onPage=self._footer)])
        self.starts = {}
        self.page_fill = {}

    def _footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Roman", 11)
        canvas.drawCentredString(PAGE_W / 2.0, 1.1 * cm, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Marker):
            self.starts[flowable.key] = self.page

    def handle_pageEnd(self):
        self.page_fill[self.page] = self.frame._y / self.frame._height
        BaseDocTemplate.handle_pageEnd(self)


# ======================================================================
# content model
# ======================================================================
def read(*parts):
    with open(os.path.join(SRC, *parts), encoding="utf-8") as fh:
        return fh.read()


PRACTICALS = [
    dict(no=1,
         title="HTML program to create resume preparation using tables.",
         files=[("resume.html", ("practical_01", "resume.html"))],
         images=[("out01_resume.png",
                  "Fig. 1.1 : Resume displayed in the browser - the complete layout is "
                  "built with nested HTML tables")],
         note="The whole resume is one outer table with eight rows; the education and "
              "skill blocks are tables placed inside a table cell (nested tables). "
              "Open resume.html in any browser to get the output shown above."),
    dict(no=2,
         title="HTML program for home page creation using frames.",
         files=[("index.html", ("practical_02", "index.html")),
                ("banner.html", ("practical_02", "banner.html")),
                ("menu.html", ("practical_02", "menu.html")),
                ("home.html", ("practical_02", "home.html")),
                ("about.html", ("practical_02", "about.html")),
                ("courses.html", ("practical_02", "courses.html")),
                ("contact.html", ("practical_02", "contact.html"))],
         images=[("out02_frames.png",
                  "Fig. 2.1 : The three frames - banner (top), menu (left) and content "
                  "(right) - share one browser window")],
         note="Open index.html. The outer frameset divides the window into a 15% banner "
              "row and an 85% row; the inner frameset divides that row into a 20% menu "
              "column and an 80% content column. Every menu link uses target=\"main\", so "
              "only the right frame is replaced. NOTE: frames are a traditional HTML "
              "feature (removed in HTML5); they run in Internet Explorer and in the "
              "legacy mode of modern browsers, which is what the syllabus asks for."),
    dict(no=3,
         title="HTML program for form creation.",
         files=[("form.html", ("practical_03", "form.html"))],
         images=[("out03_form.png",
                  "Fig. 3.1 : The registration form with all common input controls")],
         note="The form uses two fieldset blocks and demonstrates text, password, radio, "
              "checkbox, select, textarea, file, date, number, range, colour and hidden "
              "controls together with submit, reset and button inputs."),
    dict(no=4,
         title="Create a web page to embed an image map in a web page using HTML.",
         files=[("image_map.html", ("practical_04", "image_map.html")),
                ("rectangle.html", ("practical_04", "rectangle.html")),
                ("circle.html", ("practical_04", "circle.html")),
                ("triangle.html", ("practical_04", "triangle.html"))],
         images=[("out04_imagemap.png",
                  "Fig. 4.1 : One image with three hot spots; the pointer is over the "
                  "circle hot spot and its tooltip is shown")],
         note="Keep shapes.png in the same folder as image_map.html. The usemap attribute "
              "of the image is connected to the map named shapemap, and each area defines "
              "one clickable region of shape rect, circle or poly. Clicking a shape opens "
              "its own page."),
    dict(no=5,
         title="Create a web page to fix the hot spots and to show all the related "
               "information when the hot spots are clicked using HTML.",
         files=[("hotspots.html", ("practical_05", "hotspots.html"))],
         images=[("out05_hotspots.png",
                  "Fig. 5.1 : Hot spot 2 (CPU) clicked - its complete information appears "
                  "in the box below the image")],
         note="Keep hardware.png in the same folder. Three hot spots are fixed on the "
              "image with area elements; each one calls the JavaScript function "
              "showInfo() which prints the name, description and a property table of the "
              "clicked part inside the information box, without reloading the page."),
    dict(no=6,
         title="Create a web page to get the coordinates from an image using JavaScript.",
         files=[("coordinates.html", ("practical_06", "coordinates.html"))],
         images=[("out06_coords.png",
                  "Fig. 6.1 : The image clicked at X = 250, Y = 100; all coordinate pairs "
                  "are shown in the table")],
         note="Keep grid.png in the same folder. The onmousemove event fills the move "
              "coordinates continuously and the onclick event fills the click "
              "coordinates. e.offsetX / e.offsetY give the position inside the image, "
              "e.clientX / e.clientY inside the window and e.pageX / e.pageY inside the "
              "document."),
    dict(no=7,
         title="Create a web page with all types of cascading style sheets.",
         files=[("css_all_types.html", ("practical_07", "css_all_types.html")),
                ("external_style.css", ("practical_07", "external_style.css"))],
         images=[("out07_css.png",
                  "Fig. 7.1 : The same page styled by inline, internal and external CSS "
                  "at the same time")],
         note="Keep external_style.css in the same folder. Section 1 uses the style "
              "attribute (inline), section 2 uses the style block in the head (internal) "
              "and section 3 uses the link tag to the external file, so all three types "
              "of cascading style sheets are visible on one page."),
    dict(no=8,
         title="Write HTML/JavaScript to display your CV in navigator, your institute "
               "website, Department website and tutorial website for specific subject.",
         files=[("navigator.html", ("practical_08", "navigator.html")),
                ("cv.html", ("practical_08", "cv.html"))],
         images=[("out08_navigator.png",
                  "Fig. 8.1 : The navigator page with the CV loaded inside the viewer "
                  "frame")],
         note="The drop-down list and the four buttons work as a navigator: JavaScript "
              "reads the selected URL and opens it inside the iframe named viewer with "
              "window.open(url, \"viewer\"). Replace the three sample URLs in the code "
              "with the real addresses of your institute, your department and the "
              "tutorial website of your subject."),
    dict(no=9,
         title="Design HTML form for keeping student record and validate it using "
               "JavaScript.",
         files=[("student_record.html", ("practical_09", "student_record.html"))],
         images=[("out09_validation.png",
                  "Fig. 9.1 : Invalid data entered - every failed check is marked in red "
                  "and the alert box stops the submission")],
         note="validateForm() is called by the onsubmit event. It checks the name, roll "
              "number, 12-digit enrollment number, e-mail pattern, 10-digit mobile "
              "number, password length, password match, a real DD/MM/YYYY date, gender, "
              "course, semester and the acceptance box. If any check fails the function "
              "returns false so the record is not submitted; otherwise an alert confirms "
              "that the record is saved."),
    dict(no=10,
         title="Writing program in XML for creation of DTD, which specifies set of rules.",
         files=[("students.xml", ("practical_10", "students.xml")),
                ("rules.dtd", ("practical_10", "rules.dtd")),
                ("students_external.xml", ("practical_10", "students_external.xml")),
                ("invalid_example.xml", ("practical_10", "invalid_example.xml"))],
         images=[("out10_xmltree.png",
                  "Fig. 10.1 : students.xml opened in a browser - the tree follows every "
                  "rule of the internal DTD"),
                 ("out10b_dtd_error.png",
                  "Fig. 10.2 : A validating parser rejects invalid_example.xml because it "
                  "breaks two rules of the DTD")],
         note="students.xml carries the DTD inside itself (internal DTD) while "
              "students_external.xml takes the same rules from the separate file "
              "rules.dtd through the SYSTEM keyword. The DTD fixes the element order, the "
              "optional elements (address?, remarks?), the required id attribute and the "
              "allowed values of type and active. invalid_example.xml is deliberately "
              "wrong so that the enforcement of the rules can be demonstrated."),
    dict(no=11,
         title="Create a style sheet in CSS/XSL and display the document in Internet "
               "Explorer.",
         files=[("books.xml", ("practical_11", "books.xml")),
                ("books.xsl", ("practical_11", "books.xsl")),
                ("books_css.xml", ("practical_11", "books_css.xml")),
                ("books.css", ("practical_11", "books.css"))],
         images=[("out11_xsl.png",
                  "Fig. 11.1 : books.xml transformed by books.xsl into an HTML table"),
                 ("out11b_cssxml.png",
                  "Fig. 11.2 : The same data displayed through the CSS style sheet "
                  "books.css")],
         note="books.xml points to books.xsl with the xml-stylesheet instruction; the XSL "
              "sheet converts the XML into an HTML table sorted by title. books_css.xml "
              "uses books.css instead, which only changes the look of the XML tree. "
              "Browser compatibility (brief): Internet Explorer supports XSLT 1.0 and the "
              "xml-stylesheet instruction natively, so opening books.xml in IE shows the "
              "formatted table; IE does not support XSLT 2.0 constructs. Firefox and "
              "Chrome also apply the XSL sheet when both files are well formed and are "
              "opened from the same folder. The CSS version works in IE, Firefox and "
              "Chrome, but CSS cannot reorder or restructure elements - only XSL can."),
]

INDEX_NAMES = [
    "HTML program to create resume preparation using tables.",
    "HTML program for home page creation using frames.",
    "HTML program for form creation.",
    "Create a web page to embed an image map in a web page using HTML.",
    "Create a web page to fix the hot spots and to show all the related information "
    "when the hot spots are clicked using HTML.",
    "Create a web page to get the coordinates from an image using JavaScript.",
    "Create a web page with all types of cascading style sheets.",
    "Write HTML/JavaScript to display your CV in navigator, your institute website, "
    "Department website and tutorial website for specific subject.",
    "Design HTML form for keeping student record and validate it using JavaScript.",
    "Writing program in XML for creation of DTD, which specifies set of rules.",
    "Create a style sheet in CSS/XSL and display the document in Internet Explorer.",
]


# ======================================================================
# story builders
# ======================================================================
def front_page():
    s = []
    s.append(Spacer(1, 0.4 * cm))
    s.append(Paragraph("______________________________________________", ST["blank"]))
    s.append(Paragraph("(Name of the University)", ST["bodyc"]))
    s.append(Spacer(1, 0.35 * cm))
    s.append(Paragraph("______________________________________________", ST["blank"]))
    s.append(Paragraph("(Name of the College)", ST["bodyc"]))
    s.append(Spacer(1, 0.5 * cm))
    s.append(Paragraph("<b>Department of Computer Science &amp; Engineering</b>",
                       ST["bodyc"]))
    s.append(Spacer(1, 1.6 * cm))
    s.append(Paragraph("<b><font size=22>WEB TECHNOLOGY LABORATORY FILE</font></b>",
                       ST["bodyc"]))
    s.append(Spacer(1, 0.4 * cm))
    s.append(Paragraph("(A practical report of the Web Technology Laboratory course)",
                       ST["bodyc"]))
    s.append(Spacer(1, 1.8 * cm))
    rows = [
        ("Student Name", ""),
        ("Roll Number", ""),
        ("Enrollment Number", ""),
        ("Course", "B.Tech - Computer Science &amp; Engineering"),
        ("Semester", ""),
        ("Academic Session", ""),
    ]
    data = []
    for k, v in rows:
        val = v if v else "______________________________"
        data.append([Paragraph("<b>%s&nbsp; :</b>" % k, ST["body"]),
                     Paragraph(val, ST["body"])])
    t = Table(data, colWidths=[5.2 * cm, 9.5 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))
    s.append(t)
    s.append(Spacer(1, 1.6 * cm))
    s.append(Paragraph("<b>Submitted To</b>", ST["bodyc"]))
    s.append(Paragraph("______________________________", ST["blank"]))
    s.append(Paragraph("(Faculty Name)", ST["bodyc"]))
    return s


def index_page(pages):
    s = [Paragraph("INDEX", ST["h1"]), Spacer(1, 0.3 * cm)]
    data = [[Paragraph("<b>S. No.</b>", ST["bodyc"]),
             Paragraph("<b>Name of Program</b>", ST["bodyc"]),
             Paragraph("<b>Date</b>", ST["bodyc"]),
             Paragraph("<b>Page No.</b>", ST["bodyc"])]]
    for i, name in enumerate(INDEX_NAMES, start=1):
        data.append([Paragraph(str(i), ST["bodyc"]),
                     Paragraph(name, ST["body"]),
                     Paragraph("", ST["body"]),
                     Paragraph(str(pages.get(i, "")), ST["bodyc"])])
    t = Table(data, colWidths=[1.5 * cm, 10.2 * cm, 2.6 * cm, 2.2 * cm],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.94, 0.96, 0.99)]),
    ]))
    s.append(t)
    return s


def img_flowable(path, max_w=IMG_MAX_W, max_h=IMG_MAX_H):
    from PIL import Image as PILImage
    with PILImage.open(path) as im:
        pw, ph = im.size
    ratio = ph / float(pw)
    w = max_w
    h = w * ratio
    if h > max_h:
        h = max_h
        w = h / ratio
    return Image(path, width=w, height=h)


def practical_story(p, pages):
    s = [PageBreak(), Marker(p["no"])]
    s.append(Paragraph("PRACTICAL No. %d" % p["no"], ST["h1"]))
    s.append(Paragraph("<b>Program :</b> %s" % esc(p["title"]), ST["body"]))
    s.append(Paragraph("Source Code :", ST["h2"]))
    for fname, parts in p["files"]:
        code = read(*parts)
        s.append(Paragraph("<b><font name='Courier-Bold' size=10.5>%s</font></b>"
                           % esc(fname), ST["h3"]))
        s.append(XPreformatted(esc(wrap_code(code)), ST["code"]))
        s.append(Spacer(1, 0.25 * cm))
    s.append(Paragraph("Output / Result :", ST["h2"]))
    s.append(Paragraph(esc(p["note"]), ST["body"]))
    for i, (imgname, caption) in enumerate(p["images"]):
        path = os.path.join(IMG, imgname)
        if i > 0:
            s.append(Spacer(1, 0.3 * cm))
        # image and its caption must never be split across pages
        s.append(KeepTogether([img_flowable(path), Paragraph(caption, ST["cap"])]))
    return s


def build(pages, filename):
    doc = Doc(filename)
    story = []
    story += front_page()
    story.append(PageBreak())
    story += index_page(pages)
    for p in PRACTICALS:
        story += practical_story(p, pages)
    doc.build(story)
    return doc


if __name__ == "__main__":
    pdf = os.path.join(OUT, "Web_Technology_Laboratory_File.pdf")
    # ---- pass 1 : measure where each practical starts
    d1 = build({}, pdf)
    starts = dict(d1.starts)
    print("pass 1 start pages:", starts)
    # ---- pass 2 : print the real numbers in the index
    d2 = build(starts, pdf)
    starts2 = dict(d2.starts)
    if starts2 != starts:
        print("WARN: pagination shifted, doing pass 3")
        d2 = build(starts2, pdf)
        starts2 = dict(d2.starts)
    print("final start pages:", starts2)
    fills = d2.page_fill
    for p in PRACTICALS:
        n = p["no"]
        st = starts2[n]
        nxt = min([starts2[q["no"]] for q in PRACTICALS if q["no"] > n] + [max(fills) + 1])
        last_fill = fills.get(nxt - 1, 0)
        print("  practical %2d : pages %2d-%2d   last-page fill %.2f"
              % (n, st, nxt - 1, last_fill))
    print("total pages:", max(fills))
