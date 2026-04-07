# Technical Architecture Document

<!--
  STANDARD: C4 Model (Context, Container, Component, Code)
  PURPOSE: Define the system architecture using hierarchical diagrams from the broadest
           context down to component-level detail, plus technology decisions, communication
           patterns, deployment topology, and cross-cutting concerns.
  OWNER: System Architect
  CONTRIBUTOR: System Designer
  
  INSTRUCTIONS FOR THE ARCHITECT:
  1. Start from the System Context level and work downward.
  2. Every Mermaid diagram must be self-explanatory — include labels on all relationships.
  3. Technology choices must include version and justification.
  4. ADRs capture the "why" behind significant decisions — create one for each contested choice.
  5. This document feeds into design/ (Designer) and development/ (Developers).
-->

## Document Metadata

| Field | Value |
|-------|-------|
| **Document ID** | `ARCH-TECH-001` |
| **Version** | `0.1` |
| **Status** | `Draft` |
| **Owner** | System Architect |
| **Last Updated** | `YYYY-MM-DD` |
| **Approved By** | — |
| **Source Documents** | `requirements/functional-requirements.md`, `requirements/non-functional-requirements.md` |
| **Standard** | C4 Model |

---

## 1. System Context Diagram (C4 Level 1)

<!--
  The highest level of abstraction. Shows the system as a single box, surrounded by
  the users and external systems it interacts with.
  Replace [PLACEHOLDER] elements with actual actors and systems.
-->

```mermaid
C4Context
    title System Context Diagram — [PLACEHOLDER — Project Name]

    Person(user, "End User", "Uses the web and mobile applications")
    Person(admin, "Administrator", "Manages users, content, and system configuration")

    System(system, "[PLACEHOLDER — Project Name]", "The core platform providing [PLACEHOLDER — primary capability]")

    System_Ext(email, "Email Service", "[PLACEHOLDER — e.g., SendGrid / AWS SES] for transactional emails")
    System_Ext(payment, "Payment Gateway", "[PLACEHOLDER — e.g., Stripe] for payment processing")
    System_Ext(monitoring, "Monitoring Stack", "[PLACEHOLDER — e.g., Datadog / Grafana Cloud] for observability")
    System_Ext(cdn, "CDN", "[PLACEHOLDER — e.g., CloudFront / Cloudflare] for static asset delivery")

    Rel(user, system, "Uses", "HTTPS")
    Rel(admin, system, "Manages", "HTTPS")
    Rel(system, email, "Sends emails", "SMTP / API")
    Rel(system, payment, "Processes payments", "HTTPS / API")
    Rel(system, monitoring, "Sends telemetry", "HTTPS / gRPC")
    Rel(system, cdn, "Serves static assets", "HTTPS")
```

<!--
  If the Mermaid C4 extension is not available in your renderer, use the following
  flowchart-based alternative:
-->

```mermaid
flowchart TD
    subgraph External Actors
        User["👤 End User"]
        Admin["👤 Administrator"]
    end

    subgraph "System Boundary"
        System["[PLACEHOLDER — Project Name]\n Core Platform"]
    end

    subgraph External Systems
        Email["📧 Email Service\n[PLACEHOLDER]"]
        Payment["💳 Payment Gateway\n[PLACEHOLDER]"]
        Monitor["📊 Monitoring\n[PLACEHOLDER]"]
        CDN["🌐 CDN\n[PLACEHOLDER]"]
    end

    User -->|"HTTPS"| System
    Admin -->|"HTTPS"| System
    System -->|"SMTP/API"| Email
    System -->|"HTTPS/API"| Payment
    System -->|"Telemetry"| Monitor
    System -->|"Static Assets"| CDN
```

---

## 2. Container Diagram (C4 Level 2)

<!--
  Zoom into the system boundary. Show the major deployable units:
  applications, services, databases, message queues, caches.
  Each container is a separately running process or deployable artifact.
-->

