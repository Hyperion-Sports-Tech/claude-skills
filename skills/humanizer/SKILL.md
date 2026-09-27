---
name: humanizer
description: >
  Use when existing prose sounds like a machine wrote it and has to read like a
  person did: marketing and product copy, landing pages, in-app text, investor
  updates, sponsor and partner proposals, one-pagers, decks, LinkedIn posts.
  Works in Spanish and English. Trigger on "esto suena a IA", "suena a ChatGPT",
  "humaniza esto", "hazlo más corto", "make this sound human", "tighten this
  up", "this reads like marketing fluff", or any request to edit, shorten,
  sharpen or de-fluff text that already exists. Use it even when the user only
  says the text feels long, generic, or off. Do NOT use for writing from
  scratch, for translation, or for code and code comments.
---

# Humanizer

Cut what carries nothing, put the verdict first, then remove the fingerprints. In that order.

Order matters. De-fluffing a paragraph you are about to delete is wasted work, and moving the verdict to the top usually reveals another third of the text that was only there to delay it.

The value function comes from the Minimalist role in `multi-agent-council`: **the text cannot be longer than the decision it supports. Addition is almost always wrong.**

## When to use

- The text exists already and reads like an LLM produced it
- Spanish copy that sounds translated from English marketing
- An investor or sponsor document where the ask is buried in paragraph four
- Anything the user calls long, generic, inflated, or "off"

Do not use it to write a first draft, to translate, or on code. If the user wants new content, write the content; this skill only edits.

## Before the first pass

Answer two questions in one line each. Everything downstream depends on them.

1. Who reads this, and what do they do after reading it?
2. What is the one thing that has to survive if the rest is cut?

If the source does not make these answerable, ask the user. Two sentences of context beats three passes of guessing.

## The rule that outranks the others

Never add a fact. Not a number, name, date, price, metric, quote, client, or citation. This matters most in exactly the documents this skill is for, because an investor deck with an invented number is worse than an investor deck that is boring.

When the rewrite needs a fact the source does not have, leave a visible gap marker instead of filling it:

> Cerramos el trimestre con [falta dato: miembros activos] miembros activos, [falta dato: % vs Q1] más que en marzo.

The user fills the brackets. You never do. Gap markers stay in the delivered text and get called out in the summary.

## Pass 1, cut

Score every sentence against the reader's next action. Remove it, and if the reader would still decide the same thing, it stays removed.

Delete on sight:

- Preamble that announces the subject instead of stating it. "En este documento repasaremos", "A continuación detallamos", "Let's dive into"
- A sentence that restates the heading right below the heading
- Stock "desafíos y oportunidades" or "Future Outlook" sections that name no specific problem
- Hedge stacks: "podría potencialmente", "en cierta medida", "creemos que probablemente"
- Meta-commentary about the writing: "Cabe destacar que", "Es importante mencionar que", "It is worth noting that"
- Any adjective doing the work a number should do

Never delete:

- Numbers, names, dates, quotes, links, prices, legal and regulatory text
- The ask
- A caveat that is true and load bearing. The bad kind repairs an overstatement you just made; the good kind tells the reader something they need

**The output is shorter than the input.** That is a check you can run, not a feeling. If the rewrite grew, you added, and addition is almost always wrong. The only exception is expanding a real fact the source compressed into a buzzword, and that comes from the source or the user.

**Before**

> Durante los últimos meses hemos estado trabajando intensamente en consolidar nuestra propuesta de valor. Es importante destacar que, si bien el crecimiento ha sido positivo, existen desafíos que debemos considerar. Como toda empresa en etapa temprana, enfrentamos retos típicos del sector, incluyendo la adquisición de usuarios y la retención a largo plazo. No obstante, confiamos en que, con la estrategia adecuada, seguiremos avanzando por el camino correcto.

**After**

> Tenemos dos problemas: el costo de adquisición y la retención. [falta dato: CAC del trimestre vs. el anterior] [falta dato: retención a 90 días]

Four sentences of cushioning became two facts and two questions. The questions are the useful part, because now the user knows what the document is missing.

## Pass 2, lead

The failure here is structural, not verbal: the conclusion sits at the bottom because the model built up to it. Rebuild to a fixed shape instead of hunting for phrases to ban.

**Investor, sponsor, partner, board**

1. First sentence: the result or the ask, with its number
2. Second sentence: the one fact that makes it credible
3. Middle: the evidence, including the worst number, not only the good ones
4. Last line: what you want, from whom, by when

**Marketing and product copy**

1. First line: what the reader gets, in the words the reader uses
2. Second line: the mechanic or the proof of why it works
3. Close: one action

No feature list before the reader knows what the thing is. One action, not three.

Numbers beat adjectives everywhere in this pass. "Creció 3x" instead of "creció significativamente", and where there is no number, say the plain qualitative thing or leave a gap marker.

**Before**

> Sumérgete en el vertiginoso mundo del fan engagement. Zona Cóndores es una solución integral que revoluciona la manera en que los clubes se conectan con sus hinchas, permitiendo crear experiencias únicas, memorables y personalizadas. ¡Descubre todo lo que podemos hacer por ti!

**After**

> Zona Cóndores conecta a los clubes con sus hinchas: desafíos, puntos y recompensas en una sola app. Los hinchas juegan y el club, por fin, sabe quiénes son.

The English terms that survived are the ones the industry says out loud. See `references/glossary-keep-in-english.md` for how to decide.

## Pass 3, de-AI

