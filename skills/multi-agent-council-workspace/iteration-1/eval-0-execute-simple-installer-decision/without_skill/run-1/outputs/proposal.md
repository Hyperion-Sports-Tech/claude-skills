# Proposal — Installer and versioning strategy for `tomiduss/claude-skills`

| | |
|---|---|
| Decision requested | (Q1) Keep investing in the custom `skills.sh` installer, or move to the standard `npx skills` / agentskills.io flow and/or a Claude Code plugin marketplace? (Q2) Monorepo with one version, or per-skill versioning? |
| Tier | Simple, no modifiers; user unavailable at checkpoints — council ran to completion unattended |
| Council | 3 deliberators with constrained value functions, 1 round of position papers, chair synthesis. Papers: `round-1/maintainer-pragmatist.md`, `round-1/ecosystem-strategist.md`, `round-1/control-risk-advocate.md` |
| Date / environment | 2026-08-15; Claude Code 2.1.233; `skills` CLI 1.5.22; repo `github.com/tomiduss/claude-skills` (public, 0 stars, no README, 14 commits) |

---

## 1. Recommendation (TL;DR)

1. **Stop investing in `skills.sh` as an installer.** Its only irreplaceable job is the edit-in-place symlink `~/.claude/skills/<name> -> <repo>/skills/<name>` for the dev machine. Keep that as a ~20-line `link/unlink/list` helper (or a documented `ln -s`); delete the `--copy`/`update`/`.skill-source`/`setup`/`doctor` machinery. Nothing outside your machine will ever run `git clone && ./skills.sh install`.
2. **Adopt the standard flow for everything that leaves the dev machine — it already works, unchanged.** `npx skills add tomiduss/claude-skills` installed `brand-identity` from this exact layout on 2026-02-25 (recorded in `~/.agents/.skill-lock.json`), and `npx skills add <repo> --list` finds all 8 skills today. There is no migration; there is only hygiene and a README.
3. **Add a one-file Claude Code marketplace (`.claude-plugin/marketplace.json`) on top of the same layout — no restructuring.** Use the pattern Anthropic uses for `anthropics/skills` (`"source": "./"`, `"strict": false`, per-plugin `"skills": ["./skills/<name>"]`). A draft for this repo already passes `claude plugin validate --strict` (Appendix A). This is what "a marketplace where skills can be discovered, versioned and installed into any project" (CLAUDE.md) costs now: one JSON file, reversible by deleting it.
4. **Q2: keep the monorepo; make the *unit* of versioning the skill (one plugin entry per skill or tight pair), but do not hand-maintain version numbers yet.** Both channels already give per-skill update granularity for free: `npx skills update` reinstalls only skills whose folder hash changed; Claude Code (with `version` omitted) versions each plugin by the resolved commit SHA. Switch a plugin entry to an explicit semver `version` + `claude plugin tag` only when a consumer needs pinning/stability — that switch is one line and pre-decided below (single source of truth: the marketplace entry, never both `plugin.json` and `marketplace.json`).
5. **Do the hygiene first, because both channels already "see" the public repo:** untrack the vendored `.claude/skills/playwright-cli` (it is discovered as a 9th "skill" of your repo), keep workspace/eval dirs out of the scanned `skills/` tree, mark the ZON-specific `linear-*` skills `metadata.internal: true`, and move ~5.6 MB of research transcripts out of git.

Total effort: roughly 2–3 hours, every step reversible.

---

## 2. What the council established (evidence)

All facts below were verified during the run, on this machine or against current docs.

