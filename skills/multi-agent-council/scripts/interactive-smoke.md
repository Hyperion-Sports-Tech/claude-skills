# Read-only interactive adapter smoke review

This is a bounded test of the revised skill contract, not an instruction to run a council or modify files. Do not use additional agents or external systems. Read `skills/multi-agent-council/SKILL.md`, `references/execution-backends.md`, `references/deliberator-prompt.md`, and `references/patterns/judge.md` (reference paths relative to that skill).

Return under 350 words:

1. Does the contract separate transport from rounds, replay prior-role state for fresh Hermes workers, and preserve per-role continuity for external interactive Claude sessions? Cite the text, not assumptions about an unavailable runtime.
2. Is the Judge/lead comparison logically executable without the Judge seeing the lead draft? Identify at most two concrete remaining defects with file:line citations. Say no defect found if warranted; do not invent one to satisfy a quota.
3. Resolve these protocol cases in one sentence each:
   - User requests prompt export only; no execution budget has been accepted.
   - A completion marker notification fired only on an echoed initial user prompt.
   - A simulated customer persona claims willingness to pay without an interview or observed purchase.
4. End with `COUNCIL_SMOKE_COMPLETE`, then wait for a subsequent instruction.

A live external PTY can be captured and steered by its supervising Hermes session. Do not assume interactive sessions are non-persistent or that a human must manually copy every answer. This exercise verifies the running session's transport and the specified cases, not general council quality, multi-seat concurrency, or hard confidentiality isolation.
