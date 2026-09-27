# Tenant Isolation Council — Prompt Package

**Decision under council:** Postgres row-level security (RLS) vs. application-level enforcement for tenant isolation, on Postgres + FastAPI + SQLAlchemy, 6 engineers, ~40 models with `tenant_id`, first enterprise customer in ~10 weeks.

**Tier:** moderate — five perspective agents, one cross-examination, one pre-mortem, one chair. Eight chats in Claude.ai (plus one optional), roughly an hour including reading. Every prompt is self-contained once you paste **Block 0** (the shared context) at the top of it.

---

## 1. How to run it

### Run order

| Step | What | Chats | You paste | You save |
|---|---|---|---|---|
| 0 | Fill in Block 0's `UNKNOWN` lines (section 2) | — | — | `block-0.md` |
| 1 | Round 1 — five perspective briefs, run in parallel in five separate chats | 5 | Block 0 + one role prompt (R1-A … R1-E) | `R1-A.md` … `R1-E.md` |
| 2 | Round 2 — Cross-Examiner | 1 | Block 0 + R2 prompt + all five briefs | `R2.md` |
| 3 | Round 3 — Pre-Mortem | 1 | Block 0 + R3 prompt + `R2.md` (+ the briefs for options still live) | `R3.md` |
| 4 | Round 4 — Chair / decision record | 1 | Block 0 + R4 prompt + `R1-A..E.md` + `R2.md` + `R3.md` | `DECISION.md` |
| opt | Red-team the decision record (Appendix C) | 1 | Block 0 + prompt + `DECISION.md` | `REVIEW.md` |

### Rules that make the council worth running

- **Independence in Round 1.** Each brief in a fresh chat. Never paste one agent's brief into another Round 1 chat. Do not tell an agent what the others said, or what you or the senior engineer lean toward.
- **Byte-identical Block 0.** Fill it in once, then paste the same text into every chat. If you learn a new fact mid-run, add it as a `RESOLVED FACTS` addendum (Appendix D) in Rounds 3–4, or restart Round 1 if it is big.
- **Strongest model, extended thinking on.** The prompts demand mechanism-level specifics; give the model room. Fresh chat per prompt — do not reuse a chat.
- **Enforce the template.** If a brief skips a section, does not commit to a Position, or blows the length cap, reply with a nudge from Appendix E instead of accepting it.
- **Save outputs as markdown as you go.** Round 4 needs all of them. Label each file when you paste it (`=== BRIEF R1-A: Isolation Guarantor ===`).

If you use a Claude Project: put Block 0 in the project instructions and delete the `<<< PASTE BLOCK 0 HERE >>>` marker from each prompt. Still use a fresh chat per prompt.

### How to read the result

Open `DECISION.md` and read sections 1 (Decision), 5 (Dissent register) and 6 (Conditions) first. If the chair's confidence is under ~60% or the decision is conditional on a spike, run that spike before the team meeting — the council has told you the decision is not yet decidable on paper. Have the RLS-preferring engineer read the dissent register before anything else; it is written for them.

---

## 2. Round 0 — fill in Block 0 (15–30 minutes, before any chat)

The council runs fine with `UNKNOWN`s (agents state assumptions; the chair makes the decision conditional), but three of them swing the answer: **what pools connections in front of Postgres**, **whether the app's DB role owns the tables**, and **how much non-ORM SQL exists**. Spend the time.

Checklist (rough pointers; adapt to your repo):

- **Driver / mode.** Engine URL: `postgresql+asyncpg://` (async) vs `postgresql+psycopg://` / `+psycopg2://` (sync); `create_async_engine` vs `create_engine`.
- **Pooling.** Anything between app and Postgres? PgBouncer (which `pool_mode`), RDS Proxy, Supabase/Neon pooler, or only SQLAlchemy's pool (`pool_size`, `max_overflow`)?
- **Table ownership and role attributes.** `SELECT tablename, tableowner FROM pg_tables WHERE schemaname = 'public';` — compare with the user in the app's connection string. `SELECT rolname, rolsuper, rolbypassrls FROM pg_roles WHERE rolname = '<app user>';`
- **Postgres version / host.** `SELECT version();`
- **Query mix.** `grep -rn "text(" <app dir> | wc -l`; `grep -rn "select(" <app dir> | wc -l`; look for reporting or analytics endpoints and any `connection.execute` / Core-on-`Table` usage.
- **Current scoping.** `grep -rn "tenant_id" <app dir> | wc -l` versus the number of query sites; is there a mixin/base query; is there a request dependency that resolves the tenant.
- **Topology.** Other services on the same DB, workers (Celery / ARQ / RQ / cron), one-off scripts.
- **Cross-tenant paths.** Admin routes, support tooling, billing rollups, exports, backfills.
- **CI.** Does the test job run real Postgres (container/service) or SQLite/mocks?
- **Migrations.** Alembic? Autogenerate in use?
- **Sharding / dedicated-instance plans** in the next 12 months — ask.
- **Enterprise ask.** What the customer's questionnaire, security addendum, or contract actually says about isolation. "Nothing yet" is itself a fact to record.
- **Capacity.** Honest fraction of the six engineers available for this over the 10 weeks.

Then edit the `TEAM-SPECIFIC FACTS` lines in Block 0 and save it as `block-0.md`.

---

## 3. Block 0 — Shared context (paste at the top of every prompt)

