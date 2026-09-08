-- ase_docx_filter.lua — Springer ASE journal layout for the DOCX path.
--
-- Concerns handled:
--   1. Every major division starts a new page: sections 1..11, References, and
--      each appendix. The Abstract is exempt — it belongs with the title block,
--      and the run of breaks begins after it.
--   2. Horizontal rules are dropped. They separate divisions in the markdown
--      source, and a rule sitting immediately above a page break renders as a
--      stray line at the foot of the preceding page.
--
-- Usage (applied automatically by convert_docx_md.sh when family = ase):
--   pandoc input.md --lua-filter=ase_docx_filter.lua -o output.docx

local PAGE_BREAK = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

------------------------------------------------------------------------
-- 1. Page break before every H2 except the Abstract
--
-- H1 is the document title. H3+ are subsections and stay with their parent.
-- The Abstract is identified by its text rather than by position, so the rule
-- survives a reordering of the front matter.
------------------------------------------------------------------------
function Header(h)
  if FORMAT ~= "docx" or h.level ~= 2 then
    return h
  end

  if pandoc.utils.stringify(h):match("^%s*Abstract") then
    return h
  end

  return { pandoc.RawBlock("openxml", PAGE_BREAK), h }
end

------------------------------------------------------------------------
-- 2. Horizontal rules carry no meaning in the rendered manuscript
------------------------------------------------------------------------
function HorizontalRule()
  if FORMAT == "docx" then
    return {}
  end
end
