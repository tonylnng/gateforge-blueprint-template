# QA — Agent Compliance Manifest

<!--
  AGENT INSTRUCTION: This is the MANDATORY entry point for every QC Agent
  (VM-4, MiniMax 2.7, or any future QC agent). Every test report you produce
  MUST begin with the Pre-Flight Acknowledgement in §3 and honor every gate in
  §4 — especially the E2E gate (QA-G3). Reports without the acknowledgement
  fail Admin Portal validation ('agent.preflight.present') and block release.

  This file exists specifically because of a recurring problem: QC agents
  produced reports that ignored the E2E branch of qa/test-plan.md. Read §4
  carefully — that gate is non-negotiable.
-->

| Field | Value |
|---|---|
| **Document ID** | `QA-AGENTS-001` |
| **Version** | `1.0` |
| **Status** | `Approved` |
| **Owner** | QC Agents (compliance) / System Architect (rules) |
| **Read By** | All QC Agents |
| **Last Updated** | 2026-05-01 |

---

## 1. Why This File Exists (and the lesson behind it)

In a previous iteration, the QC agent skipped the E2E test plan even though
`qa/test-plan.md` mandated it. The defect class slipped to UAT and surfaced as
a customer-facing regression. The root cause was not laziness — it was the
absence of a single mandatory entry point that forced the agent to read the
test plan **and** required the agent to prove it had honored every test
level. This `AGENTS.md` is that single entry point.

Three behavioral guarantees this file gives us:

1. **One reading list, in order.** No skipping.
2. **Pre-Flight Acknowledgement.** The agent must declare what it read,
   listing each document and its version, before any test report is accepted.
3. **Per-level test gates.** Every applicable test level (Unit, Integration,
   E2E, Performance, Security) must be either executed-and-reported or
   explicitly waived with a documented reason. "Forgot" is not a valid waiver.

---

## 2. Mandatory Reading

| # | Document | Purpose |
|---|---|---|
| 1 | [`/VERSIONING.md`](../VERSIONING.md) | Test reports are versioned artifacts. |
| 2 | [`/README.md`](../README.md) | Repository master guide. |
| 3 | [`/project/admin-portal-validation.md`](../project/admin-portal-validation.md) §3, §4 | Validation rules and traceability. |
| 4 | This file (`qa/AGENTS.md`) | Role-specific compliance. |
| 5 | [`qa/README.md`](README.md) | Workflow, ownership, quality gates. |
| 6 | [`qa/test-plan.md`](test-plan.md) | **Master test plan — every level here is mandatory.** |
| 7 | [`qa/test-cases/README.md`](test-cases/README.md) | Test case format. |
| 8 | [`qa/reports/README.md`](reports/README.md) | Test report format. |
| 9 | [`qa/defects/README.md`](defects/README.md) | Defect format. |
| 10 | [`qa/performance/load-test-plan.md`](performance/load-test-plan.md) | Performance level details. |
| 11 | [`qa/performance/stress-test-plan.md`](performance/stress-test-plan.md) | Stress level details. |
| 12 | [`requirements/functional-requirements.md`](../requirements/functional-requirements.md) | Source of test conditions. |
| 13 | [`requirements/non-functional-requirements.md`](../requirements/non-functional-requirements.md) | Performance / security targets. |
| 14 | All `architecture/api-specifications/*.openapi.yaml` files in your scope | Contract-test source. |

---

## 3. Pre-Flight Acknowledgement (must appear at the top of every test report)

