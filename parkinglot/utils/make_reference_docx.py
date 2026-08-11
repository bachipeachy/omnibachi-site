#!/usr/bin/env python3
"""
make_reference_docx.py — Generate pgs_reference.docx with a centered page-number footer.

Strategy (no python-docx dependency):
  1. Generate pandoc's default reference.docx via subprocess.
  2. Open the DOCX (a ZIP archive) and inject:
       - word/footer1.xml        — centered PAGE field
       - word/_rels/document.xml.rels  — relationship entry for the footer
       - word/document.xml       — footerReference in sectPr
       - [Content_Types].xml     — Override entry for footer1.xml
  3. Write the modified bytes to pgs_reference.docx.

Usage (called automatically by convert_docx_md.sh when pgs_reference.docx is missing):
    python3 make_reference_docx.py

To customize styles after generation:
  1. Open pgs_reference.docx in Word or LibreOffice.
  2. Edit Named Styles only (not direct formatting).
  3. Save — the file is used as-is on the next conversion run.
"""

import io
import os
import subprocess
import sys
import zipfile


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(SCRIPT_DIR, "pgs_reference.docx")

REL_FOOTER = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer"
)
CT_FOOTER = (
    "application/vnd.openxmlformats-officedocument"
    ".wordprocessingml.footer+xml"
)

# Centered page number footer using the PAGE field.
# fldCharType sequence: begin → instrText → separate → cached value → end
FOOTER_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:r>
      <w:fldChar w:fldCharType="begin"/>
    </w:r>
    <w:r>
      <w:instrText xml:space="preserve"> PAGE \\* MERGEFORMAT </w:instrText>
    </w:r>
    <w:r>
      <w:fldChar w:fldCharType="separate"/>
    </w:r>
    <w:r>
      <w:t>1</w:t>
    </w:r>
    <w:r>
      <w:fldChar w:fldCharType="end"/>
    </w:r>
  </w:p>
</w:ftr>
"""


def pandoc_version():
    try:
        result = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True, text=True, check=True,
        )
        return result.stdout.splitlines()[0]
    except FileNotFoundError:
        return None


def get_default_reference_bytes():
    result = subprocess.run(
        ["pandoc", "--print-default-data-file", "reference.docx"],
        capture_output=True,
        check=True,
    )
    return result.stdout


def inject_page_number_footer(docx_bytes):
    """
    Inject a centered page-number footer into a DOCX archive (bytes → bytes).

    Modifies three existing entries and adds one new file:
      [Content_Types].xml       — register footer1.xml content type
      word/_rels/document.xml.rels  — add footer relationship
      word/document.xml         — add footerReference to sectPr
      word/footer1.xml          — new file with PAGE field
    """
    FOOTER_ID = "rIdPgsFooter1"
    FOOTER_PART = "word/footer1.xml"
    RELS_PART = "word/_rels/document.xml.rels"
    DOC_PART = "word/document.xml"
    CT_PART = "[Content_Types].xml"

    in_buf = io.BytesIO(docx_bytes)
    out_buf = io.BytesIO()

    with zipfile.ZipFile(in_buf, "r") as zin:
        names = zin.namelist()

        rels_text = zin.read(RELS_PART).decode("utf-8")
        doc_text = zin.read(DOC_PART).decode("utf-8")
        ct_text = zin.read(CT_PART).decode("utf-8")

        # 1. Add footer relationship (idempotent guard on FOOTER_ID)
        if FOOTER_ID not in rels_text:
            rel_entry = (
                f'<Relationship Id="{FOOTER_ID}" '
                f'Type="{REL_FOOTER}" '
                f'Target="footer1.xml"/>'
            )
            rels_text = rels_text.replace(
                "</Relationships>",
                rel_entry + "\n</Relationships>",
            )

        # 2. Add footerReference into sectPr (insert before closing tag)
        if FOOTER_ID not in doc_text:
            footer_ref = (
                f'<w:footerReference w:type="default" r:id="{FOOTER_ID}"/>'
            )
            # sectPr may appear multiple times; patch only the last (body sectPr)
            last_idx = doc_text.rfind("</w:sectPr>")
            if last_idx != -1:
                doc_text = (
                    doc_text[:last_idx]
                    + footer_ref
                    + doc_text[last_idx:]
                )

        # 3. Register content type for footer1.xml
        if "footer1.xml" not in ct_text:
            ct_entry = (
                f'<Override PartName="/word/footer1.xml" '
                f'ContentType="{CT_FOOTER}"/>'
            )
            ct_text = ct_text.replace("</Types>", ct_entry + "\n</Types>")

        with zipfile.ZipFile(out_buf, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for name in names:
                if name == RELS_PART:
                    zout.writestr(name, rels_text.encode("utf-8"))
                elif name == DOC_PART:
                    zout.writestr(name, doc_text.encode("utf-8"))
                elif name == CT_PART:
                    zout.writestr(name, ct_text.encode("utf-8"))
                else:
                    zout.writestr(name, zin.read(name))

            # Add footer file (not in the original archive)
            zout.writestr(FOOTER_PART, FOOTER_XML.encode("utf-8"))

    return out_buf.getvalue()


def build_reference_docx():
    version = pandoc_version()
    if version is None:
        print("ERROR: pandoc not found on PATH. Install pandoc to proceed.", file=sys.stderr)
        sys.exit(1)

    print(f"Using {version}")
    print("Generating base reference docx from pandoc defaults …")
    docx_bytes = get_default_reference_bytes()

    print("Injecting centered page-number footer …")
    modified = inject_page_number_footer(docx_bytes)

    with open(OUTPUT, "wb") as f:
        f.write(modified)

    size = os.path.getsize(OUTPUT)
    print(f"Created: {OUTPUT} ({size:,} bytes)")
    print("Footer: centered page number (PAGE field, all pages).")
    print()
    print("To customize styles (fonts, margins, heading sizes):")
    print("  1. Open pgs_reference.docx in Word or LibreOffice")
    print("  2. Edit Named Styles only (Heading 1, Heading 2, Normal, etc.)")
    print("  3. Save — used as-is on the next conversion run")


if __name__ == "__main__":
    build_reference_docx()
