# Plan Directory Rules

This directory is for local developer planning. There is no plan skill, so the
plan template, filename convention (`YYYYMMDD_topic-plan.md`), and git-tracking
rules live in `README.md` — read it before writing a plan.

- Keep the directory itself in the repository as a template.
- Do not commit individual plan files by default.
- Treat files in this directory as local working notes, not product source code.
- Do not treat old local plans as current truth when they conflict with user instructions, code, or newer decisions.
- Durable technical decisions go in `docs/decisions/` (via the `decision-record` skill), not in plan files.
- Commit a plan file only when the user explicitly wants it preserved as shared project documentation.
