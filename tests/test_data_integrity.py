"""Reject silent data loss, source drift and incomplete per-framework indexes."""

import copy
from pathlib import Path
import sys
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1] / "skills/bug-solver-pro"
sys.path.insert(0, str(SKILL / "scripts"))
from core import load_angles, load_catalog, load_json, validate_angles, validate_catalog
from recipe_index import read_section, validate_recipe_index


class DataIntegrityTests(unittest.TestCase):
    def recipe_data(self):
        return load_json(SKILL / "data/frameworks/javascript-typescript/express/recipes.json")

    def test_duplicate_json_keys_are_rejected_even_when_nested(self):
        for content in ('{"schema_version":1,"schema_version":2}',
                        '{"row":{"evidence_kind":"heuristic","evidence_kind":"verified"}}'):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "data.json"
                path.write_text(content)
                with self.assertRaises(ValueError):
                    load_json(path)

    def test_repeated_references_and_angle_domains_are_rejected(self):
        catalog = {"schema_version": 1, "patterns": copy.deepcopy(load_catalog())}
        catalog["patterns"][0]["references"] *= 2
        with self.assertRaises(ValueError):
            validate_catalog(catalog)
        data = {"schema_version": 1, "axes": copy.deepcopy(load_angles())}
        data["axes"][0]["domains"] *= 2
        with self.assertRaises(ValueError):
            validate_angles(data)

    def test_boolean_schema_versions_are_not_integer_versions(self):
        examples = [
            (validate_catalog, {"schema_version": True, "patterns": load_catalog()}),
            (validate_angles, {"schema_version": True, "axes": load_angles()}),
            (validate_recipe_index, {**self.recipe_data(), "schema_version": True}),
        ]
        for validate, data in examples:
            with self.subTest(validator=validate.__name__), self.assertRaises(ValueError):
                validate(data)

    def test_recipe_reference_cannot_silently_route_to_another_framework(self):
        data = self.recipe_data()
        row = data["recipes"][0]
        row["references"] = ["references/languages/python/frameworks/fastapi/boundary-case.md"]
        row["heading"] = (SKILL / row["references"][0]).read_text().splitlines()[0]
        with self.assertRaises(ValueError):
            validate_recipe_index(data)

    def test_renamed_or_removed_source_heading_invalidates_the_index(self):
        data = self.recipe_data()
        data["recipes"][0]["heading"] = "## 1. A heading that does not exist"
        with self.assertRaises(ValueError):
            validate_recipe_index(data)

    def test_unindexed_numbered_recipe_or_boundary_case_is_detected(self):
        for removed in (0, -1):
            data = self.recipe_data()
            data["recipes"].pop(removed)
            with self.subTest(removed=removed), self.assertRaises(ValueError):
                validate_recipe_index(data)

    def test_duplicate_recipe_id_or_section_is_rejected(self):
        data = self.recipe_data()
        duplicate = copy.deepcopy(data["recipes"][0])
        data["recipes"].append(duplicate)
        with self.assertRaises(ValueError):
            validate_recipe_index(data)
        duplicate["id"] = "different-id-same-section"
        with self.assertRaises(ValueError):
            validate_recipe_index(data)

    def test_recipe_cannot_be_promoted_to_a_verified_incident(self):
        data = self.recipe_data()
        data["recipes"][0]["evidence_kind"] = "verified"
        with self.assertRaises(ValueError):
            validate_recipe_index(data)

    def test_section_reader_ignores_fake_headings_inside_fenced_examples(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "playbook.md"
            path.write_text("# Book\n\n## 1. Actual\nKeep this.\n```md\n## 2. Fake\n```\nKeep this too.\n\n## 2. Next\nExclude this.\n")
            content = read_section(path, "## 1. Actual")
            self.assertIn("Keep this too.", content)
            self.assertNotIn("Exclude this.", content)
            with self.assertRaises(ValueError):
                read_section(path, "## 2. Fake")

    def test_ambiguous_and_empty_sections_fail_instead_of_returning_partial_knowledge(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "playbook.md"
            for text in ("## Same\nOne\n## Same\nTwo\n", "## Same\n\n## Next\nBody\n"):
                path.write_text(text)
                with self.subTest(text=text), self.assertRaises(ValueError):
                    read_section(path, "## Same")


if __name__ == "__main__":
    unittest.main()
