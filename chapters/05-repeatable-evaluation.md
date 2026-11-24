# Chapter 5 — Build a repeatable prompt evaluation
*The cases that taught the prompt don't get to grade it.*

A revised prompt is better on all eight cases you wrote it against. That is useful debugging evidence. It isn't eight independent votes that it will work on new cases: you changed the prompt because of those results. Keep development examples. Call them development examples. Then decide what test would challenge the revision on genuinely new situations.

**After this chapter:** freeze a held-out comparison and timeout policy; calculate and report a paired difference, discordant cases and response coverage; specify one limitation that changes the next test. Worked scores are synthetic, not model results.

## Separate the test from the tuning

A development set helps teach you what breaks. A held-out set lets you ask a narrower question after freezing versions and rules. If you inspect its outcomes to choose another revision, migrate those items into regression and get a fresh set before asserting generalization. Where near-duplicates share a source policy or construction template, split the related items together. Six near copies don't test six different hazards.

Use both versions on the same items and an independently determined key. Decide scoring and timeout handling first. When outcomes require human judgement, blind reviewers to the version where feasible. Define evidence requirements and disagreement resolution; agreement among graders is not the same as correctness. Record version identifiers, exact prompts, model settings where visible, evidence revisions, case IDs, the checker version and failure handling. A vendor interface can prevent exact regeneration. State that limit, and preserve enough to repeat the procedure.

## Name the decision before collecting scores

A test needs an object. “Does prompting work?” doesn't name one. “Does adding a demonstrated missing-evidence outcome improve the fraction of correctly resolved requests in this frozen repair-desk panel without introducing late arrivals on urgent cases?” gives us a particular change, an observable output, and an operational constraint. The word *this* is doing work. It says we're promising to describe one panel, not to certify all future uses.

The test also needs a baseline worth beating. If your deployed version already rejects answers without evidence, don't compare the revision to a deliberately careless prompt that accepts anything. If your real alternative is a simple policy check, include it when feasible. A deterministic program that reads existing policy fields may be cheaper and easier to review than a generative wrapper. A prompt comparison answers which of two conditions did better. It does not establish that either belongs in the workflow.

Write the unit of judgment down. Usually it is a request against a named evidence revision, not a line of JSON. If a request needs two clauses and only one is supported, you can preserve partial credit diagnostically while requiring both for a pass. That preserves what the learner did correctly without hiding that the overall response needs revision. If you mean to permit a partial answer, name what good partialness looks like: the supported claim remains, and the missing claim is explicitly left unresolved. An answer that just omits an inconvenient condition is not the same as one that explains the limit.

The relevant result might instead be a whole interaction. Imagine a toy user asks first about the north desk and later corrects themselves to the south desk. If the assistant returns the right answer for each isolated message but loses track of the correction inside a shared interaction, an isolated-turn test won't expose it. Build a separate multi-turn panel with the correction visible to both versions. Count one outcome per interaction for the interaction metric. Don't combine those counts with scores per individual turn as if they're the same unit.

### Turn the contract into a case card

Build each case card before you know how the versions scored. Its parts are simple, but each protects a different decision.

| Field | What to write | What it prevents |
| --- | --- | --- |
| Request and case ID | Exact wording and a stable identifier | Mixing cases or accidentally scoring different inputs |
| Corpus and scope | Included records, revision, place, and effective date | Letting one condition see evidence the other never got |
| Reference decision | Answer, supported partial answer, explicit abstention, or need for dispute review | Confusing a missing response with defensible uncertainty |
| Deciding evidence | Exact clauses and why each applies | Credit for correct-looking text with the wrong justification |
| Check and countercheck | Pass condition and a plausible near miss that must fail | The easy test that accepts any matching keyword |
| Group and stratum | Shared source or template; difficulty or risk category if used | Treating related cases as independent or losing the panel mix |
| Run rules | Deadline, retry procedure, read-only scope, handling of invalid outputs | Saving a preferred version from a failure after the fact |

