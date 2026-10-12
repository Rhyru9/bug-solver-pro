#!/usr/bin/env python3
"""Build local standalone-skill and Claude-plugin ZIPs; never publish or tag."""

import argparse
from pathlib import Path
import sys
import zipfile

from check_package import ROOT, check_package


def resource_files(directory):
    for path in sorted(directory.rglob("*")):
        if "__pycache__" not in path.parts and path.suffix != ".pyc" and path.name != ".DS_Store" and path.is_file():
            yield path


def build_release(output_dir, root=ROOT):
    root = Path(root).resolve()
    package = check_package(root)
    output = Path(output_dir).resolve()
    skill = root / "skills/bug-solver-pro"
    if output.is_relative_to(skill) or output.is_relative_to(root / ".claude-plugin"):
        raise ValueError("Output directory must be outside the bundled skill and plugin metadata")
    files = list(resource_files(skill))
    plugin_files = files + list(resource_files(root / ".claude-plugin"))
    plugin_files += [root / "LICENSE", root / "README.md", root / "COMPATIBILITY.md"]
    # README's maintainer-guide link remains valid in the plugin artifact.
    plugin_files += [root / ".github/CONTRIBUTING.md"]
    archives = [output / f"bug-solver-pro-skill-v{package['version']}.zip",
                output / f"bug-solver-pro-plugin-v{package['version']}.zip"]
    if any(archive.exists() for archive in archives):
        raise ValueError("Release artifacts already exist; use a new output directory")
    output.mkdir(parents=True, exist_ok=True)
    for archive, members, base in ((archives[0], files, skill.parent), (archives[1], plugin_files, root)):
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as bundle:
            for member in members:
                bundle.write(member, member.relative_to(base).as_posix())
    return archives


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, help="Explicit destination for new ZIP files")
    args = parser.parse_args()
    try:
        archives = build_release(args.output_dir)
    except (OSError, ValueError, TypeError) as error:
        print(f"Release build failed: {error}", file=sys.stderr)
        return 1
    for archive in archives:
        print(archive)
    return 0


if __name__ == "__main__":
    sys.exit(main())
