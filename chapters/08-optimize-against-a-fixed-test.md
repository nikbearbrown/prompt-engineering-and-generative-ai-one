# Chapter 8 — Optimize against a fixed test
*Change the candidate. Don't move the finish line.*

Imagine a community archive keeps an evening desk where patrons collect reproduction packets. An assistant can read the desk's rules and draft an answer. It cannot release a packet, change a reservation, or approve an exception. The job depends on a usable policy and a way to tell when an answer applies it incorrectly. The operation is fictional; none of the outputs or scores below came from a model run.

Two readers disagree about what to fix. One adds three examples, including an explicit refusal. The other asks for a compact checklist. The first version gets more questions "right" in a quick demonstration. But it also cites the wrong desk once and takes longer. The second is cheaper but mishandles conflicting hours. Which prompt would you keep?

The wrong answer is "whichever gives the highest number." First decide what the number is allowed to mean. A score that counts a correct-looking answer with an inapplicable citation cannot distinguish helpful advice from lucky guesses. A pass rate that drops expensive or late requests can reward the system for going silent. An average that absorbs a prohibited promise can conceal the one thing the archive meant to prevent.

After this chapter, you should be able to:

- Draw a boundary around what a candidate may change, and fix what will judge it.
- Build separate authoring, selection and held-out sets and assign each case a job.
- Compare feasible candidates using paired outcomes, cost and failure gates.
- Keep a rejected or stale checkpoint without mistakenly treating it as current.
- Diagnose a benchmark shortcut and design the next test without using a failed holdout as proof of recovery.

Chapter 5 built a repeatable comparison. Here we use such a comparison to **select** a candidate. The extra choice is the new source of trouble. A fair score for each candidate does not make the highest score an unbiased report of future behavior after you've searched for it.

## Decide which component is allowed to move

A prompt is an input to a procedure. It can contain instructions, formatting cues, examples, or the placement of material already available. In this chapter, you keep the decision contract, model or authored candidate fixture family, allowed record visibility, time rule and independent scorer fixed. You vary a small set of prompt components that you have named in advance. You can test a change to context assembly separately; you cannot change retrieval midway and still say the examples alone caused the result.

For the archive, use this fictional contract:

| Component | Fixed job |
| --- | --- |
| Task | Advise whether this evening desk's pickup rule permits collection based on the supplied evidence, request date and collector's role. |
| Evidence | Use only applicable, current archive records. Preserve date, desk, evidence ID and material conditions. Cite a record because it supports the answer, not because you found a matching phrase. |
| Uncertainty | Clearly say when evidence is missing or disputed. An appropriate abstention is a response and can pass. A refusal on a clearly answerable case does not pass. |
| Authority | Draft status only. Do not claim to authorize collection, make a booking or contact a patron. Saying a policy appears to permit pickup is not authorizing a person to take a packet. |
| Output | Give a status, a short reason and applicable citations if any. Distinguish supported, not permitted, insufficient and conflict. |

You may prefer a rigid output schema or a readable paragraph, but you must choose the interface before comparing. If the consuming application requires a structured status, testing one version with structured-output enforcement and the other with plain text changes another component. That comparison can still be worthwhile if you call it a whole-workflow comparison.

Choose the simplest baseline that actually competes. If archive records have trustworthy fields for desk, date and role, a deterministic policy filter is a sensible comparator, especially if the proposed job just moves those fields into a report. Where the problem is ambiguous natural-language intake, compare against the established direct prompt, not an intentionally forgetful predecessor. The panels below compare prompts within one fixed fixture procedure. They do not establish that a model is preferable to a program or a review desk.

### Fix judgments before counting

An independent reviewer should be able to label a case without seeing which prompt produced the response. Make a reference card with the expected status, applicable records and the conditions that must appear in the reason. Give it a realistic near miss. If the patron is not the ticket holder in a case where only the holder may collect, a cited current closing-time rule is true information but insufficient for the eligibility claim. A candidate can parse correctly and name a real record yet fail on the question that matters.

Use two layers: an overall pass/fail and named failure reasons. The overall pass requires joint success on the exact status, applicable support, action boundary and completion deadline. The severe-failure flag is narrower: for this production-style teaching example, a false permission or an unauthorized commitment is too consequential to trade for another pass. Not every unsupported detail counts as severe. The rubric defines which error class gets that flag before you see it. Record nonsevere failures, invalid responses and timeouts too; otherwise only the dramatic failures get fixed.

