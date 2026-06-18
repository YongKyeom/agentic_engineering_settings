# Claude Code 셋업 가이드

새 머신에 Claude Code를 처음 설치할 때 이 순서로 진행한다.

## 빠른 셋업 (권장)

자동화 가능한 부분(RTK, 전역 지침, 스킬, Codex plugin, settings, alias, Slidev 옵션)은 스크립트로 한 번에 처리:

```sh
./setup/claude-code.sh                # 기본 셋업
./setup/claude-code.sh --with-slidev  # Slidev까지 함께 설치
```

스크립트 실행 후 Claude Dashboard 플러그인은 수동으로 처리한다.

아래는 수동 설치 단계별 가이드.

## 0. 사전 조건

- Claude Code CLI 설치됨 (`claude --version`으로 확인)
- 이 레포가 clone되어 있음

## 1. RTK (Rust Token Killer) 설치

토큰 절약용 CLI proxy. Claude Code가 자주 호출하는 git/ls/grep 등을 효율적으로 처리한다.

`setup/claude-code.sh`는 RTK가 이미 설치되어 있어도 `rtk init -g`를 다시 시도한다. `rtk`가 아직 PATH에 없어도 `$HOME/.local/bin/rtk`를 확인한다. 이 명령은 전역 RTK 설정과 Claude Code hook 연결을 맞추는 idempotent 단계다.

```sh
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
rtk init -g
```

검증:
```sh
rtk --version
rtk gain
```

## 2. 전역 CLAUDE.md 설치

이 레포의 `CLAUDE.md` 내용을 `~/.claude/CLAUDE.md`로 복사한다.

```sh
cp CLAUDE.md ~/.claude/CLAUDE.md
```

> **주의**: symlink 사용 금지. Codex와의 호환성 문제로 항상 복사 방식을 쓴다.

## 3. 스킬 설치

이 레포의 `skills/` 내용을 `~/.claude/skills/`로 복사한다.

```sh
mkdir -p ~/.claude/skills
for dir in skills/*/; do
  name=$(basename "$dir")
  if [ "$name" = "code-review" ] || [ "$name" = "deep-research" ]; then
    continue
  fi
  target="$HOME/.claude/skills/$name"
  rm -rf "$target"
  mkdir -p "$target"
  cp -R "$dir/." "$target/"
  rm -f "$HOME/.claude/commands/${name}.md"
done
```

`code-review`, `deep-research`는 Claude Code built-in 기능과 중복되므로 skill로 복사하지 않는다.

설치 후 Claude Code를 재시작해야 인식된다.

## 4. Codex plugin 설치

Claude Code 안에서 Codex를 호출하기 위한 OpenAI Codex plugin은 스크립트가 자동으로 설치한다.

수동으로 복구할 때는 다음 명령을 셸에서 실행한다.

```sh
claude plugin marketplace add openai/codex-plugin-cc
claude plugin install codex@openai-codex
claude plugin list
```

## 5. settings.json 설정

`~/.claude/settings.json`에 다음 항목을 설정한다.

### 5.1 Auto 모드 + 권한 화이트리스트

```json
{
  "permissions": {
    "defaultMode": "auto",
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git show:*)",
      "Bash(git branch:*)",
      "Bash(git fetch:*)",
      "Bash(git add:*)",
      "Bash(git stash:*)",
      "Bash(git blame:*)",
      "Bash(git remote -v)",
      "Bash(git rev-parse:*)",
      "Bash(git ls-files:*)",
      "Bash(git worktree:*)",
      "Bash(ls:*)",
      "Bash(pwd)",
      "Bash(cat:*)",
      "Bash(grep:*)",
      "Bash(rg:*)",
      "Bash(find:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(wc:*)",
      "Bash(which:*)",
      "Bash(echo:*)",
      "Bash(date)",
      "Bash(stat:*)",
      "Bash(file:*)",
      "Bash(tree:*)",
      "Read",
      "Glob",
      "Grep",
      "WebFetch",
      "WebSearch"
    ],
    "ask": [
      "Bash(rm:*)",
      "Bash(mv:*)",
      "Bash(chmod:*)",
      "Bash(sudo:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git reset --hard:*)",
      "Bash(git checkout:*)",
      "Bash(git restore:*)",
      "Bash(git clean:*)",
      "Bash(git merge:*)",
      "Bash(git rebase:*)",
      "Bash(git branch -D:*)"
    ]
  }
}
```

- `allow`: 안전한 read-only/staging 명령은 묻지 않고 통과
- `ask`: 파괴적/되돌리기 어려운 명령은 항상 컨펌
- `defaultMode: "auto"`: 위 목록에 없는 명령은 auto classifier가 판단

### 5.2 출력 토큰 / 추론 강도

```json
{
  "env": {
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "65536"
  },
  "effortLevel": "xhigh"
}
```

### 5.3 Advisor 모델 (옵션)

복잡한 판단 시 Opus를 어드바이저로 사용. 비용 절감 + 품질 향상.

```json
{
  "advisorModel": "claude-opus-4-7"
}
```

참고: [The Advisor Strategy](https://claude.com/blog/the-advisor-strategy)

### 5.4 통합 예시

```json
{
  "env": {
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "65536"
  },
  "permissions": {
    "defaultMode": "auto",
    "allow": [ "..." ],
    "ask": [ "..." ]
  },
  "effortLevel": "xhigh",
  "advisorModel": "claude-opus-4-8",
  "verbose": true
}
```

## 6. Shell Alias

`claude` 실행 시 권한 프롬프트 없이 자동으로 시작되도록 `~/.zshrc`에 alias를 추가한다. 스크립트가 자동으로 처리한다.

스크립트 실행 후 alias를 즉시 적용하려면:

```sh
source ~/.zshrc
```

## 7. Claude Dashboard 플러그인 (수동)

> ⚠️ 수동 단계. 셸이 아니라 **실행 중인 Claude Code 세션 안에서** 슬래시 명령으로 입력해야 한다.

상태바에 토큰/비용/세션 정보 표시.

Claude Code를 실행한 뒤 차례대로 입력:

```
/plugin marketplace add uppinote20/claude-dashboard
/plugin install claude-dashboard
/reload-plugins
/claude-dashboard:setup
```

설정 가이드: https://wikidocs.net/342468

추천 옵션:
- displayMode: `detailed` (6줄 전체 정보) 또는 `compact`
- theme: `catppuccin` (mocha)
- plan: `max`
- language: `auto`

## 8. Slidev (옵션 - 발표자료 작성용)

발표자료를 마크다운으로 작성하고 PDF로 렌더하는 워크플로우.

```sh
npm install -g @slidev/cli
```

> npm 캐시 권한 에러가 나면: `sudo chown -R $(whoami):staff ~/.npm`

검증:
```sh
slidev --version
```

스킬 `presentation-slidev`가 워크플로우를 안내한다.

## 9. 검증

새 셋업이 잘 됐는지 확인.

```sh
# Claude Code 자체
claude --version

# 글로벌 인스트럭션 로드 확인
ls -la ~/.claude/CLAUDE.md
ls ~/.claude/skills/

# Codex plugin
claude plugin list

# settings.json 유효성
cat ~/.claude/settings.json | python3 -m json.tool
```

Claude Code 새 세션 열어서 다음 확인:
- `handoff`, `karpathy-guidelines` 같은 skill이 필요한 요청에서 자동으로 로드되는지
- 상태바에 dashboard가 뜨는지
- `git status` 같은 명령이 권한 묻지 않고 바로 실행되는지
- `rm`, `git commit` 같은 명령은 확인 프롬프트가 뜨는지