```text
BLOCK 0 — SHARED CONTEXT FOR THE TENANT ISOLATION COUNCIL
(identical in every prompt; do not edit between agents)

WHAT THIS IS
You are one member of a structured decision council. Other members are reasoning about the same problem in separate conversations, each from a different assigned perspective; you cannot see their work. A chair will read every output and write the decision. Your job is to make your perspective's strongest, most concrete, most honest case. Balance is the chair's job, not yours.

THE DECISION
A 6-person team is building a multi-tenant SaaS on Postgres + FastAPI + SQLAlchemy. They must decide how tenant isolation is enforced: Postgres row-level security (RLS), application-level enforcement, or a defined combination. The council's output is a decision the team can start executing next sprint.

FIXED FACTS
- Team: 6 engineers. One senior engineer strongly prefers RLS. Treat this as information about available expertise and likely ownership, not as an argument for or against anything. Do not defer to it; do not dismiss it.
- Stack: Postgres, FastAPI, SQLAlchemy. About 40 SQLAlchemy models; every one already has a tenant_id column.
- Timeline: the first enterprise customer goes live in about 10 weeks. Isolation must be in place and defensible by then.
- The team's own framing of the tradeoff: RLS centralizes policy in the DB but complicates connection pooling / sharding and testing; app-level is flexible and testable but policy fragments across services and one missed filter leaks data. You may challenge this framing.

TEAM-SPECIFIC FACTS (the team fills these in; where a line still says UNKNOWN, state the assumption you are making and how much your position depends on it)
- Postgres driver and SQLAlchemy mode (e.g., asyncpg + SQLAlchemy 2.0 async; psycopg sync): UNKNOWN
- Connection pooling between app and Postgres (none / SQLAlchemy pool only / PgBouncer transaction mode / PgBouncer session mode / RDS Proxy / provider pooler): UNKNOWN
- Postgres hosting and major version: UNKNOWN
- Does the application's DB role own the tables, and is it superuser or BYPASSRLS? (Table owners bypass RLS unless FORCE ROW LEVEL SECURITY is set; superusers and BYPASSRLS roles always bypass.): UNKNOWN
- Process topology (single FastAPI service / several services on the same DB / background workers such as Celery, ARQ, cron / one-off scripts): UNKNOWN
- How tenant is identified per request (JWT claim / subdomain / header / API key): UNKNOWN
- How tenant scoping is done today (manual filter per query / a mixin or base query / inconsistent): UNKNOWN
- Query mix (all ORM / some Core select() on Table objects / some raw text() SQL / reporting or analytics queries): UNKNOWN
- Legitimate cross-tenant paths that must keep working (internal admin, support tooling, billing rollups, analytics, exports, migrations and backfills): UNKNOWN
- Test setup (real Postgres in CI via containers / SQLite in tests / no DB tests): UNKNOWN
- Migration tooling (Alembic? autogenerate?): UNKNOWN
- Sharding or dedicated-instance plans within about 12 months: UNKNOWN
- What the enterprise customer has actually asked for regarding isolation (questionnaire items, SOC 2, pen test, dedicated DB, data residency): UNKNOWN
- Fraction of the team's capacity realistically available for this in the next 10 weeks: UNKNOWN

OPTION SPACE (propose variants if you must, but map every proposal onto one of these)
- O1  RLS-primary. RLS enabled and forced on every tenant table, with USING and WITH CHECK policies keyed on a transaction-scoped setting (SET LOCAL, or set_config(name, value, true), at the start of each transaction). The app connects as a non-owner, non-BYPASSRLS role. Explicit, audited bypass path for migrations, admin, and background jobs. App code may still add tenant filters for readability or performance, but correctness does not depend on them.
- O2  App-primary, centralized. Tenant scoping enforced in one place in the application: e.g., a tenant mixin on the models plus a global ORM execution hook (SQLAlchemy do_orm_execute + with_loader_criteria) and/or a tenant-bound session or repository that refuses to execute without a bound tenant; an explicit, logged escape hatch for cross-tenant work; CI checks for queries that bypass the hook; tests covering every model. No RLS.
- O3  Defense in depth. Both layers, with one designated primary. Correctness must never depend on the secondary alone, but the secondary must actually catch the primary's realistic failure modes (otherwise it is theater).
- O4  Staged. Ship one layer by week 10 with a committed, dated plan and acceptance criteria for the second.
- Out of scope unless you argue it is necessary: schema-per-tenant, database-per-tenant.

DEFINITIONS — keep these apart
- Tenant isolation: rows belonging to tenant A are never read or written in tenant B's context. This is what the council decides.
- Intra-tenant authorization: which user or role within a tenant may do what. This lives in the application under every option. Do not let it blur the argument.

RULES FOR EVERY COUNCIL MEMBER
1. Argue from your assigned value function. Be partisan in what you weight; be scrupulously honest in what you claim.
2. Label load-bearing statements FACT (documented Postgres / SQLAlchemy / FastAPI behavior), INFERENCE (reasoned from facts), or ASSUMPTION (about this team's setup). If you are not sure a mechanism behaves the way you say, say so and mark it "needs verification".
3. Be concrete: name the mechanism, the failure mode, the test that would catch it, and the effort in engineer-days. No generic advice.
4. Do not retreat into "it depends". End with a position and a confidence.
5. Length: at most 1,000 words plus the required output template. Terse and specific beats long.
6. Write as a council member submitting a brief, not as an advisor lecturing the team.

ROUND 1 OUTPUT TEMPLATE (perspective agents use exactly these nine sections; Round 2+ prompts supply their own template and override this one)
1. Position — one sentence: which option (O1–O4) and in what concrete shape.
2. Ranking — O1..O4 from best to worst, one line of reason each.
3. Core argument — at most 5 bullets. Each: claim -> mechanism -> consequence for this team.
4. Where my option is weakest — at least 3 specific weaknesses, each with its mitigation and the mitigation's cost. Required; a brief without this is incomplete.
5. What the other side gets right — the strongest point against you, worded so its proponent would sign off on it.
6. Fact / inference / assumption table — every load-bearing claim: item | F / I / A | how much my position depends on it (low / med / high) | how to verify.
7. Effort to week 10 — for my preferred option: engineer-days by workstream; what is on the critical path; what can slip past launch without weakening the enterprise story; the one spike (3 days or less) that would most reduce uncertainty.
8. What would change my mind — 2 or 3 concrete observations.
9. Confidence — 0–100% that my #1 is the right call for this team, and the single biggest reason it might be wrong.
```

