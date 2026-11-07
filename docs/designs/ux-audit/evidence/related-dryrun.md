# Slice 4a related-note ranking dry-run

| Variant | Article count |
| --- | ---: |
| related | 27 |
| latest | 0 |
| none | 0 |

Flagged slugs (variant is `latest` or `none`): none

Sanity check: selections from `load_notes()` and raw `content/articles.json` order are identical for every article.

## `when-risk-off-is-not-a-crisis`

- Date: 2026-11-06
- Topic: `market-structure`
- Research type: `investigative-analysis`
- Assets: `BTC`, `ETH`
- Selected variant: `related`
- Sorted candidate order: `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-holding-up`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `bitcoin-selloff-leverage`, `bitcoin-buying-imbalance`, `crypto-market-structure-after-midterms`, `bitcoin-recovery-beneath-resistance`, `bitcoin-rebound-spot-demand`, `monad-november-unlock-liquidity-test`, `token-unlock-liquidity-illusion-90-day-calendar`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `virtual-alpha-risk`, `venice-ai-privacy`, `deepbook-supply-transparency`, `uni-rebound-liquidity-test`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `crypto-buybacks`
- Selected notes: `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`, `bitcoin-quiet-divergence`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `crypto-leverage-liquidity-trap` | 6 | `BTC`, `ETH` | yes | yes |
| 2 | `crypto-chokepoints-november-2026` | 6 | `BTC`, `ETH` | yes | yes |
| 3 | `bitcoin-quiet-divergence` | 5 | `BTC`, `ETH` | yes | no |
| 4 | `crypto-breadth-beneath-bitcoin` | 5 | `BTC`, `ETH` | yes | no |
| 5 | `bitcoin-holding-up` | 4 | `BTC`, `ETH` | no | no |
| 6 | `bitcoin-open-interest-filter-test` | 3 | `BTC` | no | yes |
| 7 | `binance-four-hour-wallet-takeover` | 3 | `ETH` | no | yes |
| 8 | `bitcoin-selloff-leverage` | 3 | `BTC` | yes | no |
| 9 | `bitcoin-buying-imbalance` | 3 | `BTC` | yes | no |
| 10 | `crypto-market-structure-after-midterms` | 2 | none | yes | yes |
| 11 | `bitcoin-recovery-beneath-resistance` | 2 | `BTC` | no | no |
| 12 | `bitcoin-rebound-spot-demand` | 2 | `BTC` | no | no |
| 13 | `monad-november-unlock-liquidity-test` | 1 | none | no | yes |
| 14 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | no | yes |
| 15 | `small-cap-crypto-liquidity-illusion` | 1 | none | no | yes |
| 16 | `solz-launch-investigation` | 1 | none | no | yes |
| 17 | `virtual-alpha-risk` | 1 | none | no | yes |
| 18 | `venice-ai-privacy` | 1 | none | no | yes |
| 19 | `deepbook-supply-transparency` | 0 | none | no | no |
| 20 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 21 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 22 | `aero-at-0-68` | 0 | none | no | no |
| 23 | `weft-first-week` | 0 | none | no | no |
| 24 | `rune-quiet-repricing` | 0 | none | no | no |
| 25 | `pyth-revenue-unlock` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `crypto-leverage-liquidity-trap`

- Date: 2026-11-06
- Topic: `market-structure`
- Research type: `investigative-analysis`
- Assets: `BTC`, `ETH`, `SOL`, `XRP`, `TRX`, `ZEC`, `HYPE`, `USDT`, `USDC`
- Selected variant: `related`
- Sorted candidate order: `crypto-chokepoints-november-2026`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `when-risk-off-is-not-a-crisis`, `bitcoin-holding-up`, `binance-four-hour-wallet-takeover`, `bitcoin-open-interest-filter-test`, `bitcoin-selloff-leverage`, `bitcoin-buying-imbalance`, `crypto-market-structure-after-midterms`, `bitcoin-recovery-beneath-resistance`, `bitcoin-rebound-spot-demand`, `monad-november-unlock-liquidity-test`, `token-unlock-liquidity-illusion-90-day-calendar`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `virtual-alpha-risk`, `venice-ai-privacy`, `deepbook-supply-transparency`, `uni-rebound-liquidity-test`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `crypto-buybacks`
- Selected notes: `crypto-chokepoints-november-2026`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `crypto-chokepoints-november-2026` | 10 | `BTC`, `ETH`, `USDC`, `USDT` | yes | yes |
| 2 | `bitcoin-quiet-divergence` | 7 | `BTC`, `ETH`, `SOL` | yes | no |
| 3 | `crypto-breadth-beneath-bitcoin` | 7 | `BTC`, `ETH`, `SOL` | yes | no |
| 4 | `when-risk-off-is-not-a-crisis` | 6 | `BTC`, `ETH` | yes | yes |
| 5 | `bitcoin-holding-up` | 6 | `BTC`, `ETH`, `SOL` | no | no |
| 6 | `binance-four-hour-wallet-takeover` | 5 | `ETH`, `USDT` | no | yes |
| 7 | `bitcoin-open-interest-filter-test` | 3 | `BTC` | no | yes |
| 8 | `bitcoin-selloff-leverage` | 3 | `BTC` | yes | no |
| 9 | `bitcoin-buying-imbalance` | 3 | `BTC` | yes | no |
| 10 | `crypto-market-structure-after-midterms` | 2 | none | yes | yes |
| 11 | `bitcoin-recovery-beneath-resistance` | 2 | `BTC` | no | no |
| 12 | `bitcoin-rebound-spot-demand` | 2 | `BTC` | no | no |
| 13 | `monad-november-unlock-liquidity-test` | 1 | none | no | yes |
| 14 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | no | yes |
| 15 | `small-cap-crypto-liquidity-illusion` | 1 | none | no | yes |
| 16 | `solz-launch-investigation` | 1 | none | no | yes |
| 17 | `virtual-alpha-risk` | 1 | none | no | yes |
| 18 | `venice-ai-privacy` | 1 | none | no | yes |
| 19 | `deepbook-supply-transparency` | 0 | none | no | no |
| 20 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 21 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 22 | `aero-at-0-68` | 0 | none | no | no |
| 23 | `weft-first-week` | 0 | none | no | no |
| 24 | `rune-quiet-repricing` | 0 | none | no | no |
| 25 | `pyth-revenue-unlock` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `monad-november-unlock-liquidity-test`

- Date: 2026-11-05
- Topic: `tokenomics`
- Research type: `investigative-analysis`
- Assets: `MON`
- Selected variant: `related`
- Sorted candidate order: `token-unlock-liquidity-illusion-90-day-calendar`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `crypto-chokepoints-november-2026`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `aero-at-0-68`, `weft-first-week`, `virtual-alpha-risk`, `pyth-revenue-unlock`, `venice-ai-privacy`, `crypto-buybacks`, `deepbook-supply-transparency`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `institutional-adoption-token-demand`, `bitcoin-holding-up`, `bitcoin-buying-imbalance`, `rune-quiet-repricing`
- Selected notes: `token-unlock-liquidity-illusion-90-day-calendar`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `token-unlock-liquidity-illusion-90-day-calendar` | 4 | `MON` | yes | yes |
| 2 | `when-risk-off-is-not-a-crisis` | 1 | none | no | yes |
| 3 | `crypto-leverage-liquidity-trap` | 1 | none | no | yes |
| 4 | `crypto-market-structure-after-midterms` | 1 | none | no | yes |
| 5 | `bitcoin-open-interest-filter-test` | 1 | none | no | yes |
| 6 | `binance-four-hour-wallet-takeover` | 1 | none | no | yes |
| 7 | `crypto-chokepoints-november-2026` | 1 | none | no | yes |
| 8 | `small-cap-crypto-liquidity-illusion` | 1 | none | no | yes |
| 9 | `solz-launch-investigation` | 1 | none | no | yes |
| 10 | `aero-at-0-68` | 1 | none | yes | no |
| 11 | `weft-first-week` | 1 | none | yes | no |
| 12 | `virtual-alpha-risk` | 1 | none | no | yes |
| 13 | `pyth-revenue-unlock` | 1 | none | yes | no |
| 14 | `venice-ai-privacy` | 1 | none | no | yes |
| 15 | `crypto-buybacks` | 1 | none | yes | no |
| 16 | `deepbook-supply-transparency` | 0 | none | no | no |
| 17 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 18 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 19 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 20 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 21 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 22 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 23 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 24 | `bitcoin-holding-up` | 0 | none | no | no |
| 25 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 26 | `rune-quiet-repricing` | 0 | none | no | no |

---

## `crypto-market-structure-after-midterms`

