# Chapter 4 — Bound what a tool-using agent may do
*Permission belongs to the runner, not to the sentence.*

Suppose a repair desk asks for a draft recommendation when spare hinges fall below two. A model returns “Reordered three hinges.” Did it place an order? Could it? Don't resolve that by rereading the instruction. Inspect which operations the runner exposes, where it decides permission, and what a trace can establish.

The stakes look small. They're still real distinctions. A person reading “reordered” may do nothing because they think the shelf will be replenished. Another may submit a real requisition because they don't believe the message. The same sentence has nudged two people in opposite directions. You can fix the sentence by saying “I recommend three hinges.” You still haven't established whether the program can submit an order. Correct prose and a correct boundary are two deliverables.

Put the pieces on a workbench. On the left is a record of what the desk asked for. In the middle is a proposed quantity. Beside it is an independently supplied inventory snapshot. On the right is a runner: ordinary code that decides whether to look up an item, evaluate a proposal, ask for review, or stop. The model might propose terms, but it doesn't get to connect the pieces itself. If you remove the order interface, even the most convincing invented approval can't make the runner use it. If you keep an order interface close at hand and rely on a polite sentence to restrain it, you built a different system.

This is an exercise in *subtraction*. We could give the toy assistant more operations and then try to write conditions for every way those operations might be combined. Instead, we specify a smaller job: read trusted fixture data, return a reasoned recommendation, and refer the final decision to a person. When the runner ends, nothing has been ordered, sent, reserved, or changed. The cost is tangible: a person still has work to do. That isn't needless friction unless the task actually authorized the next step. Saving a click by erasing the distinction between reviewing and acting is a bad trade.

**After this chapter:** specify a read-only operation and typed suggestion; exercise stale state, bounded retry and a human review stop; test absence of effects independently of a message. The lab uses only a fictional in-memory inventory. No model account or external tool is needed.

You should be comfortable reading a small object with named fields and following the contract checks in [Chapter 1](01-describe-the-task.md). [Chapter 3](03-ground-answers.md) distinguished the presence of evidence from its relevance. Here we add one more distinction: evidence can justify *what you recommend* without changing *what you may do*. Keep an account of which piece settled which question. You'll use that account to write independent tests, not just a nicer prompt.

## Put the boundary in the interface

A suggestion is structured data: item code, positive integer quantity and source revision. A caller must decide what to do with it. Our runner can read the inventory and evaluate the suggestion. It cannot write inventory or place an order. Review means accepting the plan, not applying it. No use of the word “approved” can install a missing capability.

| Interface | Input | Output |
| --- | --- | --- |
| Read inventory | Exact code | Count, target, revision |
| Evaluate suggestion | Item, positive quantity, revision | Pending review or rejection |
| Review proposal | Human decision supplied outside the suggestion | Approved plan or denial |
| Submit order | Not present | Not present |

Don't picture these four rows as four tools issued to a model. They're the *roles* inside the example. The lab has a single local function, `evaluate_proposal`. It examines the provided dictionary and simulates separate read and review steps. It doesn't generate language or call an inventory service. That is useful: we can inspect the control flow without wondering whether the output changed because a model sampled a different word. A more complicated implementation would owe the reader the same separation, even if its parts were spread across separate processes.

### Decide what belongs to whom

Here a *capability* is an operation the runner can actually perform. *Authorization* is permission to perform a particular operation under specified conditions. The runner can read the fixture. The job authorizes reading only what is needed for a recommendation. The runner cannot order. The job doesn't authorize ordering. Those last two sentences describe different facts: one is about implementation and one is about a decision. Keeping them separate makes review much easier.

Consider a fictional replacement desk. Its planner is allowed to view item counts but not customer contact details. Its staff system needs both. If the planner and the staff system use the same broad access by default, the planner's promise to read only counts is a rule the implementation must enforce on every path. Give the planner a narrow view containing counts and omit the contact fields from that view. Now an entire category of accidental reads is out of scope for this interface. This isn't an instruction to adapt the lab to contact records. It's a method for deciding which information a plan even needs. Narrowing what the runner can read also narrows what it can accidentally include in the answer.

