-- ieee_docx_filter.lua — IEEE conference layout for the DOCX path.
--
-- The reference document sets the whole body two-column. IEEE puts the title,
-- author block, abstract and index terms full width, which Word expresses as a
-- continuous section break. Pandoc emits only one section, so the break is
-- injected here as raw OOXML: everything before it is one column, everything
-- after inherits the reference document's two.
--
-- Also: drops the author block that sits between the H1 title and the first
-- heading (it belongs to the title block, not the body), and promotes headings
-- so "## I. Situation" becomes a Heading 1.

local stringify = pandoc.utils.stringify
local inch = function(v) return math.floor(v * 1440 + 0.5) end

local ONE_COLUMN_BREAK = pandoc.RawBlock("openxml", table.concat({
  '<w:p><w:pPr><w:sectPr>',
  '<w:footnotePr><w:numRestart w:val="eachSect"/></w:footnotePr>',
  string.format('<w:pgSz w:w="%d" w:h="%d"/>', inch(8.5), inch(11)),
  string.format('<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" '
                .. 'w:header="%d" w:footer="%d" w:gutter="0"/>',
                inch(0.75), inch(0.625), inch(1.0), inch(0.625),
                inch(0.5), inch(0.5)),
  '<w:cols w:num="1"/>',
  '<w:type w:val="continuous"/>',
  '</w:sectPr></w:pPr></w:p>',
}, ""))

function Pandoc(doc)
  local out, i = {}, 1
  local blocks = doc.blocks
  local in_frontmatter = false
  local break_emitted = false

  while i <= #blocks do
    local b = blocks[i]

    if b.t == "Header" then
      local name = stringify(b.content):lower()
      if b.level == 1 then
        -- the title and the author block below it come from metadata, so that
        -- pandoc renders them in the reference document's Title/Author styles
        in_frontmatter = true
        i = i + 1
        goto continue
      end

      in_frontmatter = false

      -- The full-width section break only matters in the two-column form; a
      -- one-column manuscript has nothing to break out of.
      if not break_emitted and os.getenv("TWOCOL") ~= nil
         and name ~= "abstract" and name ~= "index terms" then
        out[#out+1] = ONE_COLUMN_BREAK
        break_emitted = true
      end

      b.level = math.max(1, b.level - 1)   -- H2 -> Heading 1, H3 -> Heading 2
      out[#out+1] = b
      i = i + 1
      goto continue
    end

    if in_frontmatter then
      i = i + 1
      goto continue
    end

    out[#out+1] = b
    i = i + 1
    ::continue::
  end

  return pandoc.Pandoc(out, doc.meta)
end
