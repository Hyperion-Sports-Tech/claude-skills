# multi-agent-council — improvement assessment (2026-08-15)

Scope: "how could we improve the multi-agent-council skill further?" — assessment only; no skill files were modified.
Skill snapshot used: commit `48cffd1` (today), symlinked live at `~/.claude/skills/multi-agent-council`.

## TL;DR

1. **The execution mechanics in Step 3 do not match the harness you are running (Claude Code 2.1.233).** `TeamCreate`/`TeamDelete` do not exist here (even with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` set); `team_name` is deprecated/ignored; and passing `name:` to `Agent` (which the skill tells the lead to do for Path A) turns the deliberator into a *mailbox teammate whose final output is never delivered*. In the live eval, a Simple-tier council **deadlocked**: 4 deliberators wrote good, well-cited papers that the lead never received. → Blocker; fix first.
2. **The good news is the fix is a simplification.** Verified in this harness: an unnamed `Agent` call is async, its result arrives as a `<task-notification>` with `<result>` **and exact `<usage>` (tokens / tool_uses / duration)**, and `SendMessage(to: <agentId>)` *resumes it with memory intact* and yields another `<result>` notification. Multi-round councils therefore need **no team, no `[MODE]`, no `[LEAD_NAME]`, no shutdown, no `TeamDelete`** — Path A and Path B collapse into one mechanism.
3. **The cost model is unvalidated and wrong by 3–50×.** Deliberators self-reported "~9k tokens" (all four, identically); measured from their transcripts each used 27–39k *output* tokens and ~485–585k billed tokens over 10–11 turns. The harness gives the lead real numbers for free (`<usage>`), so self-estimation can be dropped and the tier table calibrated from data.
4. **Where the skill clearly earns its keep today: Design mode and the gate.** Design-mode export scored 6/6 vs 2/6 baseline (verbatim roles, tension pairs, anti-sycophancy rules, pre-mortem isolation). The complexity gate refused a trivial question correctly (0 agents spawned).
5. Second-tier improvements (each low-cost, high-leverage): persist every artifact to a run directory (also fixes SPOF/recovery and gives Judge/Red-Team file inputs), an explicit unattended mode, a one-shot pre-flight brief instead of a 3-stage interrogation, value functions rewritten as structural boundaries, and a proper eval suite (now bootstrapped in this workspace).

Benchmark (iteration 1, 1 run per cell): with_skill **64%** vs without_skill **42%** pass rate; details and analyst notes in `iteration-1/benchmark.md`; outputs and grades in the viewer (`http://localhost:3117`).

---

## Method

- Read SKILL.md, all 25 reference files, both test scripts, the redesign spec (2026-03-19), the hardening plan (2026-04-09), and the git history.
- Probed the harness with 3 tiny agents (memory-persistence across `SendMessage`, nested spawning, unnamed-vs-named delivery semantics).
- Ran 3 realistic eval prompts × 2 configurations (with skill / no skill path) as background subagents, graded by independent grader agents against 17 assertions, plus a reusable inspection script that extracts facts from transcripts (`tools/inspect_run.py`).
- Evals: (0) Execute-mode Simple-tier council on a real problem in this repo (skills.sh vs `npx skills`), unattended; (1) Design-mode export (RLS vs app-level auth, Moderate + pre-mortem); (2) a trivial question the gate should refuse.

---

## A. Blocker: harness mismatch in Step 3 (verified, not speculative)

| Skill says | Harness (2.1.233, this machine) actually does |
|---|---|
| Path B: `TeamCreate(...)`, teammates with `team_name`, `TeamDelete` at the end | `TeamCreate`/`TeamDelete` **do not exist**; `team_name` is "Deprecated; ignored. The session has a single implicit team." |
| Path A: subagent "returns its position paper as the tool result" | `Agent` returns immediately ("Async agent launched"); the paper arrives later as a `<task-notification>` with `<result>` + `<usage>` |
| Path A: spawn with `name:` the role slug | `general-purpose` + `name:` → "Spawned successfully… will receive instructions via mailbox" — a teammate whose **plain final output is never delivered** and which produces **no completion notification** (probe-alpha, probe-beta, and all 4 eval deliberators) |
| `[LEAD_NAME]` = part before `@` in `lead_agent_id` from `TeamCreate` | The lead is addressed as literal `team-lead`. Teammate→lead `SendMessage`s and `idle_notification`s are delivered **only at the lead's turn boundary** (probe-alpha's message, sent 15:34, reached me after I ended my turn ~16:10). Plain final text is still never delivered. In the nested eval, the deliberators' idle notifications routed to the **top-level session**, not to the subagent that spawned them — so a mailbox design cannot work when the lead is itself a subagent |
| A one-shot subagent's name "becomes unaddressable once it finishes" | The opposite: `SendMessage(to: <agentId>)` **resumes** a finished unnamed agent with its context intact and yields a fresh `<result>` notification (verified: "Codeword stored" → "CODEWORD: XKZ") |
| Round-2 requires persistent teammates | Not needed — resume-by-agentId gives Round 2 to plain async subagents |

