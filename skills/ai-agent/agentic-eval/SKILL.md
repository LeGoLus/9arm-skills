---
name: agentic-eval
description: >
  Evaluate LLM outputs systematically. Use when building AI features that need quality
  assurance, designing eval suites, testing prompt changes, or tracking output quality
  over time. Trigger on: eval, evaluate, "test the prompt", "is the output good",
  quality, regression, benchmark, "LLM testing", "how do we know it works", "measure
  quality", "test the AI", "the AI is getting worse", "compare prompts". Essential
  for any production AI feature — without evals, you're flying blind.
---

# Agentic Eval

Systematically evaluate and improve LLM output quality.

## Why You Need Evals

- Prompts break silently (model updates, edge cases, distribution shift)
- "It works on my examples" ≠ "it works in production"
- You can't improve what you don't measure
- Evals are the tests for AI features

## Evaluation Types

### 1. Assertion-Based (Automated)
For outputs with objectively verifiable properties:

```javascript
// Examples of assertions
assert(output.format === 'json')           // Format check
assert(output.fields.includes('name'))     // Required fields
assert(output.length < 500)                // Length constraint
assert(!output.includes(userInput))        // No input echo
assert(schema.validate(output).valid)      // Schema validation
```

Best for: structured output, classification, extraction tasks.

### 2. LLM-as-Judge (Semi-automated)
For subjective quality that code can't easily check:

```
Evaluate this response on a scale of 1-5 for:
- Accuracy: Does it contain correct information?
- Completeness: Does it address all parts of the question?
- Clarity: Is it easy to understand?
- Tone: Does it match the expected tone?

Provide your reasoning before giving scores.
```

Rules for LLM-as-Judge:
- Use a **separate, stronger model** as judge (not the same model)
- **Require reasoning** before scores (improves reliability)
- **Calibrate** with human-graded examples first
- **Randomize order** in A/B comparisons (position bias is real)

### 3. Human Review (Manual)
For nuanced quality that automated checks miss:

- Create **structured review forms** (not open-ended "is this good?")
- Use **blind comparison** (A/B) when testing prompt changes
- Aggregate reviews across **multiple reviewers**
- Track **inter-rater agreement** to know if your criteria are clear

## Designing an Eval Suite

### Test Case Requirements

- **Minimum 20 cases** for meaningful results
- Cover the **input distribution**:
  - 60% common/typical inputs
  - 20% edge cases (unusual but valid)
  - 10% adversarial (trying to break it)
  - 10% "should refuse" (safety, out-of-scope)
- **Version** your test cases alongside your prompts
- **Never optimize** against your full test set — hold out 30% for validation

### Creating Test Cases

For each test case, define:
```json
{
  "id": "test-001",
  "input": "The actual input to the LLM",
  "context": "Any context/documents provided",
  "expected": {
    "format": "json",
    "must_contain": ["key_fact_1", "key_fact_2"],
    "must_not_contain": ["hallucinated_info"],
    "quality_rubric": "Should be professional tone, under 200 words"
  },
  "category": "common | edge | adversarial | safety"
}
```

### Metrics to Track

| Metric | What it tells you |
|--------|-------------------|
| Pass rate (assertions) | Hard correctness |
| Average quality score | Subjective quality |
| Failure by category | Where it breaks |
| Latency (p50, p95) | User experience |
| Token usage | Cost per request |
| Refusal rate | Over/under-cautious |

## Running Evals

### Process
1. **Create eval config**: test cases + evaluation criteria
2. **Run against current version** (baseline)
3. **Save results** with version tag
4. **Make changes** (new prompt, model update, etc.)
5. **Run against new version**
6. **Compare**: flag any regression > 5% on any metric
7. **Decide**: ship, iterate, or roll back

### Regression Detection

Set thresholds for each metric:
- **Hard fail**: any assertion pass rate drops > 10%
- **Soft fail**: quality score drops > 0.5 points
- **Monitor**: latency increases > 20%

Automate these checks in CI if possible.

## Iterating on Prompts

When evals show a problem:
1. **Identify the pattern**: which test categories fail most?
2. **Hypothesize**: what's causing the failure?
3. **Targeted fix**: change only what addresses the failure
4. **Re-run full eval**: make sure the fix didn't break other things
5. **Document**: what changed and why

## Anti-Patterns

- ❌ Testing only happy path inputs
- ❌ Using the same model to generate and judge
- ❌ No baseline comparison ("it seems better" is not a measurement)
- ❌ Eval set too small (< 10 cases, results are noise)
- ❌ Not versioning eval sets alongside code
- ❌ Optimizing against the full test set (overfitting to evals)
- ❌ Running evals only once before launch (run continuously)
- ❌ Ignoring edge case failures ("only 5% of users hit this" — that's still a lot)
