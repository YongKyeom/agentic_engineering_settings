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


def merge_codex_terminal_environment(document: dict) -> None:
    """Preserve the current allowlist while passing live Herdr terminal context."""
    policy = document.get("shell_environment_policy")
    if policy is None:
        return  # Codex defaults to inheriting all; no allowlist needs widening.
    filters = policy.get("filters")
    includes = ([key for key, action in filters.items() if action == "include"]
                if filters is not None else list(policy.get("include_only", [])))
    inherit = policy.get("inherit", "all")
    if inherit in {"core", "none"}:
        # Unix core names from Codex 0.170.0 protocol/src/shell_environment.rs.
        names = (["PATH", "SHELL", "TMPDIR", "TEMP", "TMP", "HOME", "LANG",
                  "LC_ALL", "LC_CTYPE", "LOGNAME", "USER"] if inherit == "core" else [])
        names += list(policy.get("set", {}))
        includes = [name for name in dict.fromkeys(names) if not includes or any(
            re.fullmatch(re.escape(pattern).replace(r"\*", ".*").replace(r"\?", "."), name, re.IGNORECASE)
            for pattern in includes
        )]
        policy["inherit"] = "all"
    elif not includes:
        return
    for pattern in ("HERDR_*", "HC_*"):
        if pattern not in includes:
            includes.append(pattern)
    if filters is None:
        policy["include_only"] = includes
    else:
        excludes = [key for key, action in filters.items() if action == "exclude"]
        if {key.lower() for key in excludes}.intersection(pattern.lower() for pattern in includes):
            # The keyed form cannot represent both actions for the same name.
            # Codex applies set overrides after excludes but before includes.
            del policy["filters"]
            policy["exclude"] = excludes
            policy["include_only"] = includes
            return
        for key in list(filters):
            if filters[key] == "include":
                del filters[key]
        excluded = {key.lower() for key in filters}
        for pattern in includes:
            if pattern.lower() not in excluded:
                filters[pattern] = "include"


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
    core_official = subprocess.check_output(["hc", "--skill"], text=True) if shutil.which("hc") else None

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
        datetime.now().strftime("herdr-%Y%m%d-%H%M%S-%f-") + str(os.getpid())
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
        if core_official is not None:
            core_destination = directory / "HERDR-CORE.md"
            if not core_destination.exists() or core_destination.read_text() != core_official:
                save(core_destination, f"{name}-HERDR-CORE.md")
                core_destination.write_text(core_official)
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
            codex_config = directory / "config.toml"
            if codex_config.exists():
                original = codex_config.read_text()
                codex_document = tomlkit.parse(original)
                merge_codex_terminal_environment(codex_document)
                updated_config = tomlkit.dumps(codex_document)
                if updated_config != original:
                    codex_config.write_text(updated_config)
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
