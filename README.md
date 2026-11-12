# Library Book Management: A Python-Based Design

A **theory-only**, 50-page B.Tech CSE summer training report. The fictional library records, worked examples, flowcharts and bar chart illustrate a proposed design; they are **not** screenshots, test results or a claim that software was implemented.

## Deliverables

- [`deliverables/Library_Book_Management_Internship_Report.pdf`](deliverables/Library_Book_Management_Internship_Report.pdf) — print-reference PDF, with Roman-numbered preliminary pages, Arabic-numbered chapters, the supplied colour certificate, and an A4 single-sided layout.
- [`deliverables/Library_Book_Management_Internship_Report.docx`](deliverables/Library_Book_Management_Internship_Report.docx) — editable Times New Roman document. Its contents and section-based numbering mirror the PDF, but **verify pagination after opening it in Word/LibreOffice**; layout can change between word processors. The PDF uses a Times-compatible PDF font.

## Before submitting

1. Fill in the **roll number, section, declaration date and signature**. Revise the acknowledgement if needed. Do not print the placeholder-filled version as a final submission.
2. Confirm with the department that the supplied certificate, which states **“1 Month”** but does not specify exact start/end dates, satisfies the **4–6 week** evidence requirement.
3. Confirm that a separate academic case study is acceptable: the supplied certificate confirms Python Programming training but **does not identify this library design as the assigned internship project**.
4. If you edit the DOCX, compare its table of contents and page numbers to the final printout; the contents list was laid out manually to match the PDF.
5. Print on one side of each page, print the certificate in colour and spiral-bind. Submission deadline: 16 November 2026.

`generate_report.py` contains the report content and layout code. It uses the student-provided PDFs in `/tmp/arena-coding-uploads/` to reproduce the certificate and University emblem; those private original uploads are intentionally not copied into the Git repository. It requires `pymupdf`, `reportlab` and `python-docx`.
