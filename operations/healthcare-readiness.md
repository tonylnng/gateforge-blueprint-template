# Healthcare Readiness Overlay

<!--
  AGENT INSTRUCTION: This document is the "healthcare readiness" overlay for any
  GateForge project that handles Protected Health Information (PHI) or operates
  in a healthcare context. It gathers the evidence needed to demonstrate
  readiness for audits and customer due diligence.

  IMPORTANT SCOPE & LANGUAGE:
  - Use the terms "healthcare readiness" and "compliance evidence".
  - Do NOT claim HIPAA compliance, HITRUST certification, or equivalent. Formal
    compliance requires attestation / certification processes outside this repo.
  - Describe controls and evidence; leave legal conclusions to qualified counsel.

  OWNER: Operator
  REVIEWERS: System Architect, Compliance Lead (external role, if assigned)
-->

| Field | Value |
|---|---|
| **Document ID** | `OPS-HEALTHCARE-READINESS-001` |
| **Version** | `0.1.0` |
| **Status** | `Draft` |
| **Owner** | Operator |
| **Reviewer** | System Architect |
| **Last Updated** | `[PLACEHOLDER — YYYY-MM-DD]` |

---

## 1. Purpose

Describe the additional controls, practices, and evidence that apply when the
project handles PHI. The Admin Portal reads this document to determine whether
a project is "healthcare-ready" and to surface the overlay in the portal's
Compliance tab.

**Scope note:** This overlay applies only when §2 PHI scope is checked. For
non-healthcare projects, mark this file as `Not Applicable` in §2 and leave
remaining sections as guidance for future scope changes.

---

## 2. Applicability & PHI Scope

| Field | Value |
|---|---|
| **Does this project process PHI?** | [ ] Yes &nbsp;&nbsp; [ ] No |
| **PHI classification last reviewed on** | [PLACEHOLDER — YYYY-MM-DD] |
| **Reviewer** | [PLACEHOLDER] |
| **If No — rationale** | [PLACEHOLDER — e.g., system processes de-identified data only; contractual exclusion] |

If `No`, the remaining sections are informational; the Admin Portal shows
`healthcare-readiness: n/a`. If `Yes`, all sections below must be completed.

---

## 3. Revision History

| Version | Date | Author | Change Summary |
|---|---|---|---|
| 0.1.0 | [PLACEHOLDER] | Operator | Initial healthcare readiness overlay |

---

## 4. PHI Classification

<!--
  AGENT INSTRUCTION: Classify every data element the system stores or transmits.
  PHI is defined broadly — any health information combined with an identifier.
  Mark each element `PHI`, `PII`, `Sensitive-Other`, or `Non-Sensitive`.
-->

| Data Element | Classification | Stored In | Notes |
|---|---|---|---|
| Patient name | PHI | [PLACEHOLDER] | [PLACEHOLDER] |
| Medical record number (MRN) | PHI | [PLACEHOLDER] | [PLACEHOLDER] |
| Date of birth | PHI | [PLACEHOLDER] | Combine with any health data → PHI |
| Diagnosis / clinical note | PHI | [PLACEHOLDER] | [PLACEHOLDER] |
| Insurance claim data | PHI | [PLACEHOLDER] | [PLACEHOLDER] |
| Device identifier linked to person | PHI | [PLACEHOLDER] | [PLACEHOLDER] |
| Staff email address | PII | [PLACEHOLDER] | [PLACEHOLDER] |
| Audit log event metadata | Sensitive-Other | Log store | Never echo PHI into log bodies |

### 4.1 Classification Rules

- Any field whose presence could identify an individual is PII.
- PII + health information = PHI.
- De-identified data (per §9) may be classified `Non-Sensitive` only if the
  de-identification method is documented and reviewed.

---

## 5. Data Flow

