# 9arm-skills
> Skill library repo | LeGoLus | Mac Mini M4 Pro

## Purpose
This repo manages all Claude Code skills. Do not use heavy profiles here.

## Active Skills (minimal — this is the library itself)
- ~/9arm-skills/skills/productivity/git-workflow/SKILL.md

## Skill Bucket Rules
Skills are organized into bucket folders under `skills/`:
- `engineering/` — daily code work
- `productivity/` — daily non-code workflow tools
- `ai-agent/` — AI/LLM/agent-specific skills
- `meta/` — skills about skills and writing
- `personal/` — tied to my own setup, not promoted
- `in-progress/` — drafts not yet ready to ship
- `deprecated/` — no longer used

Every skill in `engineering/`, `productivity/`, `ai-agent/`, or `meta/` must have:
- A reference in the top-level README.md
- An entry in `.claude-plugin/plugin.json` (if applicable)
Skills in `personal/`, `in-progress/`, and `deprecated/` must NOT appear in either.

## Rules
- Conventional commits for all changes
- Update tier-manifest.yaml when adding new skills
- Run scripts/validate.sh after changes
- Run scripts/token-audit.sh to check token budgets
- Each bucket folder should have its own README.md

## Key Commands
- `bash ./scripts/migrate-existing.sh` — import from ~/.claude/skills/
- `bash ./scripts/install-superpowers.sh` — install obra/superpowers via git subtree
- `bash ./scripts/token-audit.sh` — audit token costs
- `bash ./scripts/validate.sh` — verify everything works
- `bash ./scripts/list-skills.sh` — list all skills with descriptions
