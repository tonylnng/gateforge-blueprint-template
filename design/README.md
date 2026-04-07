# Design Documents — GateForge Blueprint Repository

<!-- 
  This README provides an overview of the design/ directory.
  It is the entry point for any agent or human navigating the design documentation.
  Keep this file updated whenever a design document is added, removed, or significantly changed.
-->

## Overview

The `design/` directory contains detailed design specifications that translate the System Architect's high-level architecture into implementable infrastructure, security, resilience, database, and monitoring blueprints. These documents are the primary output of the **System Designer** and serve as the bridge between architecture decisions and operational implementation.

All design documents follow GateForge template conventions: metadata tables, Mermaid diagrams, example table rows, and HTML comment instructions for agents.

---

## Document Inventory

| Document                     | Description                                                                                      |
|------------------------------|--------------------------------------------------------------------------------------------------|
| `infrastructure-design.md`   | Kubernetes cluster architecture, namespace design, Docker image strategy, CI/CD pipeline, network and storage design, environment configuration |
| `security-design.md`         | OWASP-aligned threat model (STRIDE), authentication/authorization architecture, network security policies, secrets management, TLS, security headers, incident response |
| `resilience-design.md`       | Circuit breakers, retry policies, health checks, failover architecture, database HA, disaster recovery, chaos engineering test plan |
| `database-design.md`         | PostgreSQL configuration and tuning, schema design, migration strategy, index design, query baselines, backup/PITR, Redis schema, data integrity constraints |
| `monitoring-design.md`       | Prometheus/Grafana/Loki observability stack, metrics taxonomy, dashboards, alerting rules, SLI/SLO definitions, distributed tracing with OpenTelemetry |

---

## Ownership

| Role                | Responsibility                                                          |
|---------------------|-------------------------------------------------------------------------|
| **System Designer (VM-2)** | Owns all documents in `design/`. Creates, updates, and maintains design specifications. |
| **System Architect**       | Reviews and approves all design documents. Dispatches design tasks with context from `requirements/` and `architecture/`. |

---

## Workflow

```
1. Architect dispatches design task
   └─ Provides: requirements context, architecture decisions, constraints

2. System Designer reads inputs
   └─ requirements/*.md — functional and non-functional requirements
   └─ architecture/*.md — system architecture, data model, API specs
   └─ RESILIENCE-SECURITY-GUIDE.md — resilience and security patterns

3. System Designer produces design document
   └─ Fills in all [PLACEHOLDER] sections
   └─ Includes Mermaid diagrams, example table rows, rollback strategy
   └─ Ensures security assessment section is complete

4. Architect reviews and approves
   └─ Uses review checklist at the bottom of each document
   └─ Requests revisions or approves via status field in metadata table

5. Downstream consumers read approved designs
   └─ Developers (development/) — implement according to design specs
   └─ Operator (operations/) — deploy and operate according to infrastructure and monitoring design
   └─ QC Agents (qa/) — validate implementations against design specifications
```

---

## Mandatory Sections

Every design document in this directory **must** include:

1. **Document Metadata Table** — ID, version, owner, status, last updated, approved by
2. **Rollback Strategy** — Every design change must have a documented rollback path with RTO targets
3. **Security Assessment** — Risk-level evaluation of all design decisions with controls and status tracking
4. **Change Log** — Audit trail of all significant changes with date, description, impact, and rollback plan

---

## Cross-References

| Reference                        | Purpose                                                       |
|----------------------------------|---------------------------------------------------------------|
| `RESILIENCE-SECURITY-GUIDE.md`   | Detailed resilience and security implementation patterns       |
| `architecture/system-architecture.md` | High-level architecture decisions and C4 diagrams        |
| `architecture/data-model.md`     | Entity relationships and data model definitions               |
| `architecture/api-specs.md`      | API endpoint specifications and contracts                     |
| `requirements/nfr.md`            | Non-functional requirements (performance, availability, security targets) |
| `operations/runbooks/`           | Operational runbooks linked from monitoring alerting rules     |

---

## Conventions

- **Diagrams**: Use Mermaid syntax for all architectural diagrams
- **Placeholders**: Mark incomplete sections with `[PLACEHOLDER — description]`
- **Agent instructions**: Use HTML comments `<!-- -->` for instructions invisible in rendered view
- **Tables**: Include at least one example row to demonstrate expected format
- **Status tracking**: Use metadata table status field: `Draft → In Review → Approved`
- **Versioning**: Follow semantic versioning (MAJOR.MINOR.PATCH) for document versions

<!-- 
  MAINTENANCE NOTE:
  Update this README whenever:
  - A new design document is added to this directory
  - A document is significantly restructured
  - Ownership or workflow changes
-->
