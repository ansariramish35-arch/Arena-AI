"""Build the theory-only summer training report PDF and editable DOCX.

Run: python generate_report.py (requires reportlab, python-docx, pymupdf).
Source certificate and cover-template PDFs remain in the user's upload folder.
"""
from pathlib import Path
import math
import tempfile
import shutil
import pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'deliverables'
OUT.mkdir(exist_ok=True)
UPLOAD = Path('/tmp/arena-coding-uploads')
CERT = UPLOAD / 'Certificate.pdf (2) (1).pdf'
COVER = UPLOAD / 'SY_ebdfbfee-68a3-4a45-b40f-753d7d7b0f6b_58 (1).pdf'
STUDENT = 'Mayank Kumar'
TITLE = 'Print Hello World in Python'
W, H = A4
M = 64
BODY_W = W - 2*M

from hello_world_content import pages, refs
from hello_world_diagrams import build as build_diagram

# Render the same explanatory diagrams for both the PDF and editable DOCX.
visual_directory = Path(tempfile.mkdtemp(prefix='hello-world-visuals-'))
visual_paths = {}
for number, study_page in enumerate(pages, start=1):
    if study_page['visual']:
        visual_paths[number] = build_diagram(study_page['visual'], visual_directory / f'{number:02d}.png')

# ---------- PDF rendering ----------
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
font_dir=ROOT/'report'/'assets'/'fonts'
for font_name, file_name in [('TNR','Tinos-Regular.ttf'),('TNR-B','Tinos-Bold.ttf'),('TNR-I','Tinos-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(font_name,str(font_dir/file_name)))
registerFontFamily('TNR', normal='TNR', bold='TNR-B', italic='TNR-I', boldItalic='TNR-B')

navy = HexColor('#172840')
muted = HexColor('#576170')
light = HexColor('#EEF2F6')
style = ParagraphStyle('body', fontName='TNR', fontSize=12, leading=12, alignment=TA_LEFT, textColor=black)
style_note = ParagraphStyle('note', parent=style, fontSize=10, leading=11, textColor=muted)

def para(c, text, y, x=M, width=BODY_W, note=False):
    st = style_note if note else style
    p = Paragraph(text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), st)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y-h)
    return y-h-(8 if not note else 5)

def lines_center(c, lines, y, size=12, bold=False, gap=18):
    c.setFont('TNR-B' if bold else 'TNR', size)
    for line in lines:
        c.drawCentredString(W/2, y, line)
        y -= gap
    return y

def header(c, title, number):
    c.setFillColor(navy)
    c.setFont('TNR-B', 12)
    c.drawString(M, H-55, title)
    c.setStrokeColor(navy)
    c.line(M, H-63, W-M, H-63)
    c.setFillColor(muted)
    c.setFont('TNR', 9)
    c.drawString(M, 42, 'Print Hello World in Python | Mayank Kumar')
    c.drawRightString(W-M, 42, str(number))
    c.setFillColor(black)

