-- ieee_filter.lua — reshape a paper written in Markdown into IEEEtran structure.
--
-- Responsibilities:
--   1. Lift Abstract, Index Terms, References and Author biography out of the body
--      into metadata the template places in IEEEtran's own environments.
--   2. Strip manual section numbering ("I. ", "A. ") — IEEEtran numbers sections itself.
--   3. Turn a "**TABLE n. Caption.**" paragraph plus the table that follows it into a
--      full-width table* float with a proper \caption.
--   4. Turn an image plus its following "**Fig. n.** caption" paragraph into a figure
--      float, and point it at the PDF rendition of the SVG.
--   5. Emit Acknowledgment unnumbered.

local stringify = pandoc.utils.stringify

local abstract, keywords, biography = nil, nil, nil
local bibitems = {}

-- ---------------------------------------------------------------- helpers

local function esc(s)
  s = s:gsub("\\", "\\textbackslash{}")
  s = s:gsub("([&%%%$#_{}])", "\\%1")
  s = s:gsub("~", "\\textasciitilde{}")
  s = s:gsub("%^", "\\textasciicircum{}")
  return s
end

-- inline markdown (bold/italic/code/links) -> latex, for cells and captions
local function inlines_to_latex(inlines)
  return pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), "latex")
             :gsub("%s+$", "")
end

local function strip_number(inlines)
  -- "I. Situation: ..." / "A. Genesis" -> drop the leading label
  local txt = stringify(inlines)
  local rest = txt:match("^%u+%.%s+(.*)$") or txt:match("^%u%.%s+(.*)$")
  if not rest then return inlines end
  return pandoc.read(rest, "markdown").blocks[1].content
end

-- ------------------------------------------------------- table conversion

