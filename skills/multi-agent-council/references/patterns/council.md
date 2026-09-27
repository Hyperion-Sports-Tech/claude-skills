# Council

**Type:** Core pattern
**Best for:** General multi-perspective exploration — the default when no specialized pattern fits

## What It Is

The foundational pattern. All agents share the goal and evidence packet but prioritize different objectives. Independence and explicit counterevidence help expose tradeoffs; roles do not guarantee freedom from groupthink. Follow the shared orchestration guide and selected execution backend.

## When to Use

- Default choice for any problem that benefits from multiple perspectives
- Architecture decisions, design tradeoffs, strategic direction
- Any time the team needs to surface tradeoffs that a single perspective would gloss over

## Round Structure

A Simple/Quick council defaults to one round, checkpoint, then synthesis. Standard/Deep default to two rounds. The selected backend determines transport: multi-round work can use fresh workers with explicit state packets or persistent sessions. See `references/execution-backends.md`; teammates are optional.

### Round 1 — Independent Research (parallel)

Each agent receives the goal, the relevant context, and its assigned role (value function + research directives from the role reference). Agents work in parallel. Each agent:

1. Investigates the problem through its specific lens
2. Reads relevant code, docs, or context as directed by its research directives
3. Produces a position: a concrete recommendation with reasoning grounded in its value function

All Round 1 work is parallel. Agents do not see each other's output during this round.

**Lead responsibilities** (the lead is the session running the skill):
- Dispatch per `SKILL.md` Step 3 with complete role, brief, evidence boundaries and delivery contract.
- Collect all Round 1 outputs
- Create a digest summarizing each agent's position for the user

### User Checkpoint 1

Present the Round 1 digest to the user. This is the point where the user can:

- Inject tacit knowledge that agents lack ("We tried X last year and it failed because...")
- Redirect exploration ("Agent B is on the wrong track — we can't change the database schema")
- Add constraints that were not in the original context
- Ask a specific agent to dig deeper on a point

Wait for user input unless unattended completion was explicitly accepted; then record the waived checkpoint without inventing input.

### Round 2 — Cross-Examination (parallel)

Each agent receives its own prior paper and a bounded peer digest with exact contested excerpts via the selected backend. Each agent must:

1. Identify the strongest point from each other agent
2. Respond to counterarguments against its own position
3. Revise, hold, or strengthen its recommendation — with explicit reasoning for the choice
4. Flag any new information or argument that changed its thinking

Agents work in parallel with the same peer digest; critical excerpts remain traceable to originals.

**Lead responsibilities (multi-round councils only):**
- Deliver the Round 1 Digest (not the raw peer papers) and each role's own prior state through the selected backend
- Include any user-injected context from Checkpoint 1
- Collect all Round 2 outputs

### User Checkpoint 2 — Bifurcation Point

Present Round 2 results to the user. At this point the deliberation has usually revealed one of three states:

1. **Convergence** — agents largely agree. Proceed to synthesis.
2. **Productive disagreement** — agents disagree on specific tradeoffs. The user picks a direction.
3. **Fundamental divergence** — agents are solving different problems. The user reframes or narrows the goal.

Apply the accepted checkpoint policy before synthesizing. Disagreement on missing facts calls for evidence; disagreement on values calls for an explicit owner decision, not more votes.

## Synthesis

The lead produces a proposal document containing:

1. **Recommendation** — the chosen direction in one sentence
2. **Agent contributions** — what each agent contributed to the final decision
3. **Tradeoffs accepted** — what the recommendation gives up, stated explicitly
4. **Unresolved disagreements** — any points where agents did not converge, and why they do not block the decision
5. **Next steps** — concrete actions to implement the recommendation

## Notes

- The quality of a Council deliberation depends on role selection. See the roles index for composition heuristics.
- If Round 2 produces strong convergence on a high-stakes decision, consider adding the Pre-mortem or Minority Report modifier before finalizing.
