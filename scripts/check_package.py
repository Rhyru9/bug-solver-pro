#!/usr/bin/env python3
"""Check repository packaging invariants using only the Python standard library."""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills/bug-solver-pro/scripts"))
from core import validate_angles, validate_catalog


def json_file(path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def check_package(root=ROOT, tag=None):
    root = Path(root).resolve()
    skill = root / "skills/bug-solver-pro"
    plugin = json_file(root / ".claude-plugin/plugin.json")
    marketplace = json_file(root / ".claude-plugin/marketplace.json")
    if plugin.get("name") != "bug-solver-pro" or plugin.get("license") != "MIT":
        raise ValueError("Plugin name or license does not match the package")
    version = plugin.get("version", "")
    if not isinstance(version, str) or not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?", version):
        raise ValueError("Plugin version must be a release version such as 1.0.0")
    if tag is not None and tag != f"v{version}":
        raise ValueError(f"Tag must match plugin version: v{version}")
    if marketplace.get("name") != "rhyru9-skills":
        raise ValueError("Unexpected marketplace name")
    if plugin.get("author", {}).get("name") != "Rhyru9" or marketplace.get("owner", {}).get("name") != "Rhyru9":
        raise ValueError("Plugin author and marketplace owner must be Rhyru9")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        raise ValueError("Marketplace must contain the one canonical plugin")
    if entries[0].get("name") != plugin["name"] or entries[0].get("source") != "./":
        raise ValueError("Marketplace entry must resolve to this root plugin")
    if "skills" in plugin or "skills" in entries[0]:
        raise ValueError("This package uses the default root skills/ discovery layout")
    license_text = (root / "LICENSE").read_bytes()
    if license_text != (skill / "LICENSE").read_bytes():
        raise ValueError("Root and bundled MIT licenses differ")
    if b"MIT License" not in license_text or b"Rhyru9" not in license_text:
        raise ValueError("MIT license or copyright owner is missing")
    entrypoint = (skill / "SKILL.md").read_text(encoding="utf-8")
    if not entrypoint.startswith("---\n"):
        raise ValueError("Skill frontmatter is missing")
    parts = entrypoint.split("---", 2)
    if len(parts) != 3:
        raise ValueError("Skill frontmatter is unterminated")
    # Check the simple scalar metadata authored in this repository, not general YAML.
    metadata = dict(line.split(":", 1) for line in parts[1].splitlines() if ":" in line)
    metadata = {key.strip(): value.strip() for key, value in metadata.items()}
    if metadata.get("name") != plugin["name"] or metadata.get("license") != "MIT":
        raise ValueError("Skill name/license disagree with plugin metadata")
    if not 1 <= len(metadata.get("description", "")) <= 1024:
        raise ValueError("Skill description must contain 1–1024 characters")
    patterns = validate_catalog(json_file(skill / "data/patterns.json"), root=skill)
    axes = validate_angles(json_file(skill / "data/angles.json"), root=skill)
    documents = [root / "README.md", root / "COMPATIBILITY.md"]
    documents += list(skill.rglob("*.md")) + list((root / ".github").rglob("*.md"))
    for document in documents:
        content = document.read_text(encoding="utf-8")
        if content.count("```") % 2:
            raise ValueError(f"Unclosed code fence: {document.relative_to(root)}")
        # Exclude fenced examples from Markdown link discovery.
        prose = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        for target in re.findall(r"\]\(([^)]+)\)", prose):
            target = target.strip().strip("<>")
            if urlsplit(target).scheme or target.startswith("#"):
                continue
            path = unquote(target.split("#", 1)[0])
            if not (document.parent / path).exists():
                raise ValueError(f"Broken link in {document.relative_to(root)}: {target}")
    for path in skill.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Canonical skill must not depend on symlinked resources: {path}")
    return {"version": version, "patterns": len(patterns), "angles": len(axes), "documents": len(documents)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", help="Require an existing release tag value to match the plugin version")
    args = parser.parse_args()
    try:
        result = check_package(tag=args.tag)
    except (OSError, ValueError, TypeError) as error:
        print(f"Package check failed: {error}", file=sys.stderr)
        return 1
    print(f"Package valid: v{result['version']}; {result['patterns']} patterns; {result['angles']} angles; {result['documents']} documents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
