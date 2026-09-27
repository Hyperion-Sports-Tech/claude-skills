# Proposal Document Format

This is the final artifact of a council deliberation. The team lead produces this after all rounds and user checkpoints are complete.

Use a concise decision brief with linked raw evidence, not a transcript dump. Checkpoints may be explicitly waived; record that instead of inventing approval. This template is not a wiki schema: before publishing, apply the destination's actual conventions. A report is a recommendation, not authorization to implement.

---

```markdown
# Proposal: [one-sentence summary of the recommended direction]

## Problem / Goal
[What we explored and why — 2-3 sentences establishing context and stakes]

## Decision status and criteria
[Proposed / provisional / user-approved; owner; as-of date; decision criteria
and weights; constraints; reversibility; checkpoint approvals or waivers.
Do not assume approval from completed analysis.]

## Alternatives considered
[Include status quo/do nothing, defer/test, and credible alternatives.
Why each was retained or rejected, using criteria rather than vote counts.]

## Exploration

### [Role 1 Name] — [position summary in ~5 words]
- [Key finding with citation]
- [Key finding with citation]
- [Proposed approach]
- [Primary tradeoff accepted]

### [Role 2 Name] — [position summary in ~5 words]
- [...]

<!-- One subsection per deliberator. Preserve their evidence and citations. -->

## Recommended approach
[Synthesized recommendation — the direction that best balances the competing
perspectives. 1-2 paragraphs. This is the team lead's synthesis, not any
single agent's position. Explain why this balance was chosen.]

## Tradeoffs documented
[What we are accepting and what we are giving up. Be explicit about costs.
Each tradeoff should name which value function it works against and why
the council accepted the cost anyway.]

## Dissenting perspectives preserved
[Minority positions that survived deliberation — agents who held ground
through Round 2 with evidence. These are valuable context for future
revisits. Include the key evidence that sustained each dissent.]

## Implementation scope
[If applicable — what needs to be built, rough shape of the work, key
components and boundaries. For business/wiki work: proposed artifact changes,
owners, dependencies, and non-goals. Discover any downstream skill before use;
no automatic code changes, CRM writes, publishing, commits or deployments.]

## Evidence and uncertainty
[Claim IDs, primary-source locators and dates, inference/scenario labels,
load-bearing assumptions, conflicting sources, confidence limits, and what
would change the conclusion. Raw papers are provenance, not independent facts.]

## Cheapest next test
[Hypothesis; discriminating observation; threshold or decision rule; data
collection method; proposed owner; cost/time assumptions; success/failure action.
If no further test is warranted, explain why. Do not invent scheduled work.]

## Known gaps and run accounting
[Expected vs received roles/rounds/modifiers; failed/missing contributions and
effect on confidence; actual backend/model, checkpoint state, observable usage
or unavailable; raw output paths. Name unverified claims and unavailable audits.]

## Publication and handoff
[Canonical destination and provenance links; written vs proposed changes;
approval still needed. Scratch output is not durable publication.]

## Shutdown anomalies
[Actual state of run-owned sessions; unresolved cleanup. Omit if none.]

## Review triggers
[Specific, measurable conditions that should cause revisiting this proposal.
Each trigger must be falsifiable — someone should be able to check whether
it has fired.]

<!-- Examples of good triggers:
- "If p95 latency exceeds 200ms for 3 consecutive days"
- "If the team grows past 5 engineers before Phase 2 is complete"
- "If monthly storage costs exceed $X"

Examples of bad triggers:
- "If things change significantly"
- "If performance becomes a problem"
- "If the team feels it's not working" -->
```
