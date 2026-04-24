# Audit Evidence & Log Export

<!--
  AGENT INSTRUCTION: This document describes HOW the project produces, exports,
  retains, and surfaces audit evidence. It is a documentation artifact only —
  actual audit logs MUST NEVER be committed to this repository. Instead, this
  document points to the systems of record (SIEM, log store, object-storage
  bucket) and describes the fields that an auditor or the Admin Portal can
  expect to see.

  The Admin Portal reads this file to understand the audit-logging posture and
  to render the "Audit Evidence" panel. No log contents are read from the repo.

  OWNER: Operator
  REVIEWER: System Architect
-->

| Field | Value |
|---|---|
| **Document ID** | `OPS-AUDIT-001` |
| **Version** | `0.1.0` |
| **Status** | `Draft` |
| **Owner** | Operator |
| **Reviewer** | System Architect |
| **Last Updated** | `[PLACEHOLDER — YYYY-MM-DD]` |

---

## 1. Purpose

Describe how audit-relevant events are generated, captured, exported, and
retained for this project, and how compliance reviewers (and the Admin Portal)
locate this evidence.

**Rule:** This repository contains the **description** of audit evidence — not
the evidence itself. Never commit raw logs, exported CSVs, or samples
containing real identifiers.

---

## 2. Revision History

| Version | Date | Author | Change Summary |
|---|---|---|---|
| 0.1.0 | [PLACEHOLDER] | Operator | Initial audit evidence description |

---

## 3. Auditable Event Catalog

<!--
  AGENT INSTRUCTION: List the event categories that produce audit records. For
  each category, note whether it requires "access-reason" logging (e.g., any
  view of PHI). Add or remove categories as the system evolves.
-->

| Event Category | Examples | Access-Reason Required | Source System |
|---|---|---|---|
| Authentication | login, logout, MFA challenge, failed login | ❌ | auth-service |
| Authorization / Access | role grant/revoke, permission change | ❌ | auth-service, admin-service |
| Sensitive Record Access | view of PHI / PII record, report export | ✅ | record-service |
| Administrative Action | user create/disable, config change, feature flag toggle | ❌ | admin-service |
| Data Export | bulk download, report generation | ✅ (when PHI/PII) | report-service |
| Cryptographic Operation | key rotation, signing key use | ❌ | kms-proxy |
| System Operation | deploy, scale event, config reload | ❌ | operator / CI |
| Break-glass / Emergency Access | override of normal access controls | ✅ (mandatory + notification) | auth-service |

---

## 4. Minimum Audit Record Schema

<!--
  AGENT INSTRUCTION: Every audit record MUST contain these fields at minimum.
  Use de-identified examples only. Never put real values here.
-->

| Field | Type | Required | Notes |
|---|---|---|---|
| `event_id` | UUID | ✅ | Globally unique |
| `event_type` | string | ✅ | Matches §3 category |
| `occurred_at` | ISO-8601 UTC | ✅ | With millisecond precision |
| `actor_id` | string | ✅ | Internal user ID (never a raw name) |
| `actor_role` | string | ✅ | At the time of the event |
| `target_id` | string | Conditional | Required for record access / admin actions |
| `target_type` | string | Conditional | e.g., `patient_record`, `user_account` |
| `access_reason` | enum + free-text | Conditional | **Required** for PHI/PII access; values: `treatment`, `operations`, `patient_request`, `emergency`, `other` |
| `source_ip` | string | ✅ | Observed client IP; hashed if retained > 30 days |
| `request_id` | string | ✅ | Correlation with application logs |
| `outcome` | enum | ✅ | `success` / `denied` / `error` |
| `integrity_hash` | string | ✅ | Chained hash of prior record (tamper-evident) |

---

## 5. Access-Reason Logging

When a user views or exports a record classified as PHI or PII:

1. The UI/API MUST prompt for or carry an `access_reason`.
2. The backend MUST reject the operation when `access_reason` is missing in a
   PHI/PII scope.
3. The audit record MUST capture the reason verbatim and, when the reason is
   `other`, a mandatory free-text justification (no default/empty).
4. Break-glass events additionally notify a named security contact within the
   SLA defined in `operations/incident-reports/README.md`.

---

## 6. Transport, Storage, Export, and Retention

### 6.1 Transport

- All audit events are emitted over an authenticated, TLS-1.2+ channel.
- Local buffering is size- and time-bounded; buffers are encrypted at rest.

### 6.2 Storage

- Primary store: append-only, tamper-evident log store (e.g., WORM bucket,
  append-only SIEM index).
- Integrity: each record links to the prior record's hash; periodic digests
  are archived off-system.

### 6.3 Export

- Scheduled, signed exports to the long-term retention bucket (details captured
  in `design/infrastructure-design.md`, not here).
- Ad-hoc exports for audits are performed via the documented runbook and
  logged as their own audit events (`event_type = data_export`).

### 6.4 Retention

| Log Class | Minimum Retention | Notes |
|---|---|---|
| Authentication & administrative | [PLACEHOLDER — e.g., 1 year] | Align with policy / contract |
| Sensitive record access (PHI) | [PLACEHOLDER — e.g., 6 years] | Align with applicable regulation and contract |
| System/operational | [PLACEHOLDER — e.g., 90 days hot + 1 year cold] | Tune for cost |
| Break-glass / emergency | [PLACEHOLDER — e.g., same as PHI] | Never shorter than PHI access retention |

**Retention must never be set below the longest applicable legal/contractual
requirement.** If this project is scoped for PHI, see
`operations/healthcare-readiness.md`.

---

## 7. Admin Portal Integration

The Admin Portal reads ONLY safe metadata from this document:

- Whether each §3 category is covered (✅ / ❌).
- Whether access-reason logging is enabled for PHI-scoped categories.
- The retention table in §6.4 (documented values, not actual log data).
- Pointers to the systems of record (by name, not by URL with credentials).

The Admin Portal does **not** fetch log contents from this repository. Live
audit-log inspection is performed in the SIEM / log store by authorized
personnel.

---

## 8. Acceptance Checklist

- [ ] Every event category in §3 either has a source system listed or is
      explicitly marked non-applicable with rationale.
- [ ] Minimum schema (§4) is implemented in all emitting services.
- [ ] Access-reason logging is enforced for every PHI/PII read and export.
- [ ] Integrity-hash chaining is enabled and verified during exports.
- [ ] Retention values in §6.4 meet or exceed the longest applicable obligation.
- [ ] Break-glass events trigger the documented notification within SLA.
- [ ] This document is re-verified as part of every release evidence pack
      (`project/release-evidence-pack.md`).
- [ ] No real log data, identifiers, or sample exports are committed to the
      repository.

---

## 9. Cross-References

- [`project/compliance-controls.md`](../project/compliance-controls.md) — Control catalog (CTRL-AU-*, CTRL-AC-*).
- [`project/admin-portal-validation.md`](../project/admin-portal-validation.md) — Validation rules and evidence fields.
- [`operations/healthcare-readiness.md`](healthcare-readiness.md) — Healthcare overlay (PHI retention, de-identification).
- [`design/security-design.md`](../design/security-design.md) — Authentication, authorization, encryption.
- [`design/monitoring-design.md`](../design/monitoring-design.md) — Observability and alerting on audit events.