- Date: 2026-11-04
- Topic: `market-structure`
- Research type: `investigative-analysis`
- Assets: none
- Selected variant: `related`
- Sorted candidate order: `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`, `monad-november-unlock-liquidity-test`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `token-unlock-liquidity-illusion-90-day-calendar`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `small-cap-crypto-liquidity-illusion`, `bitcoin-selloff-leverage`, `solz-launch-investigation`, `bitcoin-buying-imbalance`, `virtual-alpha-risk`, `venice-ai-privacy`, `deepbook-supply-transparency`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-rebound-spot-demand`, `institutional-adoption-token-demand`, `bitcoin-holding-up`, `aero-at-0-68`, `weft-first-week`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `crypto-buybacks`
- Selected notes: `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `when-risk-off-is-not-a-crisis` | 2 | none | yes | yes |
| 2 | `crypto-leverage-liquidity-trap` | 2 | none | yes | yes |
| 3 | `crypto-chokepoints-november-2026` | 2 | none | yes | yes |
| 4 | `monad-november-unlock-liquidity-test` | 1 | none | no | yes |
| 5 | `bitcoin-open-interest-filter-test` | 1 | none | no | yes |
| 6 | `binance-four-hour-wallet-takeover` | 1 | none | no | yes |
| 7 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | no | yes |
| 8 | `bitcoin-quiet-divergence` | 1 | none | yes | no |
| 9 | `crypto-breadth-beneath-bitcoin` | 1 | none | yes | no |
| 10 | `small-cap-crypto-liquidity-illusion` | 1 | none | no | yes |
| 11 | `bitcoin-selloff-leverage` | 1 | none | yes | no |
| 12 | `solz-launch-investigation` | 1 | none | no | yes |
| 13 | `bitcoin-buying-imbalance` | 1 | none | yes | no |
| 14 | `virtual-alpha-risk` | 1 | none | no | yes |
| 15 | `venice-ai-privacy` | 1 | none | no | yes |
| 16 | `deepbook-supply-transparency` | 0 | none | no | no |
| 17 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 18 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 19 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 20 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 21 | `bitcoin-holding-up` | 0 | none | no | no |
| 22 | `aero-at-0-68` | 0 | none | no | no |
| 23 | `weft-first-week` | 0 | none | no | no |
| 24 | `rune-quiet-repricing` | 0 | none | no | no |
| 25 | `pyth-revenue-unlock` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `bitcoin-open-interest-filter-test`

- Date: 2026-11-04
- Topic: `bitcoin`
- Research type: `investigative-analysis`
- Assets: `BTC`
- Selected variant: `related`
- Sorted candidate order: `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`, `bitcoin-recovery-beneath-resistance`, `bitcoin-rebound-spot-demand`, `bitcoin-holding-up`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-selloff-leverage`, `bitcoin-buying-imbalance`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `binance-four-hour-wallet-takeover`, `token-unlock-liquidity-illusion-90-day-calendar`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `virtual-alpha-risk`, `venice-ai-privacy`, `deepbook-supply-transparency`, `uni-rebound-liquidity-test`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `crypto-buybacks`
- Selected notes: `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `when-risk-off-is-not-a-crisis` | 3 | `BTC` | no | yes |
| 2 | `crypto-leverage-liquidity-trap` | 3 | `BTC` | no | yes |
| 3 | `crypto-chokepoints-november-2026` | 3 | `BTC` | no | yes |
| 4 | `bitcoin-recovery-beneath-resistance` | 3 | `BTC` | yes | no |
| 5 | `bitcoin-rebound-spot-demand` | 3 | `BTC` | yes | no |
| 6 | `bitcoin-holding-up` | 3 | `BTC` | yes | no |
| 7 | `bitcoin-quiet-divergence` | 2 | `BTC` | no | no |
| 8 | `crypto-breadth-beneath-bitcoin` | 2 | `BTC` | no | no |
| 9 | `bitcoin-selloff-leverage` | 2 | `BTC` | no | no |
| 10 | `bitcoin-buying-imbalance` | 2 | `BTC` | no | no |
| 11 | `monad-november-unlock-liquidity-test` | 1 | none | no | yes |
| 12 | `crypto-market-structure-after-midterms` | 1 | none | no | yes |
| 13 | `binance-four-hour-wallet-takeover` | 1 | none | no | yes |
| 14 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | no | yes |
| 15 | `small-cap-crypto-liquidity-illusion` | 1 | none | no | yes |
| 16 | `solz-launch-investigation` | 1 | none | no | yes |
| 17 | `virtual-alpha-risk` | 1 | none | no | yes |
| 18 | `venice-ai-privacy` | 1 | none | no | yes |
| 19 | `deepbook-supply-transparency` | 0 | none | no | no |
| 20 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 21 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 22 | `aero-at-0-68` | 0 | none | no | no |
| 23 | `weft-first-week` | 0 | none | no | no |
| 24 | `rune-quiet-repricing` | 0 | none | no | no |
| 25 | `pyth-revenue-unlock` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `binance-four-hour-wallet-takeover`

- Date: 2026-11-04
- Topic: `risk-verification`
- Research type: `investigative-analysis`
- Assets: `ETH`, `USDT`, `RLUSD`, `WBETH`, `XAUT`, `UNI`
- Selected variant: `related`
- Sorted candidate order: `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`, `when-risk-off-is-not-a-crisis`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `solz-launch-investigation`, `bitcoin-holding-up`, `virtual-alpha-risk`, `venice-ai-privacy`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `token-unlock-liquidity-illusion-90-day-calendar`, `small-cap-crypto-liquidity-illusion`, `deepbook-supply-transparency`, `bitcoin-recovery-beneath-resistance`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `institutional-adoption-token-demand`, `aero-at-0-68`, `bitcoin-buying-imbalance`, `weft-first-week`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `crypto-buybacks`
- Selected notes: `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`, `when-risk-off-is-not-a-crisis`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `crypto-leverage-liquidity-trap` | 5 | `ETH`, `USDT` | no | yes |
| 2 | `crypto-chokepoints-november-2026` | 5 | `ETH`, `USDT` | no | yes |
| 3 | `when-risk-off-is-not-a-crisis` | 3 | `ETH` | no | yes |
| 4 | `uni-rebound-liquidity-test` | 2 | `UNI` | no | no |
| 5 | `bitcoin-quiet-divergence` | 2 | `ETH` | no | no |
| 6 | `crypto-breadth-beneath-bitcoin` | 2 | `ETH` | no | no |
| 7 | `solz-launch-investigation` | 2 | none | yes | yes |
| 8 | `bitcoin-holding-up` | 2 | `ETH` | no | no |
| 9 | `virtual-alpha-risk` | 2 | none | yes | yes |
| 10 | `venice-ai-privacy` | 2 | none | yes | yes |
| 11 | `monad-november-unlock-liquidity-test` | 1 | none | no | yes |
| 12 | `crypto-market-structure-after-midterms` | 1 | none | no | yes |
| 13 | `bitcoin-open-interest-filter-test` | 1 | none | no | yes |
| 14 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | no | yes |
| 15 | `small-cap-crypto-liquidity-illusion` | 1 | none | no | yes |
| 16 | `deepbook-supply-transparency` | 0 | none | no | no |
| 17 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 18 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 19 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 20 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 21 | `aero-at-0-68` | 0 | none | no | no |
| 22 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 23 | `weft-first-week` | 0 | none | no | no |
| 24 | `rune-quiet-repricing` | 0 | none | no | no |
| 25 | `pyth-revenue-unlock` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `crypto-chokepoints-november-2026`