| # | Fact | Why it matters |
|---|------|----------------|
| E1 | `~/.agents/.skill-lock.json` (v3) contains `brand-identity` with `source: tomiduss/claude-skills`, `skillPath: skills/brand-identity/SKILL.md`, `skillFolderHash`, installed 2026-02-25. | The standard `npx skills` flow already works on the current layout. "Migrate" is the wrong verb. |
| E2 | `npx skills add /Users/tomasdussaillant/repos/skills --list` -> "Found 9 skills": the 8 real ones **plus `playwright-cli`** from `.claude/skills/playwright-cli/SKILL.md` (tracked in git; vendored third-party). | A discovery leak: a stale third-party skill ships under your name. Fix before advertising the repo. |
| E3 | `skills/multi-agent-council-workspace/skill-snapshot/SKILL.md` has `name: multi-agent-council` (duplicate). Untracked (0 files in `git ls-files`) but **not gitignored**. The CLI walks container dirs 3 levels deep. | One `git add -A` publishes a duplicate-named skill. Move/ignore workspaces. |
| E4 | `npx skills` "symlink" mode = agent dirs (`~/.claude/skills`, `~/.codex/skills`, `~/.cursor/skills`) -> canonical **copy** in `~/.agents/skills/<name>` (see `find-skills` on this machine). Claude Code copies marketplace plugins into `~/.claude/plugins/cache/`; symlinks pointing outside the marketplace are skipped. | Neither external channel gives edit-in-place. Only a symlink into the working tree does — that is the one job `skills.sh` must keep. |
| E5 | `~/.claude/skills/multi-agent-council` is an absolute symlink into the repo and the skill loads in this very session; docs: personal skills in `~/.claude/skills/` take precedence over same-named plugin skills. | The dev symlink and an installed plugin can coexist without conflict. |
| E6 | `~/.claude/plugins/marketplaces/anthropic-agent-skills/.claude-plugin/marketplace.json` (on disk): a `skills/<name>/` monorepo exposed as plugins via `"source": "./"`, `"strict": false`, `"skills": [...]`. Docs: "When several plugin entries share one `skills/` folder at the marketplace root (`source: "./"`), list specific subdirectories instead so each entry loads only its own skills." | A skills monorepo becomes a Claude Code marketplace with one file and zero restructuring. |
| E7 | `claude plugin validate` passes on `skills/` and on the repo root; a draft `marketplace.json` for this repo (Appendix A) passes `claude plugin validate --strict`. | The path is validated, not hypothetical. |
| E8 | Claude Code version resolution: `plugin.json` `version` -> marketplace entry `version` -> source commit SHA -> archive digest -> `unknown`. Docs warn: a set `version` **pins** — "push new commits without changing that string, existing users … keep the cached copy"; and "Avoid setting `version` in both `plugin.json` and the marketplace entry" (plugin.json silently wins). Omitting `version` is "the simplest setup for internal or actively developed plugins." | Explicit versions have a real starvation failure mode; implicit ones are safe by default. |
| E9 | `claude plugin tag` creates `{name}--v{version}` git tags per plugin and validates plugin.json/marketplace agreement; `git-subdir` source type exists specifically for monorepos. | Per-plugin releases inside one repo are a first-class, tool-supported pattern. |
| E10 | `npx skills update` compares per-skill `skillFolderHash` via the GitHub Trees API and reinstalls only changed skills; always fetches the default branch; no pin/rollback. skills.sh lists repos automatically via anonymous install telemetry, ranked by installs, no submission gate. `metadata.internal: true` hides a skill ("only visible and installable when `INSTALL_INTERNAL_SKILLS=1`"). | Per-skill granularity is free in the npx channel; discoverability is earned by installs, not by listing; there is a switch for team-only skills. |
| E11 | agentskills.io spec: required `name`, `description`; optional `license`, `compatibility`, `metadata` (string map, e.g. `version`, `author`), `allowed-tools`. Versioning/installation are out of the spec's scope. | Any version number you put in `SKILL.md` is informational only — no tool acts on it. |
| E12 | Repo data: `skills.sh` = 470 lines, touched in 2 of 14 commits; only `multi-agent-council` is actively developed (8 commits, last today); every other skill has 1 commit (qa-testing 3). No README, no tags, no versions anywhere. `docs/` = 5.6 MB of tracked research transcripts. `hooks/install-hooks.sh` mutates `~/.claude/settings.json` with `jq` to support `linear-workflow`. | Maintenance burden of the script is small; the coordination problem semver solves does not exist yet; a second bespoke installer (hooks) exists that the plugin format can absorb. |
| E13 | Claude Code 2.1.x adds plugin features gated per minor (`displayName` 2.1.143, `relevance` 2.1.152, `renames` 2.1.193, `archive` 2.1.224, `command` 2.1.229). | Use only the boring, stable subset of the schema (`name`, `source`, `skills`, `strict`, `description`, `version`). |

