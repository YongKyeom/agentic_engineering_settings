# Handoff Directory Rules

Follow [docs writing guidance](../AGENTS.md) for status format and Plan/Handoff ownership.

- Update the existing Handoff during ordinary work. Short tasks need only their status, result, and next action here.
- Plans own long-running work. Keep only the Plan link, current stage, blockers, and next action in Handoff.
- Move detailed specifications, ownership, verification logs, and lessons into the relevant Plan; do not duplicate a long-running work log here.
- Keep the current summary short, using tables or checklists. Separate historical handoff material from current status.
- Create a separate Handoff or perform an explicit transfer only when the user requests it. Apply the `handoff` skill to that requested transfer; context length alone is not a creation trigger.
- Keep local notes untracked. Preserve the tracking policy of existing shared documents; follow user direction for new shared artifacts.
- Use `YYYYMMDD_<topic>.md` for handoff filenames.
- Durable technical decisions belong in `docs/decisions/` (via the `decision-record` skill), not in handoff files.