- Date: 2026-11-04
- Topic: `market-structure`
- Research type: `investigative-analysis`
- Assets: `BTC`, `ETH`, `USDT`, `USDC`, `INJ`, `ENA`
- Selected variant: `related`
- Sorted candidate order: `crypto-leverage-liquidity-trap`, `when-risk-off-is-not-a-crisis`, `binance-four-hour-wallet-takeover`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-holding-up`, `bitcoin-open-interest-filter-test`, `token-unlock-liquidity-illusion-90-day-calendar`, `bitcoin-selloff-leverage`, `bitcoin-buying-imbalance`, `crypto-market-structure-after-midterms`, `bitcoin-recovery-beneath-resistance`, `bitcoin-rebound-spot-demand`, `monad-november-unlock-liquidity-test`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `virtual-alpha-risk`, `venice-ai-privacy`, `deepbook-supply-transparency`, `uni-rebound-liquidity-test`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `crypto-buybacks`
- Selected notes: `crypto-leverage-liquidity-trap`, `when-risk-off-is-not-a-crisis`, `binance-four-hour-wallet-takeover`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `crypto-leverage-liquidity-trap` | 10 | `BTC`, `ETH`, `USDC`, `USDT` | yes | yes |
| 2 | `when-risk-off-is-not-a-crisis` | 6 | `BTC`, `ETH` | yes | yes |
| 3 | `binance-four-hour-wallet-takeover` | 5 | `ETH`, `USDT` | no | yes |
| 4 | `bitcoin-quiet-divergence` | 5 | `BTC`, `ETH` | yes | no |
| 5 | `crypto-breadth-beneath-bitcoin` | 5 | `BTC`, `ETH` | yes | no |
| 6 | `bitcoin-holding-up` | 4 | `BTC`, `ETH` | no | no |
| 7 | `bitcoin-open-interest-filter-test` | 3 | `BTC` | no | yes |
| 8 | `token-unlock-liquidity-illusion-90-day-calendar` | 3 | `ENA` | no | yes |
| 9 | `bitcoin-selloff-leverage` | 3 | `BTC` | yes | no |
| 10 | `bitcoin-buying-imbalance` | 3 | `BTC` | yes | no |
| 11 | `crypto-market-structure-after-midterms` | 2 | none | yes | yes |
| 12 | `bitcoin-recovery-beneath-resistance` | 2 | `BTC` | no | no |
| 13 | `bitcoin-rebound-spot-demand` | 2 | `BTC` | no | no |
| 14 | `monad-november-unlock-liquidity-test` | 1 | none | no | yes |
| 15 | `small-cap-crypto-liquidity-illusion` | 1 | none | no | yes |
| 16 | `solz-launch-investigation` | 1 | none | no | yes |
| 17 | `virtual-alpha-risk` | 1 | none | no | yes |
| 18 | `venice-ai-privacy` | 1 | none | no | yes |
| 19 | `deepbook-supply-transparency` | 0 | none | no | no |
| 20 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 21 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 22 | `aero-at-0-68` | 0 | none | no | no |
| 23 | `weft-first-week` | 0 | none | no | no |
| 24 | `rune-quiet-repricing` | 0 | none | no | no |
| 25 | `pyth-revenue-unlock` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `token-unlock-liquidity-illusion-90-day-calendar`

- Date: 2026-11-03
- Topic: `tokenomics`
- Research type: `investigative-analysis`
- Assets: `MON`, `ONDO`, `APT`, `ARB`, `ENA`, `STRK`, `ZRO`, `SEI`
- Selected variant: `related`
- Sorted candidate order: `monad-november-unlock-liquidity-test`, `crypto-chokepoints-november-2026`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `aero-at-0-68`, `weft-first-week`, `virtual-alpha-risk`, `pyth-revenue-unlock`, `venice-ai-privacy`, `crypto-buybacks`, `deepbook-supply-transparency`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `institutional-adoption-token-demand`, `bitcoin-holding-up`, `bitcoin-buying-imbalance`, `rune-quiet-repricing`
- Selected notes: `monad-november-unlock-liquidity-test`, `crypto-chokepoints-november-2026`, `when-risk-off-is-not-a-crisis`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `monad-november-unlock-liquidity-test` | 4 | `MON` | yes | yes |
| 2 | `crypto-chokepoints-november-2026` | 3 | `ENA` | no | yes |
| 3 | `when-risk-off-is-not-a-crisis` | 1 | none | no | yes |
| 4 | `crypto-leverage-liquidity-trap` | 1 | none | no | yes |
| 5 | `crypto-market-structure-after-midterms` | 1 | none | no | yes |
| 6 | `bitcoin-open-interest-filter-test` | 1 | none | no | yes |
| 7 | `binance-four-hour-wallet-takeover` | 1 | none | no | yes |
| 8 | `small-cap-crypto-liquidity-illusion` | 1 | none | no | yes |
| 9 | `solz-launch-investigation` | 1 | none | no | yes |
| 10 | `aero-at-0-68` | 1 | none | yes | no |
| 11 | `weft-first-week` | 1 | none | yes | no |
| 12 | `virtual-alpha-risk` | 1 | none | no | yes |
| 13 | `pyth-revenue-unlock` | 1 | none | yes | no |
| 14 | `venice-ai-privacy` | 1 | none | no | yes |
| 15 | `crypto-buybacks` | 1 | none | yes | no |
| 16 | `deepbook-supply-transparency` | 0 | none | no | no |
| 17 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 18 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 19 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 20 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 21 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 22 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 23 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 24 | `bitcoin-holding-up` | 0 | none | no | no |
| 25 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 26 | `rune-quiet-repricing` | 0 | none | no | no |

---

## `deepbook-supply-transparency`

- Date: 2026-11-03
- Topic: `protocol-research`
- Research type: `token-due-diligence`
- Assets: `DEEP`
- Selected variant: `related`
- Sorted candidate order: `institutional-adoption-token-demand`, `rune-quiet-repricing`, `aero-at-0-68`, `weft-first-week`, `pyth-revenue-unlock`, `crypto-buybacks`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `crypto-chokepoints-november-2026`, `token-unlock-liquidity-illusion-90-day-calendar`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `small-cap-crypto-liquidity-illusion`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `solz-launch-investigation`, `bitcoin-holding-up`, `bitcoin-buying-imbalance`, `virtual-alpha-risk`, `venice-ai-privacy`
- Selected notes: `institutional-adoption-token-demand`, `rune-quiet-repricing`, `aero-at-0-68`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `institutional-adoption-token-demand` | 2 | none | yes | yes |
| 2 | `rune-quiet-repricing` | 2 | none | yes | yes |
| 3 | `aero-at-0-68` | 1 | none | no | yes |
| 4 | `weft-first-week` | 1 | none | no | yes |
| 5 | `pyth-revenue-unlock` | 1 | none | no | yes |
| 6 | `crypto-buybacks` | 1 | none | no | yes |
| 7 | `when-risk-off-is-not-a-crisis` | 0 | none | no | no |
| 8 | `crypto-leverage-liquidity-trap` | 0 | none | no | no |
| 9 | `monad-november-unlock-liquidity-test` | 0 | none | no | no |
| 10 | `crypto-market-structure-after-midterms` | 0 | none | no | no |
| 11 | `bitcoin-open-interest-filter-test` | 0 | none | no | no |
| 12 | `binance-four-hour-wallet-takeover` | 0 | none | no | no |
| 13 | `crypto-chokepoints-november-2026` | 0 | none | no | no |
| 14 | `token-unlock-liquidity-illusion-90-day-calendar` | 0 | none | no | no |
| 15 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 16 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 17 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 18 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 19 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 20 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 21 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 22 | `solz-launch-investigation` | 0 | none | no | no |
| 23 | `bitcoin-holding-up` | 0 | none | no | no |
| 24 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 25 | `virtual-alpha-risk` | 0 | none | no | no |
| 26 | `venice-ai-privacy` | 0 | none | no | no |

---

## `bitcoin-recovery-beneath-resistance`

- Date: 2026-11-03
- Topic: `bitcoin`
- Research type: `market-snapshot`
- Assets: `BTC`
- Selected variant: `related`
- Sorted candidate order: `bitcoin-rebound-spot-demand`, `bitcoin-holding-up`, `bitcoin-open-interest-filter-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-selloff-leverage`, `bitcoin-buying-imbalance`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`, `uni-rebound-liquidity-test`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `binance-four-hour-wallet-takeover`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `virtual-alpha-risk`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `venice-ai-privacy`, `crypto-buybacks`
- Selected notes: `bitcoin-rebound-spot-demand`, `bitcoin-holding-up`, `bitcoin-open-interest-filter-test`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `bitcoin-rebound-spot-demand` | 4 | `BTC` | yes | yes |
| 2 | `bitcoin-holding-up` | 4 | `BTC` | yes | yes |
| 3 | `bitcoin-open-interest-filter-test` | 3 | `BTC` | yes | no |
| 4 | `bitcoin-quiet-divergence` | 3 | `BTC` | no | yes |
| 5 | `crypto-breadth-beneath-bitcoin` | 3 | `BTC` | no | yes |
| 6 | `bitcoin-selloff-leverage` | 3 | `BTC` | no | yes |
| 7 | `bitcoin-buying-imbalance` | 3 | `BTC` | no | yes |
| 8 | `when-risk-off-is-not-a-crisis` | 2 | `BTC` | no | no |
| 9 | `crypto-leverage-liquidity-trap` | 2 | `BTC` | no | no |
| 10 | `crypto-chokepoints-november-2026` | 2 | `BTC` | no | no |
| 11 | `uni-rebound-liquidity-test` | 1 | none | no | yes |
| 12 | `monad-november-unlock-liquidity-test` | 0 | none | no | no |
| 13 | `crypto-market-structure-after-midterms` | 0 | none | no | no |
| 14 | `binance-four-hour-wallet-takeover` | 0 | none | no | no |
| 15 | `token-unlock-liquidity-illusion-90-day-calendar` | 0 | none | no | no |
| 16 | `deepbook-supply-transparency` | 0 | none | no | no |
| 17 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 18 | `solz-launch-investigation` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `aero-at-0-68` | 0 | none | no | no |
| 21 | `weft-first-week` | 0 | none | no | no |
| 22 | `virtual-alpha-risk` | 0 | none | no | no |
| 23 | `rune-quiet-repricing` | 0 | none | no | no |
| 24 | `pyth-revenue-unlock` | 0 | none | no | no |
| 25 | `venice-ai-privacy` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `uni-rebound-liquidity-test`