def roman(n):
    pairs=[(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]
    s=''
    for val, letter in pairs:
        while n>=val: s+=letter; n-=val
    return s

def prelim_footer(c, n):
    c.setFillColor(muted); c.setFont('TNR', 10)
    c.drawCentredString(W/2, 42, roman(n)); c.setFillColor(black)

def draw_table(c, rows, y, widths=None):
    ncols = len(rows[0]); widths = widths or [BODY_W/ncols]*ncols
    cell_style = ParagraphStyle('cell', fontName='TNR', fontSize=10, leading=11)
    for ri, row in enumerate(rows):
        ps=[]; heights=[]
        for txt, width in zip(row, widths):
            p=Paragraph(str(txt).replace('&','&amp;').replace('<','&lt;'), cell_style)
            _,h=p.wrap(width-12,1000); ps.append(p); heights.append(h)
        rh=max(heights)+12
        if ri == 0:
            c.setFillColor(navy); c.rect(M,y-rh,BODY_W,rh,fill=1,stroke=0)
        elif ri % 2 == 0:
            c.setFillColor(light); c.rect(M,y-rh,BODY_W,rh,fill=1,stroke=0)
        c.setFillColor(white if ri==0 else black)
        x=M
        for p,width in zip(ps,widths):
            # Paragraph has its own color; reverse header by using white canvas via text object instead
            if ri==0:
                c.setFont('TNR-B',10)
                c.drawString(x+6,y-13,str(row[ps.index(p)])[:40])
            else: p.drawOn(c,x+6,y-6-p.height)
            x+=width
        y-=rh
    c.setFillColor(black)
    return y-8

def draw_flow(c, items, y):
    count=len(items); gap=8; boxw=(BODY_W-gap*(count-1))/count
    for i, item in enumerate(items):
        x=M+i*(boxw+gap)
        c.setFillColor(light); c.setStrokeColor(navy)
        c.roundRect(x,y-48,boxw,48,5,fill=1,stroke=1)
        c.setFillColor(navy); c.setFont('TNR-B',9)
        words=item.split(); parts=[]; acc=''
        for word in words:
            candidate=(acc+' '+word).strip()
            if stringWidth(candidate,'TNR-B',9)>boxw-10 and acc:
                parts.append(acc); acc=word
            else: acc=candidate
        if acc: parts.append(acc)
        for j,line in enumerate(parts[:3]):
            c.drawCentredString(x+boxw/2,y-22+((len(parts)-1)*5)-j*11,line)
        if i<count-1:
            c.setFont('TNR-B',11); c.drawCentredString(x+boxw+gap/2,y-28,'>')
    c.setFillColor(black)
    return y-58

def draw_chart(c,y):
    groups=[('Letters',10),('Punctuation',2),('Space',1)]
    x0=M+38; yy=y-215; barw=78; scale=14
    c.setStrokeColor(navy); c.line(x0-15,yy,W-M-14,yy)
    for i,(label,value) in enumerate(groups):
        x=x0+24+i*145
        c.setFillColor([HexColor('#547D9D'),HexColor('#829AB3'),HexColor('#B8C8D8')][i])
        c.rect(x,yy,barw,value*scale,fill=1,stroke=0)
        c.setFillColor(black); c.setFont('TNR',10)
        c.drawCentredString(x+barw/2,yy-17,label)
        c.drawCentredString(x+barw/2,yy+value*scale+6,str(value))
    return yy-42

def render_main(c, d, number):
    header(c,d['title'],number); y=H-83
    for text in d['paras']: y=para(c,text,y)-5
    for text in d['bullets']: y=para(c,'•  '+text,y,x=M+11,width=BODY_W-11)
    if d['table']: y=draw_table(c,d['table'],y-5)
    if d['flow']: y=draw_flow(c,d['flow'],y-7)
    if d['fig']: y=draw_chart(c,y-5)
    if d['note']: y=para(c,d['note'],y-3,note=True)
    if d['visual']:
        visual_height = BODY_W*360/1320
        y -= visual_height+6
        c.drawImage(str(visual_paths[number]),M,y,width=BODY_W,height=visual_height)
        y=para(c,d['visual_caption'],y-4,note=True)
    if y<71: raise RuntimeError(f"Page {number} overflows: y={y:.1f} {d['title']}")
    c.showPage()

# Prepare high-quality images from authentic supplied PDFs; copies for editing are optional.
cert_doc=pymupdf.open(CERT)
cert_pix=cert_doc[0].get_pixmap(matrix=pymupdf.Matrix(2.3,2.3),alpha=False)
cert_img=OUT/'certificate_page.png'; cert_pix.save(cert_img)
cover_doc=pymupdf.open(COVER)
# Crop out only the University's emblem from the sample cover.
cover_page=cover_doc[0]
logo_clip=pymupdf.Rect(231,432,386,557)
logo_pix=cover_page.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=logo_clip,alpha=False)
logo_img=OUT/'university_emblem_from_template.png'; logo_pix.save(logo_img)

