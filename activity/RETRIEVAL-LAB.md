# Extension lab: trace retrieval across policies, notices and dates

The records in [repair_desk.json](../fixtures/repair_desk.json) are invented. Decide eligibility by hand before opening either implementation or reading the comparison notes. Nothing in this lab decides whether a real service should accept an item.

## Your review rules

A record applies only to the requested desk and only if it is a dropoff policy; a notice is not a decision rule. The effective day is included and the expiration day, if present, is excluded. The same rule applies whether you're asking about today or reconstructing a fictional past decision. Do not add a “newest wins” rule. One applicable cap permits the assessment if mass is at or below the cap. Different applicable caps mean conflict, even when the proposed mass exceeds both. No policy means insufficient evidence, not ineligible.

For cases D1 to D6, write the eligible IDs, decision, and known limits. Predict whether a naive search for the supplied keywords might miss an applicable record or lead you to examine the wrong one. Preserve this prediction.

```sh
python3 -B lab/repair_desk.py D1
python3 -B lab/repair_desk.py D4 -k 2
```

## What the script compares

The label word overlap denotes a deliberately weak retrieval baseline: tokenize records with a literal lowercase letter-or-number pattern, count shared distinct tokens, and break ties by stable ID. Only positive overlap results are returned. Rank then verify first takes the top k, then rejects wrong scope or dates. Filter then verify reads this tiny full corpus and applies the policy constraints before deciding, even if keyword overlap would be zero. Both feed the same deterministic decision logic; the difference is evidence selection, not a simulated LLM improvement.

With one result in D1, the baseline ranks the time-to-notice policy above the dropoff cap. Verification properly refuses to infer a mass limit from time. Full-corpus filtering finds N-1. In D2 the language highlights 15, the archived rule. March 1 is the boundary day on which N-0 no longer applies. D3 uses the same numerical detail, but on the day before the boundary. It verifies the contract's schedule rather than the superficial word “archived.”

In D4, the top result hides a live disagreement. Returning two records makes the disagreement visible. A caller can correctly implement verification on its input and still publish an incomplete conclusion about the corpus. This dataset's deliberately exhaustive filter doesn't drop either record. In a large corpus, completeness would be an evidence issue in its own right. A filter over untrusted desk or date metadata is no guarantee of correctness.

## Extend, don't silently mutate

Make a copy of the fixture before changing rules. Add a stipulation that seems reasonable, such as allowing the most recent policy to win, but first state what exactly makes the issue you're solving a policy conflict. If you truly change the contract, revise the independent expected outcomes and report that you are solving a different job. Otherwise write at least one regression test for a same-mass input returning different decisions purely because a date crosses its boundary.

For further work, compute how many required clauses are retrieved, then count statuses separately. Ask whether a high top-one match rate can coexist with missing complete support on multi-clause questions. Measure the effect of raising k in a separate comparison; don't increase k and change policy precedence at the same time.
