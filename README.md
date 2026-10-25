# X Signals Data Drop

This repository contains daily X (Twitter) signals about card packs and digital collectibles, written by a marketing research assistant and read by automated Claude Code pipelines.

## Structure

```
.
├── signals/
│   ├── latest.json          # Most recent signals (overwritten daily)
│   └── archive/             # Historical snapshots (YYYY-MM-DD.json)
├── schema/
│   └── signals.schema.json  # JSON Schema (draft 2020-12) defining the data format
└── scripts/
    └── validate.py          # Validation script for CI
```

## Schema

The signals file follows a strict JSON Schema with the following fields:

- **generated_at** (string): ISO 8601 timestamp with timezone offset
- **date** (string): YYYY-MM-DD format in Europe/Madrid timezone
- **status** (enum): `"ok"` | `"quiet"` | `"placeholder"`
- **window_hours** (integer): Number of hours covered in this report
- **summary** (string): Executive summary of the day's signals
- **top_posts** (array): Most significant posts from X
  - url, author_handle, text, created_at, likes, reposts, replies, quotes (optional), topic, why_it_matters
- **competitor_news** (array): News about competitors
  - project, headline, url, date
- **solflare_mentions** (array): Mentions of Solflare
  - url, author_handle, text, sentiment (positive|neutral|negative), likes
- **new_creators** (array): New creators to watch
  - handle, url, followers, segment, crypto_friendly (yes|no|unknown), reason
- **post_ideas** (array): Suggested post ideas
  - idea, draft_copy, needs_legal_check (boolean)
- **sources_note** (string): Note about data sources

### Data Integrity

All engagement counts (likes, reposts, replies, quotes, followers) come directly from the X API and are never estimated. Values are integers or `null` when unknown.

## Update Schedule

`signals/latest.json` is overwritten daily around **10:00 Europe/Madrid** time. Each day's signals are archived to `signals/archive/YYYY-MM-DD.json` before being overwritten.

## Validation

All signals files are validated against the schema on every push via GitHub Actions. To validate locally:

```bash
pip install -r requirements.txt
python scripts/validate.py
```

## Usage

This is a data drop repository with no application code. Consumer pipelines should read `signals/latest.json` for the most recent signals or browse `signals/archive/` for historical data.