Now fix the sentence-level tells in the structure that survived.

Route by the language of the text, not the language of the conversation:

- Spanish text: read `references/ai-tells-es.md`
- English text: read `references/ai-tells-en.md`
- Mixed document: read both, and apply each to its own sections

The Spanish catalog is not a translation of the English one. Spanish LLM output has its own tells, including calques that are grammatically wrong in Spanish, Peninsular defaults that are wrong for a Chilean reader, and punctuation the model drops.

The ten that show up in almost every Spanish draft, so you can start before opening the file:

| Tell | Instead |
|---|---|
| "En el vertiginoso mundo de", "En la era digital" | Start with the subject |
| "se posiciona como", "se consolida como" | "es" |
| "No solo X, sino que también Y" | One clause with the point |
| "permitiendo así", "logrando", "garantizando" tacked on with a comma | A new sentence, or nothing |
| "solución integral", "herramienta poderosa" | What it actually does |
| "revolucionar", "transformar", "potenciar", "empoderar" | The concrete verb |
| "clave", "fundamental", "crucial", "innovador" | Delete, or show why |
| "Cabe destacar que", "Es importante mencionar" | Delete the wrapper, keep the claim |
| "En resumen", "En definitiva" as a closer | End on the last real fact |
| "¡Descubre cómo!" and exclamation marks | A plain sentence |

## Spanish, register and typography

Write for a Chilean reader unless the user says otherwise. Models default to Peninsular Spanish, and it reads foreign here.

- "tú", never "vosotros". "usted" only for institutional and sponsor documents, and then hold it for the whole text
- "celular" not "móvil", "computador" not "ordenador", "arriendo" not "alquiler"
- Avoid "coger" entirely
- Opening marks are required: "¿Cómo funciona?" and "¡Vamos!", not "Como funciona?"
- No serial comma before "y" or "o". Spanish does not take it, and models insert it out of English habit
- Headings in sentence case, not Title Case. Spanish capitalizes the first word and proper nouns only
- Straight quotes, and one convention per document

## English terms in Spanish text

Keep the English term when it is what the industry actually says: white label, fan engagement, marketing, AI-native, growth, onboarding, churn, engagement, sponsor, roadmap, deploy, dashboard, paywall, drop, merchandising.

Translating those produces worse text, which is the whole point. "Compromiso del aficionado" is not fan engagement, and nobody in the room says it.

Translate when a natural Spanish word exists and people use it: "usuario", "hincha" or "socio" over "fan" depending on context, "recompensa" over "reward", "entrega" over "delivery" in a project sense.

The full decision rule, term tables, and the grammatical gender to use for English nouns are in `references/glossary-keep-in-english.md`. Read it whenever the text is Spanish.

## Check the mechanical tells with the script

Do not hand-scan for dashes and curly quotes. Run:

```bash
python skills/humanizer/scripts/check_tells.py OUTPUT.md --original SOURCE.md
```

It reports em and en dashes, curly quotes, emoji, Title Case headings, bold-label list items, Peninsular Spanish, gerund tack-ons, missing opening marks, banned phrases with line numbers, the word count delta, and sentence length variance. Code blocks, inline code, YAML frontmatter and link URLs are excluded from every check, so it will not flag your snippets.

It is a lint, not a gate. Read what it flags and decide. A flagged phrase inside a quotation stays.

Low sentence length variance is the one signal worth acting on even when nothing else fires. Human prose alternates short and long; LLM prose settles into an even mid-length cadence. If the standard deviation is under about 5 words, break something up or run two sentences together.

## What you must not change

Numbers, names, dates, quotes, prices, links, code blocks, YAML frontmatter, legal and regulatory language, and any phrase the text is discussing rather than using. If the source quotes someone saying "una solución integral", the quote keeps it.

## What not to flag

The reason this skill has a false positive list is that the tells overlap with ordinary competent writing. None of these is evidence on its own:

- Clean grammar and consistent style. Polish is not a tell
- One "sin embargo", one "además", one em dash. Piles are the tell, single instances are not
- Curly quotes alone. Word, Docs and macOS produce them without any AI involved
- One short sentence for emphasis. Flag runs of fragments, not a single one
- Formal vocabulary in a document that should be formal
- A real disclaimer, scope note, or legal caveat
- Deliberate repetition used for rhythm
- Anything written before December 2022

When unsure, look for several tells together in the same paragraph.

## How to return the result

**File named by the user.** Do the full rewrite, write only the final text to the file, and leave code, metadata, data and link targets untouched. Then give a short summary in chat: what you cut, what you moved, and every gap marker you left.

**Text pasted in chat.** Return the final rewrite, then a short list of what you changed and why, then the gap markers.

**Called by another skill or task.** Return only the final text.

## Self-check before returning

- Is it shorter than the source?
- Does the first sentence carry the result or the ask?
- Did any fact, number, name or date change or appear? If yes, revert it
- Are the missing facts marked with brackets instead of filled in?
- Did the script run clean, or is every remaining flag one you decided to keep?
- Read it out loud. Where you stumble, rewrite the paragraph around its point instead of patching the phrase

## Reference files

- `references/ai-tells-es.md`, the Spanish catalog. Read it for any Spanish text
- `references/ai-tells-en.md`, the English catalog, condensed from Wikipedia's "Signs of AI writing"
- `references/glossary-keep-in-english.md`, which terms stay in English and how to decide for a term that is not listed
- `scripts/check_tells.py`, the mechanical linter
