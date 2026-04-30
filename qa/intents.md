# AI Explorer Intents — Lane B

<!--
  AGENT INSTRUCTIONS:
  This file feeds Lane B (AI exploratory). The QC-Explorer agent reads each
  block and tries to drive a real signed-in browser session through the
  described journey. Failures get filed as defects; new edge cases get
  proposed as additions to Lane A via PR-reviewed `qa/ai-explorer/generated/`.

  Format: one fenced block per critical user journey, identified by `id`
  matching the CUJ table in `ui-auto-test-plan.md`.

  Each block contains:
    - id           CUJ-NNN identifier
    - goal         plain-English what the user is trying to do
    - preconditions seed data, signed-in role, feature flags
    - success_criteria  measurable outcomes (URL, DOM state, API call, message)
    - failure_modes  known failure modes that must surface as defects
    - data_testids  any specific selectors the agent should rely on
    - notes        free-form, including reduced-motion / a11y considerations
-->

---

```yaml
id: CUJ-001
goal: |
  [PLACEHOLDER — e.g. A new visitor signs up with email + password,
  receives a verification email, clicks the link, and lands on the
  authenticated dashboard.]
preconditions:
  - SUT URL: ${SUT_URL}
  - Email inbox accessible via Mailpit on http://mailpit:8025
  - No prior account with the test email
success_criteria:
  - Final URL matches /dashboard
  - DOM contains [data-testid="dashboard-welcome-banner"]
  - Backend API GET /me returns { verified: true }
failure_modes:
  - Verification email never arrives within 60 s
  - Verification link 404s
  - Dashboard banner missing data-testid
  - Sign-up form rejects valid emails
data_testids:
  - auth-signup-email
  - auth-signup-password
  - auth-signup-submit
  - dashboard-welcome-banner
notes:
  - Run with reduced motion enabled.
  - The agent must wait for [data-testid="page-ready"] before asserting.
```

---

```yaml
id: CUJ-002
goal: |
  [PLACEHOLDER]
preconditions:
  - [PLACEHOLDER]
success_criteria:
  - [PLACEHOLDER]
failure_modes:
  - [PLACEHOLDER]
data_testids:
  - [PLACEHOLDER]
notes:
  - [PLACEHOLDER]
```

---

<!-- Add one block per CUJ. Aim for 5–10 blocks at first seed; expand as the product grows. -->
