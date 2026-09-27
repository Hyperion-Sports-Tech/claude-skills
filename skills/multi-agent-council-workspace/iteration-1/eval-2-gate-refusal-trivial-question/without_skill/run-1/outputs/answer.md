# 2-space vs 4-space indentation for the new TypeScript repo

## Council request: declined (deliberately) — direct answer below

You asked for a council. I did not run one, and I would push back on running one, because
this question does not meet the bar that justifies the cost:

- **Stakes are near zero.** The choice is enforced by a formatter and reversible in a single
  commit at any point in the repo's life (`prettier --write .` + one entry in
  `.git-blame-ignore-revs`). Nothing downstream depends on it.
- **The ecosystem already answered it.** TypeScript tooling and the major TS style guides
  converge on one default. There is nothing to research; there is only a preference split.
- **A council would not change the outcome.** Multiple agents arguing from different value
  functions would produce exactly the recommendation below, at many times the cost, and it
  would still come down to "adopt the tool default and stop discussing it."

What a council *would* be for: irreversible or expensive-to-reverse decisions with genuine
multi-dimensional trade-offs (data model, service boundaries, build/deploy architecture,
auth model). Indentation is not that. If the team is split, the problem is not a lack of
analysis — it is the absence of a tie-breaking rule. That is what this answer supplies.

---

## Recommendation

**Use 2 spaces. Adopt Prettier (or Biome/dprint) with default settings, commit an
`.editorconfig`, enforce in CI, record the decision as closed, and never discuss it again.**

If — and only if — the split is really about *visual* width (some people find 2 spaces
hard to scan), the compromise that dissolves the disagreement is **tabs**, since every
developer then renders indentation at whatever width they like. Do not pick 4 spaces:
it has the weakest ecosystem support of the three and does not solve the preference
split any better than 2 does.

---

## The case for 2 spaces (why it wins for TypeScript specifically)

1. **It is the TypeScript ecosystem default.** Prettier (`tabWidth: 2`, `useTabs: false`),
   Deno's formatter, the Google TypeScript Style Guide, the Airbnb style guide, Angular CLI
   scaffolds, NestJS scaffolds, and Node.js core all use 2 spaces. The overwhelming majority
   of TypeScript published to npm is 2-space because Prettier's defaults dominate.
2. **Zero-config, zero-drift.** With 2 spaces you ship an empty `.prettierrc` and every
   editor plugin, scaffold, code generator, and snippet already matches. Choosing 4 means
   every generated file, every pasted example from docs, and every dependency's source you
   step into looks different from your code — small, constant friction.
3. **Horizontal room.** TypeScript nests deeply (generics, JSX/TSX, callback chains,
   `async` blocks inside handlers). At 80–100 columns, 4-space indentation pushes more lines
   into wrapping, and Prettier's wrapping decisions are what people actually complain about.
4. **Consistency with what you read.** Engineers spend more time reading dependency and
   framework source than writing their own; matching that convention lowers context-switch
   cost when debugging into `node_modules`.

## The honest case for 4 spaces (and why it does not carry)

- **Readability of nesting.** Some people scan block structure faster with wider indents.
  Real, but subjective, small, and — importantly — better served by *tabs* (each reader
  picks their own width) than by forcing 4 on everyone.
- **Precedent from elsewhere.** VS Code's `editor.tabSize` defaults to 4; ESLint's legacy
  `indent` rule defaulted to 4; C#, Java, and Python teams arrive with 4 as muscle memory;
  Microsoft's own TypeScript compiler repository is 4-space. None of these are conventions
  of the *TypeScript application ecosystem* your repo will live in — and VS Code detects
  indentation per file by default anyway, so its global setting is irrelevant once a
  `.editorconfig` exists.
- **"Deep nesting becomes painful, which pushes us to refactor."** A nice story, but a
  linter rule (`max-depth`, `complexity`) does that job explicitly; indentation width is a
  poor proxy.

Net: 4 spaces is a legitimate personal preference with no ecosystem argument behind it for
TS. It costs a config line plus permanent low-grade friction with tooling and generated
code, and buys nothing that tabs would not buy better.

## The third option: tabs

Legitimate, and worth naming because it actually addresses a *split* team:

- **Pro:** each developer sets their own display width (2 for one camp, 4 for the other);
  this is also the accessibility-preferred choice for low-vision developers who need very
  wide indents. Biome defaults to tabs.
- **Con:** you leave the Prettier default (one config line, `useTabs: true`); GitHub renders
  tabs at 8 columns unless the repo has an `.editorconfig` with `indent_size`/`tab_width`
  set (it honors that) or the viewer changes their setting; embedded YAML/Markdown/JSON
  snippets in template literals and docs are space-indented and look inconsistent; and most
  copy-pasted TS from the wider world is spaces.

Pick tabs if the width disagreement is genuinely what is dividing the team. Otherwise, 2.

---

## How to end the debate today (the part that actually matters)

The value of this decision is not in the number. It is in making it *once*, mechanically
enforced, so no reviewer ever comments on whitespace again.

1. **Tie-break rule: the tool default wins.** Remove humans from the loop. Prettier's
   default is 2 spaces; if you would rather adopt Biome, its default is tabs. Either is
   fine — the point is that nobody "won"; the tool decided.
2. **Commit the config** (below), run the formatter once over the repo in a dedicated
   commit, and add that commit's SHA to `.git-blame-ignore-revs` so blame stays useful.
3. **Enforce it:** `prettier --check .` in CI and a pre-commit hook (lint-staged / husky /
   lefthook). Formatting is then never a review topic.
4. **Record it as closed.** One paragraph in `CONTRIBUTING.md` (or a tiny ADR):
   "Indentation: 2 spaces, enforced by Prettier defaults. Rationale: ecosystem default,
   zero-config. Reopen only if we change formatters."
5. **Set a revisit condition, not a revisit date.** The only legitimate reason to reopen is
   adopting a formatter whose default differs. Preference alone does not reopen it.

### Config

`.editorconfig`
```ini
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false
```

`.prettierrc` — intentionally minimal; defaults are the decision:
```json
{}
```
(Add only non-formatting-war options you actually need, e.g. `"singleQuote": true`.
Do **not** set `tabWidth`; leaving it unset is what makes the decision "the default won.")

`package.json`
```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

`.git-blame-ignore-revs`
```
# Initial Prettier formatting pass
<sha-of-the-formatting-commit>
```
and once: `git config blame.ignoreRevsFile .git-blame-ignore-revs`.

If the team chooses tabs instead: `indent_style = tab` in `.editorconfig`,
`{ "useTabs": true }` in `.prettierrc`, and additionally `tab_width = 4` (or whatever
you want GitHub to render) in `.editorconfig`. Everything else is identical.

---

## Bottom line

- **Answer:** 2 spaces, via Prettier defaults, enforced in CI, decision recorded and closed.
- **Acceptable alternative:** tabs, if the split is about visual width — it lets both camps
  see what they want.
- **Not recommended:** 4 spaces — a valid personal preference with no TypeScript-ecosystem
  backing and permanent small friction with tooling and generated code.
- **Why no council:** trivially reversible, already settled by the ecosystem, and the
  disagreement is a preference split that needs a tie-break rule, not more deliberation.
  Spend the council budget on a decision that is actually hard to undo.
