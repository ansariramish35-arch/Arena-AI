# Web Technology Laboratory File — B.Tech (CSE)

A complete, submission-ready laboratory file for the **Web Technology** course,
containing the front page, the index and all **11 practicals** of the syllabus with
complete source code and output screenshots.

## Deliverables

| File | Description |
|---|---|
| `Web_Technology_Laboratory_File.docx` | Editable Microsoft Word file (A4, Times New Roman 12 pt, code in Courier New 10 pt, page numbers at the bottom) |
| `Web_Technology_Laboratory_File.pdf` | Matching PDF of the same document (39 pages) |

Both files contain, in order:

1. **Front page** – university / college / student / faculty fields left blank for
   handwriting (nothing is invented).
2. **Index** – all 11 programs in syllabus order; `Date` column blank; `Page No.`
   column carries the real page numbers of the document.
3. **Practicals 1–11** – each starts on a new page and follows the structure
   *Practical No. → Program → Source Code → Output/Result* (screenshot + short note).

## Runnable programs

`source/practical_01 … practical_11` hold the exact programs printed in the file.
Open the listed `.html` / `.xml` files in any browser (keep the accompanying
`.png`, `.css`, `.xsl`, `.dtd` files in the same folder).

The programs are written in **compact form** so that the file stays short: no
blank lines, no indentation, one HTML row per line and every line filled up to
the 78 columns the document prints. Only the layout of the source was changed –
the tags, attributes, text, CSS rules and JavaScript logic are exactly the same,
so the output is identical (verified against the originals before compressing).

The XML work was checked with a validating parser (libxml2):

* `students.xml` (internal DTD) — **valid**
* `students_external.xml` + `rules.dtd` — **valid**
* `invalid_example.xml` — **invalid on purpose** (missing required `id`, wrong element order)
* `books.xml` + `books.xsl` — XSLT 1.0 transformation verified

## Screenshots

`images/out*.png` are the "Output / Result" screenshots printed in the file.
`images/shapes.png`, `images/hardware.png`, `images/grid.png` are the picture files
used by practicals 4, 5 and 6 (1× copies live next to the source code).

## Rebuilding the documents

```bash
python build/make_assets.py        # redraw the three picture files
python build/make_screenshots.py   # redraw the 13 output screenshots
python build/make_document.py      # PDF  (two passes -> real index page numbers)
python build/make_docx.py          # DOCX (same content, same page numbers)
```

Requires: `python-docx`, `reportlab`, `Pillow`, `lxml` (validation only).
The DOCX uses exact line spacing equal to the PDF leading, so Word paginates the
file exactly like the PDF and the index page numbers stay correct.
