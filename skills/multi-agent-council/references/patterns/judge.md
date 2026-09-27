# Judge

**Type:** Modifier (optional, layered on any core pattern)
**Best for:** High-stakes deliberations where an independent audit of the team lead's synthesis is worth the cost
**Default:** Disabled; enable only in the accepted run configuration. Applicable after any completed core run, including one round, when an independent check is worth the added work.

## What it is

The lead's digest and synthesis can introduce framing and omission bias. The Judge independently synthesizes from raw completed rounds and authorized source evidence **without seeing the lead's synthesis**. The lead freezes its own draft before reading the Judge's output, then compares both. Divergence is a review signal, not proof that either side is right.

This is a bounded second synthesis, not a certification. Prompt-level blindness and filesystem isolation are distinct. Report the actual separation achieved; record leakage rather than claiming a blind audit when sources included the lead draft.

## When to enable

- High-stakes deliberations where the downside of a biased synthesis is worse than the token cost of an audit
- Deliberations where the team lead has been used repeatedly with the same role set and may have learned unconscious preferences
- When the user explicitly wants a "second opinion" before acting on a proposal

## When to leave disabled

- Runs where the added independent check is not worth the declared workload
- Exploratory runs — the Judge is for final deliverables, not iteration
- Pure documentation requests with no request to reassess the decision; do not stage a council as post-hoc endorsement

## Structure

### Step 1 — Spawn the Judge as a one-shot subagent

The Judge runs one isolated, one-shot analysis through `references/execution-backends.md` after the core rounds are collected. Supply the accepted budget and delivery contract. For a one-round council, use Round 1 only and state that limit; never fabricate Round 2.

### Step 2 — The Judge's inputs (in its spawn prompt)

Build its independent packet before dispatch:

- The **raw Round 1 position papers** (all deliberators, full text)
- The **raw Round 2 responses**, if actually collected
- The **problem statement** and any user-injected checkpoint context
- The decision criteria/weights, source ledger, and authorized primary evidence excerpts or scoped read-only retrieval
- A list of missing contributions and evidence limits; do not hide quality failures

The Judge is **explicitly denied**:

- The team lead's Round 1 Digest
- The team lead's Round 2 Summary
- The team lead's synthesis (**critical isolation**: the Judge never receives the synthesis during its independent pass)

Use a curated inline packet with tools disabled, or enforced source-only access. If workers share unrestricted files, prompt omission is not a blindness guarantee. No access to the run directory containing the lead draft. Missing source verification must be labeled rather than simulated.

### Step 3 — Judge produces its own independent synthesis

The Judge produces an independent proposal using `references/proposal-document.md`, ≤800 words plus compact citations, with a source-support ledger. It evaluates source support for the raw claims, not the unseen lead draft. Return through the selected backend.

### Step 4 — Team lead produces its own synthesis

Before inspecting any Judge output, freeze the lead draft at a distinct path and record that ordering. Produce it before dispatch if the backend returns the Judge result immediately. If the lead has already read that result, the comparison is not independent; disclose contamination rather than retroactively claiming a blind draft.

### Step 5 — Falsifiable rubric comparison (team lead side)

The lead compares both drafts and the Judge's source-support ledger using auditable checks. The Judge cannot flag defects in a draft it never saw; these are explicitly the lead's comparison findings:

1. **Citation existence** — each material empirical claim traces to an actual source locator, with a separate paper/claim ID for deliberation provenance. Inferences and preferences are labeled, not disguised as empirical claims.
2. **Citation-claim mapping** — source content supports the scope and date of the claim. The Judge checks available raw claims independently; the lead verifies mappings in both proposals. An existing URL is insufficient.
3. **Tradeoff naming** — the team lead's synthesis must name each tradeoff explicitly ("choosing X means accepting Y will be worse"). Missing tradeoffs are flagged.
4. **Dissent preservation** — both syntheses preserve material dissent from the final completed round, with supporting evidence. Agreement is not required.

