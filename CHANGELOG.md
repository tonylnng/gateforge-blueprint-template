# Changelog

All notable changes to the GateForge project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- AGENT INSTRUCTION: This changelog follows the Keep a Changelog format.
     Every version section must include only the applicable subsections:
     Added, Changed, Deprecated, Removed, Fixed, Security.
     Delete empty subsections — do not leave blank headers.
     
     The [Unreleased] section accumulates changes as they are merged.
     When a release is cut, move items from [Unreleased] into a new version section.
     
     Always add the newest version directly below [Unreleased].
     Include the release date in ISO format: ## [X.Y.Z] - YYYY-MM-DD -->

---

## [Unreleased]

### Added
- [PLACEHOLDER — New features added since last release]

### Changed
- [PLACEHOLDER — Changes to existing functionality]

### Fixed
- [PLACEHOLDER — Bug fixes]

### Security
- [PLACEHOLDER — Security-related changes]

---

## [0.2.2] - 2026-05-12

### Chore
- [contributor] Add UI Auto-Test scaffolding under qa/ (Lane A + Lane B + headless Ubuntu)


---

## [0.2.1] - 2026-05-01

### Fixed
- [Architect] make bump parser tolerant of plain Conventional Commits


---

## [0.2.0] - 2026-05-01

### Added
- **Versioning policy** ([`VERSIONING.md`](VERSIONING.md)) — every change destined for any environment must be pushed to GitHub first; MAJOR is human-controlled (End-user only), MINOR and PATCH are auto-incremented by the AI agent based on commit types.
- **Root `VERSION` file** — single source of truth for the current repository version, written only by the auto-bump CI.
- **Auto-bump CI workflow** (`.github/workflows/version-bump.yml`) — runs on every push to every branch (including doc-only pushes), parses commit messages, updates `VERSION` and `CHANGELOG.md`, creates an annotated git tag.
- **Pull request template** (`.github/PULL_REQUEST_TEMPLATE.md`) — mandatory Pre-Flight Acknowledgement, change-type radio, expected version-bump declaration.
- **Per-role compliance manifests** — `requirements/AGENTS.md`, `architecture/AGENTS.md`, `design/AGENTS.md`, `development/AGENTS.md`, `qa/AGENTS.md`, `operations/AGENTS.md`, `project/AGENTS.md`. Each lists the mandatory reading order, the Pre-Flight Acknowledgement template, and role-specific gates. The QA manifest includes an explicit E2E gate (QA-G3) to address the recurring issue of QC agents skipping E2E tests.
- **Four-layer agent compliance enforcement** documented in `README.md`: mandatory entry point (`AGENTS.md`), Pre-Flight Acknowledgement, evidence-of-compliance citations, Admin Portal validation gates.
- **ADR-005** Versioning Policy and **ADR-006** Agent Compliance Enforcement appended to `project/decision-log.md`.

### Changed
- `README.md` — added Versioning Principle and Agent Compliance Enforcement sections; directory structure now lists every `AGENTS.md` and the new root governance files.
- `qa/test-plan.md` — mandatory E2E execution gate added to §7 Entry/Exit Criteria; deliverables checklist now requires evidence-of-compliance citations.
- `qa/README.md` — first-action pointer changed to `qa/AGENTS.md` so QC Agents always read the manifest first.
- `operations/deployment-runbook.md` — §1 Pre-Deployment Checklist now includes "GitHub push completed and version-bump CI green"; §2–4 reference the `VERSION` file as the deployment manifest.
- `operations/README.md` — first-action pointer changed to `operations/AGENTS.md`.
- `development/README.md`, `development/coding-standards.md` — reference the versioning policy and the dev `AGENTS.md`.
- `design/README.md`, `architecture/api-specifications/README.md` — reference the corresponding `AGENTS.md`.
- `project/admin-portal-validation.md` — added §3.7 with new validation rules: `versioning.semver.compliance`, `agent.preflight.present`, `agent.doc-citation.present`, `agent.test-coverage.gates`.
- `project/release-evidence-pack.md` — release packs now require a version-bump record and per-agent Pre-Flight Acknowledgements.
- `project/status.md` — added "Version after this push" and "Agents that filed Pre-Flight" fields.

### Pushed by
- System Architect (governance change)

---

## [0.1.0] - [PLACEHOLDER — YYYY-MM-DD]

### Added
- Project scaffolding and blueprint repository structure
- Core authentication module: user registration, login, JWT access/refresh tokens
- CI/CD pipeline (GitHub Actions) for automated testing and Docker image builds
- Development environment infrastructure (Kubernetes dev namespace, PostgreSQL, Redis)
- UAT environment setup with separate namespace and configuration
- Monitoring infrastructure: Prometheus metrics, Grafana dashboards, Loki log aggregation
- Blueprint documentation templates: requirements, architecture, design, development, QA, operations, project management
- Coding standards and development conventions document
- Deployment runbook for Dev, UAT, and Production environments

### Fixed
- Redis OOM issue in Dev environment — increased memory limit from 64Mi to 256Mi (INC-001)

---

<!-- AGENT INSTRUCTION: Template for new version entries — copy and fill in:

## [X.Y.Z] - YYYY-MM-DD

### Added
- [Description of new feature]

### Changed
- [Description of change to existing functionality]

### Deprecated
- [Description of soon-to-be-removed feature]

### Removed
- [Description of removed feature]

### Fixed
- [Description of bug fix]

### Security
- [Description of security fix or improvement]

-->

[Unreleased]: https://github.com/tonylnng/gateforge-blueprint-template/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/tonylnng/gateforge-blueprint-template/releases/tag/v0.2.0
[0.1.0]: https://github.com/tonylnng/gateforge-blueprint-template/releases/tag/v0.1.0
