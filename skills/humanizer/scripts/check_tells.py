#!/usr/bin/env python3
"""Flag the mechanical signs of AI writing in a Markdown or plain text file.

This is a lint, not a gate. It finds the things a regex can find (dashes, curly
quotes, Title Case headings, stock phrases, register slips, word count) so the
agent running the humanizer skill can spend its attention on judgment instead of
scanning for punctuation.

Code blocks, inline code, YAML frontmatter and link URLs are masked before any
check runs, so snippets never get flagged. Findings inside blockquotes are
marked, because a blockquote is usually someone else's words and stays as is.

Usage:
    python check_tells.py OUTPUT.md
    python check_tells.py OUTPUT.md --original SOURCE.md
    python check_tells.py OUTPUT.md --lang es --strict
"""

import argparse
import re
import statistics
import sys
from pathlib import Path

MAX_EXAMPLES = 6  # per check, so a noisy file still prints a readable report


# ---------------------------------------------------------------------------
# Masking
#
# Every mask replaces characters with spaces rather than deleting them. Line and
# column numbers stay true to the original file, which is the whole point of
# reporting line numbers at all.
# ---------------------------------------------------------------------------

def _blank(match):
    return re.sub(r"[^\n]", " ", match.group(0))


def mask_uncheckable(text):
    """Blank out the regions where our rules do not apply."""
    # YAML frontmatter, only when it opens on line 1
    text = re.sub(r"\A---\n.*?\n---\n", _blank, text, count=1, flags=re.S)
    # Fenced code blocks. Indented blocks are left alone on purpose: four space
    # indentation is also how nested list prose is written, and masking real
    # sentences is worse than missing a tell inside a snippet.
    text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", _blank, text, flags=re.S | re.M)
    # Inline code
    text = re.sub(r"`[^`\n]+`", _blank, text)
    # Link and image targets, keeping the visible label
    text = re.sub(r"(\[[^\]]*\])\([^)\n]*\)",
                  lambda m: m.group(1) + " " * (len(m.group(0)) - len(m.group(1))),
                  text)
    # Bare URLs
    text = re.sub(r"<?https?://\S+>?", _blank, text)
    return text


def blockquote_lines(text):
    """Line numbers that sit inside a blockquote."""
    return {i for i, line in enumerate(text.split("\n"), 1)
            if line.lstrip().startswith(">")}


QUOTE_SPAN = re.compile(r'"[^"\n]{2,400}"|“[^”\n]{2,400}”|«[^»\n]{2,400}»')


def quoted_spans(text):
    """Character ranges inside inline quotation marks.

    Somebody else's words are not the writer's problem. A quoted "solución
    integral" stays exactly as it was said, so findings that land inside a
    quotation get tagged rather than dropped: the agent still sees them and
    decides.
    """
    return [(m.start(), m.end()) for m in QUOTE_SPAN.finditer(text)]


# ---------------------------------------------------------------------------
# Language
# ---------------------------------------------------------------------------

ES_MARKERS = re.compile(r"\b(de|la|que|el|en|los|del|las|para|con|por|una|más|como)\b", re.I)
EN_MARKERS = re.compile(r"\b(the|of|and|to|in|is|for|that|with|are|this|from)\b", re.I)


def detect_language(text):
    es = len(ES_MARKERS.findall(text))
    en = len(EN_MARKERS.findall(text))
    if es == en == 0:
        return "en"
    return "es" if es >= en else "en"


# ---------------------------------------------------------------------------
# Phrase catalogs
#
# Each entry is (label, pattern). Patterns are matched case insensitively. Keep
# these to phrases that are almost always a tell: anything ambiguous belongs in
# the reference docs where a human reads it in context, not in a linter.
# ---------------------------------------------------------------------------

