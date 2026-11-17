# /// script
# requires-python = ">=3.11"
# dependencies = ["tomlkit>=0.13,<1"]
# ///
"""Merge Herdr defaults and export the installed CLI's official agent Markdown."""

import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import tomlkit


def main() -> None:
    client = sys.argv[1] if len(sys.argv) == 2 else "all"
    if client not in {"codex", "claude", "all"} or len(sys.argv) > 2:
        raise SystemExit("Usage: configure-herdr.py [codex|claude|all]")
    home = Path.home()
    config = Path(os.environ.get("HERDR_CONFIG_PATH", home / ".config/herdr/config.toml")).expanduser()
    source = config.read_text() if config.exists() else ""
    document = tomlkit.parse(source)
    terminal = document.setdefault("terminal", tomlkit.table())
    terminal["default_shell"] = shutil.which("zsh") or sys.exit("zsh not found")
    terminal["shell_mode"] = "auto"
    terminal["new_cwd"] = "current"
    keys = document.setdefault("keys", tomlkit.table())
    for direction, letter in (("left", "h"), ("down", "j"), ("up", "k"), ("right", "l")):
        keys[f"focus_pane_{direction}"] = [f"prefix+{letter}", f"prefix+{direction}"]
    rendered = tomlkit.dumps(document)
    official = subprocess.check_output(["herdr", "--skill"], text=True)
    if "HERDR_ENV" not in official or not official.startswith("---\n"):
        raise SystemExit("Unexpected herdr --skill output; settings were not changed.")

    # Validate with Herdr itself before replacing the user's config.
    with tempfile.TemporaryDirectory(prefix="herdr-config-") as temporary:
        candidate = Path(temporary) / "config.toml"
        candidate.write_text(rendered)
        subprocess.run(
            ["herdr", "config", "check"],
            env={**os.environ, "HERDR_CONFIG_PATH": str(candidate)},
            check=True,
        )

    backup = home / ".local/state/agent-setup" / (
        datetime.now().strftime("herdr-%Y%m%d-%H%M%S-") + str(os.getpid())
    )

    def save(path: Path, label: str) -> None:
        if path.is_file():
            backup.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup / label)

    if source != rendered:
        save(config, "config.toml")
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(rendered)
    print(f"Config: {config}")

    launcher = home / ".config/agent-setup/herdr.zsh"
    launcher_source = Path(__file__).with_name("herdr.zsh").read_text()
    if not launcher.exists() or launcher.read_text() != launcher_source:
        save(launcher, "herdr.zsh")
        launcher.parent.mkdir(parents=True, exist_ok=True)
        launcher.write_text(launcher_source)
    zshrc = Path(os.environ.get("ZDOTDIR") or home).expanduser() / ".zshrc"
    existing_zshrc = zshrc.read_text() if zshrc.exists() else ""
    source_line = f"source {shlex.quote(str(launcher))}"
    if source_line not in existing_zshrc.splitlines():
        save(zshrc, "zshrc")
        zshrc.parent.mkdir(parents=True, exist_ok=True)
        zshrc.write_text(existing_zshrc.rstrip() + "\n\n# agent-setup: Herdr project sessions\n" + source_line + "\n")
    print(f"Project session launcher: {launcher} (open a new zsh to activate)")

    for name, variable, default, instruction, hooks in (
        ("codex", "CODEX_HOME", home / ".codex", "AGENTS.md", "hooks.json"),
        ("claude", "CLAUDE_CONFIG_DIR", home / ".claude", "CLAUDE.md", "settings.json"),
    ):
        if client not in {name, "all"}:
            continue
        directory = Path(os.environ.get(variable, default)).expanduser()
        directory.mkdir(parents=True, exist_ok=True)
        destination = directory / "HERDR.md"
        if not destination.exists() or destination.read_text() != official:
            save(destination, f"{name}-HERDR.md")
            destination.write_text(official)
        # The repo templates contain the same block; merge it for standalone installs too.
        rules = directory / instruction
        marker = "## Herdr Terminal Context"
        existing = rules.read_text() if rules.exists() else ""
        template = (Path(__file__).resolve().parent.parent / instruction).read_text()
        block = template.split(marker + "\n", 1)[1].split("\n## ", 1)[0]
        section = marker + "\n" + block.rstrip() + "\n\n"
        if re.search(r"^" + re.escape(marker) + r"$", existing, re.MULTILINE):
            updated = re.sub(
                r"^" + re.escape(marker) + r"\n.*?(?=^## |\Z)",
                lambda _, replacement=section: replacement,
                existing,
                flags=re.MULTILINE | re.DOTALL,
            )
        else:
            prefix = existing.rstrip()
            updated = (prefix + "\n\n" if prefix else "") + section
        if updated != existing:
            save(rules, f"{name}-{instruction}")
            rules.write_text(updated)
        save(directory / hooks, f"{name}-{hooks}")
        if name == "codex":
            save(directory / "config.toml", "codex-config.toml")
            save(directory / "herdr-agent-state.sh", "codex-herdr-agent-state.sh")
        else:
            save(directory / "hooks/herdr-agent-state.sh", "claude-herdr-agent-state.sh")
        subprocess.run(["herdr", "integration", "install", name], check=True)
        print(f"Official skill: {destination}")
    if backup.exists():
        print(f"Backup: {backup}")
    print("Reload a running session with: herdr server reload-config")


if __name__ == "__main__":
    main()
