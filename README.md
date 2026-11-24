# Prompt Engineering and Generative AI (AI Plus One)

**Working draft. This snapshot contains one chapter, not a complete or expert-reviewed edition.**

A good-looking answer can still solve the wrong job. This book starts by defining what good means, then tests the methods and the systems that produce it.

| Chapter | Status |
| --- | --- |
| 1. [Describe the task before writing prompts](chapters/01-describe-the-task.md) | Rough draft with offline exercise |
| 2. Compare prompt patterns on the same job | Planned |
| 3. Ground answers in evidence | Planned |
| 4. Bound what a tool-using agent may do | Planned |
| 5. Build a repeatable prompt evaluation | Planned |

## Try the first activity

Start with the [first-attempt sheet](activity/FIRST-ATTEMPT.md) and [scenarios](fixtures/scenarios.json) before reading the worked chapter. The candidate outputs are synthetic fixtures, not observations from a model. With Python 3.9+ from the repository root:

```sh
python3 -B validate.py A fixtures/candidates/A-good.json
python3 -B validate.py A fixtures/candidates/A-stale.json
python3 -B -m unittest discover -s tests -v
```

The checker uses only the Python standard library. It reads local files, makes no external calls, and takes no action on the result. It returns 0 for accepted, 1 for rejected and 2 for unusable input or scenario errors. The checker evaluates one narrow, synthetic task, not a model or an educational outcome. No purchases, account, API or LMS required.

## Provenance

This snapshot is original AI-assisted teaching material with a fictional case, examples and checker. It does not copy earlier book manuscripts, institutional files, student material, or third-party visual assets. Public technical references are linked from the chapter. This draft does not supersede any source book.
