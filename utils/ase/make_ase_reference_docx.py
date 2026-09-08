#!/usr/bin/env python3
"""Build the pandoc reference template for the ASE journal manuscript.

Sibling of make_reference_docx.py (pgs_reference.docx) and make_ieee_reference_docx.py
(ieee_reference.docx). Each paper family owns its own template; none shares state.

Pandoc's stock reference.docx is 12 pt with 10 pt of space after every
paragraph, which is why the first build ran to 67 pages. This produces a
tighter template and adds page numbering, so the .docx stays fully derived —
no hand formatting, and `build_manuscript.py` can be re-run after any edit.

    python3 make_ase_reference_docx.py   ->  ase_reference.docx
"""
import re, shutil, subprocess, zipfile

import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = "/tmp/ase_ref_default.docx"
OUT = os.path.join(SCRIPT_DIR, "ase_reference.docx")

BODY_PT   = 24   # half-points: 12 pt
TABLE_PT  = 18   # 9 pt
CAPTION_PT= 18   # 9 pt
AFTER_TW  = 120  # twips: 6 pt after a paragraph
MARGIN_TW = 1152 # twips: 0.8 inch on three sides
MARGIN_R_TW = 720  # twips: 0.5 inch on the right, to cut page count

FOOTER = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="0"/></w:pPr>
    <w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>
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

    # ---- styles: body size, paragraph spacing, headings, captions, tables ----
    st = items["word/styles.xml"].decode("utf-8")
    st = st.replace('<w:sz w:val="24" />\n        <w:szCs w:val="24" />',
                    '<w:sz w:val="%d" /><w:szCs w:val="%d" />' % (BODY_PT, BODY_PT))
    st = st.replace('<w:spacing w:after="200" />',
                    '<w:spacing w:after="%d" w:line="240" w:lineRule="auto" />' % AFTER_TW)
    # A heading or a figure caption stranded at the foot of a page is the most
    # common defect in a generated manuscript; keepNext binds each to what follows.
    for sid in ("Heading1", "Heading2", "Heading3", "Caption", "ImageCaption", "TableCaption"):
        st = keep_next(st, sid)

    # Heading levels as the author reads them: pandoc maps `#` to Heading1 (the document
    # title), `##` to Heading2 (numbered sections) and `###` to Heading3 (subsections).
    # Sized for a review copy — larger than a typeset page, deliberately.
    for sid, pt in [("Title", 40), ("Heading1", 40),   # title            20 pt
                    ("Heading2", 36),                  # level-1 section  18 pt
                    ("Heading3", 32),                  # level-2          16 pt
                    ("Heading4", 28),                  # level-3          14 pt
                    ("Author", BODY_PT), ("Abstract", BODY_PT),
                    ("Caption", CAPTION_PT), ("ImageCaption", CAPTION_PT),
                    ("TableCaption", CAPTION_PT), ("Table", TABLE_PT),
                    ("BodyText", BODY_PT), ("Compact", BODY_PT),
                    ("FirstParagraph", BODY_PT),
                    ("Bibliography", BODY_PT), ("FootnoteText", 18)]:
        st = style_size(st, sid, pt)
    items["word/styles.xml"] = st.encode("utf-8")

    # ---- page margins + footer reference ----
    doc = items["word/document.xml"].decode("utf-8")
    sect = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter1"/>'
            '<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" '
            'w:header="720" w:footer="720" w:gutter="0"/>'
            '<w:footnotePr><w:numRestart w:val="eachSect"/></w:footnotePr></w:sectPr>'
            % (MARGIN_TW, MARGIN_R_TW, MARGIN_TW, MARGIN_TW))
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
    print("%s — body %.0f pt, tables %.0f pt, %.0f pt after paragraphs, "
          "%.2f in margins (%.2f in right), page numbers on"
          % (OUT, BODY_PT/2, TABLE_PT/2, AFTER_TW/20, MARGIN_TW/1440, MARGIN_R_TW/1440))

if __name__ == "__main__":
    main()
