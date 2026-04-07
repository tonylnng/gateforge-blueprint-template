# QA Metrics Dashboard

<!--
  AGENT INSTRUCTIONS:
  This is a LIVING DOCUMENT. Update it after every test execution. QC Agents are responsible
  for keeping all tables current. The Architect reviews this document during gate decisions.
  
  Data sources:
  - Coverage data: from test execution reports (qa/reports/)
  - Defect data: from defect reports (qa/defects/)
  - Performance data: from load/stress test reports (qa/reports/PERF-REPORT-*)
  - Security data: from security scan reports
  
  All percentages must be calculated from actual test execution data — never estimated.
-->

| Field          | Value                                    |
|----------------|------------------------------------------|
| Document ID    | QA-METRICS-001                           |
| Version        | 1.0                                      |
| Owner          | QC Agents (VM-4, MiniMax 2.7)           |
| Reviewer       | System Architect                         |
| Status         | [PLACEHOLDER]                            |
| Last Updated   | [PLACEHOLDER]                            |

---

## 1. Current Quality Summary

<!--
  AGENT INSTRUCTIONS:
  Update this table after every test execution. This is the primary table the Architect
  reads during gate decisions. Gate Status must reflect the PROMOTE / HOLD / ROLLBACK model.
-->

| Module          | Unit %  | Integration % | E2E %   | Open Bugs (P0/P1/P2/P3) | Gate Status | Last Tested   |
|-----------------|---------|---------------|---------|--------------------------|-------------|---------------|
| auth            | 97.2%   | 91.5%         | 88.0%   | 0 / 1 / 1 / 0           | HOLD        | 2026-04-05    |
| user            | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER]    | [PLACEHOLDER] | [PLACEHOLDER] |
| payment         | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER]    | [PLACEHOLDER] | [PLACEHOLDER] |
| order           | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER]    | [PLACEHOLDER] | [PLACEHOLDER] |
| notification    | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER]    | [PLACEHOLDER] | [PLACEHOLDER] |
| [PLACEHOLDER]   | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER]    | [PLACEHOLDER] | [PLACEHOLDER] |

**Thresholds:** Unit ≥ 95% | Integration ≥ 90% | E2E ≥ 85% | P0 = 0 | P1 ≤ 2

---

## 2. Quality Trend

<!--
  AGENT INSTRUCTIONS:
  Track quality metrics iteration-over-iteration. Add a new row after each iteration.
  This table reveals trends — is quality improving, degrading, or stable?
-->

### Overall Coverage Trend

| Iteration | Date       | Unit %  | Integration % | E2E %   | Total Bugs Found | Bugs Closed | Bug Escape Rate | Overall Gate |
|-----------|------------|---------|---------------|---------|-----------------|-------------|-----------------|-------------|
| ITER-001  | 2026-04-05 | 97.2%   | 91.5%         | 88.0%   | 2               | 0           | 0%              | HOLD        |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### Module-Level Trend (Auth Example)

| Iteration | Unit %  | Integration % | E2E %   | Bugs Found | Bugs Fixed | Net Open |
|-----------|---------|---------------|---------|------------|------------|----------|
| ITER-001  | 97.2%   | 91.5%         | 88.0%   | 2          | 0          | 2        |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

<!-- AGENT INSTRUCTIONS: Create a similar trend table for each module as test data accumulates. -->

---

## 3. Defect Metrics

### 3.1 Defect Density per Module

<!--
  AGENT INSTRUCTIONS:
  Defect density = total bugs found / story points delivered for that module.
  Lower density indicates higher code quality. Update after each iteration.
-->

| Module          | Story Points Delivered | Bugs Found | Defect Density (bugs/SP) | Trend vs Last Iteration |
|-----------------|----------------------|------------|--------------------------|-------------------------|
| auth            | [PLACEHOLDER]        | 2          | [PLACEHOLDER]            | — (first iteration)     |
| user            | [PLACEHOLDER]        | [PLACEHOLDER] | [PLACEHOLDER]         | [PLACEHOLDER]           |
| payment         | [PLACEHOLDER]        | [PLACEHOLDER] | [PLACEHOLDER]         | [PLACEHOLDER]           |
| order           | [PLACEHOLDER]        | [PLACEHOLDER] | [PLACEHOLDER]         | [PLACEHOLDER]           |
| notification    | [PLACEHOLDER]        | [PLACEHOLDER] | [PLACEHOLDER]         | [PLACEHOLDER]           |

