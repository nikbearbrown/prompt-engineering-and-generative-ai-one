# Prompt Engineering and Generative AI (AI Plus One)

**Working draft. This is a book-length first draft across five chapters. It has not received expert or classroom review.**

A good-looking answer can still solve the wrong job. This book starts by defining what good means, then tests the methods and the systems that produce it.

| Chapter | Status |
| --- | --- |
| 1. [Describe the task before writing prompts](chapters/01-describe-the-task.md) | Rough draft with offline exercise |
| 2. [Compare prompt patterns on the same job](chapters/02-compare-prompt-patterns.md) | Rough draft |
| 3. [Ground answers in evidence](chapters/03-ground-answers.md) | Rough draft |
| 4. [Bound what a tool-using agent may do](chapters/04-bound-agent-actions.md) | Rough draft |
| 5. [Build a repeatable prompt evaluation](chapters/05-repeatable-evaluation.md) | Rough draft |

## Who this is for

For readers with basic Python, JSON, and enough arithmetic to work with fractions. You can follow the worked cases without Python and run the optional offline labs to verify the mechanisms. Predict each outcome before reading the worked answer. Any live model work is optional and uses only synthetic inputs.

## Try the first activity

Start with the [first-attempt sheet](activity/FIRST-ATTEMPT.md) and [scenarios](fixtures/scenarios.json) before reading the worked chapter. The candidate outputs are synthetic fixtures, not observations from a model. With Python 3.9+ from the repository root:

```sh
python3 -B validate.py A fixtures/candidates/A-good.json
python3 -B validate.py A fixtures/candidates/A-stale.json
python3 -B lab/check_examples.py
python3 -B -m unittest discover -s tests -v
```

The checker uses only the Python standard library. It reads local files, makes no external calls, and takes no action on the result. It returns 0 for accepted, 1 for rejected and 2 for unusable input or scenario errors. The checker evaluates one narrow, synthetic task, not a model or an educational outcome. No purchases, account, API or LMS required.

## Additional offline labs

- `python3 -B lab/decoding.py`: verify the three-token probability and sampling example in Chapter 2.
- `python3 -B lab/repair_desk.py D4 -k 2`: compare retrieval of a conflicting policy pair in Chapter 3. See the [repair-desk handout](activity/RETRIEVAL-LAB.md).
- `python3 -B lab/check_examples.py`: reproduce the toy classification, read-only review traces, and paired-evaluation arithmetic in Chapters 2, 4 and 5.

## Evidence retrieval lab

Use the [repair-desk handout](activity/RETRIEVAL-LAB.md) to compare word-overlap ranking to a scope-and-date filter. All five policies and six cases are fictional, and the comparison calls no model.

## Capstone

Use the [capstone handout](activity/CAPSTONE.md) to connect all five chapters. Start unaided and use only synthetic materials.

## Provenance

This snapshot is original AI-assisted teaching material with fictional cases, examples and checkers. It does not copy earlier book manuscripts, institutional files, student material, or third-party visual assets. Public technical references are linked from the chapters. This draft does not supersede any source book.
