#!/usr/bin/env bash
set -euo pipefail

# Creates expected folder structure.
# Default: moves extra root files into _trash/<timestamp>/
# Use --force-delete to delete extras permanently.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FORCE_DELETE="false"
if [[ "${1:-}" == "--force-delete" ]]; then
  FORCE_DELETE="true"
fi
cd "$ROOT"

ALLOWLIST=(
  ".git" ".gitignore" "README.md" "LICENSE"
  "projects" "scripts" "docs"
)

mkdir -p projects docs scripts
mkdir -p projects/p01-bill-organizer/{bill_organizer,tests,examples,output,data}

TRASH_DIR="_trash/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$TRASH_DIR"

found_extra="false"
shopt -s dotglob nullglob
for item in * .*; do
  [[ "$item" == "." || "$item" == ".." ]] && continue
  keep="false"
  for allowed in "${ALLOWLIST[@]}"; do
    [[ "$item" == "$allowed" ]] && keep="true" && break
  done

  if [[ "$keep" == "false" ]]; then
    found_extra="true"
    if [[ "$FORCE_DELETE" == "true" ]]; then
      rm -rf -- "$item"
      echo "Deleted extra: $item"
    else
      mv -- "$item" "$TRASH_DIR/"
      echo "Moved extra to $TRASH_DIR/: $item"
    fi
  fi
done
shopt -u dotglob nullglob

if [[ "$found_extra" == "false" ]]; then
  rmdir "$TRASH_DIR" 2>/dev/null || true
fi

chmod +x scripts/bootstrap_repo.sh
echo "✅ Repo structure ready."
