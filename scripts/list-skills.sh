#!/usr/bin/env bash
# list-skills.sh — list all skills with description from frontmatter

SKILLS_ROOT=~/9arm-skills/skills
echo "=== 9arm-skills Library ==="
echo ""

find "$SKILLS_ROOT" -name "SKILL.md" | sort | while read f; do
  rel="${f#$SKILLS_ROOT/}"
  name="${rel%/SKILL.md}"
  # Extract description from frontmatter
  desc=$(grep -m1 "^description:" "$f" 2>/dev/null | sed 's/^description: *//' | sed "s/^'//" | sed "s/'$//" | sed 's/^"//' | sed 's/"$//' || echo "—")
  tier=$(grep -m1 "^tier:" "$f" 2>/dev/null | sed 's/^tier: *//' || echo "?")
  printf "  %-48s  tier:%-2s  %s\n" "$name" "$tier" "$desc"
done

echo ""
echo "Total skills: $(find "$SKILLS_ROOT" -name "SKILL.md" | wc -l | tr -d ' ')"
