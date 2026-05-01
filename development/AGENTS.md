# Development — Agent Compliance Manifest

<!--
  AGENT INSTRUCTION: Mandatory entry point for Developer agents. Every push
  that modifies code or files under development/ MUST come with the Pre-Flight
  Acknowledgement in §3 and pass the gates in §4. Code changes that bypass
  this manifest fail Admin Portal validation and block release.
-->

| Field | Value |
|---|---|
| **Document ID** | `DEV-AGENTS-001` |
| **Version** | `1.0` |
| **Status** | `Approved` |
| **Owner** | System Architect (rules) / Developers (compliance) |
| **Read By** | All Developer agents |
| **Last Updated** | 2026-05-01 |

---

## 1. Mandatory Reading

| # | Document | Purpose |
|---|---|---|
| 1 | [`/VERSIONING.md`](../VERSIONING.md) | Every push bumps a version — know how. |
| 2 | [`/README.md`](../README.md) | Repository master guide. |
| 3 | [`/project/admin-portal-validation.md`](../project/admin-portal-validation.md) | Validation rules. |
| 4 | This file (`development/AGENTS.md`) | Role-specific compliance. |
| 5 | [`development/coding-standards.md`](coding-standards.md) | Naming, file structure, lint rules. |
| 6 | [`requirements/functional-requirements.md`](../requirements/functional-requirements.md) | The FR the code implements. |
| 7 | [`architecture/technical-architecture.md`](../architecture/technical-architecture.md) | Module boundaries and contracts. |
| 8 | [`architecture/data-model.md`](../architecture/data-model.md) | Entities and indexes. |
| 9 | Relevant `architecture/api-specifications/*.openapi.yaml` | API contract you must honor. |
| 10 | All `design/*.md` documents that touch your module | Security / resilience / monitoring patterns to apply. |
| 11 | [`development/modules/<your-module>.md`](modules/) | Per-module change log and contracts. |
| 12 | [`qa/test-plan.md`](../qa/test-plan.md) | What tests will validate your code. |

---

## 2. Pre-Flight Acknowledgement

```markdown
## Pre-Flight Acknowledgement
- Role: Developer
- Task: <FR-MOD-NNN — short description>
- Module: <module-name>
- Docs read (with version):
  - VERSIONING.md v____
  - README.md v____
  - project/admin-portal-validation.md v____
  - development/AGENTS.md v____
  - development/coding-standards.md v____
  - requirements/functional-requirements.md v____
  - architecture/technical-architecture.md v____
  - architecture/data-model.md v____
  - architecture/api-specifications/<service>.openapi.yaml v____
  - design/security-design.md v____
  - design/resilience-design.md v____
  - design/monitoring-design.md v____
  - development/modules/<module>.md v____
  - qa/test-plan.md v____
- Mandatory gates honored:
  - [ ] Every committed function maps to an FR-<MOD>-NNN cited in code comments
  - [ ] Lint + format pass (no warnings)
  - [ ] Unit tests added or updated for every changed function (≥ 95% line coverage on the diff)
  - [ ] OpenAPI contract not broken (run contract tests)
  - [ ] Security: input validation + auth checks present per security-design.md
  - [ ] Resilience: outbound calls wrapped in the pattern from resilience-design.md
  - [ ] Monitoring: new metric / log statement matches monitoring-design.md taxonomy
  - [ ] Module doc updated with any new endpoint, event, or config key
  - [ ] Revision History row added in every modified Markdown file
```

---

## 3. Mandatory Gates

| ID | Gate | Source |
|---|---|---|
| DEV-G1 | Every committed function/method/handler cites the FR-<MOD>-NNN it implements (in a comment or PR description) | `requirements/functional-requirements.md` |
| DEV-G2 | Lint and format pass (no warnings) | `development/coding-standards.md` |
| DEV-G3 | Unit-test coverage ≥ 95% on the diff | `qa/README.md` quality gates |
| DEV-G4 | OpenAPI contract tests pass — no breaking changes without ADR + version bump on the spec | `architecture/api-specifications/README.md` |
| DEV-G5 | Security controls (input validation, authn, authz) present per `security-design.md` | `design/security-design.md` |
| DEV-G6 | Outbound dependencies use the chosen resilience pattern (circuit breaker / retry / timeout) | `design/resilience-design.md` |
| DEV-G7 | New metrics, logs, traces follow the taxonomy in `monitoring-design.md` | `design/monitoring-design.md` |
| DEV-G8 | `development/modules/<module>.md` updated to reflect the change | `development/README.md` |
| DEV-G9 | Revision History row in every modified Markdown file; `Version` field bumped | admin-portal-validation §3.3 |

---

## 4. Commit Convention

Prefix: `[Dev]`

| Change | Type | Version impact |
|---|---|---|
| Implement a new feature | `feat` | MINOR |
| Fix a bug or defect | `fix` | PATCH |
| Internal refactor (no behavior change) | `refactor` | PATCH |
| Update / add unit / integration tests only | `test` | PATCH |
| Update module doc only | `docs` | PATCH |
| Toolchain / dependency / config | `chore` | PATCH |

Security-related fixes use the `(security)` scope to land in the **Security**
CHANGELOG section: `[Dev] fix(security): patch JWT refresh replay vector`.

---

## 5. Failure Modes & Self-Recovery

| Symptom | Likely cause | Fix |
|---|---|---|
| `agent.preflight.present` red | PR description missing or has empty checkboxes | Fill in fully and re-push |
| `blueprint.traceability.completeness` red | Code lacks FR citation | Add comment `// Implements FR-AUTH-007` or note in PR |
| Coverage drop on diff | New code lacks unit tests | Add tests; re-push |
| Contract test red | Breaking OpenAPI change | Either revert, or add ADR + bump spec version |

---

## Revision History

| Version | Date       | Author            | Change Summary |
|---------|------------|-------------------|----------------|
| 1.0     | 2026-05-01 | System Architect  | Initial development compliance manifest. |
