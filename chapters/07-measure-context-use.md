# Chapter 7 — Measure whether context can do its job
*There is room for the evidence. That does not put it to work.*

Imagine a community archive asks a reading assistant two questions about a tray: may a visitor take it out of the room, and when does it have to come back? The coordinator supplies every policy in a single packet. The response quotes a superseded notice. The packet had room for the current rule; the current rule even survived assembly. More capacity would not by itself explain the failure.

Now consider a deceptive twin. The response is word for word identical, but this time the assembler cut the document list before reaching the current policy. The user experiences the same wrong answer. The engineering task is different. In the first case, investigate what the system did with available evidence. In the second, fix how evidence reached the input. A trustworthy check must be able to tell them apart. This chapter builds that check.

## What you will be able to do

- Trace evidence from the authorized collection through the actual input packet to a scored response.
- Compare evidence position without simultaneously changing the evidence, question, and scorer.
- Measure complete support separately from correct extraction, justified abstention and cost.
- Decide when to test a larger packet, move or group information, add a deterministic retrieval filter, or leave the system unchanged.

Start with Chapter 3's difference between retrieval and verification and Chapter 5's matched evaluation panels. All archive material and responses here are invented. The offline lab runs no model. It lets you pin down the question before paying for or trusting a live experiment.

## Unpack the word context

Context is easy to count loosely and difficult to specify precisely. A folder holds ten thousand records. The search step chooses a subset. The orchestrator formats some of it into an input along with instructions, a question, optional conversation history and any earlier observations. An interface may accept a request, reject it, truncate it, summarize it or decline to expose what passed through. These are different observations. Preserve the distinction between what the system **could have seen**, what the caller **prepared**, and what the model **actually received**. If you can establish only one of them, say which one.

| Layer | Observable | What it doesn't establish |
| --- | --- | --- |
| Authorized collection | Which evidence could be selected | That it reached the input |
| Retrieval | Which IDs and versions were found | That every returned record was transmitted |
| Assembly | Which blocks, order, labels, and bytes the caller prepared | That an opaque endpoint preserved all of them |
| Model interface | Accepted input metadata or a known transmitted message, if observable | That a response used the facts correctly |
| Verification | Whether a response's facts and references satisfy the fixed rule | That a different prompt, model or workload would succeed |

Keep the distinction visible in a log. “Maximum input size equals observed supported-answer capacity” confuses at least two of these layers. A service's accepted request size is a condition for running some experiments, not proof that all facts and relationships in that request can be used reliably. Byte count also isn't token count. A byte count checks bytes; token counts depend on encoding/tokenization rules and the exact assembled text. A counted input from one endpoint is not an interchangeable measurement for another. Retain the unit and the version of whatever did the counting.

The question is not whether a long context is impressive. The question is whether a particular workflow finds, preserves, and applies the evidence it needs under its constraints. That includes plain context management, not only model internals.

### What the existing experiments motivate