```mermaid
flowchart TD
    subgraph "Client Layer"
        WebApp["React Web App\nTypeScript / React\nSingle Page Application"]
        MobileApp["React Native App\nTypeScript / React Native\niOS & Android"]
    end

    subgraph "API Layer"
        Gateway["API Gateway\nNestJS\nRouting, rate limiting, auth"]
    end

    subgraph "Service Layer"
        AuthSvc["Auth Service\nNestJS\nRegistration, login, JWT"]
        CoreSvc["[PLACEHOLDER] Service\nNestJS\n[PLACEHOLDER — primary business logic]"]
        NotifSvc["Notification Service\nNestJS\nEmail, push, in-app notifications"]
    end

    subgraph "Data Layer"
        PG[("PostgreSQL\nPrimary database\nUser data, business entities")]
        Redis[("Redis Cluster\nSession cache, rate limiting\nPub/Sub for real-time")]
        MQ["Message Queue\n[PLACEHOLDER — e.g., RabbitMQ / Redis Streams]\nAsync task processing"]
    end

    subgraph "External"
        Email["Email Service"]
        CDN["CDN"]
    end

    WebApp -->|"HTTPS/REST"| Gateway
    MobileApp -->|"HTTPS/REST"| Gateway
    CDN -->|"Serves"| WebApp

    Gateway -->|"Internal REST"| AuthSvc
    Gateway -->|"Internal REST"| CoreSvc
    Gateway -->|"Internal REST"| NotifSvc

    AuthSvc -->|"SQL"| PG
    AuthSvc -->|"Cache"| Redis
    CoreSvc -->|"SQL"| PG
    CoreSvc -->|"Cache"| Redis
    CoreSvc -->|"Publish"| MQ
    NotifSvc -->|"Subscribe"| MQ
    NotifSvc -->|"API"| Email
```

<!--
  REPLACE placeholder services with actual services from Module Decomposition
  (requirements/functional-requirements.md Section 1).
  Add or remove services as the architecture evolves.
-->

---

## 3. Component Diagrams (C4 Level 3)

<!--
  Zoom into individual containers to show their internal components.
  Create one diagram per key service. Focus on services with complex internal structure.
-->

### 3.1 Auth Service — Component Diagram

```mermaid
flowchart TD
    subgraph "Auth Service"
        Controller["Auth Controller\nREST endpoints:\nPOST /register\nPOST /login\nPOST /refresh\nPOST /reset-password"]
        AuthGuard["JWT Auth Guard\nMiddleware: validates tokens\non protected routes"]
        UserSvc["User Service\nBusiness logic:\nregistration, verification,\npassword management"]
        TokenSvc["Token Service\nJWT generation,\nvalidation, refresh\ntoken rotation"]
        HashSvc["Hash Service\nbcrypt password\nhashing and verification"]
        UserRepo["User Repository\nTypeORM / Prisma\nPostgreSQL queries"]
        SessionRepo["Session Repository\nRedis operations:\ntoken storage, TTL"]
    end

    Controller --> AuthGuard
    Controller --> UserSvc
    Controller --> TokenSvc
    UserSvc --> HashSvc
    UserSvc --> UserRepo
    TokenSvc --> SessionRepo
    UserRepo -->|"SQL"| PG[("PostgreSQL")]
    SessionRepo -->|"Cache"| Redis[("Redis")]
```

### 3.2 [PLACEHOLDER — Service Name] — Component Diagram

```mermaid
flowchart TD
    subgraph "[PLACEHOLDER — Service Name]"
        Ctrl["[PLACEHOLDER] Controller\n[PLACEHOLDER — endpoints]"]
        Svc["[PLACEHOLDER] Service\n[PLACEHOLDER — business logic]"]
        Repo["[PLACEHOLDER] Repository\n[PLACEHOLDER — data access]"]
    end

    Ctrl --> Svc
    Svc --> Repo
    Repo -->|"SQL"| DB[("PostgreSQL")]
```

<!-- Add more component diagrams as needed — one per complex service. -->

---

## 4. Technology Stack

<!--
  Every technology choice must include version and justification.
  The justification should reference project requirements or constraints.
-->

