# Article Accessibility and Related Notes

* **Author:** Bret
* **Status:** Proposed
* **Date:** 2026-11-05

## Overview

Improve the experience of readers who arrive directly at an Independent Market Notes article, especially on a phone: correct the reported contrast and keyboard-access problems, then give readers a clear path to related research. The first phase makes finding-specific accessibility corrections in generated 404 chrome and the named essay sources. Only after those corrections pass their checks does a second phase add a generated related-notes navigation area after the essay. (UX-01–06, ED-01, ED-07)

## The Problem

The supplied audit reports a low-contrast 404 kicker (UX-01), two low-contrast labels in the token-unlock article (UX-02–03), and three horizontally scrollable regions that were not keyboard-focusable (UX-04–06). The editorial review also observed limited paths between articles and from an article back to the wider library (ED-01, ED-07). The reported measurements have not been verified against the current build. Re-measure UX-01–06 first; close any finding that does not reproduce as “not reproduced,” record its evidence, and make no edit for it. Record newly found issues but keep them out of this scope unless Bret approves them. (UX-01–06, ED-01, ED-07)

Today, `build.py` inserts a site bar into each standalone essay, while each source essay controls its own typography, colors, layout, tables, and charts. This proposal preserves that boundary. It allows only the exact declaration changes needed for UX-02/03 and markup-only accessibility attributes for UX-04–06; it does not introduce a general article style layer. A later generated navigation area uses the existing catalog to offer a reproducible path to other notes without changing essay prose or DOM. (UX-02–06, ED-01)

## Goals

* **Reproduce before correcting:** re-measure UX-01–06 against the current build, recording rendered contrast, affected element and selector, and scroll-container behavior. Mark a finding that does not reproduce “not reproduced” with evidence and make no edit for it. Record newly found issues without adding them to this scope unless Bret approves them. (UX-01–06)
* Correct reproduced UX-01–03 findings with the smallest palette-family color changes that meet WCAG contrast requirements in rendered context; record each finding's before/after ratio and require zero axe color-contrast nodes on the affected routes. (UX-01–03)
* Make the existing UX-04–06 scroll containers keyboard-focusable and named, preferring `aria-labelledby` to an existing table heading or caption and using `aria-label` only when neither exists; keep content signatures unchanged. (UX-04–06)
* After Phase 1 closes and a ranking dry-run against the current catalog looks editorially sensible, add a JavaScript-independent `#cr-related` region to every generated article, outside the essay DOM. When other articles exist, show one to three resolving, non-self links; use “Latest notes” when all scores are zero. If the catalog contains only the current article, omit the empty recommendation heading. Always include an “All notes” link, work with JavaScript disabled, and keep visual baselines stable when the catalog grows. Rank by `2 × shared assets + 1 × same topic + 1 × same research_type`, then newer date, then catalog order. (ED-01, ED-07)
* Keep article source prose and presentation intact outside the six finding-specific accessibility corrections, preserve relative links for both hosts, retain current fonts, tokens, screenshot sensitivity and standard-library-only build, and prevent routine catalog changes from churning the article visual baselines. (UX-01–06, ED-01)

## Non-Goals

* No general article style layer, visual redesign, changes to essay prose, typography, palette, layout, charts, or images beyond the specific UX-02/03 correction declarations. (UX-02–06)
* No archive scanning or excerpt hierarchy (ED-02), in-article contents navigation (ED-03), taxonomy-label redesign (ED-05), broader current-topic/search navigation (ED-07), or publication/data-age labels (ED-09). (ED-02, ED-03, ED-05, ED-07, ED-09)
* No image optimization based only on reported Lighthouse opportunities, new runtime dependencies, remote services, or publication/deployment work. (UX-07–08)

## Critical User Journeys

### CUJ 1: Read a shared article link accessibly

* **Given:** A reader opens an Independent Market Notes article directly, commonly on a mobile viewport.
* **When:** The page loads with or without JavaScript, and the reader encounters the reported contrast labels or horizontally scrollable tables.
* **Then:** The reader can read the visible labels at the applicable contrast threshold and can reach, focus, and scroll the affected table regions with a keyboard. Only findings reproduced against the current build receive edits. (UX-01–06)

### CUJ 2: Continue from an article to other notes

