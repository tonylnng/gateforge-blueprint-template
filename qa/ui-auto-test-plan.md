# UI Auto-Test Plan — `<project-codename>`

<!--
  AGENT INSTRUCTIONS:
  This is the project-level instantiation of the GateForge UI Auto-Test Standard.
  The canonical standard lives in:
    - Multi-agent: install/vm-4-qc-agents/UI-AUTO-TEST-STANDARD.md
    - Single-agent: roles/qc/UI-AUTO-TEST-STANDARD.md
  Read the canonical standard before completing this template.
  This file is MANDATORY for every project that ships a web UI. The QC role
  rejects any release where this file is absent or has unfilled [PLACEHOLDER]s.
-->

| Field          | Value                                    |
|----------------|------------------------------------------|
| Document ID    | UI-AUTO-TEST-PLAN-001                    |
| Version        | 1.0                                      |
| Project        | [PLACEHOLDER — codename]                 |
| Owner          | QC role                                  |
| Reviewer       | System Architect                         |
| Status         | [PLACEHOLDER]                            |
| Last Updated   | [PLACEHOLDER — YYYY-MM-DD]               |
| Standard       | GateForge UI Auto-Test Standard v1.0+    |

---

## 1. Scope

### 1.1 In scope

- [PLACEHOLDER — list every URL / SPA route / web view this plan covers]
- [PLACEHOLDER — admin portal, public site, embedded webview, etc.]

### 1.2 Out of scope

- [PLACEHOLDER — native mobile, CLI, backend-only services]

### 1.3 Build type

- [ ] AI-developed (GateForge agents author the UI)
- [ ] Human-developed (legacy or external code under audit)
- [ ] Hybrid

If `AI-developed` or `Hybrid`, Lane B weight rises to 15–20% of test budget per the standard § 4.

---

## 2. Critical user journeys (drive both lanes)

| ID | Journey | Owner role(s) | Acceptance criteria reference | Lane A coverage | Lane B intent |
|---|---|---|---|---|---|
| CUJ-001 | [PLACEHOLDER — e.g. New user signs up + verifies email] | guest, user | `requirements/functional/FR-AUTH-001.md` | `features/auth/signup.feature` | `intents.md#cuj-001` |
| CUJ-002 | [PLACEHOLDER] | | | | |

Every CUJ must appear in **both** `qa/features/` (Lane A) and `qa/intents.md` (Lane B). Missing coverage on either side is a release-blocking issue.

---

## 3. `data-testid` namespaces in scope

| Module / Page | Namespace prefix | Owner |
|---|---|---|
| Auth pages | `auth-` | DEV (single-agent) / Developer role (multi-agent) |
| [PLACEHOLDER] | | |

Developer agents must add `data-testid` to every interactive element under these namespaces. The naming rule is `kebab-case`, scoped: `auth-login-submit`, `checkout-payment-card-input`.

---

## 4. Visual baselines

| Page | Baseline file | Captured at | Updated by |
|---|---|---|---|
| `/` | `qa/visual-baselines/home.png` | [PLACEHOLDER — git SHA] | [PLACEHOLDER] |
| [PLACEHOLDER] | | | |

Baseline updates are committed by the QC role and reviewed by the Architect. Pixel-diff threshold: **< 0.1% on the listed pages** (G-UI-2).

---

## 5. Accessibility & performance budgets

| Page | axe critical issues | Lighthouse perf (mobile) | LCP p95 budget |
|---|---|---|---|
| `/` | 0 | ≥ 80 | ≤ 2.5 s |
| [PLACEHOLDER] | 0 | ≥ 80 | ≤ 2.5 s |

These map to release gates G-UI-3 and G-UI-4.

---

## 6. Test pyramid weighting (override of standard § 4 if needed)

| Layer | Default weight | This project's weight | Rationale |
|---|---|---|---|
| L1 Unit | 60% | [PLACEHOLDER] | |
| L2 API/Integration | 20% | [PLACEHOLDER] | |
| L3 UI E2E (Lane A) | 12% | [PLACEHOLDER] | |
| L4 UI Exploratory (Lane B) | 5% | [PLACEHOLDER] | If AI-developed, raise to 15–20% |
| L5 Visual Regression | 2% | [PLACEHOLDER] | |
| L6 A11y & Performance | 1% | [PLACEHOLDER] | |

