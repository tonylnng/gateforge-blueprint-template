# Functional Requirements Document

<!--
  STANDARD: IEEE 830 / ISO/IEC/IEEE 29148 (decomposed from user-requirements.md)
  PURPOSE: Break down user stories into module-level functional requirements with
           full traceability to test cases.
  OWNER: System Architect
  
  INSTRUCTIONS FOR THE ARCHITECT:
  1. Read user-requirements.md first — every FR must trace to a User Story.
  2. Group functional requirements by module.
  3. Acceptance criteria must use Given/When/Then format for testability.
  4. Update the Traceability Matrix (Section 8) as you add requirements.
  5. The Dependency Matrix (Section 7) must be complete before handing off to Designers.
  6. FR-IDs follow the pattern: FR-<MODULE>-<NNN> (e.g., FR-AUTH-001).
-->

## Document Metadata

| Field | Value |
|-------|-------|
| **Document ID** | `REQ-FUNC-001` |
| **Version** | `0.1` |
| **Status** | `Draft` |
| **Owner** | System Architect |
| **Last Updated** | `YYYY-MM-DD` |
| **Approved By** | — |
| **Source Document** | `requirements/user-requirements.md` |
| **Standard** | IEEE 830 / ISO/IEC/IEEE 29148 |

---

## 1. Module Decomposition

<!--
  Map user stories to logical modules. Each module represents a cohesive set of functionality.
  A module typically corresponds to a NestJS service module or a React feature module.
-->

| Module ID | Module Name | Description | User Stories Covered |
|-----------|------------|-------------|---------------------|
| MOD-AUTH | Authentication | User registration, login, password management, session handling | US-001, US-002 |
| MOD-ADMIN | Administration | User management dashboard, role assignment, audit logs | US-003 |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

<!--
  Add one row per module. Aim for 4–10 modules for an MVP.
  Each module should be independently deployable or at least independently testable.
-->

---

## 2. Functional Requirements by Module

<!--
  For each module, list all functional requirements in a table.
  RULES:
  - One requirement per row — keep them atomic.
  - Priority uses MoSCoW: Must / Should / Could / Won't.
  - Acceptance Criteria use Given/When/Then for unambiguous test derivation.
  - Source User Story links back to user-requirements.md.
-->

### 2.1 MOD-AUTH — Authentication

| FR-ID | Description | Priority | Source | Acceptance Criteria |
|-------|------------|----------|--------|-------------------|
| FR-AUTH-001 | The system shall allow users to register with a valid email address and a password meeting complexity requirements. | Must | US-001 | **Given** a user provides a valid email and a password with ≥8 characters, 1 uppercase, 1 number, and 1 special character, **When** they submit the registration form, **Then** the system creates an account in `pending_verification` status and sends a verification email within 30 seconds. |
| FR-AUTH-002 | The system shall verify a user's email address via a time-limited verification link. | Must | US-001 | **Given** a user clicks a verification link within 24 hours of registration, **When** the link is valid and unexpired, **Then** the account status changes to `active` and the user is redirected to the login page. |
| FR-AUTH-003 | The system shall allow users to request a password reset via their registered email. | Must | US-002 | **Given** a user provides a registered email address, **When** they submit the password reset form, **Then** the system sends a reset link valid for 15 minutes; the link is single-use. |
| FR-AUTH-004 | [PLACEHOLDER] | [Must/Should/Could] | [US-XXX] | **Given** [PLACEHOLDER], **When** [PLACEHOLDER], **Then** [PLACEHOLDER]. |

### 2.2 MOD-ADMIN — Administration

| FR-ID | Description | Priority | Source | Acceptance Criteria |
|-------|------------|----------|--------|-------------------|
| FR-ADMIN-001 | The system shall provide an admin dashboard listing all registered users with pagination. | Should | US-003 | **Given** an authenticated admin user navigates to the user management page, **When** the page loads, **Then** it displays users in a paginated table (default 20 per page) sorted by registration date descending, loading within 2 seconds. |
| FR-ADMIN-002 | The system shall allow admins to filter users by status and registration date range. | Should | US-003 | **Given** an admin applies a filter, **When** they select status `active` and a date range, **Then** the table updates to show only matching users within 1 second. |
| FR-ADMIN-003 | [PLACEHOLDER] | [Must/Should/Could] | [US-XXX] | **Given** [PLACEHOLDER], **When** [PLACEHOLDER], **Then** [PLACEHOLDER]. |

### 2.3 [PLACEHOLDER — Module Name]

<!-- Copy the table structure above for each additional module. -->

| FR-ID | Description | Priority | Source | Acceptance Criteria |
|-------|------------|----------|--------|-------------------|
| [PLACEHOLDER] | [PLACEHOLDER] | [Must/Should/Could] | [US-XXX] | **Given** [PLACEHOLDER], **When** [PLACEHOLDER], **Then** [PLACEHOLDER]. |

---

## 3. Business Rules

<!--
  Business rules are constraints on data or behavior that apply across modules.
  They are not features — they are invariants the system must always enforce.
-->

| Rule ID | Rule Name | Description | Affected Modules | Source |
|---------|----------|-------------|-----------------|--------|
| BR-001 | Email Uniqueness | Each email address can be associated with exactly one account. Duplicate registrations are rejected. | MOD-AUTH | US-001 |
| BR-002 | Password Complexity | Passwords must contain ≥8 characters, ≥1 uppercase letter, ≥1 number, ≥1 special character. | MOD-AUTH | US-001, US-002 |
| BR-003 | Session Expiry | User sessions expire after 24 hours of inactivity. Refresh tokens expire after 7 days. | MOD-AUTH | US-001 |
| BR-004 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## 4. Data Requirements

<!--
  Define the core data entities, their relationships, and constraints.
  This section feeds into architecture/data-model.md for full schema design.
