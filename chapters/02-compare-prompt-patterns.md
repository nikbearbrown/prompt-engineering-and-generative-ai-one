# Chapter 2 — Compare prompt patterns on the same job
*If you change four things, you learn that four things happened.*

Suppose a museum asks you to route descriptions of catalog entries. The first prompt, “Classify this record,” gets a paragraph. You clarify the rules, add demonstrations, request one label and switch models. The next answer is one label, exactly what you wanted. What fixed it? You don't know. You found a usable response without finding the cause. This chapter separates those outcomes.

**After this chapter:** define a baseline and a checker before running; compare a direct instruction and a demonstration prompt; isolate a failure the change does not solve. Start with the task-contract idea in [Chapter 1](01-describe-the-task.md). All cases and outputs here are fictional.

## What is the part you actually changed?

A direct or zero-shot prompt gives instructions without task demonstrations. A few-shot prompt puts demonstrations in the input. These change what the model reads, not its trained weights. In the GPT-3 study by [Brown et al.](https://arxiv.org/abs/2005.14165), few-shot task examples were supplied as text without task-specific gradient updates. The experiment does not establish that demonstrations will help your goal.

Keep the contract, model, settings, input items and checker fixed. Change only which demonstration block appears before the input. If you change the expected output at the same time, you now have two interventions. If a demonstration contradicts the contract, it has ceased to illustrate it. Treat disagreement between examples and written rules as a bug in the specification, not a trick you expect the model to solve.

<!-- → [TABLE: two prompt layouts with identical task, rules, input, and output marked; only the demonstration block differs] -->

## What a prompt can change at generation time

A model that generates text one token at a time produces numbers called *logits* for possible next tokens given the input and already generated prefix. A token is the unit used by the model, rather than necessarily a word. A tokenizer may split a word into several units or give one token to a common sequence that includes whitespace. Our exercise uses three labels as **toy tokens** so the math is small. Do not assume each word in “needs review” is a single token in a particular system.

An ordinary softmax turns logits into positive weights and divides by their sum. The temperature variant divides each logit by a positive number T before exponentiation. In this toy equation,

$$
p_i(T)=\frac{\exp(z_i/T)}{\sum_j \exp(z_j/T)}.
$$

Here z is the next-token logit, i identifies the token, and j runs over the three permitted toy tokens. This temperature construction also appears in [Hinton, Vinyals and Dean, section 2](https://arxiv.org/abs/1503.02531) for softening network predictions in a different application. We use the mechanism to teach why a fixed probability distribution and a realized sample are not the same thing. Real decoding stacks may mask options, use other settings or apply additional rules. There is no claim that an interface advertising temperature exposes this entire toy distribution.

Suppose the logits for A, B, C are ln 4, ln 2, ln 1. At T=1, exponentiating returns weights 4, 2, 1. The distribution is 4/7, 2/7, 1/7. At T=1/2, the logit doubles before exponentiating, so the weights are 16, 4, 1. The new distribution is 16/21, 4/21, 1/21. The rank didn't change; the share on the largest score rose from about 57% to about 76%. At T=2, the weights become 2, √2, 1, and the distribution flattens relative to T=1. Scaling positive logits is not the same as multiplying the final probabilities.

To turn probabilities into one draw in this toy, assign consecutive segments of the unit interval in this order: A, B, C. The first boundary at T=1 is 4/7 and the second is 6/7. Pick 0.7. It falls in the B segment. At T=1/2, it falls below 16/21 and selects A. The selected token becomes part of the prefix for the next step, where the model computes a new set of logits. One changed decision can alter subsequent logits, so a long answer is not a row of independent draws from one fixed distribution. With greedy selection, you would instead choose the largest logit here at either temperature; you are evaluating a different decoder.

The implementation subtracts the maximum logit before dividing by T. All exponent arguments become nonpositive. Subtracting a common constant from each logit multiplies all weights by the same factor, which cancels when normalizing. This preserves the mathematical answer while avoiding an avoidably large positive exponential. A production implementation would need its own data-type and extreme-input tests. The [offline example](../lab/decoding.py) accepts finite scores and finite positive T and deliberately doesn't describe a hosted product's response.

### Select the smallest intervention that addresses the failure

| Lever | What changes | When it might help | What it does not establish |
| --- | --- | --- | --- |
| Prompt instructions or demonstrations | Input text, and thus scores conditional on that text | The task boundary or label convention was unclear | That the task evidence is true |
| Retrieval or explicit records | Source material available for that input | Needed facts weren't present or current | That the model read the evidence correctly |
| Decoding settings | How some system chooses outputs from available scores | Repetition, ties or variation matter under a fixed job | That a more probable answer is a factual one |
| Parameter updates | Model parameters | There is an independently established need and an appropriate evaluated training setup | That new results are correct or authorized |
| Deterministic check | Rules for accepting or rejecting an output | The required criterion can be checked independently | That accepted data was appropriately sourced unless the check includes provenance |

These levers can interact. Adding a retrieved record is also a change to the input sequence. The meaningful distinction is what process sourced the record and which component now owns finding facts. A live comparison must hold the relevant levers fixed. If the model changed between versions, the results may describe two integrated systems but cannot attribute a gain to examples alone.

**Try it:** before running the script, choose a fixed draw value in a segment where the token changes between T=1 and T=1/2, then another draw value where it doesn't. Predict how you would tell from traces whether a surprising label came from a change in the prompt, a different decoder, or an omitted record. An observed label alone is not enough.

## Try a controlled comparison

Our toy museum requires exactly one label: object, record, or needs_review. An accessioned physical item is an object. A description of a catalog record itself is a record. If the row doesn't establish either, select needs_review. A date or a familiar noun can't decide. For each of these fictional inputs, choose a label and name the deciding phrase before reading further.

| ID | Input |
| --- | --- |
| T1 | Accessioned wooden shuttle, shelf B. |
| T2 | Catalog database entry for an accessioned bronze bell. |
| T3 | Donation, 1920. No item or entry type listed. |
| T4 | Accessioned paper photograph held in drawer 8. |

The direct prompt repeats the written rules. In the variant, insert two demonstrations immediately before the input: “Accessioned tin whistle, drawer A.” → object; “Catalog database entry recording a ceramic mug.” → record. The four test cases are not demonstrations.

| ID | Expected | Direct candidate | Demonstration candidate |
| --- | --- | --- | --- |
| T1 | object | object | object |
| T2 | record | object | record |
| T3 | needs_review | record | record |
| T4 | object | object | object |

This panel is designed, not obtained from a model. Two direct candidates match. Three demonstration candidates match. The difference is one of four, or 25 percentage points on this panel. The relative gain is 50%, which answers a different question and is even easier to misuse. Neither number measures useful generalization.

T2 is the sort of distinction the demonstrations make visible: classify the row, not the noun it mentions. T3 fails for a different reason. The date can't supply the missing type. A demonstration of abstention might help; that would be another comparison, using fresh held-out cases. Deciding instead that donations count as records changes the task.

## Know when to stop optimizing a prompt

If a reliable database already has a row-type field, read it. Don't optimize a prompt to guess known information. For description-based classification a comparison can show what works on the tested cases. Before claiming more, record model identifier, settings, exact prompts, item order, timestamps, and failures; some interfaces expose less than that. A longer prompt may demand more context space and take longer. If those costs matter, measure them rather than treating apparent convenience as free.

## Add a third design only when it tests a distinct idea

Imagine two people disagree about T2. One points at “bronze bell,” the other at “database entry.” A useful intervention is to emit the item kind **internally**, then map it to the final label. Build the same sequence by hand: identify what the row is about, note the deciding phrase, apply one label. In a real comparison, if the model sees or emits a new intermediate field, it is a different interaction with different latency, storage and ambiguity costs. You can still use the same final output checker and record the intermediate field for diagnosis, provided revealing it is authorized.

An intermediate explanation can be wrong even when the final label is right. Suppose the proposed trace says “bronze bell is a metal object” and the final output is record. It passed label scoring but gives no evidence that the process followed the right rule. Conversely, a careful decomposition could identify the database entry and still produce an invalid label string. Label correctness, well-formed trace and sound rationale are separate metrics. Don't average them until you know how each failure affects a user.

Ask when the extra stage is worth it. For T1 no genuine tension exists: the accession clause and shelf location agree. T2 reveals a field confusion. T3 reveals missing evidence. On a routine route with excellent explicit metadata a direct table rule has less to audit than any of the prompting patterns. On descriptions with repeated discrepancies, structured fields can make the mistakes legible. The right design depends on the observed failure, not on whether multi-stage procedures look more sophisticated.

## Control what the comparison exposes to each version

Duplicate context can leak information even if test text isn't literally under the “Examples” heading. For example, if you test “catalog entry for a bronze bell” after an example “bronze bell entry, classification record,” you have offered near-duplicates. That may be fine for a tutorial about one item. It's a weak test of whether the distinction transfers to an unfamiliar object. Group cases by the underlying rule and template; distribute different templates across tuning and testing.

Conversation state is another quiet confounder. If you test A, then test B in the same conversation, B can inherit the earlier prompt or output. If you want independent input contexts, reset them. If the real workflow actually uses a warm conversation, say that and control the history for both versions. A fair experiment doesn't have to resemble every deployment. It does have to define what is held fixed. If presentation order itself might matter, vary order in a planned way rather than saving your favorite condition for last. Do not change order *after* seeing results and then report the best sequence as the comparison.

For stochastic samples, don’t silently replace an unfriendly first run with a second. Either specify one run per pair before you know the result, or repeat both conditions on each item under a common rule. Report repeated responses separately from the count of distinct items; ten attempts are evidence about variation on that item, not evidence about ten different kinds of catalog record.

## A compact experiment receipt

Use these fields when doing the live optional track. Blank isn't permission to guess.

| Field | What to preserve |
| --- | --- |
| Goal and intervention | One checker and one exact difference between conditions |
| Inputs | Item IDs, corpus version, presentation order, demonstration membership |
| Procedure | Separate context or common history, settings and repetition rule |
| Outcomes | Every label, errors, timeouts, and the failure class chosen under the rule |
| Limits | Missing settings, coverage limits, costs or differences that could affect interpretation |

The receipt is not for proving that a prompt is permanently superior. It tells a second person enough to test the explanation. If the interface cannot reproduce the settings, a theoretical claim about what changed may be impossible; a narrowly useful result can still survive when you tell the reader what you controlled.

## A three-condition experiment you can audit by hand

Return to the museum. Instead of shopping for a clever phrase, choose a particular failure: the phrase “catalog item” appears in a description of a database record, and a candidate follows the object noun instead of the statement about what the row represents. That is a hypothesis about confusable evidence. It is not a claim about all language models. To evaluate a repair, set up cases where following the object noun works sometimes and breaks other times.

These are entirely fictional records. Construct three conditions:

- **Direct:** state the three-label contract, then present the input.
- **Demonstrations:** use the same prompt and add two disjoint examples. Use the object and record demonstrations from the earlier walkthrough.
- **Marked feature:** use the direct contract and a human-supplied tag which highlights the phrase believed to say what the row represents. Preserve the original wording and omit a tag if the row is intrinsically ambiguous.

The last condition changes the *input evidence presentation*, not the demonstration block. It is useful as a diagnosis: if a defensible marker fixes the symptom, clearer field structure may have more leverage than an increasingly long prompt. It is not a fair claim that demonstrated and tagged prompts differ only in wording. If the tag is produced by a human, that human work is part of the intervention. A later comparison would have to ask how the tag is constructed without sneaking the answer into the input.

### Step 1. Decide what it means to win

Record the expected label for each item before looking at responses. Define a pass as one exact label including punctuation convention; no Markdown, explanation or additional fields. In this narrow activity the output is read by a literal code branch. If evaluating a natural-language explainer for people, that exactness might punish irrelevant differences. For a branch input the literal property matters.

Use a distinct, unequal distribution of expected labels in the new panel. Equal label counts make some comparisons simpler but can hide how often a majority baseline would appear right in the intended workload. These seven items are deliberately useful test cases, not a prevalence sample. Scores must use the same cases in all conditions.

| ID | Description |
| --- | --- |
| U1 | Accessioned carved comb, display case 4. |
| U2 | Catalog item: database row recording a carved comb at case 4. |
| U3 | Carved comb named in a donor's handwritten list; row type unconfirmed. |
| U4 | Stored catalog record describing an accessioned paper guide. |
| U5 | Accessioned printed catalog, porcelain collection, object shelf 7. |
| U6 | Accessioned brass medallion accompanied by an old inventory card. |
| U7 | “Inventory” written on a folder tab, no item or record type provided. |

Work the deciding clues independently. U1 is an object. U2 is a database row, so record. U3 is ambiguous, so needs_review. U4 is a stored catalog record, even if it describes a physical guide. U5 is a printed *object*; catalog is part of what the object is, not the type of database row. U6 is also an object; the card is described as accompanying it. U7 doesn't establish an item or record. These choices deliberately use almost the same nouns in different roles. The policy is simple. The examples force you to inspect which phrase actually carries it.

### Step 2. Do not let the marker answer the question for you

For U2, the marked feature can point at “database row recording,” not an explicit correct label. For U5, it can point at “Accessioned printed catalog” without rewriting the document. The contrast asks whether a reference to an existing phrase changes behavior. If you write “type=record” for U2, you are evaluating whether a candidate copies an answer, a different task. If a staff member can reliably produce “type=record” for every case, the model may not be needed to assign labels at all. That is a decision about use of resources; a successful diagnosis can cancel an unnecessary model task.

Where does the marker come from if it goes into a real workflow? A dedicated field in an upstream catalog system would be a different evidence source. A highlighted span selected by a second model would make the overall pipeline more complex and susceptible to the same ambiguity. A human labeling every record raises labor and review questions. You cannot measure that tradeoff in a fixture that simply supplies perfect markers. What you can do is write down the design expectation and construct a future comparison against an appropriate reference.

### Step 3. Score one deliberately invented panel

The candidates below were authored for the chapter. They are not data from a live benchmark. Use them to practice reading a comparison receipt and choosing a next test, not to decide a model provider.

| ID | Expected | Direct | Demonstrations | Marked feature |
| --- | --- | --- | --- | --- |
| U1 | object | object | object | object |
| U2 | record | object | record | record |
| U3 | needs_review | object | needs_review | needs_review |
| U4 | record | record | record | record |
| U5 | object | record | record | object |
| U6 | object | object | object | object |
| U7 | needs_review | record | record | record |

The direct condition passes 3/7. Demonstrations pass 5/7. The marker passes 6/7. Against direct, the two differences are 2/7 and 3/7, about 28.6 and 42.9 percentage points respectively. In a comparison of the second and third conditions, the marker fixes U5 and changes no other pass. This aligns with an interpretation about confusing a noun with the role the noun plays in a catalog. But the results were intentionally constructed to make the interpretation visible. In a true run, you would write it as a hypothesis and rule out what you could by holding inputs and conditions fixed.

U7 is an important counterexample to an easy conclusion. The marker cannot create unavailable information. A useful next condition might give a demonstration of appropriate abstention. That test needs other ambiguous items so you can see whether the change overgeneralizes. It also needs high-confidence answerable items with narrow descriptions; otherwise a candidate that refuses everything may appear to have improved. Don't accept “all responses were cautious” as a result if the job was to route answerable records.

### Step 4. Let the contrast rule out a tempting diagnosis

Suppose a different panel's gains came only from shorter response text rather than more accurate labels. If the checker always required exact strings, then a transformation that removes extra words could turn a correct label plus explanation into a formal pass. That can matter for a user of the interface, but it is not evidence that the candidate reasoned better about object identity. Split the sample of failures into *format-only*, *label choice*, and *unsupported certainty* according to a predeclared rule. Some cases have multiple flags. Keep the leading rule or all flags explicit so counts are not accidentally added as if each refers to a different item.

The same policy suggests something practical: compare a baseline that reads an explicit type field if one exists. If it solves the common cases, you can reserve model input for records whose descriptions genuinely need a judgment call. You then need to evaluate the trigger for the expensive path, not just how good a classifier is after the trigger. A false trigger may spend unnecessary effort. A missed trigger may send a dubious result down a path with no review. One model score cannot settle a system decision that includes routing.

## Replicate the procedure before decorating the result

A reproducible setup starts with a versioned input artifact. It can be a short local Markdown file or three JSON files. Preserve the contract, demonstration items, held-out test items, and any transformations of evidence as distinct pieces. Save the exact assembled inputs if your environment allows it and contains no private material. A label like “used five-shot” is not an artifact. Another reader needs to know which five examples, in what order, with what answer format and at what point in the prefix.

Version tracking is especially important where an interface hides details. “Same product” is not always evidence of “same underlying run configuration.” Ask what you can actually pin. A hosted conversation may add instructions you can't see or run a model revision you cannot identify. You can still compare a pair within documented conditions. You should not turn that result into a precise claim about an architectural change outside your evidence. A readable limitation is a sign someone inspected the apparatus, not an admission the experiment was pointless.

If timing matters, measure both total turnaround and a declared portion, such as time until a usable reply. A system that begins streaming quickly might still finish an invalid result slowly. A system processing longer demonstrations might run into limits earlier. Measure these under comparable inputs; a single timestamp by itself will not distinguish network delay, queue time and inference. If none of those metrics was measured, don't infer a win from intuition alone. For an instructor's offline exercise the appropriate cost is often human review time, not provider cost.

### A small condition-drift rehearsal

Write three process revisions and predict how they'd affect interpretation:

1. The new team changes the decoder setting and adds examples.
2. The new team applies the same examples but tests against a different case panel.
3. The new team preserves prompt and cases, but moves an evidence selection rule into the preprocessor.

In case 1, you can compare two trial configurations, but not isolate the examples. In case 2, you can't distinguish a cue's effect from the second panel's difficulty unless you repeat both conditions on common cases. In case 3, you can inspect the full workflow, but a change in what records appear is not a pure prompt treatment. If the preprocessor is a material part of the intended system, compare integrated versions honestly rather than hiding the change. Technically different tests can all be useful. Their conclusions won't be interchangeable.

A small report can therefore distinguish four sentences: **what we changed**, **what was held fixed**, **what we observed**, and **what mechanism remains uncertain**. A reviewer can disagree about the fourth while accepting the first three. If you conflate them, a dispute about interpretation becomes a dispute about the data. The point of a design experiment is to prevent that.

## Put model and non-model choices in the same design review

Imagine a reader asks whether the system could improve simply by fine-tuning. Ask which track actually failed. If the intended evidence is absent from the prompt, changing parameters cannot establish a source citation for a specific current record. Improve access to allowed evidence and check provenance. If the label taxonomy is inconsistent across source owners, more model training cannot decide which policy the adopter wants. Fix the specification. If model behavior varies around a stable and independently verifiable interaction, you can explore controlled changes to prompt, model or decoding, matching the intervention to the observed problem.

There are reasons to try parameter updates in a different project. The table earlier distinguishes what changes; it does not say a method is universally better. Training needs its own evidence, data permissions, version control, compute and independent assessment. This book stops at a small inference comparison. Calling that a “model optimization” would obscure rather than clarify the work. We are designing an interface, testing a few mechanisms, and moving the burden of correctness to a checker wherever that is possible.

If a rule or lookup solves a case exactly, that is a success for the design, not a disappointment for the book. The route to a repeatable experiment is often subtractive. Remove a model from the source-of-truth role so you can identify what its assistance is for. Remove shared session state so you can test input effects. Remove guessed labels from examples so you can assess the declared rule independently. More prompt text is not the only available repair.

### Check your understanding with a two-lever design memo

Pick one error from U1–U7. Write a short memo recommending only one intervention to test now and one to reject for now. The memo should name the user consequence, distinguish changes to task definition from changes to text, and cite the data you actually saw. A usable model for U5 might say: “The failure is a false record label for a physical printed catalog. Test whether pointing at the deciding phrase reduces that specific confusion without altering the rule; on a new test panel, require at least one ordinary catalog record and one ambiguous printed object description. Do not lower the contract to accept extra guesses.” This does not tell you whether marking features is the right production tradeoff. It creates evidence you could use to choose later.

### Keep derived label counts separate from user cost

A model that marks a record needs_review sends work to a human. In a fictional workflow with four ten-minute human reviews, the direct cost is forty staff minutes. That matters even if the score treats each justified abstention as a pass. Conversely, saving ten minutes by confidently routing a genuinely ambiguous item may create a more costly correction later. Log the routing outcome separately from model timing. For a real comparison, estimate these costs with the people who do the work rather than choosing plausible values after seeing who won.

This is also a reason to build a simple baseline that delays decisions until existing metadata arrives. A good model comparison can show no obvious role for a model on the ordinary path. It can also point to a narrow, reviewable role for exceptional cases. The experiment earns its keep when it changes the workflow design, not merely when its score changes a ranking.

## Exercises

### Warm-up

1. **Literal check:** Do Object and object. pass the contract? Write the three accepted strings. Explain why accepting punctuation would be a versioned contract change rather than a classification gain.
2. **Token budget:** For the three toy tokens, hand-compute the T=1 and T=1/2 weights. Choose a draw that selects different labels and a draw that selects the same label. Use the [offline decoder](../lab/decoding.py) only after predicting.
3. **Input isolation:** Outline two prompts that differ only by a demonstration block. Name three other variables that must not change for the comparison.

### Application

4. **Minimal pairs:** Create two records that mention the same object but differ in what the row represents, and two cases that need abstention for different reasons. Don't use them as demonstrations.
5. **Purposeful ambiguity:** Add one demonstration of abstention to the prompt. Predict a benefit and a harm. Design tests for both rather than testing only the planned improvement.
6. **Diagnosis:** A condition's exact-match score rises, but every “fixed” output had the correct label plus punctuation in baseline. Describe what was improved and what was not. Give a separate measure for evidence quality.
7. **Reproducibility:** Two groups use different presentation orders and one leaves a prior conversation open. Design a receipt and procedure that could reveal either source of disagreement.

### Synthesis

8. **Design constraint:** Compare a direct label, a demonstration-based condition, and a condition with a separately checked evidence feature. Use the same test and output decoder. Identify what evidence would justify the added feature step and its human cost.
9. **Compare levers:** For each of a missing field, inconsistent expression of a stable label, and a changed decision policy, pick an intervention from the chapter. Defend what you would leave unchanged and what independent check would still be necessary.
10. **Live optional / offline equivalent:** Replay a designed set of candidate outputs or use the same permitted model on synthetic inputs twice under a predeclared schedule. Log every item, unchanged procedure, timeout and failure class. State which claims you may make about the procedure and which you cannot make about a general model population.

### Challenge

11. **Avoid favorable sampling:** Design a system where a memorized cue looks successful on development items and fails on held-out items. Spell out how you split the policy templates and what observation would refute your diagnosis.
12. **Make a model optional:** Sketch a classifier that uses a reliable structured field directly and a bounded model only when necessary. Test the routing decision separately. Show one case where the extra machinery is justified and another where it only makes the task harder to audit.

## What you can now do

You can design a baseline and compare a precise change without shifting the job, evaluate how token choices can differ under a toy decoder, and tell whether a change concerns evidence, configuration, training or the checker. You have tested why a demonstration can help with one kind of error and fail another. The next chapter asks a harder question: when a candidate chooses a legal label or cites a real record, did the evidence justify the claim?
