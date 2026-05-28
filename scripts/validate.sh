#!/usr/bin/env bash
# validate.sh — verify full 9arm-skills setup is correct
# Usage: bash ~/9arm-skills/scripts/validate.sh

PASS=0; FAIL=0
ok()   { echo "✅ $1"; PASS=$((PASS+1)); }
fail() { echo "❌ $1"; FAIL=$((FAIL+1)); }
check() { eval "$2" && ok "$1" || fail "$1"; }

echo "=== 1. Tier 0 Skills ==="
check "systematic-debugging" "[ -f ~/9arm-skills/skills/engineering/systematic-debugging/SKILL.md ]"
check "git-workflow"         "[ -f ~/9arm-skills/skills/productivity/git-workflow/SKILL.md ]"
check "grill-me"             "[ -f ~/9arm-skills/skills/productivity/grill-me/SKILL.md ]"
check "grill-with-docs"      "[ -f ~/9arm-skills/skills/productivity/grill-with-docs/SKILL.md ]"

echo ""
echo "=== 2. New Skills (post-mortem, scrutinize, management-talk) ==="
check "post-mortem"     "[ -f ~/9arm-skills/skills/engineering/post-mortem/SKILL.md ]"
check "scrutinize"      "[ -f ~/9arm-skills/skills/engineering/scrutinize/SKILL.md ]"
check "management-talk" "[ -f ~/9arm-skills/skills/productivity/management-talk/SKILL.md ]"

echo ""
echo "=== 3. Superpowers Skills ==="
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
echo "=== 4. Config Files ==="
check "~/CLAUDE.md (global)"       "[ -f ~/CLAUDE.md ]"
check "tier-manifest.yaml"         "[ -f ~/9arm-skills/tier-manifest.yaml ]"
check "catalog.json"               "[ -f ~/9arm-skills/catalog.json ]"
check "init-project.sh executable" "[ -x ~/9arm-skills/scripts/init-project.sh ]"
check "link-skills.sh executable"  "[ -x ~/9arm-skills/scripts/link-skills.sh ]"
check "validate.sh executable"     "[ -x ~/9arm-skills/scripts/validate.sh ]"
check "token-audit.sh executable"  "[ -x ~/9arm-skills/scripts/token-audit.sh ]"

echo ""
echo "=== 5. Hermes MCP Tools ==="
check "claude_code_tool.py"  "[ -f ~/.hermes/tools/claude_code_tool.py ]"
check "claude_code_skill.py" "[ -f ~/.hermes/mcp_tools/claude_code_skill.py ]"

echo ""
echo "=== 6. LifeVault Folders ==="
for folder in "00-Inbox" "10-Projects" "20-Areas" "30-Resources" "40-Archive" "90-Templates"; do
  check "LifeVault/$folder" "[ -d ~/LifeVault/$folder ]"
done

echo ""
echo "=== 7. Project CLAUDE.md Files ==="
check ".hermes/CLAUDE.md"                                    "[ -f ~/.hermes/CLAUDE.md ]"
check "awoms-app/CLAUDE.md"                                  "[ -f ~/Documents/Andaman/AWOMS/awoms-app/CLAUDE.md ]"

echo ""
echo "=== 8. Smoke Test init-project.sh ==="
mkdir -p /tmp/test-proj
bash ~/9arm-skills/scripts/init-project.sh /tmp/test-proj hermes > /dev/null 2>&1
check "hermes profile generates CLAUDE.md" "[ -f /tmp/test-proj/CLAUDE.md ]"
rm -rf /tmp/test-proj

echo ""
echo "══════════════════════════════════"
echo "  Result: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ] && echo "  🎉 System ready!" || echo "  ⚠️  Fix failures above first"
echo "══════════════════════════════════"
