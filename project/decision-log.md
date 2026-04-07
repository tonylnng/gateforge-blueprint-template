# Decision Log

<!-- AGENT INSTRUCTION: This is an append-only decision record for the GateForge project.
     The System Architect maintains this document. Decisions are NEVER deleted or modified
     after recording — only their status can change (accepted → superseded / deprecated).
     Significant decisions also get a detail section in ADR format below the summary table. -->

| Field | Value |
|---|---|
| **Document ID** | PRJ-DECISIONS-001 |
| **Version** | 0.1.0 |
| **Owner** | System Architect |
| **Status** | Living Document |
| **Last Updated** | [PLACEHOLDER] |

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
