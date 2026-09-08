#!/usr/bin/env python3
"""
make_ieee_reference_docx.py — build ieee_reference.docx for pandoc.

Pandoc takes page setup and named styles from a reference document. This script
starts from pandoc's default reference.docx and rewrites it to IEEE conference
geometry and typography:

  page      US Letter, 8.5 x 11 in
  margins   0.75 top, 1.0 bottom, 0.625 left/right (in)
  columns   two, 3.5 in each, 0.25 in gutter  (0.625 + 3.5 + 0.25 + 3.5 + 0.625 = 8.5)
  body      Times New Roman, left aligned (ragged right), no first-line indent,
            12 pt between paragraphs
  tables    left aligned and single spaced, whatever the body spacing is
  title     24 pt, left aligned
  abstract  12 pt, same as body
  headings  18 / 16 / 14 pt under a 20 pt title, left aligned
  rows      6 pt of cell padding top and bottom, so rows read as separate

The title block must span the full width, which Word does with a section break.
Pandoc emits one section, so ieee_docx_filter.lua injects a continuous
single-column break after Index Terms; everything above it stays full width.
"""

import io, os, re, subprocess, sys, zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Single column is the default: it is what a magazine submission wants, and it
# is what a reviewer can mark up. TWOCOL=1 gives the two-column conference form.
TWOCOL = bool(os.environ.get("TWOCOL"))
LETTER = bool(os.environ.get("LETTER"))   # cover letter: single spaced, one page
OUTPUT = os.path.join(SCRIPT_DIR,
                      "ieee_letter_reference.docx" if LETTER else
                      "ieee_twocol_reference.docx" if TWOCOL else
                      "ieee_reference.docx")

TWIP = 1440  # twentieths of a point per inch
def inch(v): return str(int(round(v * TWIP)))

PG_SZ  = f'<w:pgSz w:w="{inch(8.5)}" w:h="{inch(11)}"/>'
PG_MAR = (f'<w:pgMar w:top="{inch(0.75)}" w:right="{inch(0.625)}" '
          f'w:bottom="{inch(1.0)}" w:left="{inch(0.625)}" '
          f'w:header="{inch(0.5)}" w:footer="{inch(0.5)}" w:gutter="0"/>')
if TWOCOL:
    COLS   = (f'<w:cols w:num="2" w:space="{inch(0.25)}" w:equalWidth="0">'
              f'<w:col w:w="{inch(3.5)}" w:space="{inch(0.25)}"/>'
              f'<w:col w:w="{inch(3.5)}"/></w:cols>')
    BODY_SZ, BODY_SPACING = "20", '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/>'
else:
    # Manuscript for submission: one column, 12 pt, 1 in margins, single spaced.
    # Line spacing and page numbers are left to the author in Word.
    COLS   = '<w:cols w:num="1"/>'
    PG_MAR = (f'<w:pgMar w:top="{inch(1.0)}" w:right="{inch(1.0)}" '
              f'w:bottom="{inch(1.0)}" w:left="{inch(1.0)}" '
              f'w:header="{inch(0.5)}" w:footer="{inch(0.5)}" w:gutter="0"/>')
    if LETTER:
        # A letter is read in one pass: single spaced, with a blank-line gap
        # between paragraphs. 1.5 spacing would push one page into two.
        BODY_SZ = "24"
        BODY_SPACING = '<w:spacing w:after="180" w:line="240" w:lineRule="auto"/>'
    else:
        BODY_SZ = "24"
        BODY_SPACING = '<w:spacing w:after="240" w:line="360" w:lineRule="auto"/>' 

TIMES = ('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
         'w:eastAsia="Times New Roman" w:cs="Times New Roman"/>')