<!--
  AGENT INSTRUCTION: Document every system boundary where PHI enters, moves, or
  leaves. Use `architecture/technical-architecture.md` as the upstream diagram.
  This section is a prose/tabular summary keyed to that diagram.
-->

| Flow | From | To | Transport | Purpose | Data Elements | PHI? |
|---|---|---|---|---|---|---|
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | TLS 1.2+ | [PLACEHOLDER] | [PLACEHOLDER] | ✅ / ❌ |

**Required properties of every PHI flow:**
- Encrypted in transit (TLS 1.2+, modern ciphers).
- Authenticated at both ends.
- Logged in the audit trail (see `operations/audit-evidence.md`).
- Minimum-necessary principle: only the fields needed for the purpose.

---

## 6. Retention & Disposition

| Data Class | Retention | Disposition Method | Owner |
|---|---|---|---|
| Active PHI records | [PLACEHOLDER] | n/a (in-use) | [PLACEHOLDER] |
| Archived PHI | [PLACEHOLDER — per contract/law] | Cryptographic erasure + key destruction | Operator |
| Audit logs (PHI access) | [PLACEHOLDER — align with `audit-evidence.md`] | Immutable until retention end | Operator |
| Backups containing PHI | [PLACEHOLDER] | Overwrite + key destruction | Operator |
| Non-prod fixtures | N/A — must be de-identified (see §9) | n/a | Developers |

**Rule:** Retention must satisfy the longest applicable contractual / legal
requirement. Shorten only with explicit written approval from the Compliance
Lead.

---

## 7. Access-Reason Logging & Minimum Necessary

- Every read or export of a PHI record MUST be accompanied by an
  `access_reason` captured in the audit log (see `operations/audit-evidence.md`
  §5).
- UI flows must encourage the "minimum necessary" amount of PHI per view
  (redact unused fields, avoid bulk defaults).
- Break-glass overrides are allowed only with heightened logging and a
  post-hoc review workflow.

---

## 8. Vendor / BAA Register

<!--
  AGENT INSTRUCTION: List every sub-processor or vendor that can receive or
  process PHI on behalf of the project. "BAA" here means the executed contract
  (Business Associate Agreement or local equivalent). Track evidence pointers
  externally (contracts repo / legal system) — do NOT paste contracts here.
-->

| Vendor | Service Used | PHI Received? | BAA / DPA Status | Effective Date | Next Review | Notes |
|---|---|---|---|---|---|---|
| [PLACEHOLDER] | [e.g., managed database] | ✅ / ❌ | executed / pending / n/a | [YYYY-MM-DD] | [YYYY-MM-DD] | [PLACEHOLDER] |

**Rule:** A vendor may not receive PHI until its BAA / DPA is `executed`.
Violations are a material incident and trigger `operations/incident-reports/`
filing.

---

## 9. De-Identification & Synthetic Data

- Non-production environments (dev, QA, staging) MUST NOT contain real PHI.
- Allowed approaches:
  1. **De-identification** — remove or transform the 18 HIPAA Safe Harbor
     identifiers (or the applicable local equivalent). Document the method,
     date, and reviewer. Retain a mapping ONLY if re-identification is
     explicitly required for a documented purpose, and store the mapping
     separately with stricter access control.
  2. **Synthetic data** — generated data that statistically resembles PHI
     without deriving from real patients. Document the generator, seed policy,
     and verification that no real patient is recoverable.
- Fixtures committed to this repository MUST use synthetic data only.
- Any accidental commit of real PHI is an incident: file under
  `operations/incident-reports/`, rotate affected credentials, and trigger the
  repository-history remediation runbook.

---

## 10. Data Residency

| Region / Jurisdiction | Allowed? | Rationale |
|---|---|---|
| [PLACEHOLDER — e.g., APAC — HK] | ✅ | Primary processing region |
| [PLACEHOLDER — e.g., US] | ❌ / ✅ | [PLACEHOLDER — contractual requirement] |

