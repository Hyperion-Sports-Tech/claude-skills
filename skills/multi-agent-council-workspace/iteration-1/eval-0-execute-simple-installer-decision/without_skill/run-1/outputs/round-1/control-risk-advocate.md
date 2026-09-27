# Round 1 — control-risk-advocate

## Value function

Preserve maintainer control, reproducibility, privacy and reversibility. Own the version semantics; depend on third-party roadmaps only where the dependency is cheap to unwind. Protect the edit-in-place dev loop. Every "leak" and every "can't roll back" is a real cost, not a hypothetical.

## Position on Q1: custom skills.sh vs `npx skills`/agentskills.io vs Claude Code plugin marketplace

**Recommendation: split skills.sh's jobs into "irreplaceable" and "commodity", keep only the irreplaceable part, and gate every external channel behind guardrails that don't exist today.**

Of the six commands in `skills.sh` (`install`, `uninstall`, `update`, `list`, `setup`, `doctor`), exactly one job is irreplaceable: **the symlink from `~/.claude/skills/<name>` into the working tree** (`readlink ~/.claude/skills/multi-agent-council` → `/Users/tomasdussaillant/repos/skills/skills/multi-agent-council`). That is the only mechanism in which the file you edit *is* the file Claude loads. Neither external channel gives you that:

- Claude Code copies marketplace plugins into `~/.claude/plugins/cache/` and "symlinks outside the marketplace are skipped for security" — edit-in-place is gone unless the symlink stays.
- `npx skills add` symlinks agent dirs to a **canonical copy** in `~/.agents/skills/<name>` (see `.skill-lock.json` v3), not to your repo; you edit the repo, nothing changes until `npx skills update` re-clones.

Everything else in skills.sh (`--copy` mode, `.skill-source` markers, `update` for copies, `setup`/`doctor` PATH plumbing) is commodity that both channels do better, and it costs 470 lines of Bash 3.2-compatible shell to keep alive. Churn is low (2 of 14 commits touched it), so the *maintenance* cost is not my objection — the objection is that the copy/update paths duplicate what the ecosystem does and add a third, un-audited install semantics you have to reason about.

**Guardrails required before exposing the repo to *either* channel** (both already effectively "see" it: the repo is PUBLIC and `npx skills add tomiduss/claude-skills` was already run once for `brand-identity` on 2026-02-25):

1. `.claude/skills/playwright-cli/` (a vendored third-party skill) **is tracked in git** and is discovered by `npx skills add … --list` as a 9th installable "skill" of *your* repo. Move it out or ignore it.
2. `skills/multi-agent-council-workspace/skill-snapshot/SKILL.md` carries `name: multi-agent-council` — a duplicate name. It is untracked today but **not gitignored**; one `git add -A` publishes a second skill with the same name at depth 2, which the CLI walks ("up to three levels deep").
3. `linear-workflow` is hard-wired to the Zona Cóndores team (`ZON-*`), and `designing-points-economy` is domain-specific. In a public repo indexed by skills.sh telemetry, they show up in a directory with no unlisting flow. Mark them `metadata.internal: true` (honoured by the CLI) or move them.

## Position on Q2: monorepo single version vs per-skill versioning

**Recommendation: keep the monorepo, adopt per-skill versions you control — `metadata.version` in each SKILL.md frontmatter (agentskills.io-compliant, tool-agnostic) — and only mirror it into a marketplace `version` field if you actually open a Claude Code marketplace.** Do NOT depend on any tool's implicit version:

- The `npx skills` "version" is a `skillFolderHash` of the default branch. It gives per-skill *update detection* for free, but **no pin and no rollback**: `skills update` always re-fetches HEAD; a bad commit is instantly live for every installer.
- Claude Code's fallback is the commit SHA of the whole marketplace repo (`installed_plugins.json` shows `"version": "unknown"` / `gitCommitSha` entries in the wild). In a monorepo, every commit to any skill re-versions every plugin. Harmless but noisy, and again no per-skill pin.
- If you *do* set `version` in `plugin.json`/marketplace, the docs' warning is the trap: "If you declare `"version": "1.0.0"` … and push new commits without changing that string, existing users … keep the cached copy." Forgetting to bump silently starves users. Mitigation must be mechanical: `claude plugin validate --strict` in CI plus `claude plugin tag --dry-run` (it "validat[es] that plugin.json and any enclosing marketplace entry agree"), and a one-line check that a changed `skills/<name>/**` diff also touched that skill's version line.

**Workspace/eval directories do not belong in this repo's `skills/` tree.** They contain a duplicate-named SKILL.md and are one `git add` away from publication. Gitignore `skills/*-workspace/` at minimum; better, move them out of `skills/`.

## Failure modes

