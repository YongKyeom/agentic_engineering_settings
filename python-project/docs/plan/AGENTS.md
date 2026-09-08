# Plan Directory Rules

Follow [docs writing guidance](../AGENTS.md) for status tables and Plan/Handoff ownership.

- Plans own the shared goal, detailed specification, file ownership, dependencies, acceptance criteria, progress, verification, and lessons for long-running or multi-agent work.
- Update the relevant existing Plan first. When a short task becomes long-running, move its details out of Handoff before continuing; leave only a summary and link there.
- Make the Plan sufficient for multiple agents to pursue the same objective without reconstructing the conversation.
- Update the current status table in place. Keep previous results, failures, and accepted/rejected approaches in separate history sections. Preserve completed Plans.
- Keep Plans local by default. Multi-agent use does not require a commit. Follow user direction and `docs/.gitignore` when sharing is needed.
- Do not add per-task Plan links to root `AGENTS.md`; its Source of Truth directory link is sufficient. Locate active Plans through task instructions or local Handoff.
- Never link an untracked Plan from tracked documentation. Reference tracked shared Plans only when needed, not as a mandatory rotating root pointer.
- Record durable technical decisions in `docs/decisions/` via `decision-record`, and link them from the Plan.
- Use `YYYYMMDD_<slug>-plan.md` for plan filenames.