For example, suppose a synthetic policy says a repaired radio may be collected only by the ticket holder, and a different record says the counter closes at 17:00. A request asks whether a friend can collect the radio at 16:30. The closing rule alone doesn't prove eligibility. A valid answer can say 16:30 falls within this announced closing time but the friend does not qualify under the ticket rule unless they themselves are the holder. A near miss would cite the correct closing rule and assert permission. Decide upfront whether the mention of time is required or optional. If it is required, make the time and authority checks separate. No part of the exercise needs a booking or release to be made.

### Split by what teaches the answer

Imagine six artificial policy groups. Group N contains two paraphrases about north-desk dropoff weights and one boundary-date case using the same source clauses. Group S contains two south-desk variants from a different policy. Group E addresses lost tickets. Groups C, H and L address collection, counter hours and missing locations, respectively. If a learner sees a north-desk paraphrase during tuning and encounters the same north rule with different punctuation in the test, the result speaks mainly to reuse of a familiar rule. That's useful if familiar-policy restatements are the intended use. It's misleading if the claim is performance on unseen policies.

For an unseen-policy question, assign whole groups rather than individual strings. One possible development split is N, E, H. Freeze a holdout with S, C, L. The particular choice is not magic; the policy separation is. If two groups share the same operative clause, combine their group assignments or state why retaining that overlap fits the claim. Some tasks need multiple grouping boundaries. A frozen case may share no clause with development yet copy the same generator template so closely that the apparent diversity is only vocabulary. Keep track of policies, scenarios and case templates separately long enough to see it.

Don't call a holdout fresh simply because you hid the answers. If you read the case questions repeatedly and tailor the prompt to them, they informed the revision. If you saw the results and then changed a threshold, the test helped train your decision process. Relabel those cases as regression; they remain useful. A subsequent evaluation needs a new holdout with the original decision rules or a newly declared design. Preserve the old panel and result as a record of what happened.

## Work a paired example

For the six toy cases, pass means the task decision, required evidence and no unauthorized action all passed. An explicit justified abstention is a returned result and can pass. A timeout is a failure and must remain on the panel.

| ID | Baseline A | Revision B | What happened |
| --- | --- | --- | --- |
| E1 | pass | pass | Answer supported |
| E2 | fail | pass | Stale evidence corrected |
| E3 | pass | timeout | No candidate returned by deadline |
| E4 | fail | pass | Justified abstention |
| E5 | fail | fail | Neither sufficiently grounded |
| E6 | pass | pass | Answer supported |

A passed 3/6. B passed 4/6. The difference is 1/6, about 16.7 percentage points. There were three discordant cases, two gains and one loss. One net win doesn't mean only one case changed. E3 may matter more than the two improvements, depending on the cost of a timeout in the intended workflow. Decide priorities before you learn which version won an item.

B returned five results; coverage was 5/6. Among the returned results, the pass rate was 4/5. Across the panel it was 4/6. The metrics have different denominators because they answer different questions. Report which one you're using. Seeing better results among returns could reflect failure to answer difficult questions rather than a more useful system.

<!-- → [TABLE: a two-by-two cross-tab of case IDs by pass/fail, with E3 explicitly counted as a timeout and failure] -->

## Keep the failure in the attempt log

Consider what a timeout actually means. At a predeclared deadline the runner had not received a complete candidate response. An on-time candidate may still be malformed or wrong. That observation doesn't tell you whether the program would have finished with the right answer later. It also doesn't mean the system explicitly declined the task. A response reading “No applicable policy was supplied” is a candidate and can be checked on its merits. At the deadline, an incomplete stream is not that response. If learners use a retry rule, the rule defines a new measurement procedure. Write it down before attempts begin.

Suppose the repair-desk panel sets a synthetic deadline of five seconds per case. B's first attempt on E3 returns no valid candidate by five seconds, then delivers a correct decision at seven. With a one-attempt, five-second rule, record a timeout. Don't retroactively extend the deadline for that case. If actual users can wait ten seconds and the workflow supports one retry, test that as a separately named procedure. Specify whether ten seconds is the total budget or ten seconds per attempt. Record old failures as well as final outcomes; the cost of retrying still happened. Don't count two attempts at one case as two independent cases and then let the success replace the earlier failure in every metric.