* **Given:** A reader reaches an article from a shared link.
* **When:** They reach the generated `#cr-related` navigation.
* **Then:** They see non-self links selected by the catalog ranking, or the honest “Latest notes” fallback when all candidate scores are zero, plus an “All notes” path. The links work without JavaScript. If the catalog contains only the current article, the empty recommendation heading is omitted. (ED-01, ED-07)

## Technical Plan (Architecture)

Deliver the work in four independent slices. The first slice establishes which reported conditions exist in the current build. No correction is made for a finding that does not reproduce; new findings are recorded but remain out of scope until Bret approves them. Slices 2 and 3 correct only reproduced UX-01–06 items. Slice 4 is gated on Phase 1 closure and a review of the ranking output against the current catalog. (UX-01–06, ED-01)

```text
Current generated pages
        |
        v
1. Re-measure UX-01–06 and record evidence
        |
        +-- finding not reproduced: close with evidence; no edit
        +-- new issue: record; wait for Bret's approval before expanding scope
        +-- reproduced findings
                |
                +--> 2. Correct UX-01–03 contrast
                +--> 3. Correct UX-04–06 scroll-region semantics
                              |
                     Phase 1 closure gate
                              |
                  ranking dry-run looks sensible
                              |
                              v
                  4. Generate #cr-related nav
```

### Slice 1: Reproduce and record UX-01–06

**Files and purpose**

* `docs/designs/ux-audit/evidence/scripts/remeasure.ts` — add a standalone Playwright script that opens the built pages from `dist/`. At 390, 768, and 1440 pixels, record UX-01–03 foreground, effective opaque background found by walking ancestors, computed font size/weight, actual element/selector, and contrast ratio. For UX-04–06, record each existing scroll wrapper, focusability, and horizontal keyboard-scroll behavior. Check essay dark-mode styles if present. This is an evidence script, not a Playwright test or production runtime file.
* `docs/designs/ux-audit/evidence/remeasure.md` — write the measured results, including reproduced/not-reproduced status and new issues. The design document summarizes those results; newly found issues remain outside scope unless Bret approves them.

**Signature impact:** None. This slice changes no essay source or generated page. No fixture refresh is allowed or needed. (UX-01–06)

**Visual targets and snapshots:** No screenshot baseline changes. The checks run at the specified viewports but collect evidence rather than establish new expected screenshots. No snapshot refresh command applies. (UX-01–06)

**Run and inspect:** Build with `python3 build.py`, serve only the generated `dist/` using `python3 -m http.server 4174 --bind 127.0.0.1 -d dist`, and run the evidence script against `http://127.0.0.1:4174`. The intended invocation is `node --experimental-strip-types docs/designs/ux-audit/evidence/scripts/remeasure.ts`; support for direct TypeScript execution in the implementation runtime is **verify during implementation**. Save results to `docs/designs/ux-audit/evidence/remeasure.md`, then summarize them here. Run the existing Python and Playwright suites as the per-slice delivery process requires, but add no `tests/visual.spec.ts` remeasurement tests. A finding that does not reproduce is recorded as “not reproduced” and proceeds to no edit. (UX-01–06)

**Rollback:** This slice adds only the local evidence script/report. If a measurement is invalid, correct or remove that measurement and rerun the script. Do not infer a defect or edit production files. Keep the recorded result and its limits in the design document. (UX-01–06)

### Slice 2: Correct reproduced contrast findings UX-01–03

**Files and purpose**

* `assets/design-system.css` — narrow the gold kicker declaration from the broad home-page selector to the dark masthead (`body.cr-home .mast .kicker`). This preserves the gold label on the dark homepage while allowing the 404 kicker to use the existing passing accent color. Confirm the actual current element/background before applying this selector correction. (UX-01)
* `content/token-unlock-liquidity-illusion-90-day-calendar.html` — change only the reproduced failing declaration or declarations for the kicker and topic label. Select the smallest foreground adjustment in the existing essay palette family that passes the measured contrast threshold; do not change prose, other declarations, or dark-mode styles unless the corresponding failing state reproduces. (UX-02–03)
* `tests/visual.spec.ts` — retain the rendered measurements at all three widths and assert the applicable ratio (4.5:1 normal text, 3:1 large text) plus zero axe color-contrast nodes on the affected routes. Do not weaken existing axe or screenshot checks. (UX-01–03)
* `docs/designs/ux-audit/article-accessibility-and-related-notes.md` — record each correction by finding ID, file, selector/property, old and new value, rendered background, font size/weight, and before/after ratio for each relevant color scheme and viewport. (UX-01–03)