| Failure mode | Trigger | Blast radius | Mitigation |
|---|---|---|---|
| Vendored `playwright-cli` installed as "your" skill | Anyone runs `npx skills add tomiduss/claude-skills` (already discovered in `--list`) | Public misattribution; a stale third-party copy shipped under your name | Untrack `.claude/skills/playwright-cli` or move to a non-scanned path |
| Duplicate `multi-agent-council` skill published | `git add -A` on the untracked, un-ignored `skills/multi-agent-council-workspace/skill-snapshot/` | Two skills, same `name`, in one repo; scanners pick a shallower one silently | Gitignore/move workspace dirs out of `skills/` |
| Team-specific skill leaks to skills.sh directory | First `npx skills add` of `linear-workflow` from a public repo → telemetry lists it | Zona Cóndores workflow visible to the world, no unlisting | `metadata.internal: true` or a private repo for team skills |
| Users starved of updates | Set `version` once in plugin.json/marketplace, forget to bump | Every marketplace installer stays on old cache | CI check tying skill diffs to version bumps; `claude plugin tag --dry-run` |
| Bad commit goes live everywhere | Push to `master`; `npx skills update` re-fetches HEAD (folder hash) | All npx installers, no rollback except revert-and-push | Publish from a `release` branch/tag; keep `master` for WIP |
| Duplicate/ambiguous skill in Claude Code | Symlink in `~/.claude/skills` **and** the same skill installed as a plugin | Two entries (`multi-agent-council` and `<plugin>:multi-agent-council`); personal one shadows the plugin | Rule: dev machine = symlink only; other machines = plugin/npx only |
| Schema churn breaks the marketplace | Claude Code plugin features gated per minor ("Requires v2.1.222/224/229…") | Marketplace fails to load or validate on older clients | Use only the boring subset (`name`, `source: "./"`, `skills`, `strict: false`, `version`); run `validate --strict` |
| Edit-in-place silently stops working | Migrate to plugin install and delete the symlink | You edit the repo, Claude runs the cache copy | Keep the symlink for the dev machine (or `--plugin-dir` for testing) |

## Evidence

- `~/.agents/.skill-lock.json` v3: `brand-identity` installed from `tomiduss/claude-skills` with `skillFolderHash` — the npx channel already works and its version unit is a folder hash.
- `npx skills add /Users/tomasdussaillant/repos/skills --list` returned **9** skills incl. `playwright-cli`; `git ls-files .claude/skills` confirms it is tracked.
- `skills/multi-agent-council-workspace/skill-snapshot/SKILL.md` has `name: multi-agent-council`; `git ls-files skills/multi-agent-council-workspace | wc -l` → 0 (untracked, not ignored).
- Claude Code docs: plugins are copied to `~/.claude/plugins/cache/`; symlinks outside the marketplace are skipped; version resolution order plugin.json → marketplace entry → commit SHA; explicit warning about un-bumped `version` pinning users.
- `~/.claude/plugins/installed_plugins.json` shows real installs with `"version": "unknown"` and SHA-derived versions — implicit versioning is what most marketplaces actually ship.
- `claude plugin tag --help`: `{name}--v{version}` tags, validated against plugin.json + marketplace entry — a maintainer-controlled per-plugin version mechanism exists in the monorepo.
- Docs: "When a plugin skill conflicts with a personal skill in `~/.claude/skills/`, the personal skill takes precedence" — the symlink+plugin duplicate mode is real.
- Repo is PUBLIC (0 stars, no README); `linear-workflow` frontmatter names ZON.

## Steelman of the opposing view and why it still loses

"The ecosystem does all of this better and for free; discoverability only comes from `npx skills`/`/plugin`; keep the repo as-is and let people install." True for the *commodity* jobs — and I concede them. It loses under my value function because "as-is" today means shipping a vendored skill, a duplicate-named skill and a team-specific skill into a public directory with **no unlisting flow and no rollback**, and, if you migrate the dev machine too, losing edit-in-place. Discoverability is reversible only if hygiene comes first; the symlink is the one thing no external channel replaces.

## Concrete plan

1. Untrack `.claude/skills/playwright-cli/` (move to `~/.claude/skills` or gitignore it) — 10 min, reversible.
2. Gitignore `skills/*-workspace/` (or move workspaces to `/workspace` at repo root, outside `skills/`) — 10 min, reversible.
3. Add `metadata: {internal: "true"}` to `linear-workflow`, `linear-agent-workflow`, `designing-points-economy` (or split them into a private repo) — 20 min, reversible.
4. Add `metadata.version` to every SKILL.md (start `"1.0"`; council at its real state) — 20 min, reversible.
5. Shrink `skills.sh` to `link`/`unlink`/`list` (drop `--copy`, `update`, `setup`, `doctor`) — 1 h; keep the old file in git history, reversible.
6. Only if a marketplace is opened: `.claude-plugin/marketplace.json` with `source: "./"`, per-plugin `skills: [...]`, `strict: false`, per-plugin `version` mirroring `metadata.version`; CI runs `claude plugin validate --strict .` and `claude plugin tag --dry-run` — 2 h.
7. Publish from a `release` branch (or tags) so `master` WIP does not go live via folder-hash updates — 30 min, reversible.

## Risks / open questions I concede

- A `release` branch adds a merge step to a one-person repo; may not be worth it until there are external users.
- `metadata.internal` hides skills only from the Vercel CLI; a Claude Code marketplace hides nothing unless the entry is omitted.
- Whether Claude Code follows a *symlinked* `~/.claude/skills/<name>` for future "skills-dir plugin" features is undocumented; it works for plain skills today.

## One-line verdict

Keep the symlink (the only irreplaceable job), shrink skills.sh to it, adopt maintainer-owned `metadata.version` per skill, and fix the three leaks before letting either external channel index the repo.
