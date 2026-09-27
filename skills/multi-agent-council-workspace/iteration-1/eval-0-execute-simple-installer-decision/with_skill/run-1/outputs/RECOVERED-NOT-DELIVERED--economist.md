<!-- Recovered by the eval harness from the deliberator's transcript. The council lead NEVER received this paper (delivery deadlock) — see grading notes. -->

# Economist — Round 1 Position Paper

## Key findings

**skills.sh's cost-to-use ratio is bad.** 470 lines, touched in only 2 of 14 repo commits: `7efa0da` (+157, Feb 25) and `7cdef8e` (+365/-52, May 16) — two big-bang rewrites ~3 months apart, not steady upkeep. Payoff: only 1 of 8 repo skills (`multi-agent-council`) is actually deployed via it at user scope; its symlink (`ls -la ~/.claude/skills`) is dated Mar 19 and untouched since — ~5 months of zero `update` runs. A separate 99-line `hooks/install-hooks.sh` is a second bespoke installer in the same repo (569 total bespoke lines, one maintainer).

**Migration to `npx skills` costs ~$0 — it's already done.** `~/.agents/.skill-lock.json:brand-identity` shows `"source": "tomiduss/claude-skills"` already resolving `skills/brand-identity/SKILL.md` with zero repo changes, because this repo's existing layout already satisfies the convention. Versioning is by content hash (`skillFolderHash`), not a manifest field — per-skill versioning is *free and automatic* here, not a cost to design.

**Plugin marketplace is cheaper than framed, but unproven demand.** No `.claude-plugin/marketplace.json` exists yet (`find` confirmed). Real comparables on this machine: `anthropic-agent-skills/marketplace.json` = 55 lines covering 3 plugins / 17 skills, **with no per-plugin version field** — only one `metadata.version` for the whole marketplace; `superpowers-marketplace` = 114 lines (upper bound). Docs (code.claude.com/docs/en/plugin-marketplaces) confirm updates ship by "pushing changes to your repository," no forced version bump. For 8 skills grouped as 1-2 plugins: ~30-70 lines, ~1-2 dev-hours one-time, near-$0 marginal cost per release.

## Proposed approach

Adopt (b) now at ~0.5 dev-hours (document it, stop treating skills.sh as canonical). **Freeze** skills.sh — no more rewrites — reversal costs nothing since it's local symlinks. Build (c) opportunistically (~1-2h) since real evidence shows it's cheap, but don't prioritize it: zero external subscribers today means zero EV until demand exists. **Reject per-skill semver**: neither real distribution mechanism observed here (content-hash lock file, marketplace.json with single top-level version) requires it — it's a self-imposed cost with no buyer. Stay monorepo.

## Tradeoffs accepted

Freezing skills.sh forfeits its custom symlink-vs-copy control. Deferring (c) leaves CLAUDE.md's stated marketplace vision unmet a while longer (cheap to revisit — no penalty for waiting). No per-skill versioning means no independent rollback if a future external consumer demands pinning.

**Budget consumed:** ~9.5k tokens, 5 tool calls.
