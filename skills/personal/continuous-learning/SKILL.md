---
name: continuous-learning
description: >
  Learn and extract patterns from development sessions. Captures reusable instincts,
  common fixes, and project-specific patterns that improve agent performance over time.
  Trigger on: "learn from this", "remember this pattern", "we keep doing this",
  "extract patterns", "save this approach", "instinct", end of session, after fixing
  a recurring bug, when discovering a codebase convention. Use at the end of any
  significant session to capture what was learned.
---

# Continuous Learning

Extract reusable patterns from development sessions and encode them as instincts
that improve future agent performance.

## What is an Instinct?

An instinct is a small, reusable pattern extracted from real work:

```markdown
## Instinct: [Name]

**Trigger**: When [specific situation]
**Action**: Do [specific action]
**Evidence**: Learned from [what happened]
**Confidence**: [high/medium/low]

### Example
Before: [what was happening]
After: [what we do now]
```

Instincts are more specific than skills — they capture a single decision or pattern
rather than a full workflow.

## When to Extract Patterns

### After Fixing a Bug
What caused it? What was the fix? Could this happen again?
```
Instinct: Always check for null before accessing nested properties in API responses
Trigger: When processing external API responses
Evidence: PaymentService crashed on null response.data.items
Confidence: high
```

### After Discovering a Convention
The codebase does something a specific way. Capture it.
```
Instinct: Use `useServerAction` hook instead of direct fetch for mutations
Trigger: When implementing form submissions or data mutations
Evidence: Existing patterns in UserForm, ProductEditor, SettingsPage
Confidence: high
```

### After a Failed Approach
Document what didn't work and why, so you don't repeat it.
```
Instinct: Don't use localStorage for auth tokens in this project
Trigger: When implementing auth token storage
Evidence: Tried localStorage, broke SSR. Project uses httpOnly cookies.
Confidence: high
```

### After Finding a Better Way
You found a more efficient/cleaner approach during implementation.
```
Instinct: Use Zod schema.parse() at API boundaries instead of manual validation
Trigger: When adding input validation to API routes
Evidence: Manual validation in /api/users had 3 bugs. Zod version has zero.
Confidence: medium
```

## Extraction Process

At the end of a session (or at a checkpoint), review what happened:

### Step 1: Identify Learnings
Ask yourself:
- What did we get wrong the first time?
- What pattern did we discover in the codebase?
- What approach worked better than expected?
- What should we always/never do in this project?

### Step 2: Format as Instincts
For each learning, create an instinct with:
- **Clear trigger**: When exactly does this apply?
- **Specific action**: What exactly should be done?
- **Evidence**: Why do we believe this? (the concrete incident)
- **Confidence**: How sure are we? (high = verified, medium = one data point, low = hypothesis)

### Step 3: Categorize

**Project-level instincts** (specific to this codebase):
- Naming conventions
- Architecture patterns
- Library-specific usage
- Configuration quirks

**Universal instincts** (apply to any project):
- General debugging strategies
- API design patterns
- Testing approaches
- Performance optimizations

### Step 4: Store
Add instincts to the project documentation:
- Project-level: `.claude/instincts.md` or similar
- Universal: your personal development notes

## Instinct Evolution

Instincts have a lifecycle:

```
Hypothesis (low confidence)
  → Verified once (medium confidence)
    → Verified multiple times (high confidence)
      → Promoted to Skill (if complex enough)
        → Integrated into Rules (if universal)
```

**Evolve instincts**:
- When several related instincts cluster, combine them into a skill
- When an instinct has been high-confidence for a month, consider making it a rule
- When an instinct is contradicted by evidence, update or remove it

## Session Review Template

At the end of a significant session:

```markdown
## Session Review: [Date] - [What was accomplished]

### Instincts Extracted
1. **[Name]**: [One-line description]
   - Trigger: [When]
   - Action: [What]
   - Confidence: [Level]

2. **[Name]**: [One-line description]
   - Trigger: [When]
   - Action: [What]
   - Confidence: [Level]

### Patterns Observed
- [Pattern 1 that might become an instinct with more evidence]
- [Pattern 2 that might become an instinct with more evidence]

### Failed Approaches (don't repeat)
- [Approach]: [Why it failed]
```

## Integration with Other Skills

- **After /tdd**: What testing patterns worked well in this codebase?
- **After /code-review**: What issues keep recurring?
- **After /grill-me**: What questions revealed unexpected complexity?
- **After /improve-codebase-architecture**: What structural patterns should be maintained?
