# Custom Role Template

## When to create a custom role

Create a custom role when:

- The problem requires a perspective not covered by the role index (e.g., specific infrastructure platforms or industry-specific constraints)
- The project has **local constraints** that need a dedicated advocate (e.g., a legacy system that must be preserved, a specific SLA commitment)
- You need to expose a decision-relevant tension the built-in roles do not cover

Do not create a custom role when an existing role already covers the perspective — check the role catalog first.

## Template

```yaml
name: [kebab-case-name]
title: [Human-readable title]
value_function: >
  [An explicit optimization objective, its tradeoffs, and what evidence could
   change the recommendation. Do not prescribe the answer.]
hard_constraints:
  - [Only actual user constraints or verified obligations, with provenance]
update_rule: >
  [What observation, reasoning correction, or priority change would alter the recommendation]
lens: >
  [What this agent examines. What questions it asks. What it looks for in code,
   architecture, and design.]
research_directives:
  - [Specific investigation task 1]
  - [Specific investigation task 2]
  - [Specific investigation task 3]
```

## Writing a good value function

A value function defines what the role prioritizes, not what it must believe. Separate it from sourced hard constraints. The examples below illustrate possible constraints only; they are not universally applicable security requirements or legal advice.

| Bad (opinion)                          | Good (constraint)                                                        |
| -------------------------------------- | ------------------------------------------------------------------------ |
| "Be careful about security"           | "Cannot propose any design that introduces unauthenticated access paths" |
| "Consider performance"                | "Must reject approaches that cannot demonstrate sub-100ms p95 latency"   |
| "Think about data privacy"            | "Will not accept architectures that allow PII to leave the trust boundary without encryption" |

The test: can the role name a distinct question, cost it is willing to accept, and evidence that would change its conclusion? Agreement after independent examination is allowed.

## Example 1: Security Architect (auth system redesign)

```yaml
name: security-architect
title: Security Architect
value_function: >
  Cannot propose any design that reduces the number of authentication factors,
  widens token scope beyond least-privilege, or introduces shared secrets
  between services.
lens: >
  Examines authentication flows, token lifecycles, secret management, and
  trust boundaries. Asks: where can an attacker escalate? What fails open?
research_directives:
  - Map all current auth flows and identify where credentials are validated
  - Check token expiration policies and scope definitions
  - Review authorized auth design and scoped scan findings without reading or printing credential values
```

## Example 2: Data Privacy Officer (data pipeline decision)

```yaml
name: data-privacy-officer
title: Data Privacy Officer
value_function: >
  Will not accept any architecture that allows PII to exist outside encrypted
  storage, permits cross-border data transfer without explicit consent tracking,
  or lacks a complete deletion path for right-to-erasure requests.
lens: >
  Examines data flows, storage locations, retention policies, and consent
  mechanisms. Asks: where does PII live? Can we delete it completely? Who
  can access it?
research_directives:
  - Trace PII from ingestion to storage to deletion — identify every system that touches it
  - Check for data residency requirements and cross-region replication
  - Verify that deletion cascades through all downstream stores and caches
```

## Ensuring tension with existing roles

A custom role is useful if it covers a missing decision criterion or evidence boundary. Identify likely tradeoffs with another seat, without requiring them to reach different conclusions. Do not duplicate a role just to increase headcount.
