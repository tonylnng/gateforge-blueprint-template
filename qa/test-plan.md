# Master Test Plan

<!--
  AGENT INSTRUCTIONS:
  This is the Master Test Plan following IEEE 829 structure. QC Agents produce this document
  at the start of the project and update it at each phase transition. The Architect must approve
  before test execution begins. Replace all [PLACEHOLDER] values with project-specific data.
  
  IEEE 829 sections: Test Plan Identifier, Introduction, Test Items, Features to Test,
  Features Not to Test, Approach, Item Pass/Fail Criteria, Suspension/Resumption Criteria,
  Test Deliverables, Environmental Needs, Responsibilities, Staffing, Schedule, Risks.
-->

| Field          | Value                                    |
|----------------|------------------------------------------|
| Document ID    | QA-TP-001                                |
| Version        | 1.0                                      |
| Owner          | QC Agents (VM-4, MiniMax 2.7)           |
| Reviewer       | System Architect                         |
| Status         | [PLACEHOLDER]                            |
| Last Updated   | [PLACEHOLDER]                            |
| IEEE 829 Ref   | IEEE 829-2008 — Test Plan                |

---

## 1. Test Plan Identifier

<!-- AGENT INSTRUCTIONS: Assign a unique identifier. Format: TP-<project>-<version>. -->

| Field               | Value                          |
|----------------------|--------------------------------|
| Identifier           | TP-GATEFORGE-[PLACEHOLDER]    |
| Project              | GateForge                      |
| Release              | [PLACEHOLDER]                  |
| Iteration Coverage   | [PLACEHOLDER]                  |
| Created By           | [PLACEHOLDER — QC Agent ID]   |
| Approved By          | [PLACEHOLDER — Architect]     |

---

## 2. Introduction

### 2.1 Purpose

This Master Test Plan defines the overall testing strategy, scope, approach, resources, and schedule for the GateForge project. It serves as the governing document for all test activities and is the single source of truth for test scope and methodology.

<!-- AGENT INSTRUCTIONS: Expand the purpose to include project-specific testing goals. -->

### 2.2 Scope

This plan covers testing for the following system boundaries:

- **In Scope:** [PLACEHOLDER — list modules, features, and integrations to be tested]
- **Out of Scope:** [PLACEHOLDER — list explicitly excluded items, e.g., third-party SaaS integrations tested by vendors]

### 2.3 Objectives

<!-- AGENT INSTRUCTIONS: Tailor these objectives to the specific release. Add or remove as needed. -->

1. Verify all functional requirements (FR-*) are met through traceable test cases.
2. Validate all non-functional requirements (NFR-*) including performance, security, and reliability.
3. Achieve quality gate coverage thresholds: Unit ≥ 95%, Integration ≥ 90%, E2E ≥ 85%.
4. Identify, report, and track all defects to resolution.
5. Provide data-driven PROMOTE / HOLD / ROLLBACK recommendations per module.

### 2.4 References

| Document                      | Location                              |
|-------------------------------|---------------------------------------|
| QA Framework                  | `../QA-FRAMEWORK.md`                  |
| Functional Requirements       | `../requirements/functional/`         |
| Non-Functional Requirements   | `../requirements/nfr.md`              |
| Architecture Overview         | `../architecture/`                    |
| API Specifications            | `../architecture/api/`                |

---

## 3. Test Items

<!-- 
  AGENT INSTRUCTIONS:
  List every module/component under test. Populate from the architecture documentation.
  "Features to Test" and "Features Not to Test" must be explicitly stated per IEEE 829.
-->

| Module          | Version      | Features to Test                                           | Features Not to Test                        |
|-----------------|-------------|-----------------------------------------------------------|---------------------------------------------|
| auth            | [PLACEHOLDER] | Login, registration, password reset, OAuth, JWT refresh, MFA | Third-party OAuth provider internals       |
| user            | [PLACEHOLDER] | Profile CRUD, role management, preferences, avatar upload  | Email delivery (tested via integration mock) |
| payment         | [PLACEHOLDER] | Checkout flow, payment processing, refunds, webhooks       | Payment gateway internals (Stripe/PayPal)   |
| order           | [PLACEHOLDER] | Order creation, status transitions, cancellation, history  | Warehouse fulfillment systems               |
| notification    | [PLACEHOLDER] | Email, push, SMS triggers, template rendering, preferences | SMS carrier delivery guarantees              |
| [PLACEHOLDER]   | [PLACEHOLDER] | [PLACEHOLDER]                                              | [PLACEHOLDER]                               |

