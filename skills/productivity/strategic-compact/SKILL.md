---
name: strategic-compact
description: >
  Context window management skill. Suggests optimal moments to compact or clear
  context to maintain quality in long sessions. Prevents degraded output from context
  overflow. Trigger on: long session, "running out of context", "getting confused",
  "forgot what we discussed", context management, token management, "session is getting
  long", when you notice quality degrading. Also trigger proactively at logical
  breakpoints in any extended session.
---

# Strategic Compact

Manage context windows proactively to maintain output quality throughout long sessions.

## Why This Matters

As conversations get longer, the agent's context window fills up. When it gets too full:
- Earlier context gets compressed or lost
- Output quality degrades silently
- The agent starts "forgetting" decisions made earlier
- Code becomes inconsistent with earlier patterns

**Don't wait for auto-compaction at 95%.** Compact strategically at logical breakpoints.

## When to Compact

### ✅ GOOD Times to Compact

**After research, before implementation:**
You've explored the codebase and docs. Summarize findings, then compact.
The implementation phase needs clean context, not research artifacts.

**After completing a milestone:**
Feature is working and tested. Compact before starting the next task.
Save the state: what was built, what tests pass, what's next.

**After debugging, before moving on:**
Bug is fixed and verified. The debugging context (failed attempts,
stack traces, wrong hypotheses) is now noise. Compact it away.

**After a failed approach:**
You tried something and it didn't work. Document why, then compact.
Start the new approach with clean context and lessons learned.

**Between unrelated tasks:**
Finished auth? Moving to payment integration? Clear or compact.
These share no context — carrying auth details wastes tokens.

### ❌ BAD Times to Compact

**Mid-implementation:**
You'll lose variable names, file paths, partial state, the mental model
of what you're building. Finish the current unit of work first.

**While debugging:**
You need the full history of what you've tried and why it failed.
Compacting now means you might repeat failed approaches.

**During a design discussion:**
The nuances of the conversation ARE the value. Don't compress them
until you've reached a decision and documented it.

## The Compact Checklist

Before compacting, save critical state:

```markdown
## Session State (save before compact)

### Completed
- [What was accomplished]
- [Key decisions made and why]

### Current State
- [What files were modified]
- [What tests pass/fail]
- [Any known issues]

### Next Steps
- [What to do after compact]
- [Any context the next phase needs]

### Key Decisions
- [Decision 1]: [Why this choice]
- [Decision 2]: [Why this choice]
```

## Cost Awareness

### Model Selection
- Use **Sonnet** for 80%+ of tasks (implementations, reviews, tests)
- Switch to **Opus** only for deep architectural reasoning, complex debugging
- Use **Haiku** for subagent tasks (simple grading, formatting)

### Token-Saving Habits
- `/clear` between unrelated tasks (free, instant reset)
- `/compact` at logical breakpoints (costs some tokens but saves more)
- Monitor spending with `/cost` during sessions
- Don't enable all MCP servers at once (each one consumes context tokens)

## Proactive Context Management

The agent should monitor its own context health:

**Warning signs that compact is needed:**
- You're referencing something from "earlier" but can't find the details
- Your responses are getting shorter or less detailed
- You're re-asking questions the user already answered
- Code suggestions conflict with earlier decisions
- You're losing track of which files you modified

**When you notice these signs:**
1. Tell the user: "Our context is getting long. I recommend compacting."
2. Summarize the current state
3. Suggest what to preserve vs. what can be dropped
4. Compact and continue

## Long Session Strategy

For sessions over 30 minutes:

```
Phase 1: Research (explore, read, understand)
  → COMPACT with research summary

Phase 2: Plan (design, decide, document)
  → COMPACT with plan document

Phase 3: Implement (code, test, iterate per task)
  → COMPACT between major tasks

Phase 4: Review (verify, clean up, document)
  → Session complete
```

Each compact carries forward only what the next phase needs.
