---
schema: "0.1"
coverage: listed
---

# SCHEMA — 2005

> The 2005 knowledge base — history, politics, science, culture, society, and people of the year 2005. Merged from year-of-ai/2005 with its history (2026-10); each article records its old year-of-ai.github.io address as `legacy_url`.

## Structure

| entry | kind | purpose | rules |
|---|---|---|---|
| `history-politics/` | dir | History & Politics articles of 2005 |  |
| `science-technology/` | dir | Science & Technology articles of 2005 |  |
| `arts-culture/` | dir | Arts & Culture articles of 2005 |  |
| `society-economics/` | dir | Society & Economics articles of 2005 |  |
| `people/` | dir | People articles of 2005 |  |
| `index.md` | file | The 2005 home (/kb/2005/) — intro, category links, the curated Notable Events table, and a Dataview topic table |  |
| `timeline.md` | file | Hand-curated chronology of 2005 (/kb/2005/timeline/) — one row per event, linked to its article |  |

## Placement

- New article → `<category>/<slug>.md` from `_templates/kb-topic.md`, with `kb: "2005"` and `permalink: /kb/2005/<category>/<slug>/`.
- A new event worth a timeline row → add it to `timeline.md` and, if notable, to the home page's Notable Events table (both curated by hand).
