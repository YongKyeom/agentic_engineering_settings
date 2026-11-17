# Skill Judge

Review whether a skill selects the right work, preserves the user's intent and permissions, and produces correct results with appropriate resource use.

## Use

Ask for an audit, comparison, or targeted improvement and identify the package or workflow. The default is a read-only review. Updating files, installing globally, publishing, or running external actions follows the user's requested scope.

The agent starts with [SKILL.md](SKILL.md), follows relevant resources, and reports evidence-backed findings rather than a grade by default.

| Review area | Question |
|---|---|
| Selection | Does the description distinguish intended requests from neighboring tasks? |
| Intent and authority | Are user choices, allowed actions, and file destinations preserved? |
| Useful content | Do the instructions add relevant decisions without unnecessary ceremony? |
| Fidelity | Are facts, conditions, uncertainty, and operational contracts preserved? |
| Resources | Are references discoverable, current enough, and loaded only when useful? |
| Behavior | What actually happened for representative requests, and what remains untested? |

## Results

The report identifies the reviewed scope, findings with file/line evidence, useful behavior to retain, prioritized changes, actual validation, and open limits. A score can be supplied when requested with explicit anchors and uncertainty; it never overrides a blocking issue or proves production readiness.

## Supporting guidance

- [Format and sources](references/format-and-sources.md): schema questions, client differences, and the distinction between requirements and recommendations.
- [Behavioral evaluation](references/behavioral-evaluation.md): representative requests, isolated execution, independent evaluation, evidence, and bounded reruns.

Neither extra directories nor a rigid report template is required for every reviewed skill. Check the package's actual purpose and consumers before recommending structural changes.
