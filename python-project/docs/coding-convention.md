# Coding Convention

Use this guide for Python code style, documentation, typing, error handling, and validation.

## Formatting And Style

- Follow the formatter and linter settings defined by the project.
- Use the project's configured formatting and linting tools actively. Prefer `ruff` as the primary linter and formatter; use `black` and `isort` alongside it when they are configured.
- Keep line length at the project default. If no default exists, use 140 characters.
- Use clear names: constants in `UPPER_SNAKE_CASE`, classes in `PascalCase`, functions and methods in `snake_case`.
- Keep logical blocks separated with blank lines when it improves readability.

## Ruff Scope

- Use `ruff` only for Python files and Python-related files supported by Ruff.
- Do not use `ruff` for Markdown, YAML, JSON, TOML, shell scripts, or documentation-only changes.
- For documentation changes, review Markdown manually or use a Markdown-specific formatter/linter only if the project already has one.
- For YAML, JSON, or TOML, use project-configured tools only. Do not introduce a new formatter just to validate a small documentation or configuration change.

## Docstrings And Comments

- Add a module-level docstring at the top of each `.py` file.
- The module docstring should explain the file's responsibility, main entry points, important dependencies, and any domain assumptions.
- Write Google-style docstrings for all public and internal functions and classes.
- Pay particular attention to classes and functions that contain business logic, branching rules, I/O, model behavior, data transformation, or non-trivial side effects.
- Always document `__init__`, `forward`, loss calculation, preprocessing, sampling, training, and evaluation methods.
- In docstrings, always include `Args`, `Returns`, `Raises`, and `Side Effects` sections. If a section has nothing to document, write "없음." explicitly.
- In docstrings, include type information for `Args`, `Returns`, and `Attributes` even when the Python signature already has type hints.
- Include tensor shape, mask semantics, input range, unit, and side effects when they affect correctness.
- Prefer concise Korean explanations for project-specific reasoning.
- Keep commands, identifiers, tensor names, and API names in English.
- Update comments when code changes.
- Add detailed comments at important branch points and business-logic decisions.
- For conditionals that change behavior, explain why the branch exists, what business or domain rule it represents, and what can break if it changes.
- For temporary exceptions, compatibility paths, fallback behavior, or policy decisions, include the reason and removal condition when known.

Use this structure when details matter:

```python
class InteractionSampler:
    """사용자 interaction sequence에서 학습용 sample을 생성.

    이 클래스는 시간순 interaction을 받아 positive/negative sample을 만든다.
    sampling 정책은 evaluation 누수와 직접 연결되므로, strategy 변경 시 `docs/decisions/` 또는 관련 plan에 변경 이유를 남긴다.

    Attributes:
        max_sequence_length (int): 모델에 입력할 최대 sequence 길이.
        negative_sample_count (int): positive item 하나당 생성할 negative item 수.
    """

    def __init__(
        self,
        *,
        max_sequence_length: int,
        negative_sample_count: int,
    ) -> None:
        """Sampler 설정을 검증하고 random generator를 초기화.

        Args:
            max_sequence_length (int): 모델에 입력할 최대 sequence 길이.
            negative_sample_count (int): positive item 하나당 생성할 negative item 수.

        Returns:
            없음.

        Raises:
            ValueError: `max_sequence_length`가 1보다 작거나, `negative_sample_count`가 음수인 경우.

        Side Effects:
            내부 random generator 상태를 초기화한다.
        """

    def sample(self, sequence: list[int]) -> list[int]:
        """주어진 interaction sequence에서 negative sample을 생성.

        Args:
            sequence (list[int]): 시간순 interaction item id 목록.

        Returns:
            list[int]: 생성된 negative item id 목록.

        Side Effects:
            내부 random generator 상태가 변경된다.
        """
```

## Comments For Execution Flow

- Add short comments at major pipeline gates: object creation, data loading, training loop, evaluation, and export.
- For CLI entry points and `if __name__ == "__main__":`, make the execution sequence easy to follow.
- For complex algorithms, split the implementation into blocks and explain the reason for each block.
- Do not add comments that merely repeat the code.

## Imports

- **Import는 모듈 최상단에만 둔다. 함수·클래스·메서드 내부 import를 금지한다** — 설치되지 않은 의존성과 꼬인 import 경로는 호출 시점이 아니라 import(기동) 시점에 드러나야 한다.
- `if TYPE_CHECKING:` 블록(타입 전용 참조)은 모듈 최상단에 있으므로 허용한다.
- 순환 import가 생기면 내부 import로 감추지 말고 모듈 경계를 고친다.

## Typing

- Add precise type hints to function signatures.
- Use built-in generic collections such as `list[int]` and `dict[str, float]`.
- Use `Protocol`, `TypedDict`, `Literal`, and `dataclass` when they make contracts clearer.
- Avoid `Any`. If `Any` is unavoidable, document why.
- Use `-> None` for functions that do not return a value.

## Error Handling And Logging

- Raise specific exceptions with actionable messages.
- Separate user-facing error messages from developer-facing log messages.
- Use `logger.exception(...)` inside exception handlers when stack traces are useful.
- Do not use `logger.exception(..., exp_info=True)`. The correct keyword is `exc_info=True`, and `logger.exception` already includes exception info.
- **No silent fallback.** Missing configuration or an unavailable dependency fails fast at startup with an explicit error; it never silently degrades to an alternative behavior (e.g., never infer mock mode from an unset URL).
  A wrong-but-loud failure beats a plausible-but-fake success.
- **Error codes live in one dedicated module.** Expected failures are enumerated as typed errors with their defined action and log message.
  Handlers catch these types and apply the defined action, so a log line alone tells "this known problem occurred and was handled this way."
- **Unexpected exceptions must always be identified.** Log with `logger.exception` and re-raise(or surface as an error event).
  Never swallow them in a broad `except` — an unidentified error running in production is worse than a visible failure.

## Validation

- Use the narrowest useful validation first.
- Prefer targeted tests for touched behavior.
- For lint validation, use `uv run ruff check path/to/touched_python_file.py`; for tests, use `uv run pytest tests/test_target.py`.
- Use `uv run ruff check --fix path/to/touched_python_file.py` only when intentionally applying automatic fixes, then inspect the diff.
- Avoid running `ruff` for documentation-only or configuration-only changes.

## Development Philosophy

- Follow `karpathy-guidelines` at all times: avoid overengineering, make surgical changes, surface assumptions, and define verifiable success criteria before starting.
- Keep code hand-editable under pressure: no excessive abstraction layers, no helper-function proliferation, minimal exception hierarchies.
  A developer must be able to read a module top-to-bottom and patch it by hand in an emergency.
