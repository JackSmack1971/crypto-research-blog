# Independent Market Notes — UX findings and editorial review

Reviewed: November 4, 2026<br>
Live site: https://independent-market-notes.netlify.app/<br>
Source: uploaded `findings.md`; independent reading of the live homepage/archive and two article pages.

**Evidence provenance and retention:** The tool-reported evidence in this review is summarized in `axe-summary.md` and `lighthouse-summary.md`. Those summaries identify their source reports; raw PNG/JSON captures and Lighthouse logs are local-only and ignored by Git.

## Editorial judgment

**Primary concern:** The site communicates an evidence-first research identity, but the pathways between investigations are weak. The next UX phase should prioritize findability, scanning, and continued reading without sacrificing the analytical voice or accessibility. Machine-scored defects remain valid; editorial observations below are deliberately distinguished from automated findings.

**Evidence limits:** The linked screenshot, axe JSON, and Lighthouse JSON files referenced by the original document were not supplied with this standalone upload. The original measured values are preserved as *reported by the source audit*, not independently rerun. Live pages were inspected through their accessible text/links, not a new visual, mobile-device, keyboard, or screen-reader test. Visual line wrapping, hit targets, interactions, and scroll behavior require browser verification.

## Confirmed tool-reported findings — retain

| ID | Reported finding | Where | Priority | Editorial decision / acceptance target |
| --- | --- | --- | --- | --- |
| UX-01 | 404 kicker contrast 1.63:1 (`#d9bd8a` on `#f6f3ec`), below 4.5:1 | `/404.html`, 390/1440 px | P1 | **Keep.** Change text color/token and confirm WCAG AA contrast in rendered state. |
| UX-02 | Topic label contrast 4.12:1 (`#6b7e86` on `#fcfcfa`) | `/token-unlock-liquidity-illusion-90-day-calendar/`, 390/1440 px | P1 | **Keep.** Audit shared muted-label tokens to avoid fixing only this page. |
| UX-03 | Article kicker contrast 4.26:1 (`#c55646` on `#fcfcfa`) | Same article, 390/1440 px | P1 | **Keep.** Audit shared kicker/accent tokens; retain intentional visual hierarchy. |
| UX-04 | `.table-scroll` horizontally scrollable region is not keyboard focusable | `/aero-at-0-68/`, 390 px | P1 | **Keep.** Ensure keyboard access and visible focus; test table semantics and scroll behavior. |
| UX-05 | `.tablewrap` horizontally scrollable region is not keyboard focusable | `/bitcoin-buying-imbalance/`, 390 px | P1 | **Keep.** Prefer reusable table-wrapper behavior over a one-off page patch. |
| UX-06 | `.scroll` horizontally scrollable region is not keyboard focusable | `/token-unlock-liquidity-illusion-90-day-calendar/`, 390 px | P1 | **Keep.** Same reusable fix; do not add redundant focus stops if the region is inherently keyboard accessible. |
| UX-07 | Lighthouse mobile homepage score 93; estimated image-delivery opportunities 426 KiB next-gen format and 608 KiB responsive sizing | `/` | P3 | ~~Treat as urgent design debt.~~ **Defer**, unless field performance or LCP points to the images. Assess responsive `srcset`/`sizes`, modern formats, and transfer size without introducing visual regressions. Estimates are opportunities, not cumulative guaranteed savings. |
| UX-08 | Newest-at-audit article mobile performance 93; accessibility 96; image-format/sizing opportunities | `/token-unlock-liquidity-illusion-90-day-calendar/` | P3 | ~~Prioritize image conversion ahead of reader journeys.~~ **Defer** behind accessibility and navigation; remeasure after changes. The article is identified as newest **at audit time**, not necessarily newest today. |

**Implementation grouping:** UX-01–03 are a shared color/contrast workstream. UX-04–06 are a reusable accessible overflow-table workstream. Preserve the six separate regression routes/assertions even when implementing one shared fix.

## Additional human/editorial findings

These are judgments based on the live text and links, **not** axe/Lighthouse failures or confirmed visual regressions.

