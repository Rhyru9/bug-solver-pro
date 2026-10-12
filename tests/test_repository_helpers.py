"""Real fixture checks for search and history helpers; no external repositories."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills/bug-solver-pro/scripts"


@unittest.skipUnless(Path("/bin/bash").exists(), "Optional Bash helpers")
class UsageTests(unittest.TestCase):
    def run_helper(self, symbol, directory):
        return subprocess.run(["/bin/bash", str(SCRIPT_DIR / "find-usages.sh"), symbol, str(directory)],
                              capture_output=True, text=True)

    def test_missing_directory_is_failure_not_no_matches(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_helper("marker", Path(directory) / "missing")
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("(none)", result.stdout)

    def test_symbol_is_literal_not_regular_expression(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "sample.txt").write_text("a.b literal-marker\naXb wrong-marker\n")
            result = self.run_helper("a.b", directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("literal-marker", result.stdout)
            self.assertNotIn("wrong-marker", result.stdout)

    def test_real_no_match_is_success(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_helper("unmatched-marker", directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("(none)", result.stdout)

    def test_credential_like_files_are_not_listed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sample.txt").write_text("visible-marker\n")
            (root / ".env").write_text("visible-marker\n")
            (root / "credentials.json").write_text("visible-marker\n")
            result = self.run_helper("visible-marker", directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("sample.txt", result.stdout)
            self.assertNotIn(".env", result.stdout)
            self.assertNotIn("credentials.json", result.stdout)


@unittest.skipUnless(Path("/bin/bash").exists() and shutil.which("git"), "Optional Bash/Git helpers")
class CoChangeTests(unittest.TestCase):
    def git(self, root, *arguments):
        return subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                               *arguments], cwd=root, capture_output=True, text=True, check=True,
                              env={**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})

    def run_helper(self, root, filename, limit="200"):
        return subprocess.run(["/bin/bash", str(SCRIPT_DIR / "co-change.sh"), filename, limit],
                              cwd=root, capture_output=True, text=True)

    def fixture(self, root, peer=True):
        self.git(root, "init", "--quiet")
        (Path(root) / "target.txt").write_text("fixture\n")
        if peer:
            (Path(root) / "peer with spaces.txt").write_text("fixture\n")
        self.git(root, "add", ".")
        self.git(root, "commit", "--quiet", "-m", "fixture")

    def test_single_commit_is_not_dropped_at_eof(self):
        with tempfile.TemporaryDirectory() as directory:
            self.fixture(directory)
            result = self.run_helper(directory, "target.txt")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("peer with spaces.txt", result.stdout)

    def test_no_cochanges_is_valid_empty_result(self):
        with tempfile.TemporaryDirectory() as directory:
            self.fixture(directory, peer=False)
            result = self.run_helper(directory, "target.txt")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("(none)", result.stdout)

    def test_bad_limit_is_not_reported_as_empty_history(self):
        with tempfile.TemporaryDirectory() as directory:
            self.fixture(directory)
            result = self.run_helper(directory, "target.txt", "invalid")
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("(none)", result.stdout)


if __name__ == "__main__":
    unittest.main()
