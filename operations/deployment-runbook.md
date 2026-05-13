# Deployment Runbook

<!-- AGENT INSTRUCTION: This runbook defines the exact steps for deploying GateForge to each environment.
     The Operator agent (VM-5) follows this runbook for every deployment.
     The System Architect must approve any changes to production deployment procedures.
     Keep commands exact and copy-pasteable. Update whenever infrastructure changes. -->

| Field | Value |
|---|---|
| **Document ID** | OPS-RUNBOOK-001 |
| **Version** | 0.1.0 |
| **Owner** | Operator (VM-5) |
| **Status** | Draft |
| **Last Updated** | [PLACEHOLDER] |
| **Approved By** | [PLACEHOLDER] |

---

## 1. Pre-Deployment Checklist

<!-- AGENT INSTRUCTION: Every item must be verified before ANY deployment begins. Do not skip items. -->

Complete **all** items before proceeding to deployment. Record pass/fail in the deployment log.

| # | Check | Verified |
|---|---|---|
| 1 | All unit tests pass (`npm run test:unit`) | ☐ |
| 2 | All integration tests pass (`npm run test:integration`) | ☐ |
| 3 | All E2E tests pass (`npm run test:e2e`) | ☐ |
| 4 | Docker images built successfully for all services | ☐ |
| 5 | Environment-specific configuration files reviewed and verified | ☐ |
| 6 | Database migration scripts tested against target environment snapshot | ☐ |
| 7 | Rollback procedure tested in staging/UAT | ☐ |
| 8 | API contract compatibility verified (no breaking changes without version bump) | ☐ |
| 9 | Security scan completed — no critical or high vulnerabilities | ☐ |
| 10 | Dependency audit passed (`npm audit --production`) | ☐ |
| 11 | Release notes / changelog updated | ☐ |
| 12 | Monitoring dashboards and alerts configured for new/changed metrics | ☐ |
| 13 | Stakeholder notification sent (for UAT/Production) | ☐ |

---

## 2. Deployment Procedure — Dev Environment

<!-- AGENT INSTRUCTION: Dev deployments are automated via CI/CD but can be triggered manually.
     No approval gate required for Dev. -->

### 2.1 Prerequisites

- Access to the Dev Kubernetes cluster
- Docker registry credentials configured
- `kubectl` context set to `gateforge-dev`

### 2.2 Steps

1. **Pull latest code and verify branch**
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **Build Docker images**
   ```bash
   docker compose -f docker-compose.dev.yml build
   ```

3. **Tag and push images to registry**
   ```bash
   docker tag gateforge/api:latest registry.gateforge.dev/api:$(git rev-parse --short HEAD)
   docker tag gateforge/web:latest registry.gateforge.dev/web:$(git rev-parse --short HEAD)
   docker push registry.gateforge.dev/api:$(git rev-parse --short HEAD)
   docker push registry.gateforge.dev/web:$(git rev-parse --short HEAD)
   ```

4. **Run database migrations**
   ```bash
   kubectl -n gateforge-dev exec deploy/api -- npx prisma migrate deploy
   ```

5. **Apply Kubernetes manifests**
   ```bash
   kubectl apply -f k8s/dev/ -n gateforge-dev
   ```

6. **Update image tags in deployment**
   ```bash
   kubectl -n gateforge-dev set image deployment/api api=registry.gateforge.dev/api:$(git rev-parse --short HEAD)
   kubectl -n gateforge-dev set image deployment/web web=registry.gateforge.dev/web:$(git rev-parse --short HEAD)
   ```

7. **Verify rollout**
   ```bash
   kubectl -n gateforge-dev rollout status deployment/api --timeout=300s
   kubectl -n gateforge-dev rollout status deployment/web --timeout=300s
   ```

8. **Run smoke tests**
   ```bash
   npm run test:smoke -- --env=dev
   ```

---

## 3. Deployment Procedure — UAT Environment

