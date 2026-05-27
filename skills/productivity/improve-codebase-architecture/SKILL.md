---
name: improve-codebase-architecture
description: >
  Codebase architecture improvement skill. Explores your codebase looking for shallow
  modules, tangled dependencies, and structural issues that hurt code quality and agent
  navigability. Use weekly or after a surge of development. Trigger on: refactor,
  architecture, "clean up", "code quality", "improve structure", "too many files",
  "hard to navigate", module boundaries, "codebase review", technical debt, "code smell",
  "spaghetti code", reorganize, restructure. Use this proactively — a well-structured
  codebase makes every other skill work better.
---

# Improve Codebase Architecture

Explore the codebase and identify opportunities to **deepen shallow modules**.

## When to Use

- Weekly maintenance (like a code health check)
- After a surge of development (new features often degrade structure)
- When agent outputs are getting worse (often a structural problem)
- Before starting a major new feature (clean house first)

## What to Look For

### 1. Confusions
Where does understanding one concept require bouncing between many small files?

Signs:
- Files under 50 lines that are always imported together
- "Utility" files that are really part of a specific feature
- Types defined far from where they're used
- Constants scattered across multiple files
- A feature's logic split across 5+ files with no clear reason

### 2. Extracted-for-Testing Anti-Pattern
Where have pure functions been extracted just for testability, but real bugs hide in how they're called?

Signs:
- `utils/` folders full of tiny pure functions
- Functions called from exactly one place
- Test files that mock the caller to test the callee

**Fix**: Inline the function. Test the behavior at the integration boundary instead.

### 3. Tightly Coupled Modules
Where do tightly coupled modules create integration risk?

Signs:
- Modules that ALWAYS change together
- Circular or near-circular dependencies
- "Pass-through" modules that add no logic
- Shotgun surgery: one change requires editing 5+ files

### 4. Shallow Modules
Where are interfaces nearly as complex as their implementation?

Signs:
- Classes/modules with many small methods (lots of surface area, little depth)
- Config objects with dozens of fields
- Abstraction layers that just forward calls
- Wrapper functions that add no value

### 5. Naming Drift
Where do names no longer match what the code does?

Signs:
- `handleClick` that does data fetching
- `UserService` that manages sessions, preferences, AND authentication
- Generic names: `utils`, `helpers`, `misc`, `common`
- Acronyms nobody can explain

## Process

### Phase 1: Explore
1. Read the directory structure — understand the shape of the project
2. Read key entry points (index files, main modules, routers)
3. Trace the import graph for 2-3 core features
4. Note where you had to read many files to understand one concept

### Phase 2: Identify
5. List **3-5 "deepening opportunities"** ranked by impact
6. For each, document:
   - **Current structure**: What files/modules are involved
   - **The problem**: Why this structure hurts (fragmentation, coupling, confusion)
   - **Deeper module design**: What would a consolidated module look like
   - **Migration path**: Step-by-step changes to get there safely

### Phase 3: Propose
7. Present the opportunities ranked by:
   - **Impact**: How much does this improve navigability and code quality?
   - **Risk**: How likely is this to break things?
   - **Effort**: How much work is involved?
8. Recommend which to tackle first (high impact, low risk)
9. **Wait for approval** before making any changes

### Phase 4: Execute (with approval)
10. Make changes one module at a time
11. Run tests after each change
12. Verify the improvement: can you now understand the concept in fewer file reads?

## The Goal

After improvements, both humans and agents should be able to:
- **Navigate** the codebase with fewer file reads
- **Understand** modules from their interfaces alone
- **Make changes** with confidence about what will and won't break
- **Add features** without degrading the structure

## Cadence

Do this **once a week** or after any development surge. As you keep refining your codebase, you'll notice the quality of agent output goes up consistently — well-structured code is the foundation everything else builds on.
