# Requirements Clarity

Resolve the missing decisions that would change implementation, using existing project context before asking the user. The operating instructions are in [SKILL.md](SKILL.md).

Use this skill when a feature's behavior, scope, permissions, or acceptance remains uncertain. A clear bug fix can proceed directly. A large feature may need only one essential decision if the project already defines the rest.

The skill distinguishes confirmed requirements, reversible implementation choices, and decisions owned by the user or an external party. It asks only for the last group when the answer matters, and continues work that does not depend on the answer. “Why?” and “Simpler?” guide reasoning without requiring a recurring interview.

For a small task, the result may be a short scope and acceptance example followed by implementation. For sustained work, update the existing Plan or specification under the project's document rules. A separate PRD, fixed output directory, English prose, numeric score, or final approval round is not required by this skill.

Examples:

- **“Fix the email validation error reproduced here.”** Inspect the relevant contract and code, define the expected result, and perform the fix.
- **“Add an approval feature.”** Inspect existing roles and states, then ask about any missing authority or state-transition decision before implementing the dependent behavior.
- **“Use the approved Plan to add the dashboard.”** Follow the Plan and existing interface conventions; ask only if a material conflict or missing decision remains.

Validate success by whether the next authorized step has a clear goal, relevant constraints, and observable completion criteria. Record unresolved decisions with their owner and blocked scope rather than filling gaps with guesses.
