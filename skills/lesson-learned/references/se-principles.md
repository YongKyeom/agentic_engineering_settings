# Software Engineering Principles

Optional vocabulary for explaining a pattern already supported by the work. The signals below suggest questions to investigate, rather than proving a principle was applied or violated. Describe the concrete change and consequence first; omit a principle name when it adds no clarity.

## Design principles

| Principle | Meaning and evidence to consider |
|---|---|
| Single Responsibility (SRP) | Group behavior that changes for the same reason. A class split can help when its responsibilities evolve independently; extraction alone does not establish improvement. |
| Open/Closed (OCP) | Support relevant variation through stable extension points. A hook, strategy, or plugin can reduce repeated edits when the variation is real; speculative extension points add cost. |
| Liskov Substitution (LSP) | A replacement must preserve the contract callers rely on, including outcomes, invariants, preconditions, and failures. Inspect caller behavior or contract tests; introducing an interface does not prove substitutability. |
| Interface Segregation (ISP) | Clients should depend only on the operations they need. Splitting an interface helps when distinct clients have distinct contracts; many tiny interfaces can add indirection. |
| Dependency Inversion (DIP) | Let policy depend on a suitable contract rather than a concrete mechanism. Injection or a provider can isolate a genuine dependency boundary; changed import syntax is insufficient evidence. |
| Composition over inheritance | Delegation can make behavior easier to vary without coupling it to a hierarchy. Compare the actual contract and state interactions before recommending a replacement. |

## Simplicity principles

| Principle | Meaning and evidence to consider |
|---|---|
| DRY | Give shared knowledge one authoritative representation. Extraction is useful when the duplicated rule must change together; visually similar code may have different owners. |
| KISS | Use the simplest solution that meets the requirements. Removed indirection can help, but fewer lines do not establish simpler behavior or a complete fix. |
| YAGNI | Avoid speculative capability without a present requirement. Removed options or generalized behavior may illustrate this; confirmed compatibility and recovery requirements still count. |
| Rule of Three | Repeated concrete cases can reveal the right abstraction. Three is a heuristic, not a required wait or extraction threshold; use change coupling, risk, and known variation. |
| Least Surprise | Align behavior with the relevant caller or user contract. Clear names, consistent return types, and explicit effects help when they match those expectations. |

## Structure and ownership

| Principle | Meaning and evidence to consider |
|---|---|
| Separation of concerns | Put distinct responsibilities behind useful boundaries, such as domain logic apart from rendering or persistence. Confirm that responsibilities and interactions became clearer. |
| High cohesion | Keep behavior that serves the same responsibility together. Moving scattered code can help when the new grouping reflects actual change reasons. |
| Loose coupling | Reduce unnecessary knowledge between modules while retaining required contracts. Events or callbacks can introduce hidden dependencies too; inspect the resulting flow. |
| Encapsulation | Expose operations that preserve invariants and limit unsupported access. Reducing public methods matters when callers still have the operations they need. |
| Information hiding | Hide design decisions or representations likely to change behind stable contracts. An accessor alone may still expose internal structure; inspect what callers must know. |

## Pragmatic principles

| Principle | Meaning and evidence to consider |
|---|---|
| Boy Scout Rule | Relevant local cleanup can make the requested change easier to understand. It does not authorize unrelated cleanup or expanding a bounded patch. |
| Fail fast | Detect an invalid condition near the appropriate boundary before it causes misleading or damaging work. Preserve recovery and distinguish invalid input from expected absence. |
| Defensive programming | Handle realistic unexpected inputs according to the contract. Null checks or defaults help only when they do not conceal invalid state or weaken validation. |
| Avoid premature optimization | Establish a relevant bottleneck and compare behavior before adding complexity. A profile or benchmark can support a decision; a claimed speedup needs comparable measured results. |

## Refactoring vocabulary

These describe transformations, not evidence of benefit by themselves:

- **Extract function:** Name a coherent operation or remove shared knowledge when the extraction clarifies behavior.
- **Extract class/module:** Establish a useful responsibility boundary without obscuring required interactions.
- **Replace conditional with polymorphism:** Represent genuine behavioral variation through a stable contract; compare it with a straightforward conditional.
- **Introduce parameter object:** Group related values with shared meaning or invariants; avoid hiding unrelated arguments in a generic object.

For each lesson, explain which condition made the technique useful in this event and what evidence supports the claimed result.
