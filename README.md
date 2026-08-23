# OmniBachi

**The home of Protocol-Governed Computing (PGC).** → **[omnibachi.org](https://omnibachi.org)**

Protocol-Governed Computing (PGC) is an open-source architecture for building trustworthy
software, AI agents, autonomous systems, and digital ecosystems through explicit protocol,
governance, and verifiable execution. Rather than embedding behavior in opaque code paths or
runtime discretion, PGC treats **governance, authority, intent, workflow, capability, and
execution** as first-class declarative artifacts that can be authored, compiled, validated, and
executed deterministically.

> **PGC and PGS.** Work predating the PGC name describes the same substrate as **Protocol-Governed
> Systems (PGS)**. The name changed; the architecture did not. PGS also names the implementation in
> which the architecture was first developed and validated, now **frozen** and retained for lineage.
> Papers and pages still carrying the PGS name are current unless marked otherwise.

This repository builds the **OmniBachi** website — the primary knowledge hub for the PGC
ecosystem, bringing together the conceptual foundations, reference architecture, technical
specifications, implementation guidance, research publications, and practical examples that
demonstrate how complex systems can be governed by protocol rather than convention.

## Explore

| Section | What's there |
|---|---|
| **[Blog](https://omnibachi.org/blog/)** | Essays, architectural insights, project updates, and design explorations. |
| **[Papers](https://omnibachi.org/papers/)** | Technical publications, including DOI-backed reference papers. |
| **[Book](https://omnibachi.org/book/)** | The practitioner's guide to protocol-governed architecture. |
| **[Learn](https://omnibachi.org/learn/)** | Tutorials, walkthroughs, examples, and hands-on resources. |
| **[Use Cases](https://omnibachi.org/use-cases/)** | Where PGC applies: agentic AI, compliance, autonomous software, and more. |
| **[About](https://omnibachi.org/about/)** | What PGC is, and how this site relates to it. |

**This site is the knowledge hub, not the implementation.** The reference implementation of PGC is
the multi-repo ecosystem — governance surface, compiler, assembler, runtime, transport, inspection,
and the transformation lifecycle — at
**[github.com/protocol-governed-computing](https://github.com/protocol-governed-computing)**. The
earlier PGS implementation at [github.com/bachipeachy](https://github.com/bachipeachy) is frozen and
kept for lineage.

## Comments & discussion

Every article page — blog posts, papers, working papers, book chapters, tutorials, use cases and
the about pages — carries a comment thread via [giscus](https://giscus.app), backed by this
repository's GitHub Discussions. Sign in with GitHub to join the conversation. Section index pages
deliberately have none: a discussion belongs against something specific.

---

## Developing this site

The site is built with [Hugo](https://gohugo.io) (extended) + the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme and deploys to GitHub Pages via
GitHub Actions.

**This repository is the source of truth for everything published here.** Markdown in `content/`
is edited directly — there is no upstream copy and no generation step. Edit, commit, push to
`main`, and GitHub Actions builds and deploys. Nothing else is involved.

```bash
git clone --recurse-submodules <this-repo>     # PaperMod is a submodule
make preview    # hugo server → http://localhost:1313 (live reload)
make build      # production build into public/
```

- **`content/`** — every page, with its Hugo front matter. The only place text is edited.
- **`static/`** — images, figures, paper PDFs, favicons, `CNAME`.
- **`hugo.toml`** — site config (menus, theme params, giscus).
- **`layouts/`** — PaperMod overrides (book ToC, blog order, series box, comments, styles).
- **`.github/workflows/deploy.yml`** — build + deploy to Pages.
- **`GO-LIVE.md`** — full setup / deployment checklist.
- **`parkinglot/`** — work in progress: draft papers and unpublished posts, with any images they
  need. Gitignored and outside `content/`, so nothing here is committed and Hugo never sees it.
  Move a document into `content/` (and its images into `static/`) when it is ready to publish.

### Adding a blog post

Copy an existing post in `content/blog/` and edit its front matter. Two fields carry meaning:

- **`date`** — the real publication date. The blog index is sorted newest first by date.
- **`weight`** — the permanent series number, ascending from `#01`. It sets the order of the
  series box at the foot of every post, and never changes once assigned. The cover image is
  `static/assets/blog_NN.jpg`, matching that number.

So the index counts down (`#20`, `#19`, `#18` …) while the series reads up. A post that is not
ready lives in `parkinglot/` with its cover image, not in `content/`.

## License & contact

Licensed under the **Apache License 2.0** — see [LICENSE](LICENSE) and [NOTICE](NOTICE).
© 2026 Bhash Ganti (aka Bachi). Part of the open-source PGC ecosystem.
Questions or collaboration: [bachipeachy@gmail.com](mailto:bachipeachy@gmail.com).
