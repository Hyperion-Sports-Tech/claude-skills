# Evaluation and maintenance

## Run offline checks

From the source repository:

```bash
bash skills/multi-agent-council/tests/prompt-assertions.sh
bash skills/multi-agent-council/tests/value-function-check.sh
python3 skills/multi-agent-council/scripts/validate_package.py
```

The Python validator checks package links, index coverage, rendering the generic prompt for supported transports, and key protocol contracts. Shell checks preserve a small explicit regression surface. These are static/structural checks, not proof of improved reasoning or runtime isolation.

## Behavioral cases

`scripts/behavioral-cases.json` contains deliberately specified TEST scenarios, not real business observations. Its default status is `not_executed`: writing a case is not running it. Evaluate each in an isolated scratch workspace, capture real tool traces and outputs, and review its must/must-not criteria. Never fabricate a tool failure or live-system answer as actual execution; use an explicitly named test harness/fixture when injecting failures.

The pre-existing `evals/evals.json` is a legacy v1 evaluation file. Preserve it unless its owner authorizes a migration: some assertions intentionally reflect superseded v1 contracts (token self-estimates, teammate-only multi-round execution, rigid new-evidence rule). Do not report those assertions as passed by v2 or change unrelated untracked eval work incidentally. The v2 cases are separate and not executed merely by the offline validator.

## Runtime smoke test

Verify the selected backend can launch a read-only seat, return one full answer, receive a second directive in the same interactive session (or explicit state in a fresh native child), and terminate cleanly. Record actual model/auth route, flags, process handle, outputs and exit status. A prompt echo matching a completion marker is not task completion.

A single-seat smoke test does not establish concurrent quota behavior, multi-seat evidence quality, or hard confidentiality isolation. Test those separately before claiming them. Native team tools also require their own live capability test.

## Outcome evaluation

Use the business-and-knowledge reference's method-evaluation recipe: matched task set, direct single-agent baseline, comparable evidence and budgets, blind review where practical, error/uncertainty checks, and ablations. Preserve raw papers and identify source/model correlations. Prefer a simpler method when the council adds no decision value.

## One source, multiple harnesses

Keep this skill source in its owning repository. When a local Hermes installation supports following skill-directory symlinks, link only this skill into the active profile and verify both `skills_list` and `skill_view`, including a reference file. Do not import the entire repository or silently create a divergent Hermes fork. A symlink means future edits affect the shared source; review Git status and diffs there. External directories are an alternative documented in Hermes, but they can broaden discovery and are not a read-only boundary.

Use `/reload-skills` to refresh slash-command discovery in an existing Hermes TUI. Do not change another profile, global provider routing, or unrelated skills to install this one.