---

## 4. Testing Approach

### 4.1 Test Levels

<!-- AGENT INSTRUCTIONS: Each test level must have defined scope, tools, and ownership. -->

| Test Level    | Scope                                                    | Tools                          | Owner          |
|---------------|----------------------------------------------------------|--------------------------------|----------------|
| Unit          | Individual functions, methods, classes                    | Jest, ts-jest                  | QC Agent VM-4  |
| Integration   | API contracts, service-to-service, database interactions | Jest + Supertest, Testcontainers | QC Agent VM-4 |
| E2E           | Full user workflows through the UI and API               | Playwright, Cypress            | QC Agent MiniMax 2.7 |
| Performance   | Load, stress, endurance, spike testing                   | k6, Artillery                  | QC Agent MiniMax 2.7 |
| Security      | OWASP Top 10, authentication/authorization, input validation | OWASP ZAP, Snyk, custom scripts | QC Agent VM-4 |

### 4.2 Test Design Techniques

<!-- AGENT INSTRUCTIONS: Select techniques appropriate to each test level. ISTQB-aligned. -->

| Technique                    | Applied To          | Description                                              |
|------------------------------|---------------------|----------------------------------------------------------|
| Equivalence Partitioning     | Unit, Integration   | Divide input domains into valid/invalid partitions        |
| Boundary Value Analysis      | Unit, Integration   | Test at boundaries of equivalence classes                 |
| Decision Table Testing       | Integration, E2E    | Enumerate business rule combinations                     |
| State Transition Testing     | E2E                 | Test state machines (e.g., order status, payment status)  |
| Exploratory Testing          | E2E                 | Session-based exploration of new features                 |
| Risk-Based Testing           | All levels          | Prioritize tests by risk assessment (section 10)          |

### 4.3 Test Automation Strategy

<!-- AGENT INSTRUCTIONS: Define what will be automated vs. manual. Target >80% automation. -->

| Category           | Automation Target | Rationale                                      |
|--------------------|------------------|-------------------------------------------------|
| Unit Tests         | 100%             | All unit tests must be automated and in CI.      |
| Integration Tests  | 100%             | All API and service tests automated in CI.       |
| E2E Tests          | ≥ 80%            | Critical user flows automated; edge cases manual.|
| Performance Tests  | 100%             | All load/stress tests scripted and repeatable.   |
| Security Tests     | ≥ 70%            | SAST/DAST automated; manual pen-test quarterly.  |

---

## 5. Test Environment Requirements

<!-- 
  AGENT INSTRUCTIONS:
  Define the infrastructure needed for each test level. Must mirror production as closely
  as possible for integration and E2E. Coordinate with operations/ for provisioning.
-->

### 5.1 Infrastructure

| Environment    | Purpose              | Infrastructure                                                  | Data                     |
|----------------|---------------------|-----------------------------------------------------------------|--------------------------|
| Unit           | Unit test execution  | Local developer machine or CI runner                             | Mocked data              |
| Integration    | API / service tests  | Docker Compose: NestJS, PostgreSQL, Redis                        | Seeded test database     |
| E2E / Staging  | Full system tests    | Kubernetes cluster (mirroring prod), all services deployed        | Anonymized production data |
| Performance    | Load / stress tests  | Dedicated Kubernetes cluster, isolated network, production-scale  | Generated realistic data |

### 5.2 Test Data

<!-- AGENT INSTRUCTIONS: Define test data strategy per environment. Never use real PII in test. -->

| Data Type          | Source                          | Management                                      |
|--------------------|--------------------------------|-------------------------------------------------|
| Unit test data     | Factories (e.g., @faker-js)    | Generated per test run, no persistence required  |
| Integration data   | SQL seed scripts               | Reset before each test suite via migration scripts|
| E2E test data      | Anonymized production snapshot  | Refreshed weekly, stored in `test-data/` repo    |
| Performance data   | k6 data generators             | Volume-matched to production (≥ 1M records)      |

### 5.3 Tools

