# Goldfish Annotated Review Report

**Status:** Halted after Round 3 per user direction; all findings resolved or accepted; no open items
**Target:** `docs/designs/ux-audit/article-accessibility-and-related-notes.md` (Rounds 1–3, full file)
**GoldfishContext:** exactly the paths supplied by the user
**Reviewer status:** implementation_readiness and codebase_details — completed all three rounds

## Prioritized Findings & AI Suggestions

### Issue 1 [implementation_readiness] — Severity: Major

* **Affected Scope:** Lines 19–23, 89–92, 227–229 (Contrast corrections)
* **Discrepancy Description:** The plan leaves exact color choices and the state-to-assertion mapping to the implementer. It calls for the “smallest” palette-family adjustment and says replacement values are “verify during implementation,” without defining how to select the value or which route, viewport, and color-scheme states each assertion covers.
* **Rationale:** Measurements can properly determine whether and what to change, but Slice 2 needs a specified evidence-to-approval checkpoint so implementation does not silently make editorial color decisions.
* ***AI Suggestion:*** PROPOSE FIX
* ***Justification:*** Record the post-measurement selector/property, approved old/new values, backgrounds and ratios for each reproduced state in the evidence/design record; explicitly block Slice 2 until that state matrix and assertion scope are approved.
* ***Proposed Edit:*** Add a Slice 1 closure artifact schema and a Slice 2 entry gate requiring approval of the reproduced-state matrix and chosen values before edits.

### Issue 2 [implementation_readiness] — Severity: Major

* **Affected Scope:** Lines 74, 81, 221–223 (Slice 1 evidence script)
* **Discrepancy Description:** The first slice depends on direct TypeScript execution support in the local Node runtime, which is currently unknown. The plan forbids adding a runtime dependency but does not define a supported invocation or fallback.
* **Rationale:** If the invocation is unsupported, the first evidence step stalls or requires an unplanned implementation choice.
* ***AI Suggestion:*** PROPOSE FIX
* ***Justification:*** Specify a tested invocation compatible with the repository’s Node/browser tooling, or name a no-dependency JavaScript fallback and include it in the exact file boundary.
* ***Proposed Edit:*** Replace “verify during implementation” on TypeScript execution with a deterministic runtime/invocation requirement and fallback, including any corresponding file path.

### Issue 3 [implementation_readiness] — Severity: Major

* **Affected Scope:** Lines 121, 199 (Slice 4 dry-run gate)
* **Discrepancy Description:** “Looks editorially sensible” has no defined dry-run artifact, review procedure, decision owner response, or acceptance criterion.
* **Rationale:** An implementer cannot determine whether the gate passed. The ranking review should be an explicit external prerequisite, not an ambiguous coding-time decision.
* ***AI Suggestion:*** PROPOSE FIX
* ***Justification:*** Define a recorded dry-run and a concrete approval checkpoint before Slice 4 begins.
* ***Proposed Edit:*** Specify where per-article candidates/scores/order are recorded, who records the decision, and that Slice 4 starts only after Bret explicitly approves the artifact; otherwise it remains deferred.

### Issue 4 [implementation_readiness] — Severity: Major

* **Affected Scope:** Lines 125, 248–250 (ranking and rendering helpers)
* **Discrepancy Description:** The ranking helper’s return contract and the generated markup schema are incomplete. “Returns the selected candidates and variant” does not define structure or variant values; positive-score heading text, list/link/date markup, and relative URL construction are also unspecified.
* **Rationale:** Tests and implementation could choose incompatible contracts despite following the stated algorithm.
* ***AI Suggestion:*** PROPOSE FIX
* ***Justification:*** State a small stable return shape and rendering contract that can be shared by generator and tests.
* ***Proposed Edit:*** Define the helper return fields and allowed variant values; specify headings for positive-match and latest fallback, the single-note behavior, markup/link/date fields, and a relative article-href rule compatible with both deployment paths.

### Issue 5 [implementation_readiness] — Severity: Major