| Question | Who settles it in this exercise? | What cannot settle it? |
| --- | --- | --- |
| What did the desk ask for? | The task contract: draft a recommendation | A stronger verb in a generated sentence |
| How many hinges are recorded? | The supplied fixture revision | The proposal's own claim |
| Is this proposal allowed under policy? | The function's deterministic checks | The object's appearance or a reviewer flag alone |
| Did a person approve this plan? | In the lab, an independently supplied simulation value | A field invented by the proposal |
| Could anything be ordered here? | The exposed interface and implementation | A successful status or a clean prose answer |

The word *trusted* is local to a claim. We treat the supplied count as the fixture's count at its revision; we don't treat it as proof that a real shelf contains that many hinges. We treat the simulation's review argument as a stand-in for a genuine review decision; we don't treat it as proof that somebody with a job title clicked a button. Production systems have to establish both propositions through their own evidence. The lab supplies neither a person nor a shelf.

### Make the proposal carry only the necessary fields

Here is the candidate for the worked example, shown in JSON to make the field boundary visible:

```json
{"item": "hinge", "quantity": 3, "revision": "R17"}
```

The program receives a Python dictionary equivalent to this object. It expects *exactly* these three keys. It checks that `item` and `revision` are strings and that `quantity` is an integer greater than zero. An item string is not confirmation that such a record exists; a revision-shaped string doesn't tell us the current revision. Type checks catch impossible representations. Lookup and version checks establish whether a well-formed representation refers to the right evidence.

In Python, a value such as `True` might be accepted by a loose integer check; the lab deliberately checks the exact type. This is not a riddle about languages. If an item count is expressed as “some,” you don't get to convert it into a unit count by guessing. Likewise, the string `"3"` is text, not the integer `3` under this contract. Agreeing to parse it would be another input rule. Right now, the narrow rule helps you inspect what is known instead of guessing which inputs the runner normalized.

The strict key check rejects a fourth field rather than quietly dropping it. This makes it difficult to mistake arbitrary extra text for something the interface acknowledges. There is a downside: if a future legitimate client needs a new field, it'll have to negotiate a new contract instead of quietly sending one. That is an acceptable cost when the output must not shift the authority boundary. A tool meant for generic notes might choose a more flexible structure for descriptive annotations. It would still need to decide which fields carry business meaning and which cannot make decisions.

The proposal carries a revision because the same quantity may be right on Tuesday and wrong on Wednesday. The revision is part of the thing being judged. Put the source lookup and the decision on opposite sides of that division: the proposal claims a revision; the trusted fixture supplies the revision against which the claim is checked. Have the caller provide the simulation review separately. A statement inside the proposed text is not its own reviewer.

<!-- → [INFOGRAPHIC: read → validate → pending review → approved plan, with separate stale, retry and denied stop paths; no action arrow] -->

## Walk through successful and failed paths

The toy policy says to recommend replenishment when the count is **below 2**. A permitted proposal brings the count to the target. At revision R17, the only fixture item is hinge, the count is 1, and the target is 4. Because `1 < 2`, the trigger fires; the deficit is `4 - 1 = 3`. A proposal for 2 leaves the count short. A proposal for 4 exceeds the target. At count 2, the trigger does *not* fire, even though `4 - 2 = 2` is a positive deficit. One test asks whether to recommend; the other asks how much. If you implement only the arithmetic, you silently change the desk's policy.

The ordering of checks tells you what the design values. First check the caller's simulation controls. The separate review input can be `None`, `True` or `False`. The number of simulated transient failures is a nonnegative integer. Misusing either raises an error; it is not an inventory outcome. Then check the proposal shape and types. Don't read anything for a proposal the interface can't interpret. Only after that, try the simulated read. On a successful read, check item existence, revision, and policy in that order. A current positive number may still fail if it's the wrong number, and a valid review cannot repair missing evidence or a bad proposal.

