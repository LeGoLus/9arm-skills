#!/usr/bin/env bash
# init-project.sh — scaffold CLAUDE.md for new project
# Usage: bash scripts/init-project.sh <project-path> <type>
# Types: engineering | ai-agent | hermes | planning | full

set -e
PROJECT_PATH=${1:-.}
TYPE=${2:-engineering}
SKILLS_BASE=~/9arm-skills/skills

skill_path() {
  local skill="$1"
  case "$skill" in
    systematic-debugging)        echo "engineering/systematic-debugging" ;;
    git-workflow)                echo "productivity/git-workflow" ;;
    grill-me)                    echo "productivity/grill-me" ;;
    grill-with-docs)             echo "productivity/grill-with-docs" ;;
    tdd)                         echo "engineering/tdd" ;;
    code-review)                 echo "engineering/code-review" ;;
    error-handling)              echo "engineering/error-handling" ;;
    verification-before-completion) echo "engineering/verification-before-completion" ;;
    writing-plans)               echo "productivity/writing-plans" ;;
    executing-plans)             echo "productivity/executing-plans" ;;
    strategic-compact)           echo "productivity/strategic-compact" ;;
    verification-loop)           echo "productivity/verification-loop" ;;
    security-review)             echo "engineering/security-review" ;;
    subagent-driven-development) echo "ai-agent/subagent-driven-development" ;;
    dispatching-parallel-agents) echo "ai-agent/dispatching-parallel-agents" ;;
    prompt-engineer)             echo "ai-agent/prompt-engineer" ;;
    agentic-eval)                echo "ai-agent/agentic-eval" ;;
    continuous-learning)         echo "ai-agent/continuous-learning" ;;
    write-a-prd)                 echo "productivity/write-a-prd" ;;
    improve-arch)                echo "productivity/improve-codebase-architecture" ;;
    document-skill)              echo "personal/document-skill" ;;
    *)                           echo "unknown/$skill" ;;
  esac
}

ALL_SKILLS="systematic-debugging git-workflow grill-me grill-with-docs tdd code-review error-handling verification-before-completion writing-plans executing-plans strategic-compact verification-loop security-review subagent-driven-development dispatching-parallel-agents prompt-engineer agentic-eval continuous-learning write-a-prd improve-arch document-skill"

case $TYPE in
  engineering)
    ACTIVE="systematic-debugging git-workflow grill-me grill-with-docs tdd code-review error-handling verification-before-completion writing-plans strategic-compact"
    BUDGET="~9,500 tokens"
    ;;
  ai-agent)
    ACTIVE="systematic-debugging git-workflow grill-me grill-with-docs tdd prompt-engineer agentic-eval continuous-learning subagent-driven-development dispatching-parallel-agents security-review"
    BUDGET="~13,000 tokens"
    ;;
  hermes)
    ACTIVE="systematic-debugging git-workflow grill-with-docs subagent-driven-development dispatching-parallel-agents prompt-engineer agentic-eval"
    BUDGET="~9,000 tokens"
    ;;
  planning)
    ACTIVE="systematic-debugging git-workflow grill-me grill-with-docs write-a-prd writing-plans"
    BUDGET="~4,500 tokens"
    ;;
  full)
    ACTIVE="systematic-debugging git-workflow grill-me grill-with-docs tdd code-review error-handling security-review verification-before-completion writing-plans executing-plans prompt-engineer agentic-eval subagent-driven-development dispatching-parallel-agents strategic-compact continuous-learning"
    BUDGET="~20,000 tokens (use sparingly)"
    ;;
  *)
    echo "Unknown type: $TYPE"
    echo "Valid: engineering | ai-agent | hermes | planning | full"
    exit 1
    ;;
esac

SKILL_LIST=""
for skill in $ACTIVE; do
  SKILL_LIST="${SKILL_LIST}
- $SKILLS_BASE/$(skill_path $skill)/SKILL.md"
done

INACTIVE_LIST=""
for skill in $ALL_SKILLS; do
  if ! echo "$ACTIVE" | grep -qw "$skill"; then
    INACTIVE_LIST="${INACTIVE_LIST}
- $skill → $SKILLS_BASE/$(skill_path $skill)/SKILL.md"
  fi
done

PLANNING_RULE="greenfield → grill-me | existing code → grill-with-docs (updates CONTEXT.md)"
PROJECT_NAME=$(basename "$PROJECT_PATH")

cat > "$PROJECT_PATH/CLAUDE.md" << EOF
# $PROJECT_NAME
> type: $TYPE | created: $(date +%Y-%m-%d) | budget: $BUDGET

## Active Skills
$SKILL_LIST

## Planning Protocol (auto-select)
$PLANNING_RULE

## Debug Protocol
ALWAYS: systematic-debugging 4 phases — no skipping.
AFTER FIX: verification-before-completion before marking done.

## Development Flow
1. grill-with-docs / grill-me → shared understanding
2. writing-plans → 2-5 min tasks with exact file paths
3. tdd → RED-GREEN-REFACTOR (delete code written before test)
4. verification-before-completion → verify fix passes
5. code-review → pre-merge checklist
6. git-workflow → conventional commit

## Repo Context
- Skills:     ~/9arm-skills/
- Knowledge:  ~/LifeVault/10-Projects/$PROJECT_NAME/
- Sources:    ~/NotebooksLM/$PROJECT_NAME/
- Domain:     $PROJECT_NAME/CONTEXT.md  ← created by grill-with-docs

## Do NOT Load (token save)
$INACTIVE_LIST
EOF

echo "✅ CLAUDE.md → $PROJECT_PATH/CLAUDE.md"
echo "📊 Token budget: $BUDGET"
echo "🎯 Profile: $TYPE"
