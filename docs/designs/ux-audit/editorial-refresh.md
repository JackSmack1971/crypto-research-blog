# Editorial design refresh

Implemented November 16, 2026 from the operator-approved three-phase UX audit.
This is a local implementation and validation record, not a deployment record.

## Implementation

1. **Visual foundation.** Consolidated the overlapping homepage rules into one
   shared stylesheet. Retained forest, paper, ink, and muted gold; gold accents on
   paper do not carry functional text. Shared serif titles and reading text,
   sans-serif labels, consistent spacing, focus treatment, and publication chrome.
2. **Homepage and archive.** Added a compact masthead, explicit research and
   methodology links, three chronological latest investigations independent of
   the editorial feature pin, and a text-led archive with dates, taxonomy, tickers,
   and research classifications. Existing featured artwork remains prominent.
   Expanded methodology discovery and the footer. Search still ranks ticker,
   title, topic, and description matches, combines filters, restores URL state,
   announces results, and retains all article links without JavaScript.
3. **Article experience.** Added catalog-derived context and a native, collapsible
   section guide using each essay's actual headings. Existing IDs survive; only
   missing section IDs are generated, without collisions. Harmonized reading
   typography, evidence callouts, citations, table fonts, and related-note framing.
   Preserved chart series, specialized analytical components, authorial text,
   source links, images, scripts, and the existing related-note ranking.

The archive's latest section hides while filtering so unrelated recent stories
are not mistaken for results. The masthead's Latest link returns to the unfiltered
edition. Generated navigation remains relative for the GitHub Pages project path.

## Review and regression scope

The existing home, Bitcoin buying imbalance, Venice AI, and AERO screenshot
baselines were reviewed at 390, 768, and 1440px using before, after, and pixel
comparison sheets. All twelve affected targets are intentionally refreshed for
shared navigation, typography, reading layout, and related-note framing; the home
also changes feature/latest/archive hierarchy and methodology presentation.
No screenshot thresholds, route coverage, or known-defect exceptions were relaxed.
The home snapshot now renders a fixed historical edition through the real
generator, rather than deleting current cards and substituting an inaccurate
count. Separate functional checks always use the complete current catalog.

Browser review also covered the current homepage, archive, methodology, and
representative article openings at desktop and mobile sizes, plus DeepBook's
comparison panel, Monad's calculator, and Bitcoin's table presentation. Local
preview captures are under the ignored directory
`evidence/screenshots/editorial-refresh/`.

The broader viewport checks exposed long-address wrapping problems, a chart
breakout on tablet, and WEFT's verdict panel exceeding its reading column at
1024px. Shared responsive rules address these without rewriting article sources.
Axe checks identified secondary text needing more contrast against paper and
heading-color overrides inappropriate inside dark panels. Metadata now uses the
shared muted color; analytical panels retain their original heading colors.

## Verification

- Python build: 43 investigations generated, with local-link verification.
- Python suite: 92 tests passed, including existing content signatures, metadata,
  canonical URLs, feed identity, image structure, and new section-guide tests.
- Browser full run: 348 passed, with one failure at WEFT / 1024px. The verdict
  breakout was then constrained in the shared stylesheet (the `fullbleed` class
  occurs only in that essay). All 7 focused WEFT checks passed after rebuilding:
  overflow at all five widths, site-bar visibility, and axe accessibility.
  Together these verify all 349 distinct browser checks on the final implementation.
- All 12 reviewed visual baselines passed both their refresh run and the full
  run's subsequent comparisons. No editorial fixture refresh was needed.
- `git diff --check`: passed.
- Content sources, catalog, site configuration, metadata/content fixtures,
  dependency declarations, lockfile, and publication workflows remain unchanged.

The optional browser suite includes all 45 routes (home, 43 articles, 404) at
320, 390, 768, 1024, and 1440px, archive interactions, no-JavaScript navigation,
keyboard use, section-guide targets, control sizes, image decoding, WCAG 2.2 AA
axe rules, and twelve visual comparisons. Automated accessibility findings are
not a full accessibility conformance certification; human visual/accessibility
review remains appropriate before publication.

No commits, pushes, hosted CI, Netlify/Pages deployment, or environment publication
were performed for this implementation.

Commands executed from the repository root:

```bash
python3 build.py
python3 -m unittest discover -s tests -p 'test_*.py'
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npx playwright test
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npx playwright test --grep 'weft-first-week'
git diff --check
```

For the screenshot refresh only, a temporary local config reused the already
running built site and kept the project comparison thresholds unchanged. The
reviewed targets were selected with `--grep 'visual baseline' --update-snapshots`.
The standard full-suite run then verified the refreshed files. Chromium
156.0.8078.79 was used; no hosted CI or cross-browser result is implied.