| Condition at its check | Status | End of trace |
| --- | --- | --- |
| Wrong keys or not a dictionary | `invalid` | `invalid_shape` |
| Wrong value type or nonpositive quantity | `invalid` | `invalid_type` |
| Both read attempts failed transiently | `unavailable` | `stop` |
| Read succeeded, item not in fixture | `invalid` | `unknown_item` |
| Read succeeded, current revision differs | `stale` | `revision_mismatch` |
| Revision matches, quantity or trigger fails | `invalid` | `outside_policy` |
| Contract checks passed, no decision supplied | `pending` | `pending_review` |
| Contract checks passed, review denied | `denied` | `review_denied` |
| Contract checks passed, simulated review approved | `approved_plan` | `review_approved_plan_only` |

Read this table as a series of *guards*: conditions that must pass before another step can occur. This isn't an extra implementation; it is a way to describe the function where a learner can check the behavior. A guard is more useful when it blocks action, not when it merely produces a warning the caller ignores. In the toy design no terminal status can submit an order, so the guards govern which recommendations are valid, not whether a writer can be invoked.

### Worked trace 1: the valid plan without review

The object is well shaped. It fits the agreed types. The first read succeeds and records `read`. There is a hinge row and its version is R17. The count is 1, the trigger is met, and the proposed quantity matches the deficit. The runner records `pending_review` and returns `pending`. It doesn't wait for a person inside the function; it hands back a result describing the missing decision. That is a good interface for the lesson: the reader can see that the policy checks are complete without pretending that someone has already acted.

Run the same case with the separate value `review=True`. The trace is now `read → pending_review → review_approved_plan_only`. The status is `approved_plan`. What new fact does this establish? Only that a valid recommendation took the simulated positive-review branch. What facts stay the same? The fixture hasn't changed. No fresh capability was created. There was no external receipt. If you told the desk “ordered,” the interface would be making an assertion its own trace can't support. A good display would say “Plan approved in the simulation; no order placed.”

Pass `review=False` instead and the last event is `review_denied`. Both cases used the same count, target and revision. Approval and denial don't change the arithmetic; they change the recommendation's review status. When tests vary one input at a time, the resulting trace makes that separation easy to check.

### Worked trace 2: the same item at a new revision

Imagine R18 contains the same visible count and target as R17. Supply the original candidate with revision R17 and set `review=True`. That candidate still has three permitted fields and its quantity is still numerically sensible. The runner records a read, detects the mismatch and returns `stale` with `revision_mismatch`. There is no `pending_review` event because the gate is earlier in the function. Do not dismiss this case as pointless: an operation that shares a visible number with an older state is not proof that every condition in the older state remains valid. The contract chooses to require a fresh proposal at a new revision, even if a human might ultimately accept the same idea again.

There is a design trade-off here. Re-review after any change can be frustrating if a large record changes for unrelated reasons. Narrowing a revision to the precise record or inputs that matter can reduce false alarms. That is a question for the system design: which fields make two cases equivalent for this decision? Don't solve the inconvenience by suppressing freshness checks or silently transferring an old approval. A separate fresh review of the unchanged quantity is a cost you can explain. A wrong decision that cites an earlier review is considerably harder to explain.

Now let R18 contain 2 instead of 1. A newly typed proposal for 2 at R18 isn't stale, but it is outside policy, because 2 is not below the threshold. This is a stronger lesson than “check revision”: stale-state handling shouldn't retry the old plan until the revision matches. It should ask whether a plan is still justified. When the trigger is gone, stop. When it survives, put fresh evidence on a fresh recommendation.

### Worked trace 3: one failure, then two

