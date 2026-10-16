---
title: Knowledge bases
type: page
description: Standalone knowledge bases published by zer0-pages — each with its own home, categories, and timeline.
permalink: /kb/
aliases:
  - /kb/
---

# Knowledge bases

Each knowledge base here is its own subject, kept apart from the vault's docs, posts, notes and wiki: it has its own home page, category pages, timeline, and sidebar, and its articles link only within it. They share the site, the theme, the Obsidian bridge, and the graph.

```dataview
TABLE description AS "About"
FROM "_kb"
WHERE type = "kb"
SORT title ASC
```

## Size

```dataview
TABLE length(rows) AS "Articles"
FROM "_kb"
WHERE type = "topic"
GROUP BY kb AS KB
SORT KB ASC
```

## Adding to a knowledge base

- **An article:** copy `_templates/kb-topic.md` to `_kb/<name>/<category>/<slug>.md` and fill in its front matter. It needs `title`, `type: topic`, `kb`, `category`, `date`, `description`, and a `permalink` mirrored in `aliases`. The category page, the home page's topic table, and this page update themselves through Dataview. The timeline and the "Notable Events" table are curated by hand.
- **A new knowledge base:** add `_kb/<name>/` with an `index.md` (`type: kb`) and its category folders, a `kb-<name>.yml` sidebar under `_data/navigation/`, and a matching `_kb/<name>` entry under `defaults:` in `_config.yml`.