Keep parsing failures, wrong answers, and absent responses distinct in the trace. This helps reviewers fix the right component. If a malformed answer arrives at four seconds, the delivery occurred but the contract wasn't satisfied. Under this chapter's coverage rule, an arrived candidate can count as returned even though it fails validation; decide and disclose whether a particular implementation counts an unparseable response as returned. When a malformed answer prevents delivery of any usable artifact to the reader, report usable coverage separately. In the original six-case example returned means arrived, not correct. The distinction matters when an old interface appears fast because it responds with invalid output.

A dependable log has one row per scheduled case-condition pair, even when the actual attempt was interrupted. Keep a cancellation caused by the researcher or a case intentionally not run distinct from a timeout from the evaluated system. If an equipment interruption invalidates a whole block of runs under the predeclared procedure, state what happened and repeat the block if needed rather than deleting a few unfavorable rows. Report counts of excluded cases and why. Avoid a comparison in which the routes start with different numbers of planned items and end with conveniently equal denominators produced by selective exclusion.

### Re-run the procedure, not just the favorite output

If both conditions use one permitted model in a shared service, time-of-day and load may matter. Suppose every A attempt runs on a quiet simulated morning, and every B attempt runs on a noisy simulated afternoon. The scores now reflect a workflow difference and a scheduling difference. Alternating which condition goes first for successive cases reduces a systematic order difference; alternating isn't proof that all outside variation disappeared. Use separate conversations when testing standalone decisions so B can't see A's answer. If interaction history is part of the design, capture and freeze the same relevant history instead of clearing it. Explicitly name session, cache and evidence settings that could plausibly affect results when you can observe them.

When the workflow produces differing answers on identical inputs, repeat attempts under the same announced schedule. For example, a panel of eight cases tested three times has 24 attempts per condition, but still only eight distinct cases. You might report attempt-level pass fractions and show per-case counts out of three. A report can also define a case-level threshold, say at least two of three passes, but that threshold isn't equivalent to the attempt pass rate. For two cases with 3/3 and 1/3 successes, the attempt pass fraction is 4/6 while the case pass fraction under that threshold is 1/2. Both can be useful. Neither turns repeat calls into new questions.

Not every environment exposes a persistent configuration identifier. Record what you can actually see, when you saw it, and where the interface did not let you freeze an important setting. If a result changes after a version or data refresh, it's not proof the earlier log was fraudulent. It tells you the earlier measurement belonged to a particular captured procedure. On the offline path, save the authored candidates and versions instead; show that running the scorer against the same inputs recovers the same report. Do not call that a model replication.

### Read all four cells of the paired table

The E-series comparison contains two cases where both passed (E1 and E6), one where both failed (E5), two where only B passed (E2 and E4), and one where only A passed (E3). The relevant margins reproduce the individual pass counts: A passes the two shared wins plus its one exclusive win; B passes the two plus its two exclusive wins. The sum across all four cells is six. Record the IDs or a private equivalent so a reviewer can find evidence behind each cell.

A zero aggregate difference can hide movement. On a four-case panel, imagine A passes two and B passes two. If the same two pass in each condition, there are no discordant cases. If A passes the first two and B passes the other two, all four are discordant. The pass-rate difference is zero either way. An operator who cares about which claims are now allowed, denied or sent for review should treat those scenarios differently. The paired table tells you where to look; it does not by itself decide which changes are valuable.

## Test the evaluator you actually use

A scorer that drops timeouts can make a system look better when it silently stops. A scorer that rewards every refusal rewards never answering. Challenge both assumptions with explicit tests. The [offline lab](../lab/check_examples.py) rejects mismatched case IDs and keeps timeout as a category. It receives decisions already graded against the toy rule; it cannot determine evidence quality by itself.

These cases support descriptive counts, not a population estimate. To say something beyond the observed panel, document how cases were sampled, how often they're near-duplicates, and how many independent observations the design supports. A statistical interval under a bad sampling assumption isn't a repair. Analyze rare, important failures separately instead of letting the aggregate hide them.

## The scoreboard is a decision, not a decoration

Define wins and losses over the same case set. For each item, map a pass to 1, anything failing the joint rule to 0, and compute revision minus baseline: 1 for a gain, 0 for no change in pass status, -1 for a regression. Sum over cases and divide by the panel size. In the worked example, the line is 0, 1, -1, 1, 0, 0. The sum is 1, the denominator is 6. This gives the difference between two pass proportions and also shows why discarding the pair matching sacrifices information about where the revision helped or hurt.

