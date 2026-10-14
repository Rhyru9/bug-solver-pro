"""Optional real-framework probe; ordinary repository checks do not install its dependencies."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

PROBE = Path(__file__).resolve().parents[1] / "skills/bug-solver-pro/scripts/probes/fastapi_response_filter.py"


class OptionalFrameworkRuntimeTests(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("fastapi"), "FastAPI not installed in this interpreter")
    def test_fastapi_output_contract_is_checked_at_the_serialized_response(self):
        result = subprocess.run([sys.executable, "-B", str(PROBE)],
                                capture_output=True, text=True, check=True, timeout=15)
        report = json.loads(result.stdout)
        self.assertEqual(report["kind"], "synthetic_runtime_probe")
        self.assertEqual(report["results"]["/normal"]["body"], {"id": 1})
        self.assertEqual(report["results"]["/explicit-output"]["body"], {"id": 1})
        self.assertEqual(report["results"]["/direct"]["body"],
                         {"id": 1, "internal_marker": "synthetic-only"})
        self.assertTrue(all(row["status"] == 200 for row in report["results"].values()))


class DataSemanticsRuntimeTests(unittest.TestCase):
    def test_sql_results_are_checked_against_entity_grain_and_explicit_null_policy(self):
        script = PROBE.with_name("sql_query_semantics.py")
        result = subprocess.run([sys.executable, "-B", str(script)],
                                capture_output=True, text=True, check=True, timeout=15)
        report = json.loads(result.stdout)
        self.assertEqual(report["join_grain"]["row_ids"], [1, 1, 1, 2, 3])
        self.assertEqual(report["join_grain"]["order_grain_sum"], 230)
        self.assertEqual(report["join_grain"]["naive_sum"], 430)
        self.assertEqual(report["join_grain"]["distinct_amount_sum"], 130)
        self.assertEqual(report["null_exclusion"]["not_in_with_null"], [])
        self.assertEqual(report["null_exclusion"]["not_in_empty_set"], [None, 1, 2])
        self.assertEqual(report["null_exclusion"]["explicit_non_null_identity_policy"], [1])


if __name__ == "__main__":
    unittest.main()
