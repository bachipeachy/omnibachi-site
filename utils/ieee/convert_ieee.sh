#!/usr/bin/env bash
# convert_ieee.sh — Markdown paper -> IEEEtran LaTeX, ready to compile.
#
# Usage:  ./convert_ieee.sh <paper.md> [outdir]
#
# Produces <outdir>/ containing:
#   paper.tex          IEEEtran conference source
#   IEEEtran.cls       the class file, if fetched or found locally
#   *.pdf              figures converted from SVG
#
# Compilation is not attempted here: no TeX engine is assumed to be present.
# Upload the directory to Overleaf, or install a TeX distribution and run
# `pdflatex paper && pdflatex paper` (twice, for the reference numbers).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

[[ $# -ge 1 ]] || { echo "Usage: $0 <paper.md> [outdir]" >&2; exit 1; }
INPUT="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
SRC_DIR="$(dirname "$INPUT")"
OUTDIR="${2:-$SRC_DIR/ieee_build}"
mkdir -p "$OUTDIR"

command -v pandoc >/dev/null || { echo "pandoc not found on PATH" >&2; exit 1; }

# --- figures: LaTeX cannot include SVG directly; render each to PDF ----------
shopt -s nullglob
for svg in "$SRC_DIR"/*.svg; do
  base="$(basename "${svg%.svg}")"
  base="${base//_/-}"   # underscores are hostile in \includegraphics arguments
  if command -v rsvg-convert >/dev/null; then
    rsvg-convert -f pdf -o "$OUTDIR/$base.pdf" "$svg"
  elif command -v inkscape >/dev/null; then
    inkscape "$svg" --export-type=pdf --export-filename="$OUTDIR/$base.pdf" >/dev/null 2>&1
  else
    echo "WARNING: no rsvg-convert or inkscape; $base.svg not converted" >&2
    continue
  fi
  echo "  figure: $base.pdf"
done
shopt -u nullglob

# --- class file -------------------------------------------------------------
if [[ ! -f "$OUTDIR/IEEEtran.cls" ]]; then
  if command -v kpsewhich >/dev/null && kpsewhich IEEEtran.cls >/dev/null 2>&1; then
    cp "$(kpsewhich IEEEtran.cls)" "$OUTDIR/"
    echo "  class:  IEEEtran.cls (from local TeX installation)"
  elif command -v curl >/dev/null; then
    if curl -fsSL -o "$OUTDIR/IEEEtran.cls" \
        "https://mirrors.ctan.org/macros/latex/contrib/IEEEtran/IEEEtran.cls" \
       && head -c 200 "$OUTDIR/IEEEtran.cls" | grep -q "IEEEtran"; then
      echo "  class:  IEEEtran.cls (fetched from CTAN)"
    else
      rm -f "$OUTDIR/IEEEtran.cls"
      echo "  class:  NOT fetched — Overleaf provides IEEEtran natively" >&2
    fi
  fi
fi

# --- convert ----------------------------------------------------------------
OUT_TEX="$OUTDIR/paper.tex"
CLASSOPTS="conference"
[[ -n "${REVIEW:-}" ]] && CLASSOPTS="12pt,draftcls,onecolumn"
echo "  class:  IEEEtran [$CLASSOPTS]"

pandoc "$INPUT" \
  --from=markdown \
  --metadata=classoptions:"$CLASSOPTS" \
  --to=latex \
  --standalone \
  --template="$SCRIPT_DIR/ieeetran.latex" \
  --lua-filter="$SCRIPT_DIR/ieee_filter.lua" \
  --metadata-file="$SCRIPT_DIR/paper_meta.yaml" \
  --top-level-division=section \
  -o "$OUT_TEX"

echo "Done: $OUT_TEX"

# --- compile, if a TeX engine is present ------------------------------------
# BasicTeX installs to /Library/TeX/texbin, which is not always on PATH.
export PATH="/Library/TeX/texbin:$PATH"

if command -v pdflatex >/dev/null; then
  echo "Compiling (two passes — the second resolves reference numbers) …"
  cd "$OUTDIR"
  for pass in 1 2; do
    if ! pdflatex -interaction=nonstopmode -halt-on-error paper.tex > "pass${pass}.log" 2>&1; then
      echo "LaTeX failed on pass ${pass}. First error:" >&2
      grep -m3 -A3 '^!' "pass${pass}.log" >&2 || tail -20 "pass${pass}.log" >&2
      exit 1
    fi
  done
  pages="$(command -v pdfinfo >/dev/null && pdfinfo paper.pdf | awk '/^Pages/{print $2}')"
  over="$(grep -c 'Overfull' paper.log || true)"
  echo "Done: $OUTDIR/paper.pdf${pages:+ (${pages} pages)}"
  [[ "${over:-0}" -gt 0 ]] && echo "Note: ${over} overfull box(es) — check paper.log"
  rm -f pass1.log pass2.log
else
  echo
  echo "No TeX engine found. Upload $OUTDIR/ to Overleaf (IEEEtran is preinstalled),"
  echo "or install BasicTeX and re-run."
fi
