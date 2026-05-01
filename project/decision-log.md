# Decision Log

> **🛑 STOP — Mandatory reading before recording or revising any ADR.** Read **[`project/AGENTS.md`](AGENTS.md)** and **[`/VERSIONING.md`](../VERSIONING.md)** first. New ADRs MUST cite the AGENTS.md and VERSIONING.md sections they comply with (`agent.doc-citation.present`).

<!-- AGENT INSTRUCTION: This is an append-only decision record for the GateForge project.
     The System Architect maintains this document. Decisions are NEVER deleted or modified
     after recording — only their status can change (accepted → superseded / deprecated).
     Significant decisions also get a detail section in ADR format below the summary table. -->

| Field | Value |
|---|---|
| **Document ID** | PRJ-DECISIONS-001 |
| **Version** | 0.2.0 |
| **Owner** | System Architect |
| **Status** | Living Document |
| **Last Updated** | 2026-05-01 |

---

## Revision History

| Version | Date | Author | Change Summary |
|---|---|---|---|
| 0.2.0 | 2026-05-01 | System Architect | Recorded **ADR-005** (Versioning Policy) and **ADR-006** (Agent Compliance Enforcement). |
| 0.1.0 | [PLACEHOLDER] | System Architect | Initial decisions ADR-001…ADR-004. |

---

## Decision Log

<!-- AGENT INSTRUCTION: Add a new row for every architectural or project decision.
     Use sequential IDs: ADR-001, ADR-002, etc.
     Status: proposed, accepted, superseded, deprecated.
     Impact: low, medium, high.
     Significant decisions (medium/high impact) must also have a detail section below. -->

| Decision ID | Date | Title | Context | Decision | Rationale | Impact | Status | Decided By |
|---|---|---|---|---|---|---|---|---|
| ADR-001 | 2026-03-10 | Backend Framework Selection | Need a structured, TypeScript-native backend framework with strong DI support | Use NestJS as the backend framework | Mature ecosystem, built-in DI, TypeScript-first, modular architecture aligns with multi-agent development | High | accepted | System Architect |
| ADR-002 | 2026-03-10 | Database Selection | Need a relational database for structured data with strong ACID guarantees | Use PostgreSQL as the primary database | Industry standard, excellent TypeScript ORM support (Prisma), JSON column support, proven scalability | High | accepted | System Architect |
| ADR-003 | 2026-03-12 | Authentication Strategy | Need secure, stateless authentication suitable for web and mobile clients | Use JWT with short-lived access tokens (15m) and long-lived refresh tokens (7d) stored in httpOnly cookies | Industry standard for SPAs, stateless reduces DB load, refresh tokens mitigate short access token risk | High | accepted | System Architect |
| ADR-004 | 2026-03-15 | Real-time Communication | Need real-time notification delivery to connected clients | Use WebSocket (Socket.IO) over SSE | Bidirectional communication needed for future features, Socket.IO provides automatic reconnection and room support | Medium | accepted | System Architect |
| ADR-005 | 2026-05-01 | Versioning Policy & Auto-Bump | Repo owner requires every push to bump `VERSION` automatically and tag a release in GitHub, including doc-only commits, so that history is fully traceable | Adopt semver `MAJOR.MINOR.PATCH`. **MAJOR** is human-only via `Version-Bump: major` commit trailer (author must be `tonylnng`). **MINOR / PATCH** auto-bumped by `.github/workflows/version-bump.yml` from Conventional-Commit types (`feat`→MINOR, `fix\|docs\|refactor\|test\|chore`→PATCH; mixed feat+fix→MINOR with PATCH reset). Workflow runs on every push, writes `VERSION`, prepends a CHANGELOG entry, creates a tag, and skips its own commit via `[skip version-bump]`. | Eliminates manual version drift; provides a single source of truth (`VERSION` + git tag); satisfies repo owner's auditability requirement | High | accepted | System Architect (proposed); Tony NG (approved) |
| ADR-006 | 2026-05-01 | Agent Compliance Enforcement (four-layer pattern) | QC agents (and other roles) historically skipped sections of role-specific MD files (e.g., `qa/test-plan.md` E2E section). Need a way to make compliance unavoidable, not optional | Adopt a four-layer enforcement pattern: (1) per-role `AGENTS.md` as the mandatory entry point in every role-owned directory; (2) Pre-Flight Acknowledgement block at the top of every PR / release-evidence pack listing each AGENTS.md read with version; (3) doc-citation requirement on every behavioural change (`per <doc> v<X.Y> §N`); (4) Admin-Portal validation gates `agent.preflight.present`, `agent.doc-citation.present`, `agent.test-coverage.gates`, `versioning.semver.compliance`. Eight named QA gates in `qa/AGENTS.md` (QA-G1…QA-G8) make E2E (QA-G3) non-skippable. | Single mandatory entry point + machine-checkable evidence, addressing the QC E2E pain point directly | High | accepted | System Architect (proposed); Tony NG (approved) |

