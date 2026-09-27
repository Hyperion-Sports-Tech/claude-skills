#!/usr/bin/env python3
"""Offline package/contract checks, not an evaluation of decision quality."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def text(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


class CouncilPackageTests(unittest.TestCase):
    def test_frontmatter_and_discovery_prefix(self):
        skill = text("SKILL.md")
        self.assertTrue(skill.startswith("---\nname: multi-agent-council\n"))
        self.assertIn("version: 2.0.0", skill.split("---", 2)[1])
        first_sentence = skill.split("description: >\n", 1)[1].splitlines()[0].strip()
        self.assertTrue(first_sentence.startswith("Use when "))
        self.assertLessEqual(len(first_sentence), 57)

    def test_role_index_covers_exactly_role_files(self):
        index = text("references/roles-index.md")
        table = index.split("## All Roles", 1)[1].split("## Composition Heuristics", 1)[0]
        indexed = {line.split("|")[1].strip() for line in table.splitlines()
                   if line.startswith("| ") and not line.startswith("| Role ")}
        files = list((ROOT / "references/roles").glob("*.md"))
        titles = {p.read_text().splitlines()[0].removeprefix("# ") for p in files}
        self.assertEqual(len(titles), len(files), "duplicate role titles")
        self.assertEqual(indexed, titles)
        for p in files:
            with self.subTest(role=p.name):
                content = p.read_text()
                self.assertEqual(content.count("**Value function:**"), 1)
                for section in ("**Natural tension with:**", "## Lens", "## Research directives"):
                    self.assertIn(section, content)

    def test_pattern_index_covers_exactly_pattern_files(self):
        table = text("references/patterns-index.md").split("## All Patterns", 1)[1].split("## Core Patterns", 1)[0]
        rows = [line.split("|") for line in table.splitlines() if line.startswith("| ")
                and not line.startswith("| Pattern ")]
        indexed = {row[1].strip() for row in rows}
        titles = {p.read_text().splitlines()[0].removeprefix("# ")
                  for p in (ROOT / "references/patterns").glob("*.md")}
        self.assertEqual(indexed, titles)
        self.assertEqual(sum(row[2].strip() == "Core" for row in rows), 3)
        self.assertEqual(sum(row[2].strip() == "Modifier" for row in rows), 5)

    def test_all_package_reference_paths_exist(self):
        documents = [ROOT / "SKILL.md", *sorted((ROOT / "references").rglob("*.md"))]
        checked = 0
        for document in documents:
            for relative in re.findall(r"`(references/[a-zA-Z0-9_./*\-]+\.md)`", document.read_text()):
                with self.subTest(document=document.name, reference=relative):
                    self.assertTrue(list(ROOT.glob(relative)), relative)
                    checked += 1
        self.assertGreater(checked, 15)

    def test_deliberator_template_renders_for_each_backend(self):
        template = text("references/deliberator-prompt.md")
        fields = set(re.findall(r"\[([A-Z_]+)\]", template))
        expected = {"ROLE_NAME", "VALUE_FUNCTION", "ROLE_LENS", "RESEARCH_DIRECTIVES",
                    "GOAL", "CONTEXT", "ROUND", "ROUND_STATE", "BOUNDARIES", "DELIVERY", "BUDGET"}
        self.assertEqual(fields, expected)
        contracts = {
            "hermes-native": "Return assigned round as final output to the parent.",
            "claude-interactive": "Print assigned round and TEST_R2_DONE; wait for the next directive.",
            "claude-native": "Return assigned round through the available Agent result.",
            "export": "Return the assigned paper to the human operator.",
        }
        for backend, delivery in contracts.items():
            with self.subTest(backend=backend):
                values = {field: "Fixture value for " + field for field in expected}
                values.update(ROUND="2", ROUND_STATE="Own prior paper plus peer digest and checkpoint delta.",
                              DELIVERY=delivery, BOUNDARIES="Read-only supplied packet; no tools.",
                              BUDGET="One bounded response; no research tools; telemetry unavailable.")
                rendered = re.sub(r"\[([A-Z_]+)\]", lambda m: values[m[1]], template)
                self.assertIsNone(re.search(r"\[[A-Z_]+\]", rendered))
                for foreign_api in ("TeamCreate", "SendMessage", "[MODE]", "[TOKEN_BUDGET]"):
                    self.assertNotIn(foreign_api, rendered)

    def test_patterns_do_not_hardcode_transport(self):
        for p in (ROOT / "references/patterns").glob("*.md"):
            with self.subTest(pattern=p.name):
                content = p.read_text()
                for stale in ("Path A", "Path B", "SendMessage", "`Agent` tool", "[TOKEN_BUDGET]"):
                    self.assertNotIn(stale, content)

    def test_truthful_usage_and_round_contract(self):
        prompt = text("references/deliberator-prompt.md")
        for expected in ("unavailable", "reasoning correction", "abstain", "Counterevidence", "Evidence ledger"):
            self.assertIn(expected, prompt)
        self.assertNotIn("Track your own consumption", prompt)
        backend = text("references/execution-backends.md")
        for expected in ("dispatch NEW children", "own previous paper in full", "asynchronous",
                         "do not poll child transcripts", "does NOT consume a Claude Max"):
            self.assertIn(expected.lower(), backend.lower())

    def test_interactive_lifecycle_and_subscription_boundaries(self):
        backend = text("references/execution-backends.md")
        for expected in ("background=true, pty=true", "--restricted", "--strict-mcp-config",
                         "--tools 'Read,Glob,Grep'", "initial prompt echo", "SEPARATE `\\r`",
                         "verify process exit", "--bare", "never extract OAuth tokens"):
            self.assertIn(expected.lower(), backend.lower())

    def test_judge_independence_and_failure_semantics(self):
        judge = text("references/patterns/judge.md")
        for expected in ("Before inspecting any Judge output, freeze", "cannot flag defects in a draft it never saw",
                         "provisional analysis", "not shipping software", "exactly one", "one-round council"):
            self.assertIn(expected, judge)
        self.assertNotIn("order does not matter", judge)

    def test_hyperion_and_simulation_boundaries(self):
        recipe = text("references/business-and-knowledge.md")
        for expected in ("wiki/CLAUDE.md", "wiki/SCHEMA.md", "wiki/index.md", "wiki/log.md",
                         "records/", "Linear", "Attio", "change preview", "explicit approval",
                         "user-confirmed speaker", "single-agent baseline", "not an observation"):
            self.assertIn(expected, recipe)
        self.assertIn("SIMULATION — not customer evidence", text("references/patterns/stakeholder-sim.md"))

    def test_legacy_eval_file_remains_valid_but_is_not_v2_contract(self):
        legacy = ROOT / "evals/evals.json"
        if legacy.exists():
            self.assertIsInstance(json.loads(legacy.read_text())["evals"], list)
        self.assertIn("not executed", text("references/evaluation.md"))

    def test_behavioral_fixture_coverage(self):
        fixture = json.loads(text("scripts/behavioral-cases.json"))
        self.assertEqual(fixture["status"], "not_executed")
        cases = fixture["cases"]
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        required = {"trivial", "export", "single-risk", "absent-user", "native-round-2", "marker-echo",
                    "quota-block", "missing-agent", "wiki-conflict", "persona-pricing", "judge-leak", "reasoning-correction"}
        self.assertEqual({case["id"] for case in cases}, required)
        for case in cases:
            self.assertTrue(case["prompt"] and case["must"] and case["must_not"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
