# 9arm-skills

> LeGoLus skill library for Claude Code — Mac Mini M4 Pro
> 24 skills across 4 tiers, 4 surfaces

## Structure

```
9arm-skills/
├── upstream/superpowers/          ← git subtree: obra/superpowers
├── skills/
│   ├── engineering/               ← tdd, code-review, debugging, security
│   ├── productivity/              ← planning, git, writing, execution
│   ├── ai-agent/                  ← subagents, dispatching, evals
│   ├── personal/                  ← document-skill, andaman-context
│   └── meta/                      ← writing-skills
├── scripts/
│   ├── init-project.sh            ← scaffold CLAUDE.md per project
│   ├── migrate-existing.sh        ← copy from ~/.claude/skills/
│   ├── install-superpowers.sh     ← git subtree + symlinks
│   ├── link-skills.sh             ← symlink to ~/.claude/skills/
│   ├── list-skills.sh             ← list all skills
│   ├── token-audit.sh             ← token cost per skill
│   └── validate.sh                ← post-setup verification
├── tier-manifest.yaml             ← tier assignments
└── README.md

```

## Quick Start

```bash
# New project
~/9arm-skills/scripts/init-project.sh ~/myproject engineering

# List all skills
~/9arm-skills/scripts/list-skills.sh

# Token audit
~/9arm-skills/scripts/token-audit.sh

# Validate setup
~/9arm-skills/scripts/validate.sh
```

## Tier System

| Tier | When | Token budget |
|------|------|-------------|
| 0 | Always | ~3,500t |
| 1 Engineering | Most projects | +~9,500t |
| 2 AI/Agent | AI features | +~7,000t |
| 3 Optional | On demand | varies |

## Profiles

| Profile | Tokens |
|---------|--------|
| planning | ~4,500t |
| engineering | ~9,500t |
| ai-agent | ~13,000t |
| hermes | ~9,000t |
| full | ~20,000t |

## Update Superpowers

```bash
git -C ~/9arm-skills subtree pull --prefix=upstream/superpowers superpowers main --squash
```

## Sources

| Skills | Source |
|--------|--------|
| 15 existing | `~/.claude/skills/` via migrate-existing.sh |
| 8+ new | [obra/superpowers](https://github.com/obra/superpowers) via install-superpowers.sh |
| grill-with-docs | [mattpocock/skills](https://github.com/mattpocock/skills) via curl |
