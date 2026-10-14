"""Regression queries for previously unreachable local techniques and new data mechanisms."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1] / "skills/bug-solver-pro"
sys.path.insert(0, str(SKILL / "scripts"))
from core import search
from recipe_index import search_recipes


class RecipeRetrievalTests(unittest.TestCase):
    def test_previously_missing_framework_queries_reach_the_relevant_technique(self):
        cases = [
            ("body signature whitespace", "express-boundary"),
            ("component key reorder draft", "react-boundary"),
            ("filtered include navigation fixup", "aspnet-core-boundary"),
            ("runtime dto metadata validation", "nest-boundary"),
            ("orwhere tenant boolean grouping", "laravel-boundary"),
            ("persist flush identity map", "symfony-boundary"),
            ("second binder eof body", "gin-boundary"),
        ]
        for query, expected in cases:
            with self.subTest(query=query):
                result = search_recipes(query)
                self.assertEqual(result["status"], "matched")
                self.assertEqual(result["results"][0]["id"], expected)
                self.assertTrue(result["results"][0]["content"])

    def test_new_shared_data_mechanisms_rank_a_specific_discriminator(self):
        cases = [
            ("write skew shared predicate", "write-skew"),
            ("cache invalidation late fill", "stale-cache-refill"),
            ("lease expired stale owner", "lease-fencing"),
            ("nested retry deadline amplification", "retry-amplification"),
            ("data join multiplies totals", "query-cardinality"),
            ("sql null not in exclusion", "null-membership"),
        ]
        for query, expected in cases:
            with self.subTest(query=query):
                result = search(query)
                self.assertEqual(result["results"][0]["id"], expected)
                self.assertEqual(result["status"], "matched")

    def test_realistic_unrelated_and_broad_queries_are_not_strong_recipe_matches(self):
        for query in ("css font weight display", "marketing launch calendar",
                      "database backup schedule documentation", "garden flowers soil water"):
            with self.subTest(query=query):
                result = search_recipes(query)
                self.assertNotEqual(result["status"], "matched")
                self.assertTrue(all(row["match_quality"] == "weak_match" for row in result["results"]))

    def test_framework_filter_applies_before_limit_without_changing_score(self):
        full = search_recipes("raw body", limit=10)
        scoped = search_recipes("raw body", framework="hono", limit=1)
        self.assertEqual(len(scoped["results"]), 1)
        hit = scoped["results"][0]
        self.assertEqual(hit["framework"], "hono")
        same = next(row for row in full["results"] if row["id"] == hit["id"])
        self.assertEqual(same["score"], hit["score"])

    def test_domain_filter_does_not_fall_back_to_other_recipe_domains(self):
        result = search_recipes("signature whitespace", framework="express", domain="state")
        self.assertEqual(result["status"], "no_match")
        self.assertEqual(result["results"], [])

    def test_cli_can_find_working_knowledge_without_inventing_a_catalog_hypothesis(self):
        for mode in ("--plan", "--explore"):
            with self.subTest(mode=mode):
                result = subprocess.run(
                    [sys.executable, "-B", str(SKILL / "scripts/search.py"),
                     "body signature whitespace", mode, "--json"],
                    capture_output=True, text=True, check=True)
                plan = json.loads(result.stdout)
                self.assertEqual(plan["status"], "no_match")
                self.assertEqual(plan["hypotheses"], [])
                self.assertEqual(plan["framework_matches"]["status"], "matched")
                self.assertEqual(plan["framework_matches"]["results"][0]["id"], "express-boundary")

    def test_corrupt_recipe_data_fails_explicitly_from_a_copied_install(self):
        with tempfile.TemporaryDirectory(prefix="recipe data ") as directory:
            root = Path(directory)
            installed = root / "installed skill"
            shutil.copytree(SKILL, installed)
            path = installed / "data/frameworks/javascript-typescript/express/recipes.json"
            path.write_text('{"schema_version":1,"schema_version":2}')
            result = subprocess.run(
                [sys.executable, "-B", str(installed / "scripts/search.py"),
                 "body signature whitespace", "--json"], cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("Duplicate JSON key", result.stderr)

    def test_plain_cli_prints_working_knowledge_instead_of_only_an_index_hit(self):
        result = subprocess.run(
            [sys.executable, "-B", str(SKILL / "scripts/search.py"), "body signature whitespace"],
            capture_output=True, text=True, check=True)
        source = SKILL / "references/languages/javascript-typescript/frameworks/express/boundary-case.md"
        self.assertIn(source.read_text(encoding="utf-8").strip(), result.stdout)


if __name__ == "__main__":
    unittest.main()
