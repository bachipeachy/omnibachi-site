-- wiley_docx_filter.lua
-- Pandoc Lua filter for the Wiley journal manuscript DOCX conversion.
--
-- One concern: every `##` section starts on a new page.
--
--   H1 is the document title and takes no leading break.
--   H2 covers the numbered sections, the AI-use declaration and the references.
--   H3+ are subsections and stay with the section they belong to.
--
-- The figure and both tables sit inside the sections that reference them, so a
-- break at H2 does not separate either from its text. It does add roughly one
-- partial page per section to the manuscript.
--
-- Usage (applied automatically by convert_docx_md.sh):
--   pandoc input.md --lua-filter=wiley_docx_filter.lua -o output.docx

local first_h2 = true

function Header(h)
  if FORMAT ~= "docx" or h.level ~= 2 then
    return h
  end

  -- The abstract is the first H2 and follows the title block on page one.
  if first_h2 then
    first_h2 = false
    return h
  end

  local page_break = pandoc.RawBlock(
    "openxml",
    '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
  )
  return { page_break, h }
end
