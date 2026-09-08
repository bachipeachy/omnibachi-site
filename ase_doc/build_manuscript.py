#!/usr/bin/env python3
"""Assemble the single-file ASE manuscript from the draft and the tables.

The draft and the table file stay the single source of truth. This regenerates
`ase_manuscript.md` and `ase_manuscript.docx` with every figure and table placed
in the body at its first substantive reference, which is what Springer asks for
in an editable single-file submission.

    python3 build_manuscript.py          # Springer single-file submission
    python3 build_manuscript.py --site   # frozen Hugo page for omnibachi.org

The --site target writes the canonical paper into content/papers/ and copies the
authored SVGs into static/figures/ase/. It is deliberately run by hand, once per
published Zenodo version: the site page is the frozen rendition of the deposit
named in its front matter, not a mirror that follows the working manuscript.
"""
import io, os, re, subprocess, sys

TEXT  = "text_ase_autonomy_without_authority.md"
TABLES = "tables_ase_autonomy_without_authority.md"
OUT_MD = "manuscript_ase_autonomy_without_authority.md"
OUT_DOCX = "manuscript_ase_autonomy_without_authority.docx"

SITE_MD  = "../content/papers/pgc_autonomy_without_authority_v0.md"
SITE_FIG = "../static/figures/ase"
SITE_URL = "/figures/ase"
DOI      = "https://doi.org/10.5281/zenodo.22650863"
FRONT = """---
title: 'Protocol-Governed Human-AI Software Engineering: Autonomy Without Authority'
date: '2026-09-08'
weight: 5
slug: autonomy-without-authority
---
**Author:** Bhash Ganti (aka Bachi)

**(c) 2026 Bhash Ganti. All rights reserved. Released under the Apache-2.0 License.**

**Preprint:** [%s](%s) — this page is the frozen rendition of that deposit.

---

""" % (DOI, DOI)

FIGCAP = {
 1:("ase_fig1_shifting_role","The human role shifted; the authorization point did not. The figure motivates the question and reports no result: the conditions it names are argued, not measured."),
 2:("ase_fig2_sdlc_scope","The whole lifecycle, not the development stage. Rows describe the architecture's intent; Section 8 reports which boundaries were exercised."),
 3:("ase_fig3_authority_vs_activity","Authority and activity, separated by two boundaries. The activity row is a summary of what an agent may do, not a dependency graph. Solid marks an implemented mechanism; dashed marks architectural intent or a deployment act that is not enforced in this realization."),
 4:("ase_fig4_governing_boundary","The boundary is set before the agent acts. The containment shown is architectural intent; the annotation on each withheld item names its mechanism, and Section 8.2 reports which were exercised."),
 5:("ase_fig5_what_the_human_supplies","Four inputs fixed before the agent acts — three established by a human, one inherited from the previous cycle."),
 6:("ase_fig6_concern_graph","The P0–P8 concern graph. Solid edges are declared priors between adjacent phases; dashed edges are direct citations of P0. Declared priors are a dependency relation, not an enforced input surface."),
 7:("ase_fig7_intent_partition","Four concerns across P5–P8, not four names for one specification. Register counts are properties of this implementation at the pinned revision."),
 8:("ase_fig8_candidate_to_baseline","Three responsibilities, deliberately not fused. Admission and sealing are enforced by the toolchain; promotion is an operator act, with no callable and no actor check in this realization."),
 9:("ase_fig9_execution_partition","Execution realizes; it does not determine. The five prohibitions are separate properties: filled marks the two the reported case stimulated, open marks the three it did not."),
 10:("ase_fig10_agent_mediated_evolution","Direct repository mutation beside governed transformation. The agent performs the engineering work in both; what differs is whether its output is the new state or a candidate."),
 11:("ase_fig11_component_map","Implementation components and artifact flow. Repository counts, published distributions and artifact totals are version-sensitive properties of one pinned revision."),
 12:("ase_fig12_worked_episode","A governed transformation performed by an agent. Solid arrows are observed transitions in this run; the refusal branch is a fixture, not a candidate the worker produced and governance rejected."),
 13:("ase_fig13_baseline_diff","What the transformation added, and what it left alone. Identifiers are snapshot identities, not projection hashes."),
 14:("ase_fig14_mutation_discrimination","Why a passing demonstration is not evidence that its guard was exercised."),
}

