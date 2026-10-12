"""Broader retrieval coverage and behavior for mechanisms outside the catalog."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills/bug-solver-pro/scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from core import DOMAINS, exploration_plan, investigation_plan, load_angles, search, validate_angles


class CoverageTests(unittest.TestCase):
    def test_new_mechanisms_rank_applicable_patterns(self):
        examples = [
            ("false zero replaced default", "missing-empty-confusion"),
            ("accent characters unicode normalization", "unicode-normalization"),
            ("unsigned integer wraps negative", "integer-overflow"),
            ("shallow copy mutable child", "aliasing-mutation"),
            ("callback accesses disposed buffer", "use-after-release"),
            ("pooled session fails after reuse", "session-state-reuse"),
            ("startup dependency before readiness", "initialization-order"),
            ("finally exception masks original", "cleanup-masks-failure"),
            ("async loop caller finishes early", "unawaited-work"),
            ("catch returns fallback success", "swallowed-failure"),
            ("terminal status reopens after event", "invalid-state-transition"),
            ("cursor pages skip tied records", "pagination-instability"),
            ("inclusive exclusive index last element", "off-by-one-boundary"),
            ("parser infinite loop never advances", "nonterminating-progress"),
            ("fragmented coalesced stream frames", "partial-stream-framing"),
            ("short writes truncate output bytes", "truncated-write"),
            ("permanent api rejection retried", "external-retry-policy"),
            ("ffi struct alignment calling convention", "native-abi-mismatch"),
            ("simultaneous edits overwrite counter", "lost-update"),
            ("nested mutex wait cycle", "deadlock-lock-order"),
            ("older delayed response replaces newer", "out-of-order-write"),
            ("bulk fails subset remains updated", "partial-batch"),
            ("acknowledged persistent write lost restart", "durability-gap"),
            ("connection pool waiters capacity", "pool-exhaustion"),
            ("cpu blocks timers shared scheduler", "scheduler-starvation"),
            ("regex exponential backtracking growth", "algorithmic-growth"),
            ("expected formula contradicts requirement", "incorrect-oracle"),
            ("mock database hides transaction semantics", "mocked-boundary-gap"),
            ("debugger logging forces lazy evaluation", "observer-effect"),
            ("sourcemap debug symbols wrong binary", "source-artifact-mapping"),
            ("secondary route bypasses resource permission", "authorization-boundary"),
            ("validation decode path changes meaning", "canonicalization-boundary"),
            ("expired token reused after signout", "credential-scope-reuse"),
        ]
        for query, expected in examples:
            with self.subTest(query=query):
                results = search(query)["results"]
                self.assertTrue(results)
                self.assertEqual(results[0]["id"], expected)

    def test_unrecorded_symptom_gets_exploration_without_invented_case(self):
        result = search("quux frobnicator oscillation")
        self.assertEqual(result["status"], "no_match")
        plan = investigation_plan(result)
        self.assertEqual(plan["hypotheses"], [])
        self.assertTrue(plan["exploration"]["axes"])
        self.assertEqual(plan["exploration"]["status"], "questions_only")

    def test_weak_overlap_is_not_promoted_into_hypotheses(self):
        result = search("cache quux frobnicator oscillation")
        self.assertEqual(result["status"], "weak_match")
        self.assertTrue(result["results"])
        self.assertIn("quux", result["unmatched_terms"])
        plan = investigation_plan(result)
        self.assertEqual(plan["hypotheses"], [])
        self.assertIn("exploration", plan)

    def test_single_broad_term_is_not_enough_to_generate_hypotheses(self):
        result = search("cache")
        self.assertEqual(result["status"], "weak_match")
        self.assertTrue(result["results"])
        self.assertEqual(investigation_plan(result)["hypotheses"], [])

    def test_strong_top_match_does_not_promote_weak_secondary_matches(self):
        result = search("duplicate webhook retry")
        self.assertEqual(result["status"], "matched")
        self.assertGreater(len(result["results"]), 1)
        plan = investigation_plan(result)
        self.assertEqual([row["pattern_id"] for row in plan["hypotheses"]], ["duplicate-delivery"])

    def test_explicit_exploration_does_not_force_a_familiar_mechanism(self):
        result = search("duplicate webhook retry")
        self.assertEqual(result["status"], "matched")
        plan = exploration_plan(result)
        self.assertEqual(plan["mode"], "exploration_plan")
        self.assertEqual(plan["hypotheses"], [])
        self.assertIn("exploration", plan)

    def test_domain_filter_routes_relevant_angles(self):
        plan = exploration_plan(search("quux", domain="security"))
        axes = plan["exploration"]["axes"]
        self.assertTrue(axes)
        self.assertTrue(all("security" in axis["domains"] for axis in axes))

    def test_axes_cover_every_domain(self):
        axes = load_angles()
        self.assertEqual({domain for axis in axes for domain in axis["domains"]}, set(DOMAINS))

    def test_incomplete_or_duplicate_angle_data_is_rejected(self):
        data = {"schema_version": 1, "axes": copy.deepcopy(load_angles())}
        for field in ("question", "observation"):
            broken = copy.deepcopy(data)
            del broken["axes"][0][field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_angles(broken)
        data["axes"].append(copy.deepcopy(data["axes"][0]))
        with self.assertRaises(ValueError):
            validate_angles(data)

    def test_exploration_cli_from_unrelated_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run([sys.executable, "-B", str(SCRIPT_DIR / "search.py"),
                                        "quux", "--explore", "--json"],
                                       cwd=directory, capture_output=True, text=True, check=True)
            plan = json.loads(completed.stdout)
            self.assertEqual(plan["status"], "no_match")
            self.assertEqual(plan["hypotheses"], [])
            self.assertTrue(plan["exploration"]["axes"])


if __name__ == "__main__":
    unittest.main()
