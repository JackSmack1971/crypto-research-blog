# Axe accessibility results

Axe ran with WCAG 2.0/2.1 A and AA tags using the installed `@axe-core/playwright`, against local `dist/` served at `127.0.0.1:4173`. Each JSON file contains the raw axe result for that scenario and viewport.

## Violation summary by impact

| Impact | Rule occurrences |
| --- | ---: |
| critical | 0 |
| serious | 7 |
| moderate | 0 |
| minor | 0 |
| unknown | 0 |

## All violations

| Scenario | Viewport | Impact | Rule | Affected nodes | Help |
| --- | ---: | --- | --- | ---: | --- |
| 404 | 1440px | serious | color-contrast | 1 | Elements must meet minimum color contrast ratio thresholds ([raw](axe/404-1440.json)) |
| 404 | 390px | serious | color-contrast | 1 | Elements must meet minimum color contrast ratio thresholds ([raw](axe/404-390.json)) |
| aero-at-0-68 | 390px | serious | scrollable-region-focusable | 1 | Scrollable region must have keyboard access ([raw](axe/aero-at-0-68-390.json)) |
| bitcoin-buying-imbalance | 390px | serious | scrollable-region-focusable | 1 | Scrollable region must have keyboard access ([raw](axe/bitcoin-buying-imbalance-390.json)) |
| token-unlock-liquidity-illusion-90-day-calendar | 1440px | serious | color-contrast | 2 | Elements must meet minimum color contrast ratio thresholds ([raw](axe/token-unlock-liquidity-illusion-90-day-calendar-1440.json)) |
| token-unlock-liquidity-illusion-90-day-calendar | 390px | serious | color-contrast | 2 | Elements must meet minimum color contrast ratio thresholds ([raw](axe/token-unlock-liquidity-illusion-90-day-calendar-390.json)) |
| token-unlock-liquidity-illusion-90-day-calendar | 390px | serious | scrollable-region-focusable | 1 | Scrollable region must have keyboard access ([raw](axe/token-unlock-liquidity-illusion-90-day-calendar-390.json)) |

Scenarios scanned: 20. This is an automated WCAG rule scan, not a full accessibility conformance assessment.

**Provenance and retention:** This summary is derived from the raw inputs `axe/404-1440.json`, `axe/404-390.json`, `axe/aero-at-0-68-1440.json`, `axe/aero-at-0-68-390.json`, `axe/bitcoin-buying-imbalance-1440.json`, `axe/bitcoin-buying-imbalance-390.json`, `axe/home-default-1440.json`, `axe/home-default-390.json`, `axe/home-empty-1440.json`, `axe/home-empty-390.json`, `axe/home-search-btc-1440.json`, `axe/home-search-btc-390.json`, `axe/home-topic-bitcoin-1440.json`, `axe/home-topic-bitcoin-390.json`, `axe/pyth-revenue-unlock-1440.json`, `axe/pyth-revenue-unlock-390.json`, `axe/token-unlock-liquidity-illusion-90-day-calendar-1440.json`, `axe/token-unlock-liquidity-illusion-90-day-calendar-390.json`, `axe/venice-ai-privacy-1440.json`, `axe/venice-ai-privacy-390.json`, and `axe/_run-index.json`. Raw JSON is local-only and ignored by Git.