ES_PHRASES = [
    ("apertura de catálogo", r"en (el|un) (vertiginoso|cambiante|competitivo) (mundo|panorama|entorno)"),
    ("apertura de catálogo", r"en (la era digital|un mundo cada vez más|el mundo de hoy)"),
    ("apertura de catálogo", r"\bhoy en día\b"),
    ("evita el verbo ser", r"se (posiciona|consolida|erige|perfila|sitúa) como"),
    ("meta-comentario", r"(cabe (destacar|mencionar|señalar)|es importante (destacar|mencionar|señalar)|vale la pena (destacar|mencionar|señalar))"),
    ("calco no solo/sino", r"no (solo|sólo|se trata solo de|es solo)\b[^.\n]{0,80}\bsino"),
    ("verbo inflado", r"\b(revolucion(a|ar|ando)|transform(a|ar|ando) la (manera|forma)|potenci(a|ar|ando)|empoder(a|ar|ando))\b"),
    ("sustantivo comodín", r"\b(solución integral|herramienta poderosa|experiencia única|propuesta de valor|abanico de posibilidades|pilar fundamental|en constante evolución|a la vanguardia)\b"),
    ("adjetivo comodín", r"\b(innovador(a|es|as)?|disruptiv[oa]s?|robust[oa]s?|memorable|de vanguardia)\b"),
    ("gancho de marketing", r"\b(sumérgete|descubre cómo|prepárate para|lleva tu \w+ al siguiente nivel|¿estás list[oa])"),
    ("cierre vacío", r"\b(en resumen|en conclusión|en definitiva|en síntesis|sin duda alguna|el futuro (es|se ve) prometedor)\b"),
    ("fuente vaga", r"\b(los expertos (coinciden|afirman|señalan)|diversos estudios|según informes del sector|está demostrado que)\b"),
    ("burocratismo", r"\b(el mismo|la misma) (contiene|permite|incluye|se|es)\b"),
    ("burocratismo", r"\b(con el fin de|mediante el uso de|a través de la cual|en el marco de|a nivel de)\b"),
    ("falso rango", r"\bdesde\b[^.\n]{0,60}\bhasta\b[^.\n]{0,60}\bpasando por\b"),
    ("gerundio de posterioridad", r",\s*(permitiendo|logrando|garantizando|generando|brindando|impulsando|consolidando|posicionando|fortaleciendo|asegurando|reflejando|destacando|ofreciendo)\b"),
]

# Checked with a threshold: one of these is ordinary writing, four is a cadence.
ES_PILEUPS = [
    ("conector de apertura", r"(?:^|(?<=[.!?»])\s)(Además|Asimismo|Por otro lado|En este sentido|Dicho esto|No obstante|Por consiguiente|Por su parte|En efecto),", 3),
]

EN_PHRASES = [
    ("inflated importance", r"\b(stands as|serves as|is a testament to|plays a (vital|crucial|pivotal|key) role|underscor\w+ the importance|marking a (pivotal|significant) (moment|shift)|evolving landscape|indelible mark)\b"),
    ("sales language", r"\b(boasts|nestled|in the heart of|breathtaking|must-visit|groundbreaking|renowned for its|commitment to excellence)\b"),
    ("vague source", r"\b(industry reports (suggest|indicate)|experts (agree|argue|say)|observers have noted|studies have shown that)\b"),
    ("stock section", r"\b(despite (its|these) (success|challenges)|future outlook|challenges and legacy)\b"),
    ("not X but Y", r"\bit'?s not (just|merely|only) (a|an|about)\b[^.\n]{0,60},? it'?s\b"),
    ("false depth", r"\b(the real question is|at its core|what really matters|the heart of the matter)\b"),
    ("announcing", r"\b(let'?s (dive|explore|break this down)|here'?s what you need to know|without further ado|now let'?s look at)\b"),
    ("fake candor", r"(^|[.!?]\s)(Honestly\?|Look,|Here'?s the thing|Let'?s be honest|Real talk)"),
    ("unraised objection", r"\b(don'?t get me wrong|to be clear,|this isn'?t (really|mainly) about|i'?m not (saying|arguing))\b"),
    ("fake alternative", r"\b(a tempting (approach|option) would be|one might be tempted to|it would be easy to just)\b"),
    ("chatbot residue", r"\b(i hope this helps|let me know if|would you like me to|great question|you'?re absolutely right)\b"),
    ("cutoff disclaimer", r"\b(as of my last (update|training)|while specific details are (not|limited)|based on available information|maintains a low profile)\b"),
    ("filler", r"\b(in order to|due to the fact that|at this point in time|it is important to note that|has the ability to)\b"),
    ("hedge stack", r"\b(could potentially|might arguably|it'?s also possible that)\b"),
    ("generic ending", r"\b(the future looks bright|exciting times (lie )?ahead|a step in the right direction)\b"),
]

