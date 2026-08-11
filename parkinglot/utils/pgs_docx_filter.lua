-- pgs_docx_filter.lua
-- Pandoc Lua filter for PGS concept paper DOCX conversion.
--
-- Concerns handled:
--   1. Page breaks before H2 headings (major sections).
--      H1 is the document title — no leading break.
--      H3+ are subsections — no break.
--   2. Horizontal rules (---) become hard page breaks.
--      (Reserve --- in source for intentional manual breaks only.)
--
-- Usage (applied automatically by convert_docx_md.sh):
--   pandoc input.md --lua-filter=pgs_docx_filter.lua -o output.docx

------------------------------------------------------------------------
-- 1. Page breaks before H2 (major section) headings
--
-- Every ## heading gets a hard page break injected before it in DOCX.
-- H1 (document title) and H3+ (subsections) are left untouched.
------------------------------------------------------------------------
function Header(h)
  if FORMAT ~= "docx" then
    return h
  end

  if h.level == 2 then
    local page_break = pandoc.RawBlock(
      "openxml",
      '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
    )
    return { page_break, h }
  end

  -- H1 (title) and H3+ (subsections): no modification
  return h
end

------------------------------------------------------------------------
-- 2. Horizontal rule → DOCX hard page break
--
-- Markdown --- in source becomes a new page in the DOCX output.
-- Use sparingly — prefer relying on the H2 rule above for section breaks.
------------------------------------------------------------------------
function HorizontalRule()
  if FORMAT == "docx" then
    return pandoc.RawBlock(
      "openxml",
      '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
    )
  end
end
