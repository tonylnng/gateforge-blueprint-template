# Test Case Format Guide

<!--
  AGENT INSTRUCTIONS:
  This document defines the mandatory format for all test case files in the qa/test-cases/ directory.
  Every test case file MUST follow this structure exactly. QC Agents should copy the template
  section and fill in all fields. The Architect will reject test cases that deviate from this format.
  
  Standards: IEEE 829 (test case specification), ISTQB (test design techniques).
-->

| Field          | Value                                    |
|----------------|------------------------------------------|
| Document ID    | QA-TC-FMT-001                            |
| Version        | 1.0                                      |
| Owner          | QC Agents (VM-4, MiniMax 2.7)           |
| Reviewer       | System Architect                         |
| Status         | [PLACEHOLDER]                            |
| Last Updated   | [PLACEHOLDER]                            |

---

## 1. File Naming Convention

```
TC-<module>-<type>-<NNN>.md
```

| Component   | Allowed Values                                   | Example             |
|-------------|--------------------------------------------------|---------------------|
| `<module>`  | auth, user, payment, order, notification, etc.    | auth                |
| `<type>`    | unit, integration, e2e, performance, security     | unit                |
| `<NNN>`     | Three-digit zero-padded sequential number         | 001                 |

**Examples:**
- `TC-auth-unit-001.md`
- `TC-payment-integration-003.md`
- `TC-order-e2e-012.md`
- `TC-auth-security-001.md`
- `TC-notification-performance-002.md`

---

## 2. Test Case Template

<!-- 
  AGENT INSTRUCTIONS:
  Copy everything between the START TEMPLATE and END TEMPLATE markers when creating a new
  test case file. Fill in every field. Do not remove any section. If a section is not
  applicable, write "N/A" with a brief justification.
-->

### --- START TEMPLATE ---

```markdown
# Test Case: [TC-ID]

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| Test Case ID       | TC-<module>-<type>-<NNN>                   |
| Module             | [module name]                              |
| Type               | unit / integration / e2e / performance / security |
| Priority           | P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low) |
| Automation Status  | automated / manual / pending               |
| Author             | [QC Agent ID]                              |
| Created            | [YYYY-MM-DD]                               |
| Last Updated       | [YYYY-MM-DD]                               |
| Status             | draft / approved / executed / deprecated   |

## Related Requirements

| Requirement ID | Description                          |
|---------------|--------------------------------------|
| FR-XXX        | [Brief description]                  |
| NFR-XXX       | [Brief description]                  |

## Preconditions

<!-- List all conditions that must be true before executing this test case. -->

1. [Precondition 1]
2. [Precondition 2]

## Test Data

<!-- Define specific test data required. Use tables for structured data. -->

| Data Element     | Value                  | Notes                    |
|-----------------|------------------------|--------------------------|
| [element name]  | [value]                | [source or constraint]   |

## Test Steps

| Step # | Action                              | Expected Result                        | Actual Result  | Status         |
|--------|-------------------------------------|----------------------------------------|----------------|----------------|
| 1      | [Describe the action]               | [What should happen]                   | [PLACEHOLDER]  | [PLACEHOLDER]  |
| 2      | [Describe the action]               | [What should happen]                   | [PLACEHOLDER]  | [PLACEHOLDER]  |
| 3      | [Describe the action]               | [What should happen]                   | [PLACEHOLDER]  | [PLACEHOLDER]  |

## Postconditions

<!-- Describe the expected system state after the test completes. -->

1. [Postcondition 1]
2. [Postcondition 2]

## Notes

<!-- Any additional context, edge cases considered, or links to related test cases. -->

[PLACEHOLDER]
```

### --- END TEMPLATE ---

---

## 3. Field Definitions

### Priority Levels

| Priority | Label    | Definition                                                        | SLA for Defects Found |
|----------|----------|-------------------------------------------------------------------|-----------------------|
| P0       | Critical | Core functionality broken. Blocks release. Data loss or security breach. | Fix within 4 hours   |
| P1       | High     | Major feature broken. Workaround exists but unacceptable for release.    | Fix within 24 hours  |
| P2       | Medium   | Minor feature issue. Workaround available. Does not block release.       | Fix within 1 iteration |
| P3       | Low      | Cosmetic issue or minor improvement. No functional impact.               | Scheduled for backlog |

### Automation Status

| Status   | Meaning                                                                 |
|----------|-------------------------------------------------------------------------|
| automated | Test is fully automated and runs in CI/CD pipeline.                    |
| manual    | Test requires manual execution (e.g., visual UI checks, exploratory).  |
| pending   | Test is written but automation implementation is not yet complete.      |