<!-- AGENT INSTRUCTION: Add new rows above this comment. Use this template:

| ADR-NNN | YYYY-MM-DD | Title | Context summary | Decision summary | Rationale summary | Low/Medium/High | proposed/accepted | Decided By |

-->

---

## Decision Details (ADR Format)

<!-- AGENT INSTRUCTION: For each significant decision (medium/high impact), create a detail section below
     using the Architecture Decision Record (ADR) format. This provides the full reasoning. -->

---

### ADR-001: Backend Framework Selection

**Date:** 2026-03-10
**Status:** Accepted
**Decided By:** System Architect

#### Context

GateForge requires a backend framework that:
- Is TypeScript-native (aligns with the full-stack TypeScript strategy)
- Supports dependency injection for modular, testable architecture
- Has a mature ecosystem with middleware, guards, interceptors, and pipes
- Enables multiple developer agents to work on isolated modules simultaneously

#### Options Considered

| Option | Pros | Cons |
|---|---|---|
| **NestJS** | TypeScript-first, built-in DI, modular architecture, large ecosystem, Angular-inspired structure | Heavier than Express alone, learning curve for developers unfamiliar with DI |
| **Express + TypeScript** | Minimal, flexible, widely known | No built-in structure, DI requires manual setup, harder to enforce conventions across agents |
| **Fastify** | Excellent performance, schema-based validation | Smaller ecosystem, less opinionated structure |

#### Decision

Use **NestJS** as the backend framework for all GateForge API services.

#### Consequences

- **Positive:** Consistent module structure across all developer agents. Built-in support for guards, interceptors, and pipes simplifies cross-cutting concerns. Strong TypeScript support with decorators.
- **Negative:** Slightly larger bundle size and memory footprint compared to raw Express. Developers must understand the NestJS module system.
- **Neutral:** NestJS uses Express (or optionally Fastify) under the hood, so low-level Express middleware remains compatible.

---

### ADR-002: Database Selection

**Date:** 2026-03-10
**Status:** Accepted
**Decided By:** System Architect

#### Context

GateForge needs a primary database that:
- Provides ACID transactions for data integrity
- Supports complex queries (joins, aggregations)
- Has excellent TypeScript ORM support
- Can handle the expected scale (thousands of concurrent users)

#### Options Considered

| Option | Pros | Cons |
|---|---|---|
| **PostgreSQL** | Mature, ACID-compliant, excellent Prisma support, JSON columns, full-text search, strong community | Requires more operational expertise than managed NoSQL options |
| **MySQL** | Widely used, good performance | Weaker JSON support, less advanced query capabilities |
| **MongoDB** | Flexible schema, easy horizontal scaling | No ACID transactions across collections (pre-5.0), schema-less can lead to inconsistency |

#### Decision

Use **PostgreSQL** as the primary database, accessed via **Prisma ORM**.

#### Consequences

- **Positive:** Strong data integrity guarantees. Prisma provides type-safe database access. JSON columns allow flexible metadata storage. Proven at scale.
- **Negative:** Requires more careful schema design upfront. Horizontal scaling requires additional tooling (e.g., Citus, read replicas).
- **Neutral:** Managed PostgreSQL available on all major cloud providers.

---

### ADR-003: Authentication Strategy

**Date:** 2026-03-12
**Status:** Accepted
**Decided By:** System Architect

#### Context

GateForge requires authentication for web (React SPA) and mobile (React Native) clients. The solution must:
- Be stateless to support horizontal scaling
- Provide secure token storage resistant to XSS and CSRF
- Support token refresh without forcing re-login
- Work across web and mobile platforms

#### Options Considered