-->

### 4.1 Core Entities

| Entity | Description | Key Attributes | Owner Module |
|--------|------------|---------------|-------------|
| User | A registered platform user | `id`, `email`, `password_hash`, `status`, `created_at` | MOD-AUTH |
| Session | An active user session | `id`, `user_id`, `token`, `expires_at`, `created_at` | MOD-AUTH |
| AuditLog | Record of administrative actions | `id`, `admin_id`, `action`, `target_entity`, `timestamp` | MOD-ADMIN |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### 4.2 Entity Relationships

| Relationship | Cardinality | Description |
|-------------|-------------|-------------|
| User → Session | 1:N | A user can have multiple active sessions (multi-device) |
| User → AuditLog | 1:N | An admin user can generate multiple audit log entries |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### 4.3 Data Constraints

| Constraint | Entity | Attribute | Rule |
|-----------|--------|-----------|------|
| NOT NULL | User | email | Email is required for all users |
| UNIQUE | User | email | No duplicate email addresses |
| CHECK | User | status | Must be one of: `pending_verification`, `active`, `suspended`, `deleted` |
| FK | Session | user_id | Must reference an existing User.id |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## 5. Interface Requirements

<!--
  Define how the system interfaces with users (UI) and other systems (API).
  This section bridges to architecture/api-specifications/ and design/.
-->

### 5.1 User Interface Requirements

| Screen | Description | Key Elements | Source FRs |
|--------|------------|-------------|-----------|
| Registration Page | New user signup form | Email field, password field, confirm password, submit button, validation messages | FR-AUTH-001 |
| Login Page | Returning user authentication | Email field, password field, "Forgot password" link, submit button | FR-AUTH-003 |
| Admin Dashboard | User management interface | User table with pagination, filters (status, date), search bar | FR-ADMIN-001, FR-ADMIN-002 |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

<!-- 
  UI mockup references should be added here once the System Designer produces wireframes.
  Format: Link to design/wireframes/<screen-name>.png
-->

### 5.2 API Contract Summary

<!--
  High-level API contracts. Detailed specs go in architecture/api-specifications/.
-->

| Endpoint | Method | Description | Request Body | Response | Source FRs |
|----------|--------|-------------|-------------|----------|-----------|
| `/v1/auth/register` | POST | Register a new user | `{ email, password }` | `201: { userId, message }` | FR-AUTH-001 |
| `/v1/auth/verify` | GET | Verify email via token | Query: `?token=xxx` | `200: { message }` / `400: { error }` | FR-AUTH-002 |
| `/v1/auth/reset-password` | POST | Request password reset | `{ email }` | `200: { message }` | FR-AUTH-003 |
| `/v1/admin/users` | GET | List users (paginated) | Query: `?page=1&limit=20&status=active` | `200: { users[], total, page }` | FR-ADMIN-001, FR-ADMIN-002 |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## 6. Dependency Matrix

<!--
  Show which functional requirements depend on others.
  This determines implementation order and identifies critical-path items.
-->

| FR-ID | Depends On | Dependency Type | Notes |
|-------|-----------|----------------|-------|
| FR-AUTH-002 | FR-AUTH-001 | Sequential | Cannot verify email without a registered account |
| FR-AUTH-003 | FR-AUTH-001 | Sequential | Cannot reset password without a registered account |
| FR-ADMIN-001 | FR-AUTH-001 | Data dependency | Admin dashboard displays User entities created by registration |
| FR-ADMIN-002 | FR-ADMIN-001 | Functional | Filtering extends the base user listing |
| [PLACEHOLDER] | [PLACEHOLDER] | [Sequential/Data dependency/Functional/Technical] | [PLACEHOLDER] |

<!--
  Dependency Types:
  - Sequential: B cannot start until A completes.
  - Data dependency: B reads data produced by A.
  - Functional: B extends or refines A's behavior.
  - Technical: B requires A's technical infrastructure (e.g., auth middleware).
-->

---

## 7. Traceability Matrix

<!--
  CRITICAL: This matrix links the entire chain: User Story → Functional Requirement → Test Case.
  QC Agents use this to derive test cases. If a cell is empty, coverage is missing.
  Update this matrix continuously as requirements and test cases are added.
-->

| User Story | Functional Requirement(s) | Test Case(s) | Status |
|-----------|--------------------------|-------------|--------|
| US-001 | FR-AUTH-001, FR-AUTH-002 | [TC-AUTH-001, TC-AUTH-002 — to be created by QC] | Requirements defined |
| US-002 | FR-AUTH-003 | [TC-AUTH-003 — to be created by QC] | Requirements defined |
| US-003 | FR-ADMIN-001, FR-ADMIN-002 | [TC-ADMIN-001, TC-ADMIN-002 — to be created by QC] | Requirements defined |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [Requirements defined / Tests designed / Tests passed] |

<!--
  Status values:
  - Requirements defined: FRs exist but no test cases yet.
  - Tests designed: Test cases created by QC but not executed.
  - Tests passed: All linked test cases passed in the latest iteration.
  - Tests failed: One or more linked test cases failed — see defect reports.
-->

---

## 8. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | YYYY-MM-DD | System Architect | Initial template created |
| | | | |

---

<!--
  DOWNSTREAM DEPENDENCIES:
  - architecture/technical-architecture.md reads Module Decomposition (Section 1) to define containers.
  - architecture/data-model.md reads Data Requirements (Section 4) to build the full schema.
  - architecture/api-specifications/ reads Interface Requirements (Section 5.2) for OpenAPI specs.
  - qa/test-cases/ reads the Traceability Matrix (Section 7) to derive test cases.
  - design/ reads Interface Requirements (Section 5.1) for UI/UX design.
-->
