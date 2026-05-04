# Architecture Guidelines

Use this guide when changing module boundaries, dependencies, data flow, or project layout.

## Single Responsibility

- Keep each function and class focused on one responsibility.
- Split derived responsibilities into helper functions or separate modules.
- Define boundaries by input, output, and ownership.
- If SRP increases complexity, pause and ask the user before over-splitting.

## Suggested Python Layout

Adapt this layout to the project instead of forcing it.

```text
src/
├── data/        # Loading, preprocessing, datasets, samplers
├── models/      # Model definitions and model utilities
├── training/    # Training loops, losses, optimizers, schedulers
├── evaluation/  # Metrics, validation, reports
├── services/    # Application services or orchestration
└── utils/       # Small shared helpers with low coupling
```

## Dependency Direction

- Keep lower-level modules independent from orchestration code.
- Avoid circular imports.
- Keep data preprocessing separate from model definition when possible.
- Keep training and evaluation logic testable without a full CLI run.

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