| Option | Pros | Cons |
|---|---|---|
| **JWT (access + refresh tokens)** | Stateless, scalable, works on web and mobile, industry standard | Requires careful token storage strategy, cannot revoke individual access tokens |
| **Session-based (server-side)** | Simple, easy to revoke | Requires session store (Redis), not truly stateless, harder for mobile |
| **OAuth2 + OpenID Connect (external provider)** | Delegates auth complexity, social login built-in | Dependency on external service, more complex setup |

#### Decision

Use **JWT-based authentication** with:
- Short-lived access tokens (15 minutes)
- Long-lived refresh tokens (7 days) stored in httpOnly, Secure, SameSite cookies (web) or secure storage (mobile)
- Redis-backed token blacklist for logout/revocation

#### Consequences

- **Positive:** Stateless access token verification (no DB lookup per request). Short access token lifetime limits exposure. httpOnly cookies prevent XSS-based token theft.
- **Negative:** Token revocation requires a Redis blacklist check (slight latency). Refresh token rotation adds implementation complexity.
- **Neutral:** Social login (ADR planned) will layer on top of this base strategy.

---

### ADR-004: Real-time Communication

**Date:** 2026-03-15
**Status:** Accepted
**Decided By:** System Architect

#### Context

GateForge needs real-time notification delivery. Evaluated during SPIKE-001.

#### Options Considered

| Option | Pros | Cons |
|---|---|---|
| **WebSocket (Socket.IO)** | Bidirectional, automatic reconnection, room/namespace support, wide browser support | More server resources than SSE, requires sticky sessions or Redis adapter for scaling |
| **Server-Sent Events (SSE)** | Simple, HTTP-based, auto-reconnect, lower server overhead | Unidirectional only, limited browser connection pool (6 per domain), no native binary support |
| **Long Polling** | Works everywhere, simple implementation | Higher latency, more server load due to repeated connections |

#### Decision

Use **WebSocket via Socket.IO** with the Redis adapter for horizontal scaling.

#### Consequences

- **Positive:** Bidirectional communication supports future features (real-time collaboration, typing indicators). Socket.IO's Redis adapter handles multi-pod scaling. Automatic reconnection and fallback to long polling.
- **Negative:** Requires Redis adapter configuration. WebSocket connections consume more server memory than SSE. Need to handle connection lifecycle carefully.
- **Neutral:** Socket.IO is a well-maintained library with strong NestJS integration (`@nestjs/websockets`).

---

### ADR-005: Versioning Policy & Auto-Bump

**Date:** 2026-05-01
**Status:** Accepted
**Decided By:** System Architect (proposed) — Tony NG (approved)

#### Context

The GateForge Blueprint Repository did not have an enforced versioning convention.
The repo owner (Tony NG) requires that **every push to the repository — including
documentation-only commits — results in a traceable version bump and a corresponding
GitHub tag**, so that any change can be located by version. The convention is
`MAJOR.MINOR.PATCH` (e.g. `1.0.0`).

The owner specified the bump rules:
- **MAJOR** — human-only; the owner decides when application changes are large
  enough to warrant it.
- **MINOR** — auto, when a push contains feature upgrades. If a push contains both
  features and bug-fixes, MINOR still bumps and PATCH resets to `0`.
- **PATCH** — auto, when a push contains only fixes / refactors / tests / docs.

#### Options Considered

| Option | Pros | Cons |
|---|---|---|
| **Real GitHub Actions workflow that reads commit messages and bumps `VERSION` + tags** | Fully enforced; no human bookkeeping; runs on every push automatically; integrates with PR template & validation | Requires write access for the workflow; needs care to avoid recursion (`[skip version-bump]` trailer) |
| Manual `VERSION` + CHANGELOG updates per PR | Simple, no automation needed | Easy to forget; defeats the owner's stated goal of *guaranteed* traceability |
| Release-Please / semantic-release third-party tool | Mature, widely used | Heavier dependency; less aligned with the simple `VERSION` file the owner requested |

#### Decision

Adopt the GitHub Actions workflow approach with the following implementation:

- `VERSION` file at repo root, single line, semver, baseline `0.2.0`.
- `/VERSIONING.md` documents the policy and the bump decision tree.
- `.github/workflows/version-bump.yml` runs on every push to any branch, with a
  concurrency group keyed on the branch.
- `decide_bump.py` parses commit subjects since the last tag and decides MAJOR /
  MINOR / PATCH; rejects manual edits to `VERSION` (must be done by the workflow).
- `apply_bump.py` writes the new `VERSION`, prepends a `CHANGELOG.md` entry, and
  creates an annotated git tag.
