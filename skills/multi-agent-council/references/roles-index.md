# Role Index

Each role has a **value function** (optimization lens) and concrete research directives. Actual evidence and hard constraints outrank role preferences. Adapt code-oriented directives to the domain; for business/wiki/method questions use `references/business-and-knowledge.md`. Do not force disagreement when evidence warrants agreement.

## All Roles

| Role | Value Function | Best For | Natural Tension With |
|---|---|---|---|
| Pragmatist | Optimize for least change, fastest path to ship, lowest risk | Speed- and risk-sensitive problems | Visionary, First Principles |
| Visionary | Map the ideal outcome and explicitly label relaxed constraints | Architecture decisions, greenfield design | Pragmatist, Regulator |
| Domain Expert | Test applicable precedents and their limits before reinvention | Well-established problem spaces | First Principles, Analogist |
| Archaeologist | Understand why the current system exists before proposing changes | Legacy systems, refactors, old code | Pragmatist, Visionary |
| Minimalist | Prefer deletion/simplification; justify additions by net value | Feature bloat, over-engineered systems | Visionary |
| Analogist | Transfer cross-domain structures and test where the analogy breaks | Novel problems, breaking domain tunnel vision | Domain Expert |
| First Principles | Rebuild from explicit axioms and test them against observed constraints | Problems where existing solutions may be local optima | Archaeologist, Domain Expert |
| Falsifier | Attack assumptions, not proposals; find hidden conditional dependencies | High-stakes proposals, validating architecture | Visionary, Domain Expert |
| Stress Tester | Find failure boundaries and distinguish plausible from extreme scenarios | Infrastructure, performance, security | Pragmatist, Visionary |
| Contrarian | Test the strongest alternative; concede when counterevidence warrants | Preventing premature consensus | Everyone |
| Economist | Expose cost/return assumptions and ranges without false precision | Resource allocation, build-vs-buy | Visionary, Domain Expert |
| Regulator | Enforce external constraints the team cannot control | Compliance, enterprise, SLA-bound work | Visionary, First Principles |
| Anthropologist | Study what people actually do, not what they say they'll do | DX, API design, developer-facing tools | Visionary, First Principles |
| Ethicist | Surface who this harms and who it excludes | User-facing systems, data handling, access control | Pragmatist, Economist |
| Integrator | Hold the full system in mind; find unintended cross-boundary consequences | Cross-cutting changes, shared infrastructure | Pragmatist, Minimalist |
| Evidence Steward | Keep claims traceable to adequate sources | Wiki, research, narrative audits | Visionary, Operator |
| Customer Advocate | Prioritize demonstrated buyer/user value and adoption constraints | ICP, pricing, product, partnerships | Economist, Visionary |
| Operator | Optimize for actual capacity, ownership, and sustainable execution | Founder planning and operations | Visionary, Evidence Steward |
| Methodologist | Require measurable value over a simpler baseline | Methods, skills, experiments | Visionary, Operator |

## Composition Heuristics

Pick council members based on the problem type:

| Problem Type | Recommended Roles |
|---|---|
| Architecture / refactor | Archaeologist + Integrator + Falsifier |
| Product / UX | Anthropologist + Economist + Minimalist |
| High-stakes / risky | Stress Tester + Contrarian + Falsifier |
| Data model design | First Principles + Archaeologist + Integrator |
| Legacy system work | Archaeologist + Regulator + Integrator |
| API / DX design | Anthropologist + Minimalist + Economist |
| Strategic / business | Customer Advocate + Economist + Operator |
| Wiki / evidence reconciliation | Evidence Steward + Archaeologist + Integrator |
| Method / skill evaluation | Methodologist + Operator + Falsifier |
| Fundraising claim audit | Evidence Steward + Economist + Visionary |
| Security-sensitive | Stress Tester + Regulator + Falsifier |

**Default pair** (when no specific fit): Pragmatist + Falsifier. Add a domain/value perspective only when the brief requires it. A Contrarian needs a concrete target proposal in Round 1; do not leak peer work just to provide an emerging consensus.
