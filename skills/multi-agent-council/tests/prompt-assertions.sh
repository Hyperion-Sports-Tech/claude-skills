#!/usr/bin/env bash
# Static assertions for the multi-agent-council skill.
# Verifies portable orchestration, evidence discipline and bounded execution.
# Static assertions are not a measurement of decision quality.
# Exits non-zero if any check fails. Run from the repo root.
set -u
SK="skills/multi-agent-council/SKILL.md"
OG="skills/multi-agent-council/references/orchestration-guide.md"
DL="skills/multi-agent-council/references/deliberator-prompt.md"
CN="skills/multi-agent-council/references/patterns/council.md"
PM="skills/multi-agent-council/references/patterns/pre-mortem.md"
JD="skills/multi-agent-council/references/patterns/judge.md"
EB="skills/multi-agent-council/references/execution-backends.md"
BK="skills/multi-agent-council/references/business-and-knowledge.md"
fail=0

check() {
  local label="$1" file="$2" pattern="$3" expect="$4"
  if [ ! -f "$file" ]; then
    echo "FAIL: $label (file missing: $file)"; fail=1; return
  fi
  if grep -qE "$pattern" "$file"; then found="present"; else found="absent"; fi
  if [ "$found" != "$expect" ]; then
    echo "FAIL: $label (expected $expect, got $found)"
    fail=1
  else
    echo "OK:   $label"
  fi
}

### Architecture — the lead is the main session ###
check "arch — SKILL declares the lead is the session running the skill"     "$SK" "You are the council lead" present
check "arch — no separate team-lead agent is spawned"                       "$SK" "Spawn the .*team lead" absent
check "arch — old 'agent-teams infrastructure' framing removed"             "$SK" "Use agent-teams infrastructure to create" absent
check "arch — orchestration-guide.md exists"                                "$OG" "^# Council Orchestration Guide" present

# team-lead-prompt.md must be gone (renamed to orchestration-guide.md)
if [ -f "skills/multi-agent-council/references/team-lead-prompt.md" ]; then
  echo "FAIL: arch — team-lead-prompt.md should have been renamed to orchestration-guide.md"; fail=1
else
  echo "OK:   arch — team-lead-prompt.md removed (renamed to orchestration-guide.md)"
fi

### Backend-neutral execution ###
check "paths — execution backend reference"                                "$SK" "references/execution-backends.md" present
check "paths — native Hermes support"                                     "$EB" "delegate_task" present
check "paths — fresh workers for native Round 2"                           "$EB" "dispatch NEW children" present
check "paths — Claude interactive support"                                "$EB" "background=true, pty=true" present
check "paths — teammates optional, not required by round count"            "$EB" "Persistent teammates are optional" present

### Honest workload bounds ###
check "tier — smallest adequate run"                                      "$SK" "smallest adequate run" present
check "tier — no false measured-cost claim"                                "$SK" "NOT measured token/cost forecasts" present
check "tier — stale 'Opus 4.6 team lead' estimate removed"                  "$SK" "Opus 4.6 team lead" absent

### Complexity gate (existing behaviour must survive) ###
check "gate — tradeoffs or consequential uncertainty"                       "$SK" "at least 2 meaningful tradeoffs" present
check "gate — 'warning, not a block' framing stays removed"                 "$SK" "the gate is a warning, not a block" absent
check "gate — explicit run acceptance"                                    "$SK" "Require acceptance of this configuration" present
check "gate — modifiers individually disableable"                           "$SK" "individually disableable" present
check "gate — refuse-to-spawn fallback present"                             "$SK" "refuse to spawn|direct analysis instead" present

### Shared orchestration protocol ###
check "orch — declares the lead is not a separate agent"                    "$OG" "council lead" present
check "orch — bounded peer digest"                                        "$OG" "Round 1 Digest.*not the raw" present
check "orch — old 'full text, not summaries' directive absent"              "$OG" "full text, not summaries" absent
check "orch — peer-context 2k-token cap present"                            "$OG" "2,?000.token" present
check "orch — Dispatch accounting section present"                          "$OG" "Dispatch [Aa]ccounting" present
check "orch — Known gaps surfacing present"                                 "$OG" "Known gaps" present
check "orch — verified shutdown"                                          "$OG" "Verify actual process exit" present
check "orch — no presumed-dead shortcut"                                   "$OG" "presumed dead" absent
check "orch — waived checkpoint supported"                                "$OG" "checkpoint waived" present

### Generic deliberator contract ###
check "delib — round placeholder"                                         "$DL" "\[ROUND\]" present
check "delib — prior-state placeholder"                                   "$DL" "\[ROUND_STATE\]" present
check "delib — research allowance placeholder"                             "$DL" "\[BUDGET\]" present
check "delib — backend delivery placeholder"                               "$DL" "\[DELIVERY\]" present
check "delib — source boundary placeholder"                                "$DL" "\[BOUNDARIES\]" present
check "delib — unavailable telemetry is honest"                            "$DL" "unavailable" present
check "delib — named-claim requirement in Round 2 present"                  "$DL" "quote the specific claim" present
check "delib — weak 'Update if warranted' directive absent"                 "$DL" "Update if warranted" absent

### council.md — method separate from backend ###
check "council — explicit state replay"                                    "$CN" "fresh workers with explicit state" present
check "council — 'spawn all agents via TeamCreate' error removed"           "$CN" "Spawn all agents via TeamCreate" absent

### pre-mortem.md — Red-Team is a one-shot subagent ###
check "premortem — isolated one-shot pass"                                 "$PM" "one-shot analysis" present
check "premortem — old team-member dispatch removed"                        "$PM" "via the existing .TeamCreate. infrastructure" absent
check "premortem — bias-isolation statement present"                        "$PM" "no access to the core council's reasoning" present

### judge.md — Judge is a one-shot subagent ###
check "judge — judge.md exists with title"                                  "$JD" "^# Judge" present
check "judge — Judge is optional / opt-in"                                  "$JD" "optional|opt-in" present
check "judge — Judge spawned as a one-shot subagent"                        "$JD" "one-shot subagent" present
check "judge — Judge runs after actual core rounds"                         "$JD" "after the core rounds are collected" present
check "judge — Judge never sees the team lead's synthesis"                  "$JD" "never receives the synthesis" present
check "judge — falsifiable rubric (citation existence) present"             "$JD" "[Cc]itation existence" present
check "judge — hard cap of one revision"                                    "$JD" "one revision|1 revision" present
check "judge — non-blocking on judge failure"                               "$JD" "non-blocking" present
check "judge — stale team-lead-prompt.md reference removed"                 "$JD" "team-lead-prompt" absent
check "judge — freeze before reading output"                              "$JD" "Before inspecting any Judge output, freeze" present
check "business — source of truth routing"                                "$BK" "Hyperion workspace routing" present
check "business — real evidence vs simulation"                            "$BK" "Stakeholder simulation is hypothesis generation" present

exit $fail
