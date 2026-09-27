# Asymmetric Info

**Type:** Core pattern
**Best for:** Problems where different stakeholders hold different context and no single person has the full picture

## What It Is

Each agent receives a different authorized context slice. Unlike Council, diversity is primarily informational, not competing objectives. The result reveals assumptions created by missing information. Follow the shared orchestration guide and execution backend; do not claim that prompt omission enforces access isolation.

For hard isolation, use curated inline packets with tools disabled or an actual filesystem/access boundary. Shared unrestricted tools can reveal other slices or drafts. If only prompt-level separation is possible, label it as such and record leakage; never treat this as a confidentiality control.

## When to Use

- Cross-functional decisions where engineering, product, and ops each hold context the others lack
- Problems where the right answer depends on combining information that currently lives in silos
- Situations where past proposals failed because they optimized for one slice while ignoring another

## Typical Context Slices

The three default slices. Adapt based on the actual problem.

**Agent A — Codebase only:** Sees the current code, architecture, and technical constraints. Has no information about business requirements or infrastructure limitations.

**Agent B — Requirements only:** Sees product goals, user stories, success metrics, and business constraints. Has no visibility into the codebase or deployment environment.

**Agent C — Ops/Infra only:** Sees deployment architecture, SLAs, monitoring, operational capacity, and infrastructure constraints. Has no visibility into the codebase or product requirements.

## Round Structure

### Round 1 — Isolated Proposals (parallel)

Each agent receives only its assigned context slice plus the shared goal. Agents work in parallel. Each agent:

1. Proposes an approach based exclusively on what it knows
2. Explicitly states what it is assuming about the context it cannot see
3. Lists the questions it would need answered to have full confidence in its proposal

**Lead responsibilities:**
- Dispatch a two-round run through the selected backend; give each worker only its assigned packet and shared goal. Fresh-worker state replay and persistent sessions are both supported.
- Enforce isolation: do not leak context between agents during Round 1
- Collect all Round 1 outputs
- Create a digest highlighting where proposals conflict and where assumptions diverge

### User Checkpoint 1

Present the Round 1 digest to the user. Highlight:

- Where agents made conflicting assumptions about context they could not see
- Where proposals are incompatible because of missing information
- Gaps that none of the agents can fill (the user may need to provide additional context)

The user can reveal additional context, correct false assumptions, or approve another slice. Under an explicit unattended waiver, record missing user input and remain within the accepted sources and budget.

### Round 2 — Information Sharing (parallel)

Analytical boundaries are lifted only for sources already authorized for sharing. Each agent receives its own paper and the peer digest with newly disclosed evidence excerpts through the selected backend. Privacy and access boundaries are never lifted merely because a round changes. Each agent must:

1. Identify which of its Round 1 assumptions were wrong
2. Identify what it now knows that changes its recommendation
3. Respond to gaps in other agents' understanding — correct their assumptions about its domain
4. Produce a revised proposal that accounts for the full picture

**Lead responsibilities:**
- Deliver a bounded digest plus necessary originally-siloed evidence excerpts; preserve source IDs and exact disputed claims, with targeted retrieval if needed
- Include any additional context from the user checkpoint
- Collect all Round 2 outputs

### User Checkpoint 2

Present Round 2 results. By this point, agents should have a shared understanding. The user confirms whether the combined picture is accurate before synthesis.

## Synthesis

The lead produces a proposal document containing:

1. **Full picture map** — the combined understanding from all context slices, including where slices conflicted and how conflicts were resolved
2. **Recommendation** — a proposal that accounts for all three slices
3. **Information gaps closed** — which Round 1 assumptions turned out to be wrong and how the recommendation changed as a result
4. **Remaining blind spots** — context that no agent held and that the user did not provide
5. **Cross-slice dependencies** — decisions that require ongoing coordination between the domains (e.g., "if the API contract changes, ops must update the load balancer config")

## Notes

- The power of this pattern is in Round 1's isolation. Resist the urge to give agents more context than their slice — the value comes from seeing what they assume when they do not know.
- This pattern works especially well when the user suspects that a previous decision failed because one perspective dominated.