```markdown
## Pre-Flight Acknowledgement
- Role: QC Agent <ID — e.g., VM-4 or MiniMax 2.7>
- Task: Execute <scope> tests for <module> in <iteration>
- Docs read (with version):
  - VERSIONING.md v____
  - README.md v____
  - project/admin-portal-validation.md v____
  - qa/AGENTS.md v____
  - qa/README.md v____
  - qa/test-plan.md v____
  - qa/test-cases/README.md v____
  - qa/reports/README.md v____
  - qa/defects/README.md v____
  - qa/performance/load-test-plan.md v____
  - qa/performance/stress-test-plan.md v____
  - requirements/functional-requirements.md v____
  - requirements/non-functional-requirements.md v____
  - architecture/api-specifications/<service>.openapi.yaml v____
- Mandatory gates honored (tick or document a waiver):
  - [ ] QA-G1  Unit tests executed       — coverage ____% (≥ 95% required)
  - [ ] QA-G2  Integration tests executed — coverage ____% (≥ 90% required)
  - [ ] QA-G3  **E2E tests executed**     — coverage ____% (≥ 85% required)
  - [ ] QA-G4  Performance tests executed — p95 ____ ms (NFR target ____ ms)
  - [ ] QA-G5  Security scan run         — high/critical findings: ____
  - [ ] QA-G6  Every executed TC links to an FR
  - [ ] QA-G7  Every found defect filed as DEF-NNN with severity
  - [ ] QA-G8  metrics.md updated with this run
- Waivers (only valid if explicitly granted by Architect; cite ADR or status report):
  - <none> | <waiver text + ADR-NNN or status-YYYY-MM-DD>
```

---

## 4. Mandatory Gates

| ID | Gate | Threshold / requirement | Source |
|---|---|---|---|
| QA-G1 | **Unit** tests executed and report attached | line + branch coverage ≥ 95% | `qa/README.md` §5 |
| QA-G2 | **Integration** tests executed | API endpoint coverage ≥ 90% | `qa/README.md` §5 |
| QA-G3 | **E2E** tests executed | workflow coverage ≥ 85%, **all critical user paths green** | `qa/README.md` §5; `qa/test-plan.md` §4 |
| QA-G4 | **Performance** tests executed | p95 within NFR target; no regression > 10% from baseline | `qa/performance/load-test-plan.md` |
| QA-G5 | **Security** scan run | zero High / Critical findings | `qa/README.md` §5 |
| QA-G6 | Every executed TC links up to an FR | TC metadata block | admin-portal-validation §4 |
| QA-G7 | Every defect found is filed as `DEF-NNN.md` with severity, repro steps, linked TC | `qa/defects/README.md` |
| QA-G8 | `qa/metrics.md` updated within the same PR | living dashboard | `qa/README.md` §4 |

**Critical rule for QA-G3 (E2E):** Skipping E2E is the failure mode this entire
manifest exists to prevent. The only valid reasons to NOT execute E2E are:
- The module has no UI or user-facing workflow (state this explicitly with the
  module's `MOD-XXX` ID).
- The Architect has granted a waiver in `project/decision-log.md` (cite the
  ADR-NNN).

"Time pressure", "no environment", and "covered by integration tests" are NOT
valid waivers. If the staging environment is down, file `INC-NNN`, pause the
release, and fix the environment.

---

## 5. Commit Convention

Prefix: `[QC]`

| Change | Type | Version impact |
|---|---|---|
| New test case or new test category | `feat` | MINOR |
| Test result report for an iteration | `test` | PATCH |
| Fix a wrong test assertion | `fix` | PATCH |
| Update test plan structure | `refactor` | PATCH |
| Update metrics dashboard | `docs` | PATCH |

---

## 6. Failure Modes & Self-Recovery

| Symptom | Likely cause | Fix |
|---|---|---|
| `agent.preflight.present` red | Pre-Flight block missing or empty | Add the block at the top of the report |
| `agent.test-coverage.gates` red | One of QA-G1..G5 below threshold and no waiver | Either re-run with more cases, or get an Architect waiver and cite it |
| `blueprint.traceability.completeness` red | A TC has no FR link | Add the FR link in the TC metadata; re-push |
| `agent.e2e.gate` red | E2E skipped without valid waiver | Run E2E. There is no shortcut. |

---

## Revision History

| Version | Date       | Author             | Change Summary |
|---------|------------|--------------------|----------------|
| 1.0     | 2026-05-01 | QC Agents + Architect | Initial QA compliance manifest with explicit E2E gate (QA-G3) and mandatory Pre-Flight Acknowledgement to address recurrent E2E-skipping. |
