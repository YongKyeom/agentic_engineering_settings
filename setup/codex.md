# Codex 셋업 가이드

새 머신에 Codex를 처음 설치할 때 이 순서로 진행한다.

## 빠른 셋업 (권장)

자동화 가능한 부분(1~3, 4번)은 스크립트로 한 번에 처리:

```sh
./setup/codex.sh                # 기본 셋업
./setup/codex.sh --with-slidev  # Slidev까지 함께 설치
```

아래는 수동 설치 단계별 가이드.

## 0. 사전 조건

- Codex CLI 설치됨
- 이 레포가 clone되어 있음

## 1. RTK (Rust Token Killer) 설치

```sh
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
rtk init -g
```

검증:
```sh
rtk --version
rtk gain
```

## 2. 전역 AGENTS.md 설치

이 레포의 `AGENTS.md`를 `~/.codex/AGENTS.md`로 복사한다.

```sh
mkdir -p ~/.codex
cp AGENTS.md ~/.codex/AGENTS.md
```

> **주의**: symlink 사용 금지. Codex hook 호환성 문제로 항상 복사 방식을 쓴다.

## 3. 스킬 설치

이 레포의 `skills/` 내용을 `~/.codex/skills/`로 복사한다.

```sh
mkdir -p ~/.codex/skills
cp -R skills/. ~/.codex/skills/
```

이미 설치된 skill을 이 레포의 버전으로 덮어쓰고 싶으면 같은 명령을 다시 실행한다.

설치 후 Codex를 재시작해야 새 skill이 인식된다.

## 4. Slidev (옵션 - 발표자료 작성용)

발표자료를 마크다운으로 작성하고 PDF로 렌더하는 워크플로우.

```sh
npm install -g @slidev/cli
```

> npm 캐시 권한 에러가 나면: `sudo chown -R $(whoami):staff ~/.npm`

스킬 `presentation-slidev`가 워크플로우를 안내한다.

## 5. 검증

```sh
ls -la ~/.codex/AGENTS.md
ls ~/.codex/skills/
```

Codex 새 세션 열어서 슬래시 커맨드(handoff, packet-review 등)가 인식되는지 확인.

## 현재 환경의 skill을 레포에 다시 반영

현재 머신의 설치 상태를 이 레포에 반영할 때, 전체 `~/.codex/skills`를 그대로 복사하지 않는다. 공식/system/plugin 계열은 제외하고, 직접 관리할 skill만 선택해서 복사한다.

```sh
cp -R ~/.codex/skills/<skill-name> skills/<skill-name>
```

그 다음 `skills/<skill-name>/SKILL.md`를 확인하고 commit한다.