**Signature impact:** CSS is skipped by the semantic signature extractor; visible text, headings, links, tables, and images remain unchanged. The content-signature fixture must remain identical. Do not run `scripts/refresh_fixtures.py`. (UX-02–03)

**Visual targets and snapshots:** `/404.html` and the token-unlock article have no approved screenshot. The home page is an existing target and must remain pixel-identical because the narrowed selector preserves the dark masthead color. No snapshot refresh is expected. If the reviewed home diff shows an intended visual correction, refresh only home with `npm run test:browser:update:home` (its package script uses `--grep "visual baseline › home @"`); otherwise keep its baseline unchanged. (UX-01–03)

**Tests:** Add the Slice 2 Playwright assertion listed in Detailed Implementation and run it with `npx playwright test tests/visual.spec.ts --grep "accessibility › UX-01–03 contrast passes for"`. Check at 390, 768, and 1440 on `/404.html` and the token-unlock route; require the measured threshold and zero axe color-contrast nodes for reproduced states. (UX-01–03)

**Rollback:** Revert only the 404 selector change or the specific essay color declarations that fail rendered contrast or alter unrelated presentation. Retain the measured baseline and failed result in the design document; leave fixtures unchanged. (UX-01–03)

### Slice 3: Correct reproduced scroll-region findings UX-04–06

**Files and purpose**

* `content/aero-at-0-68.html` — add `tabindex="0"`, `role="region"`, and an accessible name to the existing `.table-scroll` wrapper. Prefer `aria-labelledby` pointing to a relevant existing visible heading/caption; if that target lacks an ID, add only an ID attribute. (UX-04)
* `content/bitcoin-buying-imbalance.html` — apply the same attributes to the existing `.tablewrap` wrapper, using the same accessible-name precedence. (UX-05)
* `content/token-unlock-liquidity-illusion-90-day-calendar.html` — apply the same attributes to the existing `.scroll` wrapper, using the same accessible-name precedence. (UX-06)
* `tests/visual.spec.ts` — assert each reproduced region is named, keyboard-focusable, visibly focused, and horizontally scrollable; preserve the route-wide overflow and accessibility checks. (UX-04–06)

**Signature impact:** `tabindex`, `role`, `aria-label`, `aria-labelledby`, and an added heading/caption ID are generic attributes ignored by `tests/signatures.py`. No visible text, table cells, headings, CSS, or signature fixture should change. Do not refresh fixtures. (UX-04–06)

**Visual targets and snapshots:** The affected screenshot targets are `aero-at-0-68` (UX-04) and `bitcoin-buying-imbalance` (UX-05); the token-unlock article (UX-06) is not an approved screenshot target. These semantic attributes should not change the unfocused screenshot. Inspect target diffs; only if an intended visible change is confirmed, update one target at a time using `npx playwright test tests/visual.spec.ts --grep "visual baseline › aero-at-0-68 @" --update-snapshots` or `npx playwright test tests/visual.spec.ts --grep "visual baseline › bitcoin-buying-imbalance @" --update-snapshots`. Do not update token-unlock or unrelated snapshots. (UX-04–06)

**Tests:** Add the Slice 3 Playwright assertions listed in Detailed Implementation and run them with `npx playwright test tests/visual.spec.ts --grep "keyboard › UX-04–06 scroll regions operate with keyboard for"` and `npx playwright test tests/visual.spec.ts --grep "accessibility › UX-04–06 scroll regions have accessible names for"`. Verify focus and keyboard scroll at 390, 768, and 1440, and run the accessible-name assertion on the same routes. (UX-04–06)

**Rollback:** Remove only the attributes/IDs added to the reported wrappers and their focused assertions if the region becomes redundantly announced, cannot be operated as intended, or creates a regression. Preserve all prose, styles, table data, and fixture files. (UX-04–06)

### Slice 4: Add generated related-notes navigation