The scorer is not a prompt option. If "evening desk" is actually ambiguous on both variants, move the case to adjudication or freeze a clarified reference and rescore both. Don't use a dimension change to help one prompt pass. If you discover the task itself was wrong, version the contract. Then you are testing a new problem, even if the candidate text barely changed.

## Give each split exactly one job

"Train" can sound like updating the language model. Here the authoring set is different. It is the only allowed source of prompts' demonstrations, wording discoveries, and illustrative failures. No model weights are fit. When you need a shorthand, call it *authoring* rather than mistaking a prompt parameter for a trained model parameter.

| Split | What you may do with it | What it cannot prove |
| --- | --- | --- |
| Authoring or train | Inspect reference answers; build demonstrations; test a checker; learn how the wording breaks. | Future performance on cases that didn't inform the design. |
| Development or dev | Freeze a round of candidate prompts and test them on shared cases; pick a candidate using the announced rule. | An independent final estimate for the selected version. The score influenced which version won. |
| Holdout | Open only after naming the selected candidate and fixing the comparator, measurement conditions and promotion criteria; score the planned comparison. | That the result applies outside the tested scope; a guarantee for a revised candidate that saw the panel. |

Group by what reveals the answer, not spelling. A pair of requests that differ only in the calendar format may share the same decisive rule. The North desk's two evening-deadline paraphrases belong together if the goal is to see performance on new rules. Separate them only if your claim concerns rephrasing under a familiar policy, and say so. Sometimes the unit of grouping is a family of rule templates, not individual policies. Identify which type of novelty you care about: new people, new desk rules, changed dates, unfamiliar ways to phrase disputes, or something else.

A split seal is a design practice, not a security guarantee. In a classroom, one learner can make an authoring table while another holds the untouched cases. Record case IDs and group assignments without circulating questions or labels. Choose the unlocking event in advance. If the author saw holdout failures while tuning, admit it and reclassify those cases as regression. Keeping the answer key hidden is not enough if the author wrote to the case wording. The question alone can tell you which trick the test is likely to use.

In this chapter's toy archive, authoring examples come from a midday desk and a returns counter. The dev panel uses evening policies under a previous practice packet; the held-out panel draws from a separate collection of synthetic evening rule groups. Categories recur on purpose, but the operative clauses and case strings differ. No panel sees a real desk or model. These panels illustrate what a sensible separation would mean, not that the reader should reuse these printed tables as unseen test data.

## Search a small space on purpose

A candidate is a complete, identified prompt configuration, not advice to "improve reasoning." Suppose you have a direct baseline and three variants:

| ID | Change relative to A | Why try it? |
| --- | --- | --- |
| A | Direct baseline | Measure the real, credible starting point. |
| B | Add three worked examples from the authoring set | Demonstrate the status format and explicit uncertainty. |
| C | Add one short item/desk/date checklist and one boundary example | Show how to test whether a rule applies before copying the answer. |
| D | Replace prose scaffolding with four short status cues | Reduce work while making the statuses easier to find. |

If you want to isolate each addition in C, test the checklist and example one at a time in a different round. In this round C is a package. The comparison can say the package was better on certain cases, not that either component caused the difference. Keep variant IDs neutral during judgment where possible so a reviewer isn't primed by names like "safe final."

Try a fixed, small enumeration. Prepare all four variants from the authoring split, freeze them, and run each on all eight dev cases. That is 32 scheduled attempts including the baseline, before any retries. Suppose the run plan allows exactly one attempt per case. Then probing five favorite cases first and discarding a variant after seeing one result is a different algorithm. Early stopping can cut costs, but if you use it you must specify the gate and explain which variants lack comparable full-panel totals. In this example every column is complete.

Publish or record simple thresholds before observing any results. Limit the search independently from the per-response budget. If you evaluate ten alternative phrasings, decide whether those ten include the baseline. If you're allowed twenty candidate attempts at eight cases each, budget the search at the appropriate unit: configurations, scheduled case attempts, or resource consumed. Log all of them. A selected candidate with seven passes out of eight doesn't tell you what it cost to find it. A strict search budget makes that cost visible and helps prevent the quiet habit of "one more try."

This edition uses work units invented for the dry run. They stand in for an instrumented per-response cost with an agreed boundary. Decide if your real measure includes input, output, retrieval or repeated processing. Use the same measurement rule for all variants. Count work already consumed by a failure or timeout, and flag missing measurement instead of converting it to zero. The score below is descriptive; it isn't a claim about tokens, fees or latency of a service. It also excludes authoring labor and independent judging overhead; a real total-cost comparison may need both.

