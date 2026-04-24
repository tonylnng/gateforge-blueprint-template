# Compliance Controls Catalog

<!--
  AGENT INSTRUCTION: This document is the project's compliance control catalog.
  It enumerates the controls the Blueprint is expected to satisfy, identifies the
  owner of each control, points to the artifact that serves as evidence, and
  records the last review date. The Admin Portal reads this file to populate its
  "Compliance" tab.

  IMPORTANT: This is a "healthcare readiness" and general compliance scaffold. It
  is NOT a claim of HIPAA, HITRUST, SOC 2, or ISO 27001 certification. Certification
  is a formal external process. Use this catalog to gather compliance evidence
  that supports audits and readiness reviews.

  OWNER: System Architect
  REVIEW CADENCE: Quarterly (or on material change)
-->

| Field | Value |
|---|---|
| **Document ID** | `PRJ-COMPLIANCE-001` |
| **Version** | `0.1.0` |
| **Status** | `Living Document` |
| **Owner** | System Architect |
| **Last Updated** | `[PLACEHOLDER — YYYY-MM-DD]` |
| **Review Cadence** | Quarterly |

---

## 1. Purpose

Provide a single, auditable list of the compliance controls that apply to this
project, the owner accountable for each, and a pointer to the evidence that
demonstrates the control is in place. The Blueprint Repository is the
**compliance ledger**; the Admin Portal is its read-only dashboard.

---

## 2. Revision History

| Version | Date | Author | Change Summary |
|---|---|---|---|
| 0.1.0 | [PLACEHOLDER] | System Architect | Initial control catalog |

---

## 3. Control Domains

<!--
  AGENT INSTRUCTION: Scope this catalog to the domains that apply to your project.
  Mark non-applicable domains with status `N/A` and a one-line rationale.
-->

| Domain | Applies? | Rationale |
|---|---|---|
| Access Control & Authentication | ✅ | Platform has user accounts and privileged roles |
| Audit Logging | ✅ | Regulated data access must be traceable |
| Data Protection (encryption in transit/at rest) | ✅ | Default-on for all environments |
| Change Management | ✅ | All changes flow through PRs, ADRs, releases |
| Vulnerability & Patch Management | ✅ | Scans on every release |
| Backup & Recovery (BCP/DR) | ✅ | RPO/RTO defined in `design/resilience-design.md` |
| Incident Response | ✅ | Playbook in `operations/incident-reports/` |
| Vendor / Business Associate Management | Conditional | Required when handling PHI on behalf of a covered entity |
| Healthcare Readiness Overlay | Conditional | Required when the project handles PHI — see `operations/healthcare-readiness.md` |
| Data Residency | Conditional | Required when contracts or law restrict processing location |

---

## 4. Control Catalog

<!--
  AGENT INSTRUCTION: Add one row per control. `Status` values: `implemented`,
  `partial`, `planned`, `not-applicable`. `Evidence` MUST be a relative link to
  the artifact in this repository (or a named external register). Never embed
  the evidence payload itself here.
-->