<!-- AGENT INSTRUCTION: UAT deployments require passing all integration tests.
     QC agent must confirm test suite completion before UAT deploy. -->

### 3.1 Prerequisites

- All Dev environment smoke tests passing
- QC agent sign-off on test results
- `kubectl` context set to `gateforge-uat`

### 3.2 Steps

1. **Checkout the release candidate tag**
   ```bash
   git checkout tags/v[PLACEHOLDER]-rc.N
   ```

2. **Build production-optimized Docker images**
   ```bash
   docker compose -f docker-compose.uat.yml build --no-cache
   ```

3. **Tag and push images**
   ```bash
   export VERSION=$(git describe --tags --abbrev=0)
   docker tag gateforge/api:latest registry.gateforge.dev/api:${VERSION}
   docker tag gateforge/web:latest registry.gateforge.dev/web:${VERSION}
   docker push registry.gateforge.dev/api:${VERSION}
   docker push registry.gateforge.dev/web:${VERSION}
   ```

4. **Backup UAT database**
   ```bash
   kubectl -n gateforge-uat exec deploy/postgres -- pg_dump -U gateforge gateforge_uat > backup_uat_$(date +%Y%m%d_%H%M%S).sql
   ```

5. **Run database migrations**
   ```bash
   kubectl -n gateforge-uat exec deploy/api -- npx prisma migrate deploy
   ```

6. **Apply Kubernetes manifests**
   ```bash
   kubectl apply -f k8s/uat/ -n gateforge-uat
   ```

7. **Update image tags**
   ```bash
   kubectl -n gateforge-uat set image deployment/api api=registry.gateforge.dev/api:${VERSION}
   kubectl -n gateforge-uat set image deployment/web web=registry.gateforge.dev/web:${VERSION}
   ```

8. **Verify rollout**
   ```bash
   kubectl -n gateforge-uat rollout status deployment/api --timeout=300s
   kubectl -n gateforge-uat rollout status deployment/web --timeout=300s
   ```

9. **Run full UAT test suite**
   ```bash
   npm run test:e2e -- --env=uat
   ```

10. **Notify QC agent for UAT validation**

---

## 4. Deployment Procedure — Production Environment

<!-- AGENT INSTRUCTION: Production deployments require explicit approval from the System Architect.
     Always perform during the designated maintenance window unless it is a hotfix.
     Blue-green or canary deployment strategy is recommended. -->

### 4.1 Approval Gate

| Approver | Approval Status | Date |
|---|---|---|
| System Architect | ☐ Approved | [PLACEHOLDER] |
| Project Owner (End-user) | ☐ Approved | [PLACEHOLDER] |

> **⚠ DO NOT PROCEED** without both approvals recorded above.

### 4.2 Prerequisites

- UAT sign-off completed
- All UAT test results documented in QA reports
- Production maintenance window scheduled and communicated
- On-call engineer identified and available
- Rollback procedure reviewed by deployer

### 4.3 Steps

1. **Checkout the release tag**
   ```bash
   git checkout tags/v[PLACEHOLDER]
   ```

2. **Build production Docker images**
   ```bash
   docker compose -f docker-compose.prod.yml build --no-cache
   ```

3. **Tag and push images**
   ```bash
   export VERSION=$(git describe --tags --exact-match)
   docker tag gateforge/api:latest registry.gateforge.prod/api:${VERSION}
   docker tag gateforge/web:latest registry.gateforge.prod/web:${VERSION}
   docker push registry.gateforge.prod/api:${VERSION}
   docker push registry.gateforge.prod/web:${VERSION}
   ```

4. **Create production database backup**
   ```bash
   kubectl -n gateforge-prod exec deploy/postgres -- pg_dump -U gateforge gateforge_prod | gzip > backup_prod_$(date +%Y%m%d_%H%M%S).sql.gz
   ```

