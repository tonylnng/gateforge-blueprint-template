<!--
  AGENT INSTRUCTION: This template is mandatory for every PR. The Admin Portal
  validation (project/admin-portal-validation.md §3.7) checks that:
    1. The Pre-Flight Acknowledgement block is filled in.
    2. The 'Expected Version Bump' radio matches what the auto-bump workflow
       computes from the commit messages in this PR.
    3. Every modified document has a Revision History row for the new version.

  Do not delete sections. Tick the boxes that apply.
-->

## Summary

[1-3 sentence description of what this PR changes and why.]

---

## Pre-Flight Acknowledgement (mandatory)

I, the agent opening this PR, confirm that I read the documents listed below
**before** producing the changes in this PR. The version of each document I
read is recorded next to its name.

- **Role:** [ ] Architect · [ ] Designer · [ ] Developer · [ ] QC · [ ] Operator
- **Task:** [Short description of the task this PR completes]
- **Docs read (with version at time of reading):**
  - [ ] `VERSIONING.md` v1.0
  - [ ] `<role>/AGENTS.md` v____
  - [ ] [Add every other doc you consulted, with version]
- **Mandatory gates honored for my role:**
  - [ ] [Role-specific gate 1 — see your AGENTS.md §"Mandatory Gates"]
  - [ ] [Role-specific gate 2]
  - [ ] [Role-specific gate 3]

> If any box above is unchecked, the Admin Portal validation will mark this PR
> `validation: red` and block merge.

---

## Change Type & Expected Version Bump

Tick exactly **one** primary change type:

- [ ] **feat** — new feature → expect **MINOR** bump
- [ ] **fix** — bug fix → expect **PATCH** bump
- [ ] **refactor** — no functional change → expect **PATCH** bump
- [ ] **test** — test artifacts only → expect **PATCH** bump
- [ ] **deploy** — deployment / runbook change → expect **PATCH** bump
- [ ] **docs** — documentation only → expect **PATCH** bump
- [ ] **chore** — housekeeping → expect **PATCH** bump

If this PR mixes `feat` + `fix` commits → expect **MINOR** bump (PATCH resets to 0).

**Major bump?** Only Tony NG may request a MAJOR bump, and only by adding the
trailer `Version-Bump: major` to the final commit. Do NOT tick this section
yourself unless instructed.

- Current version (from `VERSION`): `____`
- Expected new version after this push: `____`

---

## Documents Modified

For every Markdown document changed in this PR, confirm:

| File | Version Bumped | Revision History Row Added |
|------|----------------|----------------------------|
| [PLACEHOLDER — path/to/file.md] | [ ] | [ ] |
| [PLACEHOLDER] | [ ] | [ ] |

---

## Traceability

Link the artifacts this change relates to (use `—` if not applicable):

- User Stories: `US-___, US-___`
- Functional Requirements: `FR-___-___`
- Test Cases: `TC-___-___-___`
- Defects fixed: `DEF-___, DEF-___`
- Incidents addressed: `INC-___`
- ADRs invoked: `ADR-___`

---

## Verification

- [ ] CI checks pass locally
- [ ] No secrets / PHI / PII added (see `project/admin-portal-validation.md` §5.2)
- [ ] If this PR will deploy, the deployment runbook pre-flight checklist has been completed
- [ ] If this PR closes defects, those defects link to this PR's eventual release tag

---

## Reviewer Notes

[Anything the reviewer should focus on. Anything explicitly out of scope.]
