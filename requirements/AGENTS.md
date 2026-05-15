# Requirements — Agent Compliance Manifest

<!--
  AGENT INSTRUCTION: This is the MANDATORY ENTRY POINT for the System Architect
  whenever they touch any file under requirements/. The Architect MUST read every
  document listed in §2 in order, MUST produce the Pre-Flight Acknowledgement
  in §3 before any commit on a requirements task, and MUST honor every gate in
  §4. Skipping any of this fails the Admin Portal validation
  ('agent.preflight.present' and 'blueprint.traceability.completeness').
-->

| Field | Value |
|---|---|
| **Document ID** | `REQ-AGENTS-001` |
| **Version** | `1.0` |
| **Status** | `Approved` |
| **Owner** | System Architect |
| **Read By** | System Architect (primary) |
| **Last Updated** | 2026-05-01 |

---

## 1. Why This File Exists

QC, Ops, and Architecture all consume requirements. If a requirement is wrong,
ambiguous, or missing a traceability link, every downstream artifact inherits
the defect. Earlier in this project we had an instance where a separately-owned
QA doc (`qa/test-plan.md`) was ignored by the QC agent because there was no
gate forcing the agent to read it. This `AGENTS.md` pattern is the cure: every
role gets a single mandatory entry point, and the auto-validator blocks pushes
that don't honor it.

---

## 2. Mandatory Reading (in order, every time)

The System Architect MUST read these documents — top to bottom — before adding
or modifying any file under `requirements/`:

| # | Document | Purpose |
|---|---|---|
| 1 | [`/VERSIONING.md`](../VERSIONING.md) | The version-bump rules. Every push bumps a version; you must understand why. |
| 2 | [`/README.md`](../README.md) | Repository master guide, ownership matrix, naming. |
| 3 | [`/project/admin-portal-validation.md`](../project/admin-portal-validation.md) §3, §4 | Validation rules and the canonical traceability model. |
| 4 | This file (`requirements/AGENTS.md`) | Role-specific compliance checklist. |
| 5 | [`requirements/user-requirements.md`](user-requirements.md) | Existing user stories — read before adding new ones to avoid duplicates. |
| 6 | [`requirements/functional-requirements.md`](functional-requirements.md) | Existing FRs — needed to assign the next FR ID and link new US → FR. |
| 7 | [`requirements/non-functional-requirements.md`](non-functional-requirements.md) | Existing NFRs and quality targets — needed when a new requirement implies new NFRs. |
| 8 | [`/project/decision-log.md`](../project/decision-log.md) | Active ADRs — a new requirement may invalidate an ADR. |

---

## 3. Pre-Flight Acknowledgement (must appear in your PR description)

Copy this block into the PR description **filled in**. Empty boxes fail validation.

```markdown
## Pre-Flight Acknowledgement
- Role: System Architect (Requirements task)
- Task: <one-line description>
- Docs read (with version):
  - VERSIONING.md v____
  - README.md v____
  - project/admin-portal-validation.md v____
  - requirements/AGENTS.md v____
  - requirements/user-requirements.md v____
  - requirements/functional-requirements.md v____
  - requirements/non-functional-requirements.md v____
  - project/decision-log.md v____
- Mandatory gates honored:
  - [ ] Every new US-NNN has at least one downstream FR linked
  - [ ] Every new FR-<MOD>-NNN cites the source US-NNN
  - [ ] NFR additions reference an ISO 25010 quality characteristic
  - [ ] No duplicate IDs introduced
  - [ ] Revision History row added in every modified file
```

---

## 4. Mandatory Gates (the Admin Portal will fail your push if any is violated)

