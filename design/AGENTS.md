# Design — Agent Compliance Manifest

<!--
  AGENT INSTRUCTION: Mandatory entry point for the System Designer. Every push
  that modifies a file under design/ MUST come with the Pre-Flight
  Acknowledgement in §3 and pass the gates in §4.
-->

| Field | Value |
|---|---|
| **Document ID** | `DES-AGENTS-001` |
| **Version** | `1.0` |
| **Status** | `Approved` |
| **Owner** | System Designer |
| **Read By** | System Designer (primary); reviewed by System Architect |
| **Last Updated** | 2026-05-01 |

---

## 1. Mandatory Reading

| # | Document | Purpose |
|---|---|---|
| 1 | [`/VERSIONING.md`](../VERSIONING.md) | Version-bump rules. |
| 2 | [`/README.md`](../README.md) | Master guide. |
| 3 | [`/project/admin-portal-validation.md`](../project/admin-portal-validation.md) §3, §4, §5 | Validation, traceability, safe-content rules. |
| 4 | This file (`design/AGENTS.md`) | Role-specific compliance. |
| 5 | [`requirements/non-functional-requirements.md`](../requirements/non-functional-requirements.md) | NFRs are the design's measuring stick. |
| 6 | [`architecture/technical-architecture.md`](../architecture/technical-architecture.md) | C4 context — design lives inside this. |
| 7 | [`architecture/data-model.md`](../architecture/data-model.md) | Persistence entities you must support. |
| 8 | All sibling design docs (`design/*.md`) | Avoid contradictions across security / resilience / DB / monitoring / infra. |
| 9 | [`/project/decision-log.md`](../project/decision-log.md) | ADRs that constrain or enable design choices. |

---

## 2. Pre-Flight Acknowledgement

```markdown
## Pre-Flight Acknowledgement
- Role: System Designer
- Task: <one-line description>
- Docs read (with version):
  - VERSIONING.md v____
  - README.md v____
  - project/admin-portal-validation.md v____
  - design/AGENTS.md v____
  - requirements/non-functional-requirements.md v____
  - architecture/technical-architecture.md v____
  - architecture/data-model.md v____
  - design/infrastructure-design.md v____
  - design/security-design.md v____
  - design/resilience-design.md v____
  - design/database-design.md v____
  - design/monitoring-design.md v____
  - project/decision-log.md v____
- Mandatory gates honored:
  - [ ] Every design choice references the NFR or FR it serves
  - [ ] OWASP Top-10 controls listed for any new attack surface
  - [ ] Resilience pattern (circuit breaker / retry / fallback) chosen for every new outbound call
  - [ ] Monitoring SLI/SLO defined for every new component
  - [ ] No secrets / hostnames / PII in design docs
  - [ ] Revision History rows added in every modified file
```

---

## 3. Mandatory Gates

| ID | Gate | Source |
|---|---|---|
| DES-G1 | Every design choice traces to an NFR or FR (link in the doc) | admin-portal-validation §4 |
| DES-G2 | New attack surface (endpoint, queue, external integration) has OWASP Top-10 controls listed in `security-design.md` | `design/security-design.md` |
| DES-G3 | Every new outbound dependency has a chosen resilience pattern documented in `resilience-design.md` | `design/resilience-design.md` |
| DES-G4 | Every new component has at least one SLI and one SLO in `monitoring-design.md` | `design/monitoring-design.md` |
| DES-G5 | Database changes include index strategy + query baseline in `database-design.md` | `design/database-design.md` |
| DES-G6 | No secrets / production hostnames / real PII in any design doc | admin-portal-validation §5.2 |
| DES-G7 | Revision History bumped per modified file | admin-portal-validation §3.3 |

---

## 4. Commit Convention

Prefix: `[Designer]`

| Change | Type | Version impact |
|---|---|---|
| Add a new design pattern or component coverage | `feat` | MINOR |
| Refine an existing design doc | `refactor` | PATCH |
| Correct an error or stale reference | `fix` | PATCH |

---

## Revision History

| Version | Date       | Author            | Change Summary |
|---------|------------|-------------------|----------------|
| 1.0     | 2026-05-01 | System Designer  | Initial design compliance manifest. |
