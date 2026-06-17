# Coding Convention

Use this guide for Python code style, documentation, typing, error handling, and validation.

## Formatting And Style

- Follow the formatter and linter settings defined by the project.
- Use `ruff` as the primary linter and formatter. Use `black` and `isort` actively alongside `ruff` when the project includes them.
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
- Write Google-style docstrings for public functions, public classes, and important internal interfaces.
- Write docstrings for classes and functions that contain business logic, branching rules, I/O, model behavior, data transformation, or non-trivial side effects.
- Always document `__init__`, `forward`, loss calculation, preprocessing, sampling, training, and evaluation methods.
- In docstrings, always include `Args`, `Returns`, `Raises`, and `Side Effects` sections. If a section has nothing to document, write "없음." explicitly.
- In docstrings, include type information for `Args`, `Returns`, and `Attributes` even when the Python signature already has type hints.
- For `__init__`, document `Args` and `Raises`. Do not add a `Returns` section unless the project explicitly requires it.
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

        Raises:
            ValueError: `max_sequence_length`가 1보다 작거나, `negative_sample_count`가 음수인 경우.
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

## Validation

- Use the narrowest useful validation first.
- Prefer targeted tests for touched behavior.
- Common validation commands: `uv run ruff check --fix .` for lint, `uv run pytest tests/test_target.py` for tests.
- For targeted lint during iteration, use `uv run ruff check --fix path/to/python_file.py`.
- Avoid running `ruff` for documentation-only or configuration-only changes.

## Development Philosophy

- Follow `karpathy-guidelines` at all times: avoid overengineering, make surgical changes, surface assumptions, and define verifiable success criteria before starting.
