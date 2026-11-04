# Independent Market Notes Blueprint

## System Overview

This repository builds a static publication of independent digital-asset research. `build.py` uses only Python standard-library modules and reads `site.json`, the editorial catalog and standalone article HTML under `content/`, plus shared assets; it writes generated pages, feeds, metadata, and copied assets to `dist/`. The essays carry their styles inline and remain individual HTML sources. Netlify's repository configuration sets the build command and publish directory; the GitHub Pages workflow separately gates deployment to `main`. `netlify.toml` does not specify Netlify's production branch, which is configured outside this repository. [build.py:main] [build.py:base64] [build.py:ET] [build.py:Path] [content/EGM.md] [netlify.toml:command] [netlify.toml:publish] [.github/workflows/pages.yml:deploy]

## Local Interface & Invariants

- `build.py` exposes the build entry point `main()` and validates inputs through `load_site()`, `load_notes()`, `featured_image()`, and `verify()`. [build.py:main] [build.py:load_site] [build.py:load_notes] [build.py:featured_image] [build.py:verify]
- `site.json` supplies the site title, canonical URL, RSS GUID origin, language, and featured article. [site.json:title] [site.json:url] [site.json:rss_guid_origin] [site.json:language] [site.json:featured_slug]
- `package.json` defines Python and Playwright development checks; `playwright.config.ts` runs the browser regression suite against a locally built site. [package.json:scripts] [playwright.config.ts:webServer]
- The committed screenshot baselines cover 390, 768, and 1440 pixel viewports. Their `maxDiffPixelRatio` is `0.001`; do not raise it to mask visual changes. [tests/visual.spec.ts:widths] [playwright.config.ts:maxDiffPixelRatio] [README.md:Reviewing a visual change]
- Screenshot rendering is pinned to Tinos for the editorial serif stack and Noto Sans for interface text. Substituting Noto Serif changes wrapping and invalidates screenshot comparisons. [tests/ci-fonts.conf:fontconfig] [.github/workflows/pages.yml:Match the fonts used to capture the baselines]
- The separate UX audit is configured by `scripts/ux-audit.playwright.config.ts` and implemented by `scripts/ux-audit.spec.ts`. It visits the live canonical site and writes screenshots and findings to `docs/ux-audit/evidence/`. [scripts/ux-audit.playwright.config.ts:defineConfig] [scripts/ux-audit.spec.ts:test]
- [Editorial catalog contract](./content/EGM.md)
- [Browser and content verification contract](./tests/EGM.md)
- [Maintenance and standalone audit scripts](./scripts/EGM.md)

## Global Invariants

- `site.json.url` is the canonical HTTPS origin; the independent RSS GUID origin remains stable. Featured article selection must resolve to a catalog slug. [build.py:site_url] [build.py:load_site] [build.py:select_featured]
- Catalog slugs, dates, taxonomy, tickers, source paths, article deks, and optional image metadata are validated before rendering. Generated local links must resolve within the generated site. [build.py:load_notes] [build.py:featured_image] [build.py:resolve_local]
- Article source integrity and reviewed metadata/signature fixtures are guarded by the Python suite; visual baselines and browser behavior are guarded by Playwright. [tests/test_content_integrity.py:ContentIntegrityTest] [tests/test_site_structure.py:SiteStructureTest] [tests/visual.spec.ts:visual baseline]
- Keep generated pages in `dist/`; do not edit them as publication sources. The reviewed fixtures in `tests/fixtures/` are test inputs, not routine build output. [build.py:DIST] [tests/signatures.py:FIXTURE]

## Global Side Effects

- `python3 build.py` deletes and recreates `dist/`, then writes generated site output there. [build.py:main]
- `npx playwright test` starts the configured local build and HTTP server and may write Playwright artifacts to its configured output directories. [playwright.config.ts:webServer]
- The standalone audit makes requests to the public Netlify site and writes PNGs and `findings.json` under `docs/ux-audit/evidence/`. [scripts/ux-audit.spec.ts:origin] [scripts/ux-audit.spec.ts:evidenceDir]
- A push to `main` can trigger the GitHub Pages deploy after its required jobs pass. `netlify.toml` sets `python3 build.py` and `dist/` but does not encode a production branch; the README documents `main` as the expected Netlify production branch, whose live setting is outside this repository. [.github/workflows/pages.yml:deploy] [netlify.toml:command] [netlify.toml:publish] [README.md:Netlify]

## System Verification

- Build: `python3 build.py`
- Python checks: `python3 -m unittest discover -s tests -p 'test_*.py'`
- CI browser regression suite: `npm ci` then `npx playwright install chromium` and `npx playwright test`
- Standalone live UX audit: `npx playwright test --config scripts/ux-audit.playwright.config.ts`
