# Chapter 2 — Compare prompt patterns on the same job
*If you change four things, you learn that four things happened.*

Suppose a museum asks you to route descriptions of catalog entries. The first prompt, “Classify this record,” gets a paragraph. You clarify the rules, add demonstrations, request one label and switch models. The next answer is one label, exactly what you wanted. What fixed it? You don't know. You found a usable response without finding the cause. This chapter separates those outcomes.

**After this chapter:** define a baseline and a checker before running; compare a direct instruction and a demonstration prompt; isolate a failure the change does not solve. Start with the task-contract idea in [Chapter 1](01-describe-the-task.md). All cases and outputs here are fictional.

## What is the part you actually changed?

A direct or zero-shot prompt gives instructions without task demonstrations. A few-shot prompt puts demonstrations in the input. These change what the model reads, not its trained weights. In the GPT-3 study by [Brown et al.](https://arxiv.org/abs/2005.14165), few-shot task examples were supplied as text without task-specific gradient updates. The experiment does not establish that demonstrations will help your goal.

Keep the contract, model, settings, input items and checker fixed. Change only which demonstration block appears before the input. If you change the expected output at the same time, you now have two interventions. If a demonstration contradicts the contract, it has ceased to illustrate it. Treat disagreement between examples and written rules as a bug in the specification, not a trick you expect the model to solve.

<!-- → [TABLE: two prompt layouts with identical task, rules, input, and output marked; only the demonstration block differs] -->

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

## Exercises

- **Warm-up | Specify the checker:** Should `Object` and `object.` pass? Decide from the contract, then write the three accepted strings.
- **Application | Isolate the intervention:** Construct two new cases where abstention is justified for different reasons, then add one abstention demonstration. State what stays unchanged.
- **Synthesis | Compare mechanisms:** Compare the demonstration prompt with a separate identification step followed by labeling. Name new costs and check both using an unchanged test.
- **Challenge | Falsify your diagnosis:** Design held-out items that break a shortcut based on dates. Describe what pattern would contradict your diagnosis.

The next chapter asks a harder question: when the model chooses a permissible label or cites an actual record, did the evidence justify it?