- Data residency constraints are enforced at the infrastructure layer (see
  `design/infrastructure-design.md`).
- Cross-region replication must be documented and approved.
- A residency change is a `High` impact ADR (see `project/decision-log.md`).

---

## 11. Downtime, Business Continuity & Disaster Recovery

| Scenario | RPO | RTO | Playbook |
|---|---|---|---|
| Single-AZ failure | [PLACEHOLDER] | [PLACEHOLDER] | `design/resilience-design.md` |
| Region failure | [PLACEHOLDER] | [PLACEHOLDER] | `design/resilience-design.md` |
| Ransomware / destructive incident | [PLACEHOLDER] | [PLACEHOLDER] | `operations/incident-reports/` + playbook |
| Extended maintenance window | n/a (planned) | [PLACEHOLDER] | `operations/deployment-runbook.md` |

- Restore drills MUST occur at least annually. File the drill as an
  operational-log entry with result and lessons learned.

---

## 12. Incident Response for PHI Exposure

- Any suspected PHI exposure triggers a `P0` or `P1` incident (see
  `operations/incident-reports/README.md` severity table).
- The post-mortem MUST include: affected record count (or explicit
  "unknown"), time window, containment timestamp, notification decision, and
  corrective actions.
- Notification obligations are determined by legal counsel and by customer
  contracts — this document does not replace legal review.

---

## 13. Admin Portal Healthcare-Readiness Fields

The Admin Portal extracts these SAFE fields from this document:

| Portal Field | Source |
|---|---|
| `phi_scope` | §2 Applicability |
| `phi_classification_last_reviewed` | §2 |
| `data_flow_documented` | §5 table populated (non-placeholder) |
| `retention_documented` | §6 table populated |
| `access_reason_enforced` | §7 acceptance |
| `baa_register_current` | §8 — all PHI-receiving vendors have `executed` BAA |
| `de_identification_policy` | §9 acceptance |
| `data_residency_documented` | §10 table populated |
| `bcp_dr_documented` | §11 table populated |
| `ir_playbook_pointer` | §12 pointer present |

No payloads — no patient data, contract text, or log content — are read from
this repository.

---

## 14. Healthcare Readiness Acceptance Checklist

- [ ] PHI scope (§2) is explicitly set to Yes or No with review date.
- [ ] Every data element is classified (§4).
- [ ] Every PHI flow is documented (§5) and encrypted in transit.
- [ ] Retention periods (§6) meet the longest applicable obligation.
- [ ] Access-reason logging is enforced for every PHI read/export (§7 and
      `operations/audit-evidence.md`).
- [ ] Every vendor receiving PHI has an executed BAA/DPA (§8).
- [ ] Non-prod uses only de-identified or synthetic data (§9).
- [ ] Data residency constraints are documented and enforced (§10).
- [ ] BCP/DR RPO/RTO and drill cadence are documented (§11).
- [ ] PHI-exposure incident playbook is in place (§12).
- [ ] This overlay is re-verified in every release evidence pack
      (`project/release-evidence-pack.md`).

---

## 15. Disclaimer

This overlay documents **healthcare readiness** and gathers **compliance
evidence**. It does not assert HIPAA, HITECH, HITRUST, or other regulatory
compliance on behalf of the project. Formal compliance assessment requires
qualified counsel and, where applicable, independent assessors.

---

## 16. Cross-References

- [`project/compliance-controls.md`](../project/compliance-controls.md) — Control catalog.
- [`project/admin-portal-validation.md`](../project/admin-portal-validation.md) — Validation rules and evidence fields.
- [`project/release-evidence-pack.md`](../project/release-evidence-pack.md) — Per-release evidence pack.
- [`operations/audit-evidence.md`](audit-evidence.md) — Audit log export and retention.
- [`design/security-design.md`](../design/security-design.md) — Security controls.
- [`design/resilience-design.md`](../design/resilience-design.md) — BCP/DR design.
