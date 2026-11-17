# Plan Directory Rules

Follow [docs writing guidance](../AGENTS.md) for status tables and Plan/Handoff ownership.

- Plans own the shared goal, detailed specification, file ownership, dependencies, acceptance criteria, progress, verification, and lessons for long-running or multi-agent work.
- Update the relevant existing Plan first. When a short task becomes long-running, move its details out of Handoff before continuing; leave only a summary and link there.
- Make the Plan sufficient for multiple agents to pursue the same objective without reconstructing the conversation.
- Lead with the current phase, completed/remaining scope, and next action. Keep every task, including completed/excluded items, in the status table with its owner, status, evidence, next action, and unblock condition where needed.
- The lead updates the existing rows after implementation, verification, review adjudication, integration, and commits. Combine sections/tables to fit the task; do not maintain duplicate status records.
- Summarize verification in compact tables: scope/commit, command, actual result, and artifact path/short hash. Distinguish Mock, real-model, Live, and external integration checks; mark unrun checks explicitly.
- Keep only decisions and failure summaries needed to resume or explain a verdict. Store raw logs/screenshots outside the Plan; avoid chronological journals, and state conclusions rather than only listing links. Preserve completed Plans.
- Keep Plans local by default. Multi-agent use does not require a commit. Follow user direction and `docs/.gitignore` when sharing is needed.
- Do not add per-task Plan links to root `AGENTS.md`; its Source of Truth directory link is sufficient. Locate active Plans through task instructions or local Handoff.
- Never link an untracked Plan from tracked documentation. Reference tracked shared Plans only when needed, not as a mandatory rotating root pointer.
- Record durable technical decisions in `docs/decisions/` via `decision-record`, and link them from the Plan.
- Use `YYYYMMDD_<slug>-plan.md` for plan filenames.