If any value differs from the default, the Architect signs off on the rationale.

---

## 7. Lane A (Deterministic Regression) configuration

- Profile: `openclaw` (set in `openclaw.qa.yaml`)
- Browser: Chromium, headless, viewport 1280×800
- Cadence: every PR + every release commit
- Reporters: `junit`, `html`, `allure`
- Reports written to: `qa/reports/laneA-<run-id>/`
- Gate: G-UI-1 (100% pass)

See `playwright.config.ts` for the runtime configuration.

---

## 8. Lane B (AI Exploratory) configuration

- Profile: `user` (attached via Chrome DevTools MCP to `ws://chrome-headful:3000`)
- Browser: Chromium 124+ in `browserless/chrome:latest` Docker container, viewport 1366×768
- Model: [PLACEHOLDER — `anthropic/claude-sonnet-4-6` for single-agent, `minimax/minimax-2.7` for multi-agent]
- Cadence: nightly 02:00 HKT + on-demand pre-release
- Intent source: `qa/intents.md`
- Reports written to: `qa/reports/laneB-<run-id>/`
- Gate: G-UI-5 (no new P0/P1 in last 24 h)

See `docker-compose.qa.yml` for the headful Chrome service and `openclaw.qa.yaml` for agent config.

---

## 9. Headless Ubuntu compliance

- [ ] Runner OS: Ubuntu Server 22.04+ LTS, no desktop.
- [ ] `bootstrap-qa-runner.sh` ran clean on the QC runner host.
- [ ] `chrome-headful` Docker container reachable on `127.0.0.1:9222` only.
- [ ] All Chromium flags present: `--no-sandbox --disable-dev-shm-usage --disable-gpu --headless=new`.
- [ ] Resource tier matches Section 9.8 of the standard for expected workload.
- [ ] Networking: SUT reachable via Tailscale MagicDNS (multi-agent) or localhost (single-agent).
- [ ] Outbound LLM calls routed via OpenClaw gateway, not directly from the runner.
- [ ] Reports persisted to S3 / MinIO.
- [ ] Section 9.12 checklist signed by QC role and committed in `qc/gates/<release>.md`.

This corresponds to release gate G-UI-7.

---

## 10. Release gate verdict block (template)

The QC role copies this block verbatim into `project/qc/gates/<release>.md` and fills in the numbers:

```json
{
  "uiAutoTest": {
    "laneA":     { "passed": 0, "failed": 0, "duration_s": 0, "report_url": "" },
    "laneB":     { "intentsExecuted": 0, "newDefects": 0, "regressions": 0, "report_url": "" },
    "visualDiff":{ "maxPctDelta": 0.0, "baselinesUpdated": false },
    "a11y":      { "criticalIssues": 0, "axeReport": "" },
    "performance": { "lighthouseScore": 0, "p95LCPms": 0 },
    "headlessChecklistSigned": false
  }
}
```

A missing or zero-only block on a release-tagged commit forces a `Rejected` verdict and a back-transition to DEV (or DESIGN if the failure traces to untestable interactions).

---

## 11. Cross-references

- Canonical standard: `roles/qc/UI-AUTO-TEST-STANDARD.md` (single-agent) or `install/vm-4-qc-agents/UI-AUTO-TEST-STANDARD.md` (multi-agent)
- Master test plan: [`test-plan.md`](test-plan.md)
- Lane B intents: [`intents.md`](intents.md)
- Lane A config: [`playwright.config.ts`](playwright.config.ts)
- OpenClaw QA profile: [`openclaw.qa.yaml`](openclaw.qa.yaml)
- Lane B Docker stack: [`docker-compose.qa.yml`](docker-compose.qa.yml)
- Bootstrap script: [`scripts/bootstrap-qa-runner.sh`](scripts/bootstrap-qa-runner.sh)
- QA metrics dashboard: [`metrics.md`](metrics.md)