Supply a well-formed R17 candidate and set the simulation to fail one read. The first attempted read emits `transient_read_failure`; the second emits `read`, and the function can reach `pending_review`. Ask for two failures and there are two failure events followed by `stop`, with status `unavailable`. Ask for five failures and the visible trace is the same as for two: the simulated source would fail five times if asked, but the runner only asks twice. A retry limit is a limit on what the caller may try, not a limit on what the source is allowed to do.

Contrast those failures with an unknown item. A successful read followed by `unknown_item` is not a transient read failure. Repeating the same query wouldn't give this example new evidence. Invalid shape never attempts the read. Stale revision does not repeat the read. A denial is a separate outcome and doesn't turn into a delay before accepting the proposal. When you map these conditions to distinct statuses, the caller stops in the right place and can state why. A single status like `failed` buys a smaller response schema at a big cost: the reader cannot tell whether to correct an input, prepare a new proposal, seek a review, or wait.

## Distinguish a stopped plan from an interrupted action

A timeout is an observation, not a verdict about what happened. Our lab simulates transient read failures, not a real timer or network timeout, and the runner has no writer at all. Assume instead that another system could apply a change. If the caller lost the reply after submitting it, the absence of a reply would not prove the absence of an effect. A blindly repeated request could apply the same change again. A request is *idempotent* when repeating it has the same intended effect as one application; the [HTTP semantics specification](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) describes that distinction for HTTP methods. This is not a claim that any operation carrying a familiar method name has been implemented correctly.

The takeaway for the toy exercise is narrower: count attempts, make the reason visible, and don't treat denied or stale states as retryable errors. For a hypothetical operation that changes a record, an unclear result might mean not attempted, attempted and unchanged, or attempted and changed but not confirmed. Which observation would distinguish the last two? It would have to come from a trustworthy account of the effects, not a paraphrase of the original request. Don't add that operation to this lab. Keep your reasoning on paper. Predict the information a separate authorized operator would need before it could responsibly decide what occurred.

Read-only isn't the same as unrestricted. Imagine a desk assistant whose whole job is to recommend whether to replenish hinges. The staff ledger also contains names, shift notes, and cost estimates for an unrelated project. Although reading doesn't change that ledger, the narrow job doesn't need those fields. A count-only view makes a better boundary than forwarding the whole ledger and asking the model nicely to summarize just one row. If the authorized view stops containing the item, the recommendation should stop or say it cannot substantiate one. The absence of writing privileges doesn't excuse unnecessary access or disclosure.

### What was approved, exactly?

A reviewer might approve an estimate at R17. Later, a displayed summary changes to R18. It would be a mistake to consider the earlier approval transferable just because an item name matches. The subject may look the same while the amount, jurisdiction, recipient or permitted time changes. An approval record should bind to the exact normalized intent and snapshot of what was reviewed. That principle guides the lab's stale-state check, but our Boolean only simulates a trusted reviewer decision. This code doesn't persist approval, authenticate reviewers, bind a token, or coordinate concurrent changes. A production service also needs a freshness rule at the boundary that actually applies effects, not just in a preview.

For a fictional plan review, describe a narrow receipt on paper:

- Which action was reviewed? “Accept a *recommendation* to bring hinge stock from 1 toward 4,” not “Do whatever is necessary to restock.”
- Which record version and constraints supported it? R17, threshold below 2, target 4.
- What exact candidate was reviewed? Item hinge, quantity 3, revision R17.
- Who reviewed it and in what role? A reviewer identity would need to be established by a trusted review channel. The proposal cannot supply that identity.
- May the receipt be reused? Not for a different candidate or revision. A receipt for accepting the plan grants no authority to submit any real order.

A signed review in a real system might help establish who approved a specific decision and whether that decision record changed. Signature isn't a synonym for permission. You still need to know what the signer was entitled to approve, what the signature actually covers, and whether the record is valid for *this* decision. A signed broad statement from somebody who cannot authorize a specific action doesn't authorize it. This is a design exercise, not an implementation recipe for review identity or signing.

