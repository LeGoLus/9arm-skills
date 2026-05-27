---
name: document-skill
description: Create or update skill documentation in Thai + English for the 9arm-skills library
tags: [personal, meta, documentation]
tier: personal
estimated_tokens: 300
---

# Document Skill

## Purpose
Create or update SKILL.md files in the 9arm-skills library with proper frontmatter and clear documentation.

## Required Frontmatter
Every SKILL.md must have:
```yaml
---
name: <skill-name>           # kebab-case, matches directory name
description: <one line>      # used by list-skills.sh; explain WHEN to use this skill
tags: [<tag1>, <tag2>]       # categories for filtering
tier: <0|1|2|3|personal>     # 0=always, 1=engineering, 2=ai-agent, 3=optional, personal=explicit
estimated_tokens: <number>   # approximate token cost (chars/4)
---
```

## Documentation Format
After frontmatter:
1. **# Skill Name** — one-line summary
2. **## When to Use** — trigger conditions
3. **## Process / Steps** — numbered steps or phases
4. **## Rules / Constraints** — what NOT to do
5. **## Examples** (optional) — concrete usage

## Language
- Headings and structure: English
- Thai explanations allowed in comments/notes for personal skills
- Keep descriptions concise — tokens cost money

## After Writing
1. Run `bash ~/9arm-skills/scripts/token-audit.sh` to verify token count
2. Update `tier-manifest.yaml` if tier changes
3. Commit with: `docs(skills): add/update <skill-name>`