pdf_path=OUT/'Hello_World_Python_Internship_Report.pdf'
c=canvas.Canvas(str(pdf_path),pagesize=A4)
c.setTitle(TITLE+' - Summer Internship Report')
c.setAuthor(STUDENT)
# Cover: arranged to match the supplied University template rather than reproducing its typo/date.
c.setStrokeColor(black); c.setLineWidth(.7); c.rect(33,34,W-66,H-68,fill=0,stroke=1)
y=H-80
y=lines_center(c,['INDUSTRIAL TRAINING REPORT'],y,18,True,25)-8
y=lines_center(c,['on'],y,12,True,25)
y=lines_center(c,['“Print Hello World in Python”'],y,15,True,21)-5
y=lines_center(c,['by','Mayank Kumar [ROLL NUMBER TO FILL]'],y,13,True,26)-4
y=lines_center(c,['Submitted in partial fulfillment of the requirements for the award of the degree','of'],y,11,True,22)-4
y=lines_center(c,['BACHELOR OF TECHNOLOGY','in','COMPUTER SCIENCE & ENGINEERING'],y,15,True,24)-2
y=lines_center(c,['from','EWB EDUTECH PRIVATE LIMITED (EWB Courses)'],y,12,True,23)-4
c.drawImage(str(logo_img),W/2-57,y-81,width=114,height=71,mask='auto'); y-=107
y=lines_center(c,['Submitted to','DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING','FACULTY OF ENGINEERING & TECHNOLOGY','UNIVERSITY OF LUCKNOW, LUCKNOW'],y,11,True,20)-7
lines_center(c,['November 2026'],y,11,True,18)
c.showPage()
# preliminary i: declaration
c.setFont('TNR-B',12); c.drawCentredString(W/2,H-90,'DECLARATION')
y=H-135
for t in [
    'I, Mayank Kumar, declare that this report titled “Print Hello World in Python” is a theory-based academic case study for the B.Tech CSE summer training submission. The syntax examples, manually derived counts, diagrams and predicted behaviours explain a beginner concept; no software product, deployment, executed test or empirical result is claimed.',
    'The attached student-supplied certificate documents completion of a one-month Python Programming internship. It does not identify Hello World as an assigned internship project. This topic is a separate academic learning study and should be described as actual internship work only if independently supported.',
    'All illustrative statements and character counts are based on public Python concepts or manually checkable reasoning. No restricted organisation information is included. The supplied documents and general reference sources are listed at the end of this report.',
]: y=para(c,t,y)-11
y-=42
c.setFont('TNR',12)
c.drawString(M,y,'Signature: ________________________')
c.drawString(M,y-29,'Name: Mayank Kumar')
c.drawString(M,y-58,'Roll No.: [TO FILL]')
c.drawString(M,y-87,'Section: [TO FILL]')
c.drawString(M,y-116,'Date: [TO FILL]')
prelim_footer(c,1); c.showPage()
# preliminary ii: certificate as colour photocopy, correctly not altered
c.setFont('TNR-B',12); c.drawCentredString(W/2,H-64,'TRAINING / INTERNSHIP CERTIFICATE')
img=ImageReader(str(cert_img)); iw,ih=img.getSize(); dw=BODY_W; dh=dw*ih/iw
c.drawImage(img,M,H-105-dh,width=dw,height=dh)
y=H-118-dh
para(c,'Colour reproduction of the student-provided original certificate. Issued 15 July 2026; the document states a one-month Python Programming internship. The original PDF should be used for final printing if higher fidelity is required.',y,note=True)
prelim_footer(c,2); c.showPage()
# preliminary iii-iv
for n,title,content in [
(3,'ABSTRACT',[
'This report presents a theory-only study of the introductory Python 3 example print("Hello, World!"). The small example is used to explain source text, function calls, arguments, string literals, standard output and the normal line ending. It is not a claim that a working model or company deliverable was produced.',
'The report breaks the greeting into manually counted character categories and discusses exact-output comparison, variants, common syntax mistakes, conceptual execution flow and a proposed verification plan. A bar chart represents ten letters, two punctuation marks and one space in the thirteen-character visible greeting. It is a manually derived illustration, not an experiment or performance result.',
'The supplied certificate confirms a one-month Python Programming internship for Mayank Kumar but does not identify this topic as the assigned internship project. Accordingly, this report is a separate academic application of beginner Python concepts.',
'Keywords: Python 3, Hello World, print, string literal, standard output, conceptual study.',
]),
(4,'ACKNOWLEDGEMENT',[
'I thank the Department of Computer Science and Engineering, Faculty of Engineering & Technology, University of Lucknow, for the prescribed report format and the opportunity to develop a careful account of a basic Python concept.',
'I acknowledge EWB EDUTECH PRIVATE LIMITED / EWB Courses for the Python Programming internship documented by the attached completion certificate. This particular Hello World study is presented as a separate academic explanation, not as a verified company-assigned project.',
'I thank the faculty reviewing this report for any guidance on its clarity and presentation. The explanatory interpretations and any errors remain my responsibility.',
'Before submitting, the student should amend this acknowledgement to reflect the support actually received.',
])]:
    c.setFont('TNR-B',12); c.drawCentredString(W/2,H-90,title); y=H-135
    for t in content: y=para(c,t,y)-13
    prelim_footer(c,n); c.showPage()
