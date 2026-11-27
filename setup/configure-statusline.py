# /// script
# requires-python = ">=3.11"
# dependencies = ["tomlkit>=0.13,<1"]
# ///
"""Install and select the shared Codex statusline in the user config."""

import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

import tomlkit


def main():
    python = shutil.which("python3")
    if not python:
        raise SystemExit("Python 3 is required for the statusline provider.")
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    codex_home.mkdir(parents=True, exist_ok=True)
    config = codex_home / "config.toml"
    original = config.read_text() if config.exists() else ""
    document = tomlkit.parse(original)
    provider = codex_home / "statusline" / "statusline.py"
    server = document.setdefault("mcp_servers", {}).setdefault("workspace-statusline", {})
    server.update({"command": python, "args": ["-u", str(provider)], "enabled": True})
    document.setdefault("features", {})["tui_extensions_statusline"] = True
    tui = document.setdefault("tui", {})
    tui["status_line_provider"] = {"server": "workspace-statusline", "tool": "statusline"}
    tui["status_line_use_colors"] = True
    updated = tomlkit.dumps(document)
    # Back up both files before updating an existing installation.
    if original != updated or (provider.exists() and provider.read_bytes() !=
                               Path(__file__).with_name("statusline.py").read_bytes()):
        backup = codex_home / "backups" / datetime.now().strftime("statusline-%Y%m%d-%H%M%S-%f")
        backup.mkdir(parents=True)
        for path in (config, provider):
            if path.exists():
                shutil.copy2(path, backup / path.name)
    provider.parent.mkdir(parents=True, exist_ok=True)
    for destination, content in (
        (provider, Path(__file__).with_name("statusline.py").read_text()),
        (config, updated),
    ):
        # Readers see either the previous complete file or the new complete file.
        with tempfile.NamedTemporaryFile(mode="w", dir=destination.parent, delete=False) as stream:
            stream.write(content)
            temporary = Path(stream.name)
        temporary.replace(destination)
    print(f"Workspace statusline installed and selected globally in {config}")
    print("Restart Codex CLI to load the provider.")


if __name__ == "__main__":
    main()
