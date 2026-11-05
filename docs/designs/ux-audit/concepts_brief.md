# Mobile Article Access and Related Notes

* **Author:** Bret
* **Date:** 2026-11-04

## Overview

This proposal targets people who open an Independent Market Notes article from a shared link, with mobile use as a working audience hypothesis. Phase 1 closes the six scoped contrast and keyboard-access findings UX-01–06. Only after those fixes meet measurable closure criteria, Phase 2 adds a generated, no-JavaScript related-notes section based on existing article topics and tickers. The first phase addresses reported accessibility defects; the second is a limited discovery experiment for ED-01 and part of ED-07, not a redesign of the archive or article system.

The audience assumption is not established by traffic or referral data. The findings document reports mobile viewport issues, but says source screenshots, axe output, and Lighthouse output were unavailable and the measurements were not rerun. Treat those values as inherited audit evidence until checked against the current build. (UX-01–06, ED-01, ED-07)

## Analysis

### Evidence and reader problem

The audit reports a 1.63:1 contrast ratio for the generated 404 kicker (UX-01), 4.12:1 and 4.26:1 for two labels on the token-unlock essay (UX-02, UX-03), and three horizontally scrollable article regions that were not keyboard-focusable (UX-04–06). These are tool-reported findings from the supplied audit, not fresh measurements. Before claiming closure, recalculate rendered contrast and confirm the actual elements and backgrounds. (UX-01–06)

The editorial findings describe thin cross-article discovery and detached navigation (ED-01, ED-07). They are observations from limited page inspection, not automated failures or evidence that readers click—or need—related links. The audit itself says the original screenshots and interaction evidence were unavailable and the reviewed pages were limited. A taxonomy-driven footer is therefore a small experiment, not proof of improved discovery. (ED-01, ED-07)

### Scope and implementation boundary

Phase 1 edits only the generated 404 chrome for UX-01, the failing declarations in the specified essay CSS for UX-02/03, and attributes on the existing horizontal-scroll wrappers for UX-04–06. Preserve article text, other CSS declarations, each essay’s palette family, table data, and the source-versus-generated boundary. Log each contrast change with finding ID, file and selector/property, old/new foreground values, rendered background, and old/new WCAG ratio. Use at least 4.5:1 for normal text unless rendered size and weight qualify for the applicable large-text threshold. Do not turn this scoped correction into a shared article style layer. (UX-01–06)

For UX-04–06, make each existing scroll container keyboard-focusable and a named region. Prefer `aria-labelledby` referencing an existing, visible, relevant table heading or caption; use a concise `aria-label` only when none exists. Confirm focus is visible and the region can actually be scrolled horizontally by keyboard. Avoid redundant ARIA and unnecessary focus stops on elements that are not the reported overflow containers. (UX-04–06, ED-10)

Phase 2 uses existing `topic`, `assets`, `research_type`, `date`, and catalog order in `content/articles.json`; it adds no catalog schema or runtime service. Generate related links in `build.py` as the last child of `<body>`, after the essay and outside its DOM, using the same injection approach as `#cr-sitebar`. Use `<nav id="cr-related" aria-label="More notes">`, not a `<footer>` element. Scope every rule under `#cr-related`, use `--cr-*` tokens, and reset font, color, background, margin, padding, link and list styles to resist essay CSS bleed. Avoid `100vw` breakouts. The generated region must work with JavaScript disabled. Keep generated title/link data out of source essays so editorial signatures continue to represent the essay itself. Inspect essays with fixed/sticky positioning or constrained body widths and list any requiring special handling. (ED-01, ED-07)

Topic or ticker overlap is a relevance signal, not evidence of substantive relation. For each candidate other than the current article, score `2 × shared assets + 1 × same topic + 1 × same research_type`; sort by score descending, then newer date, then original catalog order, and display the top three. Identical catalog input must produce identical output. If no candidate scores above zero, show the three newest other notes under the honest heading “Latest notes.” Always end with the existing “All notes” link. Test both variants, including a fixture or constructed catalog that reaches the latest-notes fallback. This rule is explainable and reproducible, but metadata overlap still does not establish editorial relevance; review representative results before release. (ED-01, ED-05)

The renderer currently injects a site bar after `<body>` and preserves independently styled source essays. Some essays already have source footers and broad footer/section selectors. The new region must not nest inside the essay or accidentally inherit article footer styling; use an explicit last-child insertion point and styles scoped to `#cr-related`. Assert that it is outside the source article and does not alter source signatures. Relative paths must continue to work under both Netlify and GitHub Pages project paths. (ED-01)

### Closure criteria and evidence limits

