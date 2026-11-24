# Plan Directory Rules

Follow [docs writing guidance](../AGENTS.md) for status tables and Plan/Handoff ownership.

- Plans own the shared goal, detailed specification, file ownership, dependencies, acceptance criteria, progress, verification, and lessons for long-running or multi-agent work.
- Update the relevant existing Plan first. When a short task becomes long-running, move its details out of Handoff before continuing; leave only a summary and link there.
- Make the Plan sufficient for multiple agents to pursue the same objective without reconstructing the conversation.
- Put one status table at the top. Include every task, including completed and excluded items, with its owner, status, and next action or unblock condition. Link to the relevant section below when an item needs more detail.
- Put the user confirmation table immediately below the status table. Keep it there even when no decision is pending.
- The lead updates the top table after implementation, verification, review, integration, or commits. Keep purpose, decisions, and evidence in the linked sections below. Add a diagram where it clarifies a flow or dependency.
- Summarize verification in compact tables: scope/commit, command, actual result, and artifact path/short hash. Distinguish Mock, real-model, Live, and external integration checks; mark unrun checks explicitly.
- Keep only decisions and failure summaries needed to resume or explain a verdict. Store raw logs/screenshots outside the Plan; avoid chronological journals, and state conclusions rather than only listing links. Preserve completed Plans.
- Keep Plans local by default. Multi-agent use does not require a commit. Follow user direction and `docs/.gitignore` when sharing is needed.
- Do not add per-task Plan links to root `AGENTS.md`; its Source of Truth directory link is sufficient. Locate active Plans through task instructions or local Handoff.
- Never link an untracked Plan from tracked documentation. Reference tracked shared Plans only when needed, not as a mandatory rotating root pointer.
- Record durable technical decisions in `docs/decisions/` via `decision-record`, and link them from the Plan.
- Use `YYYYMMDD_<slug>-plan.md` for plan filenames.