# preliminary v: contents
c.setFont('TNR-B',12); c.drawCentredString(W/2,H-75,'TABLE OF CONTENTS')
y=H-105
entries=[('Declaration','i'),('Training / Internship Certificate','ii'),('Abstract','iii'),('Acknowledgement','iv'),('Table of Contents','v'),('List of Tables','vi'),('List of Figures','vii')]
entries += [(p['title'],str(i)) for i,p in enumerate(pages,1)]
entries += [('References',str(len(pages)+1)),('Appendix A: Glossary',str(len(pages)+2)),('Appendix B: Submission Checklist',str(len(pages)+3))]
c.setFont('TNR',8.5)
for title,num in entries:
    if y<63: raise RuntimeError('TOC overflow')
    c.drawString(M,y,title); c.drawRightString(W-M,y,num); y-=11.5
prelim_footer(c,5); c.showPage()
# preliminary vi: list of tables
c.setFont('TNR-B',12); c.drawCentredString(W/2,H-75,'LIST OF TABLES')
y=H-108; table_num=0
for i,p in enumerate(pages,1):
    if p['table']:
        table_num+=1; label=p['note'].split('.')[0]+'. '+p['note'].split('. ',1)[1] if p['note'] else f'Table {table_num}'
        c.setFont('TNR',10); c.drawString(M,y,label[:85]); c.drawRightString(W-M,y,str(i)); y-=21
prelim_footer(c,6); c.showPage()
# preliminary vii: list of figures
c.setFont('TNR-B',12); c.drawCentredString(W/2,H-75,'LIST OF FIGURES')
y=H-108
for i,p in enumerate(pages,1):
    captions = ([p['note']] if p['flow'] or p['fig'] else [])
    if p['visual_caption']: captions.append(p['visual_caption'])
    for label in captions:
        if y<63: raise RuntimeError('List of figures overflow')
        c.setFont('TNR',9); c.drawString(M,y,label[:88]); c.drawRightString(W-M,y,str(i)); y-=16
prelim_footer(c,7); c.showPage()
for i,p in enumerate(pages,1): render_main(c,p,i)
# References follow the 44 main study pages.
header(c,'REFERENCES',len(pages)+1); y=H-93
for j,r in enumerate(refs,1): y=para(c,f'{j}. {r}',y)-12
c.showPage()
header(c,'APPENDIX A: GLOSSARY',len(pages)+2); y=H-95
for term,meaning in [
    ('Source statement', 'Written Python instruction, distinct from its effect.'),
    ('Function call', 'Request to apply a named callable to arguments.'),
    ('Argument', 'Value supplied to a function in a call.'),
    ('String literal', 'Source notation for a text value.'),
    ('Standard output', 'Default channel used by print for text.'),
    ('Line ending', 'Control character or sequence marking a new line.'),
    ('Expected output', 'Reasoned prediction, not a recorded observation.'),
    ('Conceptual diagram', 'Teaching representation rather than an application screenshot.'),
]: y=para(c,f'{term}: {meaning}',y)-9
c.showPage()
header(c,'APPENDIX B: SUBMISSION CHECKLIST',len(pages)+3); y=H-95
for text in [
    'Fill in the roll number, section, declaration date and signature on the printed report.',
    'Confirm that the certificate is accepted as evidence of the required four-to-six-week duration; the supplied documents say “one month” but do not specify exact start and end dates.',
    'Confirm that a separate beginner-topic academic study is acceptable. The supplied certificate does not name Hello World as an internship project.',
    'Add only personally verified training activities. Do not label expected output, diagrams or planned checks as execution screenshots or completed tests.',
    'Print all pages on one side only, use a colour print for the certificate page and spiral-bind the report.',
    'Submit by 16 November 2026: Section 1 to Dr. Zeeshan Ali Siddiqui; Section 2 to Dr. Sakshi Srivastava. Confirm your section before submission.',
]: y=para(c,'[  ]  '+text,y)-12
c.showPage(); c.save()

# ---------- Editable DOCX with matching content and manual page breaks ----------
doc=Document(); sec=doc.sections[0]
sec.page_height=Inches(11.69); sec.page_width=Inches(8.27)
sec.top_margin=Inches(.85); sec.bottom_margin=Inches(.7)
sec.left_margin=Inches(.9); sec.right_margin=Inches(.9)
styles=doc.styles
for name in ['Normal','Title','Heading 1']:
    st=styles[name]; st.font.name='Times New Roman'; st.font.size=Pt(12)
    st.paragraph_format.line_spacing=1.0
    st.paragraph_format.space_after=Pt(5)
