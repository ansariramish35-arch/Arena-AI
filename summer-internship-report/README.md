# B.Tech CSE Summer Internship Report — SwachhAI

Deliverables (report root):

| File | What it is |
|---|---|
| `B.Tech_CSE_Summer_Internship_Report_SwachhAI.docx` | Editable Word edition (live TOC field, bookmarks, internal + external links, embedded certificates) |
| `B.Tech_CSE_Summer_Internship_Report_SwachhAI.pdf` | Print-ready PDF, A4, 60 pages, single-sided for spiral binding, clickable TOC / bookmarks / cross-references |
| `SwachhAI_Project_Presentation.pptx` | Editable, 22-slide project deck following the IBM University Engagement presentation structure; includes architecture, workflow, labelled simulation, evidence limits and certificates |
| `images/` | All 21 conceptual diagrams and 2 clearly-labelled illustrative mock-ups (300 dpi PNG) |
| `certificates/` | Colour copies of the completion certificate and IBM SkillsBuild certificates used in the report and deck |

## Rebuilding

```bash
cd build
python3 figures.py        # redraw every diagram into ../images
python3 render_pdf.py     # build the PDF
python3 render_docx.py    # build the DOCX
python3 build_presentation.py  # build the editable PPTX (requires python-pptx)
```

Requirements: `reportlab`, `pymupdf`, `python-docx`, `pillow`; add `python-pptx` to build the presentation.

## How it is put together

* `content_front.py`, `content_main.py`, `content_main2.py`, `content_main3.py` — the report text,
  written once as a small block model (`model.py`): chapters, headings, paragraphs, tables,
  figures, callouts and references.
* `figures_list.py` — single source of figure and table numbering (Figure 1…21, Table 1…21),
  in document order, shared by both editions.
* `reportkit.py` — PDF layout: A4 frames, Roman/Arabic page numbering with separate sections,
  running headers and footers, clickable TOC / list of tables / list of figures, PDF outline.
* `diagramkit.py`, `figures.py` — every diagram is drawn as vector art in Times and rasterised
  at 300 dpi, so the report contains no stock imagery.
* `render_pdf.py`, `render_docx.py` — the two renderers. Cross-reference keys are hashed from the
  heading or caption text, so the same link resolves in both files.

## Content rules followed

* All student, internship and date particulars come from the uploaded documents. The completion
  certificate (22 September 2026, July–September 2026) governs the certified period; the offer
  letter's six-week window is described only as the proposed window.
* The university roll number and faculty supervisor are left as explicit placeholders.
* No working software: the project is documented through architecture, workflow, module tables,
  worked examples and labelled mock-ups. No test results, accuracy figures or user feedback are
  claimed anywhere.
* The presentation labels the simulation, impact figures and stack as conceptual; it does not
  invent a token count or public GitHub/app URL. An initials monogram is used because no portrait
  photo was present in the supplied résumés.
* Confidential material from the offer letter (course content, session content, contact details)
  is not reproduced.
