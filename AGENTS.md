# Global AI Agent Operating Rules

## RTK Usage

- Shell commands should be written with an explicit `rtk` prefix whenever possible when RTK is available.
- Write RTK-native commands rather than relying on automatic command rewriting.
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

- Skills may suggest shell commands. Adapt suggested commands to RTK-prefixed forms before execution.
- Do not patch every installed skill only to add RTK prefixes. Prefer this global rule plus targeted skill edits only when a specific skill repeatedly emits unsuitable commands.

## Herdr Terminal Context

- Before Herdr terminal work, inspect `HERDR_ENV` in the command execution environment. Only `HERDR_ENV=1` identifies this agent as running inside Herdr; an installed binary, running server, or terminal title does not.
- For a user-requested Herdr pane, tab, workspace, or agent operation inside Herdr, read `${CODEX_HOME:-$HOME/.codex}/HERDR.md`. This is the unmodified official Markdown exported by the installed CLI with `rtk proxy herdr --skill`. Read it once per task; regenerate it after upgrading Herdr. Use the installed CLI's help for current syntax.
- Outside Herdr, continue ordinary work with the available shell tools. Installation, configuration, and `--skill` export are allowed there; do not inspect or control another Herdr session from outside a managed pane.
- In Herdr, prefer the caller's context and explicit IDs, preserve the user's focus, and follow the official skill's task-selection and coordination rules. Being inside Herdr alone does not authorize pane creation, delegation, input to another agent, or session shutdown.
- Follow RTK rules for Herdr commands too: use `rtk proxy herdr ...` to preserve CLI output. Do not auto-launch bare `herdr` to detect the environment.

## Agentic Engineering

- Prefer the simplest workflow that can solve the task. Add agentic complexity only when it improves quality, speed, or context control.
- The main agent owns task framing, source-of-truth selection, delegation, integration, final decisions, and final verification. Only the main agent may spawn or assign sub-agents; workers must not delegate further.
- Treat sub-agent output as evidence, not authority. Do not blindly accept sub-agent findings or patches.
- Use sub-agents when independent research, codebase exploration, verification, or review can run in parallel and materially improve the result.
- Do not use sub-agents for small tasks, tightly coupled edits, sequential blockers, or work that would create duplicate effort or merge conflicts.
- For non-trivial coding work, consider whether a read-only explorer, bounded worker, or independent reviewer would reduce risk before proceeding.

> For detailed delegation, parallelism, review, and verification rules, see the subsections below.

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
- Do not treat diagram skills as the default solution for research-paper or thesis figures.
- For publication-quality research figures, first define the scientific message, data or concepts to show, visual encoding, caption role, and target document layout. Then create a controlled SVG/PDF/PNG asset and verify it inside the rendered document.

## Code Development

Always follow `karpathy-guidelines` when writing or modifying any code.

## Skill Composition

- Use the current user request and applicable project rules to set authority, scope, completion criteria, and record ownership. Apply the relevant skills as the procedures for that work; retain required rules even when they overlap across instruction layers.
- Resolve action-changing gaps with `requirements-clarity` using existing context first. Use `deep-research` when claims need comparison across original sources, then carry the established evidence into implementation and writing.
- Apply `karpathy-guidelines` to code and `structured-prompt-template` to tagged/Jinja2 system prompts. Use `writing-clearly-and-concisely` for document structure and wording, and `humanizer` for the necessary voice and style pass while preserving the same facts and uncertainty.
- Use `code-review` for a local diff or hotfix and `packet-review` for a frozen functional acceptance bundle. Reuse valid evidence rather than repeating the same broad review; the lead owns disposition and final acceptance.
- Use `decision-record` for durable technical decisions, `handoff` for requested transfers and existing continuity notes, and `lesson-learned` for an evidence-based retrospective. Keep detailed long-running status in the Plan. New default filenames end in `-handoff.md` and `-plan.md` respectively; preserve explicit user filenames and existing names when updating.
- Apply `mermaid-diagrams` or `excalidraw` according to the chosen diagram format. Use `presentation-slidev` for Slidev deliverables and `dark-theme-pdf` for the specified theme; verify the resulting artifact in its destination.
- Use `agent-md-refactor` when reorganizing instructions and `skill-judge` when evaluating skill changes. Use `git-commit-helper` for commit-message preparation and review within the user's authorization. Invoking a skill does not authorize additional global changes, commits, publishing, or external messages.

## Related Skills

- `handoff`: Use for session context transfer and coordination documents with fellow developers or related departments. Put the overview, item summary, priorities, decisions needed, and related documents before item-level details; include diagrams for collaboration. Default file location: `docs/handoff/`. Prefer managed `handoff`; choose `source-command-handoff` only when that legacy skill is explicitly requested.
- `requirements-clarity`: Use before implementation when scope, constraints, or completion criteria are unclear.
- `skill-judge`: Use when reviewing or modifying installed skills.
- `agent-md-refactor`: Use when agent instruction files need progressive disclosure.
- `humanizer`: Use when prose needs to remove AI-like writing, translationese, or unnatural phrasing.
- `writing-clearly-and-concisely`: Use when producing or editing prose that humans will read.
- `lesson-learned`: Use after repeated mistakes or significant debugging to extract reusable engineering rules.
- `karpathy-guidelines`: Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria.
- `packet-review`: Use for an integrated read-only review of a frozen functional bundle against its active plan and code-quality contracts. For large packets, partition reviewers by bounded scope and consolidate one verdict; do not add a duplicate broad code review.
- `decision-record`: Use when a durable technical decision (architecture, module boundary, dependency, storage, API contract, hard-to-reverse direction) has just been made and should be recorded as an ADR in docs/decisions/.
- `structured-prompt-template`: Use when designing, generating, refactoring, or auditing provider-neutral tagged Jinja2 system prompts, Skill and Tool catalogs, priority rules, or output contracts.
- `presentation-slidev`: Use when authoring or iteratively refining presentations (thesis defense, side project decks, technical talks) delivered as PDF via Slidev.
- `code-review`: Use after making changes to review the diff for bugs, type safety, style, security, and maintainability.
- `deep-research`: Use when researching a topic that requires multiple sources, fact verification, and a structured report with citations.

### Diagram Skills

- `mermaid-diagrams`: Use for software/process diagrams such as flowcharts, sequence diagrams, ERDs, state diagrams, and lightweight technical documentation diagrams.
- `excalidraw`: Use for rough sketches, planning diagrams, and editable concept sketches.

## Project Instructions

- Repository-local instruction files may add stricter rules for a project.
- If project instructions conflict with these global rules, follow the project instructions.

@RTK.md
