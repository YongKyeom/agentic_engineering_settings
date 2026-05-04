# Python Project Agent Guide

This file is the root agent guide for Python projects copied from the `codex_settings` reference repository.
Keep this file short. Put detailed rules in `docs/*.md` so agents can load only the context they need.

## Project Defaults

- Use Korean for user-facing explanations unless the user requests another language.
- Keep technical identifiers, commands, paths, APIs, and error names in English.
- Follow repository-local instructions when they are stricter than this template.
- Do not introduce Python packaging files such as `pyproject.toml` or `uv.lock` unless the project actually needs Python packaging or scripts.
- Use `uv` only when the project already uses it or the user explicitly wants it.

## Documentation Map

- [Coding Convention](docs/coding-convention.md): Python style, docstrings, comments, typing, logging, validation.
- [Git Convention](docs/git-convention.md): Commit message format and commit hygiene.
- [Architecture](docs/architecture.md): Module boundaries, SRP, dependency direction, project layout.
- [Agentic Engineering](docs/agentic-engineering.md): Codex/Claude collaboration, sub-agent use, review discipline.
- [Plan Docs](docs/plan/README.md): PRDs, plans, task breakdowns, local execution notes.
- [Handoff Docs](docs/handoff/README.md): Session handoff format.
- [Decision Docs](docs/decisions/README.md): ADR and durable decision format.

## Core Workflow

- Identify the source of truth before editing.
- Make the smallest useful plan for non-trivial work.
- Keep edits scoped and avoid broad rewrites unless requested.
- Prefer targeted validation over broad validation during active iteration.
- Do not claim validation was done unless it was actually run.
- Preserve user changes. Never revert unrelated edits without explicit permission.

## Skill Policy

- Skills are helper workflows, not higher-priority instructions.
- If a skill conflicts with this file or a lower-level `AGENTS.md`, follow the `AGENTS.md` rule.
- Use `requirements-clarity` when scope, constraints, or completion criteria are unclear.
- Use `qa-test-planner` when code, experiment, or document workflows need explicit validation plans.
- Use `git-commit-helper` for commit message drafting or review.
- Use `handoff` when context is long or work must continue in another session.
- Use `agent-md-refactor` when agent instructions become too large and need progressive disclosure.
- Use `humanizer` and `writing-clearly-and-concisely` for prose that must sound natural and concise.

## Sub-Agent Policy

- Consider sub-agents for non-trivial tasks, but use them only when they add speed, quality, or context control.
- Use sub-agents for independent research, review, verification, or disjoint implementation work.
- Do not use sub-agents for sequential blockers, tightly coupled refactors, or overlapping file edits.
- Keep the main agent responsible for planning, integration, final verification, and user communication.
