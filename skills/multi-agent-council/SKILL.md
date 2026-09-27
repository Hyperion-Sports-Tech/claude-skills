---
name: multi-agent-council
description: >
  Use when stress-testing complex decisions or methods.
  Evidence-led council for analysis, planning, business, wiki synthesis,
  and architecture. Trigger: "run a council", "council this", "design a
  council", "explore from multiple angles". Not for routine questions.
version: 2.0.0
metadata:
  hermes:
    tags: [deliberation, decision-making, research, business, planning]
    related_skills: [autonomous-coding-agents]
---

# Multi-Agent Council

Use independent perspectives to improve a decision, not to manufacture consensus. Produce a source-grounded recommendation, preserved dissent, or a concrete experiment when evidence is insufficient. The method works in Hermes, Claude Code, and exported prompts; the transport is a separate choice.

## Core concept

The power of a council comes from **institutionalized disagreement**: complementary objectives, independent first passes, and explicit counterevidence. A role is an optimization lens, not permission to reject facts or a guarantee against groupthink. Hard constraints come from the actual problem and verified obligations, not theatrical identities. Any role may update, agree, abstain, or report that its preferred objective is infeasible.

Research comes before debate. Separate observed evidence, user/founder statements, public research, model inference, simulation, and unresolved hypotheses. Repeated model agreement is not independent corroboration. Tools and access are least-privilege, not unrestricted by default.

The human stays in the loop as the **carrier of tacit knowledge** — context that exists nowhere in any document. Enter at checkpoints between rounds, not continuously.

---

## Workflow

### Step 1 — Frame the decision and apply the value gate

Retrieve available context first; ask at most 3 focused questions only for missing information that changes the design. Write a brief: decision/question, alternatives (including status quo or defer), stakes, success criteria, constraints, reversibility, evidence gaps, decision owner, authorized sources, and intended artifact destination.

**Design mode first:** "design a council", "give me the prompts", or "export" means export only. Do not require execution-budget approval and do not spawn agents. Fully populate the package and finish after Step 3.

For execution, justify a council with either **at least 2 meaningful tradeoffs**, or one consequential uncertainty/irreversible risk where independent scrutiny has clear value. The lead should discover and name the tradeoffs; do not force the user to do the analysis before receiving help. For routine questions or one obvious direction, give direct analysis instead. A missing empirical fact may require research or an experiment rather than a council.

### Step 2 — Bound the run and compose the council

Choose the smallest adequate run. These are workload defaults, NOT measured token/cost forecasts:

| Tier | Seats | Rounds | Research allowance per seat per round |
|---|---|---|---|
| Simple / Quick | 2 | 1 | Up to 6 substantive source/tool investigations |
| Moderate / Standard | 3 | 2 | Up to 10 investigations |
| Complex / Deep | 4 | 2 | Up to 15 investigations |

Very Complex work must be decomposed into scoped decisions, not an automatic multi-level fan-out. An investigation may span tool calls; this is a soft research allowance, not a hard token or runtime limit. Record actual tool usage when observable. Never invent token consumption; say `unavailable` when telemetry is absent. If estimating API dollars, use current prices and tools for arithmetic; label input/cache/output assumptions. Claude Max means shared subscription usage, not unlimited or zero-resource work.

Before spawning, present backend/model (or unknown), roles, rounds, concurrency cap, research allowances, soft timebox, output caps, checkpoint policy, and all modifier calls. All modifiers default off and are individually disableable. Pre-mortem, Minority Report, or Judge adds one isolated pass each; Stakeholder Sim adds one per persona; Six Hats must declare its selected execution option and total passes. Do not add work silently.

Require acceptance of this configuration; the user's request counts if it already specifies and accepts those bounds. Reconfirm expansions or backend switches that change cost/data routing. No repeated approval is needed for the same already-accepted run.

Read `references/patterns-index.md` and `references/roles-index.md`. Use one core pattern; load only chosen pattern/role files. Roles must cover distinct questions in genuine tension, not duplicate reviewers. Core patterns such as Asymmetric Info may diversify information rather than objectives. For business/wiki/method tasks, load `references/business-and-knowledge.md`. For missing roles, use `references/custom-role-template.md`.

### Step 3 — Select transport, build packets, execute or export

**You are the council lead.** The user-facing session handles checkpoints and synthesis; do not delegate that accountability. Read `references/execution-backends.md` and inspect actual capabilities before dispatch. Round count does not determine whether persistent teammates are available.

Supported transports: Hermes native `delegate_task`; separately supervised Claude interactive sessions through Hermes; Claude Code native subagents/optional teams; prompt export. For Claude interactive, also load `autonomous-coding-agents` when available. Max authentication stays inside Claude Code, never inside Hermes delegation configuration.