Phase 2 begins only when all six Phase 1 items pass their named-route checks: UX-01 at the generated 404, UX-02/03 at the token-unlock article, and UX-04/05/06 at their specified articles. Record actual rendered contrast ratios and source values; verify each scroll region has a useful accessible name, visible focus, keyboard reachability, and horizontal scroll operation. Retain existing route-wide overflow and serious/critical axe coverage; add focused assertions where existing checks do not prove the specific behavior. Do not add known-defect exceptions to make a check pass. (UX-01–06)

For the footer slice, assert that every generated article has the intended related-notes region, contains one to three links, has no self-link, and resolves every link to an article route. Test both the scored related variant and the “Latest notes” fallback, including a fixture/constructed case. Test keyboard access and accessibility, plus overflow on the existing article viewport matrix (390, 768, 1440 px); the homepage separately retains its 320 and 1024 px overflow checks. The existing axe scan runs at 1440 px, so do not describe it as all-width coverage. Keep current test coverage and the screenshot threshold `maxDiffPixelRatio: 0.001`; normalize the footer to a fixed slug set in visual baselines, following `homepageBaselineSlugs`, and inspect expected, actual, and diff images before refreshing only the affected targets, one at a time: bitcoin-buying-imbalance, venice-ai-privacy, and aero-at-0-68. Do not use masks or threshold changes. Do not refresh fixtures for the UX-04–06 markup attributes; the checked signature algorithm records text, headings, links, blocks, tables, alt text, and embedded SVG/image/script content, not generic wrapper attributes. (UX-01–06, ED-01)

For UX-01–03, measure computed foreground, effective opaque background (walking ancestors), and font size/weight in Playwright at 390, 768, and 1440 px. Apply 4.5:1 for normal text and 3:1 for large text; use the smallest change within the existing palette family that passes. Record before/after ratios per finding in the design document and require zero axe color-contrast nodes on those routes. Check dark-mode styles if an essay defines them. The requested target list does not include the 404 or token-unlock article; their non-screenshot checks must still establish contrast behavior. The current evidence does not establish physical-device appearance, screen-reader output, related-link usefulness, or the mobile share-link cohort; report those as unverified unless separately measured. (UX-01–03, ED-01, ED-07)

### Finding dispositions

- **ED-01 — partly addressed:** a generated footer provides onward links, but metadata overlap does not guarantee editorial relevance and the audit did not establish universal absence. Validate recommendation quality; do not claim curation or improved engagement. (ED-01)
- **ED-02 — deferred:** no archive scanning changes, excerpt hierarchy, or consistent ticker labels are in scope. (ED-02)
- **ED-03 — deferred:** no in-article table of contents or section navigation is added. (ED-03)
- **ED-05 — deferred:** topic versus research-type distinctions and label consistency remain unresolved. Related links must not imply this has been fixed. (ED-05)
- **ED-07 — partly addressed:** the current site bar already has “All notes,” and related links add contextual paths. Current-topic and search navigation remain open. (ED-07)
- **ED-09 — deferred:** no visible Published, Data as of, or Historical snapshot metadata is added. (ED-09)
- **ED-04, ED-06, ED-08 — deferred editorial hypotheses:** headline scanning, featured-placement rationale, and first-reader orientation are outside this round. (ED-04, ED-06, ED-08)
- **ED-10 — partly addressed:** keyboard access addresses one documented table barrier; visual scroll affordance and broader dense-table presentation remain open. (ED-10)
- **UX-07 and UX-08 — deferred:** image delivery opportunities are audit-reported estimates, not guaranteed savings; remeasure performance before prioritizing them. (UX-07, UX-08)

## Goals vs. Non-Goals

* **In-Scope Goals:**
  * Close UX-01–03 with scoped color declaration changes and recorded, rendered contrast evidence. (UX-01–03)
  * Close UX-04–06 with markup-only accessible names, region semantics, keyboard focus, and verified horizontal scrolling. (UX-04–06)
  * After Phase 1 closes, test a deterministic, static related-notes footer generated from existing catalog data. (ED-01, ED-07)
  * Preserve source essay text and styles outside the explicitly failing declarations, existing content signatures, no-JavaScript access, relative links, shared tokens, standard-library-only build, and current test/screenshot policy. (UX-01–06, ED-01)

* **Out-of-Scope Non-Goals:**
  * No general article style layer, broad palette cleanup, essay redesign, visible copy/layout change, image/chart change, or taxonomy/catalog schema expansion. (UX-01–06, ED-05)
  * No archive hierarchy, excerpt, ticker-label, table-of-contents, publication-timeliness, or broader current-topic/search navigation work. (ED-02, ED-03, ED-05, ED-07, ED-09)
  * No image optimization in response to unverified savings estimates, analytics, remote service, runtime JavaScript, or remote publication. (UX-07–08)
  * No claim that the footer solves all discovery needs or that the audit proves most visitors arrive on mobile. (ED-01, ED-07)

