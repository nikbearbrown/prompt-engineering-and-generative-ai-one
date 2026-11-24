# Prompt Engineering and Generative AI (AI Plus One)

**Working draft.** Nine chapters teach how to make generative-text work observable, checkable, and bounded. The examples and candidate responses are fictional. The book has not received expert or classroom review and does not replace a source textbook or a university course.

You can use the book without a model account. The optional offline labs use Python 3.9+ and no external packages. Begin each exercise by predicting the result yourself. If you use model assistance later, use only synthetic inputs, record the changes, and verify consequential claims independently.

## Learning outcomes

After working through this draft, readers should be able to:

- State a task contract and compare prompt changes against a fixed baseline.
- Ground answers in evidence and set boundaries on tool actions and permissions.
- Build a repeatable evaluation and diagnose harder cases involving audiences, long context, optimization, and multimodal workflows.

## Chapters

### Part I · Build a checkable workflow

| Chapter | Reader outcome |
| --- | --- |
| 1. [Describe the task before writing prompts](chapters/01-describe-the-task.md) | Specify what succeeds and decide what to do with missing or conflicting evidence |
| 2. [Compare prompt patterns on the same job](chapters/02-compare-prompt-patterns.md) | Change one part of a prompt and compare against a fixed baseline |
| 3. [Ground answers in evidence](chapters/03-ground-answers.md) | Verify which applicable evidence supports each claim |
| 4. [Bound what a tool-using agent may do](chapters/04-bound-agent-actions.md) | Design a read-only runner, a review boundary and a stop rule |
| 5. [Build a repeatable prompt evaluation](chapters/05-repeatable-evaluation.md) | Preserve paired evidence, timeouts and honest denominators |

Start with the [first-attempt sheet](activity/FIRST-ATTEMPT.md), then consult the [Part I guide](PART-I.md). The [Part I capstone](activity/CAPSTONE.md) connects the task, evidence, permissions and evaluation.

### Part II · Diagnose harder cases

| Chapter | Reader outcome |
| --- | --- |
| 6. [Diagnose audience, role, and evidence separately](chapters/06-diagnose-audience-and-prompt.md) | Adapt a presentation without changing the decision or its evidence |
| 7. [Measure whether context can do its job](chapters/07-measure-context-use.md) | Tell when evidence is missing and when it was present but not used correctly |
| 8. [Optimize against a fixed test](chapters/08-optimize-against-a-fixed-test.md) | Try prompt variants without teaching the holdout to agree with you |
| 9. [Operate multimodal workflows](chapters/09-operate-multimodal-workflows.md) | Verify claims across image and text, and justify a hold or a fallback |

Use the [Part II guide](PART-II.md) for the labs and the [transfer exercise](activity/TRANSFER.md) to combine them.

## Verify the offline examples

From the repository root:

```sh
python3 -B -m unittest discover -s tests -v
```

Part I gives you the baseline, the evidence checks, and the score. Part II asks what changes when the audience, context layout, candidate-selection procedure, or input format changes. Each exercise states its own decision contract: Chapter 3 can support a partial answer, while Chapter 7 deliberately requires both facts or an abstention. Neither approach is a universal rule.

The book does not copy earlier manuscripts, institutional files, student material, or proprietary assets. Primary technical references are linked where used. Simulations, diagrams and authored results are not model benchmarks or proof of deployment.