| Tool              | Purpose                    | Version          |
|-------------------|---------------------------|------------------|
| Jest              | Unit + integration testing | [PLACEHOLDER]    |
| Supertest         | HTTP API testing           | [PLACEHOLDER]    |
| Testcontainers    | Containerized dependencies | [PLACEHOLDER]    |
| Playwright        | E2E browser testing        | [PLACEHOLDER]    |
| k6                | Load / stress testing      | [PLACEHOLDER]    |
| Artillery         | Load testing (alternative) | [PLACEHOLDER]    |
| OWASP ZAP         | DAST security scanning     | [PLACEHOLDER]    |
| Snyk              | SAST / dependency scanning | [PLACEHOLDER]    |

---

## 6. Test Schedule

<!-- 
  AGENT INSTRUCTIONS:
  Align the test schedule with project iterations defined in ../project/iterations/.
  Update this table as iterations are planned and completed. Each phase maps to iteration work.
-->

| Phase                   | Start          | End            | Owner                | Dependencies                              |
|-------------------------|----------------|----------------|----------------------|-------------------------------------------|
| Test Plan Approval      | [PLACEHOLDER]  | [PLACEHOLDER]  | System Architect     | Requirements finalized                    |
| Unit Test Development   | [PLACEHOLDER]  | [PLACEHOLDER]  | QC Agent VM-4        | Module code available                     |
| Integration Test Dev    | [PLACEHOLDER]  | [PLACEHOLDER]  | QC Agent VM-4        | API specs finalized, services deployed    |
| E2E Test Development    | [PLACEHOLDER]  | [PLACEHOLDER]  | QC Agent MiniMax 2.7 | UI components available, staging deployed |
| Performance Test Dev    | [PLACEHOLDER]  | [PLACEHOLDER]  | QC Agent MiniMax 2.7 | Staging environment provisioned           |
| Security Test Execution | [PLACEHOLDER]  | [PLACEHOLDER]  | QC Agent VM-4        | Full system deployed to staging           |
| Regression Testing      | [PLACEHOLDER]  | [PLACEHOLDER]  | Both QC Agents       | All fixes applied                         |
| UAT Support             | [PLACEHOLDER]  | [PLACEHOLDER]  | Both QC Agents       | Staging stable, stakeholder availability  |

---

## 7. Entry and Exit Criteria

<!-- 
  AGENT INSTRUCTIONS:
  These criteria are mandatory. Testing CANNOT begin until entry criteria are met.
  Testing CANNOT be signed off until exit criteria are satisfied.
  Suspension criteria define when to pause testing (e.g., environment down).
-->

| Test Level   | Entry Criteria                                                      | Exit Criteria                                                          | Suspension Criteria                                    |
|--------------|---------------------------------------------------------------------|------------------------------------------------------------------------|--------------------------------------------------------|
| Unit         | Code compiles. Module code reviewed and merged to dev branch.        | ≥ 95% line + branch coverage. All P0/P1 defects resolved.             | Build broken. Critical infrastructure failure.          |
| Integration  | All dependent services deployed to integration env. API specs frozen. | ≥ 90% API endpoint coverage. All contract tests pass. ≤ 2 P1 defects. | Dependency service unavailable > 2 hours.              |
| E2E          | Staging environment stable. UI deployed. Test data seeded.           | ≥ 85% workflow coverage. All critical paths pass. Zero P0 defects.     | Staging environment unstable. > 3 blocked test cases.   |
| Performance  | Staging env at production-scale. Monitoring dashboards operational.   | All NFR performance targets met. No regressions > 10% from baseline.   | Environment resource constraints. Unreliable metrics.   |
| Security     | Full system deployed. Latest dependency scan completed.              | Zero high/critical vulnerabilities. OWASP Top 10 scan clean.           | New critical CVE discovered requiring immediate patching.|

---

## 8. Test Deliverables Checklist

<!-- AGENT INSTRUCTIONS: Check off deliverables as they are produced. This tracks completeness. -->

| Deliverable                          | Format                              | Status         |
|--------------------------------------|-------------------------------------|----------------|
| Master Test Plan (this document)     | `qa/test-plan.md`                   | [PLACEHOLDER]  |
| Unit Test Cases                      | `qa/test-cases/TC-*-unit-*.md`      | [PLACEHOLDER]  |
| Integration Test Cases               | `qa/test-cases/TC-*-integration-*.md` | [PLACEHOLDER] |
| E2E Test Cases                       | `qa/test-cases/TC-*-e2e-*.md`       | [PLACEHOLDER]  |
| Performance Test Cases               | `qa/test-cases/TC-*-performance-*.md` | [PLACEHOLDER] |
| Security Test Cases                  | `qa/test-cases/TC-*-security-*.md`   | [PLACEHOLDER]  |
| Load Test Plan                       | `qa/performance/load-test-plan.md`   | [PLACEHOLDER]  |
| Stress Test Plan                     | `qa/performance/stress-test-plan.md` | [PLACEHOLDER]  |
| Iteration Test Reports               | `qa/reports/TEST-REPORT-ITER-*.md`   | [PLACEHOLDER]  |
| Defect Reports                       | `qa/defects/DEF-*.md`               | [PLACEHOLDER]  |
| QA Metrics Dashboard                 | `qa/metrics.md`                      | [PLACEHOLDER]  |

