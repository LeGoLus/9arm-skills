---
name: grill-me
description: >
  Deep interview skill for planning and design. Use this whenever the user wants to
  plan a feature, design a system, architect a solution, or discuss requirements before
  coding. Forces thorough understanding before implementation. Trigger on: plan, design,
  architect, "let's think about", "how should we", feature planning, system design,
  "I want to build", "new feature", "what do you think about", brainstorm, scope,
  requirements gathering. Even if the user jumps straight to asking for code, consider
  whether a grilling session would help clarify ambiguity first.
---

# Grill Me

Interview me relentlessly about every aspect of this plan until we reach a shared understanding.

Walk down each branch of the design tree, resolving dependencies between decisions one by one.

If a question can be answered by exploring the code base, explore the code base instead of asking me.

## How to Interview

- Ask questions **one at a time** or in small related groups (2-3 max)
- Don't accept vague answers — push for specifics
- When I say "it depends," ask what it depends ON
- Map out the full decision tree before suggesting implementation
- Identify **blocking dependencies** between decisions
- Minimum **10 questions** for any non-trivial feature
- For complex features, expect 30-50 questions — that's normal

## What to Cover

### Scope & Boundaries
- What EXACTLY are we building?
- What are we explicitly NOT building?
- Who is the user? What's their context?

### Design Decisions
- What are the key architectural choices?
- For each choice: what are the alternatives? Why this one?
- What trade-offs are we making?

### Edge Cases
- What happens when things go wrong?
- What are the boundary conditions?
- What inputs are unexpected but possible?

### Dependencies
- What needs to exist before this can work?
- What other systems does this interact with?
- What might change that would affect this design?

### Acceptance Criteria
- How do we know when this is "done"?
- What does success look like?
- What would failure look like?

## When to Stop

You've grilled enough when:
1. You can explain the feature back to me and I say "yes, exactly"
2. All blocking dependencies are identified
3. Edge cases have been discussed
4. We both agree on scope boundaries

Then summarize the full plan and ask for confirmation before moving on.

## The Design Tree Concept

From "The Design of Design" by Frederick P. Brooks Jr.: every design decision opens some possibilities and closes others. Walk down each branch deliberately. Don't let me hand-wave past important forks in the road.
