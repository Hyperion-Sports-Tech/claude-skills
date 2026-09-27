# Temporal

**Type:** Core pattern
**Best for:** Decisions with tech debt implications, long-term sustainability concerns, or tension between shipping now and building right

## What It Is

Three agents prioritize different time horizons while respecting actual hard constraints. State the cost imposed on other horizons; agreement and feasible hybrids are allowed. Apply the shared orchestration/checkpoint protocol and selected execution backend. For business decisions, adapt horizons to runway, sales cycles, or delivery commitments rather than assuming software sprints.

## When to Use

- Build-vs-buy decisions
- "Quick fix now vs. proper solution later" tensions
- Architecture decisions that create or resolve tech debt
- Any decision where the team says "we'll fix it later" — this pattern makes "later" concrete

## Agents

**Agent NOW:** Prioritize the immediate horizon and current capacity. Name long-term liabilities rather than ignoring them; show the cheapest reversible path.

**Agent Q+1:** Optimize for next quarter. What sets the team up best for the next three months? Allowed to accept short-term cost for medium-term payoff. Thinks about the next 2-3 features the team will build.

**Agent FUTURE:** Prioritize the long-term horizon. Label assumed growth and relaxed resource constraints as scenarios, not forecasts; do not relax actual legal, safety, or privacy constraints. State a feasible migration path when possible.

## Round Structure

### Round 1 — Horizon Proposals (parallel)

Each agent receives the goal, context, and its assigned time horizon. Agents work in parallel. Each agent:

1. Proposes an approach optimized exclusively for its horizon
2. States what it is deliberately ignoring (the other horizons' concerns)
3. Describes the expected state of the system at its target time

**Lead responsibilities:**
- Dispatch two rounds through the selected backend, each role assigned its horizon and complete state packet
- Keep horizon priorities explicit without requiring irrational recommendations
- Collect all Round 1 outputs
- Create a digest contrasting the three proposals

### User Checkpoint 1

Present the three proposals side by side. Ask the user:

- Which time horizon matters most for this decision?
- Are there hard constraints that make one horizon non-negotiable? (e.g., "we must ship by Friday" locks in NOW; "we're hiring 5 engineers next quarter" changes Q+1)
- Is there a hybrid the user already has in mind?

### Round 2 — Cross-Horizon Critique (parallel)

Each agent receives its own prior paper and a bounded peer digest with exact contested excerpts through the selected backend. Each agent must:

1. Critique the other horizons' proposals from its own perspective
2. Specifically name what the other proposals sacrifice on its timeline
3. Identify any point of genuine compatibility — where its horizon's needs can be met without undermining the others
4. Produce a "cost statement": if the team chooses a different horizon, what exactly does that cost from this agent's perspective?

**Lead responsibilities:**
- Deliver the peer digest and own-role state without broadcasting every raw paper
- Include the user's horizon priority from Checkpoint 1
- Collect all Round 2 outputs

### User Checkpoint 2

Present the cross-horizon critique and confirm direction before synthesis.

## Synthesis

The lead produces a proposal document containing:

1. **Tradeoff matrix** — a table showing what each horizon gains and sacrifices under the recommended approach
2. **Recommendation** — the chosen path with explicit horizon weighting (e.g., "optimize for Q+1 with NOW constraints respected")
3. **Debt receipt** — if the recommendation favors a shorter horizon, document the debt being taken on:
   - Estimated effort to undo or redo this decision in 18 months
   - Which future features become harder or impossible
   - The earliest point at which this will become a problem
   - Specific trigger conditions for revisiting the decision
4. **Migration path** — if applicable, how the NOW solution evolves toward the FUTURE solution over time

## Notes

- The debt receipt is the most valuable output. Attach it to the decision record so future teams understand what was traded and why.
- If the user picks NOW and the debt receipt is large, consider running the Pre-mortem modifier to stress-test the short-term choice.