**Target:** Defect density < 0.5 bugs/SP for mature modules.

### 3.2 Defect Age

<!--
  AGENT INSTRUCTIONS:
  Track how long defects remain open. Aging defects indicate process bottlenecks.
  Calculate average days open for each severity level.
-->

| Severity  | Total Open | Avg Days Open | Max Days Open | SLA Target  | SLA Compliance |
|-----------|-----------|---------------|---------------|-------------|----------------|
| Critical  | 0         | —             | —             | 4 hours     | 100%           |
| Major     | 1         | 0             | 0             | 24 hours    | 100%           |
| Minor     | 1         | 0             | 0             | 1 iteration | 100%           |
| Cosmetic  | 0         | —             | —             | Backlog     | —              |

### 3.3 Defect Discovery Rate

<!--
  AGENT INSTRUCTIONS:
  Track how many bugs are found per iteration. A decreasing rate as the project matures
  is healthy. A sudden increase may indicate a problematic code change.
-->

| Iteration | Critical | Major | Minor | Cosmetic | Total | Trend         |
|-----------|----------|-------|-------|----------|-------|---------------|
| ITER-001  | 0        | 1     | 1     | 0        | 2     | — (baseline)  |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### 3.4 Bug Escape Rate

<!--
  AGENT INSTRUCTIONS:
  Bug escape rate = bugs found in UAT or Production / total bugs found.
  This measures the effectiveness of the QA process. Lower is better.
  Ideally, all bugs are caught before UAT. Target: < 5%.
-->

| Period          | Bugs Found in Dev/QA | Bugs Found in UAT | Bugs Found in Prod | Escape Rate (UAT+Prod / Total) |
|-----------------|---------------------|--------------------|--------------------|---------------------------------|
| ITER-001        | 2                   | 0                  | 0                  | 0%                              |
| Cumulative      | 2                   | 0                  | 0                  | 0%                              |

**Target:** Bug escape rate < 5%.

---

## 4. Test Automation Metrics

### 4.1 Automation Coverage by Module

<!--
  AGENT INSTRUCTIONS:
  Track what percentage of test cases are automated (vs. manual) per module.
  Target is >80% overall automation. Update as test cases are created and automated.
-->

| Module          | Total Test Cases | Automated | Manual | Pending Automation | Automation % | Target | Status   |
|-----------------|-----------------|-----------|--------|--------------------|--------------| -------|----------|
| auth            | 47              | 44        | 2      | 1                  | 93.6%        | ≥ 80%  | PASS     |
| user            | [PLACEHOLDER]   | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | ≥ 80% | [PLACEHOLDER] |
| payment         | [PLACEHOLDER]   | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | ≥ 80% | [PLACEHOLDER] |
| order           | [PLACEHOLDER]   | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | ≥ 80% | [PLACEHOLDER] |
| notification    | [PLACEHOLDER]   | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | ≥ 80% | [PLACEHOLDER] |
| **Overall**     | [PLACEHOLDER]   | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | ≥ 80% | [PLACEHOLDER] |

### 4.2 Test Execution Time

<!--
  AGENT INSTRUCTIONS:
  Track how long the full test suite takes to run. Long execution times slow CI/CD.
  Aim to keep the full suite under 15 minutes for fast feedback.
-->

| Test Suite          | Avg Duration | Max Duration | Target   | Trend vs Last Run |
|---------------------|-------------|-------------|----------|-------------------|
| Unit (all modules)  | [PLACEHOLDER] | [PLACEHOLDER] | < 2 min  | [PLACEHOLDER]   |
| Integration (all)   | [PLACEHOLDER] | [PLACEHOLDER] | < 5 min  | [PLACEHOLDER]   |
| E2E (all)           | [PLACEHOLDER] | [PLACEHOLDER] | < 10 min | [PLACEHOLDER]   |
| Full Suite          | [PLACEHOLDER] | [PLACEHOLDER] | < 15 min | [PLACEHOLDER]   |

