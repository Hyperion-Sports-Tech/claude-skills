# Council request: 2-space vs 4-space indentation in a new TypeScript repo

**Outcome: council not spawned (complexity gate refused). Direct single-pass analysis provided below.**

---

## 1. Gate decision (multi-agent-council, Step 1)

The skill's complexity gate blocks spawning unless three conditions are all met. This request fails the first one, so the council was refused before any agent was created:

> "I don't see 2 distinct tradeoffs that warrant a full council here. Want me to analyze this directly — single pass, no council overhead? Or if you think the tradeoffs are there, rephrase them more specifically and I'll check again."

The user was not available to answer, so I proceeded with the alternative the skill offers: a direct analysis. Zero deliberator, judge, or modifier agents were spawned.

### Why condition 1 ("name 2 meaningful tradeoffs") fails

I tried, in good faith, to write the tradeoffs the way the skill requires (specific, structural, of the "RLS centralizes policy but blocks multi-tenant sharding" calibre). The best candidates:

| Candidate tradeoff | Why it does not clear the bar |
|---|---|
| Ecosystem/tooling default (2) vs. team familiarity from Python/Java/C# backgrounds (4) | Real, but it is a preference, not a structural consequence. Nobody types indentation once a formatter is on save. |
| Horizontal room in deeply nested code (2) vs. more visible nesting depth (4) | Aesthetic; both fit within a 100-column print width for any code you would want to keep. Deep nesting is a code-shape problem, not a width problem. |
| Consistency with generated code / pasted snippets (2) vs. one extra config line forever (4) | True, but this is a tie-breaker, not a tradeoff that produces materially different outcomes. |

What disqualifies the question as council-shaped is not that the arguments are weak — it is that **the decision is fully reversible in one commit** (formatter rewrite + `.git-blame-ignore-revs`), has **no architectural or cost consequence**, and has **one obvious direction** in this ecosystem. The skill description is explicit: "do NOT trigger for simple questions or problems with one obvious direction."

### Conditions 2 and 3 (tier, modifiers, cost acceptance)

Moot once condition 1 fails, but for the record: the cheapest council configuration (Simple tier, no modifiers) is ~50-90k tokens, about 5-9x a single-model answer. The realistic difference in outcome between "2" and "4" for this repo is close to zero, so that spend cannot be justified.

### Clarifying questions I would have asked (user unavailable — assumptions used instead)

1. *Which formatter/toolchain are you adopting: Prettier, Biome, dprint, or none yet?* — Assumed Prettier (dominant default in TS repos); Biome note included below since its default differs.
2. *Is anything else stuck on this — is the actual disagreement about tabs vs. spaces, or about who gets to decide formatting rules in general?* — Assumed the question is literally 2 vs 4 spaces and that the underlying need is to end the debate.
3. *Any external constraint (monorepo shared config, org style guide, code that must be shared with a 4-space codebase)?* — Assumed none; a new standalone repo.

If any assumption is wrong, the recommendation below changes only at the margins (see "When 4 is the right call").

---

## 2. Direct analysis (single pass, no council)

### Recommendation

**Use 2 spaces, and make the choice invisible: enforce it with a formatter on save plus a CI check, so nobody on the team ever manually indents again.** Then stop discussing it.

### Why 2 (evidence, not taste)

