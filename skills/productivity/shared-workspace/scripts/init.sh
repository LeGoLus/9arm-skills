#!/usr/bin/env bash
# Create the shared-workspace files a folder is missing. Never overwrites anything.
#   bash init.sh <folder>
set -euo pipefail
dir="${1:?usage: init.sh <folder>}"
tpl="$(cd "$(dirname "$0")/../templates" && pwd)"
[ -d "$dir" ] || { echo "no such folder: $dir" >&2; exit 1; }
mkdir -p "$dir/.agents"

place() {   # place <template> <target>
  if [ -e "$2" ]; then echo "kept     $2"; else cp "$tpl/$1" "$2"; echo "created  $2"; fi
}
place AGENTS.md   "$dir/AGENTS.md"
place LOG.md      "$dir/.agents/LOG.md"
place HANDOFF.md  "$dir/.agents/HANDOFF.md"
if [ -e "$dir/CLAUDE.md" ]; then
  if grep -q '^@AGENTS.md' "$dir/CLAUDE.md"; then
    echo "kept     $dir/CLAUDE.md (imports AGENTS.md)"
  else
    echo "NOTE     $dir/CLAUDE.md exists without @AGENTS.md: move shared rules into AGENTS.md (ask the user), then add '@AGENTS.md' as its first line"
  fi
else
  place CLAUDE.md "$dir/CLAUDE.md"
fi