def table_block(tables, num):
    m = re.search(r"^## Table %s · (.+?)$" % re.escape(num), tables, re.M)
    if not m: sys.exit("no Table " + num)
    start = m.end()
    nxt = re.search(r"^## Table ", tables[start:], re.M)
    body = tables[start:start + (nxt.start() if nxt else len(tables) - start)]
    return m.group(1).strip(), body.strip().rstrip("-").strip()

def fig(n):
    f, cap = FIGCAP[n]
    return "\n![**Fig. %d** %s](figures/png/%s.png){width=6in}\n" % (n, cap, f)

def tab(num, title, body):
    return "\n**Table %s** %s\n\n%s\n" % (num, title, body)

def export_pngs():
    """Word embeds raster, so render the authored SVGs at 300 dpi.

    Regenerated on every build rather than committed: they are derived from the
    SVGs, and several MB of binary churn per figure edit buys nothing the SVG and
    the submission PDF do not already carry.
    """
    import glob
    os.makedirs("figures/png", exist_ok=True)
    for svg in sorted(glob.glob("figures/ase_fig*.svg")):
        png = "figures/png/" + os.path.basename(svg)[:-4] + ".png"
        if os.path.exists(png) and os.path.getmtime(png) >= os.path.getmtime(svg):
            continue
        subprocess.run(["rsvg-convert", "-f", "png", "-w", "1800", "-d", "300", "-p", "300",
                        "-o", png, svg], check=True)


def site_fig(n):
    """Hugo figure: absolute static path, SVG, and no pandoc attribute block."""
    f, cap = FIGCAP[n]
    return "\n![**Fig. %d** %s](%s/%s.svg)\n" % (n, cap, SITE_URL, f)


def write_site(s):
    """Freeze the assembled body as the canonical Hugo page."""
    import glob, shutil
    os.makedirs(SITE_FIG, exist_ok=True)
    copied = 0
    for svg in sorted(glob.glob("figures/ase_fig*.svg")):
        shutil.copy2(svg, os.path.join(SITE_FIG, os.path.basename(svg)))
        copied += 1
    if copied != 14: sys.exit("build_manuscript: expected 14 SVGs, copied %d" % copied)

    # The Springer title block is a pandoc line block; Hugo carries the same
    # facts in front matter, so drop it rather than render pipes into the page.
    body = re.sub(r"^# .*?\n\n(?:\| .*\n)+", "", s, count=1, flags=re.M)
    if body.lstrip().startswith("|"): sys.exit("build_manuscript: title block not removed")
    out = FRONT + body.lstrip()
    io.open(SITE_MD, "w", encoding="utf-8").write(out)
    print("%s — %d words, %d SVGs into %s" % (SITE_MD, len(out.split()), copied, SITE_FIG))