Start only after reproduced UX-01–06 findings are closed and Bret reviews a dry-run of the relation ranking on the current catalog as editorially sensible. The dry-run uses every other article as a candidate and the score `2 × shared assets + 1 × same topic + 1 × same research_type`. Sort by descending score, newer date, then source catalog order; show at most three. When all scores equal zero, show the three newest non-self articles under “Latest notes,” with date ties settled by catalog order. Always show “All notes.” Treat one or more positive-score matches as the related variant. A catalog containing only the current article cannot produce a truthful notes list; preserve “All notes” and omit an empty recommendation heading in that edge case. (ED-01, ED-07)

**Files and purpose**

* `build.py` — add deterministic candidate scoring and render the navigation as the last child of `<body>`, after all source essay content. The element is `<nav id="cr-related" aria-label="More notes">`, outside the essay DOM, and has relative article links. Keep the existing catalog schema and standard-library-only build. Update `verify()` to remove generated related navigation as well as the site bar before comparing built visible text with source visible text. Add generator verification for route targets and placement. (ED-01, ED-07)
* `assets/design-system.css` — add only `#cr-related`-scoped rules using existing `--cr-*` tokens. Explicitly reset font, color, background, margin, padding, link styles, and list styles; provide visible keyboard focus and responsive layout. Avoid `100vw` sizing. (ED-01, ED-07)
* `tests/visual.spec.ts` — add real-catalog browser checks for region presence outside essay content, one to three non-self links that resolve, the persistent “All notes” link, operation with JavaScript disabled, consistent computed styles, and axe violations at all severities. Normalize the displayed footer content to a fixed slug set before screenshots, following `homepageBaselineSlugs`; keep real dynamic output covered by these functional checks. Preserve the current screenshot threshold and use no masks. Do not construct synthetic catalog cases in Playwright. (ED-01, ED-07)
* `tests/test_site_structure.py` — call `rank_related_notes()` and `render_related_notes()` directly with constructed catalogs to cover deterministic score ordering, date/catalog-order tie breaks, self exclusion, the zero-score latest fallback, and the single-article empty-heading behavior. (ED-01)
* `tests/signatures.py` — extend the existing generated-chrome stripping mechanism to exclude the `#cr-related` subtree by its exact ID, just as it excludes `#cr-sitebar`. Do not strip elements by generic tag (`nav`, `a`), class, or position, and do not exclude related-looking markup from source article collection. The current helper strips only the site bar; without this exact-ID exclusion, generated nav text and links would look like essay signature drift. (ED-01)
* `tests/test_content_integrity.py` — add a regression test using an article that receives the generated nav. First prove that stripping the exact `#cr-related` subtree lets the built essay match its source fixture. Then change one sentence in a temporary copy of that essay and prove the content-signature comparison fails. This demonstrates that the chrome exclusion does not hide editorial changes. (ED-01)

**Signature impact:** The source article signature fixture remains unchanged. The generated nav adds visible text and links to built HTML, so the built-versus-source comparison removes only the subtree whose exact ID is `cr-related`, using the existing `#cr-sitebar` exclusion mechanism. The sentence-edit regression test must still fail against the existing fixture after that removal. This is a test-helper and guard-test change, not a fixture refresh. Do not refresh or rewrite signature fixtures. (ED-01)

**Style and placement checks:** The existing site bar is injected immediately after `<body>` and its styles are ID-scoped. `#cr-related` is appended before `</body>` as the last body child, after the source essay; it is not a `<footer>`. Current source inspection found a sticky `.side` panel in `content/venice-ai-privacy.html` above 900 px; it becomes static below 900 px. No fixed-position essay element was identified in the inspected source scan. Recheck this route at 1440 px for overlap/stacking, and include any other constrained-body or fixed/sticky cases found by the implementation-wide scan in the design evidence. No special-case CSS is approved in advance. (ED-01, ED-07)

**Visual targets and refresh commands:** The footer changes are expected on `bitcoin-buying-imbalance`, `venice-ai-privacy`, and `aero-at-0-68`. Normalize each screenshot to the same fixed slug set and stable heading before capture so catalog additions do not alter approved screenshots. Review expected, actual, and diff; if the intended footer appearance differs, refresh only that target, then inspect it again before moving to the next:

