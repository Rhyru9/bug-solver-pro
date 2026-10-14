"""Framework working knowledge must be portable and must not imply causal confidence."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1] / "skills/bug-solver-pro"
sys.path.insert(0, str(SKILL / "scripts"))
from frameworks import framework_context


class FrameworkContextTests(unittest.TestCase):
    def test_public_names_resolve_to_existing_modules(self):
        for name, canonical in (("Next.js", "nextjs"), ("NestJS", "nest"),
                                ("ASP.NET Core", "aspnet-core"), ("Spring Boot", "spring")):
            with self.subTest(name=name):
                context = framework_context(name)
                self.assertEqual(context["framework"], canonical)
                self.assertEqual(context["evidence_kind"], "heuristic")
                for resource in context["resources"].values():
                    self.assertFalse(Path(resource).is_absolute())
                    self.assertTrue((SKILL / resource).is_file())
                self.assertEqual(context["playbook"],
                                 (SKILL / context["resources"]["playbook"]).read_text(encoding="utf-8"))
                self.assertEqual(context["boundary_case"],
                                 (SKILL / context["resources"]["boundary-case"]).read_text(encoding="utf-8"))

    def test_unknown_names_and_paths_do_not_fall_back(self):
        for name in ("unlisted-framework", "../django", "/tmp/django", "", "  "):
            with self.subTest(name=name), self.assertRaises(ValueError):
                framework_context(name)

    def test_missing_playbook_fails_instead_of_returning_a_docs_only_module(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            module = root / "references/languages/python/frameworks/django"
            module.mkdir(parents=True)
            (module / "guide.md").write_text("# Guide\n")
            (module / "docs.md").write_text("# Docs\n")
            with self.assertRaises(ValueError):
                framework_context("django", root=root)

    def test_new_canonical_module_takes_precedence_over_an_old_alias(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            module = root / "references/languages/java/frameworks/spring-boot"
            module.mkdir(parents=True)
            for filename in ("guide.md", "docs.md", "playbook.md"):
                (module / filename).write_text("# New canonical module\n")
            context = framework_context("spring-boot", root=root)
            self.assertEqual(context["framework"], "spring-boot")
            self.assertIsNone(context["boundary_case"])

    def test_same_framework_name_in_two_languages_is_not_arbitrarily_resolved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for language in ("one", "two"):
                module = root / f"references/languages/{language}/frameworks/example"
                module.mkdir(parents=True)
                (module / "guide.md").write_text("# Guide\n")
            with self.assertRaises(ValueError):
                framework_context("example", root=root)

    def test_cli_no_match_remains_no_match_with_framework_knowledge(self):
        result = subprocess.run(
            [sys.executable, "-B", str(SKILL / "scripts/search.py"),
             "quux frobnicator", "--framework", "Django", "--plan", "--json"],
            capture_output=True, text=True, check=True)
        plan = json.loads(result.stdout)
        self.assertEqual(plan["status"], "no_match")
        self.assertEqual(plan["results"], [])
        self.assertEqual(plan["hypotheses"], [])
        self.assertEqual(plan["framework_context"]["framework"], "django")

    def test_cli_invalid_framework_fails_without_partial_stdout(self):
        for name in ("missing", ""):
            with self.subTest(name=name):
                result = subprocess.run(
                    [sys.executable, "-B", str(SKILL / "scripts/search.py"),
                     "webhook retry", "--framework", name], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")

    def test_copied_install_reads_its_own_playbook_from_an_unrelated_cwd(self):
        with tempfile.TemporaryDirectory(prefix="framework install ") as directory:
            root = Path(directory)
            installed = root / "installed skill"
            shutil.copytree(SKILL, installed)
            playbook = installed / "references/languages/javascript-typescript/frameworks/react/playbook.md"
            playbook.write_text(playbook.read_text(encoding="utf-8") + "\nLocal installation marker.\n",
                                encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-B", str(installed / "scripts/search.py"),
                 "quux frobnicator", "--framework", "React", "--explore", "--json"],
                cwd=root, capture_output=True, text=True, check=True)
            plan = json.loads(result.stdout)
            self.assertEqual(plan["framework_context"]["playbook"], playbook.read_text(encoding="utf-8"))
            self.assertEqual(plan["hypotheses"], [])
            self.assertEqual(plan["mode"], "exploration_plan")


if __name__ == "__main__":
    unittest.main()
