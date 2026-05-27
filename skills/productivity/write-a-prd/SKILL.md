---
name: write-a-prd
description: >
  Creates a Product Requirements Document with structured task breakdown and blocking
  relationships. Use after a planning or interview session when the user is ready to
  formalize requirements into actionable tasks. Trigger on: PRD, requirements,
  "write up the plan", task breakdown, "create issues", spec, specification,
  "what do we need to build", "break this down", "create tasks", action items,
  implementation plan. Also use when the user has finished a grill-me session and
  is ready to move to execution.
---

# Write a PRD

Create a Product Requirements Document based on our shared understanding.

## Process

1. **Check prerequisites**: If we haven't done a deep interview yet, suggest invoking `/grill-me` first
2. **If we've already discussed the design**, skip to step 4
3. **Summarize** the key design decisions we've made so far
4. **Write the PRD** following the structure below

## PRD Structure

### 1. Overview
One paragraph: what we're building, why, and for whom.

### 2. Goals & Non-Goals

**Goals** (what this DOES):
- Explicit, measurable outcomes
- Tied to user value

**Non-Goals** (what this DOES NOT cover):
- Scope boundaries
- Things that might be assumed but are explicitly excluded
- Future work that is out of scope for now

### 3. Design Decisions
For each key decision:
- The decision
- Alternatives considered
- Why we chose this approach
- Trade-offs accepted

### 4. Task Breakdown

For each task, provide:

```
### Task: [TASK-ID] [Title]
**Description**: What needs to be done
**Acceptance Criteria**:
  - [ ] Specific, testable condition 1
  - [ ] Specific, testable condition 2
**Complexity**: S / M / L
**Blocked By**: [TASK-IDs] or INDEPENDENT
**Parallelizable**: Yes / No
**Notes**: Any implementation hints or warnings
```

#### Task Guidelines
- Tasks should be **atomic**: completable in a single agent session
- Every task needs **clear "done" criteria** that can be tested
- Mark dependencies: `BLOCKED_BY: [TASK-01, TASK-03]` or `INDEPENDENT`
- Prefer **smaller, well-defined tasks** over large ambiguous ones
- Group related tasks but keep them independently executable
- Include edge cases discovered during the interview as **explicit tasks**

### 5. Technical Considerations
- Architecture constraints
- Performance requirements
- Security considerations
- Migration or backwards compatibility notes

### 6. Open Questions
- Anything still unresolved
- Decisions that need more information
- Risks that need monitoring

## Execution Order

After writing the PRD, suggest an execution order:
1. List which tasks are INDEPENDENT (can start immediately)
2. Show the critical path (longest chain of blocking dependencies)
3. Identify which tasks can run in parallel

## Updating the PRD

As tasks are completed, the PRD should be updated:
- Mark tasks as DONE with a brief note on what was implemented
- Add any new tasks discovered during implementation
- Update open questions as they're resolved
