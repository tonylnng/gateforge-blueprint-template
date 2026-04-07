# GateForge Blueprint Repository

<!-- 
  This README is the master guide for the GateForge Blueprint Repository.
  Every AI agent in the pipeline MUST read this file before performing any work.
  It defines the repository structure, ownership rules, workflows, and conventions.
-->

## What Is This Repository?

This repository is the **single source of truth** for a GateForge project. It contains every document that governs the software development lifecycle — from raw user requirements through architecture, design, development standards, QA artifacts, and operational runbooks.

**Key principle:** No agent operates from memory or assumption. Every decision, requirement, design choice, and test result is captured here in structured Markdown documents. If it's not in this repository, it doesn't exist.

**Owner:** Tony NG  
**Tech Stack:** TypeScript · React · NestJS · Docker · Redis · PostgreSQL · Kubernetes · React Native  
**Standards:** IEEE 830 · ISO 25010 · C4 Model · OWASP · IEEE 829 · ISTQB · SRE · ITIL · SemVer

---

## Directory Structure

```
gateforge-blueprint/
├── README.md                          # This file — master guide for the entire repository
├── requirements/
│   ├── user-requirements.md           # Raw user requirements captured from Tony (IEEE 830)
│   ├── functional-requirements.md     # Decomposed functional requirements per module
│   └── non-functional-requirements.md # Quality attributes and performance targets (ISO 25010)
├── architecture/
│   ├── technical-architecture.md      # System architecture using C4 model with Mermaid diagrams
│   ├── data-model.md                  # Entity-relationship model, schema DDL, indexing strategy
│   └── api-specifications/
│       ├── README.md                  # Guide for API spec files and OpenAPI conventions
│       └── *.openapi.yaml             # Per-service OpenAPI 3.0 specification files
├── design/
│   ├── infrastructure-design.md       # Cloud infrastructure, networking, resource provisioning
│   ├── security-design.md             # Authentication, authorization, encryption, OWASP controls
│   ├── resilience-design.md           # Circuit breakers, retries, fallbacks, chaos engineering
│   ├── database-design.md             # Query optimization, connection pooling, replication
│   └── monitoring-design.md           # Observability stack, alerting rules, dashboards
├── development/
│   ├── coding-standards.md            # Language-specific style guides and linting rules
│   ├── git-workflow.md                # Branching strategy, PR process, CI integration
│   └── modules/
│       └── <module-name>.md           # Per-module implementation documentation
├── qa/
│   ├── test-plan.md                   # Master test plan (IEEE 829)
│   ├── test-cases/
│   │   └── TC-<module>-<area>.md      # Test case files per module and area (ISTQB)
│   ├── test-reports/
│   │   └── TEST-REPORT-ITER-<NNN>-<scope>.md  # Test execution reports per iteration
│   ├── defects/
│   │   └── DEFECT-<NNN>.md            # Individual defect reports
│   └── metrics/
│       └── qa-dashboard.md            # Test coverage, defect density, pass rates
├── operations/
│   ├── deployment-runbook.md          # Step-by-step deployment procedures
│   ├── rollback-procedures.md         # Rollback steps for each service
│   ├── incident-reports/
│   │   └── INC-<NNN>.md              # Post-incident reports (ITIL)
│   ├── sla-tracking.md               # SLI/SLO/SLA definitions and compliance (SRE)
│   └── operational-logs/
│       └── OPS-LOG-<YYYY-MM-DD>.md   # Daily operational logs
└── project/
    ├── backlog.md                     # Product backlog with prioritized items
    ├── iterations/
    │   └── ITER-<NNN>.md             # Iteration plans and retrospectives
    ├── releases/
    │   └── RELEASE-<semver>.md       # Release notes per semantic version
    ├── decision-log.md               # Architectural and project decision records
    └── status-reports/
        └── STATUS-<YYYY-MM-DD>.md    # Weekly status reports from all agents
```

---

## Document Ownership

<!-- 
  This table defines which agent is the PRIMARY OWNER of each directory.
  The owner has write authority. Contributors may propose changes but the owner (or Architect) merges.
-->

| Directory | Owner Agent | Contributors | Purpose |
|-----------|------------|-------------|---------|
| `requirements/` | System Architect | — | User, functional, and non-functional requirements |
| `architecture/` | System Architect | System Designer | Technical architecture, data model, API specifications |
| `design/` | System Designer | Reviewed by Architect | Infrastructure, security, resilience, DB, monitoring design |
| `development/` | Developers | Reviewed by Architect | Coding standards, module documentation |
| `qa/` | QC Agents | Reviewed by Architect | Test plans, test cases, metrics, defect reports |
| `operations/` | Operator | Reviewed by Architect | Deployment, operation logs, incidents, SLA tracking |
| `project/` | System Architect | All agents report status | Backlog, iterations, releases, decision log, status |

