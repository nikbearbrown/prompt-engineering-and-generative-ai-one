# Chapter 3 — Ground answers in evidence
*A citation is a return address, not a proof.*

Imagine an answer says, “Reserved study kits can go home for seven days [P-2].” You click P-2. It is a real record with the words “seven” and “study kits.” It says to hold a reservation for seven hours. This isn't an invented citation. It's a real citation used to support a false claim. Checking whether a reference exists doesn't distinguish those errors.

**After this chapter:** separate retrieval, generation and verification errors; trace exact support for a claim; define when to answer, abstain or escalate. The entire library exercise below is invented.

## Three jobs behind the answer button

A retriever selects candidate evidence. A generator uses what it receives to form an answer. A verifier checks what the answer actually claims. A keyword search can miss a paraphrase. A similarity search can find the right topic without finding the right rule. Retrieval-augmented generation (RAG) joins generation to a retrieval mechanism. The [original Lewis et al. paper](https://arxiv.org/abs/2005.11401) combined a trained sequence generator with a dense document index and retriever; the simple filter in this lab isn't a recreation of that architecture. Retrieving material does not guarantee that the answer follows from it.

With three allowed records you can pass all three and concentrate on verification. With a large or restricted collection, you may need to search and limit what goes in. This can reduce context and review work, but excludes evidence and introduces gaps. Access restrictions belong with the data and retrieval paths; an answer shouldn't disclose a record simply because it was topically helpful.

<!-- → [INFOGRAPHIC: retrieval, answer, and verification stages annotated with separate failures] -->

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

## Change one stage to find the problem

Remove P-1 but leave the others visible. The generator can only abstain correctly now. That doesn't mean retrieval succeeded: the full collection had an applicable record. Restore P-1 as an independent control. If the candidate still misreads the unit or chooses the archived policy, then more retrieval alone isn't a sufficient repair. A trace can record what the system was allowed to see, what was retrieved, and what was cited. Each field answers a different question and should be logged without sensitive record content unless needed and authorized.

A stable record ID, exact supporting passage and revision make the result checkable. None of them can make a false claim true. This exercise uses a validity column supplied by the case author; deployed applications still need someone with actual policy authority to establish that status.

## Exercises

- **Warm-up | Trace support:** Separate “The kit is held seven hours and can go home overnight” into claims and label each supported, contradicted or unsupported under current policy.
- **Application | Diagnose:** Give a correct abstention with only P-2 present. Name the evidence problem distinguishing it from the end-to-end answer.
- **Synthesis | Test partial evidence:** Design a question where P-2 answers one clause and no record answers the other. Write a test that rejects invented support even if one clause is correct.
- **Challenge | Set limits:** Propose trace fields to diagnose wrong scope, stale sources and official-looking irrelevant citations, without copying private records into logs.

A citation can settle what an answer may claim. It cannot authorize the assistant to change inventory, send a notice or execute an order. That is a different boundary.