5. **Enable maintenance mode (if required)**
   ```bash
   kubectl -n gateforge-prod set env deployment/web MAINTENANCE_MODE=true
   ```

6. **Run database migrations**
   ```bash
   kubectl -n gateforge-prod exec deploy/api -- npx prisma migrate deploy
   ```

7. **Deploy using canary strategy**
   ```bash
   # Deploy canary (10% traffic)
   kubectl apply -f k8s/prod/canary/ -n gateforge-prod
   # Monitor for 10 minutes — check error rates, latency
   # If healthy, proceed to full rollout
   kubectl apply -f k8s/prod/ -n gateforge-prod
   ```

8. **Update image tags**
   ```bash
   kubectl -n gateforge-prod set image deployment/api api=registry.gateforge.prod/api:${VERSION}
   kubectl -n gateforge-prod set image deployment/web web=registry.gateforge.prod/web:${VERSION}
   ```

9. **Verify rollout**
   ```bash
   kubectl -n gateforge-prod rollout status deployment/api --timeout=600s
   kubectl -n gateforge-prod rollout status deployment/web --timeout=600s
   ```

10. **Disable maintenance mode**
    ```bash
    kubectl -n gateforge-prod set env deployment/web MAINTENANCE_MODE=false
    ```

11. **Run production smoke tests**
    ```bash
    npm run test:smoke -- --env=prod
    ```

12. **Confirm monitoring dashboards are healthy**

13. **Send deployment completion notification**

---

## 5. Post-Deployment Verification Checklist

<!-- AGENT INSTRUCTION: Complete this checklist after EVERY deployment to ANY environment. -->

| # | Verification | Verified |
|---|---|---|
| 1 | Health check endpoints return 200 OK (`/health`, `/readiness`) | ☐ |
| 2 | Smoke tests pass (API responds, UI renders, auth flow works) | ☐ |
| 3 | Database connectivity confirmed | ☐ |
| 4 | Redis connectivity confirmed | ☐ |
| 5 | Background job processing verified (queue consumer active) | ☐ |
| 6 | Log aggregation receiving logs from new deployment | ☐ |
| 7 | Monitoring dashboards showing metrics from new pods | ☐ |
| 8 | Alert rules firing correctly (test alert if applicable) | ☐ |
| 9 | SSL/TLS certificates valid and not near expiry | ☐ |
| 10 | No elevated error rates in the first 15 minutes post-deploy | ☐ |

---

## 6. Rollback Procedure

<!-- AGENT INSTRUCTION: Rollback must be executable within 5 minutes.
     If any post-deployment verification fails, initiate rollback immediately. -->

### 6.1 Decision Criteria — When to Rollback

Initiate rollback if **any** of the following occur:

- Health check endpoints fail after deployment
- Error rate exceeds 5% within 15 minutes of deployment
- p95 latency exceeds 2x baseline within 15 minutes
- Smoke tests fail on critical paths (auth, core CRUD operations)
- Data integrity issues detected
- Customer-facing errors reported

### 6.2 Rollback Steps

1. **Identify the previous stable deployment revision**
   ```bash
   kubectl -n gateforge-<env> rollout history deployment/api
   kubectl -n gateforge-<env> rollout history deployment/web
   ```

2. **Roll back deployments**
   ```bash
   kubectl -n gateforge-<env> rollout undo deployment/api
   kubectl -n gateforge-<env> rollout undo deployment/web
   ```

3. **Verify rollback**
   ```bash
   kubectl -n gateforge-<env> rollout status deployment/api --timeout=300s
   kubectl -n gateforge-<env> rollout status deployment/web --timeout=300s
   ```

4. **Roll back database migrations (if applicable)**
   ```bash
   # Only if the migration is not backward-compatible
   kubectl -n gateforge-<env> exec deploy/api -- npx prisma migrate resolve --rolled-back <migration_name>
   # Or restore from backup:
   kubectl -n gateforge-<env> exec -i deploy/postgres -- psql -U gateforge gateforge_<env> < backup_<env>_<timestamp>.sql
   ```