### Test Case Status

| Status     | Meaning                                                         |
|------------|-----------------------------------------------------------------|
| draft      | Test case written, not yet reviewed.                            |
| approved   | Reviewed and approved by Architect. Ready for execution.        |
| executed   | Test has been run at least once. Actual results recorded.       |
| deprecated | Test case is no longer valid (e.g., feature removed, redesigned). |

---

## 4. Example: Unit Test Case — User Login

<!--
  AGENT INSTRUCTIONS:
  This is a complete example showing a unit test for the authentication module.
  Use this as a reference for the expected level of detail.
-->

# Test Case: TC-auth-unit-001

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| Test Case ID       | TC-auth-unit-001                           |
| Module             | auth                                       |
| Type               | unit                                       |
| Priority           | P0 (Critical)                              |
| Automation Status  | automated                                  |
| Author             | QC Agent VM-4                              |
| Created            | 2026-04-07                                 |
| Last Updated       | 2026-04-07                                 |
| Status             | approved                                   |

## Related Requirements

| Requirement ID | Description                                              |
|---------------|----------------------------------------------------------|
| FR-AUTH-001   | System shall authenticate users via email and password    |
| FR-AUTH-003   | System shall return JWT access + refresh tokens on login  |
| NFR-SEC-001   | Passwords must be hashed with bcrypt (cost factor ≥ 12)  |

## Preconditions

1. User record exists in the database with email `test@gateforge.dev` and a bcrypt-hashed password.
2. The `AuthService.login()` method is available and its dependencies (UserRepository, JwtService) are mockable.
3. Test database is seeded or mocks are configured.

## Test Data

| Data Element     | Value                          | Notes                              |
|-----------------|--------------------------------|------------------------------------|
| Email            | test@gateforge.dev             | Valid registered email             |
| Password         | C0mpl3x!Pass#2026              | Meets password policy              |
| Invalid Password | wrongpassword                  | Does not match stored hash         |
| Hashed Password  | $2b$12$LJ3m...                 | Bcrypt hash of C0mpl3x!Pass#2026  |

## Test Steps

| Step # | Action                                                                    | Expected Result                                                         | Actual Result | Status |
|--------|---------------------------------------------------------------------------|-------------------------------------------------------------------------|---------------|--------|
| 1      | Call `AuthService.login({ email: "test@gateforge.dev", password: "C0mpl3x!Pass#2026" })` | Method accepts the input without throwing                                | As expected   | PASS   |
| 2      | Verify bcrypt.compare is called with the provided password and stored hash | `bcrypt.compare("C0mpl3x!Pass#2026", storedHash)` returns `true`        | As expected   | PASS   |
| 3      | Verify JWT tokens are generated                                           | Response contains `accessToken` (string, non-empty) and `refreshToken` (string, non-empty) | As expected | PASS |
| 4      | Verify access token payload contains correct claims                       | Payload includes `sub: userId`, `email: "test@gateforge.dev"`, `iat`, `exp` | As expected | PASS |
| 5      | Verify access token expiry is set correctly                               | Token `exp` is 15 minutes from `iat`                                     | As expected   | PASS   |
| 6      | Call `AuthService.login({ email: "test@gateforge.dev", password: "wrongpassword" })` | Throws `UnauthorizedException` with message "Invalid credentials"        | As expected   | PASS   |
| 7      | Call `AuthService.login({ email: "nonexistent@gateforge.dev", password: "any" })` | Throws `UnauthorizedException` with message "Invalid credentials"        | As expected   | PASS   |

## Postconditions

1. No database state is modified (login is read-only).
2. A login audit event is emitted for successful login (Step 1).
3. A failed login audit event is emitted for failed attempts (Steps 6, 7).

## Notes

- Steps 6–7 test the negative path. The error message must be identical for wrong password and nonexistent user to prevent user enumeration.
- Related security test: `TC-auth-security-001` covers brute-force protection and rate limiting.

---

## 5. Example: API Integration Test — User Profile Retrieval

<!--
  AGENT INSTRUCTIONS:
  This example shows an integration test that verifies the API contract for a GET endpoint.
  Integration tests should use real (containerized) dependencies, not mocks.
-->

