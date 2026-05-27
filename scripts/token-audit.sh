#!/usr/bin/env bash
# token-audit.sh — token cost of every skill

SKILLS_ROOT=~/9arm-skills/skills
echo "=== 9arm-skills Token Audit ==="
echo ""

find "$SKILLS_ROOT" -name "SKILL.md" | sort | while read f; do
  rel="${f#$SKILLS_ROOT/}"
  name="${rel%/SKILL.md}"
  chars=$(wc -c < "$f")
  tokens=$((chars / 4))
  if   [ $tokens -gt 1500 ]; then flag="🔴 HEAVY"
  elif [ $tokens -gt 800  ]; then flag="🟡 medium"
  else                             flag="🟢 light"
  fi
  printf "%-50s %5d t  %s\n" "$name" "$tokens" "$flag"
done

echo ""
echo "── Tier 0 always loaded ─────────────────"
t0=0
for s in "engineering/systematic-debugging" "productivity/git-workflow" \
         "productivity/grill-me" "productivity/grill-with-docs"; do
  f="$SKILLS_ROOT/$s/SKILL.md"
  [ -f "$f" ] && t0=$((t0 + $(wc -c < "$f") / 4))
done
echo "~${t0} tokens on EVERY project"
