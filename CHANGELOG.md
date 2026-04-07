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

### Deprecated
- [PLACEHOLDER — Features that will be removed in future versions]

### Removed
- [PLACEHOLDER — Features removed in this release]

### Fixed
- [PLACEHOLDER — Bug fixes]

### Security
- [PLACEHOLDER — Security-related changes]

<!-- AGENT INSTRUCTION: Remove any subsection above that has no entries before releasing.
     Keep [Unreleased] section present at all times, even if empty. -->

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

[Unreleased]: https://github.com/gateforge/gateforge/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/gateforge/gateforge/releases/tag/v0.1.0