- Date: 2026-11-02
- Topic: `liquidity`
- Research type: `market-snapshot`
- Assets: `UNI`
- Selected variant: `related`
- Sorted candidate order: `binance-four-hour-wallet-takeover`, `bitcoin-recovery-beneath-resistance`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `small-cap-crypto-liquidity-illusion`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `bitcoin-holding-up`, `bitcoin-buying-imbalance`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `crypto-chokepoints-november-2026`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `solz-launch-investigation`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `virtual-alpha-risk`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `venice-ai-privacy`, `crypto-buybacks`
- Selected notes: `binance-four-hour-wallet-takeover`, `bitcoin-recovery-beneath-resistance`, `bitcoin-quiet-divergence`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `binance-four-hour-wallet-takeover` | 2 | `UNI` | no | no |
| 2 | `bitcoin-recovery-beneath-resistance` | 1 | none | no | yes |
| 3 | `bitcoin-quiet-divergence` | 1 | none | no | yes |
| 4 | `crypto-breadth-beneath-bitcoin` | 1 | none | no | yes |
| 5 | `small-cap-crypto-liquidity-illusion` | 1 | none | yes | no |
| 6 | `bitcoin-rebound-spot-demand` | 1 | none | no | yes |
| 7 | `bitcoin-selloff-leverage` | 1 | none | no | yes |
| 8 | `bitcoin-holding-up` | 1 | none | no | yes |
| 9 | `bitcoin-buying-imbalance` | 1 | none | no | yes |
| 10 | `when-risk-off-is-not-a-crisis` | 0 | none | no | no |
| 11 | `crypto-leverage-liquidity-trap` | 0 | none | no | no |
| 12 | `monad-november-unlock-liquidity-test` | 0 | none | no | no |
| 13 | `crypto-market-structure-after-midterms` | 0 | none | no | no |
| 14 | `bitcoin-open-interest-filter-test` | 0 | none | no | no |
| 15 | `crypto-chokepoints-november-2026` | 0 | none | no | no |
| 16 | `token-unlock-liquidity-illusion-90-day-calendar` | 0 | none | no | no |
| 17 | `deepbook-supply-transparency` | 0 | none | no | no |
| 18 | `solz-launch-investigation` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `aero-at-0-68` | 0 | none | no | no |
| 21 | `weft-first-week` | 0 | none | no | no |
| 22 | `virtual-alpha-risk` | 0 | none | no | no |
| 23 | `rune-quiet-repricing` | 0 | none | no | no |
| 24 | `pyth-revenue-unlock` | 0 | none | no | no |
| 25 | `venice-ai-privacy` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `bitcoin-quiet-divergence`

- Date: 2026-11-02
- Topic: `market-structure`
- Research type: `market-snapshot`
- Assets: `BTC`, `ETH`, `SOL`
- Selected variant: `related`
- Sorted candidate order: `crypto-breadth-beneath-bitcoin`, `crypto-leverage-liquidity-trap`, `bitcoin-holding-up`, `when-risk-off-is-not-a-crisis`, `crypto-chokepoints-november-2026`, `bitcoin-selloff-leverage`, `bitcoin-buying-imbalance`, `bitcoin-recovery-beneath-resistance`, `bitcoin-rebound-spot-demand`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `crypto-market-structure-after-midterms`, `uni-rebound-liquidity-test`, `monad-november-unlock-liquidity-test`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `virtual-alpha-risk`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `venice-ai-privacy`, `crypto-buybacks`
- Selected notes: `crypto-breadth-beneath-bitcoin`, `crypto-leverage-liquidity-trap`, `bitcoin-holding-up`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `crypto-breadth-beneath-bitcoin` | 8 | `BTC`, `ETH`, `SOL` | yes | yes |
| 2 | `crypto-leverage-liquidity-trap` | 7 | `BTC`, `ETH`, `SOL` | yes | no |
| 3 | `bitcoin-holding-up` | 7 | `BTC`, `ETH`, `SOL` | no | yes |
| 4 | `when-risk-off-is-not-a-crisis` | 5 | `BTC`, `ETH` | yes | no |
| 5 | `crypto-chokepoints-november-2026` | 5 | `BTC`, `ETH` | yes | no |
| 6 | `bitcoin-selloff-leverage` | 4 | `BTC` | yes | yes |
| 7 | `bitcoin-buying-imbalance` | 4 | `BTC` | yes | yes |
| 8 | `bitcoin-recovery-beneath-resistance` | 3 | `BTC` | no | yes |
| 9 | `bitcoin-rebound-spot-demand` | 3 | `BTC` | no | yes |
| 10 | `bitcoin-open-interest-filter-test` | 2 | `BTC` | no | no |
| 11 | `binance-four-hour-wallet-takeover` | 2 | `ETH` | no | no |
| 12 | `crypto-market-structure-after-midterms` | 1 | none | yes | no |
| 13 | `uni-rebound-liquidity-test` | 1 | none | no | yes |
| 14 | `monad-november-unlock-liquidity-test` | 0 | none | no | no |
| 15 | `token-unlock-liquidity-illusion-90-day-calendar` | 0 | none | no | no |
| 16 | `deepbook-supply-transparency` | 0 | none | no | no |
| 17 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 18 | `solz-launch-investigation` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `aero-at-0-68` | 0 | none | no | no |
| 21 | `weft-first-week` | 0 | none | no | no |
| 22 | `virtual-alpha-risk` | 0 | none | no | no |
| 23 | `rune-quiet-repricing` | 0 | none | no | no |
| 24 | `pyth-revenue-unlock` | 0 | none | no | no |
| 25 | `venice-ai-privacy` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `crypto-breadth-beneath-bitcoin`

- Date: 2026-11-01
- Topic: `market-structure`
- Research type: `market-snapshot`
- Assets: `BTC`, `ETH`, `SOL`
- Selected variant: `related`
- Sorted candidate order: `bitcoin-quiet-divergence`, `crypto-leverage-liquidity-trap`, `bitcoin-holding-up`, `when-risk-off-is-not-a-crisis`, `crypto-chokepoints-november-2026`, `bitcoin-selloff-leverage`, `bitcoin-buying-imbalance`, `bitcoin-recovery-beneath-resistance`, `bitcoin-rebound-spot-demand`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `crypto-market-structure-after-midterms`, `uni-rebound-liquidity-test`, `monad-november-unlock-liquidity-test`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `virtual-alpha-risk`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `venice-ai-privacy`, `crypto-buybacks`
- Selected notes: `bitcoin-quiet-divergence`, `crypto-leverage-liquidity-trap`, `bitcoin-holding-up`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `bitcoin-quiet-divergence` | 8 | `BTC`, `ETH`, `SOL` | yes | yes |
| 2 | `crypto-leverage-liquidity-trap` | 7 | `BTC`, `ETH`, `SOL` | yes | no |
| 3 | `bitcoin-holding-up` | 7 | `BTC`, `ETH`, `SOL` | no | yes |
| 4 | `when-risk-off-is-not-a-crisis` | 5 | `BTC`, `ETH` | yes | no |
| 5 | `crypto-chokepoints-november-2026` | 5 | `BTC`, `ETH` | yes | no |
| 6 | `bitcoin-selloff-leverage` | 4 | `BTC` | yes | yes |
| 7 | `bitcoin-buying-imbalance` | 4 | `BTC` | yes | yes |
| 8 | `bitcoin-recovery-beneath-resistance` | 3 | `BTC` | no | yes |
| 9 | `bitcoin-rebound-spot-demand` | 3 | `BTC` | no | yes |
| 10 | `bitcoin-open-interest-filter-test` | 2 | `BTC` | no | no |
| 11 | `binance-four-hour-wallet-takeover` | 2 | `ETH` | no | no |
| 12 | `crypto-market-structure-after-midterms` | 1 | none | yes | no |
| 13 | `uni-rebound-liquidity-test` | 1 | none | no | yes |
| 14 | `monad-november-unlock-liquidity-test` | 0 | none | no | no |
| 15 | `token-unlock-liquidity-illusion-90-day-calendar` | 0 | none | no | no |
| 16 | `deepbook-supply-transparency` | 0 | none | no | no |
| 17 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 18 | `solz-launch-investigation` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `aero-at-0-68` | 0 | none | no | no |
| 21 | `weft-first-week` | 0 | none | no | no |
| 22 | `virtual-alpha-risk` | 0 | none | no | no |
| 23 | `rune-quiet-repricing` | 0 | none | no | no |
| 24 | `pyth-revenue-unlock` | 0 | none | no | no |
| 25 | `venice-ai-privacy` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `small-cap-crypto-liquidity-illusion`