### 4.3 Flaky Test Rate

<!--
  AGENT INSTRUCTIONS:
  Flaky tests pass and fail non-deterministically. They erode trust in the test suite.
  Track and fix flaky tests aggressively. Target: < 2% flaky rate.
-->

| Module          | Total Automated Tests | Flaky Tests | Flaky Rate | Status   |
|-----------------|----------------------|-------------|------------|----------|
| auth            | 44                   | 0           | 0%         | PASS     |
| user            | [PLACEHOLDER]        | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| payment         | [PLACEHOLDER]        | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| order           | [PLACEHOLDER]        | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| notification    | [PLACEHOLDER]        | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| **Overall**     | [PLACEHOLDER]        | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

**Target:** Flaky rate < 2%. Any flaky test must be fixed or quarantined within 1 iteration.

---

## 5. Performance Metrics Baseline

<!--
  AGENT INSTRUCTIONS:
  Track performance metrics over time. Populate from load test reports
  (qa/reports/PERF-REPORT-load-*.md). Baseline is set from the first successful load test.
  Flag any regression > 10% from baseline.
-->

| Endpoint                     | Baseline p95 | Current p95 | Change   | Trend   | Status   |
|------------------------------|-------------|-------------|----------|---------|----------|
| POST /api/v1/auth/login      | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| POST /api/v1/auth/refresh    | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| GET /api/v1/users/:id        | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| PUT /api/v1/users/:id        | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| POST /api/v1/orders          | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| GET /api/v1/orders/:id       | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| POST /api/v1/payments/checkout | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

**Regression threshold:** Flag if current p95 > baseline p95 + 10%.

### Throughput Baseline

| Test Profile | Baseline RPS | Current RPS | Change   | Status   |
|-------------|-------------|-------------|----------|----------|
| Baseline    | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Peak        | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### Stress Test Baseline

| Metric                    | Baseline      | Current       | Trend    |
|---------------------------|---------------|---------------|----------|
| Breaking Point (VUs)      | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Recovery Time (p95)       | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| Endurance Memory Growth   | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## 6. Security Metrics

<!--
  AGENT INSTRUCTIONS:
  Track security vulnerabilities found by SAST (Snyk), DAST (OWASP ZAP), and manual pen-testing.
  Vulnerabilities must be remediated per SLA. Update after every security scan.
-->

### Vulnerability Summary

| Severity  | Total Found | Remediated | Open | Remediation Rate | SLA           | SLA Compliance |
|-----------|------------|------------|------|------------------|---------------|----------------|
| Critical  | 0          | 0          | 0    | —                | 24 hours      | 100%           |
| High      | 0          | 0          | 0    | —                | 72 hours      | 100%           |
| Medium    | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | 1 iteration | [PLACEHOLDER] |
| Low       | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | 2 iterations | [PLACEHOLDER] |

### Vulnerability Trend

| Scan Date   | Critical | High | Medium | Low | Total | Net Change |
|-------------|----------|------|--------|-----|-------|------------|
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### OWASP Top 10 Coverage

| OWASP Category                        | Test Cases | Last Scan Result | Status   |
|---------------------------------------|-----------|------------------|----------|
| A01 — Broken Access Control           | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| A02 — Cryptographic Failures          | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| A03 — Injection                       | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| A04 — Insecure Design                 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| A05 — Security Misconfiguration       | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| A06 — Vulnerable Components           | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| A07 — Auth Failures                   | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| A08 — Software/Data Integrity Failures| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| A09 — Logging/Monitoring Failures     | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
| A10 — SSRF                            | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### Dependency Vulnerability Scan (Snyk)

| Scan Date   | Critical | High | Medium | Low | Total | New Since Last Scan |
|-------------|----------|------|--------|-----|-------|---------------------|
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## Revision History

| Version | Date          | Author         | Changes                              |
|---------|---------------|----------------|--------------------------------------|
| 1.0     | [PLACEHOLDER] | [PLACEHOLDER]  | Initial metrics dashboard created    |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER]                  |
