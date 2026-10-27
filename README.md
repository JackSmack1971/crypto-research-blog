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

3. Build and check locally:

```bash
python3 build.py
python3 -m http.server -d dist
```

Open `http://127.0.0.1:8000/`. The build fails if a page, image, or home-page link does not resolve.

4. Commit the new HTML file and the catalog entry, then push to `main`. GitHub Actions publishes the site. A new essay also needs its content signature and, if it is part of the screenshot set, a reviewed visual baseline. See below.

## Checks

These checks guard the editorial text, charts, URLs, and layout. They are not part of the published site. `build.py` still uses only the Python standard library.

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
npm ci
npx playwright install chromium
npx playwright test
```

The Python tests rebuild `dist/`. Playwright rebuilds it again and serves that folder. Screenshots cover the homepage, the Bitcoin buying-imbalance note, Venice AI, and AERO at 390, 768, and 1440 pixels. Overflow, keyboard focus, and serious accessibility findings are checked on every article.

A layout or content regression fails the suite on its own. Widening the homepage past the viewport fails `no unexpected overflow`. Changing a sentence in an essay fails the content signature. Both were confirmed before any shared CSS was adopted. The screenshot check does not accept a new image when it fails.

## Reviewing a visual change

1. Run the suite and let the screenshot check fail.
2. Open the expected image, the actual image, and the diff under `test-results/`. Confirm the change is the intended type or color, and that the words, tables, and charts are intact.
3. Refresh only the screenshots you reviewed:

```bash
npx playwright test tests/visual.spec.ts -g "venice-ai-privacy @" --update-snapshots
```

4. Commit those PNGs with the CSS change. Do not raise `maxDiffPixelRatio`, and do not run `--update-snapshots` across the whole suite, to hide a diff.

`python3 tests/signatures.py --write` and `python3 tests/test_site_structure.py` rewrite the content and metadata fixtures. Use them only when an editorial change is intentional.

`tests/fixtures/known-defects.json` lists layout and accessibility issues that are already accepted. A new critical or serious issue fails the run. The Bitcoin holding-up small-caps contrast failure was fixed during the migration, so that list is empty.

## How publishing works

The site is published at <https://jacksmack1971.github.io/crypto-research-blog/>. Pages is set to **GitHub Actions** (**Settings → Pages → Build and deployment → Source**).

[`.github/workflows/pages.yml`](.github/workflows/pages.yml) builds on every push and pull request and runs the content, structure, and browser checks in `styling-check`. A push to `main` uploads `dist/` with `actions/upload-pages-artifact` and deploys it with `actions/deploy-pages`. The deploy job waits for both `build` and `styling-check`, and its `if` still limits it to `main`. Pull requests do not publish.

No paid host, database, or package install is required. The generator is [`build.py`](build.py) and uses only the Python standard library.