- **It is the zero-config default of the TypeScript ecosystem's formatter.** Prettier's `tabWidth` defaults to `2` and `useTabs` to `false` (verified against Prettier's current option docs). Choosing 2 means the fewest configuration lines and no surprise when someone runs Prettier without the repo config present.
- **The tooling around you already writes 2-space files.** `npm`/`pnpm`/`yarn` write `package.json` with 2-space indentation; `tsc --init`, `create-vite`, `create-next-app`, the Angular CLI and Nest CLI scaffold 2-space TypeScript. Picking 4 means generated files, copied docs examples, and pasted snippets from most open-source TS projects are "wrong" until reformatted.
- **Major published style guides for JS/TS use 2 spaces** (Airbnb, Google's `gts`, Node.js core, Deno's `deno fmt` default). New hires from the TS world will expect it.
- **Aggregate cost is asymmetric.** Choosing 4 costs a little friction forever (extra config, mismatched pasted code, occasional wrong-width PR from a contributor's default). Choosing 2 costs nothing except a mild preference for some teammates, and that preference disappears once nobody types indentation.

### What 4 honestly has going for it

- VS Code's default `editor.tabSize` is 4, ESLint's legacy `indent` rule defaulted to 4, and the TypeScript compiler's own source uses 4-space indentation. So the "4 camp" is not wrong — it is just aligned with editor/legacy defaults instead of the TS *project* defaults.
- Nesting depth is slightly easier to see at 4. In a repo with a formatter and a sane max line width, that difference is negligible.

### When 4 is the right call

- Your org has an existing style guide or shared formatter config that mandates 4, or this repo will share code/reviewers with a 4-space codebase. Consistency across repos beats ecosystem default.
- The team is coming from Python/C#/Java and you are trading style debate energy for goodwill. That is a legitimate leadership call — just make it once, write it down, and enforce it the same way.

### One substantive point the 2-vs-4 framing hides

The only argument in this space with real weight is the **accessibility argument for tabs**: developers who need very large or very small indentation (low vision, screen magnifiers) can set their own tab width per editor, which spaces cannot offer. Note that Biome's formatter defaults to **tabs** for exactly this kind of reason. If someone on the team is in that situation, choose tabs (width 2 rendered) and move on; the rest of this analysis holds unchanged. Otherwise spaces are the ecosystem norm and avoid tab issues in YAML (which forbids tabs for indentation) and mixed-alignment diffs.

### Make it invisible (the part that actually matters)

```jsonc
// .prettierrc  — write the defaults out so intent is explicit
{ "tabWidth": 2, "useTabs": false }
```

```ini
# .editorconfig — keeps every editor/IDE consistent, including for non-TS files
root = true
[*]
indent_style = space
indent_size = 2
end_of_line = lf
insert_final_newline = true
```

```jsonc
// package.json (scripts)
"format": "prettier --write .",
"format:check": "prettier --check ."
```

- CI: run `npm run format:check` on every PR (fails the build on drift).
- Editor: commit `.vscode/settings.json` with `"editor.formatOnSave": true` and Prettier as default formatter; optionally lint-staged + husky for a pre-commit format.
- If you use **Biome** instead of Prettier: it defaults to tabs, so set `"formatter": { "indentStyle": "space", "indentWidth": 2 }` explicitly in `biome.json`.

Once this is in place, the width is a single config value that no human types by hand — which is why the choice does not deserve a council.

### How to end the split (decision procedure, since the outcome barely matters)

1. Time-box: 10 minutes, one meeting or one thread.
2. The repo owner / tech lead decides using a stated tie-breaker: **"least configuration; matches the ecosystem default."** That yields 2.
3. Write one line in `CONTRIBUTING.md`: "Formatting is owned by Prettier (2 spaces). Do not debate formatting in PR review; change `.prettierrc` via PR if you want a change."
4. Everyone disagrees-and-commits. Anyone who still cares can open a PR to change the config, and it will be judged on the reversal cost below (near zero), so nobody is trapped.

### If you change your mind later (reversal recipe — proof this is low-stakes)

1. Change `tabWidth` in `.prettierrc` and `indent_size` in `.editorconfig`.
2. `npx prettier --write .` and commit that reformat **alone**.
3. Put that commit SHA in `.git-blame-ignore-revs` (GitHub honors this file automatically; locally run `git config blame.ignoreRevsFile .git-blame-ignore-revs`) so `git blame` stays clean.

Total cost: one PR, no logic changes, no history damage.

---

## 3. Cost accounting

- Council (refused): would have been >= ~50-90k tokens at the Simple tier before any modifier, i.e. 5-9x a direct answer, for a decision whose reversal cost is one commit.
- What was actually spent: this direct analysis plus two documentation lookups (Prettier and Biome formatter defaults) to keep the evidence current. No agents spawned.
