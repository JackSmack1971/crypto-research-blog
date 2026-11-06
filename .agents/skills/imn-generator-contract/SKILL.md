---
name: imn-generator-contract
description: Modify or review Independent Market Notes build generation, routes, canonical metadata, feeds, or generated output while preserving publishing contracts. Use when work touches build.py or its outputs; excludes article onboarding and deployment execution.
metadata:
  short-description: Preserve generator contracts
---

# Independent Market Notes generator contract

Use when changing or assessing `build.py`, generated routes/chrome, canonical or social metadata, structured data, RSS, sitemap, robots, 404 output, or local-link verification. Read the current `README.md`, applicable instructions, `site.json`, catalog, relevant generator code and tests before proposing changes. Treat `dist/` as derived output; change its sources and regenerate rather than hand-editing it.

## Preserve the relationships

- Keep each article source as the editorial authority. The generator may add framing and metadata but must not silently rewrite article substance or flatten article-specific presentation.
- `site.json.url` supplies canonical HTTPS URLs and public metadata links. `rss_guid_origin` independently maintains stable feed GUID identity. Do not conflate them or change either incidentally.
- Generated internal navigation and local asset references must resolve on both the Netlify origin and GitHub Pages project path. Canonical absolute URLs are appropriate for metadata; root-absolute local paths can break project-site routing.
- Preserve catalog ordering and featured-article selection, route/link verification, JSON-LD semantics, social metadata, RSS, sitemap, robots, 404 output, and legacy no-image behavior unless the requested scope intentionally changes one of these contracts.
- Avoid duplicate structured-data entities or conflicting article-authored social tags. Keep generated metadata derived from catalog and article source.

## Verify affected output

Build from source and inspect generated routes, representative article HTML, links/assets, canonical tags, structured data, feed GUIDs, sitemap, and other outputs implicated by the change. Run the Python suite and inspect focused tests first when useful. Compare source and generated output to distinguish intended wrapper changes from editorial mutations. Report local outcomes separately from hosted CI and deployments; this skill does not authorize remote changes.