If a runner persists optional memory such as “preferred supplies,” that memory is evidence or a preference, not permission. A prior recommendation is not a new order; a stored approval may no longer be current. A later case should reveal whether a cache quietly reuses a stale decision. Build the test using the same item code, one changed revision, and otherwise identical details. This isolates the property better than a test that changes item, amount and date together. Don't confuse an earlier decision log with a durable grant to do related things in the future.

One more cost belongs in the design. A preview fetches data at one point in time; a reviewer may not look at it immediately. The paper trail should not conceal that interval. If conditions change during it, a trustworthy system can state exactly what was reviewed and why that review is no longer current. A design that reads “latest” at display time while relying on a separate older review elsewhere makes the evidence hard to interpret. For the toy, we choose simplicity: one in-memory fixture per call; a simulated review is conditional on the candidate matching that call's revision. Do not mistake that controlled simulation for a concurrent review system.

### Where should a stop send the reader?

A useful stop is neither a shrug nor an invitation to enlarge the task. If the model produces an invalid candidate, say which field failed and let someone provide a conforming candidate. If a record is stale, request a new recommendation based on fresh evidence. If the source was temporarily unavailable and the retry budget is spent, report that no recommendation was established. If someone denies the plan, show denial as the result. If the plan is approved, say it is a plan. None of these messages needs to invent a new recipient, assume authority to call another system, or act on a user's behalf.

A clear stop can be more useful than a forced answer. Suppose the reader sees “Three hinges recommended, review pending” alongside a precise source revision. They can decide whether to review or wait for fresher evidence. If the interface displays a bare green success label, they have to guess whether any decision happened. An output contract should specify the claim attached to each status. That is where the content problem from the opening meets the interface problem: the display must not promise a stronger outcome than the implementation can establish.

## Test the right property

Predict the status and trace for a valid proposal, the same proposal approved, a stale proposal and two temporary read failures. Then run the [offline lab](../lab/check_examples.py) and the tests:

```sh
python3 -B lab/check_examples.py
python3 -B -m unittest discover -s tests -v
```

Run from the repository root. The first command prints a `runner` section with four synthetic examples. It also prints numerical examples used in other chapters; they do not affect the runner. The test command checks the intended boundary and other fixtures. Neither command asks a model what it did. Both are local and deterministic for these fixture inputs. A check you can inspect and repeat is stronger evidence of this particular property than a persuasive account about it.

A trace without a write event only establishes what was observed by that trace. Here the code has no action interface and selected boundary tests also compare fixture state before and after calls, including approved-plan. This does not assert that a deployed service is trustworthy. Apply the same reasoning to missing input: a check that only tests the valid branch may never reveal that the error branch continues. See [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1) for a wider risk framework; this toy lab does not implement or certify it.

### Walk an independent negative test

Predict that a proposal with an extra field named `execute` must stop before an inventory read. Now look at why: the runner checks the shape before it looks up the item. A bad version might accept the valid keys it recognizes and ignore the rest. In a pedagogical read-only simulator that would still never place an order, so a no-write test alone would pass. But the shape property would be wrong. Both tests matter. The observable decision should be `invalid`, and the appropriate stopping reason is `invalid_shape`. The included policy test checks the status for this case; to test the ordering independently, assert the exact trace or supply a recording in-memory mapping and check that no lookup occurs.

Now reverse the mistake. Imagine a trace perfectly reports `pending_review`, but a debug feature also opened a separate file to record a real person's name. “Inventory unchanged” would be true and still too narrow a result for a genuinely private task. The claim depends on what assets you measured and what access was possible. In our lab no such input exists and the runner has no network or actual writer. For a real service, one witness might inspect exposed functions, another the permissions of the running service, and another its observable effects. The checks should match the claim, not just reuse a familiar testing word.

Think of the suite as a list of observed properties, not praise for a solution:

