---
name: imn-elephant
description: Establish and verify Independent Market Notes (crypto-research-blog) repository context before planning, reviewing, or changing its publishing generator, catalog, styling/UX, browser regressions, or deployment. Use for EGM Elephant context gathering; not for standalone crypto research, writing an essay, or publishing an already-approved article without repository-context analysis.
---

# Independent Market Notes — evidence-qualified Elephant

This skill exists to **assemble a current, source-traceable repository contract and risk map** when a task plans, reviews, or changes the Independent Market Notes site. It is **context preparation**, not a mandate to implement, publish, merge, or refresh baselines.

## 1. Establish actual authority and scope

1. Confirm the working repository and the requested change surface. Locate applicable `AGENTS.md` / `AGENTS.override.md` instructions from the working directory through relevant parents; **do not assume an `AGENTS.md` exists at the repository root**. If the EGM artifact location is unspecified, report that and use no invented directory.
2. Inspect `git status --short`, relevant diffs, and current sources *before* relying on the snapshot in `references/repository-contract.md`. If only remote read access exists, identify repository/ref/commit or blob SHAs and mark local working-tree state **unknown**. Never claim a remote snapshot proves the local tree is clean.
3. Read `README.md` first for workflow and build authority, then only the files required by the change surface in the table below. Inspect the relevant code/test blocks, not merely their filenames. Resolve differences in favor of current repository evidence and applicable instructions; record any conflict rather than silently applying this skill's historic values.

| Change surface | Minimum additional inspection |
|---|---|
| Build, generated chrome, routing, links, search, RSS, sitemap | `build.py`, `site.json`, `content/articles.json`, relevant Python tests; search UI also `tests/visual.spec.ts` |
| Home/catalog ordering, filters, labels, metadata | `content/articles.json`, `build.py`, relevant catalog/metadata tests and `tests/visual.spec.ts` |
| Styling, responsive UX, accessibility, images | `build.py`, representative affected `content/*.html`, `tests/visual.spec.ts`, `playwright.config.ts`, `tests/fixtures/known-defects.json` |
| Screenshot/test policy or fixture changes | Relevant tests, fixtures, `package.json`, `playwright.config.ts`, `README.md`, CI workflow |
| Deployment, publishing paths, hosting | `.github/workflows/pages.yml`, `netlify.toml`, `site.json`, `build.py`, deployment guidance in `README.md` |
| EGM review/plan/drift | Relevant files above, **actual** EGM instructions and artifacts if available; do not invent Goldfish setup or authority |

For known repo facts and previously observed hazards, load `references/repository-contract.md` **only when a matching decision is in scope**. For a change proposal or assessment, use `references/change-review.md` to build a proportionate evidence and verification matrix.

## 2. Extract the decision-changing contract

Report each applicable finding as **verified now** (path and evidence), **documented but not checked**, **changed/contradicted**, or **unknown**. At minimum, assess:

- Editorial integrity: wrapper and catalog changes must not silently mutate source essay prose; distinguish intended editorial revisions from incidental generator/UX edits. Check signature fixtures and their update workflow before editing them.
- Generation provenance: identify source (`build.py`, config, catalog, essay) versus derived `dist/` output before changes. Regenerate from authority rather than patching generated pages by hand.
- Portability: verify relative navigation and asset paths for both the canonical Netlify origin and secondary GitHub Pages project-path deployment. Canonical absolute metadata URLs may be appropriate; don't ban them indiscriminately.
- Regression scope: match check selection to affected behavior; preserve meaningful assertions, accessibility checks, and visual-diff sensitivity. Do not refresh a snapshot simply because it fails.
- Publication effects: distinguish local edits from remote publishing. A push to `main` may trigger separate hosts with **different gates**. Never equate successful GitHub Actions checks with a verified Netlify deployment.

Classify each consequential choice: **required by observed source**, **prohibited by observed source/policy**, **judgment with criteria**, or **unresolved**. Treat historic file names, exact values, expected screenshots, and command aliases as a *reverification index*, not timeless policy.

## 3. Verify before recommending action or declaring completion

- Baseline: capture relevant pre-change failures and current diff; do not attribute existing failures to the proposed change.
- Choose the narrowest reliable checks for the affected contracts. Use the commands documented in the **current** `README.md`, `package.json`, and CI; check installed tool availability before relying on them. Broaden if shared styling/build changes, failed focused checks, or risk justify it.
- Visual change: obtain a failing comparison, inspect expected/actual/diff and article text/charts, then refresh **only confirmed impacted targets** using a command verified against current test names. A baseline refresh is a reviewed change, not a defect fix. Never weaken thresholds or silently enlarge known-defect allowlists to obtain green.
- Content/catalog change: refresh text/metadata fixtures **only when the source change is intentional**, then inspect fixture diffs. Do not run refresh helpers to conceal incidental changes.
- External action: obtain required authority, validate target branch/environment and remote permissions, and verify the resulting remote state via readback. No automatic deploy, merge, publication, or issue creation is authorized by this skill alone.
- After interruption or resumed session, recheck repo state, approvals, and pending verification; do not repeat externally consequential actions without determining whether they already occurred.

## 4. Deliver a bounded Elephant handoff, then stop

Provide: (a) exact repository/ref and local-status confidence; (b) applicable source-of-truth paths and evidence; (c) invariants confirmed versus stale/unverified assumptions; (d) change-impact and regression risks; (e) a per-slice check plan with the snapshot targets/refresh commands **if visual work is proposed**; (f) blockers and permissions; (g) a clear **READY FOR NEXT PHASE**, **BLOCKED**, or **INCONCLUSIVE** conclusion, with reasons.

For an EGM artifact, use the location and format established by the current applicable instructions. If missing, provide the handoff in the conversation without manufacturing an artifact path. Stop once contextual uncertainty is sufficiently reduced; this skill does not own downstream implementation or Goldfish review.
