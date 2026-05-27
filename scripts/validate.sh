#!/usr/bin/env bash
# validate.sh — verify full setup is correct

PASS=0; FAIL=0
check() {
  if eval "$2"; then echo "✅ $1"; PASS=$((PASS+1))
  else echo "❌ $1"; FAIL=$((FAIL+1)); fi
}

echo "=== Tier 0 Skills ==="
check "systematic-debugging" "[ -f ~/9arm-skills/skills/engineering/systematic-debugging/SKILL.md ]"
check "git-workflow"         "[ -f ~/9arm-skills/skills/productivity/git-workflow/SKILL.md ]"
check "grill-me"             "[ -f ~/9arm-skills/skills/productivity/grill-me/SKILL.md ]"
check "grill-with-docs"      "[ -f ~/9arm-skills/skills/productivity/grill-with-docs/SKILL.md ]"

echo ""
echo "=== Superpowers Skills ==="
check "subagent-driven-development"    "[ -e ~/9arm-skills/skills/ai-agent/subagent-driven-development ]"
check "dispatching-parallel-agents"    "[ -e ~/9arm-skills/skills/ai-agent/dispatching-parallel-agents ]"
check "verification-before-completion" "[ -e ~/9arm-skills/skills/engineering/verification-before-completion ]"
check "writing-plans"                  "[ -e ~/9arm-skills/skills/productivity/writing-plans ]"
check "executing-plans"                "[ -e ~/9arm-skills/skills/productivity/executing-plans ]"
check "using-git-worktrees"            "[ -e ~/9arm-skills/skills/productivity/using-git-worktrees ]"
check "finishing-a-development-branch" "[ -e ~/9arm-skills/skills/productivity/finishing-a-development-branch ]"
check "receiving-code-review"          "[ -e ~/9arm-skills/skills/engineering/receiving-code-review ]"
check "writing-skills"                 "[ -e ~/9arm-skills/skills/meta/writing-skills ]"

echo ""
echo "=== Config Files ==="
check "~/CLAUDE.md (global)"       "[ -f ~/CLAUDE.md ]"
check "tier-manifest.yaml"         "[ -f ~/9arm-skills/tier-manifest.yaml ]"
check "init-project.sh executable" "[ -x ~/9arm-skills/scripts/init-project.sh ]"
check "token-audit.sh executable"  "[ -x ~/9arm-skills/scripts/token-audit.sh ]"
check "validate.sh executable"     "[ -x ~/9arm-skills/scripts/validate.sh ]"

echo ""
echo "=== Hermes MCP Files ==="
check "claude_code_tool.py"  "[ -f ~/.hermes/tools/claude_code_tool.py ]"
check "claude_code_skill.py" "[ -f ~/.hermes/mcp_tools/claude_code_skill.py ]"

echo ""
echo "=== Test init-project.sh ==="
mkdir -p /tmp/test-proj
bash ~/9arm-skills/scripts/init-project.sh /tmp/test-proj hermes > /dev/null 2>&1
check "hermes CLAUDE.md generated" "[ -f /tmp/test-proj/CLAUDE.md ]"
rm -rf /tmp/test-proj

echo ""
echo "=== Result: $PASS passed, $FAIL failed ==="
[ $FAIL -eq 0 ] && echo "🎉 All checks passed — system ready!" || echo "⚠️  Fix failures above"
