# Execution backends

The method (roles, rounds, evidence, checkpoints) is independent of the transport. The current user-facing session remains lead. Never call tools merely because another harness documents them. Inspect the actual session schema/help; when unavailable, use a supported backend or export prompts.

## Selection

| Backend | Use when | Round continuity | Delivery |
|---|---|---|---|
| Hermes native | Bounded parallel research with available Hermes tools | Fresh child per role per round, explicit state packet | `delegate_task` completion event |
| Claude interactive via Hermes | User wants Claude Code/Max, persistent steering, or a second model family | One tracked PTY session per role | Terminal output collected by Hermes |
| Claude Code native | Running inside Claude Code with the relevant tools available | One-shot `Agent`, or persistent teammates if team tools exist | Tool result or team message |
| Export/manual | No suitable runtime, or user requests prompts only | Explicit packets, relayed by operator | Written prompt package |

Prefer the user's requested backend. Otherwise use Hermes native inside Hermes. A hybrid is allowed, but name every seat's backend/model and account for all calls before dispatch. Different model families may reduce some correlated errors; they do not make outputs independent evidence.

## Hermes native

1. Inspect `delegate_task`'s live schema. Use `tasks=[{goal, context, output_schema?}, ...]` for the round. Do not invent per-task model, provider, toolsets, teammate, or resume parameters. Read configured limits from the tool; batch within them.
2. Every context is self-contained: decision brief, role, boundaries, source packet, round instructions, completion contract, and budget. Context isolation does not imply filesystem isolation; children inherit access. Read-only instructions are not a sandbox.
3. At the top level, dispatch is asynchronous. Save returned handles in the run ledger. Do unrelated work, then end the turn so completion can arrive. Do not poll child transcripts/artifacts or CI to wait for results. Use supported `list`, `steer`, `stop` controls only for supervision, not a waiting loop.
4. For Round 2, dispatch NEW children. Include the role's own previous paper in full, evidence/assumption state, bounded peer digest with exact contested excerpts, and checkpoint changes. A fresh child is not the previous agent resumed; record this in the ledger.
5. Model/provider normally inherit, unless deployment-level delegation configuration overrides them. `delegate_task` is NOT a Claude Code process and does NOT consume a Claude Max entitlement. Do not change global provider configuration just to run one seat.
6. Verify required outputs and load-bearing citations yourself. Missing/failed children become named gaps. Running children do not survive owner shutdown; a stored completion event is not resumed execution.

## Claude interactive via Hermes

Load `autonomous-coding-agents` for supervision details when available; the essential workflow is also below. Coding CLI is the execution interface, not a restriction to coding subject matter.

### Preflight and subscription boundary

- Check `command -v claude`, `claude --version`, `claude --help`, and `claude auth status --json`. Filter auth output to login method/provider/subscription type; never print tokens, email, account identifiers, or credential files.
- A Claude.ai Max login can use the subscription through Claude Code. Usage is shared with other Claude sessions and rate limits still apply. Interactive mode is not itself a billing guarantee. Check the startup account/model display and `/status` when necessary.
- Check only the PRESENCE of API-key/provider-routing environment variables, not values. If API billing, a custom provider, or an unexpected account is active, stop and ask before a paid run. Never extract OAuth tokens into Hermes or impersonate the Claude client. Never accept paid fallback/usage credits on the user's behalf.
- Do not use `--bare` for this Max path: current CLI help says it skips OAuth/keychain and requires API-key/helper authentication.
- Read source ownership/context and exact repository status before launch. For sensitive analysis, prefer a curated evidence packet in an isolated run directory, not the entire company root. A prompt restriction alone is not access control.

### Launch a read-only seat

Use the installed flags only. This command shape was exercised on Claude Code 2.1.266; check help again on later versions:

```text
terminal(
  command="claude --model sonnet --effort medium --ax-screen-reader --permission-mode plan --restricted --tools 'Read,Glob,Grep' --strict-mcp-config --mcp-config '{\"mcpServers\":{}}' --disable-slash-commands --no-chrome '<self-contained role and round prompt>'",
  workdir="<authorized source or isolated packet directory>",
  background=true, pty=true
)
```

- Use proper shell quoting (e.g. `shlex.quote` for dynamic prompts), not raw string interpolation. The model alias is illustrative, not a permanent model ID; record the actual startup model.
- `--restricted` confines file tools to working directories and suppresses ordinary settings; the explicit tools omit shell execution, edits, writes, and further delegation. Empty strict MCP configuration avoids external system writes. Managed policies may still apply. Do not enable permission bypass to get past a block.
- Read-only file tools can still read sensitive files WITHIN the allowed directory. Supply only necessary data; do not grant the vault or home directory wholesale. For hard blind review, use curated packets with no file tools, or filesystem-enforced isolation with only approved sources. Do not give the Judge a directory containing the lead draft.
- Start independent seats together within the accepted concurrency cap; one session per role. Do not reuse one Claude conversation sequentially as supposedly independent Round 1 roles. Never let each seat spawn another council.
- Record the returned process session ID per role. Inspect startup state for trust/auth dialogs and actual model/account. Ask the user for login or authorization decisions; do not auto-accept unknown workspace trust, payment, or permissions prompts.

### Collect, steer, close

1. Require a unique end marker per round (e.g. `COUNCIL_<run>_<role>_R1_DONE`) and a bounded position paper printed to the terminal. The lead saves the actual paper to its run directory; the child needs no write permission.
2. Poll/log the tracked EXTERNAL process to inspect progress. This is not polling a `delegate_task` child. PTY output may repeat partial render frames; preserve the completed message, not concatenated duplicate text.
3. A marker notification is only a hint: the initial prompt echo can match it before the agent starts. Verify the marker is in a completed assistant response and the input prompt has returned. Process-exit notification alone cannot detect an interactive turn ending.
4. For Round 2, send the digest and checkpoint delta with `process_manage(action='write', data=...)`, then send a SEPARATE `\r` if required by Ink. Confirm the message was submitted before retrying; a newline or pasted Enter can remain in the input box. Keep the same session for that role only.
5. If logs report a completed task, read the content and verify its evidence independently. A claim of file creation is not proof. Record blocked tool use and missing evidence explicitly.
6. After synthesis/corrections, send `/exit` plus a separate `\r`; verify process exit. If unresponsive, terminate only that run-owned session with `process_manage(action='kill')`, then read back its status. Never kill unrelated Claude processes.
7. At quota/auth blocks, preserve collected papers and report the gap. Switch backends only with user acceptance when it changes cost, data routing, or the accepted plan.

## Claude Code native

- For one-shot seats, use the available `Agent` tool without `team_name`; return the paper as final output.
- Persistent teammates are optional, not a requirement for multiple rounds. Use them ONLY if `TeamCreate`, team-capable `Agent`, `SendMessage`, and `TeamDelete` actually exist in the current harness. Discover their real parameter schemas; do not hardcode `to` versus `recipient` from an old example.
- When teammates are supported, the current session creates the team and remains lead. Resolve its address from the returned team metadata. Teammates explicitly send results to the lead, then idle until the next round directive.
- Otherwise run fresh one-shot seats each round with the same state packets as Hermes native. All modifiers use isolated, one-shot analysis, regardless of underlying session mechanics.
- Request shutdown from all persistent teammates; verify actual membership/process state before deletion. Silence after a timeout is NOT evidence that an agent is dead. Report unresolved cleanup instead of claiming success.

## Verification and limitations

Verify discovery, dispatch, full response receipt, a second-turn message, and shutdown separately. A single-seat smoke test proves transport, not multi-seat reasoning quality, concurrency under quota, or reliable isolation. Never report those as tested unless actually exercised.

Official references:
- https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation/
- https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/
- https://code.claude.com/docs/en/cli-reference
- https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan
