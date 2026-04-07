# Module Documentation

<!-- AGENT INSTRUCTION: This directory contains per-module technical documentation.
     Each module gets its own file named <module-name>.md.
     The owning developer agent creates and maintains the module doc.
     The System Architect reviews for consistency with architecture decisions. -->

## File Naming Convention

```
<module-name>.md
```

Examples: `auth.md`, `user-profile.md`, `notifications.md`, `payments.md`

<!-- AGENT INSTRUCTION: Module name should match the folder name under src/modules/. -->

## When to Create / Update

- **Create** when a new module is scaffolded
- **Update** when:
  - API endpoints are added, changed, or removed
  - Database tables are added or schema changes
  - Events published/consumed change
  - Dependencies on other modules change
  - Configuration (env vars) change

---

## Module Documentation Template

<!-- AGENT INSTRUCTION: Copy everything below into a new <module-name>.md file.
     Fill in all [PLACEHOLDER] values. Remove inapplicable sections. -->

```markdown
# Module: [PLACEHOLDER — Module Name]

<!-- AGENT INSTRUCTION: Keep this document in sync with the implementation.
     Update on every PR that changes this module's API, schema, events, or config. -->

## Module Metadata

| Field | Value |
|---|---|
| **Module Name** | [PLACEHOLDER] |
| **Owner Dev Agent** | [PLACEHOLDER — e.g., VM-3a] |
| **Status** | planning / in-development / active / deprecated |
| **Version** | [PLACEHOLDER — e.g., 0.1.0] |
| **Dependencies** | [PLACEHOLDER — list of npm packages specific to this module] |
| **Source Path** | `src/modules/[PLACEHOLDER]/` |

---

## Module Overview

### Purpose

[PLACEHOLDER — What does this module do? What business capability does it provide?]

### Bounded Context

[PLACEHOLDER — What domain concepts does this module own? What are its boundaries?
This module owns: ...
This module does NOT handle: ... (that is handled by <other-module>)]

---

## API Endpoints

<!-- AGENT INSTRUCTION: List every endpoint exposed by this module.
     Auth Required: Yes (role) / No / Optional.
     Reference the full request/response schemas from architecture/api-specs. -->

| Method | Path | Description | Auth Required | Request Schema | Response Schema |
|---|---|---|---|---|---|
| GET | `/api/v1/[PLACEHOLDER]` | [PLACEHOLDER] | Yes (user) | — | `[PLACEHOLDER]Response` |
| GET | `/api/v1/[PLACEHOLDER]/:id` | [PLACEHOLDER] | Yes (user) | — | `[PLACEHOLDER]Response` |
| POST | `/api/v1/[PLACEHOLDER]` | [PLACEHOLDER] | Yes (user) | `Create[PLACEHOLDER]Dto` | `[PLACEHOLDER]Response` |
| PATCH | `/api/v1/[PLACEHOLDER]/:id` | [PLACEHOLDER] | Yes (user) | `Update[PLACEHOLDER]Dto` | `[PLACEHOLDER]Response` |
| DELETE | `/api/v1/[PLACEHOLDER]/:id` | [PLACEHOLDER] | Yes (admin) | — | `204 No Content` |

---

## Database Tables Owned

<!-- AGENT INSTRUCTION: List every database table this module owns (creates, reads, writes).
     Tables read from other modules should be noted under Dependencies. -->

| Table | Purpose | Key Columns |
|---|---|---|
| `[PLACEHOLDER]` | [PLACEHOLDER] | `id (PK)`, `created_at`, `updated_at`, [PLACEHOLDER] |

---

## Events Published / Consumed

<!-- AGENT INSTRUCTION: Document all events this module emits or listens to.
     Type: domain-event, integration-event, command.
     Payload schemas should reference architecture/event-schemas if defined. -->

### Events Published

| Event | Type | Payload Schema | Description |
|---|---|---|---|
| `[PLACEHOLDER].created` | domain-event | `{ id, [PLACEHOLDER], timestamp }` | [PLACEHOLDER] |
| `[PLACEHOLDER].updated` | domain-event | `{ id, changes, timestamp }` | [PLACEHOLDER] |

### Events Consumed

| Event | Published By | Handler | Description |
|---|---|---|---|
| `[PLACEHOLDER].completed` | [PLACEHOLDER module] | `handle[PLACEHOLDER]Completed()` | [PLACEHOLDER] |

---

## Configuration

<!-- AGENT INSTRUCTION: List all environment variables this module uses.
     Never include actual secret values — only variable names and descriptions. -->

| Environment Variable | Required | Default | Description |
|---|---|---|---|
| `[PLACEHOLDER]_ENABLED` | No | `true` | Feature flag for [PLACEHOLDER] |
| `[PLACEHOLDER]_TIMEOUT_MS` | No | `5000` | Timeout for [PLACEHOLDER] operations |

---

## Dependencies on Other Modules

<!-- AGENT INSTRUCTION: List modules this module imports or calls. -->

| Module | Dependency Type | Description |
|---|---|---|
| `auth` | Import | Uses `AuthGuard` for endpoint protection |
| `[PLACEHOLDER]` | Event | Consumes `[PLACEHOLDER]` events |

---

## Known Issues / Tech Debt

<!-- AGENT INSTRUCTION: Track known issues and technical debt specific to this module.
     Link to backlog items where applicable. -->

| ID | Description | Priority | Backlog Item |
|---|---|---|---|
| TD-1 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## Change Log

<!-- AGENT INSTRUCTION: Record every significant change to this module. Link to the PR. -->

| Date | Change | Developer | PR Link |
|---|---|---|---|
| [PLACEHOLDER] | Initial module scaffolding | [PLACEHOLDER] | [PLACEHOLDER] |
```