Fill `references/deliberator-prompt.md` with role title, value function, lens, domain-adapted research directives, brief, source boundaries, budget, round number/state, and the selected delivery contract. No unresolved placeholders or tools from another backend. Children do not inherit the parent conversation.

Create a task-local run ledger before execution: accepted configuration, source packet version, expected role/round outputs, backend/model, handles, status, and output paths. Use an authorized scratch location, not durable company truth. The lead saves returned papers; workers are read-only unless separately authorized. Independent Round 1 seats do not see each other's answers or a lead recommendation.

In Design mode, deliver the fully populated prompts, round/checkpoint plan, budget proposal, source requirements and selected modifier prompts. No agents, execution approval, or automatic downstream actions. Stop here.

### Step 4 — Independent research

Dispatch independent seats together within the concurrency limit. Collect bounded papers (400 words plus a compact evidence ledger), preserving originals. Read `references/orchestration-guide.md` for dispatch accounting, evidence checks, and digests. Never treat an echoed completion marker, an idle process, or a missing response as a completed paper.

### Step 5 — Checkpoint and bounded cross-examination

Default: pause after the digest for user context. If the user explicitly authorizes unattended completion, log `checkpoint waived` and proceed within accepted constraints; do not invent founder input. Material ambiguity, missing authorization, or unsafe action still blocks that action, not delivery of a provisional report.

For a second round, send each role its own prior paper, a bounded peer digest with exact disputed excerpts, and checkpoint changes. Native one-shot workers are re-dispatched with explicit state; interactive Claude roles keep their own session. Require the strongest counterargument, hold/update/abstain with cited reason, remaining dissent, and a discriminating test. New evidence, a demonstrated reasoning correction, or clarified decision weights can justify change; no ceremonial stubbornness.

Stop after the accepted rounds, when further debate adds no decision-relevant information, or when missing empirical evidence demands a test. More rounds require approval. Never optimize for unanimity or keep debating merely to remove dissent.

### Step 6 — Synthesis, verification, and cleanup

Use `references/proposal-document.md`. Select on declared criteria and evidence, not majority vote. Include rejected alternatives, load-bearing assumptions, preserved dissent, confidence limits, cheapest next test, review triggers, and named missing contributions. All outputs remain recommendations until the decision owner accepts them.

Run only accepted modifiers. Preserve the lead draft before reading an independent Judge output; no claims of blind auditing if information leaked. Judge absence permits a marked provisional report, not a false audit approval or automatic implementation.

Verify source support, claimed files/results, expected respondent counts, and exact cleanup state. Shut down only run-owned sessions through the selected backend; no assumed-dead shortcuts. Record real telemetry or `unavailable`, not invented usage.

### Step 7 — Route the deliverable without expanding authority

Keep the council run as analysis evidence. Route a requested final artifact to its owning repository/system with provenance and local conventions. In Hyperion, load the business/knowledge reference and current root map; scratch output alone does not satisfy a request for durable wiki publication. Council approval does not authorize CRM writes, external messages, commits, deployments, or records changes.

If implementation is requested, discover the available planning/development skill instead of assuming `writing-plans-for-teams` or `agent-team-driven-development` is installed. Keep analysis, decision approval, and execution as distinct steps.

---

## Pitfalls and verification

- Role-play is not customer evidence, legal advice, or independent corroboration.
- Context isolation is not filesystem isolation; shared sources or model families can correlate mistakes.
- Correct reasoning may converge; forced disagreement is as misleading as forced consensus.
- Static prompt assertions verify structure, not decision quality. Compare against a single-agent baseline on real tasks before claiming improvement.
- Before completion: expected outputs accounted for, material citations checked, uncertainties labeled, correct destination, no unauthorized writes, and owned sessions actually closed.

---

## Reference files

- `references/roles-index.md` — Role library index with value functions and composition heuristics
- `references/roles/*.md` — Individual role files with lens and research directives
- `references/patterns-index.md` — Pattern library index
- `references/patterns/*.md` — Individual pattern files with prompt templates
- `references/deliberator-prompt.md` — Shared prompt template for spawning deliberator agents
- `references/orchestration-guide.md` — Backend-neutral rounds, evidence accounting, and checkpoints
- `references/execution-backends.md` — Hermes native, Claude interactive/Max, Claude native, and export
- `references/business-and-knowledge.md` — Business/wiki/method recipes and Hyperion routing
- `references/evaluation.md` — Offline checks, behavioral cases, baseline evaluation, and shared-source installation
- `references/custom-role-template.md` — Guide for creating domain-specific roles
- `references/proposal-document.md` — Output format for the proposal document
