# Summer Internship Report — build files

Final deliverables (repository root):

| File | Purpose |
|---|---|
| `Summer_Internship_Report_Mayank_Kumar.pdf` | Print-ready PDF (47 pages, single-sided) |
| `Summer_Internship_Report_Mayank_Kumar.docx` | Fully editable Word version |

## Report

**Title:** Python for Data Visualisation: A Case Study of Air Quality Analysis of Lucknow City
**Student:** Mayank Kumar — B.Tech CSE 3rd Year, University of Lucknow
**Internship:** Python Programming Intern, EWB Edutech Pvt Ltd — 14 Jun to 15 Jul 2026 (AICTE)
**Guide:** Dr. Zeeshan Ali Siddiqui (Section 1)

Structure follows the prescribed order: cover page (department format) → declaration →
coloured certificate copy → abstract → acknowledgement → table of contents →
list of tables → list of figures → chapters 1–8 → references → glossary → appendix.

Formatting: Times New Roman (Tinos metric-compatible), 12 pt, single spacing,
bold main headings, italic sub-headings, Roman numerals on preliminary pages,
Arabic numerals on the main report.

## Regenerating

```bash
pip install python-docx matplotlib reportlab pymupdf pillow
cd report
python3 make_figures.py     # writes figures/*.png  (17 charts)
python3 build_pdf.py        # writes ../Summer_Internship_Report_*.pdf + pages.json
python3 build_docx.py       # writes ../Summer_Internship_Report_*.docx
```

`build_pdf.py` runs a two-pass build: the first pass measures where each heading,
table and figure lands, the second pass writes those page numbers into the table of
contents and the lists of tables/figures. `pages.json` is the shared page map that the
DOCX build reuses so both files agree.

## Source files

| File | Contents |
|---|---|
| `content_front.py` | Cover data, abstract, acknowledgement, declaration |
| `content_body.py` | All chapters, captions, tables and code listings |
| `daily_data.py` | Daily air-quality dataset + CPCB sub-index/AQI computation |
| `make_figures.py` | All 17 figures (Matplotlib) |
| `build_pdf.py` | ReportLab renderer |
| `build_docx.py` | python-docx renderer |
| `assets/certificate.png` | Raster of the EWB completion certificate |
| `assets/fonts/` | Tinos (metric-compatible with Times New Roman, OFL licence) |
