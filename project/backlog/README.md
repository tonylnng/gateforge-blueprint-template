# Module-Level Backlogs

<!-- AGENT INSTRUCTION: This directory contains per-module backlogs that provide a detailed
     breakdown of bugs and enhancements for each module.
     These complement the master backlog (project/backlog.md) with module-specific detail.
     Format follows Section 8.4.6 of BLUEPRINT-GUIDE.md. -->

## File Naming Convention

```
<module-name>.md
```

Examples: `auth.md`, `user-profile.md`, `notifications.md`, `payments.md`

<!-- AGENT INSTRUCTION: Module name should match the module name used in the master backlog. -->

## Structure

Each module-level backlog contains four sections:
1. **Open Bugs** — Active bugs to be fixed
2. **Closed Bugs** — Resolved bugs (for historical reference)
3. **Open Enhancements** — Planned improvements and features
4. **Completed Enhancements** — Finished improvements (for historical reference)

---

## Module Backlog Template

<!-- AGENT INSTRUCTION: Copy the entire template below into a new <module-name>.md file. -->

```markdown
# Module Backlog: [PLACEHOLDER — Module Name]

<!-- AGENT INSTRUCTION: This is the detailed backlog for the [PLACEHOLDER] module.
     Keep in sync with the master backlog (project/backlog.md).
     The owning developer agent maintains this file. -->

| Field | Value |
|---|---|
| **Module** | [PLACEHOLDER] |
| **Owner** | [PLACEHOLDER — e.g., VM-3a] |
| **Last Updated** | [PLACEHOLDER] |

---

## Open Bugs

| ID | Title | Priority | Severity | Status | Reported | Assigned | Iteration |
|---|---|---|---|---|---|---|---|
| BUG-XXX | [PLACEHOLDER] | [PLACEHOLDER] | P0/P1/P2/P3 | open / investigating / in-progress | YYYY-MM-DD | [PLACEHOLDER] | [PLACEHOLDER] |

<!-- AGENT INSTRUCTION: Move bugs to "Closed Bugs" when resolved. Include resolution notes. -->

---

## Closed Bugs

| ID | Title | Severity | Resolution | Resolved Date | Resolved By | PR Link |
|---|---|---|---|---|---|---|
| BUG-XXX | [PLACEHOLDER] | P0/P1/P2/P3 | fixed / won't-fix / duplicate / by-design | YYYY-MM-DD | [PLACEHOLDER] | [PLACEHOLDER] |

---

## Open Enhancements

| ID | Title | Priority | MoSCoW | Status | Assigned | Iteration | Points |
|---|---|---|---|---|---|---|---|
| FEAT-XXX | [PLACEHOLDER] | [PLACEHOLDER] | Must/Should/Could/Won't | backlog / ready / in-progress | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |

<!-- AGENT INSTRUCTION: Move enhancements to "Completed Enhancements" when done. -->

---

## Completed Enhancements

| ID | Title | Completed Date | Developer | PR Link | Notes |
|---|---|---|---|---|---|
| FEAT-XXX | [PLACEHOLDER] | YYYY-MM-DD | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] |
```
