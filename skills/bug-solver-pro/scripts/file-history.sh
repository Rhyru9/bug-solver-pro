#!/usr/bin/env bash
# Inspect file history: change dates, authors, and commit messages.
# Usage: scripts/file-history.sh <file> [commit_count=15]
set -euo pipefail

FILE="${1:-}"
N="${2:-15}"

if [ -z "$FILE" ]; then
  echo "Usage: $0 <file> [commit_count]" >&2
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not inside a Git repository; history is unavailable." >&2
  exit 1
fi

# --no-pager: avoid interactive pagers. </dev/null: prevent Git from reading stdin.
G() { git --no-pager "$@" </dev/null; }

echo "=== Last $N commits touching $FILE ==="
G log --follow -n "$N" --date=short --pretty=format:'%h  %ad  %an  %s' -- "$FILE"
echo
echo
echo "=== Change statistics ==="
G log --follow -n "$N" --stat --pretty=format:'--- %h %s' -- "$FILE" | head -n 120
echo
echo "=== Contributors (commit counts) ==="
# Specify the revision (HEAD): otherwise git shortlog reads stdin when it is not a terminal.
G shortlog -sn HEAD -- "$FILE" | head -n 5
echo
echo "Follow-up commands:"
echo "  git blame -w -C -C -C $FILE          # line authors/dates (ignore whitespace and moved code)"
echo "  git log -S'<text>' -- $FILE          # when specific text was added/removed"
echo "  git log -p -n 3 -- $FILE             # recent commit diffs"
echo "  git bisect start && git bisect bad && git bisect good <commit>   # find the causal commit"
