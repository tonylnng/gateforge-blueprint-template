# Test Report Format Guide

<!--
  AGENT INSTRUCTIONS:
  This document defines the mandatory format for all test execution reports in qa/reports/.
  QC Agents produce a report after every test execution (per iteration, per module).
  The Architect reviews the report to make the PROMOTE / HOLD / ROLLBACK decision.
  
  Every report must include the quality gate assessment with a clear recommendation.
  Do not leave the assessment vague — state the decision and justify it with data.
-->

| Field          | Value                                    |
|----------------|------------------------------------------|
| Document ID    | QA-RPT-FMT-001                           |
| Version        | 1.0                                      |
| Owner          | QC Agents (VM-4, MiniMax 2.7)           |
| Reviewer       | System Architect                         |
| Status         | [PLACEHOLDER]                            |
| Last Updated   | [PLACEHOLDER]                            |

---

## 1. File Naming Convention

```
TEST-REPORT-ITER-<NNN>-<module>.md
```

| Component   | Description                                  | Example             |
|-------------|----------------------------------------------|---------------------|
| `<NNN>`     | Three-digit iteration number (zero-padded)    | 001                 |
| `<module>`  | Module under test                             | auth                |

**Examples:**
- `TEST-REPORT-ITER-001-auth.md`
- `TEST-REPORT-ITER-003-payment.md`
- `TEST-REPORT-ITER-005-order.md`

---

## 2. Test Report Template

<!-- 
  AGENT INSTRUCTIONS:
  Copy everything between START TEMPLATE and END TEMPLATE when creating a new report.
  Fill in every field. Every number must come from actual test execution — never estimate.
  The quality gate assessment must reference the thresholds from qa/README.md.
-->

### --- START TEMPLATE ---

```markdown
# Test Report: [ITER-NNN] — [Module Name]

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| Document ID        | TEST-REPORT-ITER-<NNN>-<module>            |
| Version            | 1.0                                        |
| Module             | [module name]                              |
| Iteration          | [iteration number]                         |
| Test Period        | [YYYY-MM-DD] to [YYYY-MM-DD]              |
| Author             | [QC Agent ID]                              |
| Status             | draft / final                              |
| Last Updated       | [YYYY-MM-DD]                               |

---

## 1. Test Summary

| Metric               | Count    |
|----------------------|----------|
| Total Test Cases     | [N]      |
| Passed               | [N]      |
| Failed               | [N]      |
| Skipped              | [N]      |
| Blocked              | [N]      |
| Pass Rate            | [N]%     |

---

## 2. Test Execution Matrix

| Test Case ID             | Type         | Priority | Status  | Duration | Defect ID   |
|--------------------------|-------------|----------|---------|----------|-------------|
| TC-<module>-<type>-NNN   | unit        | P0       | PASS    | 12ms     | —           |
| TC-<module>-<type>-NNN   | integration | P1       | FAIL    | 340ms    | DEF-NNN     |
| TC-<module>-<type>-NNN   | e2e         | P0       | PASS    | 2.1s     | —           |
| TC-<module>-<type>-NNN   | e2e         | P2       | SKIP    | —        | — (env issue)|
| ...                      | ...         | ...      | ...     | ...      | ...         |

---

## 3. Coverage Summary

| Test Level     | Total Cases | Executed | Passed | Coverage % | Threshold | Status   |
|----------------|------------|----------|--------|------------|-----------|----------|
| Unit           | [N]        | [N]      | [N]    | [N]%       | ≥ 95%     | PASS/FAIL|
| Integration    | [N]        | [N]      | [N]    | [N]%       | ≥ 90%     | PASS/FAIL|
| E2E            | [N]        | [N]      | [N]    | [N]%       | ≥ 85%     | PASS/FAIL|
| Performance    | [N]        | [N]      | [N]    | —          | —         | PASS/FAIL|
| Security       | [N]        | [N]      | [N]    | —          | —         | PASS/FAIL|

---

## 4. Quality Gate Assessment

### Decision: **[PROMOTE / HOLD / ROLLBACK]**

### Rationale

<!-- 
  Provide a clear, data-backed justification. Reference specific thresholds from qa/README.md.
  If HOLD or ROLLBACK, list the specific conditions that were not met.
-->

[PLACEHOLDER — detailed rationale]

### Gate Criteria Evaluation

| Criterion                        | Required          | Actual            | Met?     |
|----------------------------------|-------------------|-------------------|----------|
| Unit coverage                    | ≥ 95%             | [N]%              | Yes/No   |
| Integration coverage             | ≥ 90%             | [N]%              | Yes/No   |
| E2E coverage                     | ≥ 85%             | [N]%              | Yes/No   |
| P0 defects open                  | 0                 | [N]               | Yes/No   |
| P1 defects open                  | ≤ 2               | [N]               | Yes/No   |
| Performance p95 within NFR       | Yes               | [Yes/No]          | Yes/No   |
| Security vulnerabilities (High+) | 0                 | [N]               | Yes/No   |

---

## 5. Defects Found

| Defect ID | Severity | Priority | Module   | Summary                              | Assigned To    | Status     |
|-----------|----------|----------|----------|--------------------------------------|----------------|------------|
| DEF-NNN   | critical | P0       | [module] | [one-line summary]                   | [agent/person] | [status]   |
| DEF-NNN   | major    | P1       | [module] | [one-line summary]                   | [agent/person] | [status]   |
| DEF-NNN   | minor    | P2       | [module] | [one-line summary]                   | [agent/person] | [status]   |
| ...       | ...      | ...      | ...      | ...                                  | ...            | ...        |

### Defect Summary

| Severity | Count | Open | In Progress | Fixed | Verified |
|----------|-------|------|-------------|-------|----------|
| Critical | [N]   | [N]  | [N]         | [N]   | [N]      |
| Major    | [N]   | [N]  | [N]         | [N]   | [N]      |
| Minor    | [N]   | [N]  | [N]         | [N]   | [N]      |
| Cosmetic | [N]   | [N]  | [N]         | [N]   | [N]      |

---

## 6. Environment Issues

<!-- List any environment or infrastructure issues that impacted test execution. -->

| Issue                             | Impact                              | Resolution               |
|-----------------------------------|-------------------------------------|--------------------------|
| [description]                     | [which test cases affected]         | [how it was resolved]    |

---

## 7. Recommendations

<!-- Provide actionable recommendations based on test results. -->

1. [Recommendation]
2. [Recommendation]
3. [Recommendation]

---

## 8. Sign-off

| Role                | Name / Agent ID    | Date           | Approval        |
|---------------------|--------------------|----------------|-----------------|
| QC Author           | [PLACEHOLDER]      | [PLACEHOLDER]  | [PLACEHOLDER]   |
| System Architect    | [PLACEHOLDER]      | [PLACEHOLDER]  | [PLACEHOLDER]   |
```

