"""Report content: a single, renderer-neutral block model.

Block types
-----------
('chapter', number, title)      chapter banner / heading 1 level
('h1', text)                    section heading (numbered, e.g. "1.1  Introduction")
('h2', text)                    sub-heading
('p', text)                     justified body paragraph
('quote', text)                 indented quotation
('bullets', [..])               bulleted list
('numbered', [..])              numbered list
('fig', filename, caption)      figure + numbered caption
('table', spec)                 table + caption
('callout', text)               tinted note box
('pagebreak',)                  hard page break
('keep', [blocks])              keep a small group together
('refs', [ (num, text, url) ])  reference list

Inline markup supported by both renderers: <b>, <i>, and
<a href="#KEY"> / <a href="https://...">.
"""
import hashlib

from figures_list import FIG, TAB          # numbering tables


def K(s):
    """Deterministic cross-reference key (identical in PDF and DOCX)."""
    norm = ' '.join(s.split())
    return 'S' + hashlib.md5(norm.encode('utf-8')).hexdigest()[:12]


def X(target, label=None):
    """Clickable internal cross-reference.

    'Chapter N' labels resolve against the chapter titles; section labels that
    are themselves the target also resolve. Deterministic, so PDF and DOCX use
    the same destination names.
    """
    if label and label.startswith('Chapter'):
        import re
        title = re.sub(r'^\d+\s+', '', target).strip()
        return '<a href="#%s">%s</a>' % (K(title), label)
    return '<a href="#%s">%s</a>' % (K(target), label or target)


def E(url, label=None):
    return '<a href="%s">%s</a>' % (url, label or url)


def C(*nums):
    """Inline citation markers linked to the reference list."""
    parts = []
    for n in nums:
        parts.append('<a href="#ref%d">[%d]</a>' % (n, n))
    return ', '.join(parts)


def FIGCAP(fname):
    return FIG[fname]


def TABSPEC(fname, key):
    return TAB[key]


def TX(key, label=None):
    """Clickable cross-reference to a numbered table."""
    text = TAB[key]
    num = text.split(':')[0]
    return '<a href="#%s">%s</a>' % (K(text), label or num)


def FX(fname, label=None):
    """Clickable cross-reference to a numbered figure."""
    text = FIG[fname]
    num = text.split(':')[0]
    return '<a href="#%s">%s</a>' % (K(text), label or num)