EN_PILEUPS = [
    ("overused word", r"\b(delve|tapestry|interplay|showcase[sd]?|foster(ing|s)?|underscore[sd]?|pivotal|vibrant|crucial|intricate|garner(ed|s)?|enduring)\b", 3),
    ("opening connector", r"(?:^|(?<=[.!?”])\s)(Additionally|Moreover|Furthermore|Consequently|However|Notably),", 3),
]

EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF⬀-⯿️]"
)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

class Report:
    """Findings grouped by title.

    Several patterns share one label on purpose (a catalog opening has half a
    dozen shapes), so add() merges into an existing section instead of printing
    the same heading three times.
    """

    def __init__(self):
        self.order = []
        self.data = {}
        self.high = 0

    def add(self, title, hits, note=None, severity="high", min_hits=1):
        # min_hits encodes the rule the reference docs repeat: one "however" is
        # not a tell, a pile of them is. Below the threshold we stay quiet
        # rather than sending the agent to rewrite an innocent sentence.
        if len(hits) < min_hits:
            return
        if title not in self.data:
            self.order.append(title)
            self.data[title] = [[], note, severity]
        self.data[title][0].extend(hits)
        if note and not self.data[title][1]:
            self.data[title][1] = note
        if severity == "high":
            self.high += len(hits)

    def render(self):
        if not self.order:
            return "No mechanical tells found.\n"
        out = []
        for title in self.order:
            hits, note, severity = self.data[title]
            hits = sorted(hits, key=lambda h: h[0])
            marker = "!" if severity == "high" else "-"
            out.append(f"{marker} {title} ({len(hits)})")
            if note:
                out.append(f"    {note}")
            for line_no, snippet, tag in hits[:MAX_EXAMPLES]:
                suffix = f"  [{tag}]" if tag else ""
                out.append(f"    L{line_no}: {snippet}{suffix}")
            if len(hits) > MAX_EXAMPLES:
                out.append(f"    ... and {len(hits) - MAX_EXAMPLES} more")
            out.append("")
        return "\n".join(out)


CONTEXT = 30  # characters of surrounding line shown around a match


def find_pattern(text, pattern, quoted, flags=re.I, spans=()):
    """Return (line, snippet, tag) for every match.

    The snippet shows the matched text between guillemets with a little context
    around it. Showing the whole line is useless when a paragraph trips five
    different rules and every finding prints the same eighty characters.
    """
    line_starts = [0]
    for i, char in enumerate(text):
        if char == "\n":
            line_starts.append(i + 1)
    lines = text.split("\n")

    hits = []
    for match in re.finditer(pattern, text, flags):
        line_no = text.count("\n", 0, match.start()) + 1
        line = lines[line_no - 1]
        col = match.start() - line_starts[line_no - 1]
        matched = match.group(0).strip()
        before = line[max(0, col - CONTEXT):col].lstrip()
        after = line[col + len(match.group(0)):col + len(match.group(0)) + CONTEXT].rstrip()
        prefix = "..." if col - CONTEXT > 0 else ""
        suffix = "..." if col + len(match.group(0)) + CONTEXT < len(line) else ""
        snippet = f"{prefix}{before}[[{matched}]]{after}{suffix}".strip()
        in_quote = line_no in quoted or any(s <= match.start() < e for s, e in spans)
        hits.append((line_no, snippet, "in quote, probably leave it" if in_quote else None))
    return hits


