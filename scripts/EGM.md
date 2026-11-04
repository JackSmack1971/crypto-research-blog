# Maintenance Scripts Package

## Overview

`scripts/` contains a Python utility for explicitly refreshing reviewed article and metadata fixtures and a separate Playwright live UX audit. The repository has two Playwright configurations: the regular regression config at the root (`../playwright.config.ts`) and this directory's standalone audit config (`ux-audit.playwright.config.ts`). CI invokes only the regular config; the live audit remains outside CI. [refresh_fixtures.py:main] [ux-audit.spec.ts:test] [ux-audit.playwright.config.ts:defineConfig] [../playwright.config.ts:defineConfig] [../.github/workflows/pages.yml:Browser regression checks]

## Interface

- Run the fixture refresh utility with `python3 scripts/refresh_fixtures.py`. It rebuilds and verifies the site, then writes metadata and content-signature fixtures. [refresh_fixtures.py:main]
- Run the standalone UX audit with `npx playwright test --config scripts/ux-audit.playwright.config.ts`. [ux-audit.playwright.config.ts:testMatch]
- The audit reads `content/articles.json`, resolves its representative article slugs, and visits the canonical live origin at three viewport widths. [ux-audit.spec.ts:catalog] [ux-audit.spec.ts:representativeSlugs] [ux-audit.spec.ts:origin] [ux-audit.spec.ts:widths]

## Invariants

- Fixture refresh calls metadata generation and signature generation only after the build and structural checks have run. [refresh_fixtures.py:main] [test_site_structure.py:write_metadata]
- The live audit fails if a representative slug is absent from the catalog or if a target route does not return a successful response. [ux-audit.spec.ts:selected] [ux-audit.spec.ts:test]
- The regular config selects `tests/` and is the config invoked by CI. The audit config selects only `ux-audit.spec.ts`, runs one worker, and is not invoked by CI. [../playwright.config.ts:testDir] [ux-audit.playwright.config.ts:testMatch] [ux-audit.playwright.config.ts:workers] [../.github/workflows/pages.yml:Browser regression checks]

## Side Effects

- Fixture refresh rewrites `tests/fixtures/metadata.json` and `tests/fixtures/content-signatures.json`. [refresh_fixtures.py:main] [test_site_structure.py:write_metadata] [signatures.py:write_fixture]
- The live audit sends browser requests to the public site and writes full-page PNGs and `findings.json` under `docs/ux-audit/evidence/`. [ux-audit.spec.ts:origin] [ux-audit.spec.ts:evidenceDir] [ux-audit.spec.ts:test]

## Verification

- Fixture refresh: `python3 scripts/refresh_fixtures.py` (review resulting fixture diffs)
- Live UX audit: `npx playwright test --config scripts/ux-audit.playwright.config.ts`