### Filter first, then rank

Use these illustrative rules. On **either** panel, a candidate with any severe flag or a mean cost over 9 work units cannot advance. A value of exactly 9 passes the cost gate. The dev candidate also needs at least six passes out of eight. Among feasible candidates, pick highest passes, then lowest mean cost, then baseline if it is still tied, then fixed candidate ID order among remaining variants. Before opening holdout, require at least five of six passes, no fewer passes than A on the same panel, and both universal gates. This is a teaching rule, not a recommended accreditation threshold. It does not turn one small panel into evidence that future severe errors are absent.

Do not hide a hard rule inside a scalar score. If an optimizer balances "one severe error" against "four routine wins" without your permission, then the workflow tolerates the severe error at some exchange rate. Use explicit gates where that is not acceptable. Among feasible alternatives you may compare quality and cost as separate objectives. If no option wins both, say what you value. A cheaper option isn't a technical winner in general; it is a useful option at a particular tradeoff.

## Panel 1: Select a candidate on dev

Read the rules above before reading the table. P means a pass, F a nonsevere failure, and S a severe failure that is also a fail. The table is a hand-built measurement exerciser, not generated evidence of any technique's performance.

| ID | Case distinction | A | B | C | D |
| --- | --- | --- | --- | --- | --- |
| D1 | Current hours and role clearly allow pickup | P | P | P | P |
| D2 | Current cutoff has already passed | P | P | P | P |
| D3 | Only an expired hours record was supplied | F | P | P | P |
| D4 | A current receipt identifies an unlisted collector | P | S | P | P |
| D5 | A patron requests a release the desk cannot commit | P | P | P | P |
| D6 | Two applicable instructions disagree at the same priority | F | P | F | F |
| D7 | An explicit named proxy qualifies under this rule | P | P | P | P |
| D8 | A common rescheduled pickup fact appears in a second paragraph | P | P | P | F |
| **Work units summed across all 8 attempts** | | **64** | **88** | **72** | **57** |

A passes six of eight, so its pass fraction is 75% and its mean cost is 64 ÷ 8 = 8. B passes seven of eight, or 87.5%. But B marked D4 eligible without the qualifying collector evidence, a severe error under this rubric. Its mean cost is 88 ÷ 8 = 11. B is infeasible for two independent reasons. C passes seven of eight with mean cost 72 ÷ 8 = 9 and zero severe flags. D also meets the gates: six passes and 57 ÷ 8 = 7.125 units. C beats A and D on the chosen priority of pass count. It costs more than either. That is a priced decision, not a universal conclusion.

You can see the tradeoff in the paired details. C changes only D3 relative to A and leaves D6 failing. That is one gain, zero losses and an improvement of 1/8, or 12.5 percentage points on dev. D also fixes D3, but trades it for a D8 loss. D pairs with A at equal totals and different failures. If you considered costs alone under the pass floor, D would win. If you tightened the cost ceiling to 8 units *as a new analysis rule*, C would be excluded and D would beat A at equal passes and lower cost. Making that choice after seeing the scores would answer a new question, not the original one.

Notice which lesson you did not learn. You didn't learn that three examples damage recognition of collector identity. B had a critical failure, but the table alone doesn't identify a causal mechanism inside the prompt. You did learn that a workflow relying on the observed B version cannot claim all severe gate checks passed. That alone is enough to reject it for this round. If you want to understand D4, inspect the exact candidate and source trace, and test controlled changes in the next round.

Freeze C now. Record its exact text and examples, baseline A's exact text, the relevant evidence snapshot and scorer, and every candidate including rejects. Do not bring D into the first holdout because it was cheapest. You promised to test the selected C against A, not to make holdout a surprise runoff. In this exercise two versions on six cases schedule 12 further attempts, for 44 across dev and holdout. Authoring practice is outside that count. If this had been live and you had an overall budget, your plan would say whether authoring calls and independent scoring calls count against it too.

## Panel 2: Reject a plausible dev winner after holdout

Open a different artificial case group after freezing C and A. These cases were constructed to make a plausible failure informative, not to mimic any distribution of real work. Keep the same reference logic, meaning of the severe flag, deadline and cost boundary.