* **Affected Scope:** Lines 127, 136–144, 262–269 (screenshot normalization)
* **Discrepancy Description:** Screenshot normalization is described as a fixed slug set and stable heading, but the slug set and exact normalization behavior are not specified. The reference to `homepageBaselineSlugs` does not establish which related-note entries or text are fixed.
* **Rationale:** Snapshot stability is a key requirement; differing choices for links, dates, heading, and empty states can still make snapshots churn or hide presentation regressions.
* ***AI Suggestion:*** PROPOSE FIX
* ***Justification:*** Define a deterministic normalized fixture for the screenshot targets while keeping real catalog output under separate functional checks.
* ***Proposed Edit:*** Name the exact fixed slugs and specify which subtree fields are normalized (heading, link text, href, date and empty state), with the normalization isolated to screenshot setup.

### Issue 6 [implementation_readiness] — Severity: Major

* **Affected Scope:** Lines 91, 98, 109, 115, 229, 235–237, 277–279 (browser assertions)
* **Discrepancy Description:** The required Playwright tests are named but key procedures are not defined: the keyboard sequence and scroll-delta/end-state assertion, focus-visible check, and behavior for non-reproduced regions. The contrast assertion also lacks a precise state matrix.
* **Rationale:** Different implementations may pass materially different behavior while using the same test titles.
* ***AI Suggestion:*** PROPOSE FIX
* ***Justification:*** Translate “keyboard-operable,” “visibly focused,” and “contrast passes” into observable assertions tied to the Slice 1 evidence.
* ***Proposed Edit:*** Specify keyboard input and expected scroll movement, focus and accessible-name/role assertions, and how tests include only reproduced states while explicitly checking the documented no-edit result for non-reproduced findings.

## Reviewer Summary

* Round 1 implementation_readiness: completed — 6 Major findings; all six applied per user specifics.
* Round 1 codebase_details: completed — zero findings.

## Round 2 Findings

### Issue 7 [implementation_readiness] — Severity: Major

* **Affected Scope:** Current document lines 243–245 (contrast approval matrix)
* **Discrepancy Description:** The evidence report specifies matrix columns and says Bret approves proposed values, but it does not define a per-row approval marker or how Playwright reads the approved rows. “Assert exactly the approved rows” leaves the row format and parser behavior to the implementer.
* **Rationale:** The implementation cannot reliably select the approved finding/route/viewport/color-scheme/selector/property rows without an explicit machine-readable convention.
* ***AI Suggestion:*** PROPOSE FIX
* ***Justification:*** A per-row status and date, plus a defined parser for the Markdown matrix, makes the approval and test scope reproducible.
* ***Proposed Edit:*** Add `Approval` values `pending|approved|rejected` and `Approval date (YYYY-MM-DD)` columns to the matrix. Bret marks each proposed row `approved` with a date or leaves it pending/rejects it. State that `tests/visual.spec.ts` reads only rows whose approval field is exactly `approved`, validates each row schema, and asserts exactly one test per approved tuple; fail if the approved set is empty when a reproduced state exists or if an approved row is malformed/duplicated.

### Issue 8 [codebase_details] — Severity: Major

* **Affected Scope:** Current document lines 91, 139, and 274–282 (shared and related-region CSS)
* **Discrepancy Description:** The styling scope still leaves exact layout choices to the implementer: Slice 2 permits choosing a passing foreground, and Slice 4b says to use tokens and provide responsive layout without specifying the region's box spacing, type scale, colors, or responsive behavior.
* **Rationale:** The implementation-readiness standard requires preselected design choices. Existing shared CSS provides concrete reusable values and a container pattern, so these can be stated without inventing a new system.
* ***AI Suggestion:*** PROPOSE FIX
* ***Justification:*** Point to existing `--cr-*` tokens and the `#cr-sitebar .cr-sitebar-inner` container pattern for bounded dimensions, and define the related region’s spacing, typography, and mobile stacking before Slice 4b. Keep contrast colors gated to exact measured/approved rows.
* ***Proposed Edit:*** Specify the exact tokens/declarations or direct reuse of existing site-bar inner max-width, centered margins, horizontal padding, gap, and break behavior for `#cr-related`; state fixed heading/body typography and background/foreground tokens. Slice 2's foreground value remains per-row, explicitly approved in the state matrix before implementation.

