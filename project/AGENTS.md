# Project — Agent Compliance Manifest

<!--
  AGENT INSTRUCTION: This is the cross-agent compliance manifest. The
  System Architect is the primary owner of project/, but every agent writes
  here whenever they file a status report, propose an ADR, or contribute to
  the release evidence pack. Use this manifest before any push that touches
  project/.
-->

| Field | Value |
|---|---|
| **Document ID** | `PRJ-AGENTS-001` |
| **Version** | `1.0` |
| **Status** | `Approved` |
| **Owner** | System Architect |
| **Read By** | All agents |
| **Last Updated** | 2026-05-01 |

---

## 1. Mandatory Reading

| # | Document | Purpose |
|---|---|---|
| 1 | [`/VERSIONING.md`](../VERSIONING.md) | Status reports, release entries, ADRs are versioned. |
| 2 | [`/README.md`](../README.md) | Master guide. |
| 3 | [`/project/admin-portal-validation.md`](admin-portal-validation.md) | Validation rules — this is the rulebook the portal enforces. |
| 4 | This file (`project/AGENTS.md`) | Cross-agent compliance. |
| 5 | [`project/backlog.md`](backlog.md) | Active work items. |
| 6 | [`project/decision-log.md`](decision-log.md) | All ADRs. New ADRs append here. |
| 7 | [`project/compliance-controls.md`](compliance-controls.md) | Control catalog. |
| 8 | [`project/release-evidence-pack.md`](release-evidence-pack.md) | Evidence-pack template per release. |
| 9 | [`project/status.md`](status.md) | Current status snapshot. |

---

## 2. Pre-Flight Acknowledgement

Use this minimal block when contributing to `project/` (any role).

```markdown
## Pre-Flight Acknowledgement
- Role: <Architect | Designer | Developer | QC | Operator>
- Task: <status report | ADR | release entry | backlog edit | compliance control update>
- Docs read (with version):
  - VERSIONING.md v____
  - README.md v____
  - project/admin-portal-validation.md v____
  - project/AGENTS.md v____
  - project/decision-log.md v____
  - project/release-evidence-pack.md v____
  - project/compliance-controls.md v____
- Mandatory gates honored:
  - [ ] If filing a status report, the agent's own role matches the file's owner section
  - [ ] New ADR uses ADR-NNN with the next free number
  - [ ] Release entries include the evidence-pack pointer
  - [ ] Compliance control changes record owner + last-reviewed date
  - [ ] Revision History row added in every modified file
```

---

## 3. Mandatory Gates

| ID | Gate | Source |
|---|---|---|
| PRJ-G1 | New ADRs use the next sequential `ADR-NNN` and follow the ADR template | `project/decision-log.md` template |
| PRJ-G2 | New release entry `RELEASE-vX.Y.Z` matches `VERSION` and a git tag | `/VERSIONING.md`, `project/release-evidence-pack.md` |
| PRJ-G3 | Status reports cite linked artifacts (FRs, defects, releases) | `project/status.md` |
| PRJ-G4 | Compliance control updates include owner, status, evidence link, last-reviewed date | `project/compliance-controls.md` |
| PRJ-G5 | Revision History bumped on every modified file | admin-portal-validation §3.3 |

---

## 4. Commit Convention

Each agent uses their own role prefix (`[Architect]`, `[Designer]`, `[Dev]`,
`[QC]`, `[Ops]`). Type follows the standard table in `/VERSIONING.md` §5.

Most project/ updates are `docs`, `chore`, or `feat` (when a new ADR or new
governance doc is introduced).

---

## Revision History

| Version | Date       | Author            | Change Summary |
|---------|------------|-------------------|----------------|
| 1.0     | 2026-05-01 | System Architect  | Initial cross-agent compliance manifest for project/. |
