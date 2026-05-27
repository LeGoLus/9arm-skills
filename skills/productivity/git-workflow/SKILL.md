---
name: git-workflow
description: >
  Clean Git workflow skill. Enforces conventional commits, atomic changes, meaningful
  branch names, and PR descriptions that help reviewers. Use whenever committing code,
  creating branches, or preparing pull requests. Trigger on: commit, branch, PR, pull
  request, "push this", git, version control, merge, "clean up commits", "ready to
  commit", "create a PR", "prepare for review". Should be invoked automatically
  after completing any implementation task.
---

# Git Workflow

Maintain clean, reviewable Git history.

## Branch Naming

```
feat/short-description
fix/issue-number-description
refactor/what-is-changing
docs/what-is-documented
chore/maintenance-task
```

Rules:
- Lowercase, hyphens only (no underscores, no camelCase)
- Keep it short but descriptive
- Include issue number when applicable: `fix/142-login-timeout`

## Conventional Commits

Format: `type(scope): description`

### Types
| Type       | When to use |
|------------|-------------|
| `feat`     | New feature for the user |
| `fix`      | Bug fix |
| `refactor` | Code change that neither fixes nor adds |
| `docs`     | Documentation only |
| `test`     | Adding or fixing tests |
| `chore`    | Maintenance (deps, config, CI) |
| `perf`     | Performance improvement |
| `style`    | Formatting (no logic change) |

### Rules
- Description in **imperative mood**: "add" not "added" or "adds"
- First line under 72 characters
- Body explains **WHY**, not WHAT (the diff shows what)
- Reference issue numbers: `fixes #123` or `relates to #456`
- One logical change per commit

### Examples
```
feat(auth): add password reset flow

Implements the forgot-password email flow with token-based
verification. Tokens expire after 24 hours.

Fixes #142
```

```
fix(api): handle empty response from payment provider

The Stripe webhook was returning 200 with empty body in certain
edge cases. Now we validate response body before processing.
```

## Atomic Commits

Each commit should:
- ✅ Compile and pass tests independently
- ✅ Represent one logical change
- ✅ Be revertable without breaking other changes
- ❌ NOT mix refactoring with feature work
- ❌ NOT include unrelated changes ("while I was here...")
- ❌ NOT be a "WIP" on a shared branch

## Staging Strategy

When multiple files changed, group them intentionally:
1. Infrastructure/config changes → separate commit
2. New types/interfaces → commit before implementation
3. Implementation → one commit per logical unit
4. Tests → can go with implementation or separate
5. Documentation → separate commit

## PR Description

```markdown
## What
[One sentence: what does this PR do?]

## Why
[Context: what problem does this solve? Link to issue/PRD]

## Changes
- [Key change 1: what and why]
- [Key change 2: what and why]
- [Key change 3: what and why]

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing steps: [describe]
- [ ] Edge cases verified: [list]

## Screenshots
[If UI changes, before/after screenshots]

## Notes for Reviewers
[Anything non-obvious: tricky logic, known limitations, follow-up needed]
```

## Anti-Patterns

- ❌ "WIP" or "fix stuff" commit messages
- ❌ Mixing refactoring with feature work in one commit
- ❌ Giant commits with 20+ files
- ❌ Force-pushing to shared branches
- ❌ Committing generated files, .env, or node_modules
- ❌ Empty commit messages or "." commits
- ❌ PR descriptions that just repeat commit messages
