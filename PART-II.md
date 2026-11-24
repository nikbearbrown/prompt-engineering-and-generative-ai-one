# Part II · Diagnose harder cases

Build on [Part I](PART-I.md)'s task contracts, prompt comparisons, evidence, bounded tools and evaluation. These chapters change one source of difficulty at a time so you can tell which component failed.

1. [Diagnose audience, role, and evidence separately](chapters/06-diagnose-audience-and-prompt.md): vary the role and audience without modifying the policy, then test whether actual evidence changes the result.
2. [Measure whether context can do its job](chapters/07-measure-context-use.md): compare fixed evidence layouts and keep a missing-evidence control separate.
3. [Optimize against a fixed test](chapters/08-optimize-against-a-fixed-test.md): choose a candidate on development work and test it once against the frozen baseline on a held-out group.
4. [Operate multimodal workflows](chapters/09-operate-multimodal-workflows.md): reconcile what is visible, what can be independently verified, and what you can responsibly report in a draft.

Begin with the [context lab handout](activity/CONTEXT-LAB.md). With Python 3.9 or newer from the repository root:

```sh
python3 -B lab/context_lab.py plan B middle
python3 -B lab/context_lab.py plan B middle --visible-blocks 2
python3 -B lab/context_lab.py score
```

The lab's deliberately authored cases score evidence availability, provenance, and response facts. The block limit is a local simulation, not a provider's token limit. Use the [transfer exercise](activity/TRANSFER.md) to build a new panel, an accessible visual equivalent, and a dry-run stop rule.

This is prompt-level workflow design. Model adaptation, detailed architecture, parameter-efficient fine-tuning and alignment belong in advanced model engineering. Local shell and coding-agent workflow design belong in a separate coding-agents treatment. This part does not require, install, or invoke external services.
