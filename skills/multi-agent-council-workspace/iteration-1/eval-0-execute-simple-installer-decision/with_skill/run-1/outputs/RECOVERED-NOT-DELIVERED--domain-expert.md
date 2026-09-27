<!-- Recovered by the eval harness from the deliberator's transcript. The council lead NEVER received this paper (delivery deadlock) — see grading notes. -->

# Domain Expert — Round 1 Position Paper

## 1. Key findings

- **`npx skills` / agentskills.io** (spec: agentskills.io/specification) needs no marketplace manifest and no semver — it discovers `skills/<name>/SKILL.md` at any repo path and tracks installs by **content hash**, not a version number. Confirmed in this machine's own lockfile (`~/.agents/.skill-lock.json`): `skillFolderHash`/`installedAt` per skill, pulled straight from `obra/superpowers` and `vercel-labs/skills` (github.com/vercel-labs/skills) — both **monorepos of many skills sharing one history**. `npx skills add tomiduss/claude-skills --skill multi-agent-council` would work today, unpublished.
- **anthropics/skills' own marketplace.json** (`~/.claude/plugins/marketplaces/anthropic-agent-skills/.claude-plugin/marketplace.json`) groups 16 skills into 3 themed plugins (`document-skills`, `example-skills`, `claude-api`), each just `{name, source:"./", skills:[...]}`. **One `metadata.version` for the whole marketplace** — no per-skill or per-plugin version field exists.
- **obra/superpowers-marketplace** (`.../superpowers-marketplace/.claude-plugin/marketplace.json`) versions per **plugin**, not per-skill: `superpowers` (itself a monorepo of brainstorming/TDD/debugging/etc. — the same skills installed here via npx) ships as one unit, 5.1.0→6.3.0. Independently-paced work (`superpowers-chrome`, `episodic-memory`) was split into **separate repos**, each independently versioned — never versioned as siblings inside one repo.
- `skills.sh` has zero version handling (`grep version skills.sh` → no hits), 2 commits ever, and on this machine installs only 1 of the repo's 8 skills — while `npx skills` and Claude Code plugins each reliably manage 15-20+ skills/plugins.

## 2. Proposed approach

Both real precedents converge on the same rule: **version at repo/plugin granularity, never per-skill inside one monorepo** — that premise has no precedent anywhere I found. So: drop it. Add a root `.claude-plugin/marketplace.json` (schema: json.schemastore.org/claude-code-marketplace.json) structured like anthropics/skills, grouping the 8 skills into 2-3 themed plugins under one repo-level version. Retire `skills.sh`'s install/update logic, which reimplements — more weakly — what `npx skills` already does (hash-tracked, 76-agent support). The existing `skills/<name>/SKILL.md` layout already satisfies both channels with zero conversion needed.

## 3. Tradeoffs accepted

Losing `skills.sh --copy`'s symlink mode costs the live-edit dev loop (instant reflection of edits); `npx skills update` needs an explicit re-pull instead. Grouping into few plugins means coarser adoption units until a skill needs independent release cadence — precedent (superpowers-chrome, episodic-memory) says fork it into its own repo then, not version it separately in place.

**Budget consumed:** ~9k tokens, 6 tool calls.
