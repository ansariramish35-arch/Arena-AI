# Web Technology Laboratory File (B.Tech CSE)

Ready-to-submit lab file containing the front page, index, and all 11
practicals from the Web Technology syllabus, each with complete working
source code and a labelled representative output.

## Deliverables

- `Web_Technology_Lab_File.docx` — editable Word file (A4, Times New Roman
  12 pt, headings 14–16 pt bold, code in Consolas 10 pt, page numbers in the
  footer, every practical starts on a new page, index page numbers match the
  final pagination, Date column left blank for handwritten entry).
- `Web_Technology_Lab_File.pdf` — matching PDF rendering of the same content.

## Programs (complete, executable source)

`programs/` contains one folder per practical with every file needed to run
it in a browser:

| # | Folder | Files |
|---|--------|-------|
| 1 | `p01-resume-table` | resume.html (+ sample photo.jpg) |
| 2 | `p02-homepage-frames` | index.html (HTML 4.01 frameset), header/menu/welcome/about/education/contact/footer.html |
| 3 | `p03-form` | form.html |
| 4 | `p04-image-map` | image-map.html + campus-map.jpg |
| 5 | `p05-hotspots` | hotspots.html + campus-map.jpg |
| 6 | `p06-image-coordinates` | coordinates.html + lab-map.jpg |
| 7 | `p07-css-types` | css-types.html + styles.css (inline, internal, external) |
| 8 | `p08-cv-links` | links.html + cv.html |
| 9 | `p09-student-record-validation` | student-record.html |
| 10 | `p10-xml-dtd` | students.xml (internal DTD), students-external.dtd, students-external.xml |
| 11 | `p11-xml-xsl` | students.xml + students.xsl (opens styled in IE/any modern browser) |

## Rebuilding the documents

```bash
python3 -m venv .venv && .venv/bin/pip install python-docx reportlab
.venv/bin/python build/build_lab_file.py
```

The builder reads the program sources from `programs/`, computes the index
page numbers with a two-pass PDF build, and writes both the `.docx` and the
`.pdf`. `assets/make_images.py` regenerates the sample JPGs used by
Practicals 1, 4, 5 and 6.
