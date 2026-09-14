# utils — paper conversion toolchain

Markdown is the authored source for every paper here. This directory turns it into
the format a venue asks for, and nothing in a generated file is edited by hand: a
formatting change belongs in a family's reference document or filter, so the output
can always be regenerated from source.

## Layout

    convert_docx_md.sh      the one shared driver, md ⇄ docx
    ase/                    Springer ASE journal
    ieee/                   IEEE conference — LaTeX and DOCX paths
    jss/                    Elsevier JSS journal
    pgs/                    PGS concept papers
    wiley/                  Wiley journals — SPE, JSEP

Each family owns a subdirectory holding its reference document, its optional Lua
filter, and the builder that produces the reference document. Families share the
driver and nothing else, so a change to one venue's layout cannot reach another's.

## Forward: markdown to Word

    ./convert_docx_md.sh paper.md            # defaults to the pgs family
    ./convert_docx_md.sh paper.md ase

The driver resolves `<family>/<family>_reference.docx` and applies
`<family>/<family>_docx_filter.lua` when one exists. If the reference document is
missing it is built first from `<family>/make_<family>_reference_docx.py`.

## Reverse: Word back to markdown

    ./convert_docx_md.sh paper.docx

Writes `<basename>_from_docx.md` rather than overwriting an existing source, and
extracts images to `<basename>_media/`.

## The families

**ase** — 11 pt body, 9 pt tables, 6 pt paragraph spacing, 1 in margins, centered
page numbers, and `keepNext` on headings and captions so neither is stranded at the
foot of a page. No filter: Springer wants figures and tables in the body where they
are referenced, and a page break before each section would only add pages.

**ieee** — two paths that do not interact. `convert_ieee.sh` produces LaTeX via
`ieeetran.latex` and `ieee_filter.lua` for the camera-ready PDF; the DOCX path uses
`ieee_reference.docx` (two-column, with a letter variant) and `ieee_docx_filter.lua`,
which injects the continuous section break IEEE needs so the title block runs full
width above a two-column body.

**jss** — 12 pt body, single spaced, 1 in margins, page numbers on, single column.
A clean reading copy rather than a typeset page; line numbering is off and is one
edit to restore.

**pgs** — `pgs_docx_filter.lua` starts every `##` section on a new page, and turns a
horizontal rule into a hard break. That suits a concept paper read section by
section.

**wiley** — Times New Roman throughout, 12 pt body, 10 pt tables, single spaced,
single column, 1 in margins, as Wiley asks. Tables at 10 pt because a 26-row table
overruns the page at body size. `wiley_docx_filter.lua` starts every `##` section on
a new page except the abstract, which stays with the title block. The figure and
tables live inside the sections that reference them, so the break separates neither
from its text.

## Adding a family

Create `<family>/`, add `make_<family>_reference_docx.py` writing
`<family>_reference.docx` beside itself, and optionally `<family>_docx_filter.lua`.
The driver needs no change; it reports the available families when given an unknown
one.
