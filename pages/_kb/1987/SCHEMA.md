---
schema: "0.1"
coverage: listed
---

# SCHEMA — 1987

> The 1987 knowledge base — history, politics, science, culture, society, and people of the year 1987. Merged from bamr87/1987 with its history (2026-10).

## Structure

| entry | kind | purpose | rules |
|---|---|---|---|
| `history-politics/` | dir | History & Politics articles of 1987 |  |
| `science-technology/` | dir | Science & Technology articles of 1987 |  |
| `arts-culture/` | dir | Arts & Culture articles of 1987 |  |
| `society-economics/` | dir | Society & Economics articles of 1987 |  |
| `people/` | dir | People articles of 1987 |  |
| `index.md` | file | The 1987 home (/kb/1987/) — intro, category links, the curated Notable Events table, and a Dataview topic table |  |
| `timeline.md` | file | Hand-curated chronology of 1987 (/kb/1987/timeline/) — one row per event, linked to its article |  |

## Placement

- New article → `<category>/<slug>.md` from `_templates/kb-topic.md`, with `kb: "1987"` and `permalink: /kb/1987/<category>/<slug>/`.
- A new event worth a timeline row → add it to `timeline.md` and, if notable, to the home page's Notable Events table (both curated by hand).
