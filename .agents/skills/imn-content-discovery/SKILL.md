---
name: imn-content-discovery
description: Evolve Independent Market Notes taxonomy, archive search, navigation, or related-note discovery using explicit editorial criteria. Use when article discovery behavior changes; excludes unilateral taxonomy expansion and automatic ranking publication.
metadata:
  short-description: Improve article discovery
---

# Independent Market Notes content discovery

Use for changes to archive taxonomy, search/filter behavior, article navigation, or related-note selection. Inspect the current catalog, generator, `assets/search.js`, relevant tests, and applicable design decisions. Preserve the approved taxonomy and current archive contracts unless a coordinated taxonomy change is explicitly in scope.

## Keep discovery reviewable

- Preserve title, ticker, dek, and topic matching; combined filters; reset behavior; URL query parameters; empty-results announcement; and article links in initial server HTML.
- Do not silently infer editorial taxonomy from text or expand accepted topics/assets/research types without coordinating generator, UI, tests, fixtures, and editorial conventions.
- For related-note ranking, separate policy choice, editorial acceptance of results, and implementation. First produce a deterministic dry-run candidate list using a clearly stated, reviewable policy. Record the candidate set, eligible-note rules, signal values/weights, result limit, and deterministic tie-break order; include each candidate's signals and reason for ranking, and identify missing/ambiguous metadata. Do not modify published pages or catalog as part of the dry-run.
- Wait for explicit review of both the ranking policy and candidate results before implementing or publishing related-note rankings. A dry-run is evidence for a decision, not the decision itself.

## Verify discovery behavior

For an approved change, check archive links without JavaScript, matching across fields, combined filters, query-string initialization/update, reset, keyboard interaction, empty states, and responsive access as applicable. Run the required Python build/structure checks. Use browser checks only when available and relevant; they are optional local evidence. Report deterministic inputs, outputs, limitations, and unresolved editorial decisions. This skill does not authorize deployment.
