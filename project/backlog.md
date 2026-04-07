# Master Backlog

<!-- AGENT INSTRUCTION: This is the master backlog for the GateForge project.
     The System Architect maintains this document. All agents report items here.
     References Section 8 of BLUEPRINT-GUIDE.md for backlog management standards.
     IDs use the format: TYPE-NNN (e.g., FEAT-001, BUG-001, TASK-001, SPIKE-001). -->

| Field | Value |
|---|---|
| **Document ID** | PRJ-BACKLOG-001 |
| **Version** | 0.1.0 |
| **Owner** | System Architect |
| **Status** | Living Document |
| **Last Updated** | [PLACEHOLDER] |

---

## Backlog Summary

<!-- AGENT INSTRUCTION: Update these counts whenever the backlog changes.
     This provides a quick overview of backlog health. -->

### By Type

| Type | Count |
|---|---|
| Feature | [PLACEHOLDER] |
| Bug | [PLACEHOLDER] |
| Task | [PLACEHOLDER] |
| Spike | [PLACEHOLDER] |
| **Total** | **[PLACEHOLDER]** |

### By Priority

| Priority | Count |
|---|---|
| Critical | [PLACEHOLDER] |
| High | [PLACEHOLDER] |
| Medium | [PLACEHOLDER] |
| Low | [PLACEHOLDER] |

### By Status

| Status | Count |
|---|---|
| Backlog | [PLACEHOLDER] |
| Ready | [PLACEHOLDER] |
| In Progress | [PLACEHOLDER] |
| In Review | [PLACEHOLDER] |
| Done | [PLACEHOLDER] |
| Blocked | [PLACEHOLDER] |

---

## Master Backlog

<!-- AGENT INSTRUCTION: This is the single source of truth for all work items.
     ID format: FEAT-NNN, BUG-NNN, TASK-NNN, SPIKE-NNN.
     MoSCoW: Must, Should, Could, Won't.
     Status: backlog, ready, in-progress, in-review, done, blocked.
     Points: Fibonacci (1, 2, 3, 5, 8, 13, 21). -->

| ID | Type | Module | Title | Priority | MoSCoW | Status | Iteration | Assigned | Points |
|---|---|---|---|---|---|---|---|---|---|
| FEAT-001 | Feature | auth | User registration with email/password | Critical | Must | done | ITER-001 | VM-3a | 5 |
| FEAT-002 | Feature | auth | JWT-based authentication (access + refresh tokens) | Critical | Must | done | ITER-001 | VM-3a | 8 |
| FEAT-003 | Feature | auth | Social login (Google OAuth 2.0) | High | Should | ready | ITER-002 | VM-3a | 5 |
| FEAT-004 | Feature | user-profile | User profile CRUD operations | High | Must | in-progress | ITER-002 | VM-3b | 5 |
| FEAT-005 | Feature | notifications | Real-time notification system (WebSocket) | Medium | Should | backlog | — | — | 13 |
| BUG-001 | Bug | auth | Token refresh race condition under concurrent requests | High | Must | in-progress | ITER-002 | VM-3a | 3 |
| TASK-001 | Task | infrastructure | Set up CI/CD pipeline (GitHub Actions) | Critical | Must | done | ITER-001 | VM-5 | 8 |
| TASK-002 | Task | infrastructure | Configure monitoring dashboards (Grafana) | High | Must | in-review | ITER-002 | VM-5 | 5 |
| SPIKE-001 | Spike | notifications | Evaluate WebSocket vs. SSE for real-time notifications | Medium | Should | done | ITER-001 | VM-3b | 3 |
| FEAT-006 | Feature | payments | Payment integration (Stripe) | High | Should | backlog | — | — | 13 |

<!-- AGENT INSTRUCTION: Add new items at the bottom. Keep IDs sequential within each type.
     Every item MUST have: ID, Type, Module, Title, Priority, MoSCoW, Status.
     Iteration, Assigned, and Points should be filled when the item is groomed and scheduled. -->

---

## Backlog Health Metrics

<!-- AGENT INSTRUCTION: Review these metrics weekly to maintain backlog quality. -->

| Metric | Count | Target | Status |
|---|---|---|---|
| Items without acceptance criteria | [PLACEHOLDER] | 0 | [PLACEHOLDER] |
| Items without estimates (points) | [PLACEHOLDER] | 0 for items in Ready/In Progress | [PLACEHOLDER] |
| Stale items (no update in 30+ days) | [PLACEHOLDER] | < 5 | [PLACEHOLDER] |
| Blocked items | [PLACEHOLDER] | 0 | [PLACEHOLDER] |
| Items in progress > 2 iterations | [PLACEHOLDER] | 0 | [PLACEHOLDER] |

<!-- AGENT INSTRUCTION: If any metric exceeds its target, the System Architect should triage
     and resolve during the next backlog grooming session. -->