def main():
    site = "--site" in sys.argv
    if not site:
        export_pngs()
    s = io.open(TEXT, encoding="utf-8").read()
    tables = io.open(TABLES, encoding="utf-8").read()
    # --- front matter ---
    # The author block is whatever plain lines sit between the title and the Abstract
    # heading, which markdown would join into one paragraph. A pandoc line block keeps
    # them as hard breaks in Word without putting formatting characters into the authored
    # source. Matched by position rather than by content so that editing the affiliation
    # cannot silently turn the substitution into a no-op.
    m = re.search(r"^(# .+?\n\n)(.+?)(\n\n## Abstract\n)", s, re.S | re.M)
    if not m: sys.exit("build_manuscript: no author block between the title and Abstract")
    authors = "\n".join("| " + ln.strip() for ln in m.group(2).strip().split("\n") if ln.strip())
    s = s[:m.start(2)] + authors + s[m.end(2):]

    # The abstract is a blockquote in the draft so it reads as set apart; Word renders that
    # as an indented quote, which is wrong for an abstract. Strip the marker from every
    # paragraph of the section — stripping only the first leaves the rest styled BlockText.
    m = re.search(r"^## Abstract\n(.*?)(?=^## )", s, re.S | re.M)
    if not m: sys.exit("build_manuscript: no abstract section")
    body = re.sub(r"^> ?", "", m.group(1), flags=re.M)
    if re.search(r"^> ", body, re.M): sys.exit("build_manuscript: abstract still blockquoted")
    s = s[:m.start(1)] + body + s[m.end(1):]

    T = {n: table_block(tables, n) for n in ["1","2","3","4","5","6","7","8"]}

    CAPTION = {
      "1": "Related work by locus of authority. Columns give, for each approach, who performs the engineering work, who authorizes the resulting executable state, and whether that authorization decision is carried in the artifact that executes.",
      "2": "Research questions. For each question: the unit of analysis, the procedure applied, the boundary claimed, the evidence artifact, the rung reached on the evidence ladder of Sect. 3.2, and what the question does not establish.",
      "3": "The collaboration model by lifecycle activity. Three columns are kept apart: who holds authority, who performs the work, and what the machine determines or enforces.",
      "4": "The P0-P8 rule sets. For each phase: the number of numbered template registers, the number of distinct rule identifiers, the priors the phase declares, and the inspection operations its rule set names.",
      "5": "RQ2 boundary matrix. For each authority boundary: the stimulus applied, whether an attempt was made, whether a refusal was observed, whether the demonstration discriminates against removal of the guard, the rung reached, and what remains untested.",
      "6": "The mutation ledger. For each mutation: the exact edit applied, the demonstration suite it was applied to, the outcome at first delivery, the outcome after a negative demonstration was added, and what the result establishes.",
      "7": "Limitations. For each: the surface it bounds and what remains supported despite it.",
      "8": "Threat model. For each party the study names: what it is trusted for, what it is not trusted for or where trust is not established, and what it can do in this realization. Attacks excluded from the model follow the table.",
    }

    def tabc(num):
        return "\n**Table %s** %s\n\n%s\n" % (num, CAPTION[num], T[num][1])

    # Exhibits are placed after the paragraph carrying their first mention. Anchoring on the
    # reference itself rather than on surrounding prose means the draft can be reworded freely;
    # only removing a "Fig. N" or "Table N" mention altogether will break the build.
    marks = []
    for n in range(1, 15):
        m = re.search(r"\bFig\. %d\b" % n, s)
        if not m:
            sys.exit("build_manuscript: Fig. %d is never referenced in the draft" % n)
        marks.append((s.index("\n\n", m.end()) + 1, n, (site_fig if site else fig)(n)))
    for n in range(1, 9):
        m = re.search(r"\bTable %d\b" % n, s)
        if not m:
            sys.exit("build_manuscript: Table %d is never referenced in the draft" % n)
        marks.append((s.index("\n\n", m.end()) + 1, n, tabc(str(n))))

    for pos, _, block in sorted(marks, key=lambda t: (-t[0], -t[1])):
        s = s[:pos] + block + s[pos:]

    if site:
        write_site(s)
        return

    io.open(OUT_MD, "w", encoding="utf-8").write(s)
    subprocess.run(["../utils/convert_docx_md.sh", OUT_MD, "ase"], check=True)

    figs = sorted(int(x) for x in re.findall(r"!\[\*\*Fig\. (\d+)", s))
    tabs = re.findall(r"\*\*Table (\d+[ab]?)\*\*", s)
    print("%s — %d words, %d figures %s, %d tables %s"
          % (OUT_MD, len(s.split()), len(figs), figs, len(tabs), tabs))
    if figs != list(range(1, 15)): sys.exit("FIGURE SET INCOMPLETE")

if __name__ == "__main__":
    main()
