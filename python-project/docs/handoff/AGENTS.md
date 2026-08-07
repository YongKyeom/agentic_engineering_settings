# Handoff Directory Rules

This directory holds local session handoff notes. The handoff package format is
owned by the `handoff` skill; `README.md` has the git-tracking rules and the
template.

- Keep the directory itself in the repository as a template.
- Do not commit individual handoff files unless the user explicitly wants one preserved as shared documentation.
- Use `YYYYMMDD_<topic>.md` for handoff filenames.
- Durable technical decisions belong in `docs/decisions/` (via the `decision-record` skill), not in handoff files.