- Date: 2026-11-01
- Topic: `liquidity`
- Research type: `investigative-analysis`
- Assets: `FLOAT`, `LEVERHEDGE`, `NETWORK`, `SAFU`, `DACITYCOIN`
- Selected variant: `related`
- Sorted candidate order: `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `crypto-chokepoints-november-2026`, `token-unlock-liquidity-illusion-90-day-calendar`, `uni-rebound-liquidity-test`, `solz-launch-investigation`, `virtual-alpha-risk`, `venice-ai-privacy`, `deepbook-supply-transparency`, `bitcoin-recovery-beneath-resistance`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `institutional-adoption-token-demand`, `bitcoin-holding-up`, `aero-at-0-68`, `bitcoin-buying-imbalance`, `weft-first-week`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `crypto-buybacks`
- Selected notes: `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `monad-november-unlock-liquidity-test`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `when-risk-off-is-not-a-crisis` | 1 | none | no | yes |
| 2 | `crypto-leverage-liquidity-trap` | 1 | none | no | yes |
| 3 | `monad-november-unlock-liquidity-test` | 1 | none | no | yes |
| 4 | `crypto-market-structure-after-midterms` | 1 | none | no | yes |
| 5 | `bitcoin-open-interest-filter-test` | 1 | none | no | yes |
| 6 | `binance-four-hour-wallet-takeover` | 1 | none | no | yes |
| 7 | `crypto-chokepoints-november-2026` | 1 | none | no | yes |
| 8 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | no | yes |
| 9 | `uni-rebound-liquidity-test` | 1 | none | yes | no |
| 10 | `solz-launch-investigation` | 1 | none | no | yes |
| 11 | `virtual-alpha-risk` | 1 | none | no | yes |
| 12 | `venice-ai-privacy` | 1 | none | no | yes |
| 13 | `deepbook-supply-transparency` | 0 | none | no | no |
| 14 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 15 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 16 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 17 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 18 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `bitcoin-holding-up` | 0 | none | no | no |
| 21 | `aero-at-0-68` | 0 | none | no | no |
| 22 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 23 | `weft-first-week` | 0 | none | no | no |
| 24 | `rune-quiet-repricing` | 0 | none | no | no |
| 25 | `pyth-revenue-unlock` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `bitcoin-rebound-spot-demand`

- Date: 2026-11-01
- Topic: `bitcoin`
- Research type: `market-snapshot`
- Assets: `BTC`
- Selected variant: `related`
- Sorted candidate order: `bitcoin-recovery-beneath-resistance`, `bitcoin-holding-up`, `bitcoin-open-interest-filter-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-selloff-leverage`, `bitcoin-buying-imbalance`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`, `uni-rebound-liquidity-test`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `binance-four-hour-wallet-takeover`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `virtual-alpha-risk`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `venice-ai-privacy`, `crypto-buybacks`
- Selected notes: `bitcoin-recovery-beneath-resistance`, `bitcoin-holding-up`, `bitcoin-open-interest-filter-test`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `bitcoin-recovery-beneath-resistance` | 4 | `BTC` | yes | yes |
| 2 | `bitcoin-holding-up` | 4 | `BTC` | yes | yes |
| 3 | `bitcoin-open-interest-filter-test` | 3 | `BTC` | yes | no |
| 4 | `bitcoin-quiet-divergence` | 3 | `BTC` | no | yes |
| 5 | `crypto-breadth-beneath-bitcoin` | 3 | `BTC` | no | yes |
| 6 | `bitcoin-selloff-leverage` | 3 | `BTC` | no | yes |
| 7 | `bitcoin-buying-imbalance` | 3 | `BTC` | no | yes |
| 8 | `when-risk-off-is-not-a-crisis` | 2 | `BTC` | no | no |
| 9 | `crypto-leverage-liquidity-trap` | 2 | `BTC` | no | no |
| 10 | `crypto-chokepoints-november-2026` | 2 | `BTC` | no | no |
| 11 | `uni-rebound-liquidity-test` | 1 | none | no | yes |
| 12 | `monad-november-unlock-liquidity-test` | 0 | none | no | no |
| 13 | `crypto-market-structure-after-midterms` | 0 | none | no | no |
| 14 | `binance-four-hour-wallet-takeover` | 0 | none | no | no |
| 15 | `token-unlock-liquidity-illusion-90-day-calendar` | 0 | none | no | no |
| 16 | `deepbook-supply-transparency` | 0 | none | no | no |
| 17 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 18 | `solz-launch-investigation` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `aero-at-0-68` | 0 | none | no | no |
| 21 | `weft-first-week` | 0 | none | no | no |
| 22 | `virtual-alpha-risk` | 0 | none | no | no |
| 23 | `rune-quiet-repricing` | 0 | none | no | no |
| 24 | `pyth-revenue-unlock` | 0 | none | no | no |
| 25 | `venice-ai-privacy` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `bitcoin-selloff-leverage`

- Date: 2026-10-29
- Topic: `market-structure`
- Research type: `market-snapshot`
- Assets: `BTC`
- Selected variant: `related`
- Sorted candidate order: `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-buying-imbalance`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`, `bitcoin-recovery-beneath-resistance`, `bitcoin-rebound-spot-demand`, `bitcoin-holding-up`, `bitcoin-open-interest-filter-test`, `crypto-market-structure-after-midterms`, `uni-rebound-liquidity-test`, `monad-november-unlock-liquidity-test`, `binance-four-hour-wallet-takeover`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `virtual-alpha-risk`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `venice-ai-privacy`, `crypto-buybacks`
- Selected notes: `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-buying-imbalance`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `bitcoin-quiet-divergence` | 4 | `BTC` | yes | yes |
| 2 | `crypto-breadth-beneath-bitcoin` | 4 | `BTC` | yes | yes |
| 3 | `bitcoin-buying-imbalance` | 4 | `BTC` | yes | yes |
| 4 | `when-risk-off-is-not-a-crisis` | 3 | `BTC` | yes | no |
| 5 | `crypto-leverage-liquidity-trap` | 3 | `BTC` | yes | no |
| 6 | `crypto-chokepoints-november-2026` | 3 | `BTC` | yes | no |
| 7 | `bitcoin-recovery-beneath-resistance` | 3 | `BTC` | no | yes |
| 8 | `bitcoin-rebound-spot-demand` | 3 | `BTC` | no | yes |
| 9 | `bitcoin-holding-up` | 3 | `BTC` | no | yes |
| 10 | `bitcoin-open-interest-filter-test` | 2 | `BTC` | no | no |
| 11 | `crypto-market-structure-after-midterms` | 1 | none | yes | no |
| 12 | `uni-rebound-liquidity-test` | 1 | none | no | yes |
| 13 | `monad-november-unlock-liquidity-test` | 0 | none | no | no |
| 14 | `binance-four-hour-wallet-takeover` | 0 | none | no | no |
| 15 | `token-unlock-liquidity-illusion-90-day-calendar` | 0 | none | no | no |
| 16 | `deepbook-supply-transparency` | 0 | none | no | no |
| 17 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 18 | `solz-launch-investigation` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `aero-at-0-68` | 0 | none | no | no |
| 21 | `weft-first-week` | 0 | none | no | no |
| 22 | `virtual-alpha-risk` | 0 | none | no | no |
| 23 | `rune-quiet-repricing` | 0 | none | no | no |
| 24 | `pyth-revenue-unlock` | 0 | none | no | no |
| 25 | `venice-ai-privacy` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `solz-launch-investigation`