| Layer | Technology | Version | Justification |
|-------|-----------|---------|---------------|
| **Frontend — Web** | React | [PLACEHOLDER — e.g., 18.x] | Industry-standard SPA framework; large ecosystem; team familiarity |
| **Frontend — Mobile** | React Native | [PLACEHOLDER — e.g., 0.73.x] | Code sharing with React web; single TypeScript codebase |
| **Language** | TypeScript | [PLACEHOLDER — e.g., 5.x] | Type safety across full stack; reduces runtime errors |
| **Backend Framework** | NestJS | [PLACEHOLDER — e.g., 10.x] | Modular architecture; TypeScript-native; built-in DI, guards, interceptors |
| **API Protocol** | REST (OpenAPI 3.0) | — | Standard protocol; broad client support; tooling ecosystem |
| **Primary Database** | PostgreSQL | [PLACEHOLDER — e.g., 16.x] | ACID compliance; JSON support; proven scalability; rich indexing |
| **Cache / Session Store** | Redis | [PLACEHOLDER — e.g., 7.x] | Sub-millisecond latency; built-in TTL; Pub/Sub for real-time |
| **Message Queue** | [PLACEHOLDER — e.g., RabbitMQ / Redis Streams] | [PLACEHOLDER] | [PLACEHOLDER — justification] |
| **ORM** | [PLACEHOLDER — e.g., TypeORM / Prisma] | [PLACEHOLDER] | [PLACEHOLDER — justification] |
| **Containerization** | Docker | [PLACEHOLDER — e.g., 24.x] | Reproducible builds; consistent environments |
| **Orchestration** | Kubernetes | [PLACEHOLDER — e.g., 1.28+] | Production-grade orchestration; auto-scaling; self-healing |
| **CI/CD** | [PLACEHOLDER — e.g., GitHub Actions / GitLab CI] | — | [PLACEHOLDER — justification] |
| **Monitoring** | [PLACEHOLDER — e.g., Prometheus + Grafana] | — | [PLACEHOLDER — justification] |
| **Logging** | [PLACEHOLDER — e.g., ELK / Loki] | — | [PLACEHOLDER — justification] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## 5. Communication Patterns

<!--
  Define how services communicate with each other.
  Mix of synchronous and asynchronous patterns is typical.
-->

### 5.1 Synchronous Communication (REST)

| Caller | Callee | Protocol | Endpoint Pattern | Use Case |
|--------|--------|----------|-----------------|----------|
| API Gateway | Auth Service | HTTP/REST | `/internal/auth/*` | Authentication, token validation |
| API Gateway | [PLACEHOLDER] Service | HTTP/REST | `/internal/[PLACEHOLDER]/*` | [PLACEHOLDER] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### 5.2 Asynchronous Communication (Message Queue)

| Publisher | Event | Consumer(s) | Queue/Topic | Use Case |
|-----------|-------|-------------|-------------|----------|
| Auth Service | `user.registered` | Notification Service | `user-events` | Send welcome email after registration |
| [PLACEHOLDER] Service | `[PLACEHOLDER]` | [PLACEHOLDER] | `[PLACEHOLDER]` | [PLACEHOLDER] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### 5.3 Real-Time Communication

