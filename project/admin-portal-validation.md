# Admin Portal Validation & Traceability

<!--
  AGENT INSTRUCTION: This document defines how the GateForge Blueprint Repository is
  validated by the Admin Portal Control Tower. The Blueprint is the authoritative
  "compliance ledger" — the Admin Portal is a READ-ONLY dashboard that indexes safe
  metadata from this repository to produce validation, traceability, and evidence
  views. No secrets, no PHI, and no production data are stored in this repository.

  OWNER: System Architect
  READERS: All agents; Admin Portal validators; Compliance reviewers
-->

| Field | Value |
|---|---|
| **Document ID** | `PRJ-ADMIN-PORTAL-001` |
| **Version** | `0.1.0` |
| **Status** | `Draft` |
| **Owner** | System Architect |
| **Last Updated** | `[PLACEHOLDER — YYYY-MM-DD]` |
| **Approved By** | `—` |

---

## 1. Purpose

The **Admin Portal Control Tower** is the governance dashboard that consumes this
Blueprint Repository. It validates structural completeness, surfaces traceability
gaps, and aggregates release and compliance evidence. It does **not** store source
of truth — this repository is.

**Core principle:** The Blueprint is the **compliance ledger**. The Admin Portal
reads validation and evidence from the Markdown artifacts in this repository.
Teams update the ledger; the portal reflects it.

---

## 2. Revision History

<!-- AGENT INSTRUCTION: Every document edit appends a row here. Never edit history rows. -->

| Version | Date | Author | Change Summary |
|---|---|---|---|
| 0.1.0 | [PLACEHOLDER] | System Architect | Initial draft |

---

## 3. Blueprint Validation Rules (read by the Admin Portal)

<!--
  AGENT INSTRUCTION: These are the structural checks the Admin Portal performs on
  every branch push. Any RULE that fails blocks the "validation green" badge for
  the project. Architect may grant time-boxed exceptions via decision-log.md.
-->

### 3.1 Required Top-Level Folders

The Admin Portal requires these folders at the repository root. Missing folders
fail the `blueprint.structure.folders` check.

| Folder | Must Exist | Purpose |
|---|---|---|
| `requirements/` | ✅ | User, functional, non-functional requirements |
| `architecture/` | ✅ | Technical architecture, data model, API specs |
| `design/` | ✅ | Infrastructure, security, resilience, DB, monitoring |
| `development/` | ✅ | Coding standards, per-module docs |
| `qa/` | ✅ | Test plan, test cases, reports, defects |
| `operations/` | ✅ | Runbooks, logs, incidents, SLA tracking |
| `project/` | ✅ | Backlog, iterations, releases, decisions, status |

### 3.2 Metadata Completeness

Every document MUST begin with the standard metadata table (see `README.md` §
Template Metadata Standard). The Admin Portal parses these fields:

| Field | Required | Validation |
|---|---|---|
| `Document ID` | ✅ | Must match an ID regex in §3.4 |
| `Version` | ✅ | `MAJOR.MINOR` or `MAJOR.MINOR.PATCH` (semver) |
| `Status` | ✅ | One of: `Draft`, `In Review`, `Approved`, `Deprecated`, `Living Document` |
| `Owner` | ✅ | Must match a role in the Ownership Matrix (§3.5) |
| `Last Updated` | ✅ | ISO date `YYYY-MM-DD`; not in the future |
| `Approved By` | Conditional | Required when `Status = Approved` |

Missing or malformed metadata fails the `blueprint.metadata.completeness` check.

### 3.3 Revision History

Every document MUST include a Revision History table with the columns
`Version | Date | Author | Change Summary`. Each version bump requires a new row.
The Admin Portal verifies that the topmost row's version matches the metadata
`Version` field.

Fails the `blueprint.revision.history` check if:
- Table is missing.
- Top row version does not match metadata.
- Any row has an empty `Change Summary`.

### 3.4 ID Regex Conventions

The Admin Portal indexes artifacts by ID. All IDs MUST match these patterns:

| Entity | Regex | Example |
|---|---|---|
| User Story | `^US-\d{3}$` | `US-001` |
| Functional Requirement | `^FR-[A-Z]+-\d{3}$` | `FR-AUTH-001` |
| Non-Functional Requirement | `^NFR-[A-Z]+-\d{3}$` | `NFR-PERF-001` |
| Module | `^MOD-[A-Z]+$` | `MOD-AUTH` |
| Test Case | `^TC-[a-z]+-(?:unit\|integration\|e2e\|performance\|security)-\d{3}$` | `TC-auth-unit-001` |
| Defect | `^DEF-\d{3}$` | `DEF-001` |
| Incident | `^INC-\d{3}$` | `INC-001` |
| Iteration | `^ITER-\d{3}$` | `ITER-001` |
| Release | `^RELEASE-v\d+\.\d+\.\d+$` | `RELEASE-v1.0.0` |
| ADR | `^ADR-\d{3}$` | `ADR-001` |
| Document (generic) | `^[A-Z]+(?:-[A-Z]+)*-\d{3}$` | `REQ-FUNC-001` |

IDs that do not match fail `blueprint.ids.regex`.

### 3.5 Ownership Matrix

<!--
  AGENT INSTRUCTION: The Admin Portal uses this matrix to validate that a document's
  Owner field matches the role authorized to write to its directory. If an Owner is
  set to a role not listed here for that directory, validation fails.
-->

| Directory | Primary Owner | Contributors | Admin Portal Check |
|---|---|---|---|
| `requirements/` | System Architect | — | `blueprint.ownership.requirements` |
| `architecture/` | System Architect | System Designer | `blueprint.ownership.architecture` |
| `design/` | System Designer | System Architect (review) | `blueprint.ownership.design` |
| `development/` | Developers | System Architect (review) | `blueprint.ownership.development` |
| `qa/` | QC Agents | System Architect (review) | `blueprint.ownership.qa` |
| `operations/` | Operator | System Architect (review) | `blueprint.ownership.operations` |
| `project/` | System Architect | All agents (status) | `blueprint.ownership.project` |

### 3.6 Traceability Completeness

See §4 for the full traceability model. The Admin Portal enforces:

- Every `US-NNN` has ≥ 1 linked `FR-*`.
- Every `FR-*` has ≥ 1 linked `TC-*` (or is marked `non-testable` with rationale).
- Every `DEF-NNN` links to the `TC-*` that surfaced it and, once fixed, the
  `RELEASE-v*` that shipped the fix.
- Every `P0` or `P1` incident (`INC-NNN`) links to its root-cause `ADR-NNN` (new or
  updated) and any corrective `DEF-NNN` or `FR-*`.
- Every `RELEASE-v*` has a release evidence pack (see
  `project/release-evidence-pack.md`).

Orphans and dangling links fail `blueprint.traceability.completeness`.

---

## 4. Traceability Model