A useful next step is to name one important error that isn't captured by the average. Suppose you defined an illustrative cost of 4 units for a new timeout and one unit of benefit per newly correct answer. B's two gains are worth +2, the new timeout costs -4, and the difference is -2 under that scoring policy. These units are invented. They aren't outcome measurements, and they aren’t a reason to add costs after seeing a disliked result. If different people disagree about what should count as severe, show both the raw category counts and the decision under each declared policy. The report should make the value judgment visible rather than hiding it inside a nice looking score.

This also explains why “great performance” and “good enough for this workflow” are different questions. A small time-sensitive service might reject any newly introduced timeout on a critical path, no matter how many routine records improved. Another might accept a delay if incorrect answers were more costly. Design the benchmark around the consequences, not just the convenience of collecting cases. Do not let a teaching panel stand in for a deployment authorization.

### Report a selective assistant without rewarding silence

Suppose an assistant is asked four answerable items and two unanswerable items. It correctly answers two answerable items, abstains on two answerable items, appropriately abstains on one unanswerable item, and gives an unsupported answer on the other. There are no timeouts. It made three substantive answers, two supported, so the supported-answer rate among answers is 2/3. Its substantive answer coverage is 3/6. Its **response** coverage is 6/6 because the abstentions were returned outcomes. Under a rule that only rewards correct answers on answerable items and correct abstention on unanswerable items, its all-case pass rate is 3/6.

A baseline that refuses every item has response coverage 6/6, answer coverage 0/6, and only 2/6 all-case passes under that same rule. Its supported-answer rate among answers is undefined, not 0/0 rendered as 0% or 100%. The numbers change depending on what you mean by result, answer and success. Introduce these terms in the evaluation plan and keep them unchanged when one number looks embarrassing.

The best tradeoff doesn't follow from the arithmetic alone. On an optional library FAQ you may tolerate a refusal. Where abstention delays a needed service, the loss deserves its own line. In any high-impact case, take appropriate expert review and evidence standards rather than making the training example do that work.

### Protect a conclusion against the way the test was built

Leakage isn't only an exact case repeated across sets. Suppose you get 12 cases by turning six policy clauses into two phrasings each. Splitting randomly by individual case can put the same clause on both sides. Group both phrasings before partitioning. If a future study requires unseen policies *and* unseen venues, put those differences in the sampling plan too. The count of scored items is still useful, but tiny repeated cases don't buy wide evidence.

For a second check, separate independently specified data and scorer from the system doing the answering. If the same model creates the questions, proposes the evidence and decides it was correct, every leg can inherit the same misconception. You don't need to ban assistance from construction; you need independent adjudication for consequential claims and at least some independent cases. A second model can give a second perspective, not a guaranteed independent source of truth.

Finally, decide which failure the next batch can actually settle. If the current test mostly shows timeouts, collect timings across comparable workloads. If it mostly shows inconsistent decisions on paraphrases, collect grouped paraphrases and coverage categories. If the reference answers are in dispute, fix the corpus annotation and report that before treating either prompt as superior. A repeatable report gives the next worker a testable hypothesis, not a mandate to ship.

## Keep the evidence reviewer independent of the output writer

Make the reference card from the supplied rules. A judge who sees a fluent candidate first may write a rubric that excuses it. In an audit, present the request, eligible evidence and rubric without variant labels when practical, and shuffle the presentation separately from run order. Concealing condition labels doesn't make reviewers infallible. It just removes one obvious way preference can enter. If answer format exposes the condition, state that blinding was limited; don't claim it worked just because you replaced names with letters.

Suppose two toy reviewers each classify ten candidate responses independently. They both pass seven and both fail one. On one additional item reviewer R passes and S fails; on the other S passes and R fails. They each report eight passes, yet agree on only eight of ten items. The matching marginal totals would conceal the disagreements. Put both initial labels in the adjudication record. For one dispute, compare the exact clause versions. For the other, read the predeclared output contract alongside the candidate. If both disputes meet failure criteria, the reconciled result is seven passes out of ten, with eight initial agreements out of ten. Reconciliation does not retroactively make them ten initial agreements. If an item is genuinely ambiguous under the frozen rules, record that separately rather than inventing a missing tie-breaking policy.