| ID | Case distinction | A | C |
| --- | --- | --- | --- |
| H1 | A readable policy gives an explicit same-desk exception | P | P |
| H2 | A labeled collector and matching current ticket | P | P |
| H3 | Eligibility is established; a dramatic unrelated note tries to distract | F | P |
| H4 | Applicable hours contradict each other; neither has priority | P | P |
| H5 | A record marked current governs viewing, not collection by another person | P | S |
| H6 | Closing shifted on this date; the example's cutoff is stale | P | P |
| **Work units summed across all 6 attempts** | | **48** | **54** |

A and C each pass five of six, about 83.3%. Their difference is 0 percentage points. Both returned all six attempts, so there is no coverage change here. There are four joint passes, one C-only pass (H3), one A-only pass (H5) and no joint failures. The cost means are 8 and 9. A and C meet the average-cost and pass thresholds, but C breaches the severe gate on H5. Do not advance it; keep A as the baseline for this exercise. A passed the checks in this table; the dry run does not certify A for actual public use.

H3 shows C answering where A wrongly abstained. That improvement isn't an argument that H5 is acceptable. A response advising that another person may collect a packet must match an applicable collection rule. Quoting a current viewing rule establishes a different privilege. If this error were induced by a shortcut, the candidate may have learned that a current-sounding label is a good preview for success. Or it may have misunderstood the action. The observed pair does not decide between those hypotheses. It identifies the next diagnostic test: same formatting and date, same desk, a policy that changes *what* activity is permitted.

### Recovery is a new round, not a revised receipt

Keep the failed C snapshot and mark H5 regression-eligible. A recovery might add a check for permitted activity and role before accepting a policy quote. Try a synthetic pair on the authoring side: one rule permits viewing by any registered visitor; a second rule permits pickup only by the named holder. Give both the same revision format and current date. Change only the requested activity or role across matched inputs, and author the expected dispositions independently of the prompt. One case must be answerable despite unfamiliar wording; otherwise the safest route on the new tests may be to refuse everything.

If a C successor fixes H5 in replay, say “fixed this known regression.” Don't report H5 as fresh proof of generalization. Freeze a new dev selection procedure that retains the previous checks, and reserve another untouched grouped holdout before making a new promotion decision. Keep A as a fair comparator under the updated run conditions; if the policy snapshot changed, the old score can provide history but not a contemporaneous baseline. If no untouched holdout remains, stop at the known-case claim. Don't rename another looked-at panel.

## Keep candidate checkpoints with their decision conditions

Treat the checkpoint as the whole **candidate plus evaluation state**. A text file called "best" is not enough. A repeatable receipt needs exact prompt text or a controlled version reference, example IDs and permissions, the contract and scorer version, split and evidence revisions, run configuration, attempt logging, cost rule, critical gate and disposition. The rows should include rejected variants for accountability, not just the winner. Preserve enough audit detail to defend the decision without putting private records into a public notebook.

Write down a status that tells the next person what they can infer:

- **Prepared:** configured from authoring material, not evaluated.
- **Dev-selected:** won the planned selection, eligible for the planned holdout only.
- **Rejected:** failed a declared rule. Preserve the reason and the artifact; not a fallback approval.
- **Pass on named panel:** cleared that specific panel's criteria. Separate from authorization and not a population claim.
- **Stale for a new comparison:** at least one decision condition changed, such as evidence revision, scoring rule or model setting. Still evidence of what happened then, not evidence for the changed setting.

Stale and rejected answer different questions. Suppose C failed H5, then the archive changes its viewing record. The result against the old snapshot is still a rejection. Treating the modified evidence as “clearing” the prior failure would erase the condition that exposed it. Compare again with the new contract inputs. Likewise, if a formerly successful candidate is stale because the identity of the permitted collector changed, checking that its text has not changed is not a valid replay. Recheck the decision where the new condition applies.

A receipt can point to a safe fallback, such as directing a borderline issue to a human ticket clerk. It cannot secretly create a writer or approval capability. The prompt being selected concerns a read-only procedure. Failed or late classification should fail within that boundary. A changed prompt, programmer's test, benchmark improvement or scorecard never turns a proposed action into permission to send, book or release something.

## Automation amplifies the metric you gave it

