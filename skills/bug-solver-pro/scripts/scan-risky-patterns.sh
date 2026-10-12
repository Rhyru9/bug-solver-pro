#!/usr/bin/env bash
# List candidate LOCATIONS for manual inspection during bug investigation.
# This is a simple text search, not proof of bugs; it can miss cases (false negatives) or be noisy (false positives).
# Patterns spanning multiple lines are not detected.
# Usage: scripts/scan-risky-patterns.sh [directory=.]
set -euo pipefail

DIR="${1:-.}"
MAX=30

if [ ! -d "$DIR" ]; then
  echo "Search directory does not exist: $DIR" >&2
  exit 2
fi

if command -v timeout >/dev/null 2>&1; then
  TIMEOUT_CMD=timeout
elif command -v gtimeout >/dev/null 2>&1; then
  TIMEOUT_CMD=gtimeout
else
  echo "This optional helper requires timeout or gtimeout. Use IDE search or scripts/search.py for catalog guidance instead." >&2
  exit 2
fi

search() {
  # $1 = regex pattern (ERE). Output: file:line:text
  if command -v rg >/dev/null 2>&1; then
    "$TIMEOUT_CMD" 30 rg -n --hidden --glob '!.git' --glob '!node_modules' --glob '!vendor' \
      --glob '!dist' --glob '!build' --glob '!*.lock' --glob '!*.min.*' -e "$1" "$DIR" </dev/null
  else
    "$TIMEOUT_CMD" 30 grep -rnIE --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=vendor \
      --exclude-dir=dist --exclude-dir=build --exclude='*.lock' --exclude='*.min.*' -e "$1" "$DIR" </dev/null
  fi
}

section() {
  local title="$1" pattern="$2" out status
  echo
  echo "=== $title ==="
  if out=$(search "$pattern" | head -n "$MAX"); then
    status=0
  else
    status=$?
  fi
  # 1 means no matches; 141 is SIGPIPE after head has collected enough matches.
  if [ "$status" -ne 0 ] && [ "$status" -ne 1 ] && [ "$status" -ne 141 ]; then
    echo "Search failed for '$title' (status $status); empty output is not evidence of no matches." >&2
    return 2
  fi
  if [ -z "$out" ]; then echo "(none)"; else echo "$out"; fi
}

section "Empty single-line catch/except blocks (swallowed errors)" \
  'catch\s*(\([^)]*\))?\s*\{\s*\}|except[^:]*:\s*pass'

section "Patch markers (TODO/FIXME/HACK/workaround)" \
  'TODO|FIXME|HACK|XXX|workaround|temporary fix|quick fix'

section "Delay/sleep (using delays to 'solve' races is not a fix)" \
  'sleep\(|time\.Sleep|Thread\.sleep|usleep\(|setTimeout\('

section "forEach(async ...) (iterations are not awaited)" \
  'forEach\(\s*(async|\w+\s*=>\s*\{?\s*await)'

section "Transaction locations (inspect external effects inside them: email, HTTP, job dispatch)" \
  'transaction\(|@Transactional|\.begin\(|BEGIN;|atomic\('

section "Cache writes (inspect invalidation across write paths and TTLs)" \
  'cache\.(set|put)|Cache::(put|remember|forever)|redis\.(set|setex)|\.setex\('

section "Raw queries (bypassing ORM soft-delete/tenant scopes)" \
  'DB::raw|DB::select|executeRaw|queryRaw|\.raw\(|\.execute\(\s*f?["'"'"']'

section "Disabled safeguards (skipped tests, ignored lint/types)" \
  '\.skip\(|\bxit\(|@Ignore|pytest\.mark\.skip|eslint-disable|@ts-ignore|@ts-nocheck|# noqa|nolint'

echo
echo "Done. Each line is only a candidate; inspect context before drawing conclusions."
