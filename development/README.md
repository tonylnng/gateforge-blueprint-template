# Development Directory

<!-- AGENT INSTRUCTION: This README provides an overview of the development/ directory.
     Developer agents (VM-3) produce module documentation.
     The System Architect maintains coding standards and reviews all development docs. -->

## Purpose

The `development/` directory contains coding standards, conventions, and per-module technical documentation for the GateForge platform. These documents ensure consistent code quality across all developer agents and provide a reference for module interfaces, ownership, and dependencies.

## Directory Contents

| File / Folder | Description |
|---|---|
| `coding-standards.md` | Quick-reference coding standards for TypeScript, React, NestJS — naming conventions, file structure, Git workflow, code review checklist |
| `modules/` | Per-module technical documentation — API endpoints, database tables, events, configuration, and change logs |

## Ownership

| Role | Responsibility |
|---|---|
| **Developers (VM-3)** | Produce and maintain module documentation in `modules/`. Each developer agent owns specific modules and keeps docs in sync with implementation |
| **System Architect** | Maintains `coding-standards.md`. Reviews all development documents for consistency with architecture decisions |

## Workflow

1. **Coding Standards**: Before writing any code, developer agents reference `coding-standards.md` for conventions. The full development guide is in `DEVELOPMENT-GUIDE.md` at the repository root.
2. **Module Documentation**: When a new module is created, the owning developer creates a `modules/<module-name>.md` file using the template in `modules/README.md`. This documentation is updated with every significant change to the module.
3. **Code Review**: All PRs are reviewed against the code review checklist in `coding-standards.md`. Reviewers verify that module documentation is updated alongside code changes.

## Cross-References

- **[DEVELOPMENT-GUIDE.md](../DEVELOPMENT-GUIDE.md)** — Full development guide with detailed standards, patterns, and best practices
- **[architecture/](../architecture/)** — Technical architecture, data model, and API specifications
- **[qa/](../qa/)** — Test plans and test cases that validate module behavior
- **[project/backlog.md](../project/backlog.md)** — Work items assigned to developer agents
