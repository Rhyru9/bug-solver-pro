"""Behavior checks for retrieval, abstention, plans, and install portability."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills/bug-solver-pro/scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from core import investigation_plan, load_catalog, search, validate_catalog


class RetrievalTests(unittest.TestCase):
    def test_representative_symptoms_rank_applicable_patterns_first(self):
        examples = [
            ("webhook replay sends duplicate notification", "duplicate-delivery"),
            ("parallel inventory overspend", "check-then-act"),
            ("payment committed caller timeout", "commit-reply-ambiguity"),
            ("crash between commit publish", "commit-publish-gap"),
            ("stale replica after write", "stale-projection"),
            ("tenant cache isolation leak", "tenant-state-leak"),
            ("old records migration null", "legacy-data-shape"),
            ("totals rounding decimal precision", "numeric-representation"),
            ("date timezone midnight", "date-boundary"),
            ("client response field type changed", "consumer-contract-drift"),
            ("heap listeners retained memory", "resource-retention"),
            ("slow endpoint database query count", "query-amplification"),
            ("flaky tests order residual fixtures", "shared-test-state"),
            ("production artifact environment flag", "deployment-mismatch"),
            ("patch introduces second symptom", "patch-chain"),
            ("replayed webhook effects", "duplicate-delivery"),
            ("calendar date offset shift", "date-boundary"),
        ]
        for query, expected in examples:
            with self.subTest(query=query):
                result = search(query)
                self.assertEqual(result["results"][0]["id"], expected)

    def test_unrelated_queries_abstain(self):
        for query in ("purple typography palette", "quux frobnicator", "button border gradient"):
            with self.subTest(query=query):
                result = search(query)
                self.assertEqual(result["status"], "no_match")
                self.assertEqual(result["results"], [])

    def test_generic_and_empty_queries_are_rejected(self):
        for query in ("", "!!!", "please fix the bug", "bug error issue"):
            with self.subTest(query=query), self.assertRaises(ValueError):
                search(query)

    def test_domain_filter_does_not_silently_fall_back(self):
        result = search("webhook", domain="performance")
        self.assertEqual(result["status"], "no_match")
        self.assertEqual(result["domain"], "performance")
        rows = search("cache", domain="state")["results"]
        self.assertTrue(rows)
        self.assertTrue(all(row["domain"] == "state" for row in rows))

    def test_limit_and_deterministic_order(self):
        result = search("retry", limit=1)
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result, search("retry", limit=1))

    def test_plan_preserves_uncertainty_and_discriminating_experiments(self):
        result = search("webhook retry")
        plan = investigation_plan(result)
        self.assertEqual([row["pattern_id"] for row in plan["hypotheses"]], ["duplicate-delivery"])
        patterns = {row["id"]: row for row in result["results"]}
        for hypothesis in plan["hypotheses"]:
            pattern = patterns[hypothesis["pattern_id"]]
            self.assertEqual(hypothesis["status"], "ASSUMED")
            self.assertEqual(hypothesis["experiment"], pattern["experiment"])
            self.assertEqual(hypothesis["falsifying_observation"], pattern["falsifies"])
            self.assertNotIn("observed_cause", hypothesis)

    def test_no_match_plan_does_not_invent_hypotheses(self):
        plan = investigation_plan(search("quux frobnicator"))
        self.assertEqual(plan["hypotheses"], [])
        self.assertEqual(plan["status"], "no_match")

    def test_installed_cli_works_from_unrelated_directory_with_spaces(self):
        import shutil
        with tempfile.TemporaryDirectory(prefix="bug solver ") as directory:
            installed = Path(directory) / "installed skill"
            shutil.copytree(SCRIPT_DIR.parent, installed)
            completed = subprocess.run(
                [sys.executable, "-B", str(installed / "scripts/search.py"),
                 "webhook retry", "--plan", "--json"], cwd=directory,
                capture_output=True, text=True, check=True,
            )
            result = json.loads(completed.stdout)
            self.assertEqual(result["results"][0]["id"], "duplicate-delivery")
            self.assertEqual(result["mode"], "investigation_plan")

    def test_copied_agent_layout_runs_search(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / ".agents" / "skills" / "bug-solver-pro"
            shutil.copytree(SCRIPT_DIR.parent, installed)
            completed = subprocess.run(
                [sys.executable, "-B", str(installed / "scripts/search.py"),
                 "webhook retry", "--plan", "--json"], cwd=directory,
                capture_output=True, text=True, check=True,
            )
            result = json.loads(completed.stdout)
            self.assertEqual(result["results"][0]["id"], "duplicate-delivery")

    def test_fixture_symptom_ranks_duplicate_delivery_plan(self):
        root = SCRIPT_DIR.parents[2]
        symptom = (root / "tests/fixtures/duplicate-webhook/symptom.txt").read_text(encoding="utf-8").strip()
        result = search(symptom)
        self.assertEqual(result["results"][0]["id"], "duplicate-delivery")
        plan = investigation_plan(result)
        self.assertEqual(plan["hypotheses"][0]["pattern_id"], "duplicate-delivery")
        self.assertEqual(plan["hypotheses"][0]["status"], "ASSUMED")
        self.assertNotIn("observed_cause", plan["hypotheses"][0])

    def test_cli_invalid_query_has_nonzero_exit(self):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT_DIR / "search.py"), "!!!"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")


class CatalogTests(unittest.TestCase):
    def catalog(self):
        return {"schema_version": 1, "patterns": copy.deepcopy(load_catalog())}

    def test_complete_catalog_validates(self):
        catalog = self.catalog()
        self.assertEqual(validate_catalog(catalog), catalog["patterns"])

    def test_duplicate_id_is_rejected(self):
        catalog = self.catalog()
        catalog["patterns"].append(copy.deepcopy(catalog["patterns"][0]))
        with self.assertRaises(ValueError):
            validate_catalog(catalog)

    def test_missing_experiment_is_rejected(self):
        catalog = self.catalog()
        del catalog["patterns"][0]["experiment"]
        with self.assertRaises(ValueError):
            validate_catalog(catalog)

    def test_missing_or_escaping_reference_is_rejected(self):
        for ref in ("references/nonexistent.md", "references/../../README.md"):
            with self.subTest(ref=ref):
                catalog = self.catalog()
                catalog["patterns"][0]["references"] = [ref]
                with self.assertRaises(ValueError):
                    validate_catalog(catalog)

    def test_verified_incident_label_is_rejected_for_seed_data(self):
        catalog = self.catalog()
        catalog["patterns"][0]["evidence_kind"] = "verified"
        with self.assertRaises(ValueError):
            validate_catalog(catalog)


class ShellScanTests(unittest.TestCase):
    def run_scan(self, directory, path):
        import os
        return subprocess.run(
            ["/bin/bash", str(SCRIPT_DIR / "scan-risky-patterns.sh"), str(directory)],
            env={**os.environ, "PATH": str(path)}, capture_output=True, text=True,
        )

    @unittest.skipUnless(Path("/bin/bash").exists(), "Optional Bash helper")
    def test_missing_timeout_fails_instead_of_claiming_no_matches(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_scan(directory, directory)
            self.assertEqual(result.returncode, 2)
            self.assertIn("requires timeout or gtimeout", result.stderr)
            self.assertNotIn("(none)", result.stdout)

    @unittest.skipUnless(Path("/bin/bash").exists(), "Optional Bash helper")
    def test_invalid_search_directory_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_scan(Path(directory) / "missing", directory)
            self.assertEqual(result.returncode, 2)
            self.assertIn("does not exist", result.stderr)

    @unittest.skipUnless(Path("/bin/bash").exists(), "Optional Bash helper")
    def test_search_timeout_fails_instead_of_claiming_no_matches(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            executable = root / "timeout"
            executable.write_text("#!/bin/bash\nexit 124\n")
            executable.chmod(0o755)
            (root / "head").symlink_to(shutil.which("head"))
            result = self.run_scan(directory, directory)
            self.assertEqual(result.returncode, 2)
            self.assertIn("status 124", result.stderr)
            self.assertNotIn("(none)", result.stdout)

    @unittest.skipUnless(Path("/bin/bash").exists(), "Optional Bash helper")
    def test_gtimeout_alias_can_find_a_real_candidate(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tools = root / "tools"
            tools.mkdir()
            source = root / "source"
            source.mkdir()
            (source / "example.txt").write_text("TODO investigate this sentinel\n")
            executable = tools / "gtimeout"
            executable.write_text('#!/bin/bash\nshift\nexec "$@"\n')
            executable.chmod(0o755)
            for command in ("head", "rg" if shutil.which("rg") else "grep"):
                (tools / command).symlink_to(shutil.which(command))
            result = self.run_scan(source, tools)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("TODO investigate this sentinel", result.stdout)

    @unittest.skipUnless(Path("/bin/bash").exists(), "Optional Bash helper")
    def test_credential_like_files_are_not_scanned(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tools = root / "tools"
            tools.mkdir()
            source = root / "source"
            source.mkdir()
            (source / "example.txt").write_text("TODO visible sentinel\n")
            (source / ".env").write_text("TODO hidden secret sentinel\n")
            (source / "credentials.json").write_text("TODO credential sentinel\n")
            executable = tools / "gtimeout"
            executable.write_text('#!/bin/bash\nshift\nexec "$@"\n')
            executable.chmod(0o755)
            for command in ("head", "rg" if shutil.which("rg") else "grep"):
                (tools / command).symlink_to(shutil.which(command))
            result = self.run_scan(source, tools)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("TODO visible sentinel", result.stdout)
            self.assertNotIn("hidden secret sentinel", result.stdout)
            self.assertNotIn("credential sentinel", result.stdout)


if __name__ == "__main__":
    unittest.main()
