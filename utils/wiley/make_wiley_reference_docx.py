#!/usr/bin/env python3
"""Build the pandoc reference template for a Wiley journal review manuscript.

Sibling of make_jss_reference_docx.py and make_ase_reference_docx.py. Each paper
family owns its own template; none shares state.

Wiley asks for 12-point, single-column, single-spaced type in Times, Helvetica or
Courier, with tables and figures incorporated into the body of the main text for an
initial submission. Times New Roman is the choice here, set on the theme and on the
default run so nothing inherits a sans face from pandoc's stock template.

`wiley_docx_filter.lua` starts every `##` section on a new page, the abstract excepted
so it stays with the title block. The figure and both tables sit inside the sections
that reference them, so the break separates neither from its text; it does add about
one partial page per section.

    python3 make_wiley_reference_docx.py   ->  wiley_reference.docx
"""
import os, re, subprocess, zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = "/tmp/wiley_ref_default.docx"
OUT = os.path.join(SCRIPT_DIR, "wiley_reference.docx")

SERIF      = "Times New Roman"
BODY_PT    = 24   # half-points: 12 pt
TABLE_PT   = 20   # 10 pt — a 26-row table at 12 pt overruns the page width
CAPTION_PT = 20   # 10 pt
AFTER_TW   = 120  # twips: 6 pt after a paragraph
LINE_TW    = 240  # twips: single spacing (480 = double)
MARGIN_TW  = 1440 # twips: 1 inch, all four sides

FOOTER = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="0"/></w:pPr>
    <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>
  </w:p>
</w:ftr>"""


def keep_next(xml, style_id):
    """Bind a style's paragraph to the one after it, so it cannot be orphaned."""
    pat = re.compile(r'(<w:style [^>]*w:styleId="%s"[^>]*>)(.*?)(</w:style>)' % style_id, re.S)
    def sub(m):
        head, body, tail = m.groups()
        if "<w:keepNext" in body:
            return m.group(0)
        if "<w:pPr>" in body:
            body = body.replace("<w:pPr>", "<w:pPr><w:keepNext/>", 1)
        else:
            body = "<w:pPr><w:keepNext/></w:pPr>" + body
        return head + body + tail
    new, n = pat.subn(sub, xml)
    return new if n else xml


def style_size(xml, style_id, half_points, extra=""):
    """Force a run size (and optional extra rPr) onto one named style."""
    pat = re.compile(r'(<w:style [^>]*w:styleId="%s"[^>]*>)(.*?)(</w:style>)' % style_id, re.S)
    def sub(m):
        head, body, tail = m.groups()
        body = re.sub(r'<w:sz w:val="\d+"\s*/>', '', body)
        body = re.sub(r'<w:szCs w:val="\d+"\s*/>', '', body)
        size = '<w:sz w:val="%d"/><w:szCs w:val="%d"/>%s' % (half_points, half_points, extra)
        if "<w:rPr>" in body:
            body = body.replace("<w:rPr>", "<w:rPr>" + size, 1)
        else:
            body += "<w:rPr>" + size + "</w:rPr>"
        return head + body + tail
    new, n = pat.subn(sub, xml)
    return new if n else xml


