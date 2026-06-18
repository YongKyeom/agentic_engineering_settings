# Project Name

이 프로젝트가 해결하는 문제와 핵심 목적을 2~3문장으로 설명한다.
누가 사용하는지, 어떤 입력을 받아 어떤 결과를 내는지 먼저 적는다.

## Quick Start

```sh
# 1. 의존성 설치
uv sync

# 2. 실행
uv run python -m <package_or_module>

# 3. 테스트
uv run pytest
```

## Requirements

- Python 3.11+
- `uv`

필요한 외부 서비스, API key, 시스템 패키지, GPU/CPU 조건이 있으면 여기에 추가한다.

## Configuration

환경 변수는 `.env` 또는 실행 환경에서 관리한다. 예시는 `.env.example`에 둔다.

```sh
cp .env.example .env
```

| 변수 | 설명 | 예시 |
|------|------|------|
| `EXAMPLE_API_KEY` | 외부 API 호출에 사용하는 key | `...` |
| `LOG_LEVEL` | 로그 레벨 | `INFO` |

프로젝트에 환경 변수가 없다면 이 섹션을 삭제한다.

## Usage

가장 중요한 사용 흐름을 실제 명령 중심으로 적는다.

```sh
uv run python -m <package_or_module> --help
uv run python -m <package_or_module> --input data/input.csv --output outputs/result.csv
```

CLI가 아니라 라이브러리라면 최소 사용 예제를 둔다.

```python
from package_name import main_function

result = main_function(...)
```

## Development

```sh
# lint
uv run ruff check --fix .

# test
uv run pytest

# targeted test
uv run pytest tests/test_example.py
```

## Project Structure

```text
.
├── src/                    # source code
├── tests/                  # automated tests
├── docs/                   # project docs
└── README.md               # this file
```

실제 구조가 다르면 이 트리를 먼저 수정한다.

## Documentation

- [Coding Convention](docs/coding-convention.md)
- [Git Convention](docs/git-convention.md)
- [Architecture](docs/architecture.md)
- [Plans](docs/plan/README.md)
- [Decisions](docs/decisions/README.md)

## Testing Policy

- 변경한 동작에 가장 가까운 테스트를 먼저 실행한다.
- 문서만 바꿨다면 코드 lint/test를 억지로 실행하지 않는다.
- 검증하지 않은 내용을 완료된 것처럼 쓰지 않는다.

## Notes For Maintainers

- 프로젝트 규칙이 바뀌면 README와 `docs/` 문서를 함께 갱신한다.
- 장기적으로 남겨야 하는 결정은 `docs/decisions/`에 기록한다.
