# Browser review protocol

This is a non-blocking pre-release review for changes that affect shared layout, archive behavior, article framing, metadata presentation, or accessibility. It complements the required Python build and unit suite; it does not alter the deployment gate or require a browser dependency in CI.

## Review slice

Run the current production preview or a local `dist/` preview at 320, 390, 768, 1024, and 1440 CSS pixels. Check the homepage, an archive search and filter combination, one current illustrated article, and one older article.

- Use keyboard-only navigation to reach the navigation, archive controls, result links, article section guide, and related-note links. Verify a visible focus indicator and logical order.
- Check that archive search/filter reset behavior, result count announcement, and URL query parameters remain coherent.
- Confirm reflow without horizontal scrolling, clipped controls, or obscured text at every target viewport.
- Run the existing local browser/axe review only when Chromium is already available. Record new critical or serious findings; do not update a visual baseline merely to clear an unexpected failure.

Record the routes, viewport sizes, date, browser, and any findings in the release handoff. A failed or unavailable browser review is a finding to resolve or explicitly accept, not a reason to weaken the required publication checks.
