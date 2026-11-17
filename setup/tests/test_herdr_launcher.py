"""Exercise project selection without connecting to any Herdr server."""

import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

LAUNCHER = Path(__file__).resolve().parents[1] / "herdr.zsh"


@unittest.skipUnless(shutil.which("zsh"), "zsh is required")
class HerdrLauncherTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        binary = self.root / "bin/herdr"
        binary.parent.mkdir()
        binary.write_text('#!/bin/sh\nprintf "%s\\n" "$PWD" "$@"\n')
        binary.chmod(0o755)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("HERDR_")}
        self.env["PATH"] = str(binary.parent) + os.pathsep + self.env["PATH"]

    def invoke(self, cwd, args=(), **env):
        result = subprocess.run(
            ["zsh", "-dfc", 'source "$1"; shift; herdr "$@"', "test", str(LAUNCHER), *args],
            cwd=cwd, env={**self.env, **env}, text=True, capture_output=True, check=True,
        )
        return result.stdout.splitlines()

    def expected(self, root):
        return "project-" + hashlib.sha256(str(root.resolve()).encode()).hexdigest()[:16]

    def test_non_git_directory_with_spaces_preserves_cwd(self):
        project = self.root / "project with spaces"
        project.mkdir()
        self.assertEqual(self.invoke(project), [str(project.resolve()), "--session", self.expected(project)])

    def test_git_subdirectories_share_session_and_keep_launch_directory(self):
        project = self.root / "project"
        project.mkdir()
        subprocess.run(["git", "init", "-q", str(project)], check=True)
        child = project / "child"
        child.mkdir()
        self.assertEqual(self.invoke(project)[1:], self.invoke(child)[1:])
        self.assertEqual(self.invoke(child), [str(child.resolve()), "--session", self.expected(project)])

    def test_different_project_paths_get_different_sessions(self):
        first = self.root / "one"
        second = self.root / "two"
        first.mkdir()
        second.mkdir()
        self.assertNotEqual(self.invoke(first)[2], self.invoke(second)[2])

    def test_commands_and_explicit_session_are_passed_through(self):
        for args in [("config", "check"), ("--session", "manual"), ("--help",)]:
            with self.subTest(args=args):
                self.assertEqual(self.invoke(self.root, args)[1:], list(args))

    def test_managed_pane_and_environment_session_are_preserved(self):
        for env in [{"HERDR_ENV": "1"}, {"HERDR_SESSION": "manual"}, {"HERDR_SOCKET_PATH": "/tmp/test.sock"}]:
            with self.subTest(env=env):
                self.assertEqual(self.invoke(self.root, **env), [str(self.root.resolve())])


if __name__ == "__main__":
    unittest.main()