- Date: 2026-10-29
- Topic: `risk-verification`
- Research type: `investigative-analysis`
- Assets: `SOLZ`
- Selected variant: `related`
- Sorted candidate order: `binance-four-hour-wallet-takeover`, `virtual-alpha-risk`, `venice-ai-privacy`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `crypto-chokepoints-november-2026`, `token-unlock-liquidity-illusion-90-day-calendar`, `small-cap-crypto-liquidity-illusion`, `deepbook-supply-transparency`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `institutional-adoption-token-demand`, `bitcoin-holding-up`, `aero-at-0-68`, `bitcoin-buying-imbalance`, `weft-first-week`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `crypto-buybacks`
- Selected notes: `binance-four-hour-wallet-takeover`, `virtual-alpha-risk`, `venice-ai-privacy`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `binance-four-hour-wallet-takeover` | 2 | none | yes | yes |
| 2 | `virtual-alpha-risk` | 2 | none | yes | yes |
| 3 | `venice-ai-privacy` | 2 | none | yes | yes |
| 4 | `when-risk-off-is-not-a-crisis` | 1 | none | no | yes |
| 5 | `crypto-leverage-liquidity-trap` | 1 | none | no | yes |
| 6 | `monad-november-unlock-liquidity-test` | 1 | none | no | yes |
| 7 | `crypto-market-structure-after-midterms` | 1 | none | no | yes |
| 8 | `bitcoin-open-interest-filter-test` | 1 | none | no | yes |
| 9 | `crypto-chokepoints-november-2026` | 1 | none | no | yes |
| 10 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | no | yes |
| 11 | `small-cap-crypto-liquidity-illusion` | 1 | none | no | yes |
| 12 | `deepbook-supply-transparency` | 0 | none | no | no |
| 13 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 14 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 15 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 16 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 17 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 18 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `bitcoin-holding-up` | 0 | none | no | no |
| 21 | `aero-at-0-68` | 0 | none | no | no |
| 22 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 23 | `weft-first-week` | 0 | none | no | no |
| 24 | `rune-quiet-repricing` | 0 | none | no | no |
| 25 | `pyth-revenue-unlock` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `institutional-adoption-token-demand`

- Date: 2026-10-28
- Topic: `protocol-research`
- Research type: `token-due-diligence`
- Assets: `CC`, `LINK`
- Selected variant: `related`
- Sorted candidate order: `deepbook-supply-transparency`, `rune-quiet-repricing`, `aero-at-0-68`, `weft-first-week`, `pyth-revenue-unlock`, `crypto-buybacks`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `crypto-chokepoints-november-2026`, `token-unlock-liquidity-illusion-90-day-calendar`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `small-cap-crypto-liquidity-illusion`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `solz-launch-investigation`, `bitcoin-holding-up`, `bitcoin-buying-imbalance`, `virtual-alpha-risk`, `venice-ai-privacy`
- Selected notes: `deepbook-supply-transparency`, `rune-quiet-repricing`, `aero-at-0-68`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `deepbook-supply-transparency` | 2 | none | yes | yes |
| 2 | `rune-quiet-repricing` | 2 | none | yes | yes |
| 3 | `aero-at-0-68` | 1 | none | no | yes |
| 4 | `weft-first-week` | 1 | none | no | yes |
| 5 | `pyth-revenue-unlock` | 1 | none | no | yes |
| 6 | `crypto-buybacks` | 1 | none | no | yes |
| 7 | `when-risk-off-is-not-a-crisis` | 0 | none | no | no |
| 8 | `crypto-leverage-liquidity-trap` | 0 | none | no | no |
| 9 | `monad-november-unlock-liquidity-test` | 0 | none | no | no |
| 10 | `crypto-market-structure-after-midterms` | 0 | none | no | no |
| 11 | `bitcoin-open-interest-filter-test` | 0 | none | no | no |
| 12 | `binance-four-hour-wallet-takeover` | 0 | none | no | no |
| 13 | `crypto-chokepoints-november-2026` | 0 | none | no | no |
| 14 | `token-unlock-liquidity-illusion-90-day-calendar` | 0 | none | no | no |
| 15 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 16 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 17 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 18 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 19 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 20 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 21 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 22 | `solz-launch-investigation` | 0 | none | no | no |
| 23 | `bitcoin-holding-up` | 0 | none | no | no |
| 24 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 25 | `virtual-alpha-risk` | 0 | none | no | no |
| 26 | `venice-ai-privacy` | 0 | none | no | no |

---

## `bitcoin-holding-up`

- Date: 2026-10-27
- Topic: `bitcoin`
- Research type: `market-snapshot`
- Assets: `BTC`, `ETH`, `SOL`
- Selected variant: `related`
- Sorted candidate order: `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `crypto-leverage-liquidity-trap`, `when-risk-off-is-not-a-crisis`, `crypto-chokepoints-november-2026`, `bitcoin-recovery-beneath-resistance`, `bitcoin-rebound-spot-demand`, `bitcoin-open-interest-filter-test`, `bitcoin-selloff-leverage`, `bitcoin-buying-imbalance`, `binance-four-hour-wallet-takeover`, `uni-rebound-liquidity-test`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `virtual-alpha-risk`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `venice-ai-privacy`, `crypto-buybacks`
- Selected notes: `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `crypto-leverage-liquidity-trap`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `bitcoin-quiet-divergence` | 7 | `BTC`, `ETH`, `SOL` | no | yes |
| 2 | `crypto-breadth-beneath-bitcoin` | 7 | `BTC`, `ETH`, `SOL` | no | yes |
| 3 | `crypto-leverage-liquidity-trap` | 6 | `BTC`, `ETH`, `SOL` | no | no |
| 4 | `when-risk-off-is-not-a-crisis` | 4 | `BTC`, `ETH` | no | no |
| 5 | `crypto-chokepoints-november-2026` | 4 | `BTC`, `ETH` | no | no |
| 6 | `bitcoin-recovery-beneath-resistance` | 4 | `BTC` | yes | yes |
| 7 | `bitcoin-rebound-spot-demand` | 4 | `BTC` | yes | yes |
| 8 | `bitcoin-open-interest-filter-test` | 3 | `BTC` | yes | no |
| 9 | `bitcoin-selloff-leverage` | 3 | `BTC` | no | yes |
| 10 | `bitcoin-buying-imbalance` | 3 | `BTC` | no | yes |
| 11 | `binance-four-hour-wallet-takeover` | 2 | `ETH` | no | no |
| 12 | `uni-rebound-liquidity-test` | 1 | none | no | yes |
| 13 | `monad-november-unlock-liquidity-test` | 0 | none | no | no |
| 14 | `crypto-market-structure-after-midterms` | 0 | none | no | no |
| 15 | `token-unlock-liquidity-illusion-90-day-calendar` | 0 | none | no | no |
| 16 | `deepbook-supply-transparency` | 0 | none | no | no |
| 17 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 18 | `solz-launch-investigation` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `aero-at-0-68` | 0 | none | no | no |
| 21 | `weft-first-week` | 0 | none | no | no |
| 22 | `virtual-alpha-risk` | 0 | none | no | no |
| 23 | `rune-quiet-repricing` | 0 | none | no | no |
| 24 | `pyth-revenue-unlock` | 0 | none | no | no |
| 25 | `venice-ai-privacy` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `aero-at-0-68`

- Date: 2026-10-26
- Topic: `tokenomics`
- Research type: `token-due-diligence`
- Assets: `AERO`
- Selected variant: `related`
- Sorted candidate order: `weft-first-week`, `pyth-revenue-unlock`, `crypto-buybacks`, `monad-november-unlock-liquidity-test`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `institutional-adoption-token-demand`, `rune-quiet-repricing`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `crypto-chokepoints-november-2026`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `small-cap-crypto-liquidity-illusion`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `solz-launch-investigation`, `bitcoin-holding-up`, `bitcoin-buying-imbalance`, `virtual-alpha-risk`, `venice-ai-privacy`
- Selected notes: `weft-first-week`, `pyth-revenue-unlock`, `crypto-buybacks`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `weft-first-week` | 2 | none | yes | yes |
| 2 | `pyth-revenue-unlock` | 2 | none | yes | yes |
| 3 | `crypto-buybacks` | 2 | none | yes | yes |
| 4 | `monad-november-unlock-liquidity-test` | 1 | none | yes | no |
| 5 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | yes | no |
| 6 | `deepbook-supply-transparency` | 1 | none | no | yes |
| 7 | `institutional-adoption-token-demand` | 1 | none | no | yes |
| 8 | `rune-quiet-repricing` | 1 | none | no | yes |
| 9 | `when-risk-off-is-not-a-crisis` | 0 | none | no | no |
| 10 | `crypto-leverage-liquidity-trap` | 0 | none | no | no |
| 11 | `crypto-market-structure-after-midterms` | 0 | none | no | no |
| 12 | `bitcoin-open-interest-filter-test` | 0 | none | no | no |
| 13 | `binance-four-hour-wallet-takeover` | 0 | none | no | no |
| 14 | `crypto-chokepoints-november-2026` | 0 | none | no | no |
| 15 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 16 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 17 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 18 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 19 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 20 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 21 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 22 | `solz-launch-investigation` | 0 | none | no | no |
| 23 | `bitcoin-holding-up` | 0 | none | no | no |
| 24 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 25 | `virtual-alpha-risk` | 0 | none | no | no |
| 26 | `venice-ai-privacy` | 0 | none | no | no |

---

## `bitcoin-buying-imbalance`