# Function words that give Title Case away instantly when capitalized mid-heading.
CONNECTORS = {"y", "e", "o", "u", "de", "del", "la", "el", "los", "las", "en", "para",
              "con", "por", "un", "una", "al", "the", "of", "and", "in", "for", "to",
              "a", "an", "on", "at", "or", "with"}


def check_headings(text, quoted):
    """Title Case headings. Spanish and English both want sentence case here."""
    hits = []
    for line_no, line in enumerate(text.split("\n"), 1):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not m:
            continue
        rest = re.findall(r"[A-Za-zÁÉÍÓÚÑÜáéíóúñü']+", m.group(2))[1:]
        if not rest:
            continue
        # A capitalized connector is decisive: "Desafíos Y Oportunidades",
        # "Resultados Del Trimestre". Proper nouns never look like this.
        if any(w[0].isupper() and w.lower() in CONNECTORS for w in rest):
            hits.append((line_no, line.strip(), None))
            continue
        content = [w for w in rest if len(w) > 3 and w.lower() not in CONNECTORS]
        if len(content) >= 2 and sum(1 for w in content if w[0].isupper()) / len(content) >= 0.6:
            hits.append((line_no, line.strip(), None))
    return hits


def check_opening_marks(text, quoted, spans):
    """Spanish questions and exclamations that never opened.

    Works per sentence rather than per line, so "Hola. ¿Cómo estás?" stays clean
    while "Como funciona?" on the same line still gets caught.
    """
    hits = []
    pos = 0
    for line_no, line in enumerate(text.split("\n"), 1):
        for chunk in re.finditer(r"[^\n.?!]{0,120}[?!](?!\[)", line):
            body = chunk.group(0)
            if "¿" in body or "¡" in body:
                continue
            in_quote = line_no in quoted or any(s <= pos + chunk.start() < e for s, e in spans)
            snippet = body.strip()
            if len(snippet) > 70:
                snippet = "..." + snippet[-67:]
            hits.append((line_no, f"[[{snippet}]]",
                         "in quote, probably leave it" if in_quote else None))
        pos += len(line) + 1
    return hits


def sentence_stats(text):
    """Mean and spread of sentence length in words.

    Human prose alternates short and long sentences and LLM prose tends toward an
    even mid-length cadence, but the overlap is wide. Treat this as one weak
    signal among many, never as evidence on its own.
    """
    prose = re.sub(r"^\s*[#>|].*$", "", text, flags=re.M)  # drop headings, quotes, tables
    parts = [s.strip() for s in re.split(r"(?<=[.!?…])\s+", prose) if s.strip()]
    lengths = [len(re.findall(r"[\w'’-]+", s)) for s in parts]
    lengths = [n for n in lengths if n >= 3]
    if len(lengths) < 5:
        return None
    return statistics.mean(lengths), statistics.pstdev(lengths), len(lengths)


