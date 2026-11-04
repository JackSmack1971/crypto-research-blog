# Verification Package

## Overview

`tests/` contains Python checks for article integrity, featured-image behavior, generated routes and metadata, plus Playwright browser checks for layout, archive search, keyboard focus, accessibility, and screenshots. It also contains reviewed fixtures and visual baselines used by those checks. [test_content_integrity.py:ContentIntegrityTest] [test_featured_images.py:FeaturedImageTest] [test_site_structure.py:SiteStructureTest] [`visual.spec.ts`](./visual.spec.ts)

## Interface

- Run Python checks with `python3 -m unittest discover -s tests -p 'test_*.py'`. The modules rebuild `dist/` before checking output. [test_content_integrity.py:setUpModule] [test_site_structure.py:setUpModule]
- Run the configured Playwright suite from the repository root with `npx playwright test`; `playwright.config.ts` selects `tests/` and `visual-baselines/`. [playwright.config.ts:testDir] [playwright.config.ts:snapshotDir]
- `signatures.py` provides `signature()`, `article_sources()`, `collect()`, and fixture read/write functions for editorial source comparisons. [signatures.py:signature] [signatures.py:article_sources] [signatures.py:collect] [signatures.py:write_fixture] [signatures.py:load_fixture]
- `visual.spec.ts` covers layout and overflow, archive search, keyboard focus, axe accessibility, visual screenshots, shared design tokens, and representative image decoding. [visual.spec.ts:layout] [visual.spec.ts:research archive search] [visual.spec.ts:keyboard] [visual.spec.ts:accessibility] [visual.spec.ts:visual baseline]

## Invariants

- Article signatures compare editorial text, headings, links, blocks, tables, alt text, and embedded SVG/image/script data against reviewed fixtures. Fixture updates are explicit and must follow intentional content changes. [test_content_integrity.py:ContentIntegrityTest] [signatures.py:signature] [signatures.py:write_fixture]
- Structure checks compare generated metadata with the reviewed metadata fixture and validate generated routes, canonical URLs, feeds, and taxonomy. [test_site_structure.py:SiteStructureTest]
- Browser tests preserve article links, search and filter behavior, focus visibility, accessibility checks, overflow coverage, and screenshot contracts. [visual.spec.ts:all catalog article appears on the homepage] [visual.spec.ts:research archive search] [visual.spec.ts:keyboard] [visual.spec.ts:accessibility] [visual.spec.ts:visual baseline]
- Screenshot baselines cover 390, 768, and 1440 pixel widths. The configured screenshot tolerance is `maxDiffPixelRatio: 0.001` and must not be raised to hide a mismatch. [visual.spec.ts:widths] [playwright.config.ts:maxDiffPixelRatio] [README.md:Reviewing a visual change]
- CI screenshot typography depends on Tinos from Croscore for editorial serif text and Noto Sans for interface text; aliasing the serif stack to Noto Serif changes line wrapping. [ci-fonts.conf:fontconfig] [.github/workflows/pages.yml:Match the fonts used to capture the baselines]
- The standalone live UX audit uses its separate config and is not selected by the normal `tests/` Playwright config. [scripts/ux-audit.playwright.config.ts:testDir] [scripts/ux-audit.playwright.config.ts:testMatch] [playwright.config.ts:testDir]

## Side Effects

- Python test module setup calls `build.main()`, which rebuilds `dist/`. [test_content_integrity.py:setUpModule] [test_site_structure.py:setUpModule] [build.py:main]
- `test_site_structure.py:write_metadata()` rewrites `tests/fixtures/metadata.json`; `signatures.py:write_fixture()` rewrites `tests/fixtures/content-signatures.json`. These are explicit fixture-refresh operations, not automatic test repair. [test_site_structure.py:write_metadata] [signatures.py:write_fixture]
- Playwright may write screenshots and run artifacts under the configured test output paths. The standalone audit writes under `docs/ux-audit/evidence/`. [playwright.config.ts:snapshotDir] [scripts/ux-audit.spec.ts:evidenceDir]
- The CI workflow invokes `npx playwright test` with the repository-root config; it does not invoke the standalone UX audit config. [../.github/workflows/pages.yml:Browser regression checks] [../playwright.config.ts:testDir]

## Verification

- Python: `python3 -m unittest discover -s tests -p 'test_*.py'`
- Playwright: `npm ci`, `npx playwright install chromium`, then `npx playwright test`
