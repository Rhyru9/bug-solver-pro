#!/usr/bin/env python3
"""Validate bundled diagnostic records and their source reference paths."""

import sys
from core import DOMAINS, load_angles, load_catalog


def main():
    try:
        rows = load_catalog()
        axes = load_angles()
    except (OSError, ValueError) as error:
        print(f"Invalid catalog: {error}", file=sys.stderr)
        return 1
    domains = sorted({row["domain"] for row in rows})
    missing = sorted(set(DOMAINS) - set(domains))
    if missing:
        print(f"Catalog has no records for declared domains: {', '.join(missing)}", file=sys.stderr)
        return 1
    print(f"Valid: {len(rows)} heuristic patterns across {len(domains)} domains; {len(axes)} exploration angles; all references resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