Separate source-support defects from judgment about competing criteria. Do not present qualitative judgment as an objective score or let this checklist imply a correct business decision.

### Step 6 — Divergence handling (hard cap of 1 revision)

- **Both pass + structurally similar:** report "Independent synthesis compared; no material discrepancy found in these checks." Do not use a "Judge approved" certification stamp.
- **Comparison identifies a defect:** the lead gets **exactly one** revision with claim-level rationale. Keep the original. The Judge does not re-run and cannot approve the revised text.
- **Material recommendation/weight disagreement:** present both directions and their evidence, with the decision-owner choice made explicit. Under an unattended waiver, retain unresolved disagreement in the provisional report.
- **The Judge never runs more than once.** No revision loops.

### Step 7 — Non-blocking on failure

If the Judge fails or cannot finish within accepted bounds, delivery of an explicitly provisional analysis is non-blocking:

- Deliver the lead's analysis with "Judge unavailable: [reason]" and its effect on confidence.
- Log the missing work under Known gaps; log remaining sessions separately under Shutdown anomalies.
- Do not claim the audit passed or proceed with an action whose authorization required it. This exception permits reporting, not shipping software or taking business action.

Account for the Judge like every expected respondent; failure to receive an artifact is a gap regardless of process status.

## Budget

Budget one independent pass, including raw packet size, source checks, and output cap. State observable usage or `unavailable`; do not reuse unmeasured fixed token estimates from earlier versions.

## Output

When enabled, the Judge adds these sections to the Proposal Document:

1. **Judge rubric** — 4-item checklist (citation existence, citation-claim mapping, tradeoff naming, dissent preservation) with pass/fail and specific objections.
2. **Judge divergence summary** — where the Judge's independent synthesis differed from the team lead's, with specific claim-level citations.

If no material discrepancy was found, include the checks and their limits without a certification label.
If the Judge was unavailable, a single "Judge unavailable: [reason]" line replaces both sections.

## Judge prompt template

Use when spawning the Judge subagent:

```
You are the **Judge**, an independent synthesis reviewer. Evaluate the raw evidence against the supplied decision criteria. You will NOT see the lead draft, so do not claim to compare or approve it. The lead performs that comparison after freezing its own draft.

Your sole inputs (provided in this prompt):
- The raw completed rounds: [RAW_ROUNDS]
- The problem statement: [GOAL]
- Criteria, source ledger, authorized evidence/tools and known gaps: [EVIDENCE_PACKET]
- Delivery and completion contract: [DELIVERY]

You are explicitly denied access to the team lead's Round 1 Digest, Round 2 Summary, and final synthesis. If you somehow receive them by mistake, do not read them — flag the error in your output.

Your output is a Proposal Document in the same format as the team lead would produce (see references/proposal-document.md), length ≤800 words, based solely on the raw deliberator outputs you were given.

You do not revise your own output. You produce it once and return it as your final response. The team lead will do the rubric comparison.

Failure modes you must avoid:
- Do not second-guess your own verdict because it might disagree with the team lead
- Do not try to predict what the team lead will say and pre-emptively agree
- Do not produce a synthesis longer than 800 words — conciseness is a signal of clarity
- Do not skip citation verification — the rubric depends on it

Accepted research allowance/timebox: [BUDGET]. Report observable usage or unavailable. Read-only; no edits, external writes, scheduling or additional agents. Label source facts, inferences, simulations and uncertainty. If supplied information leaks the lead draft, flag contamination and do not claim blindness.
```

## Failure mode to watch

The Judge is still an LLM, still subject to the biases deliberators are. It is **not** a source of truth — it is a second independent pass whose **disagreement** with the team lead is the signal. Treat Judge approvals as "no obvious bias caught," not "synthesis is correct." Treat Judge rejections as "investigate this specific objection," not "the team lead was wrong."
