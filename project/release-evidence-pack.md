# Release Evidence Pack

<!--
  AGENT INSTRUCTION: This document describes the evidence pack that accompanies
  every production release. Each `RELEASE-vX.Y.Z.md` in `project/releases/` MUST
  link to or embed the items listed here. The Admin Portal Control Tower reads
  this evidence to issue a "release ready" badge and to satisfy compliance audits.

  The release evidence pack is the canonical proof that a release was planned,
  tested, reviewed, approved, and is safely rollback-able. Missing items fail
  the `release.evidence.complete` check.

  OWNER: System Architect
-->

> **🛑 STOP — Mandatory reading before assembling any release.** Read **[`project/AGENTS.md`](AGENTS.md)** and **[`/VERSIONING.md`](../VERSIONING.md)** first. Every release evidence pack must include a **Pre-Flight Acknowledgement** (§5) and a **Version-Bump Record** (§3 #13).

| Field | Value |
|---|---|
| **Document ID** | `PRJ-RELEASE-EVIDENCE-001` |
| **Version** | `0.2.0` |
| **Status** | `Living Document` |
| **Owner** | System Architect |
| **Last Updated** | `2026-05-01` |

---

## 1. Purpose

Define the minimum evidence bundle that must exist for every production release,
so that:

- An auditor can reconstruct *what shipped, why, and with what assurance* from
  this repository alone.
- The Admin Portal can render a one-click "release dossier" view.
- Rollback can be executed without guesswork.

---

## 2. Revision History

| Version | Date | Author | Change Summary |
|---|---|---|---|
| 0.2.0 | 2026-05-01 | System Architect | Added Pre-Flight Acknowledgement requirement and Version-Bump Record (item #13) to evidence pack; aligned with ADR-005 / ADR-006. |
| 0.1.0 | [PLACEHOLDER] | System Architect | Initial evidence pack guidance. |

---

## 3. Evidence Pack Contents

<!--
  AGENT INSTRUCTION: For each release, populate the template in §5 below.
  Every row's "Evidence Link" column MUST be a relative Markdown link to an
  artifact in this repository or a clearly labelled external register entry.
-->

Every release evidence pack contains:

| # | Evidence Item | Required | Source Artifact |
|---|---|---|---|
| 1 | Linked Requirements (FR IDs shipped) | ✅ | `requirements/functional-requirements.md` |
| 2 | Linked Test Cases (TC IDs executed against the release) | ✅ | `qa/test-cases/*.md` |
| 3 | Test Results (pass/fail summary, coverage, perf metrics) | ✅ | `qa/reports/TEST-REPORT-ITER-*.md` |
| 4 | Unresolved Defects (open DEF IDs at cut, with risk acceptance) | ✅ | `qa/defects/DEF-*.md` |
| 5 | ADRs Invoked (new or referenced architectural decisions) | ✅ | `project/decision-log.md` |
| 6 | Incidents in Context (open INC IDs this release addresses or is constrained by) | Conditional | `operations/incident-reports/INC-*.md` |
| 7 | Human Approvals (named approver + role + date) | ✅ | §5 of this document |
| 8 | Rollback Plan (trigger criteria, runbook pointer, data-migration reversibility) | ✅ | `operations/deployment-runbook.md` + release notes |
| 9 | Deployment Notes (migrations, config flags, breaking changes) | ✅ | `project/releases/RELEASE-vX.Y.Z.md` |
| 10 | Compliance Evidence (control IDs re-verified for this release) | Conditional | `project/compliance-controls.md` |
| 11 | Healthcare Readiness Attestation (if applicable) | Conditional | `operations/healthcare-readiness.md` |
| 12 | Security Scan Results (SAST, dependency, container) | ✅ | `qa/reports/` or external scanner report link |
| 13 | Version-Bump Record (`VERSION` value, tag, workflow run, bump type) | ✅ | `/VERSION`, `CHANGELOG.md`, GitHub Actions run for `version-bump.yml` |
| 14 | Pre-Flight Acknowledgement (per-role AGENTS.md read with version) | ✅ | §5 of this document; PR description |
| 15 | QA Gate Matrix (QA-G1…QA-G8 explicit pass/fail — includes E2E QA-G3) | ✅ | `qa/reports/TEST-REPORT-ITER-*.md` and `qa/AGENTS.md` |

### 3.1 Conditional Items

- **Incidents in Context** is required when the release ships a fix for an open
  INC or is deployed under an active incident's constraints.
- **Compliance Evidence** is required when the release touches controls listed
  in `project/compliance-controls.md` (e.g., auth, logging, encryption, data
  retention).
- **Healthcare Readiness Attestation** is required when the project is scoped
  to handle PHI. Absence in a PHI-scoped release fails `release.evidence.hc`.

---

## 4. Evidence Quality Requirements

| Item | Quality Rule |
|---|---|
| Linked Requirements | Every FR ID must be `Approved` status at release cut. |
| Linked Test Cases | Coverage must meet `qa/README.md` Quality Gate thresholds. |
| Test Results | A failed critical test without documented risk acceptance blocks release. |
| Unresolved Defects | Every open P0 defect blocks release. Every open P1 defect requires Architect-signed risk acceptance in the release notes. |
| ADRs | Any `High` impact ADR must be `Accepted` before release. |
| Human Approvals | Minimum: QC sign-off + Architect sign-off + Operator sign-off. Add Compliance Lead sign-off when healthcare readiness applies. |
| Version-Bump Record | `VERSION` value matches the latest `CHANGELOG.md` entry and the latest annotated git tag. The GitHub Actions `version-bump.yml` run for the release commit is **green**. Bump type recorded (MAJOR / MINOR / PATCH). |
| Pre-Flight Acknowledgement | Every contributing role appears in the table with the AGENTS.md version they read. Missing rows fail `agent.preflight.present`. |
| QA Gate Matrix | All eight named gates (QA-G1…QA-G8) report explicit pass / fail. “N/A” only with QC-Lead-initialled rationale. The E2E gate (QA-G3) is non-skippable. |
| Rollback Plan | Must specify: trigger conditions, maximum data loss window, DB-migration reversal steps, feature-flag kill switch (if any). |
| Security Scan | No Critical/High findings; Medium findings require documented acceptance. |

---

## 5. Evidence Pack Template

<!--
  AGENT INSTRUCTION: Copy this block into the corresponding
  `project/releases/RELEASE-vX.Y.Z.md` file (or append here as a subsection
  named "Evidence Pack — vX.Y.Z"). Fill every [PLACEHOLDER]. Do not delete rows.
-->

### --- START TEMPLATE ---

```markdown
## Release Evidence Pack — v<X.Y.Z>

| Field | Value |
|---|---|
| **Release Version** | v<X.Y.Z> |
| **Evidence Pack Compiled By** | [PLACEHOLDER — Agent name] |
| **Compiled On** | [PLACEHOLDER — YYYY-MM-DD] |
| **Admin Portal Badge Target** | `release.evidence.complete` |

### Pre-Flight Acknowledgement

<!-- Required. One row per contributing role. Author confirms they have read the
     listed AGENTS.md at the listed version, before any change for this release. -->

| Role | Agent / Author | AGENTS.md Read | Version Read | Date |
|---|---|---|---|---|
| System Architect | [PLACEHOLDER] | `project/AGENTS.md` | v[PLACEHOLDER] | [YYYY-MM-DD] |
| QC Lead | [PLACEHOLDER] | `qa/AGENTS.md` | v[PLACEHOLDER] | [YYYY-MM-DD] |
| Operator | [PLACEHOLDER] | `operations/AGENTS.md` | v[PLACEHOLDER] | [YYYY-MM-DD] |
| Developers | [PLACEHOLDER] | `development/AGENTS.md` | v[PLACEHOLDER] | [YYYY-MM-DD] |
| Designer (if touched) | [PLACEHOLDER] | `design/AGENTS.md` | v[PLACEHOLDER] | [YYYY-MM-DD] |

### Version-Bump Record

<!-- Required. Confirms the auto-bump workflow ran and the result matches
     /VERSION, the latest CHANGELOG entry, and the git tag for this release. -->

| Field | Value |
|---|---|
| `/VERSION` value at release commit | [PLACEHOLDER — X.Y.Z] |
| Latest `CHANGELOG.md` heading version | [PLACEHOLDER — X.Y.Z] |
| Annotated git tag | `v[PLACEHOLDER]` |
| Bump type for this release | MAJOR / MINOR / PATCH |
| Bump trigger | auto (commit-type) / human (`Version-Bump: major` trailer) |
| `version-bump.yml` workflow run URL | [PLACEHOLDER] |
| Workflow run status | green |

### QA Gate Matrix (all eight gates required)

| Gate | Description | Result |
|---|---|---|
| QA-G1 | Unit tests | pass / fail / N/A (rationale) |
| QA-G2 | Integration tests | pass / fail / N/A (rationale) |
| QA-G3 | **E2E tests (non-skippable)** | pass / fail / N/A (rationale) |
| QA-G4 | Performance tests vs NFRs | pass / fail / N/A (rationale) |
| QA-G5 | Security tests | pass / fail / N/A (rationale) |
| QA-G6 | TC → FR traceability | pass / fail |
| QA-G7 | Defects filed for failures | pass / fail |
| QA-G8 | `qa/metrics.md` updated | pass / fail |

### Linked Requirements (FRs shipped)

| FR ID | Title | Status | Linked US |
|---|---|---|---|
| FR-[PLACEHOLDER] | [PLACEHOLDER] | Approved | US-[PLACEHOLDER] |

### Linked Test Cases & Results

| TC ID | Type | Result | Report |
|---|---|---|---|
| TC-[PLACEHOLDER] | unit / integration / e2e | pass / fail / blocked | [link] |

| Metric | Value |
|---|---|
| Unit coverage | [PLACEHOLDER]% |
| Integration coverage | [PLACEHOLDER]% |
| E2E coverage | [PLACEHOLDER]% |
| p95 latency vs NFR | [PLACEHOLDER] |
| Security scan Critical/High | 0 / 0 |

### Unresolved Defects (at release cut)

| DEF ID | Severity | Status | Risk Acceptance |
|---|---|---|---|
| DEF-[PLACEHOLDER] | P1 / P2 / P3 | open / deferred | [link to Architect note] |

### ADRs Invoked

| ADR ID | Title | Status |
|---|---|---|
| ADR-[PLACEHOLDER] | [PLACEHOLDER] | Accepted |

### Incidents in Context (if any)

| INC ID | Status | Relationship to Release |
|---|---|---|
| INC-[PLACEHOLDER] | resolved / post-mortem | fixed-in / deployed-under |

### Human Approvals

| Role | Name | Date | Notes |
|---|---|---|---|
| QC Lead | [PLACEHOLDER] | [YYYY-MM-DD] | [PLACEHOLDER] |
| System Architect | [PLACEHOLDER] | [YYYY-MM-DD] | [PLACEHOLDER] |
| Operator | [PLACEHOLDER] | [YYYY-MM-DD] | [PLACEHOLDER] |
| Compliance Lead (if PHI) | [PLACEHOLDER] | [YYYY-MM-DD] | [PLACEHOLDER] |

### Rollback Plan

| Aspect | Detail |
|---|---|
| Trigger criteria | [PLACEHOLDER — error rate, latency, data anomaly thresholds] |
| Max data loss window (RPO) | [PLACEHOLDER] |
| DB migration reversibility | forward-only / reversible-by-[PLACEHOLDER] |
| Feature flag kill switch | [PLACEHOLDER — flag name and owner] |
| Rollback runbook pointer | `operations/deployment-runbook.md#rollback` |
| Estimated time to rollback | [PLACEHOLDER — minutes] |

### Deployment Notes (summary)

| Aspect | Detail |
|---|---|
| Migrations | [PLACEHOLDER] |
| Config / feature flags | [PLACEHOLDER] |
| Breaking changes | [PLACEHOLDER] |
| Post-deploy verification | [PLACEHOLDER] |

### Compliance Evidence (controls re-verified)

| Control ID | Evidence Link | Re-verified On |
|---|---|---|
| CTRL-[PLACEHOLDER] | [link] | [YYYY-MM-DD] |

### Healthcare Readiness Attestation (if applicable)

| Item | Status | Notes |
|---|---|---|
| PHI classification unchanged or updated | [PLACEHOLDER] | [link] |
| Audit log export verified | [PLACEHOLDER] | [link] |
| De-identified data only in non-prod | [PLACEHOLDER] | [link] |
| Vendor/BAA register current | [PLACEHOLDER] | [link] |
```

### --- END TEMPLATE ---

---

## 6. Release Acceptance Checklist

<!--
  AGENT INSTRUCTION: Machine-parsed by the Admin Portal. One item per line.
-->

- [ ] Evidence pack filled for this release version.
- [ ] All FR IDs in the pack are `Approved`.
- [ ] All linked Test Cases have executed results with date and environment.
- [ ] Coverage meets Quality Gate thresholds in `qa/README.md`.
- [ ] Zero open P0 defects.
- [ ] All P1 defects have Architect-signed risk acceptance or are closed.
- [ ] All invoked ADRs are `Accepted`.
- [ ] Rollback plan is concrete (trigger + runbook + RPO).
- [ ] Human approvals include QC, Architect, and Operator at minimum.
- [ ] Security scan shows zero Critical/High findings.
- [ ] Compliance controls re-verified (when release touches controlled areas).
- [ ] Healthcare readiness attestation included (when in PHI scope).
- [ ] Pre-Flight Acknowledgement table populated for all contributing roles.
- [ ] Version-Bump Record present and consistent (`VERSION` = latest CHANGELOG = git tag, workflow green).
- [ ] QA Gate Matrix shows explicit result for **every** gate QA-G1…QA-G8 (E2E QA-G3 included).

---

## 7. Cross-References

- [`project/releases/README.md`](releases/README.md) — Release plan template.
- [`project/admin-portal-validation.md`](admin-portal-validation.md) — Blueprint validation rules.
- [`project/compliance-controls.md`](compliance-controls.md) — Compliance control catalog.
- [`operations/deployment-runbook.md`](../operations/deployment-runbook.md) — Deployment and rollback procedure.
- [`operations/audit-evidence.md`](../operations/audit-evidence.md) — Audit log evidence.
- [`operations/healthcare-readiness.md`](../operations/healthcare-readiness.md) — Healthcare readiness overlay.