An adjudicator needs evidence, not just the two votes. For example, one response quotes a 2027 rule for an inquiry dated 2026. One reviewer rewards the clear wording; another catches the effective date. The date decides the dispute because the rubric says apply the rule in force on the request date. Neither reviewer should have to guess a rule from the polish of the answer. If the rubric didn't say whether to use the request date or the current snapshot, the dispute exposed a design omission. Report the omission. If you fix the rule, preserve the previous revision and rescore both conditions rather than reclassifying the cases that make B look worse.

Classify errors with labels that guide an intervention. “Bad” doesn't distinguish missing evidence from wrong units, expired authority, unjustified abstention, or failure to return before a deadline. One case may have several errors. Decide whether the table is multi-label, or whether a fixed precedence assigns one primary label and others are preserved as notes. A multi-label table can legitimately sum to more than the number of failed cases. A mutually exclusive primary report cannot, unless the counts used different denominators. Neither choice is neutral: a precedence of timeouts before content says you'll diagnose arrival before an answer that wasn't on time.

### Review the score by case type

Here's another synthetic panel with twelve cases. Eight are routine single-clause requests and four are demanding multi-clause requests. A passes six routine and three demanding. B passes seven routine and two demanding. Both total nine passes of twelve, or 75%, on this panel. The routine improvement is 1/8, or 12.5 percentage points. The demanding regression is 1/4, or 25 percentage points. Even without the per-case pairs, those conditional rates tell you something the aggregate didn't.

The observed twelve-case mix weights the two group rates by 8/12 and 4/12. If an *explicitly hypothetical* future installation had 90% routine and 10% demanding requests, applying these same invented conditional rates would produce a weighted difference of +8.75 points: 0.9 × 12.5 plus 0.1 × −25. With a 50/50 mix the difference is −6.25 points. Those aren't forecasts. They illustrate dependence on the mix, assuming conditional rates transfer, which this small synthetic example cannot establish. Don't weight the test after seeing the result just to produce a desired sign. A review can show several plausible compositions to make that sensitivity clear, provided it's honest about the assumptions.

The composition of a stress test is often chosen on purpose. A hand-built panel might include four conflicts even though conflicts are rare in real intake. That makes it a stress panel, not a prevalence survey. It can justify “this change breaks the conflict behavior we require,” even without establishing how often real requests contain conflicting policies. A representative-use panel answers a different question from a boundary panel. Use both when you need both conclusions, and don't combine them without explaining how they were constructed.

### Record what would reverse the judgment

An evaluation memo should make it easy to talk you out of its conclusion when evidence changes. “We like B” offers nothing to test. “On this panel B fixed two failures and introduced one timeout. We would compare again before adopting because the affected request is on the predeclared critical path” says why. A later test could show that the timeout came from a shared dependency that affects both conditions, or establish that B stays within the same deadline under a controlled run schedule. It would take new evidence, not a synonym for better.

Consider two opposite errors. The first is to overpromise after a positive aggregate. The second is to shut down any action until you can make a population claim. A small deterministic fixture can legitimately block a release if it proves the program violates a required invariant, such as declaring that an action was authorized when the required review denied it. A small synthetic comparison cannot justify an expected gain for real users. These facts coexist. Use the appropriate burden: a repeatable counterexample is evidence of a defect; a claim about rates beyond the panel needs a defensible sampling story. Neither the words “test passed” nor “test failed” say which burden you met.

## Copyable evaluation worksheet

Fill this out twice: first before either condition is run, then after judging. Preserve the first draft separately. In the final capstone it's fine to use only fictional cases and authored candidates. If that's what you did, state it in the first line.

### Before the run

