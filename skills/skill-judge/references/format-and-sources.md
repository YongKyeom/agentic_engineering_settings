# Format requirements and source guidance

Use this reference for format, portability, or source-of-truth questions. The links below were checked during the repository review on 2026-11-17; verify the current target documentation when client behavior or a schema detail matters to the task.

## Requirement classes

| Class | Treatment |
|---|---|
| Explicit user or project requirement | Binding within its scope, subject to higher-priority instructions |
| Target format/client requirement | Check against that specification or the installed validator/version |
| Official design recommendation | Assess its benefit for this task; do not mislabel it as a schema failure |
| Reviewer heuristic or local convention | State its rationale and scope; do not present it as official |

## Common format checks

The [Agent Skills specification](https://agentskills.io/specification) defines `SKILL.md` with YAML frontmatter and a Markdown body. Among its naming and metadata rules:

- `name` and `description` are required.
- Names are limited to 64 characters, use lowercase letters/numbers/hyphens, match the directory name, and must not start/end with a hyphen or contain consecutive hyphens. Consult the target parser for accepted character details.
- Descriptions are non-empty and limited to 1,024 characters under this specification.
- `license`, `compatibility`, `metadata`, and experimental `allowed-tools` have defined optional roles. Client support and accepted representations can differ; check the declared target rather than silently normalizing every package to one runtime.
- Supporting directories are optional. Validate actual referenced paths relative to the file or skill-root convention used by that reference.

A client may add its own metadata or invocation configuration. Inspect existing settings before changing them. For example, `agents/openai.yaml` can carry Codex UI and invocation settings, but its absence alone does not make an instruction-only skill invalid. Do not reset an existing invocation policy as part of a prose cleanup.

Validators have bounded coverage. Report which validator/version or checks were used; format success does not establish useful selection, safe actions, or correct task output.

## Design recommendations

[Anthropic's authoring guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) recommends concise instructions, task-appropriate freedom, on-demand references, and representative usage evaluation. Its under-500-line guidance is a context-management recommendation, not a substitute for assessing lost invariants or actual loading cost.

[OpenAI's skill guidance](https://developers.openai.com/plugins/build/skills) emphasizes clear use cases, explicit user-instruction precedence, resource routing, and evaluating activation as well as output quality. Assess direct, indirect, incomplete, adjacent, and unsupported-action requests as relevant.

Use the current `skill-creator` for skill authoring and revision, and `skill-judge` for evidence-based evaluation of the result. Resolve conflicts against the target's actual requirements and user intent. No official source cited here requires a 120-point rubric, five-pattern taxonomy, universal NEVER list, or estimated ratio of knowledge categories.
