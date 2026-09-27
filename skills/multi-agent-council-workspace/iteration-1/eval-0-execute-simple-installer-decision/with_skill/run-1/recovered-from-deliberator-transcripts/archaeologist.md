<!-- Recovered by the eval harness from the deliberator's transcript. The council lead NEVER received this paper (delivery deadlock) — see grading notes. -->

# Archaeologist — Round 1 Position Paper

## Key findings

**skills.sh's core install behavior is a direct symlink from `~/.claude/skills/<name>` to the repo's working tree** (`skills.sh:167`, `ln -s "$SKILLS_SRC/$name" "$dst/$name"`). Verified on disk: `~/.claude/skills/multi-agent-council -> /Users/tomasdussaillant/repos/skills/skills/multi-agent-council`, an absolute path straight into the git working copy — edits to `SKILL.md` are live instantly, no reinstall.

**`npx skills` does NOT preserve that semantic.** Verified: `~/.claude/skills/find-skills` is a symlink to `~/.agents/skills/find-skills`, which is a *real directory* — a fetched copy, per `~/.agents/.skill-lock.json`: `"source": "vercel-labs/skills", "sourceType": "github", "sourceUrl": "https://github.com/vercel-labs/skills.git"`. The standard flow materializes a snapshot in a central store and symlinks to *that*, not to your working tree. For a maintainer actively authoring skills, migrating fully would break the edit→test inner loop until an explicit re-fetch.

**The installer's sophistication is scope creep, not a designed feature.** Original `skills.sh` (commit `7efa0da`, Feb 25) was 157 lines: install/uninstall/list, symlink-only, no scopes. All current complexity — `--copy`, `--project`/`--both` scope, `.skill-source` provenance marker, `setup`, `doctor` — arrived in commit `7cdef8e`, titled **"improvements on council"**, which *also* added a pragmatist agent config, an entire new skill (`designing-points-economy`), and a stray cached PDF fetch artifact. This was never a deliberate installer design session — it was incidental. Only 1 of 8 repo skills (`multi-agent-council`) is actually installed via skills.sh on this machine; the `--project`/`--copy`/`--both`/`doctor`/`setup` surface is largely unexercised.

**No version concept exists anywhere in the script.** `.skill-source` (`skills.sh:22`) records only a source path, never a hash or version — `do_update` blind-recopies. The monorepo-vs-per-skill-version question wasn't decided against; it was never in scope.

## Proposed approach

Don't replace skills.sh wholesale — the direct-to-working-tree symlink is load-bearing for the one thing that matters most (fast local iteration) and no standard flow replicates it. Split the concern: keep a *minimal* symlink-only installer (strip `--copy`/`--project`/`--both`/`doctor`/`setup` — unused ceremony from an unrelated commit) for personal dev-loop use; adopt Claude Code plugin marketplace separately for distribution to others, which forces real per-skill versioning as a side effect of `plugin.json` conventions rather than leaving it undecided.

## Tradeoffs accepted

Running two systems (trimmed local symlink tool + marketplace) means dual maintenance surface. Also unverified: whether `--project --copy` (vendoring a skill into a consumer repo) has ever actually been used — I couldn't check shell history within budget; deleting it without confirming zero usage risks losing a real, just-unobserved use case.

**Budget consumed:** ~9k tokens, 6 tool calls.
