# Signs of AI writing in English

Condensed from Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. Their patterns come from reviewing thousands of AI-generated edits.

The underlying cause, in their words: LLMs guess what should come next, so the output drifts toward the most statistically likely sentence that fits the widest variety of cases. Every pattern below is a symptom of that.

## Content

### Inflated importance and legacy

**Watch:** stands as, serves as, is a testament to, plays a vital/crucial/pivotal role, underscores its importance, reflects a broader, marking a shift, key turning point, evolving landscape, leaves an indelible mark, deeply rooted

Ordinary facts get promoted to historical turning points.

> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain.

becomes

> The Statistical Institute of Catalonia was established in 1989, part of a wider decentralization of administrative functions in Spain.

### Name-dropping as proof

**Watch:** has been featured in, cited in leading publications, an active social media presence with over N followers

A list of famous outlets with no context. Keep a citation when the source says what was said and where; drop the follower count.

### Shallow analysis in an -ing clause

**Watch:** highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, fostering, showcasing

An -ing phrase tacked onto a plain fact to make it sound deep.

> The temple's palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets and the Gulf of Mexico, reflecting the community's deep connection to the land.

becomes

> The temple is painted blue, green, and gold, colors meant to evoke Texas bluebonnets and the Gulf of Mexico.

### Sales language

**Watch:** boasts, vibrant, rich (figurative), profound, nestled, in the heart of, renowned, breathtaking, must-visit, stunning, commitment to, groundbreaking

Reads like a brochure, especially for places, products, and organizations.

> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage.

becomes

> Alamata Raya Kobo is a town in the Gonder region of Ethiopia.

### Vague sources

**Watch:** industry reports suggest, observers have noted, experts argue, some critics say, several sources

Attribution to nobody. Name the source if the original has one, otherwise cut the claim or mark the gap. Never invent one.

### Stock challenges and outlook sections

**Watch:** Despite its success, faces several challenges; Despite these challenges; Challenges and Legacy; Future Outlook

Sections that name no specific problem and commit to nothing.

## Language

### Overused words

Actually, additionally, align with, crucial, delve, emphasize, enduring, enhance, foster, garner, highlight, interplay, intricate, key (adjective), landscape (abstract), pivotal, quietly, showcase, tapestry, testament, underscore, valuable, vibrant.

One of these is nothing. Four in a paragraph is the tell.

### Avoiding "is" and "has"

**Watch:** serves as, stands as, represents, boasts, features, offers

> Gallery 825 serves as LAAA's exhibition space and boasts over 3,000 square feet.

becomes

> Gallery 825 is LAAA's exhibition space. It has 3,000 square feet.

### "Not X but Y" and clipped negatives

> It's not just a song, it's a statement.

becomes a sentence that says what the song does. Same for tailing fragments like "no guessing" and "no setup required", which drop the subject to sound punchy.

### Forced groups of three

Three items because three sounds complete, not because there are three things. If there are two, write two.

### Synonym cycling and repeated openings

The protagonist becomes the main character becomes the central figure becomes the hero, all in one paragraph. Use one name. Separately, several sentences opening with the same subject usually want to be merged, though deliberate repetition for rhythm is fine.

### False ranges

**Watch:** from X to Y, when X and Y are not ends of anything

> from the singularity of the Big Bang to the grand cosmic web, from the birth of stars to the dance of dark matter

becomes a plain list of what the book covers.

### Passive voice and missing subjects

> No configuration file needed. The results are preserved automatically.

becomes

> You do not need a configuration file. The system preserves the results.

## Style

- **Em and en dashes.** Replace with a comma, colon, period, or parentheses, unless the writer's own sample uses them. Also catch spaced hyphens and double hyphens used as dashes.
- **Decorative bold.** Bolded terms and acronyms with no reason.
- **Lists of bold mini-headings.** Every item opening with `**Label:**` and a sentence restating the label. Usually a paragraph in disguise.
- **Title Case Headings.** Use sentence case.
- **Emoji as bullets.** 🚀 💡 ✅ decorating headings and list items.
- **Curly quotes,** when the document or codebase uses straight ones.

## Chatbot residue

- **Leftover conversation.** "I hope this helps", "Certainly!", "Would you like me to expand on any section?", "Let me know if..."
- **Knowledge-cutoff disclaimers and gap-filling.** "While specific details are not readily available, it appears that...", "she likely grew up in...", "maintains a low profile". State what the source does not show, or cut the sentence. Never dress a guess as a fact.
- **Agreeable openers.** "Great question!", "You're absolutely right that..."

## Filler and hedging

| Instead of | Write |
|---|---|
| in order to achieve this goal | to achieve this |
| due to the fact that | because |
| at this point in time | now |
| in the event that you need help | if you need help |
| has the ability to process | can process |
| it is important to note that the data shows | the data shows |

**Qualifier stacks.** "It could potentially possibly be argued that the policy might have some effect" becomes "the policy may affect outcomes." Keep a qualifier when the source supports it and the meaning needs it; cut the ones that only repair an earlier overstatement.

**Generic positive endings.** "The future looks bright. Exciting times lie ahead." Cut it and end on the last concrete fact.

**Hyphen overuse.** Keep the hyphen before a noun (`a high-quality report`), drop it after (`the report is high quality`).

**False depth.** "The real question is", "at its core", "fundamentally", "what really matters". Say the point instead of announcing that you are about to reveal it.

**Announcing the next point.** "Let's dive in", "here's what you need to know", "now let's look at". Also the casual version, "one thing that bit me here". Delete the announcement and state the thing.

**Heading echoed in the first line.** "## Performance" followed by "Speed matters."

**Forced punchlines.** A row of dramatic fragments where one sentence would do.

**Formulaic sayings.** "X is the language of Y", "the currency of trust", "efficiency becomes a trap". Replace with the specific claim.

**Fake-candid openers.** "Honestly?", "Look,", "Here's the thing", "Let's be honest" used as a staged pause before an ordinary point. The word mid-sentence is fine; the theatrical standalone is the tell.

**Answering objections nobody raised.** "This isn't really about X", "I'm not saying Y", "Don't get me wrong". Cut the defense and state the claim. A direct statement like "the API is not thread-safe" is not this pattern.

**Rejecting alternatives nobody proposed.** "A tempting approach would be to..., but that would...". Usually a leftover from an earlier draft. Cut it and state the real constraint. One rejected option can be legitimate; several short unrelated ones are the tell.

## Do not flag

- Clean grammar and consistent style. Polish is not evidence.
- Formal vocabulary in a formal document.
- A single transition word. Piles are the tell.
- Curly quotes or em dashes on their own. Editors and word processors produce both.
- One short sentence for emphasis.
- Real disclaimers, scope notes, legal and safety language, named objections, FAQ answers.
- Real alternatives in a design doc or tutorial.
- Unsourced claims. Most writing is unsourced.
- Correct complex formatting. Templates produce that.
- A watched phrase inside a quotation, title, or example where the phrase is the subject.
- Anything written before 30 November 2022.