1. **Claim under test:** If the intervention works, what behavior changes on what panel? What outcome should prevent recommending it?
2. **One planned intervention:** What exact text, evidence rule or interface behavior differs? Name what stays fixed and why the baseline is useful.
3. **Population versus panel:** Which observations are synthetic, real, or a planned stress challenge? Is the goal familiar cases, new cases within known policies, or unseen policies? What will you not infer?
4. **Case manifest:** List case IDs, exact request and revision, shared groups, split assignments, applicability conditions, deciding evidence and an independently checked expected outcome. Mark which cases are sensitive to delay or wrong claims.
5. **Run plan:** Record the schedule, visible model or fixture identifier, prior context, permitted tool scope, timeout, retry and incomplete-run rule. What counts as a response? Define how you record explicit abstention and invalid candidates.
6. **Scoring:** Write individual dimensions and overall pass logic. Predeclare the outcome for a wrong clause with a correct label and a refusal on an answerable case. State disagreement procedure, exclusion rules and any critical failures that outweigh a gain.

### After the run

1. **Trace receipt:** For every planned case, retain condition, attempt outcome, elapsed time if measured, candidate or absence reason, raw checks and final disposition. Use synthetic data or a locally approved policy for collecting real trace content. Do not put credentials or unapproved records into a shared report.
2. **Paired result:** Report both numerators and the same denominator, the net difference, gains and losses, and examples of both. Report all-case passes and conditional results with clearly named denominators. Include unavailable cases.
3. **Judgment note:** Preserve independent disagreements, adjudication evidence and open ambiguity. Give counts by failure category. Report critical constraints separately from means.
4. **Decision and next test:** Keep, reject, or hold the revision for this setting. Name one result that would change the decision and one uncertainty the current panel cannot answer.

A reader of the worksheet should be able to reproduce the arithmetic with a pencil and the judgment with the same evidence. If only the person who wrote B can perform the scoring, document the missing rule before adding more cases.

## Exercises

1. **Warm-up | Compute:** Recalculate the change if E2 also failed for B. Fill the four paired cells, not just the net. Then state how the answer changes if E3 was a returned incorrect response instead of a timeout.
2. **Warm-up | Translate denominators:** A returns all six planned requests and reports three correct. B reports three correct of three returned requests after three timeouts. Give both all-case pass rates, both response coverage rates and both conditional pass rates. Which difference is due to the denominator?
3. **Application | Control leakage:** Take three near-duplicate phrasings for one synthetic clause and three unrelated clauses. Give a development/holdout split that keeps the near duplicates together. Explain when a tempting item-level split answers a different, still legitimate question.
4. **Application | Fix the referee:** Write a case where the candidate cites a real policy but a wrong effective date. Freeze a rubric that lets two blind reviewers distinguish unsupported correct-looking answers from justified abstentions. Describe what you'd preserve if they disagree.
5. **Application | Test the test:** Make one B row late and another B row malformed, then remove a third B ID entirely. State what the aggregate lab should reject, which events are ordinary logged labels, and what claim you would not make.
6. **Synthesis | Report conditional performance:** Use the twelve-case mix example and construct paired case IDs consistent with its marginal totals. Make the number of discordant cases as small as possible, then write a second valid pairing with additional discordance. Explain why both have identical subgroup rates but suggest different regression work.
7. **Synthesis | Bound an inference:** Use a synthetic three-condition log: reference version, revised version and a simple deterministic rule. Give a credible change report with exact test units and known limits. State whether you measured a prompt change, a retrieval change or an entire workflow change. Don't infer a mechanism that the comparison didn't isolate.
8. **Challenge | Tradeoff:** A new prompt abstains more often and produces fewer unsupported answers. Design separate scoring for answerable and unanswerable cases. Include one critical failure whose cost makes an average gain unacceptable. Defend the threshold before seeing scores; give an example that would persuade you to revise the evaluation policy for a future study.
9. **Challenge | Transfer:** Apply the worksheet to a fictional intake job from a different field. Another learner should score both variants from the frozen rules, identify a failure you hadn't planned for, and state which rule or dataset split would have to change to test that failure fairly. Preserve both plans rather than overwriting your first one.

## Final transfer

Choose a new synthetic task or try the [capstone](../activity/CAPSTONE.md). Develop a contract, one controlled prompt change, an evidence audit, a read-only boundary, and a held-out split with a trace format. Make your first attempt unaided. If you use assistance later, preserve the first attempt and independently verify every changed decision. Hand another learner the cases and procedure without your conclusion. If they cannot reproduce the same acceptance conditions, fix the design before crediting the prompt.

The product of this book is not a collection of clever strings. It is a decision procedure that someone else can inspect, test and stop.