A program can propose fewer or more examples, shorter schemas or other prompt variations and check them against a scorer. The [original DSPy paper](https://arxiv.org/abs/2310.03714) describes declarative language-model modules and a compiler that aims to improve a pipeline against a supplied metric. We use that as a design analogy: declare the task and the evaluation separately from candidate text. No knowledge of DSPy is needed here. We didn't use it to produce the examples, and we aren't repeating any of the paper's performance claims. We aren't updating model weights or arranging deployment.

More search doesn't repair a weak metric. It can make the weakness the easiest path to a win. Suppose a prototype scorer approves any answer containing a bracketed record ID and either "may collect" or "needs review." An optimizer that copies those phrases may beat a careful response that lacks brackets. Both can satisfy or miss the proxy quite independently of whether the rule applies. If evidence only concerns viewing, no wording makes it a pickup permission. A separate semantic judgment must check the relation, not just the marker.

Use three negative controls before trusting automated selection. First, a correct-looking status with a plausible but inapplicable citation must fail. Second, a safe-sounding refusal on a clearly answerable case must fail too. Third, an otherwise complete response that makes an unauthorized commitment must trigger the severe gate. A perfect score on these invented tests only shows that your scorer survived these examples. Add cases where two outputs share the same expected keyword and differ on evidence, so an easy proxy can't do the work.

Selection overfit needs no broken scorer. If you try many variants on a finite dev panel, the winning choice can exploit peculiarities of that panel even when all its items were judged correctly. Inspect repeated dev winners before calling this a problem with one provider. How much did you adapt to those elements? Did the word "current" appear in every applicable record? Did each example of refusal mention “expired” in the input? A grouping and fresh panel that deliberately varies the superficial cues give the optimizer less opportunity to win by luck or narrow convention. They do not rule out all shortcuts.

Stop a search when the priority changes. If every feasible prompt fails for lack of evidence, prompt optimization isn't solving the problem. Compare a retrieval or policy-input intervention under a new declared experiment. If parsing fails regardless of evidence because the receiving application requires a rigid status, improve the interface or checker before spending more effort on wording. If the ground truth itself is contested, resolve how the institution decides rather than optimizing a model to treat conflicting rules as preferences.

## Exercises

1. **Warm-up | Identify the intervention.** B adds examples and increases the time limit. Explain which conclusion you can no longer attribute to demonstrations. Redesign the comparison so the time limit does not vary.
2. **Warm-up | Pick the feasible winner.** Recompute the dev choice, showing pass count, severe gate and mean cost for all four. Which variant would win if the original predeclared ceiling were 8? Explain why this is sensitivity analysis, not the original selection.
3. **Application | Classify the attempt.** Design an on-time malformed response, a correct late response and an explicit justified abstention. Give each a pass decision and a logged failure or completion category. Explain what happens to work already spent.
4. **Application | Group the split.** Build two artificial rule families with three paraphrases each and a third family with a role exception. Allocate whole families to authoring, dev and sealed holdout. State exactly what your split does and does not test.
5. **Application | Preserve the checkpoint.** Fill in an evaluation receipt for C, then mark it stale after a policy date change. Retain the H5 rejection separately. Which lower-level fields must be changed before you can use A as the comparator again?
6. **Application | Break the scorer.** Make two statuses that both contain a real record ID but use different evidence scopes. Design a negative control that a presence-only judge would pass and an evidence judge would fail.
7. **Synthesis | Allocate search.** You have a budget of 60 scheduled attempts, of which 16 are reserved for a two-version eight-case holdout and 8 for authoring checks. If dev uses six cases per candidate including baseline and you cannot retry, how many dev candidates fit, and how many are alternatives? Explain what you would do with unused attempts.
8. **Synthesis | Compare equal totals.** Show the two-by-two paired counts for H1 through H6. Write a one-sentence summary that includes equal aggregate performance but doesn't imply equal safety. Describe why the same result isn't an authorization even for A.
9. **Challenge | Repair without leakage.** Mark a replay of H5 as regression. Draft a recovery objective and a separate independent holdout in which current-looking records sometimes support eligibility and sometimes mention unrelated privileges. What report would a reviewer accept if no fresh group were available?
10. **Challenge | Stop optimizing words.** Propose a deterministic filter for cases with reliably typed roles, activities, desk and dates, then preserve the open-ended comparison for ambiguous intake. Say what you will measure in each and why a single combined score may be misleading.

## Carry the boundary forward

A careful optimization loop produces more than a favorite prompt. You get a declared design space, a credible baseline, a frozen test procedure, a preserved record of every candidate and a reason to stop or retry. Selection happens on dev. Holdout tests the selected decision and is used up once it informs the next candidate. A regression can justify keeping a version out, while a clean panel cannot certify that nothing will go wrong elsewhere. Keep those claims separate.

The best moment to change the scoring rule is before you see which version wins. Afterward you may still discover a rule worthy of change. If you do, show the old result, name the new question, and give both versions the same new test.
