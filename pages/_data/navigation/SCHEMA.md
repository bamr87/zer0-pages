---
schema: "0.1"
coverage: listed
---

# SCHEMA — navigation

> One YAML menu per navigation surface, consumed by the theme gem's navigation includes.

## Structure

| entry | kind | purpose | rules |
|---|---|---|---|
| `docs.yml` | file | Docs sidebar tree — used by pages with `sidebar: nav: docs` frontmatter | |
| `home.yml` | file | Header quick-access icon links (top-level title/icon/url entries) | |
| `kb-1987.yml` | file | Sidebar for the 1987 knowledge base — set on every `_kb/1987` page by `_config.yml` defaults | |
| `kb-2005.yml` | file | Sidebar for the 2005 knowledge base — set on every `_kb/2005` page by `_config.yml` defaults | |
| `main.yml` | file | Primary navbar with dropdown children — every URL is a real permalink | |
| `posts.yml` | file | News/posts section navigation — sections mirror the _posts/ category folders | |

## Placement

- New surface → `<surface>.yml` here, referenced from page frontmatter via `sidebar: nav: <surface>`.