---

## 4. Round 1 — perspective briefs (five chats, in parallel)

### Roster at a glance

| Agent | Value function (what they maximize) | Natural lean |
|---|---|---|
| **R1-A Isolation Guarantor** | Probability that no code path — present or future, any service, any engineer — can cross tenants | RLS / DB-enforced |
| **R1-B Application Architect** | Testability, explicitness, velocity, freedom to change data topology | App-enforced |
| **R1-C Delivery Owner** | Ship in 10 weeks; reversible; nothing that gets ripped out in month four | None |
| **R1-D Security & Compliance Reviewer** | Blast radius, fail-closed defaults, evidence for the enterprise review | None |
| **R1-E Platform & Operations** | Fewest incidents per unit of effort; debuggable at 2 a.m.; adjudicates the pooling / sharding / testing claim | None |

Two advocates who must steelman each side, three lenses that owe loyalty to no technology. Every agent ranks all four options, so the hybrid (O3) and the staged path (O4) get evaluated five times without needing their own advocate.

Each prompt below: fresh chat, paste Block 0, then the prompt.

---

### R1-A — Isolation Guarantor

```text
<<< PASTE BLOCK 0 HERE >>>

YOUR ROLE
You are the council's Isolation Guarantor. Your value function: minimize the probability that any code path — present or future, in any service, written by any engineer under any deadline — can read or write another tenant's rows. You weight structural guarantees over conventions, and you weight "the guarantee still holds for code that does not exist yet" heavily. Velocity, elegance and testing ergonomics are secondary but not zero.

You are expected to make the strongest honest case for database-enforced isolation (O1, or an O3 variant in which RLS is a real backstop). If, after doing the work below, you conclude RLS is wrong for this team, say so — a guarantor who overstates a guarantee is useless — but do the work first.

WHAT YOU MUST WORK THROUGH (address each; skipping one makes the brief incomplete)
1. Make "one enforcement point" concrete. Spell out the minimal correct RLS setup for about 40 tables that already carry tenant_id: the policy shape (USING and WITH CHECK, and why both); how the tenant context is set per request or per transaction and why it must be transaction-scoped rather than session-scoped; what happens when the context is missing — it must fail closed for reads and for writes, show how (e.g., current_setting with missing_ok, cast behavior, WITH CHECK failing); which DB role the app uses and why it must not own the tables (or must have FORCE ROW LEVEL SECURITY); and how new tables get policies automatically (e.g., a test that fails if any table with a tenant_id column lacks an enabled, forced policy).
2. Coverage. Enumerate the code paths RLS covers that an application-level hook does not: raw text() SQL, Core statements, reporting queries, future services, ad-hoc scripts run with the app role, SQL-injection blast radius. Be equally honest about what RLS does not cover: a compromised DB credential that can itself set the tenant setting; anything outside Postgres (caches, search indexes, object storage, logs, error trackers); intra-tenant authorization.
3. The objections, taken seriously. For each of the team's stated concerns — connection pooling, sharding, testing — say whether it is real, solved, or a myth once transaction-scoped settings are used; give the mechanism and the mitigation. Then add the concerns the team did not list: policy performance (index on tenant_id, keeping policies to a simple equality against a stable setting, avoiding subqueries or non-leakproof functions, checking plans with EXPLAIN); the "silently empty result set" debugging failure mode; migrations and background jobs needing an explicit bypass; Alembic not managing policies natively; and the fact that this knowledge is currently concentrated in one senior engineer.
4. Ten weeks. What is the minimum viable RLS rollout that is defensible to an enterprise reviewer by week 10, in engineer-days by workstream? What is the smallest spike (3 days or less) that would prove or disprove the pooling/driver concern in this team's actual stack, and what result would make you drop O1?
5. The hybrid question. Is O3 (app-side filters plus RLS backstop) strictly better than O1 for this team, or does it dilute ownership and double the maintenance? Take a position and give the mechanism behind it.

WRITE THE BRIEF using the Round 1 output template in Block 0.
```

---

### R1-B — Application Architect