**Rule:** Only the owner agent creates and modifies files in their directory. All other agents read from those directories. The System Architect has merge authority across all directories.

---

## Workflow: From Requirements to Delivery

<!-- 
  This is the canonical flow. Every project follows this sequence.
  Agents must not skip steps or work out of order.
-->

```mermaid
flowchart TD
    A[Tony NG provides requirements] --> B[System Architect captures in user-requirements.md]
    B --> C[Architect decomposes into functional-requirements.md]
    B --> D[Architect defines non-functional-requirements.md]
    C --> E[Architect creates technical-architecture.md]
    D --> E
    E --> F[Architect defines data-model.md & API specs]
    F --> G[System Designer creates design/ documents]
    G --> H[Developers implement per development/ standards]
    H --> I[QC Agents execute test plans from qa/]
    I --> J{All tests pass?}
    J -->|Yes| K[Operator deploys per operations/ runbook]
    J -->|No| L[Defects filed in qa/defects/]
    L --> H
    K --> M[Operator logs in operations/operational-logs/]
    M --> N[Architect updates project/ status]
```

### Step-by-Step

1. **Tony → Architect:** Tony provides business context, goals, and user stories. The Architect captures everything in `requirements/user-requirements.md`.
2. **Architect decomposes:** The Architect breaks user stories into module-level functional requirements (`requirements/functional-requirements.md`) and defines quality targets (`requirements/non-functional-requirements.md`).
3. **Architect designs architecture:** Using the C4 model, the Architect creates `architecture/technical-architecture.md`, `architecture/data-model.md`, and API specifications under `architecture/api-specifications/`.
4. **Designer details design:** The System Designer reads architecture documents and produces detailed designs in `design/` — infrastructure, security, resilience, database optimization, and monitoring.
5. **Developers implement:** Developers read requirements, architecture, and design documents. They follow `development/coding-standards.md` and document each module in `development/modules/`.
6. **QC validates:** QC Agents create test plans and test cases traceable to functional requirements. They execute tests and produce reports in `qa/test-reports/`.
7. **Operator deploys:** Once QC passes, the Operator follows `operations/deployment-runbook.md` to deploy, then tracks SLA compliance and logs operations.
8. **Architect governs:** Throughout the lifecycle, the Architect maintains `project/` — backlog, iterations, releases, decisions, and status.

---

## How to Use This Repository

### Starting a New Project

1. **Clone this template** into a new repository for your project.
2. **Architect fills requirements first** — start with `requirements/user-requirements.md` after Tony's briefing.
3. **Cascade through documents** in order: requirements → architecture → design → development → QA → operations.
4. **Never skip a document.** Each downstream document depends on its upstream inputs.

### For Each Agent

| Agent | First Action | Read From | Write To |
|-------|-------------|-----------|----------|
| System Architect | Capture Tony's requirements | Tony's briefing | `requirements/`, `architecture/`, `project/` |
| System Designer | Read architecture docs | `requirements/`, `architecture/` | `design/` |
| Developers | Read requirements + design | `requirements/`, `architecture/`, `design/` | `development/` |
| QC Agents | Read functional requirements | `requirements/`, `development/` | `qa/` |
| Operator | Read deployment design | `design/`, `operations/` | `operations/` |

---

## Naming Conventions

### File Naming

<!-- 
  Strict naming rules. Agents must follow these exactly.
  File names use UPPER-CASE prefixes with zero-padded sequence numbers.
-->

| File Type | Pattern | Example |
|-----------|---------|---------|
| Test report | `TEST-REPORT-ITER-<NNN>-<scope>.md` | `TEST-REPORT-ITER-001-auth.md` |
| Test case | `TC-<module>-<area>.md` | `TC-auth-login.md` |
| Defect report | `DEFECT-<NNN>.md` | `DEFECT-001.md` |
| Incident report | `INC-<NNN>.md` | `INC-001.md` |
| Iteration plan | `ITER-<NNN>.md` | `ITER-001.md` |
| Release notes | `RELEASE-<semver>.md` | `RELEASE-1.0.0.md` |
| Status report | `STATUS-<YYYY-MM-DD>.md` | `STATUS-2026-04-07.md` |
| Operational log | `OPS-LOG-<YYYY-MM-DD>.md` | `OPS-LOG-2026-04-07.md` |
| API specification | `<service-name>.openapi.yaml` | `auth-service.openapi.yaml` |
| Module documentation | `<module-name>.md` | `authentication.md` |