- Date: 2026-10-26
- Topic: `market-structure`
- Research type: `market-snapshot`
- Assets: `BTC`
- Selected variant: `related`
- Sorted candidate order: `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-selloff-leverage`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-chokepoints-november-2026`, `bitcoin-recovery-beneath-resistance`, `bitcoin-rebound-spot-demand`, `bitcoin-holding-up`, `bitcoin-open-interest-filter-test`, `crypto-market-structure-after-midterms`, `uni-rebound-liquidity-test`, `monad-november-unlock-liquidity-test`, `binance-four-hour-wallet-takeover`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `small-cap-crypto-liquidity-illusion`, `solz-launch-investigation`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `virtual-alpha-risk`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `venice-ai-privacy`, `crypto-buybacks`
- Selected notes: `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-selloff-leverage`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `bitcoin-quiet-divergence` | 4 | `BTC` | yes | yes |
| 2 | `crypto-breadth-beneath-bitcoin` | 4 | `BTC` | yes | yes |
| 3 | `bitcoin-selloff-leverage` | 4 | `BTC` | yes | yes |
| 4 | `when-risk-off-is-not-a-crisis` | 3 | `BTC` | yes | no |
| 5 | `crypto-leverage-liquidity-trap` | 3 | `BTC` | yes | no |
| 6 | `crypto-chokepoints-november-2026` | 3 | `BTC` | yes | no |
| 7 | `bitcoin-recovery-beneath-resistance` | 3 | `BTC` | no | yes |
| 8 | `bitcoin-rebound-spot-demand` | 3 | `BTC` | no | yes |
| 9 | `bitcoin-holding-up` | 3 | `BTC` | no | yes |
| 10 | `bitcoin-open-interest-filter-test` | 2 | `BTC` | no | no |
| 11 | `crypto-market-structure-after-midterms` | 1 | none | yes | no |
| 12 | `uni-rebound-liquidity-test` | 1 | none | no | yes |
| 13 | `monad-november-unlock-liquidity-test` | 0 | none | no | no |
| 14 | `binance-four-hour-wallet-takeover` | 0 | none | no | no |
| 15 | `token-unlock-liquidity-illusion-90-day-calendar` | 0 | none | no | no |
| 16 | `deepbook-supply-transparency` | 0 | none | no | no |
| 17 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 18 | `solz-launch-investigation` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `aero-at-0-68` | 0 | none | no | no |
| 21 | `weft-first-week` | 0 | none | no | no |
| 22 | `virtual-alpha-risk` | 0 | none | no | no |
| 23 | `rune-quiet-repricing` | 0 | none | no | no |
| 24 | `pyth-revenue-unlock` | 0 | none | no | no |
| 25 | `venice-ai-privacy` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `weft-first-week`

- Date: 2026-10-23
- Topic: `tokenomics`
- Research type: `token-due-diligence`
- Assets: `WEFT`
- Selected variant: `related`
- Sorted candidate order: `aero-at-0-68`, `pyth-revenue-unlock`, `crypto-buybacks`, `monad-november-unlock-liquidity-test`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `institutional-adoption-token-demand`, `rune-quiet-repricing`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `crypto-chokepoints-november-2026`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `small-cap-crypto-liquidity-illusion`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `solz-launch-investigation`, `bitcoin-holding-up`, `bitcoin-buying-imbalance`, `virtual-alpha-risk`, `venice-ai-privacy`
- Selected notes: `aero-at-0-68`, `pyth-revenue-unlock`, `crypto-buybacks`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `aero-at-0-68` | 2 | none | yes | yes |
| 2 | `pyth-revenue-unlock` | 2 | none | yes | yes |
| 3 | `crypto-buybacks` | 2 | none | yes | yes |
| 4 | `monad-november-unlock-liquidity-test` | 1 | none | yes | no |
| 5 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | yes | no |
| 6 | `deepbook-supply-transparency` | 1 | none | no | yes |
| 7 | `institutional-adoption-token-demand` | 1 | none | no | yes |
| 8 | `rune-quiet-repricing` | 1 | none | no | yes |
| 9 | `when-risk-off-is-not-a-crisis` | 0 | none | no | no |
| 10 | `crypto-leverage-liquidity-trap` | 0 | none | no | no |
| 11 | `crypto-market-structure-after-midterms` | 0 | none | no | no |
| 12 | `bitcoin-open-interest-filter-test` | 0 | none | no | no |
| 13 | `binance-four-hour-wallet-takeover` | 0 | none | no | no |
| 14 | `crypto-chokepoints-november-2026` | 0 | none | no | no |
| 15 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 16 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 17 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 18 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 19 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 20 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 21 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 22 | `solz-launch-investigation` | 0 | none | no | no |
| 23 | `bitcoin-holding-up` | 0 | none | no | no |
| 24 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 25 | `virtual-alpha-risk` | 0 | none | no | no |
| 26 | `venice-ai-privacy` | 0 | none | no | no |

---

## `virtual-alpha-risk`

- Date: 2026-10-23
- Topic: `risk-verification`
- Research type: `investigative-analysis`
- Assets: `VIRTUAL`
- Selected variant: `related`
- Sorted candidate order: `binance-four-hour-wallet-takeover`, `solz-launch-investigation`, `venice-ai-privacy`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `crypto-chokepoints-november-2026`, `token-unlock-liquidity-illusion-90-day-calendar`, `small-cap-crypto-liquidity-illusion`, `deepbook-supply-transparency`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `institutional-adoption-token-demand`, `bitcoin-holding-up`, `aero-at-0-68`, `bitcoin-buying-imbalance`, `weft-first-week`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `crypto-buybacks`
- Selected notes: `binance-four-hour-wallet-takeover`, `solz-launch-investigation`, `venice-ai-privacy`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `binance-four-hour-wallet-takeover` | 2 | none | yes | yes |
| 2 | `solz-launch-investigation` | 2 | none | yes | yes |
| 3 | `venice-ai-privacy` | 2 | none | yes | yes |
| 4 | `when-risk-off-is-not-a-crisis` | 1 | none | no | yes |
| 5 | `crypto-leverage-liquidity-trap` | 1 | none | no | yes |
| 6 | `monad-november-unlock-liquidity-test` | 1 | none | no | yes |
| 7 | `crypto-market-structure-after-midterms` | 1 | none | no | yes |
| 8 | `bitcoin-open-interest-filter-test` | 1 | none | no | yes |
| 9 | `crypto-chokepoints-november-2026` | 1 | none | no | yes |
| 10 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | no | yes |
| 11 | `small-cap-crypto-liquidity-illusion` | 1 | none | no | yes |
| 12 | `deepbook-supply-transparency` | 0 | none | no | no |
| 13 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 14 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 15 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 16 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 17 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 18 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `bitcoin-holding-up` | 0 | none | no | no |
| 21 | `aero-at-0-68` | 0 | none | no | no |
| 22 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 23 | `weft-first-week` | 0 | none | no | no |
| 24 | `rune-quiet-repricing` | 0 | none | no | no |
| 25 | `pyth-revenue-unlock` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `rune-quiet-repricing`

- Date: 2026-10-22
- Topic: `protocol-research`
- Research type: `token-due-diligence`
- Assets: `RUNE`
- Selected variant: `related`
- Sorted candidate order: `deepbook-supply-transparency`, `institutional-adoption-token-demand`, `aero-at-0-68`, `weft-first-week`, `pyth-revenue-unlock`, `crypto-buybacks`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `crypto-chokepoints-november-2026`, `token-unlock-liquidity-illusion-90-day-calendar`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `small-cap-crypto-liquidity-illusion`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `solz-launch-investigation`, `bitcoin-holding-up`, `bitcoin-buying-imbalance`, `virtual-alpha-risk`, `venice-ai-privacy`
- Selected notes: `deepbook-supply-transparency`, `institutional-adoption-token-demand`, `aero-at-0-68`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `deepbook-supply-transparency` | 2 | none | yes | yes |
| 2 | `institutional-adoption-token-demand` | 2 | none | yes | yes |
| 3 | `aero-at-0-68` | 1 | none | no | yes |
| 4 | `weft-first-week` | 1 | none | no | yes |
| 5 | `pyth-revenue-unlock` | 1 | none | no | yes |
| 6 | `crypto-buybacks` | 1 | none | no | yes |
| 7 | `when-risk-off-is-not-a-crisis` | 0 | none | no | no |
| 8 | `crypto-leverage-liquidity-trap` | 0 | none | no | no |
| 9 | `monad-november-unlock-liquidity-test` | 0 | none | no | no |
| 10 | `crypto-market-structure-after-midterms` | 0 | none | no | no |
| 11 | `bitcoin-open-interest-filter-test` | 0 | none | no | no |
| 12 | `binance-four-hour-wallet-takeover` | 0 | none | no | no |
| 13 | `crypto-chokepoints-november-2026` | 0 | none | no | no |
| 14 | `token-unlock-liquidity-illusion-90-day-calendar` | 0 | none | no | no |
| 15 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 16 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 17 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 18 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 19 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 20 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 21 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 22 | `solz-launch-investigation` | 0 | none | no | no |
| 23 | `bitcoin-holding-up` | 0 | none | no | no |
| 24 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 25 | `virtual-alpha-risk` | 0 | none | no | no |
| 26 | `venice-ai-privacy` | 0 | none | no | no |

---

## `pyth-revenue-unlock`

- Date: 2026-10-21
- Topic: `tokenomics`
- Research type: `token-due-diligence`
- Assets: `PYTH`
- Selected variant: `related`
- Sorted candidate order: `aero-at-0-68`, `weft-first-week`, `crypto-buybacks`, `monad-november-unlock-liquidity-test`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `institutional-adoption-token-demand`, `rune-quiet-repricing`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `crypto-chokepoints-november-2026`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `small-cap-crypto-liquidity-illusion`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `solz-launch-investigation`, `bitcoin-holding-up`, `bitcoin-buying-imbalance`, `virtual-alpha-risk`, `venice-ai-privacy`
- Selected notes: `aero-at-0-68`, `weft-first-week`, `crypto-buybacks`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `aero-at-0-68` | 2 | none | yes | yes |
| 2 | `weft-first-week` | 2 | none | yes | yes |
| 3 | `crypto-buybacks` | 2 | none | yes | yes |
| 4 | `monad-november-unlock-liquidity-test` | 1 | none | yes | no |
| 5 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | yes | no |
| 6 | `deepbook-supply-transparency` | 1 | none | no | yes |
| 7 | `institutional-adoption-token-demand` | 1 | none | no | yes |
| 8 | `rune-quiet-repricing` | 1 | none | no | yes |
| 9 | `when-risk-off-is-not-a-crisis` | 0 | none | no | no |
| 10 | `crypto-leverage-liquidity-trap` | 0 | none | no | no |
| 11 | `crypto-market-structure-after-midterms` | 0 | none | no | no |
| 12 | `bitcoin-open-interest-filter-test` | 0 | none | no | no |
| 13 | `binance-four-hour-wallet-takeover` | 0 | none | no | no |
| 14 | `crypto-chokepoints-november-2026` | 0 | none | no | no |
| 15 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 16 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 17 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 18 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 19 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 20 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 21 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 22 | `solz-launch-investigation` | 0 | none | no | no |
| 23 | `bitcoin-holding-up` | 0 | none | no | no |
| 24 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 25 | `virtual-alpha-risk` | 0 | none | no | no |
| 26 | `venice-ai-privacy` | 0 | none | no | no |

---

## `venice-ai-privacy`

- Date: 2026-10-21
- Topic: `risk-verification`
- Research type: `investigative-analysis`
- Assets: `VVV`
- Selected variant: `related`
- Sorted candidate order: `binance-four-hour-wallet-takeover`, `solz-launch-investigation`, `virtual-alpha-risk`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `monad-november-unlock-liquidity-test`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `crypto-chokepoints-november-2026`, `token-unlock-liquidity-illusion-90-day-calendar`, `small-cap-crypto-liquidity-illusion`, `deepbook-supply-transparency`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `institutional-adoption-token-demand`, `bitcoin-holding-up`, `aero-at-0-68`, `bitcoin-buying-imbalance`, `weft-first-week`, `rune-quiet-repricing`, `pyth-revenue-unlock`, `crypto-buybacks`
- Selected notes: `binance-four-hour-wallet-takeover`, `solz-launch-investigation`, `virtual-alpha-risk`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `binance-four-hour-wallet-takeover` | 2 | none | yes | yes |
| 2 | `solz-launch-investigation` | 2 | none | yes | yes |
| 3 | `virtual-alpha-risk` | 2 | none | yes | yes |
| 4 | `when-risk-off-is-not-a-crisis` | 1 | none | no | yes |
| 5 | `crypto-leverage-liquidity-trap` | 1 | none | no | yes |
| 6 | `monad-november-unlock-liquidity-test` | 1 | none | no | yes |
| 7 | `crypto-market-structure-after-midterms` | 1 | none | no | yes |
| 8 | `bitcoin-open-interest-filter-test` | 1 | none | no | yes |
| 9 | `crypto-chokepoints-november-2026` | 1 | none | no | yes |
| 10 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | no | yes |
| 11 | `small-cap-crypto-liquidity-illusion` | 1 | none | no | yes |
| 12 | `deepbook-supply-transparency` | 0 | none | no | no |
| 13 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 14 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 15 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 16 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 17 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 18 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 19 | `institutional-adoption-token-demand` | 0 | none | no | no |
| 20 | `bitcoin-holding-up` | 0 | none | no | no |
| 21 | `aero-at-0-68` | 0 | none | no | no |
| 22 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 23 | `weft-first-week` | 0 | none | no | no |
| 24 | `rune-quiet-repricing` | 0 | none | no | no |
| 25 | `pyth-revenue-unlock` | 0 | none | no | no |
| 26 | `crypto-buybacks` | 0 | none | no | no |

---

## `crypto-buybacks`

- Date: 2026-10-21
- Topic: `tokenomics`
- Research type: `token-due-diligence`
- Assets: `EDGE`, `STONK`
- Selected variant: `related`
- Sorted candidate order: `aero-at-0-68`, `weft-first-week`, `pyth-revenue-unlock`, `monad-november-unlock-liquidity-test`, `token-unlock-liquidity-illusion-90-day-calendar`, `deepbook-supply-transparency`, `institutional-adoption-token-demand`, `rune-quiet-repricing`, `when-risk-off-is-not-a-crisis`, `crypto-leverage-liquidity-trap`, `crypto-market-structure-after-midterms`, `bitcoin-open-interest-filter-test`, `binance-four-hour-wallet-takeover`, `crypto-chokepoints-november-2026`, `bitcoin-recovery-beneath-resistance`, `uni-rebound-liquidity-test`, `bitcoin-quiet-divergence`, `crypto-breadth-beneath-bitcoin`, `small-cap-crypto-liquidity-illusion`, `bitcoin-rebound-spot-demand`, `bitcoin-selloff-leverage`, `solz-launch-investigation`, `bitcoin-holding-up`, `bitcoin-buying-imbalance`, `virtual-alpha-risk`, `venice-ai-privacy`
- Selected notes: `aero-at-0-68`, `weft-first-week`, `pyth-revenue-unlock`

| Position | Candidate slug | Score | Shared assets (2 each) | Same topic (+1) | Same type (+1) |
| --- | --- | --- | --- | --- | --- |
| 1 | `aero-at-0-68` | 2 | none | yes | yes |
| 2 | `weft-first-week` | 2 | none | yes | yes |
| 3 | `pyth-revenue-unlock` | 2 | none | yes | yes |
| 4 | `monad-november-unlock-liquidity-test` | 1 | none | yes | no |
| 5 | `token-unlock-liquidity-illusion-90-day-calendar` | 1 | none | yes | no |
| 6 | `deepbook-supply-transparency` | 1 | none | no | yes |
| 7 | `institutional-adoption-token-demand` | 1 | none | no | yes |
| 8 | `rune-quiet-repricing` | 1 | none | no | yes |
| 9 | `when-risk-off-is-not-a-crisis` | 0 | none | no | no |
| 10 | `crypto-leverage-liquidity-trap` | 0 | none | no | no |
| 11 | `crypto-market-structure-after-midterms` | 0 | none | no | no |
| 12 | `bitcoin-open-interest-filter-test` | 0 | none | no | no |
| 13 | `binance-four-hour-wallet-takeover` | 0 | none | no | no |
| 14 | `crypto-chokepoints-november-2026` | 0 | none | no | no |
| 15 | `bitcoin-recovery-beneath-resistance` | 0 | none | no | no |
| 16 | `uni-rebound-liquidity-test` | 0 | none | no | no |
| 17 | `bitcoin-quiet-divergence` | 0 | none | no | no |
| 18 | `crypto-breadth-beneath-bitcoin` | 0 | none | no | no |
| 19 | `small-cap-crypto-liquidity-illusion` | 0 | none | no | no |
| 20 | `bitcoin-rebound-spot-demand` | 0 | none | no | no |
| 21 | `bitcoin-selloff-leverage` | 0 | none | no | no |
| 22 | `solz-launch-investigation` | 0 | none | no | no |
| 23 | `bitcoin-holding-up` | 0 | none | no | no |
| 24 | `bitcoin-buying-imbalance` | 0 | none | no | no |
| 25 | `virtual-alpha-risk` | 0 | none | no | no |
| 26 | `venice-ai-privacy` | 0 | none | no | no |

---

Slice 4 Gate: Bret records approved or deferred, plus an ISO date, here.
