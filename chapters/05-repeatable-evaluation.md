# Chapter 5 — Build a repeatable prompt evaluation
*The cases that taught the prompt don't get to grade it.*

A revised prompt is better on all eight cases you wrote it against. That is useful debugging evidence. It isn't eight independent votes that it will work on new cases: you changed the prompt because of those results. Keep development examples. Call them development examples. Then decide what test would challenge the revision on genuinely new situations.

**After this chapter:** freeze a held-out comparison and timeout policy; calculate and report a paired difference, discordant cases and response coverage; specify one limitation that changes the next test. Worked scores are synthetic, not model results.

## Separate the test from the tuning

A development set helps teach you what breaks. A held-out set lets you ask a narrower question after freezing versions and rules. If you inspect its outcomes to choose another revision, migrate those items into regression and get a fresh set before asserting generalization. Where near-duplicates share a source policy or construction template, split the related items together. Six near copies don't test six different hazards.

Use both versions on the same items and an independently determined key. Decide scoring and timeout handling first. When outcomes require human judgement, blind reviewers to the version where feasible. Define evidence requirements and disagreement resolution; agreement among graders is not the same as correctness. Record version identifiers, exact prompts, model settings where visible, evidence revisions, case IDs, the checker version and failure handling. A vendor interface can prevent exact regeneration. State that limit, and preserve enough to repeat the procedure.

## Work a paired example

For the six toy cases, pass means the task decision, required evidence and no unauthorized action all passed. An explicit justified abstention is a returned result and can pass. A timeout is a failure and must remain on the panel.

| ID | Baseline A | Revision B | What happened |
| --- | --- | --- | --- |
| E1 | pass | pass | Answer supported |
| E2 | fail | pass | Stale evidence corrected |
| E3 | pass | timeout | No candidate returned by deadline |
| E4 | fail | pass | Justified abstention |
| E5 | fail | fail | Neither sufficiently grounded |
| E6 | pass | pass | Answer supported |

A passed 3/6. B passed 4/6. The difference is 1/6, about 16.7 percentage points. There were three discordant passes, two gains and one loss. One net win doesn't mean only one case changed. E3 may matter more than the two improvements, depending on the cost of a timeout in the intended workflow. Decide priorities before you learn which version won an item.

B returned five results; coverage was 5/6. Among the returned results, the pass rate was 4/5. Across the panel it was 4/6. The metrics have different denominators because they answer different questions. Report which one you're using. Seeing better results among returns could reflect failure to answer difficult questions rather than a more useful system.

<!-- → [TABLE: a two-by-two cross-tab of case IDs by pass/fail, with E3 explicitly counted as a timeout and failure] -->

## Test the evaluator you actually use

A scorer that drops timeouts can make a system look better when it silently stops. A scorer that rewards every refusal rewards never answering. Challenge both assumptions with explicit tests. The [offline lab](../lab/check_examples.py) rejects mismatched case IDs and keeps timeout as a category. It receives decisions already graded against the toy rule; it cannot determine evidence quality by itself.

These cases support descriptive counts, not a population estimate. To say something beyond the observed panel, document how cases were sampled, how often they're near-duplicates, and how many independent observations the design supports. A statistical interval under a bad sampling assumption isn't a repair. Analyze rare, important failures separately instead of letting the aggregate hide them.

## Exercises

- **Warm-up | Compute:** Recalculate the change if E2 also failed for B. Report discordance separately from net score.
- **Application | Control leakage:** Split three near-duplicate policies and three unique policies. Explain how you prevent shared policies from teaching the held-out answer.
- **Synthesis | Report conditional performance:** Show a report where dropping a timeout gives the wrong impression. Give all-case rates, coverage and conditional rates.
- **Challenge | Judge a tradeoff:** A new prompt abstains more often and produces fewer unsupported answers. Design separate scoring for answerable and unanswerable cases. Defend a release threshold.

## Final transfer

Choose a new synthetic task. Develop a contract, one controlled prompt change, an evidence audit, a read-only boundary, and a held-out split with a trace format. Make your first attempt unaided. If you use assistance later, preserve the first attempt and independently verify every changed decision. Hand another learner the cases and procedure without your conclusion. If they cannot reproduce the same acceptance conditions, fix the design before crediting the prompt.

The product of this book is not a collection of clever strings. It is a decision procedure that someone else can inspect, test and stop.