* `npx playwright test tests/visual.spec.ts --grep "visual baseline › bitcoin-buying-imbalance @" --update-snapshots`
* `npx playwright test tests/visual.spec.ts --grep "visual baseline › venice-ai-privacy @" --update-snapshots`
* `npx playwright test tests/visual.spec.ts --grep "visual baseline › aero-at-0-68 @" --update-snapshots`

No other visual target may be refreshed for this slice. The normalized screenshot path and the functional path must remain separate: screenshots test stable presentation; functional tests test real catalog-driven links. (ED-01, ED-07)

**Tests:** First run focused generator tests for both ranking variants and deterministic ties. Then run `python3 build.py`, `python3 -m unittest discover -s tests -p 'test_*.py'`, and `npx playwright test`. The browser suite must cover JavaScript-disabled access, all article footer routes, keyboard focus, axe issues at all severities attributable to the new nav, article overflow at 390/768/1440, and fixed computed styles across articles. Existing homepage overflow at 320/1024 and all current screenshot routes remain covered. Keep `maxDiffPixelRatio: 0.001`, Tinos/Noto Sans rendering, and the current `--cr-*` token values. (ED-01, ED-07)

**Rollback:** Keep this as a separate final slice. If the dry-run results are not editorially sensible, do not implement it. If the generated region causes link, accessibility, signature-comparison, style-isolation, or overflow failures, remove only the `build.py` related-nav generation, `#cr-related` CSS, its tests, and its screenshot normalizer/baseline updates. Retain completed Phase 1 corrections and unchanged content fixtures. (UX-01–06, ED-01, ED-07)

## Non-Functional Requirements

* **Accessibility:** Meet the specified contrast thresholds for reproduced UX-01–03 states; expose keyboard-operable, named regions for reproduced UX-04–06 states; avoid new axe findings from `#cr-related`. (UX-01–06, ED-01)
* **Editorial integrity:** Preserve prose and article presentation outside the finding-specific corrections. Keep source signatures and `tests/fixtures/content-signatures.json` unchanged; strip only generated elements with exact IDs for the built-versus-source comparison. (UX-02–06, ED-01)
* **Runtime and hosting:** Keep the site static, add no runtime dependency, render links in the initial HTML, and use relative article paths that work on Netlify and GitHub Pages project paths. (ED-01, ED-07)
* **Visual stability:** Keep Tinos/Noto Sans, `--cr-*` tokens, and `maxDiffPixelRatio: 0.001`; use fixed-slug screenshot normalization without masks or threshold changes. (ED-01, ED-07)

## Alternatives Considered

### 1. Correct accessibility issues at their current owning layers

* **Trade-off:** Small, finding-specific CSS and markup changes preserve each essay’s presentation but do not create a shared article-wide contrast system.
* **Verdict:** Selected for Phase 1. (UX-01–06)

### 2. Change shared color tokens across article styles

* **Trade-off:** A global adjustment could align more article labels, but article palettes and token fallbacks differ and could change unrelated charts or styles.
* **Verdict:** Rejected for this scope; adjust only declarations tied to reproduced findings. (UX-02–03)

### 3. Use CSS-only or JavaScript changes for scroll-region accessibility

* **Trade-off:** CSS or runtime behavior avoids source markup edits, but cannot reliably provide keyboard focus, region semantics, and an accessible name without JavaScript.
* **Verdict:** Rejected; use source attributes on the existing wrappers. (UX-04–06)

### 4. Curate related links manually for each article

* **Trade-off:** Manual selection may be more editorially relevant but requires ongoing editorial maintenance; metadata ranking is reproducible but may produce weaker matches.
* **Verdict:** Rejected for the initial implementation, subject to the current-catalog dry-run gate. (ED-01)

### 5. Defer related links entirely

* **Trade-off:** This avoids misleading matches, but leaves the observed discovery gap unaddressed if the deterministic ranking produces sensible results.
* **Verdict:** Rejected as the default path; retain as the fallback if the dry-run or implementation checks fail. (ED-01)

### 6. Add archive scanning, contents navigation, taxonomy, or date-label changes now

* **Trade-off:** These could address separate reader needs but add scope and make the results of this work harder to assess.
* **Verdict:** Rejected for this round; keep ED-02, ED-03, ED-05, and ED-09 deferred, with broader ED-07 navigation still open. (ED-02, ED-03, ED-05, ED-07, ED-09)

