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

Refresh a baseline only after reviewing the diff. Do not update snapshots just to make a red check pass.

```bash
python3 tests/signatures.py --write
python3 tests/test_site_structure.py
npx playwright test --update-snapshots
```

`tests/fixtures/known-defects.json` records layout and accessibility issues that already existed before the styling work. A new critical or serious issue fails the run.

## How publishing works

[`.github/workflows/pages.yml`](.github/workflows/pages.yml) runs `python3 build.py` on every push and pull request. A push to `main` uploads `dist/` with `actions/upload-pages-artifact` and deploys it with `actions/deploy-pages`.

GitHub Pages has to be switched on once, by a repository admin:

**Settings → Pages → Build and deployment → Source: GitHub Actions**

Until that is set, the workflow can build successfully and the deploy job will not have a Pages environment to publish to.

No paid host, database, or package install is required. The generator is [`build.py`](build.py) and uses only the Python standard library.
