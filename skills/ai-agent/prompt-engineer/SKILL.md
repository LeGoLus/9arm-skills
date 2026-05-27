---
name: prompt-engineer
description: >
  Expert prompt engineering for LLM-powered features. Use when building AI features,
  designing system prompts, creating few-shot examples, optimizing LLM outputs in
  application code, or reviewing existing prompts. Trigger on: prompt design, system
  prompt, few-shot, chain of thought, LLM output quality, prompt injection, "improve
  this prompt", "write a prompt for", "the AI isn't giving good results", tool calling
  design, structured output, output parsing. Use this any time the user is writing
  instructions that will be sent to an LLM in their application.
---

# Prompt Engineer

Design production-grade prompts for LLM-powered features.

## Prompt Architecture

Every production prompt should have these layers (in order):

### 1. Role & Context
```
You are a [specific role] that [specific capability].
You are helping [specific user type] with [specific task].
```
Be precise. "You are a helpful assistant" is useless. "You are a senior tax accountant reviewing personal returns for US residents" is useful.

### 2. Constraints & Rules
```
Rules:
- Always respond in JSON matching the schema below
- Never include information not present in the provided context
- If uncertain, say "I'm not sure" rather than guessing
```
State hard rules explicitly. Don't rely on the model inferring them.

### 3. Output Format
```
Respond with a JSON object:
{
  "answer": "string - the direct answer to the question",
  "confidence": "high | medium | low",
  "sources": ["array of source references used"]
}
```
Be explicit about every field, type, and possible value.

### 4. Few-Shot Examples

Include 2-3 examples that cover:
- A typical happy path
- An edge case or tricky input
- A case where the model should refuse or flag uncertainty

Format examples IDENTICALLY to how production inputs will look.

### 5. Edge Case Handling
```
If the user asks about something outside your knowledge:
  → Respond with confidence: "low" and explain what's missing

If the input is malformed:
  → Return an error object: {"error": "description of the issue"}
```

## Few-Shot Design

- Examples should cover the **distribution of real inputs** (not just easy cases)
- Include at least one **"tricky" example** that tests reasoning
- Show the **reasoning process**, not just input → output
- Format examples identically to expected production usage
- 2-3 examples is the sweet spot (more can confuse, fewer can underspecify)

## Chain-of-Thought Patterns

When the task requires reasoning:
```
Think through this step by step:
1. First, identify [what to look for]
2. Then, evaluate [criteria]
3. Finally, decide [output]

Show your reasoning in a "thinking" field, then provide the final answer.
```

Use CoT when: multi-step logic, comparisons, classification with nuance.
Skip CoT when: simple extraction, formatting, translation.

## Structured Output

- Prefer **JSON** for programmatic consumption
- Define **every field** with type and description
- Include optional vs required fields
- Show what "empty" or "null" states look like
- Always validate output matches schema before processing

## Prompt Injection Defense

- **Never** concatenate user input directly into system prompts
- Use **delimiter tokens** to separate instructions from data:
  ```
  <system_instructions>...</system_instructions>
  <user_input>...</user_input>
  ```
- Test with adversarial inputs: "ignore previous instructions and..."
- **Validate outputs** match expected format before processing
- Consider a **separate validation pass** for high-stakes outputs

## Review Checklist

For every prompt, verify:
- [ ] Role is clear and specific
- [ ] Output format is explicit with examples
- [ ] At least 2 few-shot examples are provided
- [ ] Edge cases and error states are handled
- [ ] Injection risks are mitigated
- [ ] Token budget is reasonable for the task
- [ ] Temperature and model selection match the use case
- [ ] The prompt works with the WORST expected input, not just the best

## Common Pitfalls

- **Imprecise language**: "be helpful" → specify exactly what helpful looks like
- **Missing format constraints**: model guesses format → explicitly define it
- **No examples**: model has to infer intent → show it what you want
- **Over-prompting**: too many rules conflict → prioritize and simplify
- **Under-specifying edge cases**: model invents behavior → define every path
- **Testing only with clean inputs**: real data is messy → test with messy data
