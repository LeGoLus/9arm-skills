#!/usr/bin/env bash
# init-project.sh — scaffold CLAUDE.md for a new project
# Skills reference ~/.claude/skills/ (symlinked from ~/9arm-skills, sourced from GitHub)
# Usage: bash scripts/init-project.sh <project-path> <type>
# Types: engineering | ai-agent | hermes | planning | full

set -e
PROJECT_PATH=${1:-.}
TYPE=${2:-engineering}
SKILLS_BASE=~/.claude/skills   # runtime path — symlinked from ~/9arm-skills

skill_path() {
  case "$1" in
    systematic-debugging)        echo "systematic-debugging" ;;
    git-workflow)                echo "git-workflow" ;;
    grill-me)                    echo "grill-me" ;;
    grill-with-docs)             echo "grill-with-docs" ;;
    tdd)                         echo "tdd" ;;
    code-review)                 echo "code-review" ;;
    error-handling)              echo "error-handling" ;;
    verification-before-completion) echo "verification-before-completion" ;;
    writing-plans)               echo "writing-plans" ;;
    executing-plans)             echo "executing-plans" ;;
    strategic-compact)           echo "strategic-compact" ;;
    verification-loop)           echo "verification-loop" ;;
    security-review)             echo "security-review" ;;
    subagent-driven-development) echo "subagent-driven-development" ;;
    dispatching-parallel-agents) echo "dispatching-parallel-agents" ;;
    prompt-engineer)             echo "prompt-engineer" ;;
    agentic-eval)                echo "agentic-eval" ;;
    continuous-learning)         echo "continuous-learning" ;;
    post-mortem)                 echo "post-mortem" ;;
    scrutinize)                  echo "scrutinize" ;;
    management-talk)             echo "management-talk" ;;
    write-a-prd)                 echo "write-a-prd" ;;
    improve-arch)                echo "improve-codebase-architecture" ;;
    document-skill)              echo "document-skill" ;;
    *)                           echo "$1" ;;
  esac
}

ALL_SKILLS="systematic-debugging git-workflow grill-me grill-with-docs tdd code-review error-handling verification-before-completion writing-plans executing-plans strategic-compact verification-loop security-review subagent-driven-development dispatching-parallel-agents prompt-engineer agentic-eval continuous-learning post-mortem scrutinize management-talk write-a-prd improve-arch document-skill"

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
    ACTIVE="systematic-debugging git-workflow grill-me grill-with-docs tdd code-review error-handling security-review verification-before-completion writing-plans executing-plans prompt-engineer agentic-eval subagent-driven-development dispatching-parallel-agents strategic-compact continuous-learning post-mortem scrutinize"
    BUDGET="~22,000 tokens (use sparingly)"
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
# - $skill → $SKILLS_BASE/$(skill_path $skill)/SKILL.md"
  fi
done

PROJECT_NAME=$(basename "$PROJECT_PATH")

cat > "$PROJECT_PATH/CLAUDE.md" << EOF
# $PROJECT_NAME
> type: $TYPE | created: $(date +%Y-%m-%d) | budget: $BUDGET
> Skills source: github.com/LeGoLus/9arm-skills (sync: bash ~/9arm-skills/scripts/link-skills.sh)

## Active Skills
$SKILL_LIST

## Planning (auto-select)
IF src/ exists OR CONTEXT.md exists → grill-with-docs (writes CONTEXT.md + ADRs)
ELSE → grill-me (clarification only)

## Debug Protocol
ALWAYS: systematic-debugging 4 phases — no skipping
AFTER FIX: verification-before-completion before marking done

## Dev Flow
1. grill-with-docs / grill-me → shared understanding
2. writing-plans → 2-5 min tasks with exact file paths
3. tdd → failing test BEFORE code (delete code written before test)
4. verification-before-completion → confirm fix
5. code-review → pre-merge checklist
6. git-workflow → conventional commit

## Repo Context
- Skills:    github.com/LeGoLus/9arm-skills  (local: ~/9arm-skills/)
- Runtime:   ~/.claude/skills/               (symlinked, always fresh)
- Knowledge: ~/LifeVault/10-Projects/$PROJECT_NAME/
- Sources:   ~/NotebooksLM/$PROJECT_NAME/
- Domain:    CONTEXT.md  ← created by grill-with-docs

## On-Demand Skills (not loaded by default)
$INACTIVE_LIST
EOF

echo "✅ CLAUDE.md → $PROJECT_PATH/CLAUDE.md"
echo "📊 Budget: $BUDGET | Profile: $TYPE"
echo "🔗 Skills from: ~/.claude/skills/ (→ ~/9arm-skills/ → GitHub)"
