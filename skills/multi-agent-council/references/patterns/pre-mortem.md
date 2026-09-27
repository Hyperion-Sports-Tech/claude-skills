# Pre-mortem

**Type:** Modifier (layers on top of a core pattern)
**Best for:** Stress-testing a proposal after initial convergence, before finalizing

## What It Is

A red-team pass that runs after a core pattern has produced a converged proposal. A dedicated red-team agent assumes the proposal was implemented and failed, then works backwards to identify the failure modes that were visible at decision time but ignored. The team lead then patches the proposal to close the top risks.

## When to Add

- After the council converges on a direction and the proposal looks solid — that is precisely when blind spots are most dangerous
- Before finalizing any high-stakes decision (infrastructure changes, data model redesigns, public API commitments)
- When the convergence was suspiciously fast or unanimous — fast agreement often means shared blind spots

## Structure

### Step 1 — Spawn the Red-Team as a one-shot subagent

The Red-Team runs as one isolated, one-shot analysis using `references/execution-backends.md`, with the accepted budget and delivery contract. Do not reuse a deliberator's conversation. Follow the shared checkpoint policy; do not add this pass without budget acceptance.

Return the hypothetical post-mortem through the selected backend. Fresh conversation context is useful, but shared files/tools can leak council reasoning; it is not an access-control guarantee.

### Step 1.1 — Give the Red-Team its isolated context

Spawn the Red-Team with a prompt containing **only**:

- The **converged proposal artifact** itself — the Proposal Document's final recommendation and scope sections, **stripped of the "we considered / we rejected" reasoning sections**. Only the outcome, not the deliberation.
- The **problem statement** as the user originally provided it.
- Authorized source excerpts or scoped read-only tools to investigate failure mechanisms independently, without access to council drafts or raw deliberation.

The Red-Team agent is **explicitly denied** (not included in the message, not available through any other channel):

- The Round 1 position papers
- The Round 1 Digest
- The Round 2 responses or Round 2 Summary
- The tradeoff discussion from the core deliberation
- Any dissent notes from the core rounds

Target **no access to the core council's reasoning**: use curated packets with tools disabled or enforced access boundaries. Otherwise disclose prompt-level separation and any leakage. A directory containing the full council run is not a blind-review workspace.

Mandate: **"As a hypothetical exercise, assume the proposal failed at the stated horizon. Work backwards from failure using the proposal and authorized evidence. Label scenario claims, distinguish plausible from extreme failures, and do not invent actual events or probabilities."**

**Why this matters:** a fresh agent that reads the council's analysis can still anchor on its framing. Separation helps surface overlooked mechanisms; it does not prove independence or completeness.

### Step 2 — Red-Team Analysis

The red-team agent produces a post-mortem from six months in the future containing:

1. **Up to three plausible failure mechanisms** — specific, sourced where possible, with likelihood left unknown unless supported. For example, bypassing a slow validation step is a hypothesis to test, not permission to invent a measured latency.
2. **False assumptions** — assumptions baked into the proposal that turned out to be wrong. What did the team believe that the future proved false?
3. **Warning signs visible now** — signals that were available at decision time but were ignored or downweighted. What should the team have been watching?
4. **What a different team would have done** — an alternative approach that avoids the identified failure modes. Not necessarily better overall, but specifically better at avoiding these failures.

### Step 3 — Patch Synthesis

The team lead reviews the red-team analysis and produces a **patch synthesis**: the minimum changes to the original proposal that close the top two failure modes. Rules:

- Do not start over. Patch, do not rebuild.
- Each patch must directly address a specific failure mode from the red-team analysis.
- If a failure mode cannot be mitigated without fundamentally changing the approach, flag it explicitly and let the user decide whether to accept the risk or change direction.
- Add monitoring or trigger conditions for any failure mode that the patch reduces but does not eliminate.

### User Checkpoint

Present the red-team analysis and patch synthesis to the user. The user decides:

- Accept the patches and finalize the proposal
- Reject a patch and accept the risk (with documented reasoning)
- Reopen the core deliberation if the red-team analysis reveals a fundamental problem

## Output

The modifier adds two sections to the proposal document:

1. **Red-team analysis** — the full post-mortem output
2. **Patches applied** — the changes made to the original proposal in response, with traceability to the specific failure modes they address

## Notes

- The red-team agent should not have participated in the core deliberation. A fresh perspective is the point.
- The most valuable pre-mortems find failure modes that arise from the interaction of individually reasonable decisions — things that only break when combined.
- If the red-team analysis is weak (generic risks, no mechanisms), the proposal may genuinely be robust — or the red-team agent may need more context. Give it access to the codebase if it did not have it.