---

## 9. Risk Assessment

<!-- 
  AGENT INSTRUCTIONS:
  Identify risks to the testing effort (not product risks — those belong in requirements).
  Assess probability (Low/Medium/High) and impact (Low/Medium/High/Critical).
  Define concrete mitigations. Update this table throughout the project.
-->

| Risk ID | Risk                                              | Probability | Impact   | Mitigation                                                       |
|---------|---------------------------------------------------|-------------|----------|------------------------------------------------------------------|
| TR-001  | Test environment instability delays execution      | Medium      | High     | Containerized environments with automated provisioning. Fallback to local Docker Compose. |
| TR-002  | Incomplete or changing requirements                | Medium      | High     | Freeze requirements per iteration. Change requests trigger test plan update. |
| TR-003  | Test data does not represent production scenarios  | Low         | High     | Use anonymized production data snapshots. Validate data distributions. |
| TR-004  | Performance test results inconsistent              | Medium      | Medium   | Run performance tests in isolated environment. Average across 3 runs minimum. |
| TR-005  | Insufficient test automation coverage              | Low         | Medium   | Track automation % per module in metrics.md. Flag modules below 80%. |
| TR-006  | QC Agent capacity bottleneck                       | Medium      | Medium   | Distribute modules across VM-4 and MiniMax 2.7. Prioritize by risk. |
| TR-007  | Third-party service sandbox unavailability          | Low         | Medium   | Maintain mock services for all external dependencies. |
| [PLACEHOLDER] | [PLACEHOLDER]                                | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER]                                             |

---

## 10. Staffing and Responsibilities

<!-- 
  AGENT INSTRUCTIONS:
  Map QC Agent assignments to modules. Each module must have a primary QC Agent.
  The Architect reviews all output but does not produce test artifacts.
-->

| Role               | Agent / Person       | Responsibilities                                                      |
|--------------------|---------------------|-----------------------------------------------------------------------|
| QC Lead            | QC Agent VM-4       | Test plan maintenance, unit + integration + security test production   |
| QC Engineer        | QC Agent MiniMax 2.7| E2E test production, performance test production and execution         |
| Test Reviewer      | System Architect     | Review all test artifacts, make quality gate decisions                 |
| Environment Admin  | Operator Agent       | Provision and maintain test environments                              |

### Module Assignments

| Module          | Primary QC Agent     | Secondary QC Agent   |
|-----------------|---------------------|---------------------|
| auth            | VM-4                | MiniMax 2.7          |
| user            | VM-4                | MiniMax 2.7          |
| payment         | VM-4                | MiniMax 2.7          |
| order           | MiniMax 2.7         | VM-4                 |
| notification    | MiniMax 2.7         | VM-4                 |
| [PLACEHOLDER]   | [PLACEHOLDER]       | [PLACEHOLDER]        |

---

## 11. Approvals

<!-- 
  AGENT INSTRUCTIONS:
  This section must be completed before test execution begins. The Architect signs off
  on the plan. If the plan is revised, a new approval is required.
-->

| Role                | Name / Agent ID    | Date           | Signature / Approval |
|---------------------|--------------------|----------------|---------------------|
| QC Lead             | [PLACEHOLDER]      | [PLACEHOLDER]  | [PLACEHOLDER]       |
| System Architect    | [PLACEHOLDER]      | [PLACEHOLDER]  | [PLACEHOLDER]       |
| Project Owner       | Tony NG             | [PLACEHOLDER]  | [PLACEHOLDER]       |

---

## Revision History

| Version | Date          | Author         | Changes                    |
|---------|---------------|----------------|----------------------------|
| 1.0     | [PLACEHOLDER] | [PLACEHOLDER]  | Initial test plan created  |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER]        |