### --- END TEMPLATE ---

---

## 3. Example: Auth Module — Iteration 001 Report

<!--
  AGENT INSTRUCTIONS:
  This is a complete example report. Use it as a reference for the expected level of detail.
  Every number is illustrative — actual reports must use real test execution data.
-->

# Test Report: ITER-001 — Auth Module

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| Document ID        | TEST-REPORT-ITER-001-auth                  |
| Version            | 1.0                                        |
| Module             | auth                                       |
| Iteration          | 001                                        |
| Test Period        | 2026-04-01 to 2026-04-05                  |
| Author             | QC Agent VM-4                              |
| Status             | final                                      |
| Last Updated       | 2026-04-05                                 |

---

## 1. Test Summary

| Metric               | Count    |
|----------------------|----------|
| Total Test Cases     | 47       |
| Passed               | 44       |
| Failed               | 2        |
| Skipped              | 1        |
| Blocked              | 0        |
| Pass Rate            | 93.6%    |

---

## 2. Test Execution Matrix

| Test Case ID             | Type         | Priority | Status  | Duration | Defect ID   |
|--------------------------|-------------|----------|---------|----------|-------------|
| TC-auth-unit-001         | unit        | P0       | PASS    | 15ms     | —           |
| TC-auth-unit-002         | unit        | P0       | PASS    | 8ms      | —           |
| TC-auth-unit-003         | unit        | P1       | PASS    | 12ms     | —           |
| TC-auth-unit-004         | unit        | P1       | PASS    | 11ms     | —           |
| TC-auth-unit-005         | unit        | P1       | PASS    | 9ms      | —           |
| TC-auth-unit-006         | unit        | P2       | PASS    | 7ms      | —           |
| TC-auth-unit-007         | unit        | P2       | PASS    | 14ms     | —           |
| TC-auth-unit-008         | unit        | P2       | PASS    | 10ms     | —           |
| TC-auth-unit-009         | unit        | P2       | PASS    | 8ms      | —           |
| TC-auth-unit-010         | unit        | P3       | PASS    | 6ms      | —           |
| TC-auth-unit-011         | unit        | P3       | PASS    | 5ms      | —           |
| TC-auth-unit-012         | unit        | P3       | PASS    | 7ms      | —           |
| TC-auth-unit-013         | unit        | P0       | PASS    | 18ms     | —           |
| TC-auth-unit-014         | unit        | P1       | PASS    | 13ms     | —           |
| TC-auth-unit-015         | unit        | P1       | PASS    | 11ms     | —           |
| TC-auth-unit-016         | unit        | P2       | PASS    | 9ms      | —           |
| TC-auth-unit-017         | unit        | P2       | PASS    | 8ms      | —           |
| TC-auth-unit-018         | unit        | P2       | PASS    | 12ms     | —           |
| TC-auth-unit-019         | unit        | P3       | PASS    | 6ms      | —           |
| TC-auth-unit-020         | unit        | P3       | PASS    | 7ms      | —           |
| TC-auth-integration-001  | integration | P0       | PASS    | 245ms    | —           |
| TC-auth-integration-002  | integration | P0       | PASS    | 312ms    | —           |
| TC-auth-integration-003  | integration | P1       | PASS    | 198ms    | —           |
| TC-auth-integration-004  | integration | P1       | FAIL    | 1.2s     | DEF-001     |
| TC-auth-integration-005  | integration | P1       | PASS    | 267ms    | —           |
| TC-auth-integration-006  | integration | P2       | PASS    | 189ms    | —           |
| TC-auth-integration-007  | integration | P2       | PASS    | 204ms    | —           |
| TC-auth-integration-008  | integration | P2       | PASS    | 176ms    | —           |
| TC-auth-integration-009  | integration | P3       | PASS    | 155ms    | —           |
| TC-auth-integration-010  | integration | P3       | PASS    | 143ms    | —           |
| TC-auth-e2e-001          | e2e         | P0       | PASS    | 2.1s     | —           |
| TC-auth-e2e-002          | e2e         | P0       | PASS    | 3.4s     | —           |
| TC-auth-e2e-003          | e2e         | P1       | PASS    | 2.8s     | —           |
| TC-auth-e2e-004          | e2e         | P1       | FAIL    | 4.2s     | DEF-002     |
| TC-auth-e2e-005          | e2e         | P1       | PASS    | 2.5s     | —           |
| TC-auth-e2e-006          | e2e         | P2       | PASS    | 1.9s     | —           |
| TC-auth-e2e-007          | e2e         | P2       | PASS    | 2.3s     | —           |
| TC-auth-e2e-008          | e2e         | P2       | PASS    | 2.0s     | —           |
| TC-auth-e2e-009          | e2e         | P3       | SKIP    | —        | — (MFA provider sandbox down) |
| TC-auth-e2e-010          | e2e         | P3       | PASS    | 1.8s     | —           |
| TC-auth-security-001     | security    | P0       | PASS    | 890ms    | —           |
| TC-auth-security-002     | security    | P0       | PASS    | 1.1s     | —           |
| TC-auth-security-003     | security    | P1       | PASS    | 750ms    | —           |
| TC-auth-security-004     | security    | P1       | PASS    | 920ms    | —           |
| TC-auth-security-005     | security    | P1       | PASS    | 680ms    | —           |
| TC-auth-performance-001  | performance | P1       | PASS    | 12.5s    | —           |
| TC-auth-performance-002  | performance | P2       | PASS    | 8.3s     | —           |

