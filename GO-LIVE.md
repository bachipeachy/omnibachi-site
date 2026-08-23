# Go-Live Checklist — omnibachi.org

Sequential. Everything above the line is built; this is the part that needs you + GitHub.

## 0. Pre-flight (local)
- [ ] `make preview` → eyeball http://localhost:1313 one last time
- [ ] Add the 5 missing covers `static/assets/blog_01..05.<ext>` (optional)
- [ ] `git add -A && git commit -m "Initial omnibachi.org site"` (you do the commit)

## 1. Create the repo (public)
- [ ] New **public** GitHub repo `bachipeachy/omnibachi-site`
- [ ] `git remote add origin git@github.com:bachipeachy/omnibachi-site.git`
- [ ] `git push -u origin main`

## 2. Enable Pages (GitHub Actions)
- [ ] Repo **Settings → Pages → Build and deployment → Source = GitHub Actions**
- [ ] Watch the **Actions** tab — the `Deploy Hugo site` workflow should go green
- [ ] Verify the staging build at `https://bachipeachy.github.io/omnibachi-site/`
      (nav, a blog post, the book ToC, a paper figure, dark/light, search)

## 3. Comments (giscus)
- [ ] Settings → **General → Features → ✓ Discussions**
- [ ] Discussions tab → create a **Comments** category (Announcement format is fine)
- [ ] At <https://giscus.app>: enter `bachipeachy/omnibachi-site`, pick the Comments category,
      `pathname` mapping → copy `data-repo-id` and `data-category-id`
- [ ] Put them in `hugo.toml [params.giscus]` (`repoId`, `categoryId`) → commit + push
- [ ] Confirm a comment box appears at the bottom of an article page (every page except the
      section indexes, the home page and search)

## 4. Custom domain (DNS cutover)
- [ ] Namecheap → confirm **Namecheap BasicDNS** (not WordPress.com nameservers)
- [ ] Advanced DNS → apex `@` **A records** → `185.199.108.153`, `185.199.109.153`,
      `185.199.110.153`, `185.199.111.153`
- [ ] `www` → **CNAME** → `bachipeachy.github.io.`
- [ ] Remove any old WordPress.com / parking / URL-redirect records that conflict
- [ ] GitHub **Settings → Pages → Custom domain** = `omnibachi.org` → Save (GitHub adds CNAME)
- [ ] Wait for DNS check ✓, then enable **Enforce HTTPS** (free cert provisions automatically)
- [ ] Load `https://omnibachi.org` — confirm it serves the new site

## 5. After go-live
- [ ] Retire the WordPress.com subscription
- [ ] Mint **Zenodo** DOIs per paper → add the DOI line to that paper's page in `content/papers/`
- [ ] Retrofit real Medium publish dates into `content/blog/*.md` (`date:` in the front matter)
- [ ] Decide whether `#21` (in `parkinglot/`, with its cover) gets published here

## Daily authoring loop (after go-live)
```bash
# edit content/ directly — this repo is the source of truth
make preview                                  # test at localhost:1313
git add -A && git commit -m "update" && git push   # → live, fully replaced
```

## Rollback
- Revert the offending commit and push — the Action redeploys the previous state.
- DNS issues: lower TTL beforehand; A/CNAME changes propagate in minutes–hours.
