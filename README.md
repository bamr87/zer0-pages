# zer0-pages

> Obsidian vault published as a Jekyll knowledge site via build-time bridge plugins; the second brain of zer0-mistakes.

[![CI](https://github.com/bamr87/zer0-pages/actions/workflows/ci.yml/badge.svg)](https://github.com/bamr87/zer0-pages/actions/workflows/ci.yml) [![License](https://img.shields.io/github/license/bamr87/zer0-pages)](LICENSE) [![Live site](https://img.shields.io/badge/live-bamr87.github.io%2Fzer0--pages-2ea44f)](https://bamr87.github.io/zer0-pages/)

## Overview

**Zero friction. Infinite possibilities.**

zer0-pages is an AI-powered knowledge site with a twist: the content is an [Obsidian](https://obsidian.md) vault, the librarian is [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian), and the publisher is [Jekyll](https://jekyllrb.com) running in GitHub Actions. You (or Claude, on your behalf) write plain Obsidian-native markdown — wikilinks, callouts, Dataview queries — and a set of custom build-time "bridge" plugins convert those constructs to HTML for GitHub Pages. The site's look and feel comes from the [zer0-mistakes](https://github.com/bamr87/zer0-mistakes) theme, consumed as the published `jekyll-theme-zer0` gem.

The vault is never polluted with Liquid templating. The published site never requires Obsidian. One body of content, two first-class consumers.

Beyond showcasing the theme, zer0-pages' declared purpose is to act as a **second brain for [zer0-mistakes](https://github.com/bamr87/zer0-mistakes)** — a place where research, decisions, and usage knowledge about the theme accumulate and can feed back into its development, rather than living only in this repo's own showcase content. See [pages/wiki/entities/zer0-mistakes.md](pages/wiki/entities/zer0-mistakes.md) for the current state of that relationship (and an open gap: the deep technical knowledge still lives only in the zer0-mistakes repo itself, not yet ingested here).

## Features

- Content is a plain Obsidian vault with wikilinks, callouts and Dataview queries
- Build-time bridge plugins convert Obsidian constructs to HTML for GitHub Pages
- Styled by the zer0-mistakes theme, consumed as the `jekyll-theme-zer0` gem
- claude-obsidian acts as the vault's librarian
- A graph view of how notes connect

## Architecture

```
             AUTHOR                      BUILD                      SERVE
  ┌──────────────────────┐   ┌─────────────────────────┐   ┌──────────────────┐
  │  claude-obsidian     │   │  GitHub Actions          │   │  GitHub Pages    │
  │  skills (engine)     │   │                          │   │                  │
  │   /wiki-ingest       │   │  Jekyll 4 + theme gem    │   │  bamr87.github   │
  │   /save              ├──▶│  (jekyll-theme-zer0)     ├──▶│  .io/zer0-pages/ │
  │   /autoresearch      │   │   + pages/_plugins/      │   │                  │
  │   /wiki-query        │   │     obsidian bridge:     │   │  static HTML,    │
  │          │           │   │     wikilinks → <a>      │   │  zer0-mistakes   │
  │          ▼           │   │     callouts  → alerts   │   │  theme + an      │
  │  pages/  (Obsidian   │   │     dataview  → tables   │   │  interactive     │
  │  vault = Jekyll src) │   │     graph → JSON index   │   │  vault graph     │
  └──────────────────────┘   └─────────────────────────┘   └──────────────────┘
```

- **`claude-obsidian/`** — git submodule; the content engine. Its skills read sources,
  synthesize knowledge, and file structured notes into the vault.
- **`pages/`** — the Obsidian vault *and* the Jekyll source. Three content collections
(`_docs/`, `_posts/`, `_notes/`), standalone knowledge bases under `_kb/` (see below), Maps of Content (`_moc/`), a growing `wiki/` knowledge base, plus the bridge plugins, the theme's data files (`_data/` — navigation, UI text, authors; theme gems can't ship these), and two local include overrides kept for site-specific reasons (see `.theme-overrides.yml`), not for theme bugs — both bugs they were originally cut for shipped fixed in v1.26.0. Everything else — layouts, includes, vendored Bootstrap 5 — comes from the `jekyll-theme-zer0` gem, which the Gemfile deliberately leaves unconstrained so the site tracks the latest theme (`Gemfile.lock` is what pins a build).
- **`.github/workflows/pages.yml`** — builds and deploys on every push to `main`.

## Quickstart

```bash
git clone --recurse-submodules https://github.com/bamr87/zer0-pages
```

1. **Browse and author**: open the `pages/` directory as a vault in Obsidian (install the
   Dataview community plugin so the MOC dashboards populate). Start at `_moc/Home.md`.
2. **Let Claude do the writing**: run Claude Code in the repo and use the
claude-obsidian skills — they are the primary authoring path. Drop a file in `pages/.raw/` and say "ingest it" (`/wiki-ingest`), or "save this" (`/save`), or "research X" (`/autoresearch`); ask questions with `/wiki-query`. Docs, posts, and notes all flow from the same engine.
3. **One-time setup**: in the repo on GitHub, go to Settings → Pages → Build and
deployment and set **Source: GitHub Actions**. Skipping this makes the first deploy fail with a `Get Pages site failed` 404.
4. **Publish**: push to `main`. GitHub Actions builds the site with Jekyll, the
`jekyll-theme-zer0` theme, and the Obsidian bridge plugins, and deploys it to [bamr87.github.io/zer0-pages](https://bamr87.github.io/zer0-pages/).

To build locally instead: `bundle install && bundle exec jekyll build` (Ruby 3.x recommended; CI uses 3.3). Unit tests run on plain system Ruby: `ruby -Ipages/_plugins tests/test_obsidian_bridge.rb` (bridge) and `ruby -Ipages/_plugins tests/test_graph_index.rb` (graph index).

## Knowledge bases

zer0-pages also publishes standalone knowledge bases at [/kb/](https://bamr87.github.io/zer0-pages/kb/), each about one subject and kept apart from the vault's own docs, posts and wiki: **[1987](https://bamr87.github.io/zer0-pages/kb/1987/)** (26 articles, formerly [bamr87/1987](https://github.com/bamr87/1987)) and **[2005](https://bamr87.github.io/zer0-pages/kb/2005/)** (75 articles, formerly [year-of-ai/2005](https://github.com/year-of-ai/2005)). Each has a home page with a curated table of notable events, a timeline, category pages, and its own sidebar. Both were merged with their git history. Add an article from `pages/_templates/kb-topic.md`; [CLAUDE.md](CLAUDE.md#knowledge-bases-pages_kb) has the rules.

## Graph view

The published site includes an interactive Obsidian-style graph of the whole vault at [/docs/obsidian/graph/](https://bamr87.github.io/zer0-pages/docs/obsidian/graph/). At build time, a plugin (`pages/_plugins/obsidian_graph_index.rb`) reuses the bridge's wikilink parser to emit `/assets/data/wiki-index.json`; in the browser, the theme's Cytoscape-based UI renders every doc/post/note as a node, every wikilink as an edge, colored by collection — dead links show up as red "broken" nodes, which makes the graph double as a link-rot detector. Note pages also get a backlinks panel driven by the same JSON index.

## Writing content

Everything in `pages/` follows one rule: **Obsidian-native markdown, no Liquid.** Use
wikilinks (`[[_docs/jekyll/index|Jekyll docs]]`), callouts (`> [!tip] Title`), and the
supported Dataview grammar for listings. Frontmatter carries `title`, `type`, `description`, and a `permalink`/`aliases` pair. The full contract, including the exact Dataview grammar the bridge supports, lives in [CLAUDE.md](CLAUDE.md); vault-level conventions live in [pages/CLAUDE.md](pages/CLAUDE.md).

## Preview images

AI banner images come from the [zer0-image-generator](https://github.com/bamr87/zer0-image-generator) gem (a zer0-mistakes companion, installed via the Gemfile):

```bash
bundle exec jekyll preview-images --list-missing   # what needs a banner?
bundle exec jekyll preview-images                  # generate + wire `preview:` front matter
```

Images land in `pages/assets/images/previews/` (the gem honors `source: pages`); config lives under `preview_images:` in `_config.yml`. Rendering uses OpenAI by default (`OPENAI_API_KEY`); `--provider local` needs no keys.

## Learn more

- [PRD.md](PRD.md) — an early, aspirational product-requirements document; it describes
a Django+React CMS vision that predates and does not match the vault+bridge system described above (see [pages/wiki/sources/zer0-pages-prd.md](pages/wiki/sources/zer0-pages-prd.md) for the reality check).
- [zer0-mistakes](https://github.com/bamr87/zer0-mistakes) — the Jekyll theme behind
the site's UI, published as the `jekyll-theme-zer0` gem, and the project this repo exists to be a second brain for (see [pages/wiki/entities/zer0-mistakes.md](pages/wiki/entities/zer0-mistakes.md)). Working on the theme itself? See the "local theme development" tip in [CLAUDE.md](CLAUDE.md).
- [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) — the upstream
  knowledge-engine project (Karpathy's LLM Wiki pattern).

## Development

```bash
bundle install && bundle exec jekyll build
ruby -Ipages/_plugins tests/test_obsidian_bridge.rb
```

Full commands, conventions and gotchas for humans and AI agents live in [CLAUDE.md](CLAUDE.md).

## Contributing

Contributions are welcome via pull request. Use [Conventional Commits](https://www.conventionalcommits.org/) and keep the CI checks green. The fleet-wide workflow is described in the hub's [CONTRIBUTING.md](https://github.com/bamr87/bamr87/blob/main/CONTRIBUTING.md). AI agents should start with [CLAUDE.md](CLAUDE.md).

## Changelog

Notable changes are recorded in [CHANGELOG.md](CHANGELOG.md); the full record is in the [commit history](https://github.com/bamr87/zer0-pages/commits/main).

## License

Released under the [MIT License](LICENSE).

---

<!-- bamr87-portfolio-footer -->
Part of the [bamr87 portfolio](https://github.com/bamr87) — browse every project on [Amr's GitHub profile](https://github.com/bamr87).