| Technology | Use Case | Protocol | Notes |
|-----------|----------|----------|-------|
| [PLACEHOLDER — e.g., WebSocket via Socket.IO] | [PLACEHOLDER — e.g., Live notifications, real-time updates] | WSS | [PLACEHOLDER — e.g., Redis Pub/Sub as backend for horizontal scaling] |
| [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## 6. Data Flow Diagrams

<!--
  Show how data moves through the system for key operations.
  One diagram per critical data flow.
-->

### 6.1 [PLACEHOLDER — Flow Name, e.g., User Registration Data Flow]

```mermaid
flowchart LR
    A["Client\n(React App)"] -->|"1. POST /v1/auth/register\n{email, password}"| B["API Gateway"]
    B -->|"2. Forward request"| C["Auth Service"]
    C -->|"3. Hash password\n(bcrypt)"| C
    C -->|"4. INSERT user"| D[("PostgreSQL")]
    D -->|"5. User record created"| C
    C -->|"6. Publish event\nuser.registered"| E["Message Queue"]
    E -->|"7. Consume event"| F["Notification Service"]
    F -->|"8. Send verification email"| G["Email Service\n(External)"]
    C -->|"9. Return userId"| B
    B -->|"10. 201 Created\n{userId, message}"| A
```

### 6.2 [PLACEHOLDER — Flow Name]

```mermaid
flowchart LR
    A["[PLACEHOLDER — Source]"] -->|"[PLACEHOLDER — Step 1]"| B["[PLACEHOLDER — Target]"]
    B -->|"[PLACEHOLDER — Step 2]"| C["[PLACEHOLDER — Target]"]
```

---

## 7. Deployment Architecture

<!--
  Show the Kubernetes cluster topology, namespaces, pods, and external service connections.
  This feeds directly into design/infrastructure-design.md.
-->

```mermaid
flowchart TD
    subgraph "Internet"
        Users["Users"]
        CDN["CDN\n[PLACEHOLDER]"]
    end

    subgraph "Kubernetes Cluster"
        subgraph "ingress namespace"
            Ingress["Ingress Controller\nNginx / Traefik\nTLS termination"]
        end

        subgraph "app namespace"
            GW["API Gateway\n2+ replicas"]
            Auth["Auth Service\n2+ replicas"]
            Core["[PLACEHOLDER] Service\n2+ replicas"]
            Notif["Notification Service\n2+ replicas"]
        end

        subgraph "data namespace"
            PG["PostgreSQL\nPrimary + Read Replica"]
            Redis["Redis Cluster\n3+ nodes"]
            MQ["[PLACEHOLDER — Message Queue]\n[PLACEHOLDER — HA config]"]
        end

        subgraph "monitoring namespace"
            Prom["Prometheus"]
            Grafana["Grafana"]
            Loki["[PLACEHOLDER — Log aggregator]"]
        end
    end

    subgraph "External Services"
        EmailExt["Email Service"]
        PaymentExt["[PLACEHOLDER]"]
    end

    Users -->|"HTTPS"| CDN
    CDN -->|"Static assets"| Users
    Users -->|"API requests"| Ingress
    Ingress --> GW
    GW --> Auth
    GW --> Core
    GW --> Notif
    Auth --> PG
    Auth --> Redis
    Core --> PG
    Core --> Redis
    Core --> MQ
    Notif --> MQ
    Notif --> EmailExt
    Prom -->|"Scrapes metrics"| GW
    Prom -->|"Scrapes metrics"| Auth
    Prom -->|"Scrapes metrics"| Core
```

---

## 8. Cross-Cutting Concerns

<!--
  These concerns span all services and must be implemented consistently.
  Each concern should reference the design/ document where it is detailed.
-->

### 8.1 Authentication & Authorization

| Aspect | Approach | Details |
|--------|---------|---------|
| Authentication | JWT (access + refresh tokens) | See NFR-SEC-001; detailed in `design/security-design.md` |
| Authorization | RBAC with guards | NestJS `@Roles()` decorator + `RolesGuard`; roles stored in JWT claims |
| Service-to-service auth | [PLACEHOLDER — e.g., Internal API keys / mTLS] | [PLACEHOLDER] |

### 8.2 Logging

| Aspect | Approach | Details |
|--------|---------|---------|
| Log format | Structured JSON | `{ timestamp, level, service, traceId, message, metadata }` |
| Log levels | `error`, `warn`, `info`, `debug` | Production: `info`+; Staging: `debug`+ |
| Correlation | Distributed trace ID | Injected at API Gateway; propagated via `x-trace-id` header |
| Aggregation | [PLACEHOLDER — e.g., Loki / ELK] | See `design/monitoring-design.md` |

### 8.3 Monitoring & Alerting

| Aspect | Approach | Details |
|--------|---------|---------|
| Metrics | [PLACEHOLDER — e.g., Prometheus] | RED metrics (Rate, Errors, Duration) per service |
| Dashboards | [PLACEHOLDER — e.g., Grafana] | Service health, latency percentiles, error rates |
| Alerting | [PLACEHOLDER — e.g., Alertmanager → PagerDuty/Slack] | See `design/monitoring-design.md` |

### 8.4 Error Handling

| Aspect | Approach | Details |
|--------|---------|---------|
| Error response format | Standardized JSON | `{ statusCode, error, message, traceId }` |
| Exception filters | NestJS global exception filter | Catches unhandled exceptions; logs; returns sanitized response |
| Retry policy | Exponential backoff with jitter | Max 3 retries; inter-service calls only |
| Circuit breaker | [PLACEHOLDER — e.g., Custom / opossum] | Open after 5 consecutive failures; half-open after 30s |

---

## 9. Architecture Decision Records (ADRs)

<!--
  Document significant architectural decisions using the ADR format below.
  Create one ADR for each contested or non-obvious choice.
  ADR-IDs are sequential: ADR-001, ADR-002, etc.
-->

### ADR Template

```
### ADR-<NNN>: <Title>

| Field | Value |
|-------|-------|
| **Status** | Proposed / Accepted / Deprecated / Superseded |
| **Date** | YYYY-MM-DD |
| **Decision Makers** | System Architect, [others] |

**Context:**
[What is the issue or question that needs a decision?]

**Decision:**
[What was decided and why?]

**Alternatives Considered:**
1. [Alternative 1] — [Why rejected]
2. [Alternative 2] — [Why rejected]

**Consequences:**
- Positive: [Benefits of this decision]
- Negative: [Trade-offs and risks]
- Neutral: [Implications that are neither good nor bad]
```

---

### ADR-001: Use NestJS as the Backend Framework

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | [YYYY-MM-DD] |
| **Decision Makers** | System Architect |

**Context:**
The project requires a TypeScript backend framework that supports modular architecture, dependency injection, middleware, and built-in support for REST APIs. The team needs a framework that scales from MVP to production without rewrites.

**Decision:**
Use NestJS as the backend framework for all API services.

**Alternatives Considered:**
1. **Express.js (raw)** — Rejected because it lacks built-in module system, DI, and decorators. Would require extensive boilerplate for a structured multi-service architecture.
2. **Fastify (raw)** — Rejected for the same structural reasons as Express, despite better raw performance. NestJS can use Fastify as its underlying HTTP adapter if performance optimization is needed later.
3. **tRPC** — Rejected because the project requires OpenAPI-documented REST APIs for potential third-party integration. tRPC is better suited for tightly-coupled full-stack TypeScript monorepos.

**Consequences:**
- Positive: Strong module system maps cleanly to domain modules; built-in guards, interceptors, and pipes reduce boilerplate; large ecosystem of NestJS-specific packages.
- Negative: Slightly higher learning curve than raw Express; decorator-heavy code style may feel unfamiliar to developers new to NestJS.
- Neutral: Performance overhead vs. raw Fastify is negligible for most CRUD-heavy applications.

---

### ADR-002: [PLACEHOLDER — Title]

<!-- Copy the ADR template above and fill in for each significant decision. -->

| Field | Value |
|-------|-------|
| **Status** | [Proposed / Accepted] |
| **Date** | [YYYY-MM-DD] |
| **Decision Makers** | [PLACEHOLDER] |

**Context:**
[PLACEHOLDER]

**Decision:**
[PLACEHOLDER]

**Alternatives Considered:**
1. [PLACEHOLDER] — [PLACEHOLDER]
2. [PLACEHOLDER] — [PLACEHOLDER]

**Consequences:**
- Positive: [PLACEHOLDER]
- Negative: [PLACEHOLDER]
- Neutral: [PLACEHOLDER]

---

## 10. Constraints and Assumptions

### 10.1 Architectural Constraints

| # | Constraint | Impact | Source |
|---|-----------|--------|--------|
| 1 | All services must be stateless (state in PostgreSQL/Redis only). | Enables horizontal scaling; no sticky sessions. | NFR-SCAL-001 |
| 2 | All inter-service communication within the cluster uses internal DNS (no external routing). | Reduces latency; improves security. | Architecture decision |
| 3 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

### 10.2 Architectural Assumptions

| # | Assumption | Impact if Wrong | Mitigation |
|---|-----------|----------------|------------|
| 1 | A single PostgreSQL instance (with read replicas) is sufficient for Year 1 data volumes. | Would need to shard or migrate to a distributed database. | Monitor query latency; plan sharding strategy proactively. |
| 2 | Redis Cluster can handle all caching, session, and Pub/Sub needs without a separate message broker. | May need to introduce RabbitMQ/Kafka for complex event routing. | Abstract message publishing behind an interface for easy swap. |
| 3 | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

---

## 11. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | YYYY-MM-DD | System Architect | Initial template created |
| | | | |

---

<!--
  DOWNSTREAM DEPENDENCIES:
  - architecture/data-model.md derives from Containers (Section 2) and Data Flow (Section 6).
  - architecture/api-specifications/ derives from Communication Patterns (Section 5).
  - design/infrastructure-design.md derives from Deployment Architecture (Section 7).
  - design/security-design.md derives from Cross-Cutting Concerns — Auth (Section 8.1).
  - design/monitoring-design.md derives from Cross-Cutting Concerns — Monitoring (Section 8.3).
  - design/resilience-design.md derives from Cross-Cutting Concerns — Error Handling (Section 8.4).
  - development/ uses Technology Stack (Section 4) and ADRs (Section 9).
-->