# styleId -> (paragraph properties, run properties). Half-points for w:sz.
STYLES = {
    "Title":         ('<w:jc w:val="left"/><w:spacing w:before="0" w:after="240"/>',
                      f'{TIMES}<w:sz w:val="40"/><w:szCs w:val="40"/>'),
    "Author":        ('<w:jc w:val="left"/><w:spacing w:before="0" w:after="120"/>',
                      f'{TIMES}<w:sz w:val="22"/><w:szCs w:val="22"/>'),
    "Date":          ('<w:jc w:val="left"/>',
                      f'{TIMES}<w:sz w:val="22"/><w:szCs w:val="22"/>'),
    "AbstractTitle": ('<w:jc w:val="left"/><w:spacing w:before="0" w:after="0"/>',
                      f'{TIMES}<w:b/><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/>'),
    "Abstract":      ('<w:jc w:val="left"/><w:spacing w:before="0" w:after="240"/>'
                      '<w:ind w:firstLine="0"/>',
                      f'{TIMES}<w:sz w:val="24"/><w:szCs w:val="24"/>'),
    "Heading1":      ('<w:jc w:val="left"/><w:spacing w:before="240" w:after="120"/>'
                      '<w:ind w:firstLine="0"/>',
                      f'{TIMES}<w:smallCaps/><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/>'),
    "Heading2":      ('<w:jc w:val="left"/><w:spacing w:before="180" w:after="60"/>'
                      '<w:ind w:firstLine="0"/>',
                      f'{TIMES}<w:i/><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/>'),
    "Heading3":      ('<w:jc w:val="left"/><w:spacing w:before="120" w:after="60"/>'
                      '<w:ind w:firstLine="0"/>',
                      f'{TIMES}<w:i/><w:sz w:val="28"/><w:szCs w:val="28"/>'),
    "BodyText":      ('<w:jc w:val="left"/><w:ind w:firstLine="0"/>' + BODY_SPACING,
                      f'{TIMES}<w:sz w:val="{BODY_SZ}"/><w:szCs w:val="{BODY_SZ}"/>'),
    "FirstParagraph":('<w:jc w:val="left"/><w:ind w:firstLine="0"/>' + BODY_SPACING,
                      f'{TIMES}<w:sz w:val="{BODY_SZ}"/><w:szCs w:val="{BODY_SZ}"/>'),
    "Compact":       ('<w:jc w:val="left"/><w:ind w:firstLine="0"/>'
                      '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/>',
                      f'{TIMES}<w:sz w:val="20"/><w:szCs w:val="20"/>'),
    "ImageCaption":  ('<w:jc w:val="left"/><w:spacing w:before="120" w:after="120"/>'
                      '<w:ind w:firstLine="0"/>',
                      f'{TIMES}<w:sz w:val="20"/><w:szCs w:val="20"/>'),
    "TableCaption":  ('<w:jc w:val="left"/><w:spacing w:before="120" w:after="60"/>'
                      '<w:ind w:firstLine="0"/>',
                      f'{TIMES}<w:smallCaps/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/>'),
}

FOOTER_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p><w:pPr><w:jc w:val="center"/></w:pPr>
    <w:r><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:instrText xml:space="preserve"> PAGE \\* MERGEFORMAT </w:instrText></w:r>
    <w:r><w:fldChar w:fldCharType="separate"/></w:r>
    <w:r><w:t>1</w:t></w:r>
    <w:r><w:fldChar w:fldCharType="end"/></w:r>
  </w:p>
</w:ftr>
"""
REL_FOOTER = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer"
CT_FOOTER = ("application/vnd.openxmlformats-officedocument"
             ".wordprocessingml.footer+xml")


def patch_styles(xml):
    # document-wide defaults: Times 10 pt, no paragraph spacing
    xml = re.sub(
        r"<w:rPrDefault>.*?</w:rPrDefault>",
        f"<w:rPrDefault><w:rPr>{TIMES}<w:sz w:val=\"{BODY_SZ}\"/><w:szCs w:val=\"{BODY_SZ}\"/>"
        f"<w:lang w:val=\"en-US\"/></w:rPr></w:rPrDefault>",
        xml, flags=re.S)
    xml = re.sub(
        r"<w:pPrDefault>.*?</w:pPrDefault>",
        f'<w:pPrDefault><w:pPr>{BODY_SPACING}</w:pPr></w:pPrDefault>',
        xml, flags=re.S)

    # Row separation comes from cell padding, not from paragraph spacing, so
    # line spacing inside a multi-line cell is unaffected.
    xml = re.sub(
        r'(<w:style [^>]*w:styleId="Table".*?<w:tblCellMar>)\s*<w:top[^/]*/>(.*?)<w:bottom[^/]*/>',
        r'\1<w:top w:type="dxa" w:w="120"/>\2<w:bottom w:type="dxa" w:w="120"/>',
        xml, flags=re.S)

    for style_id, (ppr, rpr) in STYLES.items():
        pattern = re.compile(
            r'(<w:style [^>]*w:styleId="%s".*?</w:style>)' % re.escape(style_id), re.S)
        m = pattern.search(xml)
        if not m:
            continue
        block = m.group(1)
        # replace or insert the property blocks, preserving name/basedOn
        if "<w:pPr>" in block:
            block = re.sub(r"<w:pPr>.*?</w:pPr>", f"<w:pPr>{ppr}</w:pPr>", block, flags=re.S)
        else:
            block = block.replace("</w:style>", f"<w:pPr>{ppr}</w:pPr></w:style>")
        if "<w:rPr>" in block:
            block = re.sub(r"<w:rPr>.*?</w:rPr>", f"<w:rPr>{rpr}</w:rPr>", block, flags=re.S)
        else:
            block = block.replace("</w:style>", f"<w:rPr>{rpr}</w:rPr></w:style>")
        xml = xml[:m.start(1)] + block + xml[m.end(1):]
    return xml


def patch_document(xml, footer_id):
    """Give the body sectPr Letter size, IEEE margins, two columns and the footer."""
    body_sect = re.search(r"<w:sectPr[^>]*>.*?</w:sectPr>", xml, re.S)
    footer_ref = (f'<w:footerReference w:type="default" r:id="{footer_id}"/>'
                  if TWOCOL else "")
    new_sect = ("<w:sectPr>"
                '<w:footnotePr><w:numRestart w:val="eachSect"/></w:footnotePr>'
                + footer_ref
                + f"{PG_SZ}{PG_MAR}{COLS}"
                '<w:docGrid w:linePitch="360"/>'
                "</w:sectPr>")
    if body_sect:
        return xml[:body_sect.start()] + new_sect + xml[body_sect.end():]
    return xml.replace("</w:body>", new_sect + "</w:body>")


def build():
    try:
        base = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                              capture_output=True, check=True).stdout
    except FileNotFoundError:
        sys.exit("ERROR: pandoc not found on PATH.")

    footer_id = "rIdIeeeFooter1"
    zin = zipfile.ZipFile(io.BytesIO(base), "r")
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in zin.namelist():
            data = zin.read(name)
            if name == "word/styles.xml":
                data = patch_styles(data.decode()).encode()
            elif name == "word/document.xml":
                data = patch_document(data.decode(), footer_id).encode()
            elif name == "word/_rels/document.xml.rels":
                t = data.decode().replace(
                    "</Relationships>",
                    f'<Relationship Id="{footer_id}" Type="{REL_FOOTER}" '
                    f'Target="footer1.xml"/></Relationships>')
                data = t.encode()
            elif name == "[Content_Types].xml":
                t = data.decode().replace(
                    "</Types>",
                    f'<Override PartName="/word/footer1.xml" '
                    f'ContentType="{CT_FOOTER}"/></Types>')
                data = t.encode()
            zout.writestr(name, data)
        zout.writestr("word/footer1.xml", FOOTER_XML.encode())

    with open(OUTPUT, "wb") as f:
        f.write(out.getvalue())
    print(f"Created: {OUTPUT} ({os.path.getsize(OUTPUT):,} bytes)")
    if TWOCOL:
        print("  Letter, 0.75/1.0/0.625 in margins, two 3.5 in columns, Times 10 pt")
    elif LETTER:
        print("  Letter, 1 in margins, one column, Times 12 pt, single spaced, 9 pt after")
    else:
        print("  Letter, 1 in margins, one column, Times 12 pt, 1.5 lines, 12 pt after")


if __name__ == "__main__":
    build()
