# Round 1 — ecosystem-strategist

## Value function (2–3 lines)

Maximize reach, discoverability and interoperability of these skills — across Claude Code, Codex, Cursor and the other agents that read `SKILL.md` — and their longevity beyond any single tool. Be where users already look (`npx skills find` / the skills.sh leaderboard, and Claude Code's `/plugin` marketplaces), stay aligned with the open agentskills.io spec, and treat the CLAUDE.md "marketplace" vision as a real goal that the ecosystem now fulfils for free.

## Position on Q1: custom skills.sh vs `npx skills`/agentskills.io vs Claude Code plugin marketplace

**Do both standard channels; retire `skills.sh` as a distribution mechanism and keep only its one irreplaceable job (a dev symlink).** The two channels are not alternatives — they are additive files on the *same* repo layout, and each buys something the other cannot:

- **`npx skills` / agentskills.io / skills.sh** buys *cross-agent reach and zero-gate discoverability*. One command (`npx skills add tomiduss/claude-skills`) installs into Claude Code, Codex, Cursor and 40+ agents; every install auto-lists the repo on skills.sh via anonymous telemetry — no submission, no review. **This channel already works today with zero changes**: your own `~/.agents/.skill-lock.json` records `brand-identity` installed from `tomiduss/claude-skills` at `skills/brand-identity/SKILL.md`, and `npx skills add <repo> --list` found the skills. There is nothing to migrate; only hygiene.
- **A Claude Code plugin marketplace** buys *in-product install/update UX, project-scope installs, auto-update, and the ability to bundle hooks* (your `hooks/install-hooks.sh`, which mutates `~/.claude/settings.json` with `jq`, becomes a plugin `hooks/hooks.json` instead of a bespoke installer). It costs one file, `.claude-plugin/marketplace.json`, and needs **no restructuring**: the exact pattern is on your disk at `~/.claude/plugins/marketplaces/anthropic-agent-skills/.claude-plugin/marketplace.json` — a `skills/<name>/` monorepo where each plugin entry has `"source": "./"`, `"strict": false` and an explicit `"skills": ["./skills/<name>", ...]` list, and the docs bless it ("when several plugin entries share one `skills/` folder at the marketplace root, list specific subdirectories").
- **`skills.sh` (the custom script)** buys neither. Nobody outside you will `git clone && ./skills.sh install`. Its `--copy` + `.skill-source` marker + `update` reimplements — worse (no hash, single agent, no discovery) — what the `npx skills` lockfile already does. Its only unique value, the edit-in-place symlink `~/.claude/skills/<name> → repo/skills/<name>`, is one `ln -s`, and Claude Code guarantees personal skills in `~/.claude/skills/` take precedence over same-named plugin skills, so the dev symlink and an installed plugin coexist.

Concrete `marketplace.json` for this repo (name `tomiduss-skills`; note `agent-skills`/`anthropic-*` names are reserved):

```json
{
  "name": "tomiduss-skills",
  "owner": { "name": "Tomás Dussaillant", "url": "https://github.com/tomiduss" },
  "plugins": [
    { "name": "council",        "source": "./", "strict": false, "version": "1.0.0",
      "description": "Multi-agent council deliberation for high-stakes decisions",
      "keywords": ["council","deliberation","architecture"], "skills": ["./skills/multi-agent-council"] },
    { "name": "agent-teams",    "source": "./", "strict": false, "version": "1.0.0",
      "description": "Plan and execute implementation plans with agent teams",
      "skills": ["./skills/writing-plans-for-teams", "./skills/agent-team-driven-development"] },
    { "name": "qa-testing",     "source": "./", "strict": false, "version": "1.0.0", "skills": ["./skills/qa-testing"] },
    { "name": "brand-identity", "source": "./", "strict": false, "version": "1.0.0", "skills": ["./skills/brand-identity"] }
  ]
}
```

Grouping: one plugin per skill (or per tight pair users always install together) so the `/plugin` UI lists each with its own description/keywords and each updates independently. Short plugin names avoid the `multi-agent-council:multi-agent-council` invocation wart (skills load as `plugin:skill`, e.g. `/council:multi-agent-council`). The ZON-specific skills (`linear-workflow`, `linear-agent-workflow`, `designing-points-economy`) stay out of the public catalog: `metadata.internal: true` hides them from `npx skills` discovery, and they simply aren't listed in `marketplace.json`.

## Position on Q2: monorepo single version vs per-skill versioning

**Keep the monorepo; version per skill.** Marketplaces want per-*plugin* versions, not per-*repo* repos — `anthropics/skills`, `vercel-labs/skills` and `obra/superpowers` are all monorepos. Mechanism per channel:

- **`npx skills`**: nothing to do. Its lockfile stores a per-skill `skillFolderHash` and `skills update` reinstalls only the skills whose folder tree changed. Per-skill update granularity is free.
- **Claude Code marketplace**: a `version` per plugin entry in `marketplace.json`, bumped on release (Claude Code's resolution order is `plugin.json` → marketplace entry → commit SHA; a set `version` pins, so it *must* be bumped, and the docs warn not to set it in both places). Optionally tag releases `<plugin>--v<version>` (`claude plugin tag`) — only needed if anything ever depends on these plugins.
- **Portable, spec-level**: `metadata: { version: "1.0", author: tomiduss }` in each `SKILL.md` frontmatter — the agentskills.io way; it travels with the skill into any agent. Make it the single source of truth and mirror it into `marketplace.json` with a 5-line check in CI (`claude plugin validate --strict .`).

## Evidence

- `~/.agents/.skill-lock.json` (v3): `brand-identity` ← `tomiduss/claude-skills`, `skillPath: skills/brand-identity/SKILL.md`, `skillFolderHash` → the standard flow already works with the current layout; per-skill hashes = per-skill updates.
- `~/.claude/skills/find-skills`, `~/.codex/skills/find-skills`, `~/.cursor/skills/find-skills` all → `../../.agents/skills/find-skills`: the cross-agent fan-out `npx skills` gives and `skills.sh` cannot.
- `npx skills add /repo --list` found **9** skills, including `playwright-cli` from `.claude/skills/` (the CLI scans `.claude/skills/`): a leak to fix. `skills/multi-agent-council-workspace/` is untracked and its snapshot is named `multi-agent-council`, so it is shadowed — fine remotely, fragile locally.
- `anthropic-agent-skills` marketplace on disk: `source: "./"`, `strict: false`, `skills: [...]` lists — a skills monorepo doubling as a marketplace; `claude plugin validate` passes on `skills/` and the repo root; `claude plugin tag` exists (`{name}--v{version}`).
- skills.sh FAQ: "Skills appear on the leaderboard automatically through anonymous telemetry when users run `npx skills add <owner/repo>`"; ranking by installs; no submission process.
- Repo is public, 0 stars, 0 forks, **no README** → today the discoverable channels have nothing to point at.
- `skills.sh` is 470 lines, touched in 2 of 14 commits: cheap to keep, but everything except `ln -s` duplicates ecosystem tooling.
- `docs/` holds 5.6 MB of checked-in research transcripts; with `source: "./"` every plugin copies the whole repo into `~/.claude/plugins/cache` — hygiene, not a blocker.

## Steelman of the opposing view and why it still loses

"Nobody is asking for these skills; the script works; the plugin schema is churning (`displayName` v2.1.143, `relevance` v2.1.152, `renames` v2.1.193, `archive` v2.1.224, `command` v2.1.229) and the Vercel CLI is at 1.5.x — you'd chase two moving targets for zero demand." Under my value function it loses: (1) both channels are *additive files* on the existing layout, and the fields I use (`name`, `source`, `skills`, `strict`, `version`) are the stable core that `anthropics/skills` itself uses; (2) discoverability compounds and is permanent once installs start, while a private installer compounds nothing; (3) the CLAUDE.md goal *is* a marketplace, and the shortest path to one is publishing into two that already have users — for ~2–3 hours total.

## Concrete plan

1. **Hygiene (30 min, reversible):** add `README.md` with both one-liners (`npx skills add tomiduss/claude-skills`; `/plugin marketplace add tomiduss/claude-skills` → `/plugin install council@tomiduss-skills`); untrack `.claude/skills/playwright-cli`; move `docs/.../research/*.jsonl` out of git; add `metadata.internal: true` to the ZON-specific skills.
2. **Marketplace (45 min, reversible — one file):** create `.claude-plugin/marketplace.json` as above; `claude plugin validate .`; test with `/plugin marketplace add ./` and `claude plugin install council@tomiduss-skills`.
3. **Spec metadata (15 min):** add `metadata: {version, author}` (and `compatibility: Designed for Claude Code` where true) to each `SKILL.md`.
4. **Shrink `skills.sh` → `dev-link.sh` (20 min, reversible):** keep symlink install/uninstall/list for `~/.claude/skills`; delete `--copy`, `update`, `setup`, `doctor` (the lockfile/plugin cache own those jobs). Use `claude --plugin-dir` to test the plugin form.
5. **Hooks as a plugin (30 min, when/if `linear-workflow` is shared):** `hooks/hooks.json` in a `linear-workflow` plugin replaces `install-hooks.sh`.
6. **Release discipline (10 min/release):** bump `metadata.version` + marketplace `version`; optional `git tag <plugin>--v<version>`; CI runs `claude plugin validate --strict .` and `npx skills add . --list`.
7. **Distribution (ongoing, minutes):** put the `npx skills add` line in each skill's docs; each install lists the repo on skills.sh; submit to community plugin lists.

## Risks / open questions I concede

- Two manifests to keep in sync (frontmatter `metadata.version` + `marketplace.json` `version`); a forgotten bump silently withholds updates from marketplace users. Mitigate with the CI check, or start with commit-SHA versioning (omit `version`) and add numbers when there is an audience.
- Cold start: skills.sh ranks by installs; a 0-star repo with no README gets nothing until it is shared. Only the general skills (council, qa-testing, brand-identity, agent-teams) are worth exposing.
- Namespacing: marketplace users invoke `/council:multi-agent-council`, not `/multi-agent-council` (your dev symlink keeps the short name).
- Both ecosystems are young; `npx skills` offers users no pinning (always latest folder hash) — acceptable for a personal repo, worth stating in the README.

## One-line verdict

Publish the same monorepo through both `npx skills` (already working) and a one-file Claude Code marketplace, version per skill, and demote `skills.sh` to a ten-line dev-symlink helper.
