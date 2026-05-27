#!/bin/bash
# install-superpowers.sh — git subtree + symlinks
set -e

cd ~/9arm-skills

git remote add superpowers https://github.com/obra/superpowers.git 2>/dev/null || true
git fetch superpowers
git subtree add --prefix=upstream/superpowers superpowers main --squash

SKILLS=~/9arm-skills/skills
UP=~/9arm-skills/upstream/superpowers/skills

ln -sf "$UP/subagent-driven-development"    "$SKILLS/ai-agent/subagent-driven-development"
ln -sf "$UP/dispatching-parallel-agents"    "$SKILLS/ai-agent/dispatching-parallel-agents"
ln -sf "$UP/executing-plans"                "$SKILLS/productivity/executing-plans"
ln -sf "$UP/verification-before-completion" "$SKILLS/engineering/verification-before-completion"
ln -sf "$UP/using-git-worktrees"            "$SKILLS/productivity/using-git-worktrees"
ln -sf "$UP/finishing-a-development-branch" "$SKILLS/productivity/finishing-a-development-branch"
ln -sf "$UP/receiving-code-review"          "$SKILLS/engineering/receiving-code-review"
ln -sf "$UP/writing-skills"                 "$SKILLS/meta/writing-skills"
# writing-plans lives inside superpowers differently — copy directly
cp -r "$UP/writing-plans" "$SKILLS/productivity/writing-plans" 2>/dev/null || \
  ln -sf "$UP/writing-plans" "$SKILLS/productivity/writing-plans"

echo "✅ Superpowers installed"
echo "Update later: git subtree pull --prefix=upstream/superpowers superpowers main --squash"