- The workflow's own commit carries `[skip version-bump]` to prevent recursion.
- The workflow ignores commits authored by `github-actions[bot]`.
- **MAJOR** is gated to author `tonylnng` AND the presence of a `Version-Bump: major`
  commit trailer.
- The Admin Portal validates `versioning.semver.compliance` (see
  `project/admin-portal-validation.md` §3.7).

#### Consequences

- **Positive:** Every push produces a traceable version + tag automatically. The
  `VERSION` file gives a single source of truth. The CHANGELOG is always in sync.
  Documentation-only commits are versioned, satisfying the owner's intent.
- **Negative:** Many tags will be produced (one per push). Slight CI cost per push.
  Authors must use Conventional-Commit types or the workflow falls back to PATCH.
- **Neutral:** Existing CHANGELOG history is preserved; the workflow appends new
  entries above the most recent.

---

### ADR-006: Agent Compliance Enforcement (four-layer pattern)

**Date:** 2026-05-01
**Status:** Accepted
**Decided By:** System Architect (proposed) — Tony NG (approved)

#### Context

The repo owner reported a recurring pain point: **QC agents skipped the E2E
testing section of `qa/test-plan.md`**, even though it is a published quality
gate. The same risk applies to every role-specific MD file (architecture,
operations runbook, etc.). Markdown alone is not enforceable.

#### Options Considered

| Option | Pros | Cons |
|---|---|---|
| **Four-layer pattern: AGENTS.md entry points + Pre-Flight Acknowledgement + doc-citation requirement + Admin-Portal validation gates** | Single mandatory entry point per role; machine-checkable evidence; directly addresses the E2E pain point; reuses existing Admin Portal validation harness | Adds ceremony to every PR; agents must be retrained on the Pre-Flight format |
| Add a checklist to the existing PR template only | Lightweight | Same failure mode — agents tick boxes without reading; no per-role enforcement |
| Build a separate compliance bot that posts on every PR | Highly visible | Heavy to build; duplicates Admin Portal responsibilities |

#### Decision

Adopt the four-layer pattern:

1. **Mandatory entry point** — a per-role `AGENTS.md` file lives at the root of
   every role-owned directory (`requirements/`, `architecture/`, `design/`,
   `development/`, `qa/`, `operations/`, `project/`). Each AGENTS.md lists
   mandatory reading, the Pre-Flight template, role gates, commit conventions,
   and known failure modes.
2. **Pre-Flight Acknowledgement** — every PR / release-evidence pack starts with
   a Pre-Flight block listing each AGENTS.md the author read with the version they
   read.
3. **Evidence-of-compliance citations** — deliverables cite the source doc
   + version they comply with, e.g. `per qa/test-plan.md v1.1 §2.3`.
4. **Admin Portal validation gates** — `agent.preflight.present`,
   `agent.doc-citation.present`, `agent.test-coverage.gates` (named QA gates
   QA-G1…QA-G8), `versioning.semver.compliance`. See
   `project/admin-portal-validation.md` §3.7.

#### Consequences

- **Positive:** E2E (QA-G3) becomes non-skippable — a missing gate row in the QC
  report fails `agent.test-coverage.gates`. Pre-Flight makes "I forgot to read X"
  impossible to claim. Doc-citation makes drift detectable.
- **Negative:** Higher ceremony per PR. Authors must update Pre-Flight when
  AGENTS.md versions change.
- **Neutral:** Pattern is composable — future roles can drop in their own
  AGENTS.md without reworking the validation harness.

<!-- AGENT INSTRUCTION: For each new significant decision, copy the template below:

---

### ADR-NNN: [Title]

**Date:** YYYY-MM-DD
**Status:** Proposed / Accepted / Superseded / Deprecated
**Decided By:** [Role]

#### Context

[PLACEHOLDER — What is the issue or decision that needs to be made? What are the constraints?]

#### Options Considered

| Option | Pros | Cons |
|---|---|---|
| **Option A** | [PLACEHOLDER] | [PLACEHOLDER] |
| **Option B** | [PLACEHOLDER] | [PLACEHOLDER] |
| **Option C** | [PLACEHOLDER] | [PLACEHOLDER] |

#### Decision

[PLACEHOLDER — What was decided and any key parameters]

#### Consequences

- **Positive:** [PLACEHOLDER]
- **Negative:** [PLACEHOLDER]
- **Neutral:** [PLACEHOLDER]

-->