local function table_to_latex(tbl, caption_md, label)
  local ncols = #tbl.colspecs
  local spec = {}
  for i, cs in ipairs(tbl.colspecs) do
    -- last-column prose gets more room; numeric columns stay narrow and centred
    local align = cs[1]
    if align == "AlignRight" or align == "AlignCenter" then
      spec[i] = "c"
    else
      spec[i] = "L"
    end
  end

  local out = {}
  out[#out+1] = "\\begin{table*}[!t]"
  out[#out+1] = "\\renewcommand{\\arraystretch}{1.15}"
  out[#out+1] = "\\caption{" .. caption_md .. "}"
  out[#out+1] = "\\label{" .. label .. "}"
  out[#out+1] = "\\centering"
  out[#out+1] = "\\footnotesize"
  out[#out+1] = "\\begin{tabularx}{\\textwidth}{" .. table.concat(spec) .. "}"
  out[#out+1] = "\\toprule"

  local function row_to_tex(row, bold)
    local cells = {}
    for i, cell in ipairs(row.cells) do
      local txt = inlines_to_latex(pandoc.utils.blocks_to_inlines(cell.contents))
      cells[i] = bold and ("\\textbf{" .. txt .. "}") or txt
    end
    return table.concat(cells, " & ") .. " \\\\"
  end

  for _, row in ipairs(tbl.head.rows) do
    out[#out+1] = row_to_tex(row, true)
  end
  out[#out+1] = "\\midrule"
  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do
      out[#out+1] = row_to_tex(row, false)
    end
  end

  out[#out+1] = "\\bottomrule"
  out[#out+1] = "\\end{tabularx}"
  out[#out+1] = "\\end{table*}"
  return pandoc.RawBlock("latex", table.concat(out, "\n"))
end

-- ------------------------------------------------------------- main pass

function Pandoc(doc)
  local blocks = doc.blocks
  local out = {}
  local i = 1
  local section = nil          -- which lifted section we are inside

  while i <= #blocks do
    local b = blocks[i]

    -- ---- section routing -------------------------------------------------
    if b.t == "Header" then
      local name = stringify(b.content):lower()
      if name == "abstract" then section = "abstract"; i = i + 1; goto continue
      elseif name == "index terms" then section = "keywords"; i = i + 1; goto continue
      elseif name == "references" then section = "references"; i = i + 1; goto continue
      elseif name == "author biography" then section = "biography"; i = i + 1; goto continue
      elseif name == "acknowledgment" or name == "acknowledgement" then
        section = nil
        out[#out+1] = pandoc.RawBlock("latex", "\\section*{Acknowledgment}")
        i = i + 1; goto continue
      elseif b.level == 1 then
        -- the document title; it and the author block that follows it come
        -- from metadata, so discard everything up to the next known header
        section = "frontmatter"
        i = i + 1; goto continue
      else
        section = nil
        b.content = strip_number(b.content)
        b.level = b.level - 1        -- H2 -> \section, H3 -> \subsection
        out[#out+1] = b
        i = i + 1; goto continue
      end
    end

    if section == "frontmatter" then
      i = i + 1; goto continue
    elseif section == "abstract" then
      abstract = inlines_to_latex(pandoc.utils.blocks_to_inlines({ b }))
      i = i + 1; goto continue
    elseif section == "keywords" then
      keywords = inlines_to_latex(pandoc.utils.blocks_to_inlines({ b }))
      i = i + 1; goto continue
    elseif section == "biography" then
      biography = (biography or "") .. inlines_to_latex(
        pandoc.utils.blocks_to_inlines({ b })) .. "\n\n"
      i = i + 1; goto continue
    elseif section == "references" then
      local txt = stringify(b)
      local n, rest = txt:match("^%[(%d+)%]%s*(.*)$")
      if n then
        local body = inlines_to_latex(b.content):gsub("^%s*%[%d+%]%s*", "")
        bibitems[#bibitems+1] = "\\bibitem{ref" .. n .. "} " .. body
      end
      i = i + 1; goto continue
    end

    -- ---- "**TABLE n. Caption.**" followed by a table ----------------------
    if b.t == "Para" then
      local txt = stringify(b)
      local num, cap = txt:match("^TABLE%s+([IVXLC]+)%.%s*(.*)$")
      if num and blocks[i+1] and blocks[i+1].t == "Table" then
        cap = cap:gsub("%s*$", ""):gsub("%.$", "")
        out[#out+1] = table_to_latex(blocks[i+1], esc(cap), "tab:" .. num)
        i = i + 2; goto continue
      end
    end

    -- ---- figure (pandoc 3 Figure node, or a bare image paragraph) ---------
    local img = nil
    if b.t == "Figure" then
      pandoc.walk_block(b, { Image = function(im) img = im end })
    elseif b.t == "Para" and #b.content == 1 and b.content[1].t == "Image" then
      img = b.content[1]
    end
    if img then
      -- match the hyphenated name the build script writes; an underscore in an
      -- \includegraphics argument is a classic LaTeX failure
      local src = img.src:gsub("%.svg$", ".pdf"):gsub("_", "-")
      local capblock = blocks[i+1]
      local cap = ""
      local consumed = 1
      if capblock and capblock.t == "Para" and stringify(capblock):match("^Fig%.") then
        local inl = capblock.content
        -- drop the leading "Fig. n." label; IEEEtran generates it
        local rendered = inlines_to_latex(inl)
        cap = rendered:gsub("^%s*\\textbf{Fig%.%s*%d+%.}%s*", "")
        consumed = 2
      end
      out[#out+1] = pandoc.RawBlock("latex", table.concat({
        "\\begin{figure*}[!t]",
        "\\centering",
        "\\includegraphics[width=\\textwidth]{" .. src .. "}",
        "\\caption{" .. cap .. "}",
        "\\label{fig:1}",
        "\\end{figure*}",
      }, "\n"))
      i = i + consumed; goto continue
    end

    out[#out+1] = b
    i = i + 1
    ::continue::
  end

  local meta = doc.meta
  if abstract  then meta.abstract  = pandoc.RawInline("latex", abstract)  end
  if keywords  then meta.keywords  = pandoc.RawInline("latex", keywords)  end
  if biography then meta.biography = pandoc.RawInline("latex", biography) end
  if #bibitems > 0 then
    meta.bibliography_body = pandoc.RawInline("latex", table.concat(bibitems, "\n\n"))
    meta.bibcount = tostring(#bibitems)
  end

  return pandoc.Pandoc(out, meta)
end
