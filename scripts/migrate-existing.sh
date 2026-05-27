#!/usr/bin/env bash
# migrate-existing.sh — copy จาก ~/.claude/skills/ เข้า 9arm-skills
# Usage: bash scripts/migrate-existing.sh

set -e
SKILLS_ROOT=~/9arm-skills/skills
SOURCE=~/.claude/skills   # adjust if different

migrate() {
  local skill="$1" cat="$2"
  local src="$SOURCE/$skill"
  local dst="$SKILLS_ROOT/$cat/$skill"
  if [ -d "$src" ]; then
    cp -r "$src" "$dst" && echo "✅ $cat/$skill"
  else
    echo "⚠️  not found: $skill"
  fi
}

# engineering
migrate tdd             engineering
migrate code-review     engineering
migrate error-handling  engineering
migrate security-review engineering
migrate search-first    engineering

# productivity
migrate git-workflow                  productivity
migrate grill-me                      productivity
migrate write-a-prd                   productivity
migrate strategic-compact             productivity
migrate improve-codebase-architecture productivity
migrate verification-loop             productivity

# ai-agent
migrate prompt-engineer ai-agent
migrate agentic-eval    ai-agent

# personal
migrate continuous-learning personal
migrate document-skill      personal

echo ""
echo "Done. Run scripts/token-audit.sh to verify."