### 7. Render the footer client-side from `search-index.json`

* **Trade-off:** This could reuse the search index, but it would leave the footer unavailable when JavaScript is disabled and add a runtime dependency.
* **Verdict:** Rejected; generate the footer in `build.py`. (ED-01)

### 8. Mask the footer or exclude it from article screenshots

* **Trade-off:** This would avoid baseline updates when catalog matches change, but masks are prohibited and exclusion would leave footer layout unguarded.
* **Verdict:** Rejected; normalize footer links to fixed slugs before screenshot capture and keep functional tests on real output. (ED-01, ED-07)

## Open Questions

* **Dry-run acceptance:** Bret reviews the current-catalog output before implementation; no numeric relevance threshold is assumed beyond the explicit score and deterministic ordering. (ED-01, ED-05)

## Additional Resources

* UX evidence and finding IDs: `docs/designs/ux-audit/evidence/findings.md`
* Shared and article style inventory: `docs/designs/ux-audit/evidence/style-inventory.md`
* Authoring, validation, screenshot, and publishing contract: `README.md`
* Current generation and test contracts: `build.py`, `tests/signatures.py`, and `tests/visual.spec.ts`

## Future Improvements

* Archive scanning, excerpts, and ticker-label consistency remain deferred under ED-02.
* In-article contents navigation remains deferred under ED-03.
* Topic/research-type label alignment remains deferred under ED-05; current-topic and search navigation remain open under ED-07.
* Visible publication/data-age labels remain deferred under ED-09. Headline display changes, featured-placement explanation, and first-reader orientation remain separate editorial hypotheses under ED-04, ED-06, and ED-08.

## Detailed Implementation Plan

This section fills in call points, selectors, test names, and delivery order for the four slices above. It does not change their scope or repeat their rationale.

### 1. Reproduce UX-01–06

Add `docs/designs/ux-audit/evidence/scripts/remeasure.ts` as a standalone Playwright script and `docs/designs/ux-audit/evidence/remeasure.md` as its report output. The script is not a test and does not edit `tests/visual.spec.ts`. It reads pages from the built `dist/`: run `python3 build.py`, serve it with `python3 -m http.server 4174 --bind 127.0.0.1 -d dist`, then run `node --experimental-strip-types docs/designs/ux-audit/evidence/scripts/remeasure.ts`. Direct TypeScript execution support in the current Node runtime is **verify during implementation**; do not add a runtime dependency to run it. (UX-01–06)

At 390, 768, and 1440 px, record UX-01–03 foreground, effective opaque background (walking ancestors), font size/weight, element, selector, and contrast ratio. For UX-04–06, record each wrapper selector, focusability, horizontal overflow, and keyboard-scroll behavior. Check essay dark-mode styles if present. Save reproduced/not-reproduced status and any newly observed issue to `remeasure.md`, then summarize each finding here. If a selector or route does not match the current build, record that result rather than guessing a replacement. Do not change essay or generated production files in this slice. (UX-01–06)

### 2. Correct reproduced contrast findings

The current 404 kicker color rule is `body.cr-home .kicker`; the existing `body.cr-home .mast .kicker` selector can retain the gold color on the dark homepage masthead while leaving the 404 kicker on the existing `--cr-accent` rule. Change only this selector after Slice 1 confirms the reported 404 element and effective background. In `content/token-unlock-liquidity-illusion-90-day-calendar.html`, adjust only the reproduced `.kicker` and `.mast span:last-child` foreground declarations, using measured results to choose the smallest passing values in the existing palette family. Exact replacement values are **verify during implementation** after the three viewport measurements. (UX-01–03)

In the existing `test.describe("accessibility", ...)` block of `tests/visual.spec.ts`, add the contrast assertion listed in Detailed Implementation — check the 404 and token-unlock routes at all three widths and require no axe `color-contrast` nodes for the corrected states.

Do not alter existing home layout assertions or snapshots unless a reviewed home diff demonstrates an intended change. If a home screenshot genuinely changes, the exact command is `npm run test:browser:update:home`. The 404 and token-unlock article are not current screenshot targets. (UX-01–03)

