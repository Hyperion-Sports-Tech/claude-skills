# Round 1 — maintainer-pragmatist

## Value function (2–3 lines)
Minimize total cost of ownership for one person over the next 12–24 months. Every hour on installer/versioning plumbing is an hour not spent on the skills themselves. Fewest moving parts, only reversible steps, and no infrastructure for users who do not exist yet.

## Position on Q1: custom skills.sh vs `npx skills`/agentskills.io vs Claude Code plugin marketplace
**Retire skills.sh as an installer. Keep only its one irreplaceable job — the edit-in-place dev symlink — as a ~20-line script (or a documented `ln -s`).** Make `npx skills add tomiduss/claude-skills` the primary distribution path (it already works, unchanged, today). Optionally add a `.claude-plugin/marketplace.json` because it is ~20 minutes and fully reversible — but only with SHA-based versions (no `version` fields), and only if you actually want `/plugin install` + auto-update for yourself on other machines.

Job-by-job replacement of the 470-line script:
- `install` (symlink, user scope) → `ln -s $REPO/skills/<name> ~/.claude/skills/<name>` for the skill you are editing; `npx skills add ... -g` for everything else (it symlinks `~/.claude/skills/<name>` → `~/.agents/skills/<name>`, same shape).
- `install --copy` / `update` / `.skill-source` marker → `npx skills add --copy` + `npx skills update` (folder-hash based) — you stop maintaining a homemade provenance marker.
- `list` / `uninstall` → `npx skills list|remove`.
- `setup` / `doctor` (PATH launcher plumbing) → delete; nothing needs a launcher once there is no CLI.

## Position on Q2: monorepo single version vs per-skill versioning
**Monorepo, no version numbers, no tags — now.** You get per-skill update granularity for free from both ecosystems without writing a single number: `npx skills` updates only skills whose folder tree hash changed; Claude Code (with `version` omitted) uses the source commit SHA. Semver adds a recurring chore with a documented failure mode (forget to bump → users silently stuck). Add `version` to a plugin entry the day a skill has an external consumer who asks for stability; that is a one-line change and Claude Code treats the newly present string as a new version. `claude plugin tag` exists for that day; ignore it until then.

## Evidence
- **The standard flow already installed your repo, unchanged, in February.** `~/.agents/.skill-lock.json` has `brand-identity` with `source: tomiduss/claude-skills`, `skillPath: skills/brand-identity/SKILL.md`, installed 2026-02-25. Zero migration work exists to "migrate to".
- **`npx skills add /Users/tomasdussaillant/repos/skills --list` found all 8 real skills** (plus one leak, below). `claude plugin validate .` and `validate ./skills` both pass. Layout is already standard.
- **skills.sh is low-churn but not free:** 470 lines, touched in 2 of 14 commits, Bash-3.2 workarounds, symlink-resolution loop, PATH launcher, `.skill-source` marker semantics. All of that is a reimplementation of features `skills` v1.5.22 ships (symlink/copy, lock, update, list, remove).
- **The dev loop is one `ln -s`.** `~/.claude/skills/multi-agent-council` is an absolute symlink into the repo — exactly what skills.sh does and exactly what a one-liner does. Claude Code picks up SKILL.md edits live through it. Personal skills also take precedence over same-named plugin skills, so a dev symlink never fights an installed copy.
- **Only one skill is actually changing.** `multi-agent-council`: 8 commits, last today. Every other skill: 1 commit (qa-testing: 3). Per-skill versioning solves a coordination problem this repo does not have.
- **Nobody is waiting on stability.** Public repo, 0 stars, 0 forks, no README. Discoverability is not the bottleneck; a README with the one-line install is.
- **A marketplace.json needs no restructure.** anthropics/skills (already added on this machine as `anthropic-agent-skills`) uses `"source": "./"`, `"strict": false`, `"skills": ["./skills/x", ...]` over a `skills/<name>/` monorepo identical to yours. Docs: "When several plugin entries share one `skills/` folder at the marketplace root (`source: "./"`), list specific subdirectories".
- **Version bookkeeping is a trap the docs warn about:** "If you declare `"version": "1.0.0"` in `plugin.json` and push new commits without changing that string, existing users … keep the cached copy." Omitting `version` → "Claude Code uses the source's resolved commit SHA … this is the simplest setup for … actively developed plugins."
- **npx versioning is per-skill by construction:** `skills update` compares `skillFolderHash` per `skillPath` via the GitHub Trees API and reinstalls only changed skills.
- **Leak to fix (5 min):** discovery lists `playwright-cli` from `.claude/skills/playwright-cli/SKILL.md` — a vendored third-party skill — as one of "your" skills. Also `skills/multi-agent-council-workspace/skill-snapshot/SKILL.md` sits inside the scanned tree (walked 3 levels deep); currently shadowed, but fragile.