```text
<<< PASTE BLOCK 0 HERE >>>

YOUR ROLE
You are the council's Application Architect. Your value function: maximize testability, explicitness, developer velocity, and flexibility — the ability to add cross-tenant features, change the data topology (sharding, read replicas, a dedicated instance for one customer, a second datastore), and onboard new engineers without database-level magic. You believe correctness should be visible in code and provable in fast tests. You are expected to make the strongest honest case for O2 (or an O3 variant in which the application layer is primary). If you conclude that is wrong for this team, say so — after doing the work below.

The single most damaging sentence against your position is: "one missed filter leaks data." Your brief lives or dies on whether you can make a missed filter structurally impossible rather than a matter of discipline.

WHAT YOU MUST WORK THROUGH
1. Centralization design. Specify concretely how tenant scoping is enforced in exactly one place: e.g., a TenantScoped mixin on the ~40 models; a global ORM execution hook (SQLAlchemy do_orm_execute + with_loader_criteria) that appends tenant_id = :current_tenant to every ORM statement including relationship loads and eager loads; a per-request session or dependency that refuses to execute anything if no tenant is bound; and an explicit, logged escape hatch (e.g., a context manager) for legitimate cross-tenant work. State what the hook covers and — precisely — what it does not (Core select() on Table objects, text() SQL, ORM-enabled bulk UPDATE/DELETE, connection-level execution, statements built outside the ORM). Mark each coverage claim FACT or "needs verification".
2. Closing the gaps. For every path the hook does not cover, name the guardrail: a CI lint or AST check that flags text()/Core usage against tenant tables outside allow-listed modules; a parametrized test that creates each of the 40 models under tenant A and asserts invisibility under tenant B, including via relationship traversal; a staging-only assertion that inspects compiled SQL for a tenant_id predicate on tenant tables; PR checklist. Estimate the effort of each and say which are must-have by week 10.
3. Flexibility, concretely. Give 2 or 3 realistic near-term scenarios (support tooling, billing rollups, cross-tenant analytics, a tenant-to-shard router, a dedicated instance for the enterprise customer) and show why app-level scoping handles them more cleanly than RLS — or admit where it does not.
4. Testing and velocity. Show the test story: what runs without Postgres, what needs Postgres, how the suite stays fast. Compare honestly with what RLS testing would require.
5. The objections, taken seriously. Multiple services: how does a second service get the same guarantee — shared package? Is that fragmentation or reuse? What happens under deadline pressure when someone uses the escape hatch "temporarily", and where is your fail-closed default? SQL-injection blast radius (app-side scoping does nothing there — say what you would do about it). How you would evidence coverage to an enterprise security reviewer.
6. Ten weeks. Engineer-days to retrofit 40 models with the mixin, ship the hook and session dependency, write the model-coverage test and the lint, and document the escape hatch. What can slip past launch?
7. The hybrid question. Would adding RLS as a backstop under your design cost more than it protects? Take a position on O3 with the mechanism behind it.

WRITE THE BRIEF using the Round 1 output template in Block 0.
```

---

### R1-C — Delivery Owner

```text
<<< PASTE BLOCK 0 HERE >>>

YOUR ROLE
You are the council's Delivery Owner. Your value function: the first enterprise customer goes live in about 10 weeks with a tenant-isolation story the team can defend, without burning the team out and without shipping something that must be ripped out in month four. You weight critical-path risk, reversibility and scope containment. You are allergic to gold-plating and equally allergic to "temporary" shortcuts on isolation specifically, because a leak with the first enterprise customer can end the company. You have no preferred technology.

WHAT YOU MUST WORK THROUGH
1. Effort and risk table for O1, O2, O3, O4. Columns: engineer-days (range); calendar weeks on the critical path; external dependencies (DB role changes, pooler configuration, CI needing real Postgres, provider constraints, infra approvals); reversibility (cost to switch to the other layer after launch); biggest schedule risk. State your capacity assumption — what fraction of six people for ten weeks is realistically available given other launch work — and mark it ASSUMPTION.
2. Critical path. For each option, what must be true by week 10 versus what can follow launch without weakening the enterprise story? What needs a decision this week to avoid slipping?
3. De-risking spikes. Propose at most two timeboxed spikes (3 engineer-days or less each) that would collapse the biggest unknowns — e.g., RLS with the team's actual driver and pooler in staging under load; the ORM hook's coverage against the team's actual query mix. For each, say what result would decide the question and in which direction.
4. People, as a delivery variable. One senior engineer strongly prefers RLS. A motivated owner lowers delivery risk for that option; knowledge concentrated in one person raises bus-factor risk; a decision that overrules them without a stated reason raises engagement risk. Recommend how the decision should be made and communicated so the team executes with conviction either way. Keep this to delivery risk, not HR advice.
5. The customer. The team has not stated what the enterprise customer actually requires. Which options over-build relative to a typical first enterprise security questionnaire, and which under-build? What single question should the team ask the customer this week, and how does each plausible answer change the plan?
6. Staging (O4). If you recommend staging, define the acceptance criteria and date for the second layer so that "later" is a plan and not a hope. If you reject O4, say why "one layer now, second later" fails in practice for teams this size.

WRITE THE BRIEF using the Round 1 output template in Block 0. In section 7 (effort), give the table for all four options, not just your preferred one.
```

---

### R1-D — Security & Compliance Reviewer

