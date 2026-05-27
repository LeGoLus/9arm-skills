---
name: search-first
description: >
  Research-before-coding skill. Forces the agent to search documentation, explore
  the codebase, and verify assumptions BEFORE writing any code. Prevents hallucination
  and outdated patterns. Trigger on: implement, build, "add a feature", "how do I",
  any coding task where the agent might guess instead of verify, working with unfamiliar
  APIs, libraries, or frameworks. Use this alongside TDD — research first, then test,
  then code.
---

# Search First

**NEVER write code based on assumptions. Always verify first.**

This is the most important skill for preventing hallucinated APIs, outdated patterns,
and wrong library usage. The agent must research before implementing.

## The Rule

Before writing ANY implementation code, you MUST:

1. **Search the codebase** for existing patterns that solve this problem
2. **Read the relevant documentation** for any library/API you'll use
3. **Check for existing utilities** that already do what you need
4. **Verify version compatibility** — APIs change between versions

## Research Process

### Step 1: Explore the Codebase First
```
Before implementing anything new, answer:
- Does this pattern already exist somewhere in the codebase?
- How do similar features handle this?
- What conventions does this project follow?
- What dependencies are already available?
```

Use Grep, Glob, and Read to find answers. Don't ask the user if you can find it yourself.

### Step 2: Check Documentation
For any external library or API:
- Read the ACTUAL docs, not what you remember from training
- Check the installed version: `package.json`, `requirements.txt`, `go.mod`
- Verify the API signature matches the installed version
- Look for migration guides if the version is different from what you expect

### Step 3: Verify Assumptions
Before writing code, state your assumptions:
```
I'm going to use [library X] version [Y] with [this API].
I verified this by reading [source].
```

If you can't verify an assumption, say so explicitly.

### Step 4: Check for Breaking Changes
- Has this API been deprecated?
- Is there a newer recommended approach?
- Are there known issues or gotchas?

## When to Research

**ALWAYS research when:**
- Using a library you haven't used in this session
- Implementing a pattern you're not 100% certain about
- Working with configuration files (formats change between versions)
- Making API calls to external services
- Using framework-specific features (React hooks, Django ORM, etc.)

**You can skip research when:**
- Using basic language features (loops, conditionals, string operations)
- Repeating a pattern you already verified in this session
- The user explicitly told you the exact approach to use

## Anti-Patterns

- ❌ Writing code from memory without checking docs
- ❌ Assuming an API exists because it "should"
- ❌ Using patterns from an older version of a library
- ❌ Guessing configuration options instead of reading docs
- ❌ Implementing something that already exists in the codebase
- ❌ Saying "I believe this is the correct API" without verifying

## Integration with Other Skills

- **Before /tdd**: Research first, then write tests based on verified APIs
- **Before /grill-me**: Research the problem space to ask better questions
- **During /code-review**: Verify that used APIs match installed versions
