# Business, knowledge, and method recipes

These are configurations of the same deliberation protocol, not extra mandatory frameworks. Load only the recipe relevant to the decision. Existing domain skills provide the actual domain research method; the council adds independent critique, evidence reconciliation, and synthesis.

## Select the artifact before selecting the roles

| Use case | Decision/question | Useful seats | Evidence and output |
|---|---|---|---|
| ICP / go-to-market | Which buyer segment should receive the next selling effort? | Customer Advocate + Economist + Falsifier | Verified buying process, interviews, pipeline observations; segment decision plus cheapest discovery test |
| Pricing / packaging | Which offer is viable, and what remains unvalidated? | Customer Advocate + Economist + Operator | Willingness-to-pay evidence, delivery costs, alternatives; pricing hypothesis, sensitivity ranges, validation test. Role-play is NOT willingness-to-pay evidence |
| Fundraising / narrative review | Which claims withstand investor scrutiny? | Evidence Steward + Economist + Visionary | Dated traction/model sources; claim-level evidence audit, gaps, and narrative changes. Never fabricate investor reactions or traction |
| Founder prioritization | What should be done, deferred, or stopped? | Operator + Economist + Minimalist | Capacity, commitments, runway scenarios and opportunity cost; bounded priorities, explicit non-goals, next validation step |
| Proposal / partnership pre-mortem | What breaks delivery or buyer adoption? | Operator + Customer Advocate + Regulator when relevant | Actual scope/obligations, dependencies and approval paths; failure mechanisms, mitigations, acceptance boundaries |
| Wiki synthesis / conflicting sources | What can be asserted, and with what provenance? | Evidence Steward + Archaeologist + Integrator | Source ledger with dates/authority; claim reconciliation, unresolved conflicts, proposed page changes. No voting facts into truth |
| Research / lead-intelligence audit | Which claims are verified versus inferred? | Evidence Steward + Falsifier | Primary sources, dated contact/role evidence; corrections and gaps, not automatic CRM enrichment |
| Methods / skills / operating-process design | Does the proposed method beat a simpler baseline? | Methodologist + Operator + Falsifier | Task cases, failure modes, evaluation logs; testable protocol, ablations and stop rules rather than rhetorical endorsement |
| Product or points-economy design | What incentives, abuse paths, and adoption tradeoffs result? | Anthropologist + Economist + Stress Tester | Observed platform behavior, reward costs, incentive assumptions; design alternatives plus controlled tests. Query live platform data when needed |

Prefer two or three complementary seats. Do not add both a role and a new persona that cover the same question. A Regulator is useful only where an actual constraint is material; do not make it the default business strategy seat.

## Evidence discipline

Classify load-bearing claims rather than attaching one blanket disclaimer to a whole report:

- **Observed / primary evidence** — source, date, locator, scope and limits.
- **Meeting evidence** — exact passage or timestamp and user-confirmed speaker identity; do not guess who spoke.
- **Founder statement / conclusion** — attributed, dated, and distinct from observed facts.
- **Public research** — source and access date, with applicability limits.
- **Model inference** — derivation from named evidence, including alternative explanations.
- **Simulation / scenario** — constructed for stress-testing; not an observation or forecast.
- **Unresolved hypothesis** — missing evidence and the next discriminating test.

A citation to another agent's paper is a deliberation trace, not an independent source. Multiple agents repeating one source count as one evidence origin. Check source support and freshness, not just URL existence. Use tools for arithmetic; label assumptions, ranges, currency, period, and sensitivity rather than inventing precise financial values.

## Hyperion workspace routing (local overlay)

Apply this overlay only in the Hyperion estate. Read the CURRENT root `README.md` first; it overrides this summary if ownership changes. Do not generalize local paths as universal skill defaults.

- The root is a multi-system Obsidian vault, not one Git repository. Read the owning area's context and inspect its exact Git status before edits.
- `wiki/` owns durable reviewed company synthesis; `wiki/raw/` owns point-in-time evidence captures. Before wiki query/ingest/edit, read `wiki/CLAUDE.md`, `wiki/SCHEMA.md`, `wiki/index.md`, recent `wiki/log.md`, and search existing pages. Follow frontmatter, index, log, links, and provenance rules.
- `business/` owns editable/sendable workbooks, decks, proposals and collateral. Do not reorganize its mixed working layout as incidental cleanup.
- `records/` originals are immutable. Never edit them in place.
- `.hermes/artifacts/` holds temporary council runs and model output; it is NOT publication into company truth. After review, route a requested durable decision/research deliverable to its owner, linking the run instead of duplicating mutable artifacts.
- Zona Cóndores-specific implementation material belongs in its `project-docs/` workspace; reusable Hyperion conclusions belong in the wiki.
- Linear owns current execution status; Attio owns CRM relationships and deals; code/GitHub/CI/deployments/observability own implementation/runtime state; Zona Cóndores admin MCP owns live platform data. Query the live owner for current claims. If its tool is unavailable, mark the claim unverified rather than infer from wiki prose.
- CRM writes require verified facts, a change preview, and explicit approval. A council recommendation or an approved analysis budget is NOT CRM-write authorization. Apply equivalent scope checks before tickets, publishing, deployments, or other external mutations, then read back the exact target.
- Do not inspect secrets, credential-like files, personal records, candidate/interview/personnel/evaluation material, or `project-docs/.deleted/` without the task-specific permission required by the root rules. Naming a boundary is not permission to read it. Delegate only minimum necessary authorized evidence.

## Stakeholder simulation is hypothesis generation

Useful business personas include a club commercial director, day-to-day membership operator, fan/member, sponsor, and skeptical investor. Build personas from verified role constraints, not imagined private facts about named individuals. Label every simulated response. Turn each consequential claim into an interview question, observation plan, or experiment. Do not publish invented quotations as customer evidence.

## Method evaluation recipe

1. Define a task set before improving the method: routine questions (should not spawn), consequential decisions, conflicting evidence, absent user, missing agent, quota failure, and design-only export.
2. Run a direct single-agent baseline with comparable evidence and an explicit budget. Separate transport smoke tests from substantive quality evaluations.
3. Evaluate source support, decision usefulness, calibration, dissent fidelity, coverage of critical risks, and actionable tests. More words, more disagreement, or consensus are not success metrics.
4. Compare the same cases against the council, retaining the exact prompts/versions and raw outputs. Review blind to method where feasible. Include latency and observable resource usage; say when token/cost telemetry is unavailable.
5. Ablate expensive parts (extra round, Judge, personas). Keep them only where they materially improve the evaluation, not because they look rigorous.
6. Stop with an experiment recommendation if the decision hinges on missing market evidence. More debate cannot manufacture customer validation.