| ID | Gate | Source of truth |
|---|---|---|
| REQ-G1 | Every new `US-NNN` links down to ≥ 1 `FR-*` | `project/admin-portal-validation.md` §3.6, §4.2 |
| REQ-G2 | Every new `FR-<MOD>-NNN` links up to a `US-NNN` (or has a documented "internal" tag) | §4.2 |
| REQ-G3 | New NFRs cite an ISO 25010 quality characteristic | §3, `requirements/non-functional-requirements.md` |
| REQ-G4 | All IDs match the regex in §3.4 | §3.4 |
| REQ-G5 | A Revision History row is added to every modified file, version field bumped | §3.3 |
| REQ-G6 | If a requirement contradicts an active ADR, the ADR is superseded in `project/decision-log.md` in the same PR | §4 |

---

## 5. Commit Convention

Use the prefix `[Architect]` and one of these types:

| Action | Type | Example |
|---|---|---|
| Add a new user story | `feat` | `[Architect] feat: add US-042 multi-tenant org switching` |
| Refine an existing FR | `refactor` | `[Architect] refactor: tighten FR-AUTH-007 wording on session timeout` |
| Fix a wrong NFR threshold | `fix` | `[Architect] fix: correct NFR-PERF-003 p95 latency target to 200ms` |
| Pure structural cleanup | `chore` | `[Architect] chore: reorder NFR table by category` |

Per [`/VERSIONING.md`](../VERSIONING.md):
- A `feat` push triggers a **MINOR** bump.
- Any other type triggers a **PATCH** bump.
- A MAJOR bump requires the End-user's `Version-Bump: major` trailer.

---

## 6. Failure Modes & Self-Recovery

| Symptom | Likely cause | Fix |
|---|---|---|
| Push rejected with "Pre-Flight missing" | PR description has empty checkboxes | Fill them in, push amended commit |
| `blueprint.traceability.completeness` red | New US has no FR child | Add the FR(s) and re-push |
| `blueprint.ids.regex` red | Wrong ID pattern (e.g. `FR-Auth-1`) | Use `FR-AUTH-001` |
| `blueprint.metadata.completeness` red | Forgot to bump `Version` field | Bump it; add Revision History row |

---

## Pre-Work Gate (MUST complete before implementation)

<!--
  AGENT INSTRUCTION: This gate prevents the "code first, document later" anti-pattern.
  Every checkbox below MUST be checked (with evidence) before you write ANY implementation
  code. The CI workflow prework-gate.yml enforces this — pushes with code changes but
  without prior doc commits will be rejected.
-->

Before writing ANY implementation code, the agent MUST have completed and committed:

- [ ] **GitHub Issues created** for all tasks in this iteration/feature
- [ ] **Requirements documented** (user-requirements.md and/or functional-requirements.md updated)
- [ ] **Architecture/design docs written** (technical-architecture.md, data-model.md, or design/*.md as applicable)
- [ ] **Feature spec written or updated** (docs/ specification document, if user-facing)
- [ ] **project/backlog.md updated** with task entries for this work
- [ ] **project/status.md updated** with current phase and iteration
- [ ] **All of the above pushed to GitHub** before the first code commit

**Enforcement:** The Pre-Work Gate CI workflow checks for these artifacts on every push
that includes implementation code. Missing artifacts → `agent.prework-gate.violated` →
`validation: red` → release blocked.

**Exception process:** If a hotfix requires skipping the gate, any agent may add
`Pre-Work-Gate: skip` as a commit trailer with a justification in the commit body.
The CI logs the exception (commit, author, and trailer) in the audit trail for
human review — abuse will be caught downstream and may revoke the agent's authority.


## Revision History

| Version | Date       | Author            | Change Summary |
|---------|------------|-------------------|----------------|
| 1.0     | 2026-05-01 | System Architect  | Initial requirements compliance manifest. Defines mandatory reading order, Pre-Flight Acknowledgement, six mandatory gates, and commit convention. |
| 1.1     | 2026-05-15 | System Architect  | Add Pre-Work Gate section (mandatory docs-before-code checklist) aligned with `.github/workflows/prework-gate.yml` and the README Mandatory Work Order. |
