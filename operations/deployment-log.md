# Deployment Log

<!-- AGENT INSTRUCTION: This is an append-only log. Never delete or modify past entries.
     The Operator agent (VM-5) adds a new entry for every deployment to any environment.
     Each deployment must have a row in the summary table AND a detail section for significant deployments. -->

| Field | Value |
|---|---|
| **Document ID** | OPS-DEPLOY-LOG-001 |
| **Version** | 0.1.0 |
| **Owner** | Operator (VM-5) |
| **Status** | Living Document |
| **Last Updated** | [PLACEHOLDER] |

---

## Deployment History

<!-- AGENT INSTRUCTION: Add a new row for every deployment. Use sequential Deploy IDs (DEP-001, DEP-002, etc.).
     Status values: success, failed, rolled-back, in-progress.
     Duration is wall-clock time from deploy start to post-deploy verification complete. -->

| Deploy ID | Date | Version | Environment | Status | Deployer | Duration | Notes |
|---|---|---|---|---|---|---|---|
| DEP-001 | 2026-03-15 | v0.1.0-rc.1 | Dev | success | VM-5 | 8m | Initial infrastructure deployment |
| DEP-002 | 2026-03-18 | v0.1.0-rc.1 | UAT | success | VM-5 | 12m | First UAT deployment, all smoke tests passed |
| DEP-003 | 2026-03-20 | v0.1.0-rc.1 | Dev | rolled-back | VM-5 | 15m | DB migration failed — rolled back, see DEP-003 details |

<!-- AGENT INSTRUCTION: Add new rows above this comment. Keep reverse chronological order (newest first)
     if preferred, or chronological. Be consistent. -->

---

## Deployment Details

<!-- AGENT INSTRUCTION: Create a detail section for every production deployment and any deployment
     that encountered issues. Minor dev deployments may omit the detail section. -->

### DEP-001 — v0.1.0-rc.1 → Dev

| Field | Value |
|---|---|
| **Deploy ID** | DEP-001 |
| **Date/Time** | 2026-03-15 14:30 HKT |
| **Commit SHA** | `a1b2c3d` |
| **Image Tags** | `api:a1b2c3d`, `web:a1b2c3d` |
| **Config Changes** | Initial environment variables set, Redis connection configured |
| **Test Results Link** | [CI Run #42](https://ci.gateforge.dev/runs/42) |
| **Issues Encountered** | None |
| **Rollback Performed** | No |

---

### DEP-002 — v0.1.0-rc.1 → UAT

| Field | Value |
|---|---|
| **Deploy ID** | DEP-002 |
| **Date/Time** | 2026-03-18 10:00 HKT |
| **Commit SHA** | `a1b2c3d` |
| **Image Tags** | `api:v0.1.0-rc.1`, `web:v0.1.0-rc.1` |
| **Config Changes** | UAT database connection string, UAT Redis endpoint |
| **Test Results Link** | [CI Run #45](https://ci.gateforge.dev/runs/45) |
| **Issues Encountered** | None |
| **Rollback Performed** | No |

---

### DEP-003 — v0.1.0-rc.1 → Dev (Rolled Back)

| Field | Value |
|---|---|
| **Deploy ID** | DEP-003 |
| **Date/Time** | 2026-03-20 16:15 HKT |
| **Commit SHA** | `e4f5g6h` |
| **Image Tags** | `api:e4f5g6h`, `web:e4f5g6h` |
| **Config Changes** | Added new environment variable `FEATURE_FLAG_NOTIFICATIONS=true` |
| **Test Results Link** | [CI Run #48](https://ci.gateforge.dev/runs/48) |
| **Issues Encountered** | Database migration `20260320_add_notifications_table` failed due to missing extension `uuid-ossp`. Migration script updated to include `CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`. |
| **Rollback Performed** | Yes — rolled back to DEP-001 state using `kubectl rollout undo` |

<!-- AGENT INSTRUCTION: For each new significant deployment, copy the template below and fill in details:

### DEP-XXX — vX.Y.Z → Environment

| Field | Value |
|---|---|
| **Deploy ID** | DEP-XXX |
| **Date/Time** | YYYY-MM-DD HH:MM HKT |
| **Commit SHA** | `xxxxxxx` |
| **Image Tags** | `api:tag`, `web:tag` |
| **Config Changes** | [PLACEHOLDER] |
| **Test Results Link** | [CI Run #N](https://ci.gateforge.dev/runs/N) |
| **Issues Encountered** | [PLACEHOLDER] |
| **Rollback Performed** | No / Yes — reason |

-->