styles['Heading 1'].font.bold=True
styles['Heading 1'].paragraph_format.space_before=Pt(0)
styles['Title'].font.bold=True

def addp(txt='', center=False, bold=False, italic=False):
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    r=p.add_run(txt); r.bold=bold; r.italic=italic
    return p

def breakpage(): doc.add_page_break()
for s in ['INDUSTRIAL TRAINING REPORT','on','“'+TITLE+'”','by',STUDENT+' [ROLL NUMBER TO FILL]','Submitted in partial fulfillment of the requirements for the award of the degree','of','BACHELOR OF TECHNOLOGY','in','COMPUTER SCIENCE & ENGINEERING','from','EWB EDUTECH PRIVATE LIMITED (EWB Courses)']:
    addp(s,center=True,bold=True)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(logo_img),width=Inches(1.25))
for s in ['Submitted to','DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING','FACULTY OF ENGINEERING & TECHNOLOGY','UNIVERSITY OF LUCKNOW, LUCKNOW','November 2026']:addp(s,center=True,bold=True)
prelim_section=doc.add_section(WD_SECTION_START.NEW_PAGE)
prelim_section.footer.is_linked_to_previous=False
prelim_section.footer.paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER
prelim_section.footer.paragraphs[0].add_run('')
pgtype=OxmlElement('w:pgNumType');pgtype.set(qn('w:fmt'),'lowerRoman');pgtype.set(qn('w:start'),'1')
prelim_section._sectPr.append(pgtype)
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE')
prelim_section.footer.paragraphs[0]._p.append(field)
addp('DECLARATION',center=True,bold=True)
for s in [
'I, Mayank Kumar, declare that this report titled “Print Hello World in Python” is a theory-based academic case study for the B.Tech CSE summer training submission. The syntax examples, manually derived counts, diagrams and predicted behaviours explain a beginner concept; no software product, deployment, executed test or empirical result is claimed.',
'The attached student-supplied certificate documents completion of a one-month Python Programming internship. It does not identify Hello World as an assigned internship project. This topic is a separate academic learning study and should be described as actual internship work only if independently supported.',
'All illustrative statements and character counts are based on public Python concepts or manually checkable reasoning. No restricted organisation information is included. The supplied documents and general reference sources are listed at the end of this report.',
] :addp(s)
for s in ['Signature: ________________________','Name: Mayank Kumar','Roll No.: [TO FILL]','Section: [TO FILL]','Date: [TO FILL]']:addp(s)
breakpage();addp('TRAINING / INTERNSHIP CERTIFICATE',center=True,bold=True)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(cert_img),width=Inches(6.4))
addp('Colour reproduction of the student-provided original certificate. Issued 15 July 2026; it states a one-month Python Programming internship.',italic=True)
breakpage()
for title,content in [
('ABSTRACT',[
'This report presents a theory-only study of the introductory Python 3 example print("Hello, World!"). The small example is used to explain source text, function calls, arguments, string literals, standard output and the normal line ending. It is not a claim that a working model or company deliverable was produced.',
'The report breaks the greeting into manually counted character categories and discusses exact-output comparison, variants, common syntax mistakes, conceptual execution flow and a proposed verification plan. A bar chart represents ten letters, two punctuation marks and one space in the thirteen-character visible greeting. It is a manually derived illustration, not an experiment or performance result.',
'The supplied certificate confirms a one-month Python Programming internship for Mayank Kumar but does not identify this topic as the assigned internship project. Accordingly, this report is a separate academic application of beginner Python concepts.',
'Keywords: Python 3, Hello World, print, string literal, standard output, conceptual study.',
]),('ACKNOWLEDGEMENT',[
'I thank the Department of Computer Science and Engineering, Faculty of Engineering & Technology, University of Lucknow, for the prescribed report format and the opportunity to develop a careful account of a basic Python concept.',
'I acknowledge EWB EDUTECH PRIVATE LIMITED / EWB Courses for the Python Programming internship documented by the attached completion certificate. This particular Hello World study is presented as a separate academic explanation, not as a verified company-assigned project.',
'I thank the faculty reviewing this report for any guidance on its clarity and presentation. The explanatory interpretations and any errors remain my responsibility.',
'Before submitting, the student should amend this acknowledgement to reflect the support actually received.',
])]:
    addp(title,center=True,bold=True)
    for t in content:addp(t)
    breakpage()
