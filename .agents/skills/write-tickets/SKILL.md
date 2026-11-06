---
name: write-tickets
description: Turn feature requests into build-ready specification tickets, each with rd.md requirements, eval.md pass/fail checks, and a dependency-aware approval board. Use when asked to write tickets, scope features, define acceptance criteria, or split a feature list into work items before implementation. Do not use to implement features, publish issues to external trackers, or produce non-implementation roadmaps.
---

# Write Tickets

Turn requested features into independently verifiable work items. Each ticket has **exactly two authored files**: `rd.md` (what and why) and `eval.md` (how to prove it). A project-level board manages dependencies, review, and potential concurrency. **Writing a ticket is not approval to implement it.**

## 1. Reconcile the repository and split by feature

1. Read applicable `AGENTS.md` / `AGENTS.override.md`, planning authority, existing tickets, relevant code/tests and `git status --short`. Do not edit unrelated files or overwrite an existing ticket scheme. Existing repository conventions outrank this skill's defaults unless they conflict with user instructions.
2. Identify the user's outcomes and split at the **smallest cohesive, independently demonstrable value**. Combine a UI control with required persistence if neither is useful alone. Split independent login and dashboard capabilities. An enabling infrastructure slice may be a ticket only when independently verifiable and necessary; label it an enabler.
3. Record dependencies as a directed acyclic graph; do not confuse prerequisites with shared-file conflicts. Identify likely touched components and shared resources; mark unknown concurrency **not assessed**, never silently parallel-safe.
4. Present the split, key assumptions, dependencies, and decisions that affect scope. Prefer source-backed defaults to needless questions, but do not invent business/security/compatibility requirements when an authoritative decision is missing; leave that ticket in draft and state what decision is needed.

## 2. Author each requirements/evaluation pair

Use `assets/rd.md` and `assets/eval.md` as structures, replacing template guidance with actual specifics. Read `references/ticket-quality.md` **when writing or revising tickets** for quality and browser-check criteria.

- `rd.md`: user-visible outcome, bounded behavior, numbered atomic requirements (`**R-01**:` etc.), data/error/accessibility/security/compatibility considerations **only when relevant**, dependencies, explicit exclusions, assumptions and unresolved decisions. Requirements must describe externally observable results, not prescribe speculative implementation.
- `eval.md`: exactly one coverage row per `R-nn`, with a **reproducible setup, action/tool, and unambiguous expected observation**; additional integration/negative checks when needed. When testing UI, include browser interactions, viewport and accessible behavior when tools exist; do not invent an `agent-browser` binary or claim browser checks ran while merely writing tickets.
- Never silently mark uncertain requirements as proven or invent commands, fixtures, test IDs, environments, API responses, performance thresholds, or credentials. An unknown prerequisite may be documented as unresolved, with a concrete resolution route. An uncheckable assertion is a defect to fix, not a PASS.

## 3. Create a reviewable board (not an execution plan)

1. Choose the repository's existing ticket location/format if present. Otherwise use `tickets/`, allocate the next unused monotonically increasing ID, and create `tickets/NNN-short-slug/{rd.md,eval.md}`. Do not renumber existing tickets; preserve existing files. For the default format copy `assets/board.json` to `tickets/board.json` on first use, then append entries using `references/board-contract.md`. Do not convert an established tracker without authorization.
2. All newly authored or materially revised tickets have `status: "draft"`, `approval: null`. Only after the user has reviewed the *specific current content* and explicitly approved it may the ticket become `ready`. Read `references/board-contract.md` **before approving, changing status, or planning concurrent implementation**.
3. Run `python <skill-root>/scripts/ticket_board.py validate --root tickets`; fix structural or traceability errors. Run `python <skill-root>/scripts/ticket_board.py render --root tickets --write`, then `python <skill-root>/scripts/ticket_board.py validate --root tickets --check-rendered`. On Windows, use the available Python 3 launcher and actual skill path. These commands apply only to the **default** board format; inspect established repository tooling otherwise.
4. The generated `tickets/BOARD.md` distinguishes **eligible now**, **waiting on dependencies**, **draft/unapproved**, and **already active or done**. Suggested concurrent groups are only *candidates*: dispatch still requires isolated write ownership, resource reconciliation, tool/permission checks, and separate authorization for implementation.

## 4. Independently inspect and hand off

Check that each requested outcome maps to at least one ticket; each `R-nn` has one actionable evaluation row; no ticket duplicate or cycle exists; ordering/statuses match the board; no unknown consequential decision is presented as settled; and the final diff contains **only intended planning artifacts**. The validator checks structure and hashes, **not semantic quality or whether approval really occurred**. Do not change implementation files, open external issues, or execute acceptance tests without a separate request.

Report the ticket IDs and paths, decomposition and dependency choices, current draft/ready status, proposed concurrency with limitations, exact validation commands/results, unresolved decisions, and the approval needed. Stop when the ticket set is reviewed for structural consistency; do not treat drafts as actionable or automatically start workers.

## Failures and stopping rules

- **Missing code, conventions, or authority:** inspect available sources; use a conservative draft with explicitly bounded unknowns rather than fabricate facts. If the repository is inaccessible, write a provisional proposal in the response; do not claim repository artifacts exist.
- **Existing changes/colliding numbers:** inspect and preserve them; choose an unused ID or stop if ownership is ambiguous. Do not overwrite edited existing ticket documents or custom boards.
- **Incomplete checks or unavailable Python:** manually inspect every pair/board, report exactly what was unverified; never claim validator PASS.
- **Dependency cycle, orphan row, stale approval hash, blocked/ambiguous concurrency:** correct the source or restore draft and request reapproval; do not waive a failed check.
- **Authorization:** no issue creation, remote writes, deployment, or code execution follows from a ticket-writing request. Skills cannot override host sandbox or permissions.