---

## 3. Coverage Summary

| Test Level     | Total Cases | Executed | Passed | Coverage % | Threshold | Status |
|----------------|------------|----------|--------|------------|-----------|--------|
| Unit           | 20         | 20       | 20     | 97.2%      | ≥ 95%     | PASS   |
| Integration    | 10         | 10       | 9      | 91.5%      | ≥ 90%     | PASS   |
| E2E            | 10         | 9        | 8      | 88.0%      | ≥ 85%     | PASS   |
| Performance    | 2          | 2        | 2      | —          | —         | PASS   |
| Security       | 5          | 5        | 5      | —          | —         | PASS   |

---

## 4. Quality Gate Assessment

### Decision: **HOLD**

### Rationale

All coverage thresholds are met (Unit: 97.2%, Integration: 91.5%, E2E: 88.0%). However, two defects were discovered:

- **DEF-001** (Major, P1): JWT refresh token rotation fails when the original token is used within 1 second of rotation. This is a race condition that could affect concurrent sessions. Root cause identified — fix estimated at 2 hours.
- **DEF-002** (Minor, P2): MFA setup flow displays incorrect QR code dimensions on mobile viewport (< 375px width). Functional but poor UX.

The module cannot be promoted because DEF-001 is a P1 defect affecting a critical auth flow. Once DEF-001 is fixed and verified, the module can be re-evaluated for PROMOTE.

