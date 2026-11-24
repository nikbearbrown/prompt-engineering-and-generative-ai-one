# Context measurement lab: hold the evidence still

All outputs in this lab were authored for teaching. They are not model observations. The archive, policies and packet limits are imaginary. No network, API key, dependency or real record is needed.

## Before opening the worked answer

From the repo root run one input-only plan:

```sh
python3 -B lab/context_lab.py plan B middle
```

Read the **question** and write the exact access label, deadline label, two applicable record IDs, and a condition under which you would abstain. Mark every candidate distractor you expect to be misleading. Then compare the input-only plan at front and end. The question, blocks, record IDs and bytes are held fixed except for order; byte count is not model token count. SHA-256 of the assembled UTF-8 text changes with order. The file containing the designed outputs is available in the repo, not protected; don't open it until you record your first attempt.

## Inspect a missing-evidence control

```sh
python3 -B lab/context_lab.py plan B absent
python3 -B lab/context_lab.py plan B middle --visible-blocks 2
```

The absent control swaps the required block for unrelated notes. The limited plan separately simulates an explicit prefix budget measured in whole blocks, not provider truncation. An absence simulation is not comparable evidence for position effects. Write down which state should result in both cases and why. This toy contract requires both facts or an abstention with no facts or citations. It does not imply all readers should discard supported partial answers.

## Check the designed response panel

```sh
python3 -B lab/context_lab.py score
python3 -B -m unittest discover -s tests -v
```

For each of the three cases compare the ground truth, visible record IDs and candidate. Predict one tempting false pass that would be missed by a shape-only or label-only checker. Describe whether your repair belongs in retrieval, assembly, presentation or verification. Log the first changed observation after a single repair. Do not change the scorer just to accept a preferred result.

If running a permitted model elsewhere, use only synthetic material and record exact procedure and uncertainties. The example runner does no model calls, and its CLI does not accept external inputs as a substitute for the fixed fixture. A score on this lesson is evidence about your reasoning and your checker, not about any service.
