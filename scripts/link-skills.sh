#!/usr/bin/env bash
# link-skills.sh — create symlinks from ~/.claude/skills/ to 9arm-skills
# Usage: bash scripts/link-skills.sh

set -e
SKILLS_ROOT=~/9arm-skills/skills
CLAUDE_SKILLS=~/.claude/skills

echo "=== Linking 9arm-skills → ~/.claude/skills/ ==="

find "$SKILLS_ROOT" -name "SKILL.md" | while read f; do
  dir=$(dirname "$f")
  skill=$(basename "$dir")
  link="$CLAUDE_SKILLS/$skill"
  if [ ! -e "$link" ]; then
    ln -sf "$dir" "$link" && echo "✅ linked: $skill"
  else
    echo "⏭️  exists: $skill"
  fi
done

echo "Done."