5. **Run smoke tests to confirm rollback**
   ```bash
   npm run test:smoke -- --env=<env>
   ```

6. **Log rollback in deployment log** with reason and impact

7. **Create incident report** if rollback was in Production

---

## 7. Hotfix Deployment Procedure

<!-- AGENT INSTRUCTION: Hotfix path bypasses normal release cycle but still requires
     Architect approval for Production. Hotfixes must be merged back into develop. -->

### 7.1 When to Use

- Critical production bug affecting >10% of users
- Security vulnerability with active exploitation
- Data corruption or integrity issue

### 7.2 Steps

1. **Create hotfix branch**
   ```bash
   git checkout -b hotfix/v<X.Y.Z+1> tags/v<X.Y.Z>
   ```

2. **Apply fix, commit, and push**
   ```bash
   git add .
   git commit -m "hotfix: <description>"
   git push origin hotfix/v<X.Y.Z+1>
   ```

3. **Run critical test suite (abbreviated)**
   ```bash
   npm run test:unit
   npm run test:smoke
   ```

4. **Get emergency approval** — System Architect verbal/written approval (document in Slack or decision log)

5. **Deploy to Production** following Section 4 steps (skip UAT if Architect approves)

6. **Merge hotfix back into develop**
   ```bash
   git checkout develop
   git merge hotfix/v<X.Y.Z+1>
   git push origin develop
   ```

7. **Tag the hotfix release**
   ```bash
   git tag v<X.Y.Z+1>
   git push origin v<X.Y.Z+1>
   ```

8. **Create incident report** documenting the hotfix trigger, fix, and verification

---

## 8. Environment Configuration

<!-- AGENT INSTRUCTION: Update this table whenever environment configuration changes.
     Secrets must NEVER appear in this document — only reference the secrets source. -->

| Field | Dev | UAT | Production |
|---|---|---|---|
| **URL** | `https://dev.gateforge.dev` | `https://uat.gateforge.dev` | `https://app.gateforge.com` |
| **API URL** | `https://api-dev.gateforge.dev` | `https://api-uat.gateforge.dev` | `https://api.gateforge.com` |
| **DB Host** | `postgres-dev.internal` | `postgres-uat.internal` | `postgres-prod.internal` |
| **DB Name** | `gateforge_dev` | `gateforge_uat` | `gateforge_prod` |
| **Redis Host** | `redis-dev.internal:6379` | `redis-uat.internal:6379` | `redis-prod.internal:6379` |
| **Secrets Source** | Kubernetes Secrets (dev namespace) | Kubernetes Secrets (uat namespace) | HashiCorp Vault (`gateforge/prod/*`) |
| **Monitoring URL** | `https://grafana-dev.gateforge.dev` | `https://grafana-uat.gateforge.dev` | `https://grafana.gateforge.com` |
| **Log Aggregation** | Loki (dev) | Loki (uat) | Loki + S3 archival |
| **K8s Namespace** | `gateforge-dev` | `gateforge-uat` | `gateforge-prod` |
| **Replicas (API)** | 1 | 2 | 3+ (HPA) |
| **Replicas (Web)** | 1 | 2 | 3+ (HPA) |

---

## Revision History

| Version | Date          | Author                | Changes |
|---------|---------------|-----------------------|---------|
| 0.1.0   | [PLACEHOLDER] | Operator              | Initial deployment runbook draft. |
| 0.2.0   | 2026-05-01    | Operator + Architect  | §1: pre-deployment checklist now requires GitHub push, auto-bump CI green, and version-tag match (items 1–3); added Pre-Flight Acknowledgement requirement (item 17). §8: new "Hotfix and Versioning Note" deferring all version writes to the auto-bump CI. Added pointer to `operations/AGENTS.md` and `/VERSIONING.md` in the metadata header. |
