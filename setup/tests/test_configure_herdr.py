"""Check config preservation and validation before touching real agent settings."""

import contextlib
import fnmatch
import importlib.util
import io
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tomlkit

SCRIPT = Path(__file__).resolve().parents[1] / "configure-herdr.py"
SPEC = importlib.util.spec_from_file_location("configure_herdr", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
OFFICIAL = "---\nname: herdr\n---\nCheck HERDR_ENV=1 before controlling panes.\n"
CORE_OFFICIAL = "# hc manual\nUse HC_TERMINAL_ID as the caller address.\n"


def official_output(arguments, **kwargs):
    return CORE_OFFICIAL if arguments[0] == "hc" else OFFICIAL


class ConfigureHerdrTests(unittest.TestCase):
    def test_core_policy_retains_only_core_overrides_and_terminal_context(self):
        document = tomlkit.parse(
            '# keep this\n[shell_environment_policy]\ninherit = "core"\n'
            'exclude = ["LANG"]\n[shell_environment_policy.set]\nCUSTOM = "mine"\n'
        )
        MODULE.merge_codex_terminal_environment(document)
        policy = document["shell_environment_policy"]
        self.assertEqual(policy["inherit"], "all")
        allowed = lambda name: any(fnmatch.fnmatchcase(name, pattern) for pattern in policy["include_only"])
        for name in ["PATH", "HOME", "CUSTOM", "HERDR_ENV", "HERDR_PANE_ID", "HC_TERMINAL_ID", "HC_TERMINAL_SOCKET", "HC_SCOPE"]:
            self.assertTrue(allowed(name), name)
        for name in ["OPENAI_API_KEY", "UNRELATED", "SSH_AUTH_SOCK"]:
            self.assertFalse(allowed(name), name)
        self.assertEqual(policy["exclude"], ["LANG"])
        self.assertEqual(policy["set"], {"CUSTOM": "mine"})
        first = tomlkit.dumps(document)
        MODULE.merge_codex_terminal_environment(document)
        self.assertEqual(tomlkit.dumps(document), first)

    def test_filtered_core_policy_does_not_expand_existing_nonterminal_selection(self):
        document = tomlkit.parse('[shell_environment_policy]\ninherit = "core"\ninclude_only = ["PATH", "MY_*"]\n')
        MODULE.merge_codex_terminal_environment(document)
        self.assertEqual(document["shell_environment_policy"]["include_only"], ["PATH", "HERDR_*", "HC_*"])

    def test_codex_patterns_treat_brackets_literally(self):
        document = tomlkit.parse('[shell_environment_policy]\ninherit = "core"\ninclude_only = ["[P]ATH"]\n')
        MODULE.merge_codex_terminal_environment(document)
        self.assertEqual(document["shell_environment_policy"]["include_only"], ["HERDR_*", "HC_*"])

    def test_canonical_exclude_then_override_preserves_effective_path(self):
        document = tomlkit.parse(
            '[shell_environment_policy]\ninherit = "core"\n'
            '[shell_environment_policy.set]\nPATH = "/custom/bin"\n'
            '[shell_environment_policy.filters]\n"*" = "include"\nPATH = "exclude"\n'
        )
        MODULE.merge_codex_terminal_environment(document)
        policy = document["shell_environment_policy"]
        self.assertNotIn("filters", policy)
        environment = {"PATH": "/usr/bin", "HOME": "/Users/test", "UNRELATED": "no", "HC_TERMINAL_ID": "t9"}
        environment = {k: v for k, v in environment.items() if k not in policy["exclude"]}
        environment.update(policy["set"])
        environment = {k: v for k, v in environment.items() if any(fnmatch.fnmatchcase(k, p) for p in policy["include_only"])}
        self.assertEqual(environment, {"PATH": "/custom/bin", "HOME": "/Users/test", "HC_TERMINAL_ID": "t9"})

    def test_canonical_filters_preserve_exclusions_and_restrict_core(self):
        document = tomlkit.parse(
            '[shell_environment_policy]\ninherit = "core"\n'
            '[shell_environment_policy.filters]\nPATH = "include"\n"EXTRA_*" = "include"\nHC_SECRET = "exclude"\n'
        )
        MODULE.merge_codex_terminal_environment(document)
        policy = document["shell_environment_policy"]
        self.assertNotIn("include_only", policy)
        self.assertEqual(policy["filters"], {"PATH": "include", "HC_SECRET": "exclude", "HERDR_*": "include", "HC_*": "include"})

    def test_new_instruction_is_stable_and_codex_config_is_backed_up(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            directory = home / "codex"
            directory.mkdir()
            (home / ".zshrc").write_text("# keep my shell settings\nexport MY_SETTING=1\n")
            original_config = '[features]\nhooks = false\n[shell_environment_policy]\ninherit = "core"\n'
            (directory / "config.toml").write_text(original_config)
            with (
                patch.dict(os.environ, {"CODEX_HOME": str(directory), "HERDR_CONFIG_PATH": str(home / "herdr.toml")}),
                patch.object(Path, "home", return_value=home),
                patch.object(MODULE.sys, "argv", [str(SCRIPT), "codex"]),
                patch.object(MODULE.shutil, "which", return_value="/test/zsh"),
                patch.object(MODULE.subprocess, "check_output", side_effect=official_output),
                patch.object(MODULE.subprocess, "run"),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                MODULE.main()
                first = (directory / "AGENTS.md").read_bytes()
                first_zshrc = (home / ".zshrc").read_bytes()
                MODULE.main()
                self.assertEqual((directory / "AGENTS.md").read_bytes(), first)
                self.assertEqual((home / ".zshrc").read_bytes(), first_zshrc)
                self.assertTrue(first_zshrc.startswith(b"# keep my shell settings\nexport MY_SETTING=1\n"))
                self.assertEqual((home / ".config/agent-setup/herdr.zsh").read_bytes(), SCRIPT.with_name("herdr.zsh").read_bytes())
                self.assertEqual((directory / "HERDR-CORE.md").read_text(), CORE_OFFICIAL)
                installed = tomlkit.parse((directory / "config.toml").read_text())
                self.assertFalse(installed["features"]["hooks"])
                self.assertIn("HC_*", installed["shell_environment_policy"]["include_only"])
            backups = list((home / ".local/state/agent-setup").glob("*/codex-config.toml"))
            self.assertTrue(backups)
            self.assertTrue(any(path.read_text() == original_config for path in backups))

    def test_merge_custom_paths_and_repeated_install_preserve_user_settings(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            config = home / "custom config.toml"
            config.write_text(
                '# keep my comment\n[theme]\nname = "dracula"\n'
                '[terminal]\nnew_cwd = "home"\nkitty_graphics = false\n'
                '[keys]\nprefix = "ctrl+a"\nfocus_pane_left = "prefix+x"\n'
                '[[keys.command]]\nkey = "prefix+z"\ntype = "pane"\ncommand = "pwd"\n'
            )
            codex = home / "custom codex"
            claude = home / "custom claude"
            codex.mkdir()
            rules = codex / "AGENTS.md"
            rules.write_text(
                "# User rules\nKeep me.\n\n## Herdr Terminal Context\nStale block.\n\n"
                "## Other rules\nKeep these too.\n"
            )
            calls = []

            def run(arguments, **kwargs):
                calls.append(arguments)
                if arguments[1:] == ["config", "check"]:
                    parsed = tomlkit.parse(Path(kwargs["env"]["HERDR_CONFIG_PATH"]).read_text())
                    self.assertEqual(parsed["terminal"]["default_shell"], "/test/zsh")

            environment = {
                "HERDR_CONFIG_PATH": str(config),
                "CODEX_HOME": str(codex),
                "CLAUDE_CONFIG_DIR": str(claude),
            }
            with (
                patch.dict(os.environ, environment),
                patch.object(Path, "home", return_value=home),
                patch.object(MODULE.sys, "argv", [str(SCRIPT), "codex"]),
                patch.object(MODULE.shutil, "which", return_value="/test/zsh"),
                patch.object(MODULE.subprocess, "check_output", side_effect=official_output),
                patch.object(MODULE.subprocess, "run", side_effect=run),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                MODULE.main()
                first = (config.read_bytes(), rules.read_bytes())
                MODULE.main()
                self.assertEqual(first, (config.read_bytes(), rules.read_bytes()))
            parsed = tomlkit.parse(config.read_text())
            self.assertIn("# keep my comment", config.read_text())
            self.assertEqual(parsed["theme"]["name"], "dracula")
            self.assertFalse(parsed["terminal"]["kitty_graphics"])
            self.assertEqual(parsed["terminal"]["new_cwd"], "current")
            self.assertEqual(parsed["keys"]["prefix"], "ctrl+a")
            self.assertEqual(parsed["keys"]["command"][0]["command"], "pwd")
            for direction, letter in (("left", "h"), ("down", "j"), ("up", "k"), ("right", "l")):
                self.assertEqual(parsed["keys"][f"focus_pane_{direction}"], [f"prefix+{letter}", f"prefix+{direction}"])
            self.assertEqual((codex / "HERDR.md").read_text(), OFFICIAL)
            self.assertEqual(rules.read_text().count("## Herdr Terminal Context"), 1)
            self.assertNotIn("Stale block", rules.read_text())
            self.assertIn("## Other rules\nKeep these too.", rules.read_text())
            self.assertFalse(claude.exists())
            self.assertIn(["herdr", "integration", "install", "codex"], calls)
            self.assertNotIn(["herdr", "integration", "install", "claude"], calls)
            self.assertTrue(list((home / ".local/state/agent-setup").glob("*/config.toml")))

    def test_rejected_candidate_leaves_config_and_agent_files_untouched(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            config = home / "config.toml"
            original = '[keys]\nprefix = "ctrl+a"\n'
            config.write_text(original)
            with (
                patch.dict(os.environ, {"HERDR_CONFIG_PATH": str(config)}),
                patch.object(Path, "home", return_value=home),
                patch.object(MODULE.sys, "argv", [str(SCRIPT)]),
                patch.object(MODULE.shutil, "which", return_value="/test/zsh"),
                patch.object(MODULE.subprocess, "check_output", side_effect=official_output),
                patch.object(MODULE.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "check")),
                self.assertRaises(subprocess.CalledProcessError),
            ):
                MODULE.main()
            self.assertEqual(config.read_text(), original)
            self.assertFalse((home / ".codex").exists())
            self.assertFalse((home / ".local").exists())


if __name__ == "__main__":
    unittest.main()
