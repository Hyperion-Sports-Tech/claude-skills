# Council Orchestration Guide

You are the **council lead**, the user-facing session. Keep decision criteria explicit and distinguish your synthesis from source evidence. You are not magically neutral; preserve raw papers and explain weighting choices so synthesis can be inspected.

Use this protocol with any backend in `references/execution-backends.md`. A single-round run skips Round 2, not evidence verification or dispatch accounting. Patterns change analytical structure; they cannot override access boundaries, budget acceptance, checkpoint policy, or truthful reporting.

## Run ledger and evidence packet

Create a unique run directory in the authorized scratch location. The lead, not the read-only workers, writes:

```text
brief.md                 decision, criteria, constraints, alternatives
run.json                 accepted bounds, source version, role/round/handle/status
sources.md               evidence IDs, authority, dates, source locators
round-1/<role>.md         actual returned papers, preserved verbatim
digest-1.md              positions, contested excerpts, checkpoint delta
round-2/<role>.md         when applicable
proposal-draft.md        frozen before independent Judge comparison
proposal.md              final recommendation/provisional report
```

Optional modifier artifacts get distinct names. Do not create empty completed papers for missing agents. Save original output separately from editorial corrections. No canonical company writes by default.

Every source entry records ID, type (observed, user statement, research, inference, simulation, hypothesis), locator, relevant date/as-of scope, and support limits. Every contested claim has a stable ID. Share only authorized sources; isolated prompts are not a security boundary.

## Round 1 — Collect and digest

1. Dispatch independent seats together within the accepted concurrency cap. No peer papers or lead recommendation in Round 1. Collect by the actual backend delivery contract, not imaginary team messages.
2. Account for every expected output. Verify load-bearing source support directly. Distinguish a missing source from a source that contradicts the claim. Log shared source origins so model repetition is not mistaken for corroboration.
3. Create a **Round 1 Digest**: each role in 2-3 sentences; key evidence IDs; exact short quotations of disputed claims with author/locator; tensions classified as factual, inferential, preference/weight, or missing information. Do not flatten minority evidence for neatness.
4. Present the digest and checkpoint. Pause unless unattended completion was explicitly accepted; otherwise record `checkpoint waived`. Attribute user corrections and distinguish factual information from priority changes.

## Dispatch accounting (runs every round)

Record expected role/round pairs, handles, and status: pending, running, received, blocked, failed, or cancelled. Count and deduplicate programmatically before finalizing. A role is received only when its required content is actually available, not because a marker appeared or a worker is idle.

- Use backend-specific completion supervision. For Hermes native, do unrelated work and end the turn to receive completion; do not poll its transcripts/artifacts. For external Claude PTYs, inspect tracked process state/logs.
- Check steady progress against the accepted soft timebox. Silence alone is not failure; do not kill useful research after an arbitrary short timeout. A warning is not a hard enforced timer.
- Allow one bounded corrective retry for malformed/missing content if within the accepted allowance. Ask before adding substantive work or changing provider/cost. If a worker is still active, stop or resolve its ownership before replacement to avoid duplicate work.
- Failed or missing contributions appear under **Known gaps**, named with expected work and impact. If absence undermines the decision, deliver a provisional report, not an unqualified recommendation. Critical missing evidence does not become less important because the agent failed.

## Round 2 — Cross-pollinate and collect

5. Send each role its own prior paper and source/assumption state, the **Round 1 Digest, not the raw peer papers**, exact contested excerpts, and checkpoint delta. Fresh workers need the complete brief, role, boundaries and delivery contract again. Persistent roles retain their own session.
6. Keep peer context to roughly 2,000 tokens when a tokenizer is available; otherwise use a declared 6,000-character cap (not a token-equivalence claim). Preserve load-bearing dissent, quotes and source IDs; split targeted follow-ups rather than erasing them to fit. Narrow raw excerpts can be requested when the digest is disputed, within budget.
7. Require a named/quoted counterclaim, hold/update/abstain, reason, remaining disagreement, and cheapest discriminating test. A demonstrable reasoning correction or changed decision weight can justify an update without a new external source. Mere social agreement cannot.
8. Collect papers and summarize what changed and why. Stop at the accepted round cap, diminishing decision value, or a need for empirical validation. Present the final checkpoint under the accepted pause/waiver policy; do not invent user approval.

## Synthesis

9. Produce the proposal using `references/proposal-document.md`. Make an accountable recommendation using the decision criteria; do not vote on facts or imply the lead has no preferences. Separate analytical conclusions from user-approved decisions.
10. Preserve material dissent and raw papers, even without the optional Minority Report modifier. The modifier strengthens an argument; basic dissent fidelity is never paywalled behind another agent.
11. Freeze the lead draft before inspecting a blind Judge output. Compare source support and omissions; disagreement in weighting is not automatically a factual error. Record gaps and leakage. Designated quality failures block claims of validation, not delivery of a marked provisional report.

## Shutdown

12. Close only sessions/teams owned by this run using `references/execution-backends.md`. Verify actual process exit or team membership state. Never infer termination from silence; record any unresolved cleanup under Shutdown anomalies.
13. Verify expected-versus-received counts, material evidence, output paths, and publication scope. Report what is complete, provisional, unverified, or awaiting a decision. No automatic external mutations or implementation.
