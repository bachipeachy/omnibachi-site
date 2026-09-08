#!/usr/bin/env bash
# convert_paper.sh — bidirectional paper conversion using pandoc
#
# Usage:
#   ./convert_paper.sh <input_file> [family]
#
# `family` selects the reference document and filter (default: pgs). Each paper
# family owns its own pair; the IEEE path has its own driver in ieee/ and is not
# reached from here.
#
# Direction is inferred from the input file extension:
#   .md   → produces <basename>.docx   (forward: md → docx)
#   .docx → produces <basename>.md     (reverse: docx → md)
#
# Forward conversion options applied:
#   --reference-doc  <family>/<family>_reference.docx
#   --lua-filter     <family>/<family>_docx_filter.lua  (skipped if absent)
#
# Each paper family owns a subdirectory holding its reference document, its
# optional filter, and the builder that produces the reference document. Nothing
# is shared between families except this driver.
#
# Reverse conversion options applied:
#   --wrap=none        (no line-wrapping — one paragraph per line)
#   --markdown-headings=atx  (## style headings)
#   --extract-media    (images extracted to <basename>_media/)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <file.md | file.docx> [family]   # family defaults to pgs" >&2
  exit 1
fi

INPUT="$1"
FAMILY="${2:-pgs}"
BASENAME="${INPUT%.*}"
EXT="${INPUT##*.}"

case "${EXT}" in
  md)
    OUTPUT="${BASENAME}.docx"
    FAMILY_DIR="${SCRIPT_DIR}/${FAMILY}"
    REFERENCE="${FAMILY_DIR}/${FAMILY}_reference.docx"
    FILTER="${FAMILY_DIR}/${FAMILY}_docx_filter.lua"

    if [[ ! -d "${FAMILY_DIR}" ]]; then
      echo "Unknown family '${FAMILY}' — expected a directory at ${FAMILY_DIR}" >&2
      echo "Available: $(cd "${SCRIPT_DIR}" && ls -d */ 2>/dev/null | tr -d / | tr '\n' ' ')" >&2
      exit 1
    fi

    if [[ ! -f "${REFERENCE}" ]]; then
      echo "Building $(basename "${REFERENCE}") …"
      python3 "${FAMILY_DIR}/make_${FAMILY}_reference_docx.py"
    fi

    echo "Forward: ${INPUT} → ${OUTPUT}  [${FAMILY}]"
    if [[ -f "${FILTER}" ]]; then
      pandoc "${INPUT}" --reference-doc="${REFERENCE}" --lua-filter="${FILTER}" -o "${OUTPUT}"
    else
      pandoc "${INPUT}" --reference-doc="${REFERENCE}" -o "${OUTPUT}"
    fi
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