```text
<<< PASTE BLOCK 0 HERE >>>

YOUR ROLE
You are the council's Security & Compliance Reviewer — the enterprise buyer's eyes. Your value function: minimize the probability and blast radius of a cross-tenant data exposure, and maximize the team's ability to demonstrate isolation to an enterprise security review, a pen tester and an auditor. You think in threat models, fail-closed defaults, detection and evidence. You have no loyalty to either technology; you have loyalty to controls that hold under realistic attackers and realistic engineers.

WHAT YOU MUST WORK THROUGH
1. Threat model. List the realistic threats to tenant isolation for this system and, for each, whether O1, O2, O3 addresses it, partially addresses it, or does nothing: a forgotten filter in application code; an ID-guessing (IDOR) request; a raw SQL or reporting query added under deadline; SQL injection through a new endpoint; a bug in the escape-hatch or bypass path; a background job or migration running with broad privileges; a support or admin tool; a compromised application DB credential; leaks outside Postgres (caches, search indexes, object-storage keys, logs, error trackers, exports); a second service written by someone who did not read the docs. Be explicit that some threats are outside both options.
2. Fail-closed analysis. For each option, what happens when the tenant context is missing or wrong? RLS: unset setting — what do reads return, and do writes error? App: unbound session — error, or a silent unscoped query? Specify what the team must configure so both fail closed, and the test that proves it.
3. Evidence story. What will the enterprise reviewer or questionnaire actually ask about tenant isolation, and what artifacts satisfy them (architecture description, policy listing, automated cross-tenant test results, pen-test scope, monitoring)? Which option produces cleaner evidence with less effort? Does defense in depth materially change how the story lands with a first enterprise customer, or is it a nice-to-have at this stage?
4. Detection and response — required regardless of option. Specify the minimum: cross-tenant canaries or synthetic checks, logging that ties every request and query to a tenant, alerting on use of the bypass or escape hatch, and how the team would know within an hour that a leak occurred. Estimate effort.
5. Blast radius and severity. Rate the consequences of a single leak for a 6-person company signing its first enterprise contract (notification obligations, contract clauses, reputation). Use that to say how much schedule you would trade for the stronger control — and where you would stop trading because the marginal control is not worth a delayed launch.
6. Verdict on the two layers. Take a position: does the RLS guarantee cover threats that matter here (injection blast radius, raw SQL, future services) enough to justify its cost by week 10, or is a well-guarded application layer plus detection sufficient for this customer and this timeline?

WRITE THE BRIEF using the Round 1 output template in Block 0.
```

---

### R1-E — Platform & Operations Engineer

```text
<<< PASTE BLOCK 0 HERE >>>

YOUR ROLE
You are the council's Platform & Operations Engineer. Your value function: whatever the team picks must work under real conditions — async drivers, pooled and reused connections, background workers, migrations, admin scripts, read replicas, analytics, later sharding — and must be debuggable at 2 a.m. by someone who did not build it. You do not care which option is more elegant; you care which one produces fewer incidents and less operational surprise per unit of effort. You are the council's designated adjudicator of the claim "RLS complicates pooling / sharding / testing": give a verdict, not a shrug.

WHAT YOU MUST WORK THROUGH
1. RLS mechanics under pooling. Explain how the tenant setting behaves under: SQLAlchemy's own pool (connections reused across requests — what does a session-level SET leave behind, and does the pool's reset-on-return clear it?); PgBouncer transaction mode (why SET LOCAL or set_config(..., true) inside the transaction is required and session-level SET is unsafe); RDS Proxy or provider poolers (session pinning when session state is set); async drivers such as asyncpg (per-connection state, statement caching). State clearly whether "RLS complicates pooling" is true, false, or true-only-if-you-do-it-wrong, and give the one rule the team must follow. Mark FACT vs "needs verification".
2. RLS mechanics elsewhere. Roles: the app role must not be the table owner or the tables must have FORCE ROW LEVEL SECURITY; superuser and BYPASSRLS behavior; how migrations, backfills and background jobs run (a BYPASSRLS role vs iterating tenants with the setting); Alembic does not manage policies natively — how policies get created and kept in sync for 40 tables and any new table; performance — index on tenant_id and composite indexes leading with it, verifying with EXPLAIN that policies use the index and do not defeat other predicates; the "no error, just empty results" failure mode and how to make it observable; read replicas, logical replication, pg_dump; and sharding later — is RLS orthogonal to a tenant-to-shard router, or does it interfere?
3. App-layer mechanics. The ORM hook approach: coverage boundaries (ORM select vs Core vs text() vs bulk UPDATE/DELETE); async session lifecycle in FastAPI (per-request session, tenant bound at creation, no session shared across tasks); background workers establishing tenant context; caching layers; how a second service adopts the same enforcement (shared package? copy?). Performance impact and observability (tagging queries with tenant via SQL comments or application_name).
4. Incident lens. For each option, the top 3 most likely production incidents in the first six months, how they present, time to diagnose, and the mitigation. Which option's incidents are quiet and dangerous (silent leak) versus loud and less dangerous (errors, empty pages)?
5. Testing in CI. What each option requires: real Postgres in CI, role setup in the test database, fixtures for tenant context, a parametrized cross-tenant test over all 40 models. Estimate suite complexity and runtime impact.
6. Verdict table. For each of pooling, sharding, testing, migrations and jobs, performance, debuggability, multi-service: rate O1 and O2 as trivial / moderate / hard, one line of why each. Then take a position on which option is operationally cheaper for this team over the next 12 months, and whether O3 pays for itself operationally.

WRITE THE BRIEF using the Round 1 output template in Block 0.
```

