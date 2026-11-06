# Phase 1 closure evidence

Measured: 2026-11-06 (local Windows evidence reported by Codex)

## Commands and environment

- `python -X utf8 build.py` — exit 0; built 25 notes.
- `python -m http.server 4173 --bind 127.0.0.1 -d dist` — served the built output at `http://127.0.0.1:4173/`; stopped after measurement.
- `node docs/designs/ux-audit/evidence/scripts/phase1-closure.mjs` — exit 0; 36 contrast samples, 18 axe route/state samples, 9 scroll samples, 0 failures. No screenshots or PNG files were written.
- Environment: Python 3.14.3; Node v26.13.0; Playwright 1.64.1; Chromium 156.0.8078.4.

## Contrast results

All values were identical for light/dark emulation and across the three viewport widths. Every sample passed the 4.5:1 normal-text threshold.

| Finding / rendered element | Current foreground | Effective background | Font size / weight | Ratio | Samples |
|---|---|---|---|---:|---:|
| UX-01 404 kicker | `#1d5c55` | `#f6f3ec` | 18px / 700 | 6.98:1 | 6/6 pass |
| UX-02 token-unlock mast span | `#53636b` | `#fcfcfa` | 12px / 700 | 6.08:1 | 6/6 pass |
| UX-03 token-unlock kicker | `#994536` | `#fcfcfa` | 12px / 700 | 6.27:1 | 6/6 pass |
| UX-09 Binance mast span | `#53636b` | `#f8f7f3` | 13px / 700 | 5.82:1 | 6/6 pass |
| UX-09 Binance kicker | `#53636b` | `#f8f7f3` | 12px / 700 | 5.82:1 | 6/6 pass |
| UX-09 Binance footer | `#53636b` | `#f8f7f3` | 13px / 400 | 5.82:1 | 6/6 pass |

## Axe results

WCAG 2.0/2.1 A and AA axe scans reported zero color-contrast nodes in every viewport and color scheme: `/404.html` 6/6; `/token-unlock-liquidity-illusion-90-day-calendar/` 6/6; `/binance-four-hour-wallet-takeover/` 6/6.

## Scroll-region results

| Finding / route | Viewport | tabindex / role / label | Scroll width / client width | Tab | Focus-visible / computed outline | scrollLeft before → ArrowRight → End | Result |
|---|---:|---|---:|---|---|---:|---|
| UX-04 `/aero-at-0-68/` | 390 | `0 / region / AERO unlock data table` | 610 / 346 (overflow) | yes | yes / `rgb(40, 107, 92) solid 3px` | 0 → 120 → 120 | pass |
| UX-04 `/aero-at-0-68/` | 768 | `0 / region / AERO unlock data table` | 704 / 704 (none) | yes | yes / `rgb(40, 107, 92) solid 3px` | 0 → 0 → 0 | pass |
| UX-04 `/aero-at-0-68/` | 1440 | `0 / region / AERO unlock data table` | 704 / 704 (none) | yes | yes / `rgb(40, 107, 92) solid 3px` | 0 → 0 → 0 | pass |
| UX-05 `/bitcoin-buying-imbalance/` | 390 | `0 / region / Bitcoin buying imbalance data table` | 540 / 366 (overflow) | yes | yes / `rgb(32, 94, 84) solid 3px` | 0 → 120 → 120 | pass |
| UX-05 `/bitcoin-buying-imbalance/` | 768 | `0 / region / Bitcoin buying imbalance data table` | 718 / 718 (none) | yes | yes / `rgb(32, 94, 84) solid 3px` | 0 → 0 → 0 | pass |
| UX-05 `/bitcoin-buying-imbalance/` | 1440 | `0 / region / Bitcoin buying imbalance data table` | 870 / 870 (none) | yes | yes / `rgb(32, 94, 84) solid 3px` | 0 → 0 → 0 | pass |
| UX-06 `/token-unlock-liquidity-illusion-90-day-calendar/` | 390 | `0 / region / 90-day token unlock calendar data table` | 590 / 354 (overflow) | yes | yes / `rgb(16, 16, 16) auto 1px` | 0 → 120 → 120 | pass |
| UX-06 `/token-unlock-liquidity-illusion-90-day-calendar/` | 768 | `0 / region / 90-day token unlock calendar data table` | 718 / 718 (none) | yes | yes / `rgb(16, 16, 16) auto 1px` | 0 → 0 → 0 | pass |
| UX-06 `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440 | `0 / region / 90-day token unlock calendar data table` | 1078 / 1078 (none) | yes | yes / `rgb(16, 16, 16) auto 1px` | 0 → 0 → 0 | pass |

## Tooling findings and raw evidence

- `tests/visual.spec.ts` has no `APPROVED_CONTRAST_STATES` declaration. Reported; tests were not changed.
- Search found no script or test parsing `remeasure.md` or its Approval column; `remeasure.mjs:274` is the writer.
- Full per-sample values and axe node details: `docs/designs/ux-audit/evidence/axe/phase1-closure-raw/phase1-closure.json` (git-ignored; not committed).
- The run wrote no screenshots/PNGs. Axe and keyboard/focus measurements are local browser evidence, not hosted CI evidence.
