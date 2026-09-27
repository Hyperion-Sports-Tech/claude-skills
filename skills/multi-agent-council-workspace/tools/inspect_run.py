#!/usr/bin/env python3
"""Extract checkable facts from an eval run: outputs on disk + the subagent transcript (JSONL).
Usage: inspect_run.py <run_dir> <transcript.jsonl>
Prints a JSON blob of facts used to grade assertions programmatically."""
import json, os, re, sys, glob

run_dir, transcript = sys.argv[1], sys.argv[2]
out = os.path.join(run_dir, "outputs")
facts = {"outputs": {}, "transcript": {}}

# ---------- outputs ----------
def words(t): return len(re.findall(r"\b\w+\b", t))
def citations(t):
    urls = re.findall(r"https?://\S+", t)
    paths = re.findall(r"(?<![\w/])(?:[\w.-]+/)+[\w.-]+\.\w+(?::\d+)?", t)  # a/b/c.ext or with :line
    return len(set(urls)), len(set(paths))
PLACEHOLDERS = ["[GOAL]","[CONTEXT]","[ROLE_NAME]","[VALUE_FUNCTION]","[ROLE_LENS]","[RESEARCH_DIRECTIVES]","[TOKEN_BUDGET]","[MODE]","[LEAD_NAME]","[INJECTED_IN_PROMPT]"]
SECTIONS = ["Problem / Goal","Exploration","Recommended approach","Tradeoffs documented","Dissenting perspectives preserved","Implementation scope","Review triggers"]
for f in sorted(glob.glob(os.path.join(out, "**", "*.md"), recursive=True)):
    t = open(f, encoding="utf-8", errors="replace").read()
    rel = os.path.relpath(f, out)
    u, p = citations(t)
    facts["outputs"][rel] = {
        "words": words(t),
        "url_citations": u, "path_citations": p,
        "placeholders_left": [ph for ph in PLACEHOLDERS if ph in t],
        "sections_present": [s for s in SECTIONS if re.search(r"^#+\s*" + re.escape(s), t, re.M | re.I)],
        "mentions_budget_consumed": bool(re.search(r"budget|tool calls?|tokens", t, re.I)),
        "mentions_not_warranted": bool(re.search(r"not warrant|doesn't warrant|does not warrant|overkill|refuse|direct analysis|single pass|no council", t, re.I)),
    }

# ---------- transcript ----------
agent_calls, agent_calls_per_msg, tool_names, tool_errors, ask_user, notifications = 0, [], {}, [], 0, []
sendmsg = 0
first_ts = last_ts = None
try:
    for line in open(transcript, encoding="utf-8", errors="replace"):
        try: d = json.loads(line)
        except Exception: continue
        ts = d.get("timestamp")
        if ts:
            first_ts = first_ts or ts; last_ts = ts
        m = d.get("message", {})
        if not isinstance(m, dict): continue
        c = m.get("content")
        if isinstance(c, list):
            n_agent_in_msg = 0
            for b in c:
                if b.get("type") == "tool_use":
                    name = b.get("name"); tool_names[name] = tool_names.get(name, 0) + 1
                    if name == "Agent":
                        agent_calls += 1; n_agent_in_msg += 1
                    if name == "AskUserQuestion": ask_user += 1
                    if name == "SendMessage": sendmsg += 1
                if b.get("type") == "tool_result" and b.get("is_error"):
                    cc = b.get("content"); s = cc if isinstance(cc, str) else json.dumps(cc)
                    tool_errors.append(s[:300])
            if n_agent_in_msg: agent_calls_per_msg.append(n_agent_in_msg)
        if isinstance(c, str) and "<task-notification>" in c:
            r = re.search(r"<subagent_tokens>(\d+)</subagent_tokens><tool_uses>(\d+)</tool_uses><duration_ms>(\d+)</duration_ms>", c)
            summ = re.search(r"<summary>(.*?)</summary>", c, re.S)
            notifications.append({"summary": summ.group(1)[:120] if summ else None,
                                  "tokens": int(r.group(1)) if r else None,
                                  "tool_uses": int(r.group(2)) if r else None,
                                  "duration_ms": int(r.group(3)) if r else None})
except FileNotFoundError:
    facts["transcript"]["error"] = "transcript not found"

facts["transcript"].update({
    "agent_calls_total": agent_calls,
    "agent_calls_per_message": agent_calls_per_msg,
    "max_parallel_spawn": max(agent_calls_per_msg) if agent_calls_per_msg else 0,
    "nonexistent_team_tools_called": {k: v for k, v in tool_names.items() if k in ("TeamCreate", "TeamDelete")},
    "tool_call_counts": tool_names,
    "tool_errors": tool_errors,
    "ask_user_question_calls": ask_user,
    "sendmessage_calls": sendmsg,
    "child_agent_notifications": notifications,
    "child_agent_tokens_sum": sum(n["tokens"] for n in notifications if n["tokens"]),
    "first_ts": first_ts, "last_ts": last_ts,
})
print(json.dumps(facts, indent=2))