| Property | Independent observation | What this still doesn't prove |
| --- | --- | --- |
| Fixture remains unchanged in the exercised branch | Pre-call and post-call fixture values match | Absence of unrelated service effects in a different implementation |
| A stale proposal does not reach the review gate | Exact trace ends at `revision_mismatch` | Whether another service might reuse an old decision |
| Transient retries are bounded | Two failure events followed by `stop` even when five failures are configured | That a real network timeout is implemented or that upstream deadlines are respected |
| Approval cannot redeem a disallowed amount | Simulate approval and still observe the expected invalid path | That a real reviewer identity was established |
| Runner cannot submit an order in this exercise | Inspect exposed operations and the function's implementation, not just its message | The capability boundary of any larger host that imports it |

We don't need an external service to test these conditions. Smaller examples make the causal story inspectable. The trade-off is that small examples don't test credentials, external state, real identities or actual approvals. State both facts: the property was exercised in the lab and is still to be established in a different environment. That's not a disclaimer tacked on at the end. It tells another engineer whether they can reuse the tests or need a different check.

### Put the pieces together at a second desk

Imagine a classroom print desk asks for a planning note about paper stock before an event. On a worksheet, use the same threshold and target as the hinge case: below 2 packages, propose enough to reach 4. The fictional revision P31 records 1 package, so three is the valid quantity. The desk permits consulting the fixture and preparing a note for a staff reviewer, not changing stock or calling a supplier. An optional comment attached to the inventory says, “extra paper wanted”; the comment doesn't change the arithmetic or the scope. The counted packages and policy are decision evidence. A comment is contextual material, not a directive with priority.

Sketch the stages before running anything: identify fields, check the source revision, check the trigger then amount, then assign the simulated review status. Before review, the next legal result is a recommendation waiting for a decision. If the reviewer accepts the plan, that controls the plan's status and nothing more. If a newer snapshot shows stock at 2, a fresh proposal at the new revision would fail the trigger. If a single read fails, the runner can make its second attempt; if both fail, it stops with an unavailable result. A correct answer to “did you replenish?” is still no, even if the plan itself passed every test.

Try to break only one property at a time. Give the worksheet a wrong revision but the correct quantity. Hold the revision fixed while replacing the integer with a textual amount. Keep the evidence unchanged while giving the candidate an extra field. Repeat the scenario where the plan is approved, compare the fixture before and afterward, then inspect whether there's an action interface at all. Don't change the simulation to call a real service to test your claim. A local fixture can distinguish policy, review, and absent capability without creating a real-world side effect.

Finally, report to another learner in three lines: the plan result and fixture version; which review decision, if any, was simulated; which effects the runner deliberately cannot perform. If they read the note and think a supplier has been contacted, you haven't described the outcome. If they can point to the exact guard that stopped a stale plan and the check supporting no inventory mutation, your account is usable. That is the point of the teardown: an observer can tell which block caused the next block to run, and which block never existed.

## Exercises

**Warm-up**

1. **Specify the interface.** List the allowed proposal fields and their types. Write two otherwise identical objects that differ only in the representation of the quantity, one with a number and one with a string. Predict which representation fails before any read. Cite the rule you used rather than guessing from the value's appearance.
2. **Trace the review.** In the hinge fixture, draw two traces for the same valid proposal. Give the first no review and the second a simulated denial. Label the first event where they diverge. In a sentence for a reader at the desk, distinguish “not yet reviewed” from “review denied.”

**Application**

3. **Separate the trigger from the amount.** Replace the count with 2 and the revision with R18; leave the target at 4. Work two cases: an old R17 proposal, then a new R18 proposal that suggests buying two. For each case state the exact guard that should end the trace and what future evidence, if any, could change that result.
4. **Exercise the retry budget.** Hand-trace the valid R17 case with zero, one and three configured transient failures. For each, predict the number of attempts, status, and last trace event before running it. Make one version use simulated approval and explain why that input cannot override an unavailable read.
5. **Keep knowledge separate from permission.** Invent an item description for the fictional print desk that includes a staff preference as ordinary text. Define a schema in which the preference can inform a human without changing the plan's permission. Add a separate case where a required trusted field is missing. Show what the reader learns and what the runner must stop short of claiming.
6. **Make an independent observation.** Design one local test for rejection of an extra field *before* reading, then another for unchanged inventory after simulated approval. State the observation needed for each and explain why the tests aren't interchangeable. Keep both tests in memory. No external calls or action tooling.

