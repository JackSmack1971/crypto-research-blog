# Crypto Research

Static site for independent crypto market notes. The published site is [jacksmack1971.github.io/crypto-research-blog](https://jacksmack1971.github.io/crypto-research-blog/).

Each essay stays a standalone HTML page, with its own styles and images. The build adds a home page, a small “back to all notes” bar, an RSS feed, and basic social meta tags. It does not rewrite the prose.

[![Pages](https://github.com/JackSmack1971/crypto-research-blog/actions/workflows/pages.yml/badge.svg)](https://github.com/JackSmack1971/crypto-research-blog/actions/workflows/pages.yml)

## Change the site title

Edit `title` in [`site.json`](site.json). The home page, article bar, feed, and meta tags all read that file. `url` is the public site origin used for canonical links, the sitemap, and RSS. Navigation links are relative, so the pages still work if the site is served from the `/crypto-research-blog/` project path.

## Add a note

1. Save the essay as a self-contained HTML file in [`content/`](content/). Keep styles and images inline (or use paths relative to that file). Avoid root-absolute links such as `href="/chart.png"` — they break on a project site. The file should include a `<title>` and, ideally, `<meta name="description">`.
2. Add an entry to [`content/articles.json`](content/articles.json):

```json
{
  "slug": "my-new-note",
  "source": "my-new-note.html",
  "date": "2026-11-02",
  "title": "Optional. Defaults to the document title.",
  "dek": "Optional. A sentence copied from the essay. Defaults to the meta description."
}
```

`slug` becomes the URL (`/my-new-note/`). `date` is `YYYY-MM-DD` and controls the order: newest first. Notes from the same day keep the order they appear in the file. If you set `dek`, it must appear in the essay itself.

3. Refresh the committed text and metadata baselines with one command:

```bash
python3 scripts/refresh_fixtures.py
```

This regenerates `tests/fixtures/content-signatures.json` and `tests/fixtures/metadata.json` in catalog order. Review both diffs; run it only after an intentional article or metadata change.

4. Build and check locally:

```bash
python3 build.py
python3 -m http.server -d dist
```

Open `http://127.0.0.1:8000/`. The build fails if a page, image, or home-page link does not resolve.

5. Commit the HTML, catalog, and refreshed text fixtures together, then push to `main`. GitHub Actions publishes only after the existing checks pass.

## Checks

These checks guard the editorial text, charts, URLs, and layout. They are not part of the published site. `build.py` still uses only the Python standard library.

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
npm ci
npx playwright install chromium
npx playwright test
```

The Python tests rebuild `dist/`. Playwright rebuilds it again and serves that folder. Screenshots cover the homepage, the Bitcoin buying-imbalance note, Venice AI, and AERO at 390, 768, and 1440 pixels. Homepage screenshots use a stable list of article slugs declared in `tests/visual.spec.ts`; new articles are checked separately for homepage presence, overflow, keyboard focus, and accessibility, so routine publishing does not require a homepage screenshot refresh. Overflow, keyboard focus, and serious accessibility findings are checked on every article. CI installs the faces Chromium used for these baselines: Tinos, from the Croscore fonts, for the editorial serif stack, and Noto Sans for interface text. Aliasing that serif stack to Noto Serif changes wrapping and fails the screenshot check.

A layout or content regression fails the suite on its own. Widening the homepage past the viewport fails `no unexpected overflow`. Changing a sentence in an essay fails the content signature. Both were confirmed before any shared CSS was adopted. The screenshot check does not accept a new image when it fails.

## Reviewing a visual change

1. Run the suite and let the screenshot check fail. CI now uploads `test-results/` as a `browser-failure-<run_id>` artifact, so the actual screenshots and diffs are available from the failed run without changing the workflow.
2. Download and inspect the expected image, actual image, and diff. Confirm the visual change is intended and that text, tables, and charts remain intact.
3. Refresh only the reviewed targets. For an intentional homepage design change, run:

```bash
npm run test:browser:update:home
```

For another target, use `npx playwright test tests/visual.spec.ts --grep "<target> @" --update-snapshots` with that target’s exact test name. Commit the reviewed PNGs with the visual change. Do not raise `maxDiffPixelRatio` or update the whole screenshot suite to hide a diff.

`python3 scripts/refresh_fixtures.py` regenerates both the content signature and metadata fixtures. It is an explicit local command; CI never refreshes baselines automatically.

`tests/fixtures/known-defects.json` lists layout and accessibility issues that are already accepted. A new critical or serious issue fails the run. The Bitcoin holding-up small-caps contrast failure was fixed during the migration, so that list is empty.

## How publishing works

The site is published at <https://jacksmack1971.github.io/crypto-research-blog/>. Pages is set to **GitHub Actions** (**Settings → Pages → Build and deployment → Source**).

[`.github/workflows/pages.yml`](.github/workflows/pages.yml) builds on every push and pull request and runs the content, structure, and browser checks in `styling-check`. A push to `main` uploads `dist/` with `actions/upload-pages-artifact` and deploys it with `actions/deploy-pages`. The deploy job waits for both `build` and `styling-check`, and its `if` still limits it to `main`. Pull requests do not publish.

No paid host, database, or package install is required. The generator is [`build.py`](build.py) and uses only the Python standard library.