## Steelman of the opposing view and why it still loses
"Own the installer and versions now; retrofitting semver and a marketplace later is painful; the custom `--copy` + `.skill-source` gives auditable project-committed copies; Vercel/Anthropic will change conventions under you."
- Retrofit cost is one line per plugin entry, no data migration; SHA→semver just triggers one update for users. Not painful.
- `npx skills add --copy` + lockfile gives the same provenance (source, path, hash) with `update -p` for project scope. You do not need to maintain the marker.
- Convention churn risk is real but bounded: the fallback for both ecosystems is `ln -s` or `cp -R` of a plain `skills/<name>/` folder — the exact layout you already have. Owning 470 lines of bash does not hedge that risk; the standard layout does.
- "Full control over version semantics" is control over a policy with zero consumers. Buy it when someone needs it.

## Concrete plan
1. (10 min, reversible) Add `README.md`: `npx skills add tomiduss/claude-skills` (+ `--skill <name>`, `-g`), the dev-loop `ln -s`, and which skills are team-specific (linear-workflow/ZON, designing-points-economy).
2. (5 min, reversible) Remove `.claude/skills/playwright-cli` from the repo (gitignore `.claude/skills/`, reinstall locally via `npx skills add … -a claude-code` if you use it) and move `skills/multi-agent-council-workspace/` out of `skills/` (e.g. `workspace/`) so nothing non-skill lives under the scanned dir.
3. (20 min, reversible — old script stays in git history) Replace skills.sh with `link.sh`: `link [name]` / `unlink [name]` for `~/.claude/skills`, idempotent, ~20 lines. Delete `--copy`, `update`, `list`, `setup`, `doctor`.
4. (20 min, reversible, optional) Add `.claude-plugin/marketplace.json`: 2–3 plugins with `source: "./"`, `strict: false`, `skills: [...]`, **no `version` fields**. Bundle rather than one-plugin-per-skill to avoid `multi-agent-council:multi-agent-council` namespacing. `claude plugin validate .` then `claude plugin marketplace add tomiduss/claude-skills` on a second machine. If it causes friction, delete the file — nothing else depends on it.
5. (0 min) Do not add version numbers, tags, or a CHANGELOG. Trigger to revisit: an external user (or a second machine you actually pin) asks "which version am I on?".
6. (0 min) Stop iterating on installer tooling; spend the recovered hours on the 7 one-commit skills.

## Risks / open questions I concede
- Two install paths (npx + marketplace) is one more thing to explain; if the README grows past a screen, drop the marketplace file.
- SHA-based plugin versions in a monorepo re-cache every plugin on every commit. Trivial at 8 skills; revisit if the repo hits dozens.
- Vercel's CLI is a third-party dependency with telemetry and its own roadmap; skills.sh's `--copy` semantics were slightly nicer for git-committed project copies. Fallback is `cp -R`.
- Public repo mixes personal/team skills; a marketplace makes that more visible. Splitting is a later, separate decision.

## One-line verdict
The ecosystem already installed your repo for you in February — delete the installer, keep a one-line dev symlink, add a README, skip version numbers, and go write skills.
