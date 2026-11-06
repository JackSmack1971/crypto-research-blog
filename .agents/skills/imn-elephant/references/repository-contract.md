# Independent Market Notes repository contract

Use this as an inspection index, not as a substitute for current source. Recheck relevant files before relying on any fact below.

## Verified local contract (2026-11-05)

- `README.md`: standalone HTML essays are source; `build.py` generates the static site in `dist/` without rewriting essay prose. `content/articles.json` is the article catalog. Merge one entry for an article; do not replace the catalog.
- `site.json`: owns canonical site URL and RSS GUID origin. Internal navigation must work under the GitHub Pages project path; absolute canonical metadata URLs are expected.
- `.github/workflows/pages.yml`: jobs are `build`, `content-check`, and `deploy`. Deploy is limited to `main` and waits for build and content-check. Browser/Playwright checks are not in this workflow.
- `netlify.toml`: build command runs `python3 build.py` and `python3 -m unittest discover -s tests -p 'test_*.py'`, publishing `dist/`.
- Required local commands documented by the repository: `python3 build.py` and `python3 -m unittest discover -s tests -p 'test_*.py'`. Playwright is optional local visual evidence, not a publication gate.
- Article/catalog invariants in `AGENTS.md`: required taxonomy fields, approved topics and research types, uppercase tickers, relative local links, reviewed content/metadata fixtures, and no fixture refresh to hide regressions.

## Recheck when relevant

Inspect `build.py`, `content/articles.json`, tests, `assets/`, `package.json`, Playwright config, and provider configuration for the task at hand. Repository state can change; current source and applicable instructions take precedence over this snapshot. A local test result does not establish GitHub Actions, Netlify, Pages, or live-site status.
