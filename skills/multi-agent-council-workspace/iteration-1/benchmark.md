# Skill Benchmark: multi-agent-council

**Model**: <model-name>
**Date**: 2026-08-15T16:06:25Z
**Evals**: 0, 1, 2 (3 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 64% ± 38% | 42% ± 22% | +0.22 |
| Time | 391.1s ± 294.7s | 558.0s ± 378.8s | -166.9s |
| Tokens | 77261 ± 33468 | 87527 ± 58727 | -10266 |
## Analyst notes

- Eval 0 (Execute mode): both configurations score 2/8 for opposite reasons. with_skill produced NO outputs at all — the lead spawned 4 deliberators with `name:` (mailbox teammates), ended its turn 'waiting for position papers', received 0 notifications, and never synthesized (deadlock; the 4 papers exist only in the deliberators' own transcripts). without_skill finished a proposal + 3 papers but violated the structure the assertions encode (papers 1280/1565/1634 words vs <=450; ad-hoc roles; 4 of 5 review triggers non-falsifiable; sequential spawns).
- Assertion 'deliberators spawned in parallel in one message' failed in BOTH eval-0 runs (max_parallel_spawn=1 in facts.json for each) — the skill's 'all in one message' instruction was not followed even with the skill; neither run called nonexistent tools (TeamCreate/TeamDelete: 0 calls).
- Assertion 'position papers report budget consumed' passed for with_skill only via the recovered, never-delivered papers: all four self-reported '~9k tokens'; measured from their transcripts they used 27-39k OUTPUT tokens and ~485-585k billed tokens each (10-11 assistant turns) — self-reports understate by ~3-4x (output-only) to ~50x (billed).
- Eval 1 (Design mode): with_skill 6/6 vs without_skill 2/6 — the clearest skill value (verbatim role content, 3 library roles in tension, anti-sycophancy rules, pre-mortem isolation). Caveat: 4 of 6 assertions encode skill-specific structure, so the baseline is structurally disadvantaged; assertion 2 (no [PLACEHOLDER] tokens) passed in both and does not discriminate.
- Eval 1 output size: with_skill package is 10,220 words (111k tokens, 730s) vs baseline 7,640 words (81k tokens, 716s); the with_skill package repeats the full ~150-line deliberator template three times.
- Eval 2 (gate refusal): identical 2/3 in both configurations — refusal did NOT discriminate: the baseline also declined a council (it could see the installed skill's name/description in its registry and cited it). Both failed the <=400-word check (with_skill 1393 words, without_skill 1215) — the refusal path produced council-synthesis-shaped documents for a trivial question. with_skill cost 44k vs 32k tokens (+~12k reading skill files) and 194s vs 126s.
- Aggregate time/token deltas (with_skill 391s/77k vs without 558s/88k) are NOT meaningful for eval 0: with_skill's 250s/76k reflects a lead that stopped early with no output, and its 4 deliberators' ~2M billed tokens are off-ledger (not counted in subagent_tokens of the lead).
- Baseline purity: multi-agent-council is symlinked into ~/.claude/skills, so 'without_skill' agents still saw its name+description in their skill registry (eval-2 baseline explicitly mentioned it). No baseline transcript shows a Skill call or a Read of SKILL.md, so outputs are uncontaminated, but triggering behaviour is not a clean baseline.
- Sample size is 1 run per configuration per eval — no variance data; treat pass rates as indicative, not statistical.
