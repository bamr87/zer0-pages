---
schema: "0.1"
coverage: listed
---

# SCHEMA — _kb

> The kb collection — standalone knowledge bases, one folder each, published under /kb/<name>/ and kept apart from docs, posts, notes and the wiki.

## Structure

| entry | kind | purpose | rules |
|---|---|---|---|
| `1987/` | dir | Knowledge base: the year 1987 |  |
| `2005/` | dir | Knowledge base: the year 2005 |  |
| `index.md` | file | /kb/ landing page — lists every knowledge base (Dataview over `type: kb`) |  |

## Placement

- New knowledge base → `<name>/` with `index.md` (`type: kb`), its category folders (each with a SCHEMA.md), a `_data/navigation/kb-<name>.yml` sidebar, and a `_kb/<name>` scope under `defaults:` in `_config.yml`.
- Articles never go here directly — always inside a knowledge base's category folder.