### 3. Correct reproduced scroll-region findings

Add only the agreed attributes to the existing `.table-scroll`, `.tablewrap`, and `.scroll` containers in their named source essays. If a relevant existing heading or caption lacks an ID, add an ID to that existing element and point `aria-labelledby` to it; use `aria-label` only when no suitable heading or caption exists. Do not add visible text or CSS. **Verify during implementation** that the current selector and the best naming target match each finding before editing. (UX-04–06)

In the existing `test.describe("keyboard", ...)` and `test.describe("accessibility", ...)` blocks of `tests/visual.spec.ts`, add the Slice 3 assertions listed in Final Test Titles to verify keyboard operation, accessible name, and region role. Keep existing route-wide overflow and axe tests unchanged; their article route loops will exercise the edited source. (UX-04–06)

If and only if a reviewed, intended visual diff requires a snapshot refresh, use one target command at a time:

* `npx playwright test tests/visual.spec.ts --grep "visual baseline › aero-at-0-68 @" --update-snapshots`
* `npx playwright test tests/visual.spec.ts --grep "visual baseline › bitcoin-buying-imbalance @" --update-snapshots`

There is no approved token-unlock screenshot target. Attributes alone should not change screenshots; otherwise leave all baselines unchanged. (UX-04–06)

### 4. Add `#cr-related`

In `build.py`, add `rank_related_notes(note, notes)` next to `article_bar()` and the article-rendering helpers. It receives the current note and the already-loaded, ordered catalog, returns the selected candidates and variant, and applies the agreed score/date/catalog-order rules. `verify during implementation` that each note dictionary retains original catalog order through `load_notes()`; do not add or reorder catalog fields.

Change `render_article()` to receive the full ordered `notes` list, and update its call in the main build loop. Keep the current `#cr-sitebar` insertion exactly where it is: `render_article()` inserts it immediately after `body_match.end()`, as the first body child. After that injection and after all original essay content, insert the generated `#cr-related` markup immediately before the closing `</body>` so it is the last body child. Put markup construction in a neighboring `render_related_notes(note, notes)` helper. **Verify during implementation** the existing body-close matching behavior for every catalog source and keep the same missing-body failure behavior.

In `assets/design-system.css`, place one `#cr-related` block beside the existing ID-scoped `#cr-sitebar` block. Keep every selector rooted at `#cr-related`; use these selector forms:

* `#cr-related` and `#cr-related *` for the region box and inherited reset.
* `#cr-related .cr-related-inner` for the centered content width and spacing.
* `#cr-related h2`, `#cr-related ul`, `#cr-related li`, `#cr-related a`, and `#cr-related a:visited` for title, list, item, and link presentation.
* `#cr-related a:focus-visible` for a visible focus indicator.
* Any responsive or print rule must keep the `#cr-related` ID in its selector.

Reset `box-sizing`, `display`, `float`, `font` (family, size, weight, line-height), `color`, `background`, `margin`, and `padding` at the region; reset `margin`, `padding`, and `list-style` on lists and items; reset `font`, `color`, `background`, `text-decoration`, `text-transform`, `letter-spacing`, `border`, `margin`, and `padding` on links. Use existing `--cr-*` tokens and avoid `100vw`. **Verify during implementation** whether any essay sets inherited properties beyond this list that visibly bleed into the ID-scoped region; add a narrowly scoped reset only when browser evidence requires it. (ED-01, ED-07)

In `tests/test_site_structure.py`, call `rank_related_notes()` and `render_related_notes()` directly with constructed catalogs to test score weighting, date/catalog-order ties, self exclusion, zero-score fallback, and the one-article behavior. Keep the synthetic catalogs out of Playwright. In `tests/visual.spec.ts`, add only the real-output assertions listed in Final Test Titles under a new `test.describe("related notes", ...)` block.

* The actual, unnormalized article pages must show the region as the last body child, outside essay content, with one to three resolving non-self article links and an “All notes” link.
* Block JavaScript and confirm the server-rendered region and links remain available.
* Compare `font-family`, `font-size`, `color`, and `background-color` for `#cr-related` across catalog routes.
* Check the new region and page-level axe findings at all severities on article routes.