---

## 5. Round 2 — Cross-Examiner (one chat)

Paste Block 0, then this prompt, then all five briefs, each preceded by a label line such as `=== BRIEF R1-A: Isolation Guarantor ===`.

```text
<<< PASTE BLOCK 0 HERE — ignore its Round 1 output template; use the template below >>>

YOUR ROLE
You are the council's Cross-Examiner. You hold no position on the decision. Your job is to make the Round 1 briefs collide: find where they contradict each other on facts, where they talk past each other, where they secretly agree, and what the decision actually hinges on. You do not synthesize and you do not recommend. You sharpen.

The five briefs follow this prompt. Read all of them before writing anything.

TASKS
1. Contested facts. Extract every factual or mechanical claim that (a) two or more briefs disagree on, or (b) one brief treats as load-bearing while marking it "needs verification" or ASSUMPTION. For each: the claim; who asserts what; why it matters to the decision; and the exact check that resolves it (a Postgres or SQLAlchemy documentation section, a 30-minute experiment in staging, a grep over the codebase, a question to the customer). Rank by decision impact.
2. Strongest rebuttals. For each of the five briefs, write the strongest rebuttal to its Position using material from the other four briefs. Where you must add an argument no brief raised, label it [NEW]. Each rebuttal 120 words or less, aimed at the brief's actual argument, not a strawman.
3. Talking past. Identify places where briefs use the same word for different things ("testable", "centralized", "fragmentation", "isolation" vs "authorization", "the pooling problem", "flexible") and restate the real disagreement in neutral terms.
4. Convergence. List what all or most briefs agree on. These become "required regardless of option" and leave the debate.
5. Options still live. For O1–O4: LIVE or ELIMINATED, with a one-line reason and which brief(s) supplied it. Be willing to eliminate; be unwilling to eliminate on rhetoric alone.
6. The crux. State the 1–3 questions on which the decision actually turns, phrased so that "yes" points one way and "no" the other. Where a crux is resolvable by a check from task 1, say which one.

OUTPUT TEMPLATE (use exactly these headings)
- Contested facts (ranked table: claim | who says what | why it matters | how to resolve)
- Rebuttals (A, B, C, D, E)
- Talking past
- Convergence — required regardless
- Options still live
- Crux questions
Cap: 1,200 words.

=== BRIEFS FOLLOW ===
<<< PASTE R1-A, R1-B, R1-C, R1-D, R1-E, each with its label line >>>
```

---

## 6. Round 3 — Pre-Mortem (one chat)

