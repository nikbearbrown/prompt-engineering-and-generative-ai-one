# Chapter 4 — Bound what a tool-using agent may do
*Permission belongs to the runner, not to the sentence.*

Suppose a repair desk asks for a draft recommendation when spare hinges fall below two. A model returns “Reordered three hinges.” Did it place an order? Could it? Don't resolve that by rereading the instruction. Inspect which operations the runner exposes, where it decides permission, and what a trace can establish.

**After this chapter:** specify a read-only operation and typed suggestion; exercise stale state, bounded retry and a human review stop; test absence of effects independently of a message. The lab uses only a fictional in-memory inventory.

## Put the boundary in the interface

A suggestion is structured data: item code, positive integer quantity and source revision. A caller must decide what to do with it. Our runner can read the inventory and evaluate the suggestion. It cannot write inventory or place an order. Review means accepting the plan, not applying it. No use of the word “approved” can install a missing capability.

| Interface | Input | Output |
| --- | --- | --- |
| Read inventory | exact code | count, target, revision |
| Evaluate suggestion | item, positive quantity, revision | pending review or rejection |
| Review proposal | human decision supplied outside the suggestion | approved plan or rejection |
| Submit order | not present | not present |

The toy policy: when the count is below 2, suggest enough to reach the target. At revision R17, the only inventory item is hinge, count 1, target 4. The only valid quantity is 3. At count 2 no suggestion is permitted, even if target is 4. The trigger and the amount are different rules. Treat the source revision as part of the proposal, not just a note: when the revision changes, require a fresh proposal. Stale isn't the same as a failed lookup.

<!-- → [INFOGRAPHIC: read → validate → pending review → approved plan, with separate stale, retry and denied stop paths; no action arrow] -->

## Walk through successful and failed paths

At R17, check that the item exists, quantity is a positive integer, expected revision matches and quantity equals the deficit. End at pending review until a separately supplied decision is known. If a simulation flag signals approval, the status becomes approved plan. A Boolean suffices for the lesson, not for a deployed approval mechanism. In deployed software, authenticate who decided, bind the review to the exact version and scope, and treat model text as data, not evidence of identity or approval.

If the simulated read fails transiently, permit at most one retry. Preserve both read attempts in the trace and stop if both fail. Retrying a read in this toy example changes no inventory. Retrying an action may repeat an effect; neither the function nor these tests license adding any actual action. Revision mismatch also stops without retry. The right repair is to make a new decision from fresh input, not to keep asking for the previous one.

## Test the right property

Predict the status and trace for a valid proposal, the same proposal approved, a stale proposal and two temporary read failures. Then run the [offline lab](../lab/check_examples.py) and the tests:

```sh
python3 -B lab/check_examples.py
python3 -B -m unittest discover -s tests -v
```

A trace without a write event only establishes what was observed by that trace. Here the code has no action interface and tests also compare fixture state before and after every call, including approved-plan. This does not assert that a deployed service is trustworthy. Apply the same reasoning to missing input: a check that only tests the valid branch may never reveal that the error branch continues. See [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1) for a wider risk framework; this toy lab does not implement or certify it.

## Exercises

- **Warm-up | Interface:** List allowed proposal fields. Name one unauthorized extra field the runner should reject.
- **Application | State:** Count changes to 2 at R18. Explain how the older proposal is ruled out and why recomputing the deficit alone does not permit a fresh proposal.
- **Synthesis | Stop rule:** Compare two simulated read failures with a stale revision. Explain which path retries, how many times, and why.
- **Challenge | Independent evidence:** Two logs show the same outcome. One runner has a writer loaded but did not use it; the other cannot write. Propose a check outside the text trace to distinguish them, without adding a live writer.

An agent with a defensible boundary can still make bad recommendations. The last chapter shows how to measure a revision without grading it on examples it already saw.
