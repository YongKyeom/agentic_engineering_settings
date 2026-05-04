# Handoff Directory Rules

This directory is for local session handoff notes.

- Keep the directory itself in the repository as a template.
- Do not commit individual handoff files by default.
- Use this directory when work must continue in another local session, another tool, or another agent thread.
- Handoff is the smallest transfer package that lets another agent or the user continue the work.
- Prefer final-answer handoff when the work is complete and the diff is small.
- Write a file handoff when long-term tracking is needed or the next worker must continue from files.
- Use `YYYYMMDD_<topic>.md` for handoff filenames.
- Preserve status, work scope, changed files, key changes, decisions, validation, key files, cautions, risks, next actions, previous handoff reference, and local artifact handling.
- Be concrete enough that a new session can continue without rereading the whole history.
- Do not claim validation that was not run.
- Commit a handoff file only when the user explicitly wants it preserved as shared project documentation.
