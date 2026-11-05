# Lighthouse results

Audited the live Netlify site (homepage and two article pages) with Lighthouse 12.8.2. Each URL was run in mobile and desktop modes; categories are performance, accessibility, best practices, and SEO. JSON reports preserve full audit detail.

## Category scores

| Page | Mode | Performance | Accessibility | Best practices | SEO |
| --- | --- | ---: | ---: | ---: | ---: |
| bitcoin-buying-imbalance | desktop | 100 | 100 | 100 | 100 |
| bitcoin-buying-imbalance | mobile | 100 | 100 | 100 | 100 |
| home | desktop | 100 | 100 | 100 | 100 |
| home | mobile | 93 | 100 | 100 | 100 |
| newest-token-unlock | desktop | 100 | 96 | 100 | 100 |
| newest-token-unlock | mobile | 93 | 96 | 100 | 100 |

## Core performance metrics

Times are milliseconds; CLS is unitless.

| Report | LCP | FCP | CLS | TBT | Speed Index |
| --- | ---: | ---: | ---: | ---: | ---: |
| [bitcoin-buying-imbalance-desktop.json](lighthouse/bitcoin-buying-imbalance-desktop.json) | 356 | 353 | 0.0009015352267948593 | 0 | 515 |
| [bitcoin-buying-imbalance-mobile.json](lighthouse/bitcoin-buying-imbalance-mobile.json) | 1324 | 1312 | 0.002821569205723791 | 0 | 1493 |
| [home-desktop.json](lighthouse/home-desktop.json) | 492 | 453 | 0.01594695717276665 | 0 | 580 |
| [home-mobile.json](lighthouse/home-mobile.json) | 1865 | 1365 | 0 | 223 | 4254 |
| [newest-token-unlock-desktop.json](lighthouse/newest-token-unlock-desktop.json) | 433 | 326 | 0.0009015352267948593 | 12 | 482 |
| [newest-token-unlock-mobile.json](lighthouse/newest-token-unlock-mobile.json) | 1803 | 1203 | 0 | 229 | 4338 |

## Failed audits

| Report | Failed audit IDs |
| --- | --- |
| [bitcoin-buying-imbalance-desktop.json](lighthouse/bitcoin-buying-imbalance-desktop.json) | forced-reflow-insight, network-dependency-tree-insight |
| [bitcoin-buying-imbalance-mobile.json](lighthouse/bitcoin-buying-imbalance-mobile.json) | forced-reflow-insight, network-dependency-tree-insight |
| [home-desktop.json](lighthouse/home-desktop.json) | forced-reflow-insight, lcp-discovery-insight, network-dependency-tree-insight |
| [home-mobile.json](lighthouse/home-mobile.json) | cache-insight, forced-reflow-insight, image-delivery-insight, lcp-discovery-insight, network-dependency-tree-insight |
| [newest-token-unlock-desktop.json](lighthouse/newest-token-unlock-desktop.json) | color-contrast, cache-insight, forced-reflow-insight, image-delivery-insight, lcp-discovery-insight, network-dependency-tree-insight |
| [newest-token-unlock-mobile.json](lighthouse/newest-token-unlock-mobile.json) | color-contrast, cache-insight, forced-reflow-insight, image-delivery-insight, lcp-discovery-insight, network-dependency-tree-insight |

Lighthouse scores vary with network, browser, and host conditions; these are single-run measurements.

**Provenance and retention:** This summary is derived from `lighthouse/bitcoin-buying-imbalance-desktop.json`, `lighthouse/bitcoin-buying-imbalance-mobile.json`, `lighthouse/home-desktop.json`, `lighthouse/home-mobile.json`, `lighthouse/newest-token-unlock-desktop.json`, `lighthouse/newest-token-unlock-mobile.json`, and `lighthouse/_run-index.json`. Raw Lighthouse JSON and logs are local-only and ignored by Git.
