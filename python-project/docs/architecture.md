# Architecture Guidelines

Use this guide when changing module boundaries, dependencies, data flow, or project layout.

## Single Responsibility

- Keep each function and class focused on one responsibility.
- Split derived responsibilities into helper functions or separate modules.
- Define boundaries by input, output, and ownership.
- If SRP increases complexity, pause and ask the user before over-splitting.

## Suggested Backend Agent Layout

For an agent-enabled backend, use the `Project Map` in the root `AGENTS.md` as the starting point. Adapt the layout to the project instead of forcing it, and replace it for non-agent backends.

```text
src/<package>/
├── core/        # Pure domain rules, models, and contracts
├── app/         # Application use cases and composition root
│   ├── http/    # HTTP/SSE API, authentication boundary, and response mapping
│   └── storage/ # Repository, transaction, database, and external-service adapters
├── agents/      # LLM-facing layer: roles, Tools, policies, providers, and evaluation
├── cli/         # Development and operations command entry points
└── main.py      # Application startup entry point
tests/           # Tests organized to mirror the relevant source area
```

Keep the detailed `agents/` subpackage map in the root `AGENTS.md` rather than duplicating it here.

## Dependency Direction

- Keep `core/` independent from `app/`, `agents/`, HTTP, ORM, and provider SDKs.
- Let `app/` own application composition and inject approved ports into `agents/`.
- Keep `agents/` independent from HTTP routes and ORM implementations; it may depend on `core/` contracts.
- Avoid circular imports.
- Keep the agent runtime and Tool contracts testable without a full HTTP or CLI run.

## Configuration

- Prefer explicit configuration objects over scattered constants.
- Keep environment-specific values outside source code.
- Document defaults that affect reproducibility, metrics, or model behavior.

## Architecture Changes

When making a structural change, document:

- The previous problem.
- The new boundary.
- The migration impact.
- The validation needed.

Long-lived choices belong in `docs/decisions/`.
