# 9arm-skills
> Skill library repo | LeGoLus | Mac Mini M4 Pro

## Purpose
This repo manages all Claude Code skills. Do not use heavy profiles here.

## Active Skills (minimal — this is the library itself)
- ~/9arm-skills/skills/productivity/git-workflow/SKILL.md

## Rules
- Conventional commits for all changes
- Update tier-manifest.yaml when adding new skills
- Run scripts/validate.sh after changes
- Run scripts/token-audit.sh to check token budgets

## Key Commands
- `./scripts/migrate-existing.sh` — import from ~/.claude/skills/
- `./scripts/install-superpowers.sh` — install obra/superpowers via git subtree
- `./scripts/token-audit.sh` — audit token costs
- `./scripts/validate.sh` — verify everything works
- `./scripts/list-skills.sh` — list all skills with descriptions
