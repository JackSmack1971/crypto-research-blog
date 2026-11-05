# Independent Market Notes

Static site for independent crypto market notes. The canonical publication URL is [independent-market-notes.netlify.app](https://independent-market-notes.netlify.app/). GitHub Pages remains available as a secondary deployment.

Each essay stays a standalone HTML page, with its own styles and images. The build adds a home page, a small “back to all notes” bar, an RSS feed, and basic social meta tags. It does not rewrite the prose.

[![Pages](https://github.com/JackSmack1971/crypto-research-blog/actions/workflows/pages.yml/badge.svg)](https://github.com/JackSmack1971/crypto-research-blog/actions/workflows/pages.yml)

## Change the site title

Edit `title` in [`site.json`](site.json). The home page, article bar, feed, and meta tags all read that file. `url` is the canonical public origin used for canonical links, the sitemap, and RSS permalinks. `rss_guid_origin` preserves stable RSS item identifiers when the canonical domain changes. `featured_slug` selects the lead investigation; when empty, the newest article is used. Navigation links are relative, so both Netlify and the GitHub Pages project path continue to work.

## Add a note

1. Save the essay as a self-contained HTML file in [`content/`](content/). Keep styles and images inline (or use paths relative to that file). Avoid root-absolute links such as `href="/chart.png"` — they break on a project site. The file should include a `<title>` and, ideally, `<meta name="description">`.
2. Add an entry to [`content/articles.json`](content/articles.json):

```json
{
  "slug": "my-new-note",
  "source": "my-new-note.html",
  "date": "2026-11-02",
  "title": "Optional. Defaults to the document title.",
  "dek": "Optional. A sentence copied from the essay. Defaults to the meta description.",
  "topic": "liquidity",
  "assets": ["UNI"],
  "research_type": "market-snapshot"
}
```

`slug` becomes the URL (`/my-new-note/`). `date` is `YYYY-MM-DD` and controls the order: newest first. Notes from the same day keep the order they appear in the file. If you set `dek`, it must appear in the essay itself.

`topic`, `assets`, and `research_type` are required. They power the archive filters and generated `search-index.json`. Topics are `bitcoin`, `market-structure`, `liquidity`, `tokenomics`, `protocol-research`, and `risk-verification`. Research types are `market-snapshot`, `investigative-analysis`, and `token-due-diligence`. Use uppercase ticker symbols for `assets`; the build rejects missing or unapproved values.

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

### Featured images and social previews

Save a real 1200 x 630 JPEG, PNG, or WebP file in `assets/featured/`.
Add optional fields to the existing entry in `content/articles.json`:

```json
{ "image": "assets/featured/my-new-note.jpg", "image_alt": "Editorial illustration of the article thesis", "image_width": 1200, "image_height": 630, "image_mime_type": "image/jpeg" }
```

The build validates the file signature, image path, declared dimensions, MIME type, and alt text. It publishes the asset under `dist/assets/featured/`, generates absolute Open Graph and X image URLs, uses `summary_large_image`, and adds the image to BlogPosting schema. Legacy articles without images retain their previous rendering and metadata.

The featured artwork stays separate from article visuals. Any preexisting source `og:image`, `twitter:image`, or conflicting `twitter:card` tags must be removed before registering an image; the build refuses conflicting metadata. The build does not insert an article hero or rewrite charts.

The canonical hostname comes from `site.json`. Confirm that this URL matches the live domain before distributing links; social crawlers must be able to fetch both article and image over HTTPS. Social preview cache behavior requires post-deployment testing.

For a ChatGPT publication ZIP: copy its HTML to `content/`, featured artwork to `assets/featured/`, and merge `publish.json` fields into the existing `content/articles.json` entry. Never replace the entire catalog with one manifest.
## Checks

The required publication checks guard content and structure. CI builds the site and runs the Python checks; it does not install Chromium or run Playwright. The generator still uses only the Python standard library.

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

The Python tests rebuild `dist/` and verify content signatures, metadata, and site structure. Browser-based visual and accessibility checks remain available for local review, but they are not a publication or deployment gate.

## Reviewing a visual change

1. Run the browser suite locally and inspect any screenshots or diffs in `test-results/`.
2. Download and inspect the expected image, actual image, and diff. Confirm the visual change is intended and that text, tables, and charts remain intact.
3. Refresh only the reviewed targets. For an intentional homepage design change, run:

```bash
npm run test:browser:update:home
```

For another target, use `npx playwright test tests/visual.spec.ts --grep "<target> @" --update-snapshots` with that target’s exact test name. Commit the reviewed PNGs with the visual change. Do not raise `maxDiffPixelRatio` or update the whole screenshot suite to hide a diff.

`python3 scripts/refresh_fixtures.py` regenerates both the content signature and metadata fixtures. It is an explicit local command; CI never refreshes baselines automatically.

`tests/fixtures/known-defects.json` lists layout and accessibility issues that are already accepted. A new critical or serious issue fails the run. The Bitcoin holding-up small-caps contrast failure was fixed during the migration, so that list is empty.

## How publishing works

The canonical site is <https://independent-market-notes.netlify.app/>. The repository also retains its GitHub Pages deployment at <https://jacksmack1971.github.io/crypto-research-blog/>. Pages is set to **GitHub Actions** (**Settings → Pages → Build and deployment → Source**).

[`.github/workflows/pages.yml`](.github/workflows/pages.yml) builds on every push and pull request and runs the Python content and structure checks. A push to `main` uploads `dist/` with `actions/upload-pages-artifact` and deploys it with `actions/deploy-pages`. The deploy job waits for both `build` and `content-check`, and its `if` still limits it to `main`. Pull requests do not publish.

No paid host, database, or package install is required. The generator is [`build.py`](build.py) and uses only the Python standard library.

## Netlify

The repository includes [`netlify.toml`](netlify.toml), which runs `python3 build.py` and publishes `dist/`. Netlify's build command and publish directory should match those values. Deploy from the repository root with `main` as the production branch; do not publish the repository root, which has no generated `index.html`.