addp('TABLE OF CONTENTS',center=True,bold=True)
for title,n in entries:
    p=addp(f'{title}  ..........  {n}')
    p.paragraph_format.space_after=Pt(0)
    p.paragraph_format.line_spacing=1.0
    for run in p.runs:run.font.size=Pt(9)
breakpage();addp('LIST OF TABLES',center=True,bold=True)
for i,p in enumerate(pages,1):
    if p['table']:addp(f"{p['note']}  ..........  {i}")
breakpage();addp('LIST OF FIGURES',center=True,bold=True)
for i,p in enumerate(pages,1):
    captions = ([p['note']] if p['flow'] or p['fig'] else [])
    if p['visual_caption']: captions.append(p['visual_caption'])
    for label in captions:
        item=addp(f'{label}  ..........  {i}')
        item.paragraph_format.space_after=Pt(0)
        for run in item.runs: run.font.size=Pt(9)
main_section=doc.add_section(WD_SECTION_START.NEW_PAGE)
main_section.footer.is_linked_to_previous=False
main_section.footer.paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER
pgtype=OxmlElement('w:pgNumType');pgtype.set(qn('w:fmt'),'decimal');pgtype.set(qn('w:start'),'1')
main_section._sectPr.append(pgtype)
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE')
main_section.footer.paragraphs[0]._p.append(field)
for i,d in enumerate(pages,1):
    addp(d['title'],bold=True)
    for s in d['paras']: addp(s)
    for s in d['bullets']: addp('•  '+s)
    if d['table']:
        rows=d['table']; t=doc.add_table(rows=0,cols=len(rows[0]));t.style='Table Grid';t.alignment=WD_TABLE_ALIGNMENT.CENTER
        for row in rows:
            cells=t.add_row().cells
            for cell,text in zip(cells,row): cell.text=str(text)
    if d['flow']: addp('  →  '.join(d['flow']),center=True,bold=True)
    if d['fig']:
        # Extract only the original illustrative vector chart from the finished PDF.
        pdf_view=pymupdf.open(pdf_path)
        chart_page=pdf_view[8+i-1]
        chart_crop=chart_page.get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(80,260,525,500),alpha=False)
        chart_img=OUT/'illustrative_chart.png';chart_crop.save(chart_img)
        p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(chart_img),width=Inches(5.9))
        pdf_view.close()
    if d['note']: addp(d['note'],italic=True)
    if d['visual']:
        paragraph=doc.add_paragraph()
        paragraph.alignment=WD_ALIGN_PARAGRAPH.CENTER
        paragraph.add_run().add_picture(str(visual_paths[i]),width=Inches(5.8))
        addp(d['visual_caption'],italic=True)
    breakpage()
addp('REFERENCES',bold=True)
for j,r in enumerate(refs,1):addp(f'{j}. {r}')
breakpage();addp('APPENDIX A: GLOSSARY',bold=True)
for term,meaning in [('Source statement', 'Written Python instruction, distinct from its effect.'),('Function call', 'Request to apply a named callable to arguments.'),('Argument', 'Value supplied to a function in a call.'),('String literal', 'Source notation for a text value.'),('Standard output', 'Default channel used by print for text.'),('Line ending', 'Control character or sequence marking a new line.'),('Expected output', 'Reasoned prediction, not a recorded observation.'),('Conceptual diagram', 'Teaching representation rather than an application screenshot.')]:addp(f'{term}: {meaning}')
breakpage();addp('APPENDIX B: SUBMISSION CHECKLIST',bold=True)
for s in ['Fill roll number, section, date and signature.','Check acceptance of one-month certificate for four-to-six-week requirement; exact dates are not shown.','Confirm that a separate academic case study is acceptable.','Do not present predicted output, proposed checks or diagrams as actual execution evidence.','Print single-sided, certificate in colour, and spiral-bind.','Submit by 16 November 2026 to the faculty member designated for your section.']:addp('[  ]  '+s)
# The editable file uses Roman numbering for preliminaries and restarts at 1
# for the main report; verify layout in the chosen word processor before printing.
doc.save(OUT/'Hello_World_Python_Internship_Report.docx')
for temporary_image in (cert_img, logo_img, OUT/'illustrative_chart.png'):
    temporary_image.unlink(missing_ok=True)
shutil.rmtree(visual_directory)
print(f'Created {pdf_path} and DOCX; main pages={len(pages)} total PDF pages={8+len(pages)+3}')
