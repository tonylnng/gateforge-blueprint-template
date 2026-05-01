# Operations Directory

<!-- AGENT INSTRUCTION: This README provides an overview of the operations/ directory.
     The Operator agent (VM-5) is the primary producer of documents in this directory.
     The System Architect reviews all operations documents for consistency. -->

> **First action for the Operator:** open [`operations/AGENTS.md`](AGENTS.md) and complete the Pre-Flight Acknowledgement before any deploy or operational entry. Per [`/VERSIONING.md`](../VERSIONING.md), every change — including doc-only edits — must be pushed to GitHub first; the auto-bump CI writes the version.

## Purpose

The `operations/` directory contains all operational documentation for the GateForge platform. This includes deployment procedures, operational logs, incident reports, and service-level tracking. These documents ensure the platform is deployed, monitored, and maintained according to established standards.

## Directory Contents

| File / Folder | Description |
|---|---|
| `deployment-runbook.md` | Step-by-step deployment procedures for all environments (Dev, UAT, Production), including pre/post-deployment checklists and rollback procedures |
| `deployment-log.md` | Running log of all deployments with version, status, and configuration details |
| `operation-log.md` | Running log of all operational events — maintenance, scaling, config changes, security patches, etc. |
| `sla-slo-tracking.md` | Service Level Indicators, Objectives, and Agreement tracking based on SRE principles |
| `incident-reports/` | Individual incident reports following ITIL incident management standards |

## Ownership

| Role | Responsibility |
|---|---|
| **Operator (VM-5)** | Produces and maintains all operations documents. Executes deployments, logs operational events, files incident reports, and tracks SLI/SLO metrics |
| **System Architect** | Reviews operations documents for accuracy and completeness. Approves deployment runbook changes and SLO targets |

## Workflow

1. **Deployment Flow**: The Operator follows `deployment-runbook.md` for every deployment. Each deployment is recorded in `deployment-log.md` with full traceability (commit SHA, image tags, config changes).
2. **Operational Events**: Any operational event (maintenance, scaling, config change, certificate rotation, backup, failover, security patch) is logged in `operation-log.md`.
3. **Incident Management**: When an incident occurs, the Operator creates a new incident report in `incident-reports/` following the `INC-<NNN>.md` naming convention. The report follows ITIL standards including root cause analysis, timeline, and action items.
4. **SLA/SLO Tracking**: The Operator updates `sla-slo-tracking.md` monthly with reliability metrics, error budget consumption, and burn rate analysis.

## Cross-References

- **[MONITORING-OPERATIONS-GUIDE.md](../MONITORING-OPERATIONS-GUIDE.md)** — Comprehensive guide for monitoring infrastructure, alerting rules, and operational procedures
- **[design/monitoring-alerting-design.md](../design/monitoring-alerting-design.md)** — Monitoring and alerting system design
- **[design/infrastructure-design.md](../design/infrastructure-design.md)** — Infrastructure architecture and environment topology
- **[project/status.md](../project/status.md)** — Current project status and active blockers

---

## Revision History

| Version | Date       | Author    | Changes |
|---------|------------|-----------|---------|
| 1.0     | [PLACEHOLDER] | Operator | Initial operations directory README. |
| 1.1     | 2026-05-01 | Operator + Architect | Added pointer to `operations/AGENTS.md` and `/VERSIONING.md` at top. |
