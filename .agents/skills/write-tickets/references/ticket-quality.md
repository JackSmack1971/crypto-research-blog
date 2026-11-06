# Ticket-authoring decisions

Open when drafting or revising a requirements/evaluation pair.

## Granularity

A feature ticket yields a user-observable or independently checkable result. Split only when the pieces have separate value/verification or legitimately unblock other work. A button plus its only useful save behavior belongs together; login and a separate dashboard belong apart. Do not create a ticket per source file or generic phase ("frontend", "backend", "QA") unless that phase independently satisfies a testable capability. Enabler tickets must have a verifiable technical contract and a dependent deliverable.

## Requirements (`rd.md`)

- Use the exact marker `- **R-01**: ...`, incrementing numbers locally per ticket. Each row states a **condition/action/result** in language an implementer can follow without guessing consequential choices. Use stable identifiers for revisions; if a requirement is deleted, update its eval mapping deliberately.
- Include authentic repository context: existing routing/data models, supported client/server boundaries, build/test tooling, security controls, generated outputs and architecture constraints. If unavailable, say **not yet verified** rather than inventing.
- Describe expected inputs, outputs, state transitions, visible errors, permissions, persistence/rollback, and accessibility when they affect the feature. Prefer bounded examples over vague qualifiers ("fast", "user-friendly", "properly"). Do not assert universal numeric targets unless supplied or authoritative.
- Record exclusions, upstream dependencies and any conflicts with existing architecture. Avoid locking technology choices not required by existing architecture or the user.
- Mark important unresolved product decisions in both the ticket's assumptions section and `board.json` `open_decisions`; they prevent ready promotion.

## Verification (`eval.md`)

- Make exactly one Markdown table data row for each requirement identifier. Multiple substeps may live within the row's Action/Expected cells, but the expected result must distinguish PASS from FAIL. Put extra integration and negative checks below the table.
- Setup must explain what state to create or locate; action must identify a usable command or interaction **only when verified**, otherwise a test mechanism that still needs confirmation; result must identify a concrete observed value, state, DOM/accessibility behavior, error class, or persisted change.
- For UI work: if a browser test facility is available, specify target route, device/viewport, interaction sequence, state change, and at least one keyboard/accessible-name or focus check when relevant. Include responsive/overflow behavior for layout changes. Tool unavailable? State that browser verification is pending; never replace it with unsupported PASS.
- For server/data/security work: specify realistic negative paths and authorization boundaries. Do not use real production data, secrets, remote writes, or deployments as a default acceptance-test fixture. Prefer isolated fixtures and existing repo tooling.
- Distinguish evidence the implementer must gather from evidence already gathered. Writing `eval.md` does not execute it.

## Readiness review

Before proposing approval: outcome is useful and bounded; each requirement is noncontradictory; all constraints have provenance; 1:1 evaluation coverage is complete; setup/action/result are falsifiable; dependencies exist and are acyclic; risks and unknown decisions are visible; the user has enough information to approve or request targeted edits.
