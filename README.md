# DSA Practice Tracker

A Python + SQL command-line tool I built to track my own data structures & algorithms practice; logging problems by topic and difficulty, flagging what needs review, and surfacing priorities directly from a real SQLite database.

Started as a JSON-based CLI tool, then rebuilt to run on SQLite as I learned SQL. Every core feature (search, sort, priority ranking, review tracking) now runs through real SQL queries instead of in-memory Python logic. A static HTML/CSS mockup of a future web version is also in progress.

## Features

- **SQLite-backed storage** — all problems are stored in a real relational database (`tracker.db`), queried and updated through parameterized SQL
- **Interactive CLI menu** — add, search, sort, edit, mark reviewed, and delete problems without touching the code
- **SQL-based sorting** — sort by difficulty (custom severity order via `CASE WHEN`, not alphabetical) or by name
- **Review tracking** — flags problems not reviewed in the last 7 days, and lets you mark a problem reviewed (updates `last_reviewed` to today)
- **Partial, case-insensitive search** — find problems by topic or name substring using `LIKE`
- **Duplicate-name handling** — since problem names aren't guaranteed unique (e.g. "BFS" under Graph vs. Binary Tree), editing or deleting prompts for disambiguation by ID when multiple matches exist
- **Top-3-hardest view** — surfaces the 3 hardest problems via `ORDER BY` + `LIMIT`
- **Formatted table output** — clean, aligned display via the `tabulate` library
- **Legacy JSON version preserved** — the original JSON-based implementation is archived in `legacy_json_version.py` for reference

## How to run

```bash
pip install tabulate
python3 dsa_tracker.py
```

## What I learned building this

This project started as a way to reinforce Python fundamentals, then became my introduction to SQL — every SQL concept (parameterized queries, `LIKE`, `CASE WHEN`, `UPDATE`/`DELETE`, `JOIN`, `GROUP BY`) was learned and applied here as I went, including real bugs found and fixed along the way (a case-sensitivity mismatch in name matching, a circular import between the CLI and database modules, and a design problem around non-unique problem names). It's a living project — the next phase is adding a real web frontend (HTML/CSS/JS + Flask) on top of the existing SQL backend.

## Tech stack

Python 3, SQLite (`sqlite3`), `tabulate`, HTML/CSS (in progress)