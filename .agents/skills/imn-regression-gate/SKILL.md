---
name: imn-regression-gate
description: Choose and interpret evidence for Independent Market Notes changes across content, generator, archive, styling, metadata, and deployment configuration. Use when a repository change needs verification; excludes release authorization.
metadata:
  short-description: Match changes to evidence
---

# Independent Market Notes regression gate

Establish the current Git baseline, inspect the changed source and applicable instructions, then map each affected contract to observable evidence. Read the current README, `AGENTS.md`, workflow, and Netlify configuration when implicated; current files outrank this skill's examples.

## Match checks to impact

- Article/catalog/artwork: signatures and metadata fixtures, generated route/assets/metadata, build, and Python suite.
- Generator, canonical, feed, or route behavior: generated output plus route, canonical, JSON-LD, RSS/GUID, sitemap, and structure checks implicated by the change.
- Search/archive/taxonomy: combined filters, URL state, reset and empty state, keyboard use, and initial HTML links without JavaScript; run relevant Python checks.
- Shared styling/article rendering: affected content-integrity checks and, when browser review is in scope and available, representative routes/viewports, accessibility, overflow, and targeted screenshots.
- CI or hosting config: inspect exact workflow conditions and provider config; verify syntax and local checks without claiming hosted results.

The Python suite is the publication gate in this repository; Playwright is optional local evidence, not a substitute or a reason to install browser dependencies for routine publication. Check availability before proposing optional browser checks.

## Interpret, do not game results

Separate pre-existing failures from introduced ones. A failing screenshot requires review of expected, actual, and diff before deciding whether it is a defect or an intended change. Refresh only specifically reviewed targets after an intentional visual change. Refresh content/metadata fixtures only after an intentional source change and inspect the exact diff. Never weaken checks, broaden exceptions, or update baselines just to obtain a pass.

Report each affected contract as passed, failed, blocked, not run, or not applicable, with exact commands and evidence. State limits plainly. A local pass does not establish CI, Netlify, Pages, or live-site success. Verification does not authorize product changes or remote actions.