## Round 2 Reviewer Summary

* implementation_readiness: completed — 1 new Major finding.
* codebase_details: completed — 1 new Major finding; zero current-state inaccuracies.

## Round 2 Resolution

* **Issue 7 — PARTIAL:** Added `Approval` (`pending|approved|rejected`) and `Approval date` columns to the evidence matrix. **CONTESTED, settled decision:** tests will not read Markdown. The document now requires a literal `APPROVED_CONTRAST_STATES` array copied from approved rows in the same PR, with PR review as the consistency check. This deliberate decision is documented in the target and is settled for later rounds.
* **Issue 8 — ACCEPTED, constrained to existing values:** The target now names existing container, home entry title/link/date/spacing selectors, copies their CSS values, names the `--cr-*` tokens, mandates one column/no horizontal scroll at 390 px, and prohibits new values/tokens.

## Round 3 Findings

### Issue 9 [implementation_readiness] — Severity: Major

* **Affected Scope:** Current document lines 20, 77, 93, 141, 247 (contrast thresholds and state matrix)
* **Discrepancy Description:** The document names 4.5:1 for normal text and 3:1 for large text, but the state matrix has no threshold column or rule that determines which threshold applies to a row. The array requires `minRatio`, so its value cannot be copied directly from the approved matrix as currently specified.
* **Rationale:** A row-level threshold prevents an implementer from classifying text size/weight or deriving a different minimum when creating `APPROVED_CONTRAST_STATES`.
* ***AI Suggestion:*** PROPOSE FIX
* ***Justification:*** Record the applicable minimum alongside each measured state and define the large-text criterion in terms of rendered CSS size and weight.
* ***Proposed Edit:*** Add `Minimum ratio` to the evidence matrix; use 4.5:1 for normal text and 3:1 only for WCAG large text (at least 24 CSS px regular or 18.66 CSS px bold). Copy this field to the array's `minRatio`.

### Issue 10 [codebase_details] — Severity: Major

* **Affected Scope:** Current document line 321 (per-slice delivery order)
* **Discrepancy Description:** The delivery plan says to verify branch naming and whether to use five separate PRs or a stacked sequence during implementation, leaving both choices open.
* **Rationale:** The implementation-readiness standard expects the plan to settle execution choices before work begins.
* ***AI Suggestion:*** PROPOSE FIX
* ***Justification:*** State a branch and PR strategy in the document so implementation can follow a predetermined sequence; this does not authorize the external GitHub actions.
* ***Proposed Edit:*** Specify one topic branch named `ux/article-accessibility-related-notes` and one PR, with the five slices delivered as ordered commits. Hold Slice 2 edits until its row-level contrast approval and Slice 4b work until the recorded Slice 4 gate is approved. The PR/deploy/merge actions remain subject to separate authorization.

## Round 3 Reviewer Summary

* implementation_readiness: completed — 1 new Major finding.
* codebase_details: completed — 1 new Major finding.

## Round 3 Resolution and Halt

* **Issue 9 — ACCEPTED:** Added a `Minimum ratio` matrix column. Normal text uses 4.5; WCAG large text uses 3.0 only at rendered font-size ≥ 24 CSS px, or ≥ 18.66 CSS px with rendered font-weight ≥ 700. The approved array copies this value to `minRatio`.
* **Issue 10 — ACCEPTED strategy; REJECTED single-PR proposal:** The target specifies one PR per slice, each branched from up-to-date `main` after the preceding slice merges, using `ux/s1-remeasure`, `ux/s2-contrast`, `ux/s3-scroll-regions`, `ux/s4a-related-ranking`, and `ux/s4b-related-nav`. It records the approval-gate, independent Phase 1, single-revert rollback, and Netlify-on-merge rationale, plus Bret's separate authorization requirement for PR creation, merge, and deployment.
* The user directed the loop to halt after these edits. The target status is **Approved for Slice 1**; this does not approve later slices or external publishing actions.
