# Audit status

Raw tool outputs (`evidence/axe/*.json`, `evidence/lighthouse/*.json`, Lighthouse logs, and PNG captures) are local-only and ignored by Git. The committed Markdown summaries name the raw inputs from which they were derived.

- Step 1 (screenshots): complete. `python build.py` initially generated `dist/` but returned a Windows cp1252 console encoding error; `python -X utf8 build.py` succeeded (20 catalog articles). Local server responded at `http://127.0.0.1:4173/`. Captured 30 full-page PNGs: home default/search BTC/bitcoin topic/no matches, 404, and five requested articles at 390, 768, and 1440 px. No capture errors. Initial inventory is in `step1-inventory.md`.
- Step 2 (axe): complete. 20 raw JSON reports in `axe/`; `axe-summary.md` reports all impacts. WCAG 2.0/2.1 A+AA tags. Counts: critical 0, serious 7, moderate 0, minor 0, unknown 0. All scans completed successfully.
- Step 3 (Lighthouse): complete. Live site reachable (HTTP 200). Lighthouse 12.8.2 completed six runs: mobile and desktop for homepage, bitcoin-buying-imbalance, and newest catalog article token-unlock-liquidity-illusion-90-day-calendar. Raw JSON in `lighthouse/`; summary in `lighthouse-summary.md`.
- Step 4 (style inventory): complete. Shared generated chrome and inline style declarations for all 20 source articles are inventoried in `style-inventory.md`.
- Step 5 (findings): complete. `findings.md` contains evidence-linked issues and a not-checked list. It includes only observed axe and Lighthouse outcomes.

Errors recovered during execution: the initial build command hit Windows cp1252 output encoding after generating `dist/`; `python -X utf8 build.py` succeeded. An initial axe invocation used a Playwright convenience page unsupported by the installed axe integration; the runner was corrected to use `browser.newContext()` and all 20 scans completed. The first Lighthouse runner attempt had Windows argument quoting errors and no reports; the corrected runner completed all six live audits. A summary-script syntax typo was corrected before the Lighthouse summary was saved. No final requested step remains failed.