# Test Case: TC-user-integration-001

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| Test Case ID       | TC-user-integration-001                    |
| Module             | user                                       |
| Type               | integration                                |
| Priority           | P1 (High)                                  |
| Automation Status  | automated                                  |
| Author             | QC Agent VM-4                              |
| Created            | 2026-04-07                                 |
| Last Updated       | 2026-04-07                                 |
| Status             | approved                                   |

## Related Requirements

| Requirement ID | Description                                              |
|---------------|----------------------------------------------------------|
| FR-USER-002   | System shall return user profile data for authenticated users |
| FR-USER-003   | System shall not expose sensitive fields (password hash, internal IDs) in API responses |
| NFR-PERF-001  | API response time ≤ 200ms at p95 for single-record GET requests |

## Preconditions

1. Integration test environment running (NestJS app, PostgreSQL via Testcontainers, Redis).
2. Test user seeded in database with known `userId` and profile data.
3. Valid JWT access token available for the test user.

## Test Data

| Data Element     | Value                                  | Notes                              |
|-----------------|----------------------------------------|------------------------------------|
| User ID          | `usr_test_001`                         | Seeded test user                   |
| Access Token     | Generated via AuthService in test setup | Valid JWT for usr_test_001         |
| Expected Name    | Jane Doe                               | Seeded profile data                |
| Expected Email   | jane@gateforge.dev                     | Seeded profile data                |
| Expired Token    | Generated with exp = now - 1h          | For auth failure test              |

## Test Steps

| Step # | Action                                                              | Expected Result                                                         | Actual Result | Status |
|--------|---------------------------------------------------------------------|-------------------------------------------------------------------------|---------------|--------|
| 1      | `GET /api/v1/users/usr_test_001` with valid Bearer token           | HTTP 200. Body contains `{ id, name, email, avatar, createdAt }`         | As expected   | PASS   |
| 2      | Verify response body field values                                   | `name: "Jane Doe"`, `email: "jane@gateforge.dev"`                       | As expected   | PASS   |
| 3      | Verify sensitive fields are NOT present in response                 | Response body does NOT contain `passwordHash`, `internalId`, `refreshToken` | As expected | PASS |
| 4      | Verify response Content-Type header                                 | `application/json; charset=utf-8`                                        | As expected   | PASS   |
| 5      | Verify response time                                               | Response returned in < 200ms                                             | 45ms          | PASS   |
| 6      | `GET /api/v1/users/usr_test_001` with NO Authorization header      | HTTP 401. Body: `{ statusCode: 401, message: "Unauthorized" }`          | As expected   | PASS   |
| 7      | `GET /api/v1/users/usr_test_001` with expired Bearer token         | HTTP 401. Body: `{ statusCode: 401, message: "Token expired" }`         | As expected   | PASS   |
| 8      | `GET /api/v1/users/nonexistent_id` with valid Bearer token         | HTTP 404. Body: `{ statusCode: 404, message: "User not found" }`        | As expected   | PASS   |

## Postconditions

1. No database records modified.
2. API access logs contain entries for all requests.

## Notes

- This test validates the API contract defined in `../architecture/api/user-api.yaml`.
- Response time in Step 5 is informational; formal performance testing is in `TC-user-performance-001`.
- Steps 6–8 validate error responses conform to the project's standard error schema.

---

## 6. Example: E2E Test — Complete Login Flow

<!--
  AGENT INSTRUCTIONS:
  This example shows an end-to-end test using Playwright that tests the full login flow
  through the browser UI. E2E tests must cover the happy path and critical error paths.
-->

# Test Case: TC-auth-e2e-001

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| Test Case ID       | TC-auth-e2e-001                            |
| Module             | auth                                       |
| Type               | e2e                                        |
| Priority           | P0 (Critical)                              |
| Automation Status  | automated                                  |
| Author             | QC Agent MiniMax 2.7                       |
| Created            | 2026-04-07                                 |
| Last Updated       | 2026-04-07                                 |
| Status             | approved                                   |

## Related Requirements

| Requirement ID | Description                                              |
|---------------|----------------------------------------------------------|
| FR-AUTH-001   | System shall authenticate users via email and password    |
| FR-AUTH-002   | System shall display appropriate error messages for failed login |
| FR-AUTH-005   | System shall redirect authenticated users to the dashboard |
| NFR-UX-001   | Login flow must complete within 3 seconds under normal load |

## Preconditions

1. Staging environment is deployed and accessible at `https://staging.gateforge.dev`.
2. Test user account exists: `e2e-user@gateforge.dev` / `E2eT3st!Pass#2026`.
3. Playwright browser context is initialized (Chromium, viewport 1280×720).
4. No active sessions exist for the test user (cookies cleared).

