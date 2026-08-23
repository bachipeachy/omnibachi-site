#!/usr/bin/env bash
# convert_paper.sh — bidirectional paper conversion using pandoc
#
# Usage:
#   ./convert_paper.sh <input_file>
#
# Direction is inferred from the input file extension:
#   .md   → produces <basename>.docx   (forward: md → docx)
#   .docx → produces <basename>.md     (reverse: docx → md)
#
# Forward conversion options applied:
#   --reference-doc  pgs_reference.docx  (page numbers, letter margins)
#   --lua-filter     pgs_docx_filter.lua (page breaks, table widths)
#
# Reverse conversion options applied:
#   --wrap=none        (no line-wrapping — one paragraph per line)
#   --markdown-headings=atx  (## style headings)
#   --extract-media    (images extracted to <basename>_media/)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <file.md | file.docx>" >&2
  exit 1
fi

INPUT="$1"
BASENAME="${INPUT%.*}"
EXT="${INPUT##*.}"

case "${EXT}" in
  md)
    OUTPUT="${BASENAME}.docx"
    REFERENCE="${SCRIPT_DIR}/pgs_reference.docx"
    FILTER="${SCRIPT_DIR}/pgs_docx_filter.lua"

    if [[ ! -f "${REFERENCE}" ]]; then
      echo "Building reference.docx …"
      python3 "${SCRIPT_DIR}/make_reference_docx.py"
    fi

    echo "Forward: ${INPUT} → ${OUTPUT}"
    pandoc "${INPUT}" \
      --reference-doc="${REFERENCE}" \
      --lua-filter="${FILTER}" \
      -o "${OUTPUT}"
    echo "Done: ${OUTPUT}"
    ;;

  docx)
    OUTPUT="${BASENAME}_from_docx.md"
    MEDIA_DIR="${BASENAME}_media"

    # Refuse to silently overwrite an existing .md of the same base name
    if [[ -f "${BASENAME}.md" ]]; then
      echo "Note: ${BASENAME}.md already exists — writing to ${OUTPUT} to avoid overwrite."
    fi

    echo "Reverse: ${INPUT} → ${OUTPUT}"
    pandoc "${INPUT}" \
      --from=docx \
      --to=markdown \
      --wrap=none \
      --markdown-headings=atx \
      --extract-media="${MEDIA_DIR}" \
      -o "${OUTPUT}"
    echo "Done: ${OUTPUT}"
    if [[ -d "${MEDIA_DIR}" ]]; then
      echo "Media: ${MEDIA_DIR}/"
    fi
    ;;

  *)
    echo "Unsupported extension: .${EXT}  (expected .md or .docx)" >&2
    exit 1
    ;;
esac
