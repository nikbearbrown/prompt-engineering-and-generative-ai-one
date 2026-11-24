# Chapter 3 — Ground answers in evidence
*A citation is a return address, not a proof.*

Imagine an answer says, “Reserved study kits can go home for seven days [P-2].” You click P-2. It is a real record with the words “seven” and “study kits.” It says to hold a reservation for seven hours. This isn't an invented citation. It's a real citation used to support a false claim. Checking whether a reference exists doesn't distinguish those errors.

**After this chapter:** separate retrieval, generation and verification errors; trace exact support for a claim; define when to answer, abstain or escalate. The entire library exercise below is invented.

## Three jobs behind the answer button

A retriever selects candidate evidence. A generator uses what it receives to form an answer. A verifier checks what the answer actually claims. A keyword search can miss a paraphrase. A similarity search can find the right topic without finding the right rule. Retrieval-augmented generation (RAG) joins generation to a retrieval mechanism. The [original Lewis et al. paper](https://arxiv.org/abs/2005.11401) combined a trained sequence generator with a dense document index and retriever; the simple filter in this lab isn't a recreation of that architecture. Retrieving material does not guarantee that the answer follows from it.

With three allowed records you can pass all three and concentrate on verification. With a large or restricted collection, you may need to search and limit what goes in. This can reduce context and review work, but excludes evidence and introduces gaps. Access restrictions belong with the data and retrieval paths; an answer shouldn't disclose a record simply because it was topically helpful.

<!-- → [INFOGRAPHIC: retrieval, answer, and verification stages annotated with separate failures] -->

### Give the handoffs names

When someone says that the model “used the library records,” there are several claims hiding in the verb *used*. Did the record exist in the collection being searched? Did it make it into the shortlist? Did its decisive sentence survive the handoff to the answer generator? Did the answer cite it and preserve its meaning? A yes at one handoff answers nothing about the next.

Write down what crosses each boundary. The search stage receives a query and an allowed collection, and produces candidate record IDs. The context-building stage chooses which parts of those records to deliver. The answering stage gives a decision and cites support. The review stage can inspect the decision against exact passages and their applicability. That last stage must be able to reject the answer. If the review only reformats the same answer or repeats its confidence, it isn't doing that job.

Take the fictional library example. Say a search trace lists P-1 at rank one. The context passed downstream includes only P-1's heading, “Reserved study kits.” The decisive due-time sentence is missing. If the answer gives the wrong due time, “P-1 was retrieved” is true in one sense, but calling this successful delivery of evidence would wrongly absolve a broken handoff. A smaller context can be useful; a shorter context without the required clause cannot establish the claim. Log a passage identity or revision, not just the title of the document.

In the opposite direction, imagine P-1 was present verbatim, and the answer put closing time on the following day. Increasing the shortlist from three to eight doesn't fix an answer that misreads the clause it already has. Make that failure reproducible by fixing the visible passage and looking first at interpretation, not at search ranking. If a change in ranking happens to fix this one answer, it is not yet evidence that your diagnosis was right.

For a small and authorised collection, begin with a complete read as a control. That doesn't require giving all the material to a generator in a real application; it requires a reviewer who can establish what support exists in the allowed collection. A control with the decisive evidence visible asks what the answer stage can do under that narrower condition. It doesn't estimate how often the actual search will put that evidence there.

### Define the question before judging the records

“What are the kit rules?” is not a well-defined evaluation item. There might be rules about pickup, use, return, fees and renewal. A reviewer who judges the answer against all of these could penalise it for omitting irrelevant details. A reviewer who accepts any one fact could miss a decision the patron needed. Break the request into the decisions it actually asks for, and specify the jurisdiction, the item and the date if those can change the decision. If the request is underspecified in a consequential way, asking a short question can be more useful than retrieving more broadly.

Here the patron specifies the current central-desk policy, a reserved study kit and a checkout. Two requested decisions are separable: where the kit can be used, and when a checked-out kit is due. A hold is not a checkout. Closing time on a given day is not a known hour unless a schedule says so. The answer can be complete at the requested level without guessing that hour. An evaluator should not silently add a request for the closing hour, just as an answer should not silently discard a request for the due time.

## Read the clauses, not the keywords

| ID | Validity | Excerpt |
| --- | --- | --- |
| P-1 | Current policy, central desk | Reserved study kits are for in-library use. Return them to the central desk by closing on the day of checkout. |
| P-2 | Current operations note, central desk | Hold a reserved study kit for seven hours after the pickup notice; after that it becomes available to others. |
| P-3 | Archived central-desk policy | Reserved study kits may be borrowed overnight for one night. |

**Question:** Under current central-desk policy, may a patron take a reserved kit home? When is it due once checked out?

Before reading the solution, mark words that settle each half. Now check the candidate at the top of the chapter. P-2 describes the duration of a hold *before checkout*. It does not govern lending, and its unit is hours. P-3 describes lending but is archived. P-1 answers both questions: **No. The kit is for in-library use and must be back at the central desk by closing on the checkout day [P-1].**

Source eligibility, relevance and support are different tests. An eligible operations note can still apply to the wrong event. A topically relevant archived policy can be ineligible. Recognition of the word “seven” is not preservation of the unit. Write down the exact phrases that settle permission and due time, not just a record ID.

Ask about a branch library or a late-fee amount. These records don't establish either. “The policy never charges a fee” and “the records don't establish a fee amount” are different claims. If one half is supported, report that separately. For two conflicting eligible policies, a maintainer needs an explicit priority rule or manual escalation. Choosing the last result is no substitute.

### Version is a fact about a rule, not a decoration on a document

Use a new, invented example to make dates do real work. A fictional tool room lends practice meters. The record identifiers in this table refer to versions of the rules, not to live policies. The room's contract says effective dates are inclusive and end dates are exclusive. No end date means no end date is given; it doesn't guarantee the rule will stay in force forever.

| Record | Kind and scope | Applies on | Exact rule in this example |
| --- | --- | --- | --- |
| M-1 | Checkout rule, east room | May 1 through May 31 | Practice meters are due two calendar days after checkout. |
| M-2 | Checkout rule, east room | June 1 onward | Practice meters are due one calendar day after checkout. |
| M-3 | Pickup rule, east room | May 1 onward | A reserved practice meter is held until 18:00 local time on the reservation date. |
| M-4 | Return-location rule, east room | May 1 onward | Return practice meters to the east counter. |
| M-5 | Checkout rule, west room | May 1 onward | Practice meters are due four calendar days after checkout. |

For this exercise, the text contains no due hour and no statement that a day should be skipped when a room is closed. Ask: “I checked out an east-room practice meter on May 31. What day is it due, where do I return it, and what hour is it due?”

First isolate the three decisions. The **day** needs an east-room checkout rule applicable at checkout and the known checkout date. At that date M-1 applies; adding two calendar days gives June 2. M-2 is in force by the due date, but the question's contract selects the rule at checkout, not at return. If the organisation applied new rules retroactively, that would be a different contract needing an authoritative statement. The **place** needs M-4. The **hour** is not established. M-3's 18:00 goes with a reservation's pickup deadline, not with an actual loan's return. M-5 explicitly concerns the wrong room.

A defensible answer says: “For a May 31 east-room checkout, the two-day checkout rule makes the due date June 2 [M-1]. Return it to the east counter [M-4]. The supplied return rules don't specify a due hour.” The answer can explain the arithmetic without quoting every record. The exact date came from both the user-stated checkout date and M-1, not from M-1 alone. If that checkout date were unconfirmed, a conditional such as “If the checkout was on May 31…” would keep the assumption visible instead of passing it off as a verified fact.

Now change only the date to June 1. M-2 supplies one day, so the due date is again June 2. The headline result is identical; its justification has changed. An evaluation that compares only the returned date would accept a system citing the wrong version in one of the two cases. Move the second date to June 2. The correct due date becomes June 3. A system that merely repeats the June 2 outcome now fails on the answer as well. Together these cases distinguish remembering a prior result, selecting by time and checking the actual evidence.

### Prefer a checkable claim ledger to a pile of references

A ledger is a small review table, not a transcript of a model thinking. Its entries should let an independent person reconstruct the answer. The proposed value and the evidence belong in separate columns so that a server or reviewer can reject one without losing the other.

| Claim requested | Proposed value | Source and calculation | Review |
| --- | --- | --- | --- |
| Due date | June 2 | User states May 31; M-1 gives two calendar days and applies on May 31. May 31 + 2 = June 2. | Supported as conditional on stated checkout date |
| Return place | East counter | M-4 applies to east-room meters and explicitly names the counter. | Supported |
| Due hour | 18:00 | M-3 says 18:00 for pickup of reservations, not for return. | Unsupported as a return hour; remove it |

The reviewer can check three rows without reading the model's entire answer as if it were a single indivisible allegation. “18:00” is a real value. M-3 really says it. A citation validator that checks only the occurrence of that number and the existence of M-3 would pass a false statement about the return hour. Requiring the *event* to match prevents this failure. The time at which a record was downloaded can't stand in for the time when its rule applies.

Likewise, a string can be copied faithfully from a record and still not support a claim. Suppose a candidate writes “M-1 says ‘due two calendar days after checkout,’ so all meters at every room follow the two-day rule.” The quote is exact; the expansion from east room to every room is not. A quote field is useful for review, but the test also needs the subject, event, scope and effective version. When an answer joins two cited passages, record which passage supports which part. An undifferentiated pair of citations makes a reader do the evidence matching again; it can also conceal a clause with no support at all.

### Do not resolve disagreement by hiding a record

Imagine a sixth record, M-6, explicitly states three calendar days for east-room checkout on May 31, and no documented priority decides M-1 versus M-6. That is not simply a missing fact. The relevant allowed collection contains two incompatible rules. You could still report that the return counter is the east counter because neither checkout rule changes M-4. You should not promise a due date. Say that the checkout records disagree and identify the applicable alternatives if both are authorised to share. An organisation could enact a priority rule for such cases, but retrieval order, a higher similarity score, or a filename ending in `final` cannot enact one.

There is a subtler version in which both rules give the same answer to the patron's immediate yes-or-no question, while the governing policy numbers disagree. Whether that is a conflict you must surface depends on the task contract. The repair-desk lab treats different applicable caps as a conflict even when the proposed mass exceeds both. A different application might report “No under either cap; the published limits disagree,” but that would be a different outcome with its own acceptance criteria. The important error is burying policy disagreement because the current item fell on the same side of two thresholds.

## Change one stage to find the problem

Remove P-1 but leave the others visible. The generator can only abstain correctly now. That doesn't mean retrieval succeeded: the full collection had an applicable record. Restore P-1 as an independent control. If the candidate still misreads the unit or chooses the archived policy, then more retrieval alone isn't a sufficient repair. A trace can record what the system was allowed to see, what was retrieved, and what was cited. Each field answers a different question and should be logged without sensitive record content unless needed and authorized.

A stable record ID, exact supporting passage and revision make the result checkable. None of them can make a false claim true. This exercise uses a validity column supplied by the case author; deployed applications still need someone with actual policy authority to establish that status.

### Separate absence, exclusion and deletion

A single “no evidence” indicator hides different mechanics. The allowed corpus may have no policy covering the question. Useful records may exist, but the current reader might not be authorised to inspect them. The search may miss an in-scope record, or the context builder may drop it after search. The caller often needs the same safe answer in these cases: don't claim more than what can be disclosed. The maintainer needs a sharper diagnosis.

You cannot always tell a caller what is missing without exposing it. Do not say “I found a confidential record that answers your question,” merely to make the system sound helpful. The visible message can say that the available material does not establish the answer. The trace can record the authorised collection used, the type of material searched, the known checkout date and the list of evidence that crossed the handoff, without disclosing other collections. A reviewer with a different scope must review their own authorised material, not route it into the original response through the review channel.

Also distinguish *no known deletion* from *known deletion*. An index may still return an identifier whose record is no longer in the current corpus. The correct lookup should mark the identifier unavailable rather than reconstructing its old passage from the heading. If a later review cannot recover a past version, it can establish that an ID once appeared in the trace, not verify the vanished passage by assertion. This is why a revision can matter even when the publisher never changes the record's title.

A useful review sequence is to replay three states separately:

1. **Allowed-corpus control:** a reviewer decides what an ideal search could have found. Mark a truly absent rule as absent, not a retriever failure.
2. **Visible-evidence control:** a reviewer checks whether the decisive clause, not only its title, reached the answer stage.
3. **Answer check:** a reviewer judges the answer using what was eligible, visible and actually cited. If the answer got the right value for the wrong reason, record both facts.

The controls do not require secret access, a different AI provider, a large model or logging private text. They require an independent source judgment for precisely the fields a reader relies on. In the kit case, every step can be reconstructed by hand.

## Measure retrieval without letting it borrow credit from the generator

Take a new synthetic question about checkout and suppose two admissible clauses are required: one says the kit does not leave the library, another says when it comes back. If a retriever returns the due-time clause plus one irrelevant notice, its retrieved set contains one of the two required clauses. In this exercise, **recall of required clauses** is one divided by two. The returned set has two records, one required, so its **precision for required clauses** is also one divided by two. Those happen to match, but they describe different denominators.

Return the due-time clause, the lending clause and eight irrelevant records. Under our labels, recall is now 2/2, precision 2/10. The answer generator got what it needed, at a cost: more irrelevant text to process and more chances for a response to pick the wrong clause. Neither metric determines which configuration is better. The more useful statistic may be the share of cases where *every* required clause was visible, especially when a partial policy answer would be misleading. A user who only asked about due time could be served by the smaller set. Score against the question, not against a global list of supposedly relevant records.

Don't declare retrieval correct if the answer happened to match a fact missing from the input. A model could supply the right answer from memory, guess, or infer from something else. Evaluate end-to-end correctness and evidence behavior separately. A strong result in one column cannot erase absent provenance in another. The inverse matters too: an attractive answer can be wrong even with perfect retrieval. Run the known-good evidence control when deciding which component deserves engineering effort.

### A four-item retrieval review you can reproduce by hand

Return to the invented meter room. In this table each record represents one decision clause. Pretend two configurations produced the **listed candidate sets**; these sets are constructed for comparison, not collected from a service. The reviewer reads the whole synthetic corpus first and declares which eligible clauses are necessary for each task. In Q4, suppose the collection includes the M-6 conflict described above.

| Task | Declared necessary clauses | A delivered | B delivered |
| --- | --- | --- | --- |
| Q1. May 31 east-room due date and return place | M-1, M-4 | M-1, M-3 | M-1, M-3, M-4 |
| Q2. June 1 east-room due date | M-2 | M-2 | M-2, M-3 |
| Q3. May 31 west-room due date | M-5 | M-3 | M-3, M-4 |
| Q4. Do the May 31 east-room checkout deadlines agree? | M-1, M-6 | M-1, M-4 | M-1, M-4, M-6 |

Count a hit only when a delivered clause is in that row's required set. A has 1 + 1 + 0 + 1 = 3 hits in six delivered clauses. B has 2 + 1 + 0 + 2 = 5 hits in ten. Aggregate precision across clause deliveries is 3/6 for A and 5/10 for B: both 50%. There are six required clauses counted across the tasks, so aggregate recall climbs from 3/6 to 5/6. All required support is present only in Q2 under A and in Q1, Q2 and Q4 under B. **Complete-support coverage** on the four questions rises from 1/4 to 3/4.

Here the same aggregate precision hides a meaningful change. The four extra deliveries bought two extra hits, each on a different previously incomplete question. If you averaged per-question recall instead, the delivered-support fractions for A would be 1/2, 1, 0, 1/2, averaging 1/2. For B they would be 1, 1, 0, 1, averaging 3/4. The calculations sound similar because both call themselves recall. One weights a question by how many clauses it needs; the other gives each question equal weight. State your unit and method before comparing.

The persistent miss, Q3, would be lost in a success headline. M-5 covers the west room; an extra east-room note doesn't help. A safe answer while M-5 is not visible would say the delivered evidence doesn't establish the west deadline. That is good behaviour in the answer stage and still a retrieval miss relative to the allowed corpus. Review the false negatives by scope, date, missing passage and missing record instead of prescribing a uniformly larger shortlist.

If two equivalent approved clauses can independently establish a fact, the all-required-set rule in this exercise is too strict. For example, if both an approved bulletin and an approved copy of M-4 state the exact same return location, either can meet that part of Q1. Define the equivalent alternatives before evaluating. Do not count copies of the same rule twice or treat two conflicting clauses as interchangeable alternatives. If an item really is unanswerable in the allowed corpus, its required support set is empty. Clause recall for that item has no needed-clause denominator; report that case separately as a test of appropriate abstention or escalation rather than silently treating it as 0% or 100% recall.

### Stop citing documents when the decision lives in a clause

The unit of checking is a claim. Identify its subject, condition, quantity or unit, and time scope. “All kits may leave the library” adds the quantifier **all**, even if a footnote permits taking home one kind of kit. A clause referring to a central-desk kit doesn't decide a branch kit. A rule that begins after the reservation notice doesn't govern what happens after checkout. When you audit a response, mark the extra assertion as a separate claim instead of approving the whole sentence by topic similarity.

A useful record for each atomic claim has four fields: claim text, evidence span, why the span applies, and disposition. Disposition can be direct support, a derivation with stated assumptions, contradiction, or insufficient evidence. When a conclusion is calculated rather than quoted, include the calculation and check which source record supplied each input. Exact quotation is not required for insight. It is required that the insight can be reconstructed without taking the generator's word for it.

Suppose a learner says, “P-2 does not mention fines; therefore there are no fines.” The exact selected text, “after that it becomes available,” doesn't decide charges. A reviewer can still praise the student's citation location while rejecting the inference. This is why citation validity, eligibility, support and completeness are useful separate criteria. Give credit where it was earned without issuing a false pass.

### Design a failure path you would want to receive

Abstention is an output design, not a sign the system ended unexpectedly. “Current central-desk policy states when to return kits but doesn't state a late fee” is useful; “cannot answer any part of the question” wastes evidence. “Likely no fee” makes an unsupported substantive claim. A response contract can allow partial answers, cite their scope, list missing facts, and say which person or record could resolve the question without contacting them on the user's behalf.

There is a cost to being conservative. A weak retriever can make a cautious generator look useless, because it rightly abstains. Keep the distinction visible so you can fix the evidence path rather than instructing the answer system to guess. Review answerable and unanswerable cases separately. Otherwise, a system that answers everything and a system that answers nothing can each look good by selecting the right denominator.

## Executable lab

Use the [repair-desk exercise](../activity/RETRIEVAL-LAB.md) to compare a literal ranking baseline to full-corpus metadata filtering. Its date boundary and overlapping-policy fixtures test failures that topical relevance alone cannot detect.

### Bring the lab failures back to the answer contract

Open the lab instructions before running a script; they give you the policy contract and ask for a prediction. The relevant table has five records across the north and south desks, including N-2, which reports a time to notice, not an in-scope mass cap. Pick D1, D2 and D4. For each, predict first what a top-one word-overlap search delivers and then what the full-scope filter would deliver. Write one sentence the answer stage could truthfully emit under each condition. Do not read a field name as permission to act on its value.

Pay attention to D4. With only one south cap, the logic can correctly conclude that an 11 kg item exceeds the cap it sees. With both south caps the lab reports conflict, even though 11 also exceeds the other cap. This is the kind of false assurance that an accuracy test based only on an assumed yes/no policy can conceal. The system didn't choose an arithmetic error; it failed to preserve the authoritative disagreement required by the contract. See how the conclusion changes when the configured shortlist raises from one to two without changing the decision code.

Now run an ablation you design. Keep the synthetic records, limit and policy contract fixed, and change the in-scope date by one day across a version boundary. Scope and temporal selection have changed even if the slate of word-overlap matches hasn't. A test that changes the wording, date and room together could reveal a failure but would make its cause harder to isolate. Keep one interesting difference per comparison where you can. When multiple dimensions must move together, name them rather than attributing any uplift to one.

In a real workstream, the success measure also needs a cost description. A complete read of five allowed records is inexpensive in this exercise; a complete read across thousands of records might be too slow or disclose material the answer stage doesn't need. Compare a cheap scope-and-date filter plus a smaller ranker against the current system under the same permission limits. Count decisive clauses delivered, look for the specific situations still missed and verify the resulting answer. The fact that a control solves the toy task is useful engineering evidence, not a blanket recommendation to pass every record to a model.

### Write down enough to repeat the diagnosis

A useful run card identifies the exact question and requested scope, the as-of date and the rule for which date matters, the corpus revision, the retrieval configuration, the delivered passage identities and the expected decision categories. For a lab, add the fixture revision and the command you ran. For a restricted collection, use only the trace metadata you are permitted to retain, and keep that trace within the same access boundary as the records it describes. Recording revisions makes a repeatable test possible; it doesn't make a confidential passage safe to export.

Make the baseline and repair answer the same task. If A evaluates the policy at checkout while B evaluates it on the review date, the chosen rule can change without a retrieval improvement. In the May example, that change could even save the answer-value score while corrupting the rationale. First reproduce an input where only scope filtering changes. Then compare passage coverage with the contract fixed. If you need to revise the policy-time rule too, report its effect separately rather than treating it as a hidden search setting.

## Exercises

- **Warm-up | Trace support:** Separate “The kit is held seven hours and can go home overnight” into claims and label each supported, contradicted or unsupported under current policy.
- **Application | Diagnose:** Give a correct abstention with only P-2 present. Name the evidence problem distinguishing it from the end-to-end answer.
- **Synthesis | Test partial evidence:** Design a question where P-2 answers one clause and no record answers the other. Write a test that rejects invented support even if one clause is correct.
- **Challenge | Set limits:** Propose trace fields to diagnose wrong scope, stale sources and official-looking irrelevant citations, without copying private records into logs.

- **Warm-up | Preserve units:** Explain why a correct quote of “seven hours” can be wrong evidence for a due time. Name the event and the item, not only the unit.
- **Application | Audit a version boundary:** For May 31 and June 1, write the meter-room due date, version and calculation. Predict why a test that checks only “June 2” misses a version error. Introduce one case whose due date changes.
- **Application | Count support:** Calculate complete-support coverage for A and B after changing Q3 to a candidate set containing both M-5 and M-4 in B only. Explain whether the extra M-4 counts as support.
- **Synthesis | Diagnose an apparent win:** Find a toy example where an answer matches the key even though no required clause was delivered. Give separate outcomes for the retrieval test, answer-value test and citation-support test. Say at which stage a corrective change belongs.
- **Synthesis | Preserve scope:** Design a response with one supported answer, one missing fact and one open disagreement. Separate what can be shared, what the user can do next and what the system has not done.
- **Challenge | Teach the tradeoff:** Propose a baseline, a small test set and a metric for a situation where returning more evidence increases both complete-support coverage and unnecessary exposure. Keep authorisation constraints unchanged. Show one test where revealing even the existence of a restricted record would be unacceptable.

**Takeaway:** retrieval is an evidence-delivery job; generation is an interpretation job; verification is a decision about whether the claims survive inspection. A single final answer score can hide a broken handoff. Mark the smallest reproducible counterexample, hold the next stage fixed, and test the boundary that failed.

A citation can settle what an answer may claim. It cannot authorize the assistant to change inventory, send a notice or execute an order. That is a different boundary.