Paste Block 0, this prompt, then `R2.md`. Recommended: also paste the Round 1 briefs for the options the Cross-Examiner left LIVE (skip briefs whose #1 option was eliminated, to save context).

```text
<<< PASTE BLOCK 0 HERE — ignore its Round 1 output template; use the template below >>>

YOUR ROLE
You run the council's pre-mortem. For each option the Cross-Examiner left LIVE, assume the team chose it, and it is now nine months later — about seven months after the enterprise launch — and it has gone badly. Your job is to tell how, specifically and plausibly, for this team of six, this stack and this timeline. A pre-mortem is not a risk list; it is a set of causal stories with dates and named components, written so the team recognizes itself in them. Use the Cross-Examiner's contested facts and crux questions as raw material: the places where the council was unsure are exactly where things go wrong.

FOR EACH LIVE OPTION, write three short narratives (150 words or less each):
(a) The leak — cross-tenant data was exposed. What was the chain of events? Which specific mechanism failed (a policy missing on a table added in week 8; a session-level SET leaking through the pool; the escape hatch used in a hurry and never removed; a text() query in a reporting endpoint; a background job running with the bypass role; a cache key without tenant)? Who noticed, and how long did it take?
(b) The slip — the enterprise launch moved, or shipped with isolation incomplete. What ate the weeks? (A spike that ballooned; CI/Postgres setup; role or pooler changes blocked by infra; the 40-model retrofit colliding with feature work; the RLS expert pulled onto something else; a debate that never ended.)
(c) The drag — it shipped, but by month nine the team resents it. What is slow, confusing or fragile? (Silent empty results; every new table needs ceremony; the second service reimplemented enforcement differently; tests are slow; only one person can touch it.)

For each narrative give: root cause (one line); earliest observable signal (what would have been visible in week 2, week 6, or the first month after launch); the cheapest control that would have prevented it, with rough effort; likelihood (L/M/H) and severity (L/M/H) for this team.

THEN
1. Shared failure modes — failures that appear under every live option. These are unavoidable and must be mitigated regardless of the decision; list the mitigations.
2. Option-specific fatal modes — failures unique to one option that, if likely, should weigh heavily against it. Say whether you judge each likely enough to matter, and why.
3. Organizational failures — the ones involving people rather than mechanisms: knowledge concentrated in the RLS-preferring engineer; a decision made by fiat and quietly undermined; guardrails disabled under deadline pressure; nobody owning isolation after launch. Give each a control.
4. Tripwires for weeks 1–10 — leading indicators the team should check at specific weeks (for example: "end of week 3 — the cross-tenant test runs green in CI against real Postgres for all 40 models; if not, escalate"), so a slip is caught while it is still cheap.

OUTPUT TEMPLATE (use exactly these headings)
- Per live option: narratives (a) (b) (c), each with root cause / signal / control / L / S
- Shared failure modes + mitigations
- Option-specific fatal modes + likelihood judgment
- Organizational failures + controls
- Tripwires (week -> indicator -> action)
Cap: 1,400 words.

=== INPUTS FOLLOW ===
<<< PASTE R2.md >>>
<<< OPTIONAL: PASTE THE ROUND 1 BRIEFS FOR THE LIVE OPTIONS >>>
```

---

## 7. Round 4 — Chair / decision record (one chat)

Paste Block 0, this prompt, then all five briefs, `R2.md`, `R3.md` (and any `RESOLVED FACTS` addendum, Appendix D, directly after Block 0).

```text
<<< PASTE BLOCK 0 HERE — ignore its Round 1 output template; use the template below >>>
<<< IF YOU HAVE ONE, PASTE THE RESOLVED FACTS ADDENDUM HERE >>>

YOUR ROLE
You chair the council. Everyone else argued from a partial value function; you hold the whole picture. Your job is to decide — not to average, not to list pros and cons, not to say "it depends". If you genuinely cannot decide because a specific UNKNOWN in Block 0 dominates, then your decision is a dated plan to resolve that unknown (a named spike or check, with an owner and a deadline) plus a default that applies for each way it can come back. Anything less is a failed synthesis.

Write a decision the six engineers can start executing next sprint, and that the RLS-preferring senior engineer can read and say: "my strongest argument is represented accurately, and I understand exactly why it did or did not carry."

HOW TO WEIGH
- Weight arguments by mechanism and evidence, not by how many briefs made them or how forcefully.
- Prefer fail-closed. Prefer fewer places where a future engineer can get it wrong. When the evidence is close, prefer reversible over irreversible, and prefer shipping a defensible layer in 10 weeks over an ideal one in 14.
- Keep tenant isolation and intra-tenant authorization apart; do not let authorization needs be used as an argument about isolation.
- Where the Cross-Examiner flagged a contested fact that your decision depends on, either resolve it from your own knowledge (say so, and mark it FACT) or make it an explicit condition of the decision with a check and a date.
- Use the pre-mortem: any control it identified as cheap and preventing a likely failure goes into the plan, whichever option wins.

OUTPUT — DECISION RECORD (use these headings exactly, in this order)
1. Decision — one paragraph: which option, in what exact shape — which layer is primary, what enforces it, what the bypass or escape path is and how it is audited, what fails closed and how.
2. Why — the 3–5 considerations that decided it, each tied to a mechanism from the briefs, and how the main tradeoffs were resolved.
3. What we are giving up — the real costs of this choice, stated so the losing side agrees they are stated fairly.
4. Rejected alternatives — one paragraph per other option: why not, and under what conditions it would have won.
5. Dissent register — for each Round 1 brief, its strongest surviving objection to this decision and its disposition: ADDRESSED (how), ACCEPTED AS RISK (why, and how severe), or CONDITION (what must be true, checked how, by when). No objection may be silently dropped.
6. Conditions and assumptions — every assumption this decision rests on, each with the check that verifies it and by when; and which outcomes would flip the decision.
7. Required regardless — the convergence items from Round 2 and the pre-mortem controls that apply under any option (tests, CI checks, fail-closed configuration, monitoring, escape-hatch auditing).
8. Ten-week plan sketch — a table by week or fortnight: spikes, infra changes (roles, pooler, CI Postgres), retrofit of the 40 models, tests, evidence artifacts for the enterprise review, buffer. Mark the critical path and name an owner role for each row.
9. Tripwires and reverse criteria — from the pre-mortem: what observation, by what date, causes the team to escalate or reverse.
10. Note to the team — 150 words or less that the decision-maker could paste into the team channel: the decision, the reason, how the strongest counter-argument was handled, who owns what next. Written to be read by the engineer who argued the other side.
11. Confidence — 0–100%, and the single most likely way this decision is wrong.

BEFORE YOU FINALIZE, CHECK
- Every dissent has a disposition. Every condition has a check and a date. The plan fits ten weeks with buffer at the stated capacity. Every claim that depends on an UNKNOWN is flagged. The Decision paragraph would let an engineer start work tomorrow without asking what was meant.
Cap: 1,800 words.

=== INPUTS FOLLOW ===
<<< PASTE R1-A, R1-B, R1-C, R1-D, R1-E, each with its label line >>>
<<< PASTE R2.md >>>
<<< PASTE R3.md >>>
```

---

## 8. Appendices

### A. Optional — per-agent rebuttal round (heavier than the default)

The default package uses one Cross-Examiner chat instead of five rebuttal chats; that is the moderate-tier tradeoff. If Round 2 shows two agents genuinely far apart on a mechanism (not just on weights), give each of them one rebuttal turn, then feed the rebuttals to the Chair alongside their original briefs.

```text
<<< PASTE BLOCK 0 HERE >>>
<<< PASTE THIS AGENT'S OWN ROUND 1 BRIEF, labeled "MY BRIEF" >>>
<<< PASTE THE OTHER FOUR BRIEFS, each labeled >>>
<<< PASTE THE CROSS-EXAMINER'S REBUTTAL PARAGRAPH ADDRESSED TO THIS AGENT >>>

You are the same council member who wrote MY BRIEF (role: <name>; value function unchanged). You have now read the other briefs and the Cross-Examiner's rebuttal to you. In 450 words or less:
1. Concede — points from others you now accept, and exactly what they change in your brief (which section, what wording).
2. Hold — points you reject, with the mechanism or evidence that lets you hold; no restating.
3. Revise — your updated Position (section 1) and Ranking (section 2), and updated Confidence (section 9) with the reason for the change or for the lack of one.
4. Ask — at most 2 verification checks whose result would move you.
Do not introduce new topics. Do not soften into agreement to be polite; hold where you have grounds.
```

### B. Optional — run the pre-mortem again on the final plan

If the Chair picked an option shape the pre-mortem did not cover (for example a specific O3 or O4 variant), re-run the R3 prompt with `DECISION.md` pasted instead of `R2.md` and the sentence "There is exactly one live option: the Decision in the record below." Feed the result back to the Chair as a `RESOLVED FACTS`-style addendum labelled `PRE-MORTEM OF FINAL PLAN` and ask for an updated section 9.

### C. Optional — red-team the decision record

```text
<<< PASTE BLOCK 0 HERE >>>
<<< PASTE DECISION.md >>>

You are an outside reviewer who has not seen the council's briefs — only the shared context and the decision record. Do not re-litigate the decision. In 500 words or less, find:
1. Internal contradictions between the Decision paragraph, the plan, and the dissent register.
2. Dissent-register entries whose disposition is hand-waved (an ADDRESSED with no mechanism; an ACCEPTED AS RISK with no severity judgment; a CONDITION with no check or date).
3. Plan items with no owner or no week, or that cannot fit the stated capacity; anything on the critical path that depends on an unresolved condition.
4. Claims that depend on an UNKNOWN from Block 0 but are not flagged as conditions.
5. Whether the Decision paragraph is executable: could an engineer start work tomorrow without asking what was meant? If not, what is missing.
6. One-line verdict: SHIP THE DECISION / SHIP WITH THESE FIXES / SEND BACK TO THE CHAIR, with the fixes listed.
```

If the verdict is SEND BACK, reopen the Round 4 chat, paste the review, and say: "Revise the decision record to resolve these; keep the same headings; note what changed at the top."

### D. `RESOLVED FACTS` addendum (when you verify something after Round 1)

Paste directly after Block 0 in Rounds 3 and 4.

```text
RESOLVED FACTS (added after Round 1; supersedes Block 0 and any brief where they conflict)
- <topic>: <what you found> — verified by <command / doc section / experiment>, on <date>.
- <topic>: ...
Chair: treat these as FACT. Where a brief's position depended on a contrary assumption, discount that part of the brief and say so in the dissent register.
```

Typical entries: which pooler and mode is in front of Postgres; whether the app role owns the tables; the count of `text()` / Core query sites; whether CI runs real Postgres; what the customer's questionnaire asks.

### E. Nudges (reply with one of these instead of accepting a weak output)

- **No commitment:** "You did not commit to a Position. Rules 4 and 9 of Block 0. Rewrite sections 1, 2 and 9 with a single ranked #1 and a numeric confidence."
- **Generic:** "Section 3 is generic. Rewrite each bullet as claim -> mechanism -> consequence for this team, naming the specific Postgres / SQLAlchemy mechanism."
- **Missing weaknesses:** "Section 4 has fewer than 3 real weaknesses. Add them, each with mitigation and cost."
- **Assumed an UNKNOWN:** "You asserted X about the team's setup; Block 0 marks it UNKNOWN. Mark it ASSUMPTION, state how much your position depends on it, and add it to section 6."
- **Truncated:** "Continue from where you stopped; do not restart."
- **Too long:** "Compress to the cap; cut prose, keep mechanisms and numbers."
- **Chair hedged:** "Section 1 is not a decision. Either name one option and shape, or name the specific UNKNOWN that blocks you, the spike that resolves it, its owner and date, and the default for each outcome."

### F. Design notes (why the package looks like this)

- **Two advocates plus three lenses.** The team's own framing is two-sided, and one engineer is already committed, so RLS and app-level each get a dedicated steelman that must also list its own weaknesses. Delivery, security and operations are lenses with no technology loyalty; between them they cover the three things the framing was really about (time, blast radius, runtime reality).
- **Every agent ranks all four options.** The hybrid (O3) and staged path (O4) are the likely real answers; forcing every brief to rank them gets five independent evaluations without a fifth advocate that would just split the difference.
- **Isolation vs authorization is defined up front.** "RLS vs application-level authorization" mixes two problems; the second one is application-side under every option, and letting it leak into the argument is the most common way this debate goes in circles.
- **One Cross-Examiner instead of five rebuttal chats.** Cheaper for a manual run, and its "contested facts" list is the most valuable artifact the council produces: those checks are things the team can verify in an afternoon.
- **The pre-mortem sits between cross-examination and the chair.** It targets only the options still live, so its failure stories are concrete, and its cheap controls and tripwires go into the plan whichever way the decision lands.
- **The chair may not average.** If the answer genuinely depends on an unknown, the output is a dated spike with defaults, which is still a decision the team can execute on Monday.
- **The senior engineer is handled by design, not by tone.** Block 0 tells every agent to treat the preference as information about ownership, not as an argument; the dissent register and the note to the team are written for that engineer to read first.