def word_count(text):
    return len(re.findall(r"[\w'’-]+", text))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def analyze(path, lang=None, original=None):
    raw = Path(path).read_text(encoding="utf-8")
    text = mask_uncheckable(raw)
    quoted = blockquote_lines(raw)
    lang = lang or detect_language(text)

    report = Report()
    spans = quoted_spans(text)

    def scan(pattern, flags=re.I):
        return find_pattern(text, pattern, quoted, flags=flags, spans=spans)

    report.add("Em and en dashes", scan(r"[—–]"),
               "Replace with a comma, colon, period or parentheses.")
    report.add("Double hyphen used as a dash", scan(r"\S\s--\s\S"))
    report.add("Curly double quotes", scan(r"[“”]"),
               "Only a tell alongside others. Switch to straight quotes if the document uses them.",
               severity="low")
    report.add("Emoji", scan(EMOJI.pattern, flags=0))
    report.add("Title Case headings", check_headings(text, quoted),
               "Use sentence case. Spanish capitalizes only the first word and proper nouns.")
    # The colon lands inside or outside the bold depending on who wrote it.
    report.add("List items with a bold label",
               scan(r"^\s*[-*+]\s+\*\*[^*\n]{1,60}\*\*\s*:|^\s*[-*+]\s+\*\*[^*\n]{1,60}:\s*\*\*", flags=re.M),
               "Usually a paragraph in disguise. Consider writing it as prose.")
    report.add("Exclamation marks", scan(r"!(?!\[)"),
               "One per document is usually one more than needed.", severity="low", min_hits=2)

    if lang == "es":
        for label, pattern in ES_PHRASES:
            report.add(f"ES: {label}", scan(pattern, flags=re.I | re.M))
        for label, pattern, threshold in ES_PILEUPS:
            report.add(f"ES: {label}", scan(pattern, flags=re.M),
                       "Uno solo no es señal. Varios seguidos son ritmo de modelo.",
                       min_hits=threshold)
        report.add("ES: español peninsular",
                   scan(r"\b(vosotros|vuestr[oa]s?|ordenador(es)?|zumo|coger|alquiler)\b|\b(el|un|los|mi|tu|su)\s+móvil(es)?\b"),
                   "Para un lector chileno: ustedes, computador, jugo, tomar, arriendo, celular.")
        report.add("ES: falta signo de apertura", check_opening_marks(text, quoted, spans),
                   "En español ¿ y ¡ son obligatorios.")
        report.add("ES: coma antes de y/o", scan(r",\s+(y|o|e|u)\s+\w"),
                   "El español no lleva coma serial al cerrar una enumeración. Revisa cada caso: entre oraciones independientes sí es correcta.",
                   severity="low")
        report.add("ES: formato de cifras en inglés", scan(r"\b\d{1,3},\d{3}\b"),
                   "En español el punto separa miles y la coma decimales: 42.000 y 3,5x.")
    else:
        for label, pattern in EN_PHRASES:
            report.add(f"EN: {label}", scan(pattern, flags=re.I | re.M))
        for label, pattern, threshold in EN_PILEUPS:
            report.add(f"EN: {label}", scan(pattern, flags=re.M),
                       "One is ordinary writing. Several in a row is the tell.",
                       min_hits=threshold)

    print(f"File: {path}")
    print(f"Language detected: {lang}")

    words = word_count(text)
    if original:
        src = word_count(mask_uncheckable(Path(original).read_text(encoding="utf-8")))
        delta = words - src
        pct = (delta / src * 100) if src else 0
        verdict = "OK, shorter" if delta < 0 else "PROBLEM, the rewrite grew"
        print(f"Words: {src} -> {words} ({delta:+d}, {pct:+.0f}%)  {verdict}")
        if delta >= 0:
            report.high += 1
    else:
        print(f"Words: {words}")

    stats = sentence_stats(text)
    if stats:
        mean, spread, n = stats
        flag = "  <- worth a look, the rhythm is even" if spread < 3.5 and n >= 10 else ""
        print(f"Sentences: {n}, mean {mean:.1f} words, stdev {spread:.1f}{flag}")

    gaps = re.findall(r"\[(?:falta dato|revisar)[^\]]*\]", text, re.I)
    if gaps:
        print(f"Gap markers left for the user: {len(gaps)}")
        for gap in gaps[:MAX_EXAMPLES]:
            print(f"    {gap}")

    print()
    print(report.render())
    return report.high


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="the rewritten file to check")
    parser.add_argument("--original", help="the source file, to compare word counts")
    parser.add_argument("--lang", choices=["es", "en"], help="override language detection")
    parser.add_argument("--strict", action="store_true", help="exit 1 when a high severity tell is found")
    args = parser.parse_args()

    high = analyze(args.file, lang=args.lang, original=args.original)
    if args.strict and high:
        sys.exit(1)


if __name__ == "__main__":
    main()