## Test Data

| Data Element     | Value                          | Notes                              |
|-----------------|--------------------------------|------------------------------------|
| Login URL        | https://staging.gateforge.dev/login | Login page                    |
| Valid Email      | e2e-user@gateforge.dev         | Registered E2E test account        |
| Valid Password   | E2eT3st!Pass#2026              | Known valid password               |
| Invalid Password | WrongPassword123               | Triggers login failure             |
| Dashboard URL    | https://staging.gateforge.dev/dashboard | Expected redirect target    |

## Test Steps

| Step # | Action                                                              | Expected Result                                                         | Actual Result | Status |
|--------|---------------------------------------------------------------------|-------------------------------------------------------------------------|---------------|--------|
| 1      | Navigate to `https://staging.gateforge.dev/login`                  | Login page loads. Email and password fields visible. "Sign In" button visible. | As expected | PASS |
| 2      | Verify page title                                                   | Title is "Sign In — GateForge"                                          | As expected   | PASS   |
| 3      | Enter `e2e-user@gateforge.dev` in email field                      | Email field populated. No validation errors.                             | As expected   | PASS   |
| 4      | Enter `E2eT3st!Pass#2026` in password field                        | Password field populated. Characters masked.                             | As expected   | PASS   |
| 5      | Click "Sign In" button                                              | Loading indicator appears. Button becomes disabled.                      | As expected   | PASS   |
| 6      | Wait for navigation to complete                                     | Browser redirects to `https://staging.gateforge.dev/dashboard`          | As expected   | PASS   |
| 7      | Verify dashboard content                                            | Dashboard page loads. User name "E2E Test User" visible in header.      | As expected   | PASS   |
| 8      | Verify total login flow time                                        | Steps 1–7 completed within 3 seconds                                    | 1.8s          | PASS   |
| 9      | Log out and navigate back to login page                             | Session cleared. Login page displayed.                                   | As expected   | PASS   |
| 10     | Enter `e2e-user@gateforge.dev` and `WrongPassword123`, click Sign In | Error message displayed: "Invalid email or password." No redirect.      | As expected   | PASS   |
| 11     | Verify error message styling                                        | Error message is red, appears below the form, does not reveal which field is wrong. | As expected | PASS |
| 12     | Verify email field retains value after failed attempt               | Email field still contains `e2e-user@gateforge.dev`. Password field is cleared. | As expected | PASS |

## Postconditions

1. Test user session is terminated (logout in Step 9 or test teardown).
2. No persistent state changes in the system.
3. Browser context is closed.

## Notes

- This test covers the critical happy path (Steps 1–8) and the primary error path (Steps 10–12).
- Additional E2E tests cover: `TC-auth-e2e-002` (password reset flow), `TC-auth-e2e-003` (OAuth login), `TC-auth-e2e-004` (MFA flow).
- Playwright test file: `e2e/tests/auth/login.spec.ts`
- Screenshot on failure is configured globally in `playwright.config.ts`.

---

## 7. Traceability Rules

<!--
  AGENT INSTRUCTIONS:
  Every test case MUST trace back to at least one requirement. If a test case does not
  map to a requirement, either the requirement is missing or the test case is unnecessary.
-->

1. **Every functional requirement** (`FR-*`) must have at least one test case linked to it.
2. **Every non-functional requirement** (`NFR-*`) must have at least one test case validating it.
3. The `Related Requirements` table in each test case creates the forward traceability.
4. The QA Metrics Dashboard (`../metrics.md`) tracks backward traceability (requirement → test coverage).
5. Test cases without requirement links must be justified in the Notes section or removed.

---

## 8. Review Checklist (for Architect)

<!--
  AGENT INSTRUCTIONS:
  The Architect uses this checklist when reviewing test cases produced by QC Agents.
  If any item fails, the test case is returned for revision.
-->

- [ ] File name follows `TC-<module>-<type>-<NNN>.md` convention
- [ ] All metadata fields populated (no remaining `[PLACEHOLDER]`)
- [ ] At least one requirement linked in Related Requirements
- [ ] Preconditions are specific and verifiable
- [ ] Test data is defined with concrete values (no vague descriptions)
- [ ] Each step has a clear, verifiable expected result
- [ ] Negative / error paths are tested (not just happy path)
- [ ] Priority is appropriate for the functionality being tested
- [ ] Automation status is realistic and aligns with the automation strategy
- [ ] Postconditions describe the expected system state
