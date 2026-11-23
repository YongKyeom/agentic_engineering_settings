"""기존 전역 설정을 백업하고 RTK/Serena hook과 Serena MCP를 병합한다."""

import json
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def save(path: Path, content: str, backup: Path) -> None:
    """변경 파일만 원래 상대 경로로 백업하고 저장한다."""
    if path.exists():
        if path.read_text() == content:
            return
        target = backup / path.relative_to(Path.home())
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def read_json(path: Path) -> dict:
    """기존 JSON을 읽고 파일이 없으면 빈 설정을 반환한다."""
    return json.loads(path.read_text()) if path.exists() else {}


def merge_hooks(data: dict, client: str, rtk: str, serena_hooks: str) -> None:
    """관리 대상 hook만 교체하고 사용자 hook과 event 속성을 보존한다."""
    events = data.setdefault("hooks", {})
    for event, groups in events.items():
        kept = []
        for group in groups:
            hooks = [h for h in group.get("hooks", []) if not re.search(
                r"(?:^|[/\s'\"])serena-hooks(?:[\s'\"]|$)|rtk-rewrite|\brtk(?:['\"])?\s+hook\b",
                h.get("command", ""),
            )]
            if hooks or not group.get("hooks"):
                kept.append({**group, "hooks": hooks})
        events[event] = kept

    def command(action: str) -> dict:
        return {"type": "command", "command": f"{shlex.quote(serena_hooks)} {action} --client={client}",
                "timeout": 3 if action == "cleanup" and client == "codex" else 5}

    def add(event: str, matcher: str, hooks: list) -> None:
        events.setdefault(event, []).append({"matcher": matcher, "hooks": hooks})

    # RTK만 Bash 명령을 rewrite한다. Serena 사용은 에이전트가 선택한다.
    add("PreToolUse", "Bash", [
        {"type": "command", "command": f"{shlex.quote(rtk)} hook {'codex' if client == 'codex' else 'claude'}"},
    ])
    if client == "codex":
        add("PreToolUse", "^mcp__serena__", [command("plan-guard")])
        add("UserPromptSubmit", "", [command("plan-context")])
    else:
        add("PreToolUse", "mcp__serena__.*", [command("auto-approve")])
    add("PostToolUse", "^mcp__serena__", [command("reset")])
    add("SessionStart", "startup|resume", [command("activate")])
    add("SessionEnd", "", [command("cleanup")])


def main() -> None:
    """선택한 클라이언트에 실행 파일 절대 경로와 전역 설정을 적용한다."""
    selected = sys.argv[1] if len(sys.argv) > 1 else "all"
    if selected not in {"codex", "claude", "all"}:
        raise SystemExit("Expected codex, claude, or all")
    binaries = {name: shutil.which(name) for name in ("rtk", "serena", "serena-hooks")}
    if not all(binaries.values()):
        raise SystemExit("rtk, serena and serena-hooks must be on PATH")
    backup = Path.home() / ".local/state/agent-setup" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    print(f"Backup: {backup}")
    for name in ("codex", "claude"):
        if selected not in {name, "all"}:
            continue
        path = Path.home() / (".codex/hooks.json" if name == "codex" else ".claude/settings.json")
        data = read_json(path)
        merge_hooks(data, "codex" if name == "codex" else "claude-code", binaries["rtk"], binaries["serena-hooks"])
        save(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n", backup)
        args = ["start-mcp-server", "--project-from-cwd", f"--context={'codex' if name == 'codex' else 'claude-code'}",
                "--open-web-dashboard", "false"]
        if name == "codex":
            config = Path.home() / ".codex/config.toml"
            if config.exists():
                target = backup / ".codex/config.toml"
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(config, target)
            subprocess.run(["codex", "mcp", "add", "serena", "--", binaries["serena"], *args], check=True)
        else:
            config = Path.home() / ".claude.json"
            settings = read_json(config)
            settings.setdefault("mcpServers", {})["serena"] = {"type": "stdio", "command": binaries["serena"], "args": args}
            save(config, json.dumps(settings, indent=2, ensure_ascii=False) + "\n", backup)


if __name__ == "__main__":
    main()
