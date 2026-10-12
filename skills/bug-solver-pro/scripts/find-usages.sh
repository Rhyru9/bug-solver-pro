#!/usr/bin/env bash
# Find symbol usages (functions, classes, fields, event names, route names, table/column names).
# Usage: scripts/find-usages.sh <symbol> [directory=.]
# Shows direct usages and possible indirect usages (strings/config/tests/migrations).
set -euo pipefail

SYMBOL="${1:-}"
DIR="${2:-.}"

if [ -z "$SYMBOL" ]; then
  echo "Usage: $0 <symbol> [directory]" >&2
  exit 1
fi

if [ ! -d "$DIR" ]; then
  echo "Search directory does not exist: $DIR" >&2
  exit 2
fi

WORK_DIR=$(mktemp -d "${TMPDIR:-/tmp}/bug-solver-pro-usages.XXXXXX")
trap 'rm -rf "$WORK_DIR"' EXIT

if command -v rg >/dev/null 2>&1; then
  SEARCH() {
    rg -n --glob '!.git' --glob '!node_modules' --glob '!vendor' --glob '!dist' --glob '!build' \
      --glob '!.venv' --glob '!venv' --glob '!.ssh' --glob '!.aws' \
      --glob '!.env' --glob '!.env.*' --glob '!*.pem' --glob '!*.p12' --glob '!id_rsa' --glob '!id_rsa.*' \
      --glob '!*secret*' --glob '!*credential*' --glob '!.netrc' --glob '!.npmrc' --glob '!*.lock' "$@"
  }
else
  SEARCH() {
    grep -rnI --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=vendor --exclude-dir=dist \
      --exclude-dir=build --exclude-dir=.venv --exclude-dir=venv --exclude-dir=.ssh --exclude-dir=.aws \
      --exclude='.env' --exclude='.env.*' --exclude='*.pem' --exclude='*.p12' --exclude='id_rsa' \
      --exclude='*secret*' --exclude='*credential*' --exclude='.netrc' --exclude='.npmrc' "$@"
  }
fi

# 1 means no match. Other failures must not be turned into '(none)'.
capture_search() {
  local output="$1" status
  shift
  if SEARCH "$@" > "$output"; then
    return 0
  else
    status=$?
  fi
  if [ "$status" -eq 1 ]; then
    return 0
  fi
  echo "Usage search failed (status $status); no reliable result is available." >&2
  return 2
}

display_result() {
  if [ -s "$1" ]; then cat "$1"; else echo "(none)"; fi
}

filter_result() {
  local pattern="$1" output="$2" status
  if grep -Ei "$pattern" "$WORK_DIR/all" > "$output"; then
    return 0
  else
    status=$?
  fi
  if [ "$status" -eq 1 ]; then return 0; fi
  echo "Usage result filtering failed (status $status)." >&2
  return 2
}

echo "=== Direct usages: $SYMBOL ==="
capture_search "$WORK_DIR/direct" -F -w -- "$SYMBOL" "$DIR"
display_result "$WORK_DIR/direct"

# Naming variants (snake_case, camelCase, kebab-case, PascalCase) may appear across layers.
snake=$(echo "$SYMBOL" | sed -E 's/([a-z0-9])([A-Z])/\1_\2/g' | tr '[:upper:]' '[:lower:]' | tr '-' '_')
kebab=$(echo "$snake" | tr '_' '-')
camel=$(echo "$snake" | awk -F_ '{out=$1; for(i=2;i<=NF;i++){out=out toupper(substr($i,1,1)) substr($i,2)}; print out}')

for variant in "$snake" "$kebab" "$camel"; do
  if [ "$variant" != "$SYMBOL" ] && [ -n "$variant" ]; then
    echo
    echo "=== Naming variant: $variant ==="
    capture_search "$WORK_DIR/variant" -F -w -- "$variant" "$DIR"
    display_result "$WORK_DIR/variant"
  fi
done

capture_search "$WORK_DIR/all" -F -i -- "$SYMBOL" "$DIR"

echo
echo "=== Tests mentioning the symbol ==="
filter_result '(test|spec|__tests__|fixture)' "$WORK_DIR/tests"
display_result "$WORK_DIR/tests"

echo
echo "=== Migrations / seeders / configuration / documentation mentioning the symbol ==="
filter_result '(migrat|seed|config|\.env|\.ya?ml|\.json|\.md|openapi|swagger)' "$WORK_DIR/related"
display_result "$WORK_DIR/related"

echo
echo "NOTE: indirect usages (reflection, dynamic strings, DI, raw queries, templates, external consumers)"
echo "may be missed. Inspect access logs/metrics and consult consumer owners when contracts are involved."
