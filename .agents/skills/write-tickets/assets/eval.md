# Evaluation: <Feature title>

**Ticket:** <NNN-feature-slug>

## Verification prerequisites

State the environment, setup, fixtures, access, and available test mechanisms needed to make observations repeatable. Do not fabricate repo commands or test credentials.

## Requirement checks

| Requirement | Setup / initial state | Action and tool | Expected observable result (PASS; otherwise FAIL) |
|---|---|---|---|
| R-01 | Preconditions and data | Exact steps/tool/command or browser flow | Specific observable expected state |
| R-02 | Preconditions and data | Exact steps/tool/command or browser flow | Specific observable expected state |

## Browser checks (for browser-delivered UI only)

For every relevant UI requirement: record the verified route, viewport, starting state, user interaction, observable DOM/visual change, keyboard/accessibility behavior, and required evidence. Prefer existing repo browser tooling; if unavailable, explicitly mark the browser check **not run / pending**, never PASS. Remove this section for non-UI tickets.

## Cross-feature and negative-path checks

Include only checks that reveal credible integration, authorization, failure, and boundary defects not already covered in the table.

## Evidence and limitations

What evidence must be retained (test output, browser observation, screenshot, logs without secrets), what still requires tools or fixture design, and what would make a result inconclusive. This is a **specification of future checks**, not a claim they have run.
