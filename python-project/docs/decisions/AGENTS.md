# Decisions Directory Rules

This directory holds ADRs. The writing procedure, numbering, 6-section template,
and supersede model are owned by the `decision-record` skill; `README.md` has the
folder convention. Ask the agent "ADR 남겨줘" to create one.

- An ADR is committed as shared documentation (unlike `plan/` and `handoff/`).
- When a decision is made on a `feature/` or `fix/` branch, put its ADR in the
  SAME branch and merge it together with the implementation — never split the
  decision record from the code it justifies in history (see `docs/git-convention.md`).