| ID | Observation / evidence | Priority | Recommendation and check |
| --- | --- | --- | --- |
| ED-01 | **Article-to-article discovery is thin.** The inspected token-unlock article ends with sources/methodology and caveats, and the DeepBook article begins with a minimal `Independent Market Notes / All notes` navigation. No contextual “related notes” links were visible in the inspected article content. | P1 | Add 2–4 curated related investigations at article end (shared asset, market-structure question, or investigative method). Ensure links are genuinely relevant, and test that recommendations update as the archive grows. Verify rendered footer before labeling this a universal absence. |
| ED-02 | **Archive scanning demands effort.** The archive currently lists more than 20 investigations, with lengthy headlines, summaries, topic labels, dates, and sometimes tickers. Some entries have no visible ticker label. | P1 | Define consistent metadata hierarchy: topic, date, compact title, 1–2 sentence excerpt, optional ticker chips. Clamp excerpts visually only if full text remains accessible; avoid forcing uniform but vague headlines. Test 320/390/768/1440 px and zoom. |
| ED-03 | **Research journeys stop at single articles.** Articles present substantial technical work but the inspected token-unlock piece has multiple sections, tables, and a 90-day calendar with no section-navigation controls visible in the extracted page. | P1 | Provide a compact, keyboard-accessible on-page contents list for long investigations with stable heading anchors and a clear return to archive. Validate that contents links correspond to headings and do not collide with sticky elements. |
| ED-04 | **Headlines are strong but sometimes hard to skim.** Examples include “Binance's Four-Hour Wallet Takeover: 50 Authorizations, One Malicious Delegation, and a Delayed Revocation” and “DeepBook’s Supply Question: Is the Treasury Locked or Discretionary?” | P2 | Keep original H1s and editorial specificity; test optional shorter *archive display titles* or line lengths, not automated rewriting or SEO-title duplication. Prefer asset + consequence + key uncertainty within the visible opening lines. |
| ED-05 | **Archive taxonomy asks readers to interpret two parallel schemes.** Homepage filters include “Filter by topic” and “Filter by research type,” while visible tags include Bitcoin, Liquidity, Tokenomics, Protocol Research, and Risk & Verification; featured DeepBook is called “Protocol Research” on the homepage and “Tokenomics / Investigative analysis” on the article. | P1 | Define a canonical taxonomy and distinguish **subject** from **method/type**. Make labels consistent across feature, cards, article breadcrumbs, filtering, and structured data. Test every filter option against actual content. |
| ED-06 | **Featured placement needs a clear rule.** The homepage spotlights the November 3 DeepBook investigation while the November 4 archive includes newer pieces. This can be intentional curation, but the rationale is not explained. | P2 | Explicitly label as “Editor's pick”/“Featured investigation” and decide whether feature is curated or newest. Keep “Latest research” separately identifiable. Do not assume chronology is a bug. |
| ED-07 | **Article navigation feels detached from the broader library.** The inspected article header offers a home/site link and “All notes”; homepage offers subject chips and search/filter controls. | P1 | Add a compact, responsive global navigation strategy across article templates: archive access, current topic, and search entry point. Avoid a large mobile nav or duplicate menus. Verify actual touch/keyboard behavior before implementation. |
| ED-08 | **The site promise could be clearer for first-time readers.** “Research, with receipts” and “Evidence first. Conviction second.” are memorable, but the archive gives little immediate guidance about what a research type means or how to use it. | P2 | Introduce one concise orientation sentence or lightweight filter help; show what each classification means. Keep the homepage editorial, not dashboard-like. |
| ED-09 | **Timeliness and research validity need consistent visual differentiation.** Articles use snapshot dates and historical-price caveats; a reader arriving from search may overlook that a market setup has expired. | P1 | Standardize “Published”, “Data as of”, and, where relevant, “Historical snapshot / not live” in visible metadata. Avoid auto-labeling old research as invalid; distinguish time-sensitive trade setups from durable investigations. |
| ED-10 | **Dense research tables need more than horizontal scroll.** Token-unlock analysis includes rankings plus monthly event tables. The original audit documents keyboard-access failures in multiple wrappers. | P1 | Along with keyboard fixes, add scroll affordance or responsive table headings as appropriate; preserve sortable/numeric readability and accessible table headers. Never convert analytical data into unlabeled stacked cards. |

## Suggested delivery order

1. **Accessibility foundation:** Resolve UX-01–06 via shared tokens and reusable table wrappers. Preserve targeted axe/keyboard tests.
2. **Research navigation:** Implement ED-01, ED-03, ED-07: related notes, in-article contents, and a cohesive path to archive/search.
3. **Archive clarity and editorial metadata:** Implement ED-02, ED-05, ED-09, with filter testing and publication/snapshot distinctions.
4. **Editorial polish:** Evaluate ED-04, ED-06, ED-08 against mobile screenshots and real reading sessions.
5. **Performance follow-up:** Reassess UX-07–08 against measured Core Web Vitals, especially LCP and image weight; optimize where justified.

## Verification brief

- **Visual:** Review home, archive, article, and 404 at 320, 390, 768, 1024, and 1440 px; check headline wrapping, metadata order, header behavior, horizontal scroll cues, and focus visibility.
- **Interaction:** Keyboard-only and screen-reader pass for navigation, filter/search, contents links, and horizontally scrollable tables; verify no trapped focus, lost context, or unlabeled controls.
- **Content:** Related-note relevance, canonical taxonomy consistency, correct article counts, featured-vs-latest behavior, visible timestamp distinctions, and zero dead links.
- **Regression:** Keep axe checks, existing route coverage, and image/performance measurements. Do not introduce hard-coded article counts that will fail when the archive grows.
- **Evidence:** Record before/after screenshots, contrast ratios, measured performance, tested devices/browsers, and explicit exceptions. These editorial items become verified defects only after targeted inspection confirms them.

## Not checked / limitations

- Original linked screenshot, axe, and Lighthouse files were unavailable in the standalone upload. Their numbers were carried over from the supplied findings; no fresh automated scan was performed.
- Actual physical-device visual appearance, touch target sizes, text clipping, text wrapping, interactive filters/search, screen-reader output, and keyboard focus order were not independently exercised.
- Only the homepage/archive plus the token-unlock and DeepBook article content were independently reviewed; statements about article-wide patterns are hypotheses to test, not claims that every template behaves identically.

## References

- Source audit: `findings.md` (uploaded)
- https://independent-market-notes.netlify.app/
- https://independent-market-notes.netlify.app/token-unlock-liquidity-illusion-90-day-calendar/
- https://independent-market-notes.netlify.app/deepbook-supply-transparency/