### Gate Criteria Evaluation

| Criterion                        | Required          | Actual            | Met?     |
|----------------------------------|-------------------|-------------------|----------|
| Unit coverage                    | ≥ 95%             | 97.2%             | Yes      |
| Integration coverage             | ≥ 90%             | 91.5%             | Yes      |
| E2E coverage                     | ≥ 85%             | 88.0%             | Yes      |
| P0 defects open                  | 0                 | 0                 | Yes      |
| P1 defects open                  | ≤ 2               | 1                 | Yes      |
| Performance p95 within NFR       | Yes               | Yes               | Yes      |
| Security vulnerabilities (High+) | 0                 | 0                 | Yes      |

**Note:** While all gate criteria are technically met (P1 ≤ 2), the nature of DEF-001 (race condition in token refresh) warrants a HOLD until the fix is verified. The Architect may override to PROMOTE with conditions if the fix is deployed and verified within the current iteration.

---

## 5. Defects Found

| Defect ID | Severity | Priority | Module | Summary                                        | Assigned To     | Status     |
|-----------|----------|----------|--------|-------------------------------------------------|-----------------|------------|
| DEF-001   | major    | P1       | auth   | JWT refresh token race condition within 1s window | Developer Agent | reported   |
| DEF-002   | minor    | P2       | auth   | MFA QR code dimensions incorrect on mobile < 375px | Developer Agent | reported   |

### Defect Summary

| Severity | Count | Open | In Progress | Fixed | Verified |
|----------|-------|------|-------------|-------|----------|
| Critical | 0     | 0    | 0           | 0     | 0        |
| Major    | 1     | 1    | 0           | 0     | 0        |
| Minor    | 1     | 1    | 0           | 0     | 0        |
| Cosmetic | 0     | 0    | 0           | 0     | 0        |

---

## 6. Environment Issues

| Issue                                        | Impact                                    | Resolution                        |
|----------------------------------------------|-------------------------------------------|-----------------------------------|
| MFA provider sandbox was down on 2026-04-04  | TC-auth-e2e-009 skipped (MFA E2E test)    | Test will be executed next iteration when sandbox is restored |

---

## 7. Recommendations

1. **Fix DEF-001 urgently** — The JWT refresh race condition could impact production users with multiple active sessions. Implement token rotation locking or a grace period for the previous token.
2. **Re-run TC-auth-e2e-009** — Schedule MFA E2E test as soon as the provider sandbox is restored. This test validates a P0 (critical) auth flow.
3. **Add concurrency test cases** — The race condition in DEF-001 suggests insufficient concurrency testing. Add test cases for concurrent token refresh, concurrent login from multiple devices, and concurrent password reset.

---

## 8. Sign-off

| Role                | Name / Agent ID    | Date           | Approval                |
|---------------------|--------------------|----------------|-------------------------|
| QC Author           | QC Agent VM-4      | 2026-04-05     | Report submitted        |
| System Architect    | [PLACEHOLDER]      | [PLACEHOLDER]  | [PLACEHOLDER]           |

---

## 4. Review Checklist (for Architect)

<!--
  AGENT INSTRUCTIONS:
  The Architect uses this checklist when reviewing test reports. If any item fails,
  the report is returned to the QC Agent for correction.
-->

- [ ] File name follows `TEST-REPORT-ITER-<NNN>-<module>.md` convention
- [ ] All metadata fields populated
- [ ] Test summary numbers are internally consistent (total = pass + fail + skip + blocked)
- [ ] Every failed test case has a corresponding defect ID
- [ ] Coverage percentages are calculated correctly
- [ ] Quality gate assessment matches the data (decision is justified)
- [ ] All defects are linked to the defect report files in `../defects/`
- [ ] Environment issues are documented with impact assessment
- [ ] Recommendations are actionable (not vague)
- [ ] Sign-off section is present