**Synthesis**

7. **Write the state table for a second desk.** Borrow a toy domain such as checking a reading room's supply count. Specify the authorized read, typed proposal, trigger, target, current revision, grounds for denial, and prohibited operations. Include a transition matrix with at least six rows and a stop that has a different cause from a read timeout. Give enough detail that another learner can predict the same traces before seeing your preferred result.
8. **Review an exact draft.** On paper, design a receipt for accepting a proposal at one revision. Represent the same item at a second revision with a new amount. Give your receipt to a partner and ask them to identify exactly which facts attach to the first review and which cannot carry forward. Revise the receipt only if the first version left that boundary ambiguous. Treat the receipt as documentation, not an actual signature or authorization.

**Challenge**

9. **Compare two convincing logs.** One fictional runner has a writer available and did not invoke it during the observed run; another cannot load a writer at all. Both logs show the same approval of a plan. Design a second source of evidence that can distinguish the designs. Discuss which observation you'd trust if the log and independent check disagree. Do not implement or invoke a writer to make the comparison.
10. **Budget for justified stops.** Your fictional desk reports that stale-plan stops frustrate reviewers. Outline two design changes that might reduce delay while preserving exact review and current evidence. Evaluate each against a case where the item name remains unchanged but a material decision input changes. Show which cost you accepted and why. Don't treat a high completion count as proof that the new design respected the boundary.

## What you can now do

You can draw the line between what a runner can do and what its task authorizes. That isn't just a distinction in vocabulary. You can represent one interface that has no action operation and another, conceptually, that would need its own authority review before it could act. You can identify information the reader needs for a recommendation and leave unrelated fields out of the exposed view. You can also explain which kinds of certainty aren't available: a fixture is not the real world, and a Boolean isn't a person's proof of identity.

You can design a proposal a program can judge without relying on persuasive prose. You can read independently supplied version information, compute a deficit after checking the trigger, and bind the recommendation to the conditions that justify it. If the proposal is stale, you can distinguish starting a fresh decision from reusing an old one. If the source is unavailable, you can stop within a fixed retry budget and expose enough trace to explain what happened. None of those properties relies on loading an external writer or making an actual change.

Finally, you can test a bounded workflow with evidence that doesn't take the model's word for it. You can trace a negative path, verify that the fixture didn't change in an exercised case, and inspect what capability the runner exposed. You know how those checks complement one another and which conclusions can't be drawn from them. The payoff is a readable account of behavior: what was considered, what was denied, what was approved **as a plan**, and what was never part of the job.

## Next: measure whether the design holds on new cases

An agent with a defensible boundary can still make bad recommendations. The last chapter shows how to measure a revision without grading it on examples it already saw. Carry forward the separate columns you've earned: validity, version, review, availability, and observable effect. Don't blend them into a single success label just because it is convenient to put one number on a slide. A timeout may warrant one analysis, an unjustified recommendation another, and an unauthorized action still another. If decisions have different consequences, your evaluation should retain those distinctions long enough for a reviewer to see them.

Suppose you decide to give the runner two chances to read instead of one. To know if it helped, you'll need a fixed panel, equivalent inputs, repeatable outcomes, and a clean comparison of records that changed status. You will also want to know whether the change produced delay that mattered more than a small improvement in recommendations. You could tell an upbeat story about the extra try. [Chapter 5](05-repeatable-evaluation.md) gives you a better option: decide the measurement first, preserve the failure status, and let somebody else reproduce the result.
