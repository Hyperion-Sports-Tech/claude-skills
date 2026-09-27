#!/usr/bin/env python3
"""Convert a Claude Code subagent JSONL transcript into a compact markdown transcript for grading.
Usage: jsonl_to_md.py <transcript.jsonl> <out.md> [max_chars_per_block=1500]"""
import json, sys
src, dst = sys.argv[1], sys.argv[2]
MAX = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
lines = ["# Execution transcript (compacted from JSONL)\n"]
step = 0
for line in open(src, encoding="utf-8", errors="replace"):
    try: d = json.loads(line)
    except Exception: continue
    m = d.get("message", {})
    if not isinstance(m, dict): continue
    role = m.get("role"); c = m.get("content")
    ts = d.get("timestamp", "")
    if isinstance(c, str):
        step += 1
        lines.append(f"\n## Step {step} — {role} message ({ts})\n\n{c[:MAX]}{' …[truncated]' if len(c) > MAX else ''}\n")
        continue
    if not isinstance(c, list): continue
    for b in c:
        t = b.get("type")
        if t == "text" and b.get("text", "").strip():
            step += 1
            txt = b["text"]
            lines.append(f"\n## Step {step} — {role} text ({ts})\n\n{txt[:MAX]}{' …[truncated]' if len(txt) > MAX else ''}\n")
        elif t == "tool_use":
            step += 1
            inp = json.dumps(b.get("input", {}), ensure_ascii=False)
            lines.append(f"\n## Step {step} — Tool: {b.get('name')} ({ts})\n\n```json\n{inp[:MAX]}{' …[truncated]' if len(inp) > MAX else ''}\n```\n")
        elif t == "tool_result":
            cc = b.get("content"); s = cc if isinstance(cc, str) else json.dumps(cc, ensure_ascii=False)
            err = " (ERROR)" if b.get("is_error") else ""
            lines.append(f"\n**Tool result{err}:** {s[:MAX//2]}{' …[truncated]' if len(s) > MAX//2 else ''}\n")
open(dst, "w", encoding="utf-8").write("\n".join(lines))
print(dst, "steps:", step)
