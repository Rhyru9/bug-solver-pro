#!/usr/bin/env bash
# Find files that FREQUENTLY CHANGE TOGETHER with the target (a signal of hidden coupling / blast radius).
# Usage: scripts/co-change.sh <file> [commit_limit=200] [top=15]
set -euo pipefail

FILE="${1:-}"
LIMIT="${2:-200}"
TOP="${3:-15}"

if [ -z "$FILE" ]; then
  echo "Usage: $0 <file> [commit_count] [top]" >&2
  exit 1
fi

if ! [[ "$LIMIT" =~ ^[1-9][0-9]*$ && "$TOP" =~ ^[1-9][0-9]*$ ]]; then
  echo "commit_count and top must be positive integers." >&2
  exit 2
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a Git repository." >&2
  exit 1
fi

WORK_DIR=$(mktemp -d "${TMPDIR:-/tmp}/bug-solver-pro-cochange.XXXXXX")
trap 'rm -rf "$WORK_DIR"' EXIT

echo "=== Files most frequently changed alongside $FILE (among the last $LIMIT commits touching it) ==="
# tformat terminates the final commit line; format can leave it unread at EOF.
git --no-pager log --follow -n "$LIMIT" --pretty=tformat:'%H' -- "$FILE" > "$WORK_DIR/commits" </dev/null
: > "$WORK_DIR/files"
while IFS= read -r commit; do
  git --no-pager show --pretty=format: --name-only "$commit" >> "$WORK_DIR/files" </dev/null
done < "$WORK_DIR/commits"

# Read the target as a literal line instead of an awk variable with escape rules.
printf '%s\n' "$FILE" > "$WORK_DIR/target"
awk 'NR == FNR { target=$0; next } length($0) && $0 != target' "$WORK_DIR/target" "$WORK_DIR/files" \
  | sort | uniq -c | sort -rn | awk -v maximum="$TOP" 'NR <= maximum' > "$WORK_DIR/result"
if [ -s "$WORK_DIR/result" ]; then cat "$WORK_DIR/result"; else echo "(none)"; fi

echo
echo "Interpretation: high counts suggest possible logic/contract coupling with $FILE."
echo "Review these files during impact analysis (templates/impact-analysis.md), even if searches did not find them."
echo "Limits: line-based Git paths and prior names across renames need manual review; co-change is not proof of coupling."