Live consequence (eval-0 with_skill): lead read the skill, chose Archaeologist + Domain Expert + Falsifier + Economist, spawned them **with `name:`** in 4 separate messages (not one — the "all in one message" instruction was also ignored), created the output dir, then ended its turn: *"Deliberators are researching in the background. Waiting for their position papers to arrive"*. Zero notifications, zero outputs. The four papers (418–455 words, real `file:line` and URL citations, all with "Budget consumed: ~9k tokens") were recovered from the deliberators' transcripts by the harness — see `iteration-1/eval-0-…/with_skill/run-1/recovered-from-deliberator-transcripts/`.

Also observed: `fork` + `name:` behaves as async (the baseline's 3 forks completed and wrote files), so `name` is only a trap for `general-purpose` — which is exactly what the skill prescribes.

Addendum (after the turn boundary): the four named deliberators each sent `{"type":"idle_notification","idleReason":"available"}` to my session when they finished — never their papers. A mailbox-based lead would therefore know *that* an agent finished only after yielding its turn, and would still have to fetch the paper by other means (explicit `SendMessage` from the agent, or a file). Async agents deliver the paper itself, mid-turn.

**Recommendation A1 (rewrite Step 3 around what works):**
- Spawn each deliberator as an **unnamed** async `Agent` (`subagent_type: general-purpose`, `model` per tier); keep a private role→agentId map.
- Round 1 papers arrive as `<task-notification>` results; record each notification's `<usage>` next to the role.
- Round 2 = `SendMessage(to: agentId, message: <digest + directives>)`; responses arrive as new `<result>` notifications. No team, no shutdown, no `[MODE]`/`[LEAD_NAME]` placeholders (delete both from `deliberator-prompt.md`), no `TeamDelete`, no 30-second ack protocol.
- Belt-and-braces: **also** instruct deliberators to write their paper to `<run-dir>/round-1/<role>.md` (the baseline lead independently arrived at this file handoff, and it makes recovery trivial — see C1).
- Keep a 3-line "if your harness has `TeamCreate`/teams" fallback note if you also run older builds — but make async+resume the primary path.
- Update `tests/prompt-assertions.sh`: several checks assert the *old* API strings (`no .team_name`, `team_name: .council`, `TeamDelete fails…`, `30 seconds`, `presumed dead`) and will need to flip.

---

## B. The cost model is unvalidated (and self-reporting is fiction)

- Measured (Sonnet 5 deliberators, Simple tier, ~10 tool calls each): output tokens 26.6k / 29.1k / 33.2k / 39.3k; billed ≈ 485k–585k each (cache reads dominate); 10–11 assistant turns; ~2 min wall-clock each. Self-reported: "~9k / ~9k / ~9.5k / ~9.5k".
- SKILL.md tier table: "Simple … ~10k tool budget/agent … ~50–90k total … ~5–9× single-Opus". Off by ≥3× on output tokens alone; the "× single-Opus" framing is undefined; "Sonnet 4.6" is stale (Sonnet 5 / Opus 5 / Haiku 4.5 today); "`model:` per tier" is never specified.
- Plan (2026-04-09) Test H "cost regression" and Test J "reference problem" were never executed; no `tests/reference-problem.md` exists.

**Recommendation B1:** express the per-agent budget in **tool calls** (observable by the agent) and let the lead record **harness-reported** usage from each notification; drop "report actual budget consumed". Put a "Council cost" line in the Proposal Document (per-role tokens + total) so every run calibrates the table. Re-derive the tier table from 2–3 real runs and name the default models (e.g. deliberators `sonnet`, Judge/Red-Team `opus`).

---

## C. Behavioural findings from the evals

1. **No artifacts are persisted.** Everything lives in the conversation; when the lead's turn ended, all research was lost from the lead's point of view. The plan deferred "SPOF recovery (A.1)" and the "Deliberation Ledger (P1.1)" as heavy — but a plain run directory (`docs/council/<date>-<slug>/{brief.md, round-1/*.md, digest-1.md, round-2/*.md, proposal.md, cost.json}`) is cheap and unlocks: recovery/rehydration, Judge and Red-Team inputs by **file path** instead of 15–25k-token pasted prompts, a durable deliverable, a real input file for `writing-plans-for-teams`, and gradeable evals. **→ C1: persist artifacts.**
2. **No unattended mode.** The eval prompt said "don't block on me at checkpoints"; the skill has no concept for that, so behaviour was improvised. Real users say this constantly. **→ C2: add an explicit "unattended" option** (all checkpoints auto-proceed, everything is written to the run dir, the digest/summary are included in the proposal) while keeping checkpointed as the default.
3. **The gate's refusal path is disproportionate.** With and without the skill, the "not warranted, here is a direct answer" for tabs-vs-spaces ran 1.2–1.4k words with tables and config blocks. The refusal message also addresses a live user ("Want me to analyze this directly?") even when none is present. **→ C3: make the fallback a bounded direct answer** (≤300 words unless the user asks for more) and phrase the refusal so it works with or without a live user.
4. **Prompt-following slippage in deliberators:** 3 of 4 papers exceeded 400 words (418–455). Minor; a "hard stop at 400 — cut findings, not citations" line or a structural cap (bullets per section) would hold better than a number.
5. **Design-mode export is faithful but heavy:** 10.2k words, the full ~150-line deliberator template repeated 3× (including "How you were spawned: teammate", "Shutdown", tool lists irrelevant to a human running it in Claude.ai). **→ C4: export = one shared block + per-role deltas, or one file per role,** with a 1-page "how to run" — and never mention `[MODE]`/shutdown in an export.
6. **Parallel-spawn instruction ignored** in both eval-0 runs (one `Agent` call per message). Harmless for concurrency (calls are async anyway) but the instruction is dead weight as written; either drop it or explain *why* (all results arrive as notifications; batching just saves turns).
7. Every deliberator re-oriented itself in the repo (`ls`, `git log`, reading skills.sh) — 4× duplicated discovery. **→ C5: the lead writes a short `brief.md` (repo map, key files, what has been tried) into `[CONTEXT]`/a `[STARTING_POINTS]` slot** before spawning; ~1 tool call for the lead saves 3–5 per agent.

---

## D. Internal contradictions and drift (cheap, do alongside A)

- `patterns/council.md:48` "Each agent receives **all other agents' Round 1 positions**" vs `council.md:58` "the Round 1 Digest (**not the raw papers**)"; same contradiction in `patterns/temporal.md:51,59` and `patterns/asymmetric-info.md:54,62` versus `orchestration-guide.md:31-32` (2,000-token digest cap).
- "team lead" wording (25× in `judge.md`, also pre-mortem, six-hats, proposal-document) now that the lead is the session and there is no team — rename to "lead" everywhere.
- `judge.md` says the Judge "applies only to multi-round / Path B councils"; with A1 there is no Path B — say "councils with a Round 2".
- Skills must be self-contained (CLAUDE.md), yet `pre-mortem.md:48` cites `docs/superpowers/plans/…research/` and `judge.md` carries "an earlier draft was rejected…" narrative — trim to the rule + the reason.
- The plan's "Pilot status" section for the Pragmatist standalone (14-day kill criterion, ~May 16) never landed in SKILL.md and appears not to have been evaluated; decide and either record the verdict or delete `.claude/agents/pragmatist.md` + `tests/value-function-check.sh` per the plan's own rule.
- Static tests are string-greps on the old API and cannot detect a run that deadlocks; keep them as regression guards for wording, but the behavioural evals in this workspace should become the primary test.

---

## E. Design-level opportunities (bigger swings, after A–D)

- **E1 Value functions as structural boundaries.** Only ~6 of 15 role files phrase the value function as a hard "cannot/must/only" constraint; the rest are preferences ("Optimize for…", "Study what people do…"). SKILL.md's own example ("You cannot propose adding code — only removing it") is *stronger* than the actual Minimalist file ("addition is *almost always* wrong"). Add a one-line **Forbidden conclusions** field per role — it makes Round-2 sycophancy checks verifiable and gives the lead something concrete to flag.
- **E2 One-shot pre-flight brief.** Today Step 1 is a 3-condition interrogation (name 2 tradeoffs → pick tier → pick modifiers → accept cost). Have the lead do a 1–2 tool-call scan and *propose* the tradeoffs it sees, tier, roles, modifiers and a cost line in **one** message; the user answers "go / change X". Keep the refusal when <2 real tradeoffs exist, but the lead should be the one who tries to find them first.
- **E3 Non-code problems.** Research directives and citation rules assume a codebase; add one line for strategy/product questions (web/doc citations, no `file:line`).
- **E4 Description optimisation** via the skill-creator loop once the mechanics are fixed (the current description is reasonable; the gate already stopped a trivial request in eval-2).
- Deferred items from the April plan that become cheap once C1 exists: SPOF recovery (rehydrate from the run dir), stall detection (notifications tell you exactly when an agent stops), the "ledger" (it *is* the run dir).

---

## F. Eval infrastructure now in place (reuse for iteration 2)

- `skills/multi-agent-council/evals/evals.json` — 3 prompts + 17 assertions.
- `skills/multi-agent-council-workspace/iteration-1/` — per-eval `with_skill/` and `without_skill/` runs with `outputs/`, `transcript.md`, `facts.json`, `grading.json`, `timing.json`; `benchmark.{json,md}` with analyst notes; `skill-snapshot/` (pristine copy of today's skill for the next baseline).
- `tools/inspect_run.py` (facts from outputs + transcript: parallelism, nonexistent-tool calls, per-file word/citation counts, placeholders, child-agent usage) and `tools/jsonl_to_md.py` (compact transcripts for graders).
- Eval-suite gaps flagged by graders: add a Moderate-tier (2-round) Execute eval to exercise resume-by-agentId; add an assertion that the Problem/Context in exports preserves the user's stated constraints; tighten the "≤400 words" assertion to the whole file; the placeholder assertion is non-discriminating.

---

## Suggested order of work

1. **A1 + D** (mechanics rewrite + contradictions) — unblocks everything; re-run eval-0 to confirm a Simple council completes end-to-end. *(~1 focused session)*
2. **C1 + C2** (run directory + unattended mode) and **B1** (harness usage, recalibrated table). *(same session or next)*
3. **C3–C5, E1, E2** — quality passes, each verifiable with the existing evals + one new Moderate-tier eval.
4. **E4** — description optimisation last.
