# Change-specific evidence matrix

Use this matrix to plan inspection and checks, not instead of reading the actual implementation and current instructions.

| Change | Inspect | Evidence to consider | Stop condition |
| --- | --- | --- | --- |
| Article/catalog/image | Essay, catalog, generator, signatures/metadata fixtures | Build, Python suite, route/assets/metadata, reviewed fixture diff | Unintended research or catalog mutation |
| Generator/routes/feed | `build.py`, `site.json`, structure tests | Generated routes, relative links, canonical, JSON-LD, RSS/GUID, sitemap | Existing contract changes without scope |
| Archive/search/taxonomy | Catalog, generator, search JS, tests | Initial HTML links, query state, combined filters, reset, keyboard/no-JS | Missing links or changed taxonomy without coordinated scope |
| Shared styling/article rendering | Shared CSS and affected article sources | Content integrity, representative routes/viewports, accessibility/overflow; optional screenshots if available and in scope | Unreviewed visual diff or obscured research content |
| CI/deployment | Exact workflow, `netlify.toml`, README | Conditions, local config checks, separate host readback if authorized | Treating one host/check as proof for another |

## Evidence record

For each change, record objective, inspected paths and Git baseline, affected contract, intended files, exact checks and outcomes, pre-existing failures, optional screenshot targets, and unresolved authority or environment issues. Mark unknown facts unknown. Classify conclusions as required by source, prohibited by source/policy, judgment with criteria, or unresolved.

A test passing after fixture or screenshot refresh is not independent evidence that the refresh was justified. Compare against the intended source change and review the precise baseline diff.