---

## 3. Options, reframed as jobs

The question "custom vs standard vs marketplace" hides four different jobs. Each channel is good at some and useless at others:

| Job | `skills.sh` (custom) | `npx skills` / agentskills.io | Claude Code marketplace |
|---|---|---|---|
| A. Edit-in-place dev loop on the maintainer's machine | **Yes** (symlink into working tree) — its only unique value | No (canonical copy) | No (cache copy); `--plugin-dir` is session-only |
| B. Install on other machines / other projects (yours or anyone's) | Requires a clone + PATH setup; single agent | **Yes, today, one command**, 40+ agents, project or global, symlink or copy, lockfile + `update` | Yes: `/plugin install x@tomiduss-skills`, `--scope project`, auto-update, `/plugin` UI |
| C. Discoverability | None | Automatic listing on skills.sh via install telemetry; `npx skills find` | Only for people who add your marketplace by name (no central directory); can bundle hooks/agents/MCP |
| D. Versioning / updates | Homemade `.skill-source` marker; no hash, no pin | Per-skill folder hash; latest-only | Per-plugin `version` or commit SHA; pinning; `claude plugin tag`; release channels via refs |

Conclusion the three deliberators reached independently: keep the custom script only for job A; hand jobs B–D to the two standard channels, which are additive files on the same layout rather than alternatives.

---

## 4. Decision Q1 — installer

**Decision:** Retire `skills.sh` as a product; keep a dev-symlink helper; make `npx skills add tomiduss/claude-skills` the documented install path; add `.claude-plugin/marketplace.json` for the Claude Code channel.

Reasoning:
- The maintenance argument cuts less than expected — the script is low-churn (E12) — but the *duplication* argument cuts hard: `--copy`, `.skill-source`, `update`, `setup`, `doctor` re-implement, single-agent and without hashes, what the `skills` CLI lockfile already does (E1, E10). Two install semantics for one repo is a cost with no consumer.
- The dev loop is not negotiable and no external channel provides it (E4). It is one `ln -s` per skill; keep exactly that.
- The marketplace file is worth adding now rather than "later" because (i) it *is* the CLAUDE.md vision, delivered by the ecosystem for free; (ii) it validated cleanly (E7); (iii) it buys things npx cannot: `/plugin` UI, project-scope installs shared through `.claude/settings.json`, auto-update, and bundling the Linear hooks so `hooks/install-hooks.sh` (a second bespoke installer, E12) can eventually go away; (iv) it is a single file — delete it and nothing else depends on it.
- What you give up: control over conventions you were not exercising (no versions, no tags exist today), and acceptance of two third-party roadmaps. The fallback if either ecosystem moves under you is `cp -R`/`ln -s` of a plain `skills/<name>/` folder — the layout you already have. Owning 470 lines of bash does not hedge that risk; the standard layout does.

Grouping and naming for the marketplace (chair's call after the strategist/pragmatist split): one plugin entry per skill (per-skill versioning was your stated requirement), pairs only where skills are always used together (`agent-teams` = `writing-plans-for-teams` + `agent-team-driven-development`). Plugin name = skill name so the name is identical across `npx skills --skill <name>` and `/plugin install <name>@tomiduss-skills`; the resulting invocation form `/<name>:<name>` is cosmetic (your dev symlink keeps the short `/multi-agent-council`). If the doubling bothers you, use short aliases (`council`) — not decision-critical.

Keep the ZON-specific `linear-workflow` / `linear-agent-workflow` out of the first marketplace and mark them internal for npx (E10). Optional later: a `linear` plugin entry that bundles `hooks/` via the entry's `hooks` field, replacing `install-hooks.sh` — a marketplace is opt-in by name, so this is not "public discovery".

---

## 5. Decision Q2 — versioning

**Decision:** Monorepo stays. Version *unit* = skill (plugin entry). Version *numbers* = implicit by default (folder hash / commit SHA); explicit semver per plugin only on a trigger, with the mechanism fixed now so the switch is one line.

Reasoning:
- "Any marketplace will want per-skill versions" is true about *units*, not about *numbers*: Claude Code marketplaces need per-plugin entries (which you get from the `skills:` lists) and accept SHA-derived versions; skills.sh has no versions at all (E8, E10). Nothing in either channel is unlocked by hand-maintained numbers today.
- The most likely way a solo maintainer harms users is forgetting to bump a pinned `version` (E8). With no external consumers and one actively changing skill (E12), the starvation risk outweighs the benefit of pretty numbers.
- Splitting into per-skill repos (the `obra/superpowers-marketplace` pattern) is overkill for 8 skills and one maintainer; `git-subdir` sources and `claude plugin tag` exist so that monorepos never need to split (E9).

Pre-decided mechanism for when a trigger fires (an external user asks "which version am I on?", a plugin becomes a dependency of another, or you want a stable/latest split):
1. Put `"version": "x.y.z"` **only** in that plugin's `marketplace.json` entry (never also in a `plugin.json`, E8).
2. Release with `claude plugin tag --push` -> `<name>--vx.y.z`; CI runs `claude plugin validate --strict .`.
3. Optionally mirror the number into that skill's `SKILL.md` `metadata.version` for spec-level portability (E11) — informational only, so drift there cannot starve updates.

Trade-off accepted: with SHA-derived versions and `source: "./"`, every commit re-versions every plugin and each plugin copy is the whole repo, so auto-updating installs re-copy on unrelated commits. Harmless at 8 skills; keeps everyone fresh; and it is why the docs/transcripts should leave the git tree (Phase 0). Revisit if the repo grows to dozens of plugins or commit frequency makes the churn annoying — that is a second trigger for explicit versions.

---

## 6. Where the deliberators disagreed, and how it was resolved

| Topic | Pragmatist | Strategist | Control/Risk | Resolution (chair) |
|---|---|---|---|---|
| Add version numbers now? | No — SHA/hash until someone asks | Yes — `metadata.version` in SKILL.md as source of truth, mirrored to marketplace, CI check | Yes — `metadata.version` maintainer-owned; mirror only if marketplace opened; CI + `tag --dry-run` | **Not now.** Starvation risk (E8) and no consumers (E12) beat portability. Mechanism pre-decided (Section 5) so adopting later is one line. Dissent recorded: two of three preferred numbers now. |
| Marketplace file now? | Optional (20 min, reversible) | Yes | Only if you actually want it, with guardrails | **Yes, after hygiene** — it is the CLAUDE.md goal, validated, one file, and absorbs the hooks installer later. |
| Publish from a `release` branch? | — | — | Yes — folder-hash updates have no pin/rollback | **Not now.** One-person repo; blast radius of a bad HEAD is a revert-and-push of prompt files. Keep WIP on branches/PRs (already your pattern, PR #1). Trigger: external users depending on stability. |
| ZON-specific skills | Document in README | `metadata.internal: true`, omit from marketplace | internal or private repo | **`metadata.internal: true` on both `linear-*` skills; omit from first marketplace.** Repo is public regardless, so this is curation, not secrecy; `designing-points-economy` stays visible (plausibly useful to others). |
| Plugin grouping | 2–3 bundles (avoid `x:x` naming) | Per skill / tight pair, short names | — | **Per skill, pairs where always co-used; plugin name = skill name** (cross-channel consistency > cosmetics). |

Everything else — retire the installer, keep the symlink, npx already works, fix the three leaks, keep the monorepo — was unanimous.

---

## 7. Implementation plan

Everything below is reversible (old files stay in git history; the marketplace is one file). Do Phase 0 before publicising anything.

**Phase 0 — hygiene (≈40 min)**
1. `git rm -r --cached .claude/skills/playwright-cli` and add `.claude/skills/` to `.gitignore` (reinstall locally with `npx skills add … -a claude-code -g` if you use it). Fixes E2.
2. Move `skills/multi-agent-council-workspace/` out of `skills/` (e.g. `workspace/`, gitignored) or add `skills/*-workspace/` to `.gitignore`. Nothing that is not a skill should live under the scanned dir. Fixes E3.
3. Move `docs/superpowers/plans/*-research/**/*.jsonl` (5.6 MB) out of git or into an ignored path (E12). Optional but cheap.
4. Add `metadata:\n  internal: true` to `linear-workflow` and `linear-agent-workflow` frontmatter (E10). On other machines: `INSTALL_INTERNAL_SKILLS=1 npx skills add tomiduss/claude-skills --skill linear-workflow`.

**Phase 1 — adopt the standard flow (≈20 min)**
5. Write `README.md`: what each skill is; `npx skills add tomiduss/claude-skills` (+ `--skill <name>`, `-g`, `--copy`); the dev-loop line; note that npx has no pinning (always latest). Today the discoverable channels have nothing to point at.
6. Update `CLAUDE.md`: layout is `skills/<name>/SKILL.md`; the "marketplace" is `.claude-plugin/marketplace.json` + skills.sh listing; `skills.sh`/`link.sh` is dev-only.

**Phase 2 — Claude Code marketplace (≈45 min)**
7. Add `.claude-plugin/marketplace.json` from Appendix A (no `version` fields). `claude plugin validate --strict .`
8. Test without touching your dev setup: `claude --plugin-dir ./` for a session, or on a second machine `claude plugin marketplace add tomiduss/claude-skills` then `claude plugin install qa-testing@tomiduss-skills`. Rule: dev machine = symlinks only; other machines = plugin or npx only (avoids duplicate `x` and `x:x` entries, E5).
9. Add the `/plugin marketplace add` + `/plugin install` lines to the README.

**Phase 3 — shrink the custom script (≈30 min)**
10. Replace `skills.sh` with `link.sh` (or `make link`): `link [name]`, `unlink [name]`, `list`, idempotent, absolute symlinks into `~/.claude/skills`. Delete `--copy`, `update`, `.skill-source`, `setup`, `doctor`, `--project`, `--both`. Update `.claude/settings.local.json` allow-rules that reference `skills.sh` if you keep using them.
11. Optional CI (GitHub Actions, 15 min): `claude plugin validate --strict .` and `npx skills add . --list` on PRs, so a bad manifest or a stray SKILL.md never reaches the default branch.

**Later, on triggers only**
12. Explicit `version` + `claude plugin tag` for a plugin someone depends on (Section 5).
13. `linear` plugin entry bundling `hooks/` (retire `hooks/install-hooks.sh`) if you want one-command setup on other machines.
14. `release` branch or pinned `ref` marketplace only if external users need stability.

---

## 8. Guardrails and failure modes to keep in view

| Failure mode | Trigger | Mitigation in this proposal |
|---|---|---|
| Third-party skill shipped under your name | Anyone runs `npx skills add tomiduss/claude-skills` | Phase 0.1 |
| Duplicate-named skill published | `git add -A` on the workspace dir | Phase 0.2 |
| Users starved of updates | Set `version` once, forget to bump | Do not set `version` until triggered; when set, single location + `tag`/`validate --strict` in CI |
| Edit-in-place silently stops | Delete the dev symlink after installing your own plugin | Keep the symlink; dev machine never installs its own plugins |
| Duplicate/ambiguous skill entries | Symlink and plugin both present on one machine | Same rule as above; personal skill wins if it happens (E5) |
| Schema churn breaks the marketplace | Using per-minor gated fields (E13) | Use only `name`, `source`, `strict`, `skills`, `description`, (`version`) |
| Bad HEAD goes live to npx installers | Push WIP to `master` | Keep WIP on branches/PRs; escalate to a release branch only on external demand |
| Cache churn from SHA versions | Frequent commits with `source: "./"` | Keep the repo small (Phase 0.3); switch to explicit versions if it becomes annoying |

---

## 9. Triggers to revisit this decision

- An external user, or a second machine you actually pin, asks "which version am I on?" -> explicit `version` for that plugin.
- A skill becomes a dependency of another plugin -> explicit `version` + `claude plugin tag`.
- The repo passes ~20 plugins or commits become daily -> explicit versions to stop cache churn; consider `metadata.pluginRoot`.
- Either ecosystem changes its discovery/layout conventions -> the fallback is still `skills/<name>/` + `ln -s`; re-evaluate then, not pre-emptively.
- You want the Linear hooks on other machines -> `linear` plugin with bundled hooks (Phase "later" item 13).

---

## Appendix A — validated `.claude-plugin/marketplace.json` for this repo

Passed `claude plugin validate --strict` on 2026-08-15 (Claude Code 2.1.233) against a scratch copy of the current `skills/` tree. Intentionally no `version` fields (Section 5). Reserved names (`agent-skills`, `anthropic-*`, `claude-plugins-*`, …) are avoided.

```json
{
  "name": "tomiduss-skills",
  "owner": { "name": "Tomás Dussaillant", "url": "https://github.com/tomiduss" },
  "description": "Personal Claude Code agent skills: multi-agent council, QA teams, brand identity, agent-team planning",
  "plugins": [
    {
      "name": "multi-agent-council",
      "description": "Structured multi-agent deliberation for complex, multi-tradeoff decisions",
      "source": "./",
      "strict": false,
      "skills": ["./skills/multi-agent-council"]
    },
    {
      "name": "qa-testing",
      "description": "Parallel multi-agent QA team for running web apps",
      "source": "./",
      "strict": false,
      "skills": ["./skills/qa-testing"]
    },
    {
      "name": "brand-identity",
      "description": "Brand identity systems: strategy, visual research, design tokens",
      "source": "./",
      "strict": false,
      "skills": ["./skills/brand-identity"]
    },
    {
      "name": "agent-teams",
      "description": "Team-oriented planning and execution: writing-plans-for-teams + agent-team-driven-development",
      "source": "./",
      "strict": false,
      "skills": ["./skills/writing-plans-for-teams", "./skills/agent-team-driven-development"]
    },
    {
      "name": "designing-points-economy",
      "description": "Design and validate challenges and points economies for fan-engagement campaigns",
      "source": "./",
      "strict": false,
      "skills": ["./skills/designing-points-economy"]
    }
  ]
}
```

Usage once pushed: `/plugin marketplace add tomiduss/claude-skills` then `/plugin install qa-testing@tomiduss-skills` (or `claude plugin install qa-testing@tomiduss-skills --scope project`).

## Appendix B — `skills.sh` job map

| `skills.sh` today | Replacement |
|---|---|
| `install [name]` (symlink, user scope) | keep as `link.sh link [name]` (`ln -s "$REPO/skills/$name" ~/.claude/skills/$name`) |
| `install --copy`, `update`, `.skill-source` marker | `npx skills add tomiduss/claude-skills [--skill x] [-g] [--copy]`; `npx skills update` |
| `install --project` / `--both` | `npx skills add …` in the project (default scope) or `claude plugin install x@tomiduss-skills --scope project` |
| `list` | `link.sh list`; `npx skills list [-g]`; `claude plugin list` |
| `uninstall` | `link.sh unlink`; `npx skills remove`; `claude plugin uninstall` |
| `setup`, `doctor` (PATH launcher) | delete |
| `hooks/install-hooks.sh` (jq into settings.json) | later: `hooks` field on a `linear` plugin entry |

## Appendix C — sources consulted

- Claude Code docs: *Create and distribute a plugin marketplace* (schema, sources, `strict`, `skills` lists, version resolution and release channels), *Plugins reference* (version-management order, skills-dir plugins, caching/symlink rules, `--plugin-dir`, namespacing), *Plugin dependencies* (`{name}--v{version}` tags) — code.claude.com, fetched 2026-08-15.
- `claude plugin --help`, `claude plugin tag|init|validate|install|marketplace --help` (2.1.233).
- vercel-labs/skills README and AGENTS.md (commands, discovery paths, symlink/copy modes, `metadata.internal`, lockfile/`skillFolderHash` update logic) via Context7; skills.sh FAQ (telemetry-based listing).
- agentskills.io specification (frontmatter fields, `metadata` map).
- Local evidence: `~/.agents/.skill-lock.json`, `~/.claude/skills/*` symlinks, `~/.claude/plugins/marketplaces/anthropic-agent-skills/.claude-plugin/marketplace.json`, `~/.claude/plugins/installed_plugins.json`, repo git history and file tree, `npx skills add <repo> --list`, `claude plugin validate`.