Modify the existing visual-baseline test listed in Final Test Titles to normalize only the `#cr-related` subtree to a fixed slug set and stable heading before taking screenshots for its three article targets. Keep the live-output assertions above separate and run them before normalization. Do not change `maxDiffPixelRatio`, mask the region, or remove its screenshots. (ED-01, ED-07)

In `build.py`, update `verify()` so its source-versus-built visible-text check removes the exact `#cr-related` subtree as well as `#cr-sitebar`. In `tests/signatures.py`, update the existing site-bar stripping path to remove only the elements with those exact IDs; never ignore generic `nav`/`a` tags, classes, or last-child content. Update the existing source-versus-build content-integrity assertion, and add the sentence-edit guard listed under Python Test Names. Keep `tests/fixtures/content-signatures.json` unchanged. (ED-01)

#### Final Test Titles

Add these Playwright titles in the stated `test.describe` blocks. Route and width placeholders are interpolated from the test loops:

* `accessibility › UX-01–03 contrast passes for <route> @ <width>`
* `keyboard › UX-04–06 scroll regions operate with keyboard for <route> @ <width>`
* `accessibility › UX-04–06 scroll regions have accessible names for <route>`
* `related notes › server-rendered region and links are valid for every article`
* `related notes › remains available without JavaScript`
* `related notes › keeps computed styles consistent across articles`
* `related notes › adds no axe violations`
* Existing screenshot tests retain the title pattern `visual baseline › <target> @ <width>`.

Add these Python test names in `tests/test_site_structure.py` and `tests/test_content_integrity.py`:

* `test_rank_related_notes_uses_weight_date_and_catalog_ties`
* `test_render_related_notes_uses_latest_notes_when_scores_are_zero`
* `test_render_related_notes_omits_latest_heading_for_single_article`
* `test_sentence_edit_is_not_hidden_by_related_nav_exclusion`

The existing `ContentIntegrityTest.test_build_preserves_source_signature` changes to remove the generated subtree by exact ID before comparing built and source signatures. The existing `visual baseline` tests keep their titles; only their screenshot setup gains fixed-slug normalization for the three article targets. No remeasurement test is added to `tests/visual.spec.ts`. (UX-01–06, ED-01, ED-07)

### Per-slice delivery order

For each slice, use this order: create or switch to its topic branch; make only that slice’s changes; run `python3 build.py`, `python3 -m unittest discover -s tests -p 'test_*.py'`, and `npx playwright test`; inspect failing test output and any expected/actual/diff images; refresh only an approved screenshot target after confirming the diff is intentional; open a PR; verify the Netlify deploy preview; merge only when required checks and the preview are green. Branch names and whether the repository prefers four separate PRs or a stacked PR sequence are **verify during implementation**. The current `netlify.toml` establishes the build command and publish directory, but availability and URL behavior of PR deploy previews are **verify during implementation**. Do not merge without a working, reviewed preview and green gates. (UX-01–06, ED-01)

The PR, deploy-preview, and merge steps describe the future delivery sequence; they are not present authorization to perform those external actions. Verify approval and remote state at implementation time. (UX-01–06, ED-01)

| Slice | Snapshot refresh, only after reviewing the target diff |
| --- | --- |
| 1 — reproduce | None. Evidence capture only. |
| 2 — contrast | `npm run test:browser:update:home` only if the reviewed home target has an intended paint change; otherwise none. |
| 3 — scroll regions | `npx playwright test tests/visual.spec.ts --grep "visual baseline › aero-at-0-68 @" --update-snapshots`; separately, `npx playwright test tests/visual.spec.ts --grep "visual baseline › bitcoin-buying-imbalance @" --update-snapshots`. No other targets. |
| 4 — related nav | `npx playwright test tests/visual.spec.ts --grep "visual baseline › bitcoin-buying-imbalance @" --update-snapshots`; then separately `npx playwright test tests/visual.spec.ts --grep "visual baseline › venice-ai-privacy @" --update-snapshots`; then separately `npx playwright test tests/visual.spec.ts --grep "visual baseline › aero-at-0-68 @" --update-snapshots`. |

For every slice, if a visual diff fails, inspect it before any update; correct unintended regressions and rerun the affected checks. Preserve earlier completed slices when rolling back a later one. (UX-01–06, ED-01)