### Identifiers

| Entity | Format | Example |
|--------|--------|---------|
| User Story | `US-<NNN>` | `US-001` |
| Functional Requirement | `FR-<module>-<NNN>` | `FR-AUTH-001` |
| Non-Functional Requirement | `NFR-<category>-<NNN>` | `NFR-PERF-001` |
| Test Case | `TC-<module>-<NNN>` | `TC-AUTH-001` |
| Defect | `DEFECT-<NNN>` | `DEFECT-001` |
| Architecture Decision Record | `ADR-<NNN>` | `ADR-001` |

---

## Git Commit Message Conventions

<!-- 
  Each agent uses a prefix that identifies them in the git log.
  This makes it trivial to filter commits by agent.
-->

Every commit message follows this format:

```
[<Agent>] <type>: <short description>

<optional body with details>
```

### Agent Prefixes

| Agent | Prefix | Example Commit |
|-------|--------|----------------|
| System Architect | `[Architect]` | `[Architect] feat: add user-requirements for auth module` |
| System Designer | `[Designer]` | `[Designer] feat: add security-design document` |
| Developer | `[Dev]` | `[Dev] feat: implement authentication module` |
| QC Agent | `[QC]` | `[QC] test: add test cases for login flow` |
| Operator | `[Ops]` | `[Ops] deploy: release v1.0.0 to production` |

### Commit Types

| Type | Usage |
|------|-------|
| `feat` | New document or section added |
| `fix` | Correction to existing content |
| `refactor` | Restructure without changing meaning |
| `test` | Test plans, test cases, test reports |
| `deploy` | Deployment actions and runbook updates |
| `docs` | Meta-documentation (README, guides) |
| `chore` | Housekeeping (formatting, typos) |

---

## Version Control Rules

<!-- 
  Critical governance rules. The Architect is the gatekeeper.
  Other agents propose changes; only the Architect merges.
-->

### Merge Authority

- **The System Architect has sole merge authority** for all directories.
- Other agents propose changes by updating their owned files and flagging them in status reports.
- The Architect reviews, validates traceability, and merges.

### Change Proposal Process

1. **Agent updates their document** with proposed changes.
2. **Agent adds an entry** to the document's Revision History table.
3. **Agent reports the change** in their next status report (`project/status-reports/`).
4. **Architect reviews** the change for consistency with upstream documents.
5. **Architect merges** and updates the document version in the metadata table.

### Document Versioning

- Documents use `MAJOR.MINOR` versioning (e.g., `1.0`, `1.1`, `2.0`).
- **MAJOR** increments when the document's scope or structure changes significantly.
- **MINOR** increments for content additions, corrections, or refinements.
- Every version change requires a Revision History entry.

### Branching Strategy

- `main` — Always reflects the latest approved state of all documents.
- `iter/<NNN>` — Working branch for each iteration (e.g., `iter/001`).
- Agents work on the iteration branch. Architect merges to `main` at iteration close.

---

## Template Metadata Standard

Every document in this repository begins with a metadata table in this exact format:

```markdown
| Field | Value |
|-------|-------|
| **Document ID** | e.g., `REQ-USER-001` |
| **Version** | e.g., `0.1` |
| **Status** | `Draft` · `In Review` · `Approved` · `Deprecated` |
| **Owner** | Agent name |
| **Last Updated** | `YYYY-MM-DD` |
| **Approved By** | `—` until approved |
```

Status lifecycle: `Draft` → `In Review` → `Approved` → (optionally `Deprecated`)

---

## Quick Reference: Industry Standards

| Standard | Applied To | Key Documents |
|----------|-----------|---------------|
| IEEE 830 / ISO/IEC/IEEE 29148 | Requirements | `requirements/*.md` |
| ISO 25010 | Non-functional requirements | `requirements/non-functional-requirements.md` |
| C4 Model | Architecture | `architecture/technical-architecture.md` |
| OWASP | Security | `design/security-design.md` |
| IEEE 829 | Test documentation | `qa/test-plan.md` |
| ISTQB | Test cases | `qa/test-cases/*.md` |
| SRE (Google) | SLI/SLO/SLA | `operations/sla-tracking.md` |
| ITIL | Incident management | `operations/incident-reports/*.md` |
| Semantic Versioning | Releases | `project/releases/*.md` |
