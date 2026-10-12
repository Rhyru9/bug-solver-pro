"""Check metadata/license invariants and behavior after artifact extraction."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_release import build_release
from check_package import check_package


class PackagingTests(unittest.TestCase):
    def fixture(self, destination):
        root = Path(destination)
        for directory in ("skills", ".claude-plugin", ".github"):
            shutil.copytree(ROOT / directory, root / directory)
        for filename in ("LICENSE", "README.md", "COMPATIBILITY.md"):
            shutil.copy2(ROOT / filename, root / filename)
        return root

    def test_tag_must_match_manifest(self):
        version = check_package()["version"]
        self.assertEqual(check_package(tag=f"v{version}")["version"], version)
        with self.assertRaises(ValueError):
            check_package(tag="v999.0.0")

    def test_standalone_license_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            (root / "skills/bug-solver-pro/LICENSE").write_text("different license\n")
            with self.assertRaises(ValueError):
                check_package(root)

    def test_marketplace_source_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            manifest = root / ".claude-plugin/marketplace.json"
            data = json.loads(manifest.read_text())
            data["plugins"][0]["source"] = "./missing-plugin"
            manifest.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                check_package(root)

    def test_extracted_skill_and_plugin_execute_search(self):
        with tempfile.TemporaryDirectory(prefix="bug solver artifacts ") as directory:
            root = Path(directory)
            artifacts = build_release(root / "output")
            self.assertEqual(len(artifacts), 2)
            for index, artifact in enumerate(artifacts):
                extracted = root / f"extracted-{index}"
                with zipfile.ZipFile(artifact) as bundle:
                    self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in bundle.namelist()))
                    bundle.extractall(extracted)
                skill = extracted / ("bug-solver-pro" if index == 0 else "skills/bug-solver-pro")
                self.assertEqual((skill / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
                result = subprocess.run([sys.executable, "-B", str(skill / "scripts/search.py"),
                                         "webhook retry", "--plan", "--json"],
                                        cwd=root, capture_output=True, text=True, check=True)
                plan = json.loads(result.stdout)
                self.assertEqual(plan["results"][0]["id"], "duplicate-delivery")
                if index == 1:
                    plugin = json.loads((extracted / ".claude-plugin/plugin.json").read_text())
                    self.assertEqual(plugin["name"], "bug-solver-pro")

    def test_existing_artifacts_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            artifacts = build_release(directory)
            original = artifacts[0].read_bytes()
            with self.assertRaises(ValueError):
                build_release(directory)
            self.assertEqual(artifacts[0].read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
