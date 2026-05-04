# Global Codex Operating Rules

## RTK Usage

- Shell commands should be written with an explicit `rtk` prefix whenever possible when RTK is available.
- Do not rely on PreToolUse command rewriting for RTK adoption. Some Codex hook runners reject `updatedInput`, so commands should be RTK-native before execution.
- Prefer RTK-native forms for common commands:
  - `rtk git status`
  - `rtk git diff`
  - `rtk ls`
  - `rtk find . -name "*.py"`
  - `rtk grep "pattern" path`
  - `rtk pytest -q`
  - `rtk ruff check .`
- If the exact raw command output is required, use `rtk proxy <command>` instead of bypassing RTK entirely.
- If an RTK wrapper changes behavior or hides information needed for the task, rerun with `rtk proxy` and state why.

### Skill And Hook Interaction With RTK

- Skills are allowed to suggest shell commands, but Codex should adapt those commands to RTK-prefixed forms before execution.
- Do not patch every installed skill only to add RTK prefixes. Prefer this global rule plus targeted skill edits only when a specific skill repeatedly emits unsuitable commands.
- If a PreToolUse hook fails with `unsupported updatedInput`, treat it as a hook schema compatibility problem, not a skill failure.
- For Codex, fail-safe operation is preferred: explicit RTK commands are safer than automatic hook rewriting.

## Agentic Engineering

- Prefer the simplest workflow that can solve the task. Add agentic complexity only when it improves quality, speed, or context control.
- The main agent owns task framing, source-of-truth selection, integration, final decisions, and final verification.
- Treat sub-agent output as evidence, not authority. Do not blindly accept sub-agent findings or patches.
- Use sub-agents when independent research, codebase exploration, verification, or review can run in parallel and materially improve the result.
- Do not use sub-agents for small tasks, tightly coupled edits, sequential blockers, or work that would create duplicate effort or merge conflicts.
- For non-trivial coding work, consider whether a read-only explorer, bounded worker, or independent reviewer would reduce risk before proceeding.

### Sub-Agent Delegation Contract

Every delegated task should specify:

- Objective.
- Scope and files to inspect.
- Files allowed to edit, if any.
- Source-of-truth and priority order.
- Constraints and forbidden changes.
- Expected output format.
- Verification criteria.

### Parallel Work Rules

- Parallelize only independent tasks.
- Avoid overlapping write scopes.
- For coding work, prefer disjoint file ownership.
- For review work, ask for findings with evidence rather than broad rewrites.
- The main agent must integrate, resolve conflicts, and verify the final state.

### Review Discipline

- Classify sub-agent feedback as accepted, deferred, or rejected.
- Reject feedback that conflicts with user instructions, source-of-truth, verified data, or local project rules.
- Record important rejected feedback when the reason affects future work.
- When quality matters, separate producer and reviewer roles.

### Context Management

- Keep noisy exploration, long logs, broad searches, and large-file inspection out of the main context when a sub-agent can summarize them.
- Ask sub-agents for concise findings with file paths, line references, confidence, and residual risks.
- For long-running work, preserve decisions, assumptions, open risks, and next actions in durable project documents.
- Use `handoff` before switching threads or when the context is too large to reliably continue.

### Verification Loop

- After integrating work, run the narrowest useful validation.
- For code, run targeted tests, linters, type checks, or smoke tests before broader validation.
- For documents, render the artifact and visually inspect affected pages before calling the work done.
- Do not mark work complete just because a sub-agent or tool reported success.

### Quality-Critical Artifacts

- For papers, theses, reports, presentations, and user-facing documents, a cycle is not complete until the artifact is rendered, visually checked, independently reviewed when useful, and patched if needed.
- Old PASS judgments become stale after new user feedback or major rendering changes. Re-evaluate against the latest artifact.
- Keep generated notes, review logs, and source assets separate from final user-facing output.

## Related Skills

- `handoff`: Use when context is long, work must continue in a new thread, or current state must be preserved.
- `requirements-clarity`: Use before implementation when scope, constraints, or completion criteria are unclear.
- `qa-test-planner`: Use when code, experiments, or document workflows need explicit verification plans.
- `skill-judge`: Use when reviewing or modifying installed skills.
- `agent-md-refactor`: Use when `AGENTS.md`, `CLAUDE.md`, or long instruction files need progressive disclosure.
- `humanizer`: Use when prose needs to remove AI-like writing, translationese, or unnatural phrasing.
- `writing-clearly-and-concisely`: Use when producing or editing prose that humans will read.
- `lesson-learned`: Use after repeated mistakes or significant debugging to extract reusable engineering rules.

### Diagram Skills

- `c4-architecture`: Use for software system architecture, C4 context/container/component/deployment diagrams, and architecture documentation.
- `mermaid-diagrams`: Use for software/process diagrams such as flowcharts, sequence diagrams, ERDs, state diagrams, and lightweight technical documentation diagrams.
- `excalidraw`: Use for rough sketches, planning diagrams, and editable concept sketches.
- Do not treat these diagram skills as the default solution for research-paper or thesis figures.
- For publication-quality research figures, first define the scientific message, data or concepts to show, visual encoding, caption role, and target document layout. Then create a controlled SVG/PDF/PNG asset and verify it inside the rendered document.

## Project Instructions

- Repository-local `AGENTS.md` files may add stricter rules for a project.
- If project instructions conflict with these global rules, follow the project instructions unless they would reintroduce broken hook behavior.
