#!/usr/bin/env bash
set -euo pipefail

# Links all shippable skills to ~/.gemini/config/skills/ so the Antigravity CLI (agy)
# discovers them — same source as link-skills.sh (which serves Claude Code).
# Skips: personal/, in-progress/, deprecated/
# Also mirrors real (non-symlink) skill dirs from ~/.claude/skills (docx, pdf, ...).
# Only touches symlinks it owns; never deletes a real dir it did not create.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.gemini/config/skills"
CLAUDE_SKILLS="$HOME/.claude/skills"

mkdir -p "$DEST"

link() {
  local src="$1" name target
  name="$(basename "$src")"
  target="$DEST/$name"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    echo "skip $name (real dir already in $DEST)" >&2
    return
  fi
  ln -sfn "$src" "$target"
  echo "linked $name -> $src"
}

find -L "$REPO/skills" -name SKILL.md \
  -not -path '*/node_modules/*' \
  -not -path '*/deprecated/*' \
  -not -path '*/in-progress/*' \
  -not -path '*/personal/*' \
  -print0 |
while IFS= read -r -d '' skill_md; do
  link "$(dirname "$skill_md")"
done

if [ -d "$CLAUDE_SKILLS" ]; then
  for d in "$CLAUDE_SKILLS"/*/; do
    d="${d%/}"
    [ -L "$d" ] && continue
    [ -f "$d/SKILL.md" ] || continue
    link "$d"
  done
fi

# Drop dangling links (skill removed/renamed upstream)
find "$DEST" -maxdepth 1 -type l ! -exec test -e {} \; -print -delete | sed 's/^/pruned /'

echo ""
echo "✅ Done. Skills linked to $DEST (run /skills reload inside agy)"
