# OmniBachi

**The home of Protocol-Governed Systems (PGS).** → **[omnibachi.org](https://omnibachi.org)**

Protocol-Governed Systems (PGS) is an open-source architecture for building trustworthy
software, AI agents, autonomous systems, and digital ecosystems through explicit protocol,
governance, and verifiable execution. Rather than embedding behavior in opaque code paths or
runtime discretion, PGS treats **governance, authority, intent, workflow, capability, and
execution** as first-class declarative artifacts that can be authored, compiled, validated, and
executed deterministically.

This repository builds the **OmniBachi** website — the primary knowledge hub for the PGS
ecosystem, bringing together the conceptual foundations, reference architecture, technical
specifications, implementation guidance, research publications, and practical examples that
demonstrate how complex systems can be governed by protocol rather than convention.

## Explore

| Section | What's there |
|---|---|
| **[Blog](https://omnibachi.org/blog/)** | Essays, architectural insights, project updates, and design explorations. |
| **[Papers](https://omnibachi.org/papers/)** | Technical publications, including DOI-backed reference papers. |
| **[Book](https://omnibachi.org/book/)** | The practitioner's guide to Protocol-Governed Systems. |
| **[Learn](https://omnibachi.org/learn/)** | Tutorials, walkthroughs, examples, and hands-on resources. |
| **[Use Cases](https://omnibachi.org/use-cases/)** | Where PGS applies: agentic AI, compliance, autonomous software, and more. |
| **[About](https://omnibachi.org/about/)** | What PGS is, and OmniBachi as its reference implementation. |

**OmniBachi** is the reference implementation of PGS — organized as an open-source, multi-repo
ecosystem (compiler, runtime, governed capabilities, inspection tooling, and more). Browse the
projects at **[github.com/bachipeachy](https://github.com/bachipeachy)**.

## Comments & discussion

Each post supports comments via [giscus](https://giscus.app), backed by this repository's GitHub
Discussions — sign in with GitHub to join the conversation.

---

## Developing this site

The site is built with [Hugo](https://gohugo.io) (extended) + the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme and deploys to GitHub Pages via
GitHub Actions.

Content authoring is **single-sourced**: the canonical markdown lives in a separate `pgs_workspace`
repo; a one-way adapter (`scripts/ingest.py`) copies it here and adds Hugo front matter, so the
source is never mutated. CI builds from the **committed** `content/` + `static/` (it does not run
the adapter).

```bash
git clone --recurse-submodules <this-repo>     # PaperMod is a submodule
make ingest     # pull canonical markdown → content/ + static/   (needs pgs_workspace alongside)
make preview    # hugo server → http://localhost:1313 (live reload)
make build      # production build into public/
```

- **`hugo.toml`** — site config (menus, theme params, giscus).
- **`ingest.config.yaml`** — content manifest (source paths, titles, slugs, order).
- **`scripts/ingest.py`** — the markdown → Hugo adapter.
- **`layouts/`** — PaperMod overrides (book ToC, series box, comments, styles).
- **`.github/workflows/deploy.yml`** — build + deploy to Pages.
- **`GO-LIVE.md`** — full setup / deployment checklist.

## License & contact

Licensed under the **Apache License 2.0** — see [LICENSE](LICENSE) and [NOTICE](NOTICE).
© 2026 Bhash Ganti (aka Bachi). Part of the open-source PGS ecosystem.
Questions or collaboration: [bachipeachy@gmail.com](mailto:bachipeachy@gmail.com).
