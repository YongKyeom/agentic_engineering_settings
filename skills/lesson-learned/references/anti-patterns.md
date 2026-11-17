# Anti-Patterns

Use these prompts when the event suggests a design problem. A signal warrants inspection; it does not establish an anti-pattern. Confirm the responsibility, contract, or maintenance cost before naming one. A generated file, broad rename, single implementation, or long cohesive algorithm may be appropriate.

| Possible pattern | Evidence to inspect | Bounded response when confirmed |
|---|---|---|
| God Object / God Class | Unrelated responsibilities force the same module to change for different reasons. Inspect dependencies and actual change reasons, rather than file length. | Separate responsibilities with distinct owners or contracts while preserving required interactions. |
| Shotgun Surgery | One business rule requires repeated coordinated edits because its knowledge has several owners. A deliberate interface migration or rename alone is insufficient. | Give the shared rule one owner; preserve legitimate integration changes. |
| Feature Envy | A function repeatedly reaches through another module's internals to implement behavior that belongs to that owner. Cross-module imports alone are insufficient. | Consider moving the behavior near its data or exposing the missing operation. |
| Premature Abstraction | A general interface, factory, or configuration increases complexity without a current requirement, variation, or useful boundary. One implementation alone is insufficient. | Simplify to demonstrated needs; retain boundaries justified by testing, platform isolation, or contracts. |
| Copy-Paste Programming | Similar blocks encode the same knowledge and must evolve together. Similar syntax with independently changing rules is not enough. | Centralize shared knowledge or parameterize the actual variation without coupling unrelated behavior. |
| Magic Numbers / Strings | A literal hides a domain constraint, unit, protocol rule, or unexplained threshold. Obvious local values need no constant by default. | Name or document the meaning where it is owned; keep external protocol values exact. |
| Long Method | Independent responsibilities or interleaved phases obscure invariants and make relevant changes error-prone. Length is a prompt, not a threshold. | Extract meaningful operations when that makes behavior and state easier to follow. |
| Excessive Comments | Comments repeat obvious syntax, conceal unclear naming, or contradict current behavior. Explanations of intent and constraints can be essential. | Improve names and remove stale repetition; retain necessary rationale, units, warnings, and examples. |

Explain the observed cost and relevant tradeoff before suggesting an improvement. A lesson is not authorization to perform the refactor.