[Liu et al., *Lost in the Middle*](https://aclanthology.org/2024.tacl-1.9/) vary where relevant information occurs in multi-document question answering and key–value retrieval. Position mattered in the settings they tested, and middle placement was often weaker. That is a reason to measure position in a workflow where order can change; it is not a law that the middle always fails or a mechanistic explanation for every provider's relative behavior.

[Hsieh et al., *RULER*](https://arxiv.org/abs/2404.06654) construct a benchmark with variable context and tasks beyond a single lookup, including tracing and aggregation. They show how stronger performance on a simple retrieval test can coexist with weakness on harder tasks as length increases. Draw a bounded design lesson: a retrieval-only needle test cannot settle whether your user can get a complete answer requiring several distinct facts. Both papers report specific experiments. Our teaching fixture is not a reproduction, and its authored results say nothing about model capability.

<!-- → [INFOGRAPHIC: six evidence records moving from archive to assembled packet to two checked claims; only one arrow drops a needed record] -->

## Build a panel that can answer one question

Suppose our fictional archive accepts questions with exactly two required facts. In this lab, the output contract is strict: return both facts with the exact two applicable IDs, or give an insufficient-evidence state with neither facts nor citations. A deployed assistant might support useful partial answers. Here we declare a full-only contract so a missing fact controls the expected state. That is a choice, not a definition of correctness in every archive.

Give each case one two-record block containing the required current policy and four one-record distractor blocks. The distractors are not noise generated afresh at every run. They are fixed by the case. Some contain a stale policy or an appealing hour that applies to a different event. The query, contract, block boundaries, record wording and scorer stay unchanged. Move the required block to the front, middle and end of the evidence list. Keep distractors in their original relative order. A fourth absence control replaces the required block with two benign notes, keeping the number of blocks and records, not necessarily their byte or token lengths. Because it changes the content, **absence is not a position condition**.

```text
front:   AUTH, F1, F2, F3, F4
middle:  F1, F2, AUTH, F3, F4
end:     F1, F2, F3, F4, AUTH
absent:  F1, F2, ALT, F3, F4
```

“Front” here means after the same fixed task and question, at the start of the evidence section, not before the provider's unseen instructions. Changing the position of evidence can also change which instructions or distractors are adjacent to it. Therefore the controlled comparison estimates a **layout intervention** across these packets, not a universal biological-style response to ordinal position. The test does not separate ordinal slot from distance to the question or dependency on adjacent records. If you need those effects apart, construct a second controlled factor with varied benign neighbors, deliberate question placement, or multiple matched packet lengths, and declare exactly which comparison supports which claim.

The same caveat applies to length. The authored front, middle and end packet bytes are equal for each case because the lab permutes the same pre-rendered blocks. An opaque service may format or tokenize a new boundary differently. You can check the precise byte equality in this local packet. Don't silently substitute it for claim about service tokens. For a live optional track, capture trustworthy token counts where available, and disclose invisible wrappers or truncation rules.

### Plan before looking at candidates

Read the [context lab handout](../activity/CONTEXT-LAB.md). Before scoring, retrieve one input packet:

```sh
python3 -B lab/context_lab.py plan B middle
```

The script prints the exact text and which records are visible. Its plan does not print the candidate or keyed facts. You can still reason out an answer from the records. Write the two required facts and exact IDs, then predict what an answer should do if just one required record is available. The included lab moves the two required clauses together. A later extension can split them; decide whether you want to measure position of a group or separation between dependent facts before editing the panel. The same heading should not hide a different intervention.

## Walk one case end to end

The west archive lends map sleeves. The case asks whether a sleeve may leave the room and when it must come back. Two current records answer the request:

- B-CURRENT1: checked-out sleeves may leave the reading room.
- B-CURRENT2: sleeves are due the next calendar day at 14:00.

Other records include old checkout-day language, a description of map-reading tables and a notice that the west desk starts accepting hold requests at 14:00. The critical issue is not whether 14:00 occurs in the input. It is whether the **event at that time** is sleeve return rather than hold intake. The record set lets an independent reader tell.

Suppose the author-supplied middle candidate returns the right access and deadline labels but gives the table description and the hold notice as evidence. A loose exact-answer scorer gives it a pass. The lab's fixed scorer rejects it as wrong evidence. The required records are there; increasing the retrieval budget alone isn't a repair for the observed problem. A useful next test would put two otherwise similar records side by side and ask the candidate to identify the event that each describes before committing a deadline. Preserve the exact same pass rule when trying that repair.

Suppose the absent candidate instead returns those same factual labels and lists the correct two IDs despite their absence. The keyed outputs happen to match, but the candidate cannot derive them from the packet. A scorer that checks the ID strings against the key without verifying they were supplied would give another false pass. In this exercise, that answer must be replaced by an insufficient state. You have not established whether a model remembered or guessed anything: the examples are authored. You have established what a system would need to prove about input provenance before accepting the candidate.

A third pattern is also useful. An answer can cite the correct records but return the wrong day. That is a checked factual failure, not a citation-eligibility failure. Once the correct IDs exist and applicable support was present, compare the specific semantic difference. For example, if a record says “the reservation day at 17:00” and the answer says “the next day at 17:00,” matching a time string is not enough. Feed a verifier the event and date units, not just an acceptable-looking clock range.

### Do not lose earlier failures in your error counts

The scorer emits one leading reason per candidate, not every possible reason. It checks shape, support availability, evidence identity, and then the answer. Case A in the middle condition cites an old rule and returns wrong facts. It is labeled wrong evidence because that check fails first. That does not imply the facts were right. If you intend to count every error, use distinct flags rather than interpreting leading-reason counts as an exhaustive root-cause analysis. This priority rule limits this tool's claims; it doesn't prove how any particular output came to be written.

The absence control deserves a separate metric. Put three supported-answer tests in one denominator and three strict abstention tests in a different one. A score that adds them without labels may make an aggressive guesser look useful on answerable data, or make a system that always refuses look safe and successful. Both mistakes obscure what the output contract actually requires.

## Score the authored comparison

Now run:

```sh
python3 -B lab/context_lab.py score
```

Here are the expected results, checked independently against the record set:

| Case | Front | Middle | End | Absent control |
| --- | --- | --- | --- | --- |
| A | supported answer | wrong evidence; also wrong facts | supported answer | supported abstention |
| B | supported answer | wrong evidence despite matching labels | supported answer | answer without complete support |
| C | supported answer | unjustified abstention | wrong facts | supported abstention |

Among positions containing complete evidence, front gives three of three supported answers, middle zero of three, and end two of three. The synthetic paired contrast front–end is one net improvement across three paired cases. Cases A and B are shared wins; C is the one disagreement in pass status. Front–middle differs on all three. Two of three absence responses correctly abstain. The values are not model performance estimates, not statistically representative, and were constructed to teach diagnostically useful subcases. A change to context order does not address every kind of error. One end candidate has the correct evidence and a wrong fact; one absence candidate asserts a fact without evidence.

Suppose a report only prints a 3/3 score for front. It omits other layouts and the control. You cannot tell whether the evaluator checked support, whether later record assembly altered availability, or how the system acts when the correct rule is missing. A minimal scorecard needs per-condition counts and case IDs, a statement of evidence availability, and the method of checking response, facts and provenance. Even a small panel can present enough information for a reader to challenge the design rather than simply accepting a headline.

### Budget experiment: position or delivery?

Now run:

```sh
python3 -B lab/context_lab.py plan B front --visible-blocks 2
python3 -B lab/context_lab.py plan B middle --visible-blocks 2
```

The first packet contains both B-CURRENT records because the packer keeps the first two **blocks**, and those records share a block. The second does not. It keeps two filler blocks. Even though the condition name says middle, the change no longer varies position alone. The required material is absent from the actual packet. A model might still return a correct-looking answer, but the reader can't justify it from the supplied evidence.

The block limit is ours, not a demonstration of model truncation. If your live system limits tokens, decide where constraints apply and log a real observable from the relevant stage. Keep some budget for the question, instructions and expected response as applicable to the receiving interface; allocation rules and token accounting differ by system. Legal or authorization boundaries should enter selection before content is prepared, not get cleaned up after data was disclosed. A teaching toy cannot establish provider privacy, hidden instructions, or exactly what the service retained.

There is another separation worth testing. The lab holds the two necessary clauses together. If you need to demonstrate how distance between clauses matters, split the required pair into separately marked blocks and ensure both were delivered in all compared layouts. Retain the exact record IDs and version. Compare fixed short distances against fixed long ones while balancing each clause's location. Otherwise a finding about distance might merely be an artifact of the harder record occupying a weak slot in one condition only. Start with one defensible comparison. A design with every factor changed at once can be complex without being informative.

## From a teaching case to an engineering decision

A longer packet costs something. At minimum you spend review attention. A real system may also have processing latency, input charges, privacy exposure and allocation competition between retrieved evidence and the requested task. Don't invent a stable ratio for any of those costs. Choose what matters and measure it in the same comparison. If you cannot measure a cost because an interface hides it, record that limit rather than making a price or speed claim.

Use three levels to design a repair:

1. **Assemble less on purpose.** A department, room or version filter can keep irrelevant records out. This can preserve space and reduce review. It may fail if metadata is absent or wrong. Test boundary cases from Chapter 3 where a filter that reads the wrong timestamp drops the only applicable clause.
2. **Present what remains deliberately.** Group clauses that jointly establish a decision, show record IDs, use stable boundaries, and clearly separate quotations from the task. This can make the audit easier. It doesn't guarantee that a model responds differently, and it cannot replace an independent evidence check.
3. **Test the next observed failure.** If both clauses were visible and the candidate cited a pickup notice as if it were a return requirement, enlarge evaluation of role and temporal semantics before adding more context. If the candidate never had the due-date clause, improve delivery. If it returns valid JSON with no supported facts, trace why a shape check was treated as a truth check.

A brief route can make a longer one unnecessary. When a user asks for one deadline from an authorized fixed table, a keyed lookup plus a known-format explanation may be better than feeding ten policies to a generator. When a user asks for a comparison among records requiring several independent facts and careful abstention, a bounded generator may help draft the explanation, but source selection and claim checks still need owners. The point is to preserve evidence and make the system testable, not to maximize the amount of material it handles.

### Copyable experiment card

| Field | Declare before running |
| --- | --- |
| User workflow | Which question type, source scope, answer or abstain rule, review owner |
| Manipulation | Position, length, retrieval method, or clause separation; name one first |
| Fixed factors | Corpus and versions, questions, labels, relevant evidence IDs, decision scorer, run schedule |
| Observable delivery | IDs and order actually supplied, evidence availability class, packet bytes and known token measure |
| Outcomes | Supported answers, abstentions, wrong evidence, wrong facts, missing/late candidates, time or charge only if observed |
| Cost and stop | Measurement window and budget, what will block or reverse rollout |
| Inference limit | Location relative to fixed prompt, actual model/settings if any, small sample, inaccessible or uncertain logs |

For a live optional design, independently construct more cases than the ones shown here. Freeze the conditions and bounds before running. Hold common settings where that is possible, reset unintended conversation carryover, and log paired cases and repetitions rather than silently replacing bad samples. With varying domain, consider grouped holdouts. Distinguish a service test from this authored demonstration. Use only permitted synthetic data, no external action tools, and no personal records. If a local deterministic experiment gives you the engineering answer you need, stop there.

## Exercises

### Warm-up

1. **Scope:** List three different statements someone could mean by “we sent all the documents.” For each, name a different verification artifact.
2. **Match conditions:** Predict the delivered record IDs and complete-support signal for case B at front, middle and end. Then check exact UTF-8 lengths, relative order of distractors and different hashes in the lab.
3. **Check support:** Explain why case B's absent candidate is wrong even if its access and deadline labels match the key.

### Application

4. **Diagnose:** Give a candidate for C that cites the right records but gets the event date wrong. Explain which check exposes it and what a digits-only scorer would miss.
5. **Budget:** Under a four-block prefix, predict the complete-support property of front, middle and end. Confirm it from the plan output. State why this is not a pure position experiment.
6. **Co-occurrence:** Separate the two required clauses into two blocks while retaining all distractors. Write one pair that changes separation but does not accidentally change whether both were delivered. Discuss the job-specific tradeoff with grouping.
7. **Abstention:** Propose a partial-answer rule for one missing clause. Write expected records for both missing, one present, and both present. Do not rescore the original panel as if the contract stayed the same.

### Synthesis

8. **System design:** One excellent short input produces a verified answer, while a longer packet gives an unsupported answer. Sketch two controlled experiments, one changing only layout and one testing selection. List all observations required to distinguish the failures.
9. **Outcome mix:** Report per-position supported-answer rates and separate absence-control correctness. Then predict how a scorer that accepts matching facts without citations changes the case-level result for the B middle and B absent cases.
10. **Review case:** Explain what evidence would make a metadata filter useful to an archive. Add two tests to catch a false rejection at a date boundary and overinclusion of a stale rule.

### Challenge

11. **Stress your inference:** Develop a panel with two independent facts, one fact that applies only before a particular date, and two sibling tasks that require the facts for different decisions. Avoid fresh generated filler per condition. Write an honest limit statement about adjacency, hidden context, and random variation even if one variant wins every item.
12. **Design a stop rule:** Suppose optional live runs can consume a bounded budget. Choose a falsifiable stop criterion and a set of traps that the best-looking configuration could fail. Define what evidence warrants a redesign rather than another run.

## What you can now do

You can separate what fit, what was delivered, what was cited and what was warranted. You can hold the question and evidence fixed while varying layout, preserve a clean absence control, and compare a non-answer against the full-support state rather than against a desire for confident prose. The next chapter converts that discipline into a search procedure. It asks how to try several prompt variants without letting repeated optimization teach the test its own answers.