<!--
  AGENT INSTRUCTION: This is the canonical traceability chain. Every chain link is
  a Markdown cross-reference (e.g., [US-001](../requirements/user-requirements.md#us-001)).
  The Admin Portal parses these links to build the traceability graph.
-->

```
User Story (US)
   └── Functional Requirement (FR)
          └── Test Case (TC)
                 └── Defect (DEF, if any)
                        └── Release (RELEASE-vX.Y.Z) — ships the fix
                               └── ADR — if the fix required a decision
                                      └── Incident (INC) — if the defect escaped to prod
```

### 4.1 Link Direction

| From | To | Where the link lives |
|---|---|---|
| `US-*` | `FR-*` | `requirements/functional-requirements.md` traceability matrix |
| `FR-*` | `TC-*` | `qa/test-cases/*.md` metadata and `requirements/functional-requirements.md` |
| `TC-*` | `DEF-*` | `qa/defects/DEF-NNN.md` metadata |
| `DEF-*` | `RELEASE-v*` | `project/releases/RELEASE-vX.Y.Z.md` included items |
| `RELEASE-v*` | `ADR-*` | `project/decision-log.md` and the release evidence pack |
| `INC-*` | `ADR-*`, `DEF-*`, `FR-*` | `operations/incident-reports/INC-NNN.md` post-mortem |

### 4.2 Minimum Traceability Per Artifact

| Artifact | Must Link Up To | Must Link Down To |
|---|---|---|
| User Story | — | ≥ 1 FR |
| Functional Requirement | 1 US | ≥ 1 TC (or `non-testable` tag) |
| Test Case | 1+ FR | Defects (as discovered) |
| Defect | 1 TC | 1 Release (when fixed) |
| Release | Defects closed, FRs shipped | ADRs invoked, Evidence Pack |
| Incident | — | Root-cause ADR + corrective DEF/FR |
| ADR | Triggering US/FR/INC | Releases where enacted |

---

## 5. Admin Portal Evidence Fields

<!--
  AGENT INSTRUCTION: The Admin Portal extracts ONLY the fields listed below. Authors
  MUST NOT put secrets, production credentials, patient data, or other sensitive
  payloads into documents. Use pointers to secret managers and de-identified examples.
-->

### 5.1 Safe Metadata (extracted by the portal)

The Admin Portal reads the following SAFE fields from this Blueprint:

| Source Document | Safe Fields Extracted |
|---|---|
| `requirements/*.md` | Document ID, Version, Status, Owner, Last Updated, FR/NFR IDs, linked US IDs |
| `architecture/*.md`, `design/*.md` | Document ID, Version, Status, ADR IDs referenced |
| `qa/test-cases/*.md` | TC ID, linked FR IDs, test type, status (pass/fail/blocked) |
| `qa/defects/DEF-*.md` | DEF ID, severity, status, linked TC + Release |
| `operations/incident-reports/INC-*.md` | INC ID, severity, detection/resolution times, linked ADR/DEF/FR |
| `project/releases/RELEASE-v*.md` | Release version, status, included FRs, linked evidence pack |
| `project/decision-log.md` | ADR IDs, status, impact |
| `project/compliance-controls.md` | Control IDs, status, owner, last reviewed |

### 5.2 Prohibited Content (MUST NEVER appear in any file)

The following fail the `blueprint.evidence.safety` check and **block** the
validation badge:

- Plaintext passwords, API keys, tokens, certificates, private keys.
- `.env` values with real credentials (use `.env.example` with placeholders).
- Protected Health Information (PHI): real patient names, MRNs, DOBs, addresses,
  diagnoses tied to identity, claims data, device identifiers linked to a person.
- Personally Identifiable Information (PII) of real customers or staff.
- Production database dumps, real payloads from production traffic.
- Internal IP addresses or hostnames that are not already public.

**If sensitive data must be referenced**, use:
- `{{SECRET:name}}` placeholders and point to the secret manager path.
- Synthetic or de-identified examples (see
  `operations/healthcare-readiness.md` § De-identification & Synthetic Data).
- Structural examples only (field names + types, not values).

### 5.3 Validation Badge States

The Admin Portal surfaces one of:

| Badge | Meaning |
|---|---|
| `validation: green` | All §3 checks pass; all §5.2 prohibited-content scans clean. |
| `validation: amber` | Traceability incomplete or metadata stale (> 30 days); no sensitive-content hits. |
| `validation: red` | Structural check failed OR prohibited content detected. Release is blocked. |

---

## 6. Acceptance Checklist (Admin Portal reads this directly)

<!--
  AGENT INSTRUCTION: This checklist is machine-parsed. Keep one item per line with
  the exact `[ ]` / `[x]` prefix so the Admin Portal can toggle state. Do not
  change item wording without updating the portal's check registry.
-->

- [ ] All seven top-level folders exist (`requirements/`, `architecture/`, `design/`, `development/`, `qa/`, `operations/`, `project/`).
- [ ] Every Markdown document starts with the standard metadata table.
- [ ] Every document has a Revision History table with a row for the current version.
- [ ] All IDs match the regex patterns in §3.4.
- [ ] Every Owner field matches the directory's authorized role in §3.5.
- [ ] Every User Story links to ≥ 1 Functional Requirement.
- [ ] Every Functional Requirement links to ≥ 1 Test Case (or is tagged `non-testable`).
- [ ] Every Defect links to its surfacing Test Case and, once fixed, to a Release.
- [ ] Every Release has a matching `project/release-evidence-pack.md` evidence entry.
- [ ] Every P0/P1 Incident has a post-mortem linked to an ADR and corrective item.
- [ ] `project/compliance-controls.md` exists and lists each applicable control with owner and last-reviewed date.
- [ ] `operations/audit-evidence.md` documents how audit logs are exported and retained (no logs in repo).
- [ ] `operations/healthcare-readiness.md` exists when the project handles health data.
- [ ] No file contains plaintext secrets, real PHI, or real PII (see §5.2).

---

## 7. Cross-References

- [`README.md`](../README.md) — Master repository guide.
- [`project/compliance-controls.md`](compliance-controls.md) — Control catalog.
- [`project/release-evidence-pack.md`](release-evidence-pack.md) — Per-release evidence guidance.
- [`operations/audit-evidence.md`](../operations/audit-evidence.md) — Audit log export and retention.
- [`operations/healthcare-readiness.md`](../operations/healthcare-readiness.md) — Healthcare readiness overlay.
