<!-- Recovered by the eval harness from the deliberator's transcript. The council lead NEVER received this paper (delivery deadlock) — see grading notes. -->

# Falsifier — Round 1 Position Paper

## Key findings

**The script's own invariant is unpatched.** `skill_status()` (skills.sh:89-123) correctly refuses to clobber unmanaged dirs (conflict branch, skills.sh:158-160) — real safety, verified by reading the code. But the live symlink is an absolute path baked at install time: `~/.claude/skills/multi-agent-council -> /Users/tomasdussaillant/repos/skills/skills/multi-agent-council` (confirmed via `ls -la`). Rename `skills/` or move the repo → silent dangling link. `doctor` (skills.sh:323-347) only checks that the `my-skills` launcher resolves on PATH — never that existing skill links still resolve. Assumption (iii), "full control over version semantics," holds for install/uninstall bookkeeping but has a real gap on the one invariant that matters most.

**(i) "discoverability"** is already true, already free — not hypothetical. `~/.agents/.skill-lock.json`: `"brand-identity": {"source": "tomiduss/claude-skills", ...}`. The standard `npx skills` flow already installs a skill from this exact repo today, zero marketplace submission needed. Cheapest check: done, cost zero.

**(ii) "no maintenance"** conflates two labor pools. Lockfile `installedAt == updatedAt` for most entries shows updates are pull-based, not automatic — the user still runs a command and still authors SKILL.md content either way. "No maintenance" holds only for distribution tooling, not content.

**(iv) "any marketplace will want per-skill versions"** is falsified here. `claude-plugins-official/.claude-plugin/marketplace.json` entries for `context7`, `frontend-design`, `superpowers` carry **no `version` field** (parsed directly). `installed_plugins.json` shows 7+ plugins as literal `"version": "unknown"` while `gitCommitSha` is *always* present — SHA is the real enforced identity; semver is optional. Stronger: Anthropic's own `anthropic-agent-skills` marketplace bundles 4 skills (xlsx/docx/pptx/pdf) under **one** plugin, **one** version — structurally identical to this repo's current monorepo. The reference implementation contradicts the premise driving half this decision.

## Proposed approach

Don't commit to (a)/(b)/(c) or per-skill versioning yet — two of four stated assumptions fail against evidence on this machine, a third has a live gap. Run `npx skills add` against 2-3 more of the 8 skills (brand-identity already proven), and confirm Claude Code *loads* skills reached via `~/.claude/skills/x -> ../../.agents/skills/x` — discoverability ≠ confirmed usability; I did not verify that hop. If it holds, skills.sh loses its remaining justification (2 commits ever) and per-skill versioning has no marketplace forcing it.

## Tradeoffs accepted

Defers a clean answer; skills.sh keeps straddling half-deprecated longer — the exact ambiguity the user wants to escape. Accepted because locking per-skill semver on a falsified premise costs more to reverse than a few days running both flows in parallel.

Budget consumed: ~9.5k tokens, 7 tool calls.