def main():
    subprocess.run(["pandoc", "-o", SRC, "--print-default-data-file", "reference.docx"], check=True)
    zin = zipfile.ZipFile(SRC)
    items = {n: zin.read(n) for n in zin.namelist()}
    zin.close()

    # ---- theme: every themed font becomes the serif face ----
    th = items["word/theme/theme1.xml"].decode("utf-8")
    th = re.sub(r'<a:latin typeface="[^"]*"', '<a:latin typeface="%s"' % SERIF, th)
    items["word/theme/theme1.xml"] = th.encode("utf-8")

    st = items["word/styles.xml"].decode("utf-8")

    # ---- default run: serif face, explicit rather than themed ----
    explicit = ('<w:rFonts w:ascii="%s" w:hAnsi="%s" w:eastAsia="%s" w:cs="%s"/>'
                % (SERIF, SERIF, SERIF, SERIF))
    st = st.replace('<w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia" '
                    'w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi" />', explicit, 1)
    # Any style carrying its own themed face (headings use majorHAnsi) is overridden too.
    st = re.sub(r'<w:rFonts[^>]*Theme="[^"]*"[^>]*/>', explicit, st)

    # ---- body size, paragraph spacing ----
    st = st.replace('<w:sz w:val="24" />\n        <w:szCs w:val="24" />',
                    '<w:sz w:val="%d" /><w:szCs w:val="%d" />' % (BODY_PT, BODY_PT))
    st = st.replace('<w:spacing w:after="200" />',
                    '<w:spacing w:after="%d" w:line="%d" w:lineRule="auto" />' % (AFTER_TW, LINE_TW))

    # A heading or caption stranded at the foot of a page is the most common defect
    # in a generated manuscript; keepNext binds each to what follows.
    for sid in ("Heading1", "Heading2", "Heading3", "Heading4",
                "Caption", "ImageCaption", "TableCaption"):
        st = keep_next(st, sid)

    # Heading levels as the author reads them: pandoc maps `#` to Heading1 (the
    # document title), `##` to Heading2 (numbered sections), `###` to Heading3.
    # Restrained sizes — Wiley typesets from the accepted source, so this is a
    # reading copy rather than an imitation of the published page.
    for sid, pt in [("Title", 32), ("Heading1", 32),   # title            16 pt
                    ("Heading2", 28),                  # level-1 section  14 pt
                    ("Heading3", 26),                  # level-2          13 pt
                    ("Heading4", BODY_PT),             # level-3          12 pt
                    ("Author", BODY_PT), ("Abstract", BODY_PT),
                    ("Caption", CAPTION_PT), ("ImageCaption", CAPTION_PT),
                    ("TableCaption", CAPTION_PT), ("Table", TABLE_PT),
                    ("BodyText", BODY_PT), ("Compact", BODY_PT),
                    ("FirstParagraph", BODY_PT),
                    ("Bibliography", BODY_PT), ("FootnoteText", 20)]:
        st = style_size(st, sid, pt)
    items["word/styles.xml"] = st.encode("utf-8")

    # ---- page margins + footer reference: single column throughout ----
    doc = items["word/document.xml"].decode("utf-8")
    sect = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter1"/>'
            '<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" '
            'w:header="720" w:footer="720" w:gutter="0"/>'
            '<w:cols w:space="720"/>'
            '<w:footnotePr><w:numRestart w:val="eachSect"/></w:footnotePr></w:sectPr>'
            % (MARGIN_TW, MARGIN_TW, MARGIN_TW, MARGIN_TW))
    doc = re.sub(r"<w:sectPr>.*?</w:sectPr>", sect, doc, flags=re.S)
    items["word/document.xml"] = doc.encode("utf-8")

    # ---- footer part, relationship, content type ----
    items["word/footer1.xml"] = FOOTER.encode("utf-8")
    rels = items["word/_rels/document.xml.rels"].decode("utf-8")
    rels = rels.replace("</Relationships>",
        '<Relationship Id="rIdFooter1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" '
        'Target="footer1.xml"/></Relationships>')
    items["word/_rels/document.xml.rels"] = rels.encode("utf-8")
    ct = items["[Content_Types].xml"].decode("utf-8")
    ct = ct.replace("</Types>",
        '<Override PartName="/word/footer1.xml" ContentType="application/vnd.'
        'openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>')
    items["[Content_Types].xml"] = ct.encode("utf-8")

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in items.items():
            z.writestr(n, data)
    print("%s — %s, body %.0f pt, tables %.0f pt, %s spaced, single column, "
          "%.0f in margins, page numbers on"
          % (OUT, SERIF, BODY_PT / 2, TABLE_PT / 2,
             "single" if LINE_TW == 240 else "double", MARGIN_TW / 1440))


if __name__ == "__main__":
    main()