| Control ID | Domain | Description | Owner | Status | Evidence | Last Reviewed |
|---|---|---|---|---|---|---|
| CTRL-AC-001 | Access Control | MFA required for all production administrative access | Operator | [PLACEHOLDER] | `design/security-design.md#mfa` | [PLACEHOLDER] |
| CTRL-AC-002 | Access Control | Role-based access control with least privilege, reviewed quarterly | System Architect | [PLACEHOLDER] | `design/security-design.md#rbac` | [PLACEHOLDER] |
| CTRL-AC-003 | Access Control | Access-reason logging for PHI/sensitive record views | Developers | [PLACEHOLDER] | `operations/audit-evidence.md#access-reason` | [PLACEHOLDER] |
| CTRL-AU-001 | Audit Logging | Immutable, append-only audit log for authentication, authorization, data access, and administrative actions | Operator | [PLACEHOLDER] | `operations/audit-evidence.md` | [PLACEHOLDER] |
| CTRL-AU-002 | Audit Logging | Audit logs exported to long-term retention store; in-repo logs prohibited | Operator | [PLACEHOLDER] | `operations/audit-evidence.md#export` | [PLACEHOLDER] |
| CTRL-DP-001 | Data Protection | TLS 1.2+ in transit; AES-256 at rest | System Designer | [PLACEHOLDER] | `design/security-design.md#encryption` | [PLACEHOLDER] |
| CTRL-DP-002 | Data Protection | PHI classification applied at field level; no PHI in logs, analytics, or non-prod | System Architect | [PLACEHOLDER] | `operations/healthcare-readiness.md#phi-classification` | [PLACEHOLDER] |
| CTRL-DP-003 | Data Protection | Non-prod environments use de-identified or synthetic data only | Developers | [PLACEHOLDER] | `operations/healthcare-readiness.md#de-identification` | [PLACEHOLDER] |
| CTRL-CM-001 | Change Management | All production changes merged via PR with Architect approval | System Architect | [PLACEHOLDER] | `README.md#version-control-rules` | [PLACEHOLDER] |
| CTRL-CM-002 | Change Management | Releases carry an evidence pack with linked requirements, tests, defects, ADRs | System Architect | [PLACEHOLDER] | `project/release-evidence-pack.md` | [PLACEHOLDER] |
| CTRL-VM-001 | Vulnerability Management | SAST + dependency scan on every PR; critical/high must be zero before release | QC Agents | [PLACEHOLDER] | `qa/test-plan.md` | [PLACEHOLDER] |
| CTRL-BR-001 | Backup & Recovery | Documented RPO/RTO, periodic restore drills | Operator | [PLACEHOLDER] | `design/resilience-design.md` | [PLACEHOLDER] |
| CTRL-IR-001 | Incident Response | Incident playbook; P0/P1 post-mortems within 5 business days | Operator | [PLACEHOLDER] | `operations/incident-reports/` | [PLACEHOLDER] |
| CTRL-VN-001 | Vendor Management | BAA / DPA register maintained for all sub-processors handling PHI or PII | System Architect | [PLACEHOLDER] | `operations/healthcare-readiness.md#vendor-register` | [PLACEHOLDER] |
| CTRL-DR-001 | Data Residency | Processing region(s) documented; data does not leave approved regions | System Designer | [PLACEHOLDER] | `design/infrastructure-design.md` | [PLACEHOLDER] |
| CTRL-HC-001 | Healthcare Readiness | Healthcare readiness overlay maintained and reviewed per release | System Architect | [PLACEHOLDER] | `operations/healthcare-readiness.md` | [PLACEHOLDER] |

<!--
  AGENT INSTRUCTION: Append new rows above this comment. Use sequential IDs per
  domain. If a control is retired, do not delete it — set Status to `not-applicable`
  and note the superseding control in the Description.
-->

---

## 5. Control Review Procedure

1. The System Architect schedules a quarterly review of this catalog.
2. Each row's Owner confirms `Status` and updates `Last Reviewed`.
3. Broken or stale `Evidence` links are fixed or replaced.
4. Any control that changed from `implemented` to `partial` or `planned` is
   flagged as a risk in `project/status.md` and, if material, recorded as an ADR.
5. The Admin Portal displays the review date and colour-codes rows older than
   one full cadence (`stale`).

---

## 6. Scope & Disclaimer

- This catalog captures **compliance evidence** and **healthcare readiness**.
- It is **not** a certification, attestation, or legal opinion.
- Specific regulatory obligations (e.g., HIPAA, GDPR, SOC 2) require the
  involvement of qualified counsel and, where applicable, independent auditors.
- Use terms like "healthcare readiness" and "compliance evidence" in
  user-facing artifacts; avoid claiming HIPAA (or equivalent) compliance.

---

## 7. Cross-References

- [`project/admin-portal-validation.md`](admin-portal-validation.md) — Validation rules and evidence fields.
- [`project/release-evidence-pack.md`](release-evidence-pack.md) — Per-release evidence pack.
- [`operations/audit-evidence.md`](../operations/audit-evidence.md) — Audit log export.
- [`operations/healthcare-readiness.md`](../operations/healthcare-readiness.md) — Healthcare overlay.
- [`design/security-design.md`](../design/security-design.md) — Security controls design.
