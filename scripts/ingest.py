#!/usr/bin/env python3
"""ingest.py — the one adapter.

Reads canonical markdown from `source_root` (pgs_workspace) and writes Hugo-ready
pages into the site's content/ + static/. It NEVER mutates the source tree.

Per section it:
  1. derives Hugo front matter (title/date/draft/weight/series/slug/tags),
  2. strips the leading title/subtitle/part block from the body (front matter owns the title),
  3. rewrites image refs to /assets/... and copies images into static/assets/,
     dropping refs whose target file does not exist (broken pandoc/Word artifacts),
  4. fixes placeholder inter-post links [Part k](link-to-part-k) -> real slug,
  5. lightly unescapes pandoc backslash escapes,
  6. regenerates each target section from scratch (clean, idempotent), preserving _index.md.

stdlib + pyyaml only. No frameworks.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

import yaml

SITE_ROOT = Path(__file__).resolve().parent.parent
ASSET_SRC_SUBDIR = "blogs/assets"  # where canonical blog images live

IMG_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)(?:\{[^}]*\})?\\?")
PANDOC_ESCAPE_RE = re.compile(r"\\([-'\".@\[\]()*_])")
PLACEHOLDER_LINK_RE = re.compile(r"\]\([^)]*link-to-part-(\d+)\)", re.IGNORECASE)
# Redundant series tagline (front matter already records the series) — strip anywhere,
# tolerating a wrapped continuation up to the closing italic '*'.
SERIES_TAGLINE_RE = re.compile(r"\*Part\b[^*]*?\bSeries\b[^*]*?\*")
STRAY_BACKSLASH_RE = re.compile(r"(?m)^\\\s*$")
# Pandoc Word-export artifacts: {.class}/{#anchor} attribute spans and [[x]]() double brackets.
PANDOC_SPAN_RE = re.compile(r"\{[#.][^}]*\}")
DOUBLE_BRACKET_RE = re.compile(r"\[\[([^\]]+)\]\]\(")

# Single leading lines that make up a title block (stripped from body).
# The series tagline is handled globally by SERIES_TAGLINE_RE (wrap-aware).
_TITLE_LINE_RES = [
    re.compile(r"^#{1,6}\s"),                        # ATX heading
]


def _consume_emphasis_run(lines: list[str], i: int) -> int | None:
    """If lines[i:] open a (possibly multi-line) **...** / ***...*** run, return the
    index past its end; else None."""
    if not lines[i].strip().startswith("**"):
        return None
    text = ""
    j = i
    while j < len(lines) and j - i <= 6:
        text = (text + " " + lines[j].strip()).strip()
        if text.rstrip("\\").rstrip().endswith("**") and len(text.rstrip("\\").rstrip()) >= 4:
            return j + 1
        j += 1
    return None


def log(msg: str) -> None:
    print(f"[ingest] {msg}")


def strip_title_block(body: str) -> str:
    """Drop leading blank lines and the opening title/subtitle/part lines."""
    lines = body.splitlines()
    i = 0
    consumed_any = False
    while i < len(lines):
        line = lines[i].strip()
        if line == "":
            i += 1
            continue
        run_end = _consume_emphasis_run(lines, i)
        if run_end is not None:
            i = run_end
            consumed_any = True
            continue
        if any(r.match(line) for r in _TITLE_LINE_RES):
            i += 1
            consumed_any = True
            continue
        break
    if not consumed_any:
        return body
    return "\n".join(lines[i:]).lstrip("\n")


def strip_inline_images(body: str) -> str:
    """Remove all inline image refs from the body. Header images come from the
    `assets/blog_NN.<ext>` convention (see find_header_image), not from body markup."""
    return IMG_RE.sub("", body)


def slugify(text: str) -> str:
    text = PANDOC_SPAN_RE.sub("", text).strip()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text or "section"


def process_images(body: str, src_dir: Path, fig_static: Path, url_prefix: str) -> str:
    """Copy referenced images (resolved relative to the source file's directory) into
    the figures static dir and rewrite paths; keep external URLs; drop missing files."""
    def repl(m: re.Match) -> str:
        path = m.group("path").strip()
        if path.startswith(("http://", "https://", "//")):
            return m.group(0)
        candidate = (src_dir / path).resolve()
        if candidate.is_file():
            fig_static.mkdir(parents=True, exist_ok=True)
            shutil.copy2(candidate, fig_static / candidate.name)
            return f"![{m.group('alt')}]({url_prefix}/{candidate.name})"
        log(f"  dropped missing image: {path}")
        return ""
    return IMG_RE.sub(repl, body)


ASSET_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")


def process_asset_links(body: str, src_dir: Path, fig_static: Path, url_prefix: str) -> str:
    """Rewrite markdown LINKS (not images) that point to a local asset file (png/pdf/etc.):
    copy the file into the figures dir and repoint the href. External/anchor/internal/.md
    links are left untouched."""
    def repl(m: re.Match) -> str:
        text, path = m.group(1), m.group(2).strip()
        if path.startswith(("http://", "https://", "//", "/", "#", "mailto:")):
            return m.group(0)
        target = path.split(" ", 1)[0]  # drop optional ("title")
        if target.lower().endswith(".md") or not target:
            return m.group(0)
        candidate = (src_dir / target).resolve()
        if candidate.is_file():
            fig_static.mkdir(parents=True, exist_ok=True)
            shutil.copy2(candidate, fig_static / candidate.name)
            return f"[{text}]({url_prefix}/{candidate.name})"
        return m.group(0)
    return ASSET_LINK_RE.sub(repl, body)


def split_book(raw: str, split_cfg: dict) -> list[tuple[str, str]]:
    """Split a long document into (title, body) chunks at top-level `# ` headings.
    Titles listed in `skip_titles` (e.g. the ToC) are dropped."""
    marker = split_cfg.get("by_heading", "# ")
    skip = {s.strip().lower() for s in split_cfg.get("skip_titles", [])}
    chunks: list[tuple[str, list[str]]] = []
    for line in raw.splitlines():
        if line.startswith(marker) and not line.startswith(marker + "#"):
            title = PANDOC_SPAN_RE.sub("", line[len(marker):]).strip()
            title = re.sub(r"\s*---\s*", " — ", title)  # pandoc em-dash in titles
            chunks.append((title, []))
        elif chunks:
            chunks[-1][1].append(line)
    out = []
    for title, body_lines in chunks:
        if title.lower() in skip:
            continue
        out.append((title, "\n".join(body_lines).strip()))
    return out


def find_header_image(asset_src_dir: Path, weight: int) -> Path | None:
    """Canonical header image by position: assets/blog_NN.<ext> (any extension)."""
    matches = sorted(asset_src_dir.glob(f"blog_{weight:02d}.*"))
    return matches[0] if matches else None


def clean_body(body: str) -> str:
    body = PANDOC_SPAN_RE.sub("", body)
    body = DOUBLE_BRACKET_RE.sub(r"[\1](", body)
    body = SERIES_TAGLINE_RE.sub("", body)
    body = STRAY_BACKSLASH_RE.sub("", body)
    body = PANDOC_ESCAPE_RE.sub(r"\1", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.lstrip("\n")


def fix_placeholder_links(body: str, part_to_slug: dict[int, str], section_url: str) -> str:
    def repl(m: re.Match) -> str:
        k = int(m.group(1))
        slug = part_to_slug.get(k)
        if slug:
            return f"]({section_url}/{slug}/)"
        log(f"  unresolved placeholder link: part {k}")
        return m.group(0)
    return PLACEHOLDER_LINK_RE.sub(repl, body)


def yaml_front_matter(d: dict) -> str:
    fm = yaml.safe_dump(d, sort_keys=False, allow_unicode=True, default_flow_style=False)
    return f"---\n{fm}---\n\n"


def clean_section_dir(target: Path) -> None:
    """Remove generated pages but keep _index.md."""
    if not target.exists():
        target.mkdir(parents=True, exist_ok=True)
        return
    for child in target.iterdir():
        if child.name == "_index.md":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def run(config_path: Path) -> int:
    cfg = yaml.safe_load(config_path.read_text())
    source_root = Path(cfg["source_root"]).resolve()
    date_base = dt.date.fromisoformat(str(cfg.get("date_base", "2026-01-01")))
    date_step = int(cfg.get("date_step_days", 7))
    asset_src_dir = source_root / ASSET_SRC_SUBDIR
    static_assets = SITE_ROOT / "static" / "assets"      # blog covers (assets/blog_NN.*)
    fig_static = SITE_ROOT / "static" / "figures"        # paper/book figures
    # Regenerate published images from scratch (mirrors "fully replaced" semantics).
    for d in (static_assets, fig_static):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)

    total = 0
    for section_name, sec in cfg.get("sections", {}).items():
        entries = sec.get("entries") or []
        if not entries:
            continue
        target = SITE_ROOT / sec["target"]
        section_url = "/" + sec["target"].replace("content/", "", 1).rstrip("/")
        clean_section_dir(target)

        part_to_slug = {i + 1: e["slug"] for i, e in enumerate(entries) if e.get("slug")}
        default_tags = sec.get("default_tags", [])
        series = sec.get("series")
        use_header_convention = bool(sec.get("header_image"))
        number_titles = bool(sec.get("number_titles"))

        log(f"section '{section_name}': {len(entries)} entries -> {target}")
        for idx, entry in enumerate(entries, start=1):
            src = source_root / entry["src"]
            if not src.exists():
                log(f"  MISSING SOURCE: {src}")
                return 1
            raw = src.read_text(encoding="utf-8")

            def write_page(title, body, slug, weight, fname, cover=None, extra=None):
                nonlocal total
                if entry.get("date"):
                    date = str(entry["date"])
                else:
                    # Synthesize ascending dates, clamped to today so long sections
                    # don't fall under Hugo's buildFuture=false cutoff.
                    synth = date_base + dt.timedelta(days=(weight - 1) * date_step)
                    date = min(synth, dt.date.today()).isoformat()
                fm = {"title": title, "date": date, "draft": False,
                      "weight": weight, "slug": slug}
                if series:
                    fm["series"] = [series]
                tags = entry.get("tags", default_tags)
                if tags:
                    fm["tags"] = tags
                if cover:
                    fm["cover"] = cover
                if extra:
                    fm.update(extra)
                (target / fname).write_text(
                    yaml_front_matter(fm) + body.rstrip() + "\n", encoding="utf-8")
                total += 1

            # --- Book: split one long source into per-chapter pages ---
            if entry.get("split"):
                chapters = split_book(raw, entry["split"])
                log(f"  [{idx:>2}] book split -> {len(chapters)} chapters")
                for cidx, (ctitle, cbody) in enumerate(chapters, start=1):
                    cbody = process_images(cbody, src.parent, fig_static, "/figures")
                    cbody = process_asset_links(cbody, src.parent, fig_static, "/figures")
                    cbody = clean_body(cbody)
                    cslug = slugify(ctitle)
                    write_page(ctitle, cbody, cslug, cidx, f"book_{cidx:02d}_{cslug}.md")
                continue

            # --- Single-page entry (blog / paper / learn) ---
            body = strip_title_block(raw)
            cover = None
            if use_header_convention:
                # Header image is assets/blog_NN.<ext> by position; inline images dropped.
                body = strip_inline_images(body)
                img = find_header_image(asset_src_dir, idx)
                if img:
                    shutil.copy2(img, static_assets / img.name)
                    cover = {"image": f"/assets/{img.name}", "alt": entry["title"]}
                else:
                    log(f"  [{idx:>2}] no header image yet (expected assets/blog_{idx:02d}.*)")
            else:
                body = process_images(body, src.parent, fig_static, "/figures")

            body = clean_body(body)
            if part_to_slug:
                body = fix_placeholder_links(body, part_to_slug, section_url)
            body = process_asset_links(body, src.parent, fig_static, "/figures")

            # DOI / PDF placeholders for papers (filled in Phase 7).
            extra = {}
            badge = []
            if entry.get("doi"):
                extra["doi"] = entry["doi"]
                badge.append(f"**DOI:** [{entry['doi']}](https://doi.org/{entry['doi']})")
            if entry.get("pdf"):
                extra["pdf"] = entry["pdf"]
                badge.append(f"[Download PDF]({entry['pdf']})")
            if badge:
                body = " · ".join(badge) + "\n\n" + body

            # Filename carries the series number (blog_NN_) so it lines up with
            # assets/blog_NN.<ext>; the URL is still governed by front-matter `slug`.
            fname = (f"blog_{idx:02d}_{entry['slug']}.md"
                     if use_header_convention else f"{entry['slug']}.md")
            # Orient the reader with the blog number in the title. The number is taken from
            # the SOURCE filename (e.g. pgs_09_smart_coding.md -> 09), which the author maintains
            # as the canonical series number — so it always matches in-post recaps. Sort is
            # still ascending by weight (config order).
            if number_titles:
                fnum = re.search(r"_(\d+)", Path(entry["src"]).name)
                nn = int(fnum.group(1)) if fnum else idx
                title = f"#{nn:02d} — {entry['title']}"
            else:
                title = entry["title"]
            write_page(title, body, entry["slug"], idx, fname, cover=cover,
                       extra=extra or None)

    log(f"done: {total} pages written.")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Ingest canonical markdown into the Hugo site.")
    ap.add_argument("--config", default=str(SITE_ROOT / "ingest.config.yaml"))
    args = ap.parse_args()
    sys.exit(run(Path(args.config).resolve()))


if __name__ == "__main__":
    main()