## Alternatives Weighed

1. **Fix the reported contrast and overflow problems at their current owning layers (selected for Phase 1).** This matches the repository’s split between generated chrome and independently styled essay sources, and limits changes to known declarations and wrappers. The cost is that local essay palettes do not become a site-wide contrast system. (UX-01–06)
2. **Change shared color tokens for all article styles (rejected for this slice).** The style inventory shows article-specific palettes and fallbacks; changing a shared token can affect unrelated labels, charts, or pages and exceeds the findings. Use only if rendered inspection proves the token itself owns the failed declaration. (UX-02–03)
3. **Use CSS-only styling or JavaScript to make overflow regions accessible (rejected).** CSS cannot supply keyboard focus, region semantics, and a name; runtime enhancement adds a dependency and risks leaving content inaccessible when JavaScript is unavailable. Native source attributes directly address the reported regions. (UX-04–06)
4. **Curate related links manually per article (not selected for the experiment).** Curation can improve semantic relevance but requires editorial maintenance and catalog changes. Metadata matching avoids that work but has weaker relevance; validate its quality before treating it as a lasting recommendation system. (ED-01, ED-05)
5. **Defer related links entirely (valid fallback).** Phase 1 is independently useful and better evidenced. If topic/asset matches are not consistently useful across representative articles, stop after Phase 1 rather than shipping misleading recommendations. (UX-01–06, ED-01)
6. **Add archive scanning, on-page contents, taxonomy, or date-label improvements now (rejected as scope expansion).** These target separate editorial hypotheses and would weaken attribution of results for this bounded phase. Revisit them separately against ED-02, ED-03, ED-05, and ED-09. (ED-02, ED-03, ED-05, ED-09)

## Key Decisions & Staging for Next Steps

1. **Reproduce before correcting:** remeasure UX-01–06 against the current build, including rendered contrast, exact element/selector, and scroll-container behavior. Record evidence. If a finding does not reproduce, close it as “not reproduced” with evidence and make no edit. Record newly found issues but do not add them to scope without Bret’s approval. (UX-01–06)
2. **Phase 1 — accessibility corrections:** inspect the actual rendered targets, map exact selectors and wrapper elements, make only the specified declaration/attribute changes, and record contrast evidence. Preserve essay prose, other styles, fixtures, screenshot baselines, and known-defect policy. Close the phase only after named-route contrast and keyboard behavior checks pass. (UX-01–06)
3. **Phase 2 gate:** do not begin footer implementation until Phase 1 has objective closure evidence. Before implementation, dry-run the candidate relation rule against the current catalog and have Bret confirm the output is editorially sensible. (UX-01–06, ED-01)
4. **Phase 2 — generated navigation:** score every other article `2 × shared assets + 1 × same topic + 1 × same research_type`; sort by score descending, then newer date, then catalog order; show the top three. When all scores are zero, show the three newest non-self notes under “Latest notes.” If the catalog contains only the current article, omit that empty heading and keep “All notes.” Always include “All notes.” Insert `<nav id="cr-related" aria-label="More notes">` as the last child of `<body>`, outside essay DOM, with ID-scoped resets and styles. (ED-01, ED-07)
5. **Baseline stability and tests:** normalize the generated nav to a fixed slug set in visual tests, following the `homepageBaselineSlugs` pattern; keep a separate functional test for real links and the latest-notes variant. Do not use masks, change `maxDiffPixelRatio`, or refresh content-signature fixtures. Record rendered contrast values and check 390/768/1440 px, axe contrast results, keyboard behavior, overflow, route resolution, and computed nav style. Keep `build.py` standard-library-only. (UX-01–06, ED-01)
6. **Independent delivery and rollback:** keep each of the four slices buildable and verifiable on its own. If Phase 2 fails the ranking dry-run, accessibility, link, style-isolation, or layout checks, do not ship it or revert only that slice without undoing completed Phase 1 fixes. No push, merge, deployment, or fixture refresh is authorized by this proposal. (UX-01–06, ED-01)
7. **Success measures:** first reproduce and record UX-01–06; then close only reproduced findings using applicable WCAG thresholds and keyboard access. Phase 2 must produce a correctly placed region on every article with 1–3 resolving non-self note links (or the zero-score latest variant), a persistent All notes link, no JavaScript dependency, and stable screenshots after catalog growth. Relevance quality remains a manual editorial review. (UX-01–06, ED-01)
8. **Effort and unknowns:** Phase 1 is a small, bounded source change with verification effort driven by rendered contrast and keyboard behavior. Phase 2 is a small-to-moderate generator/CSS/test change; first inspect current ranking output and source-placement edge cases. Exact hours and test runtime are not estimated. No local checks were run as part of this brainstorm; the brief is not implementation or deployment evidence. (UX-01–06, ED-01)
