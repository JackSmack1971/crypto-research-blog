# Slice 1 remeasurement — UX-01–06

Measured: 2026-11-05T06:11:19.991Z against `http://127.0.0.1:4173`; build: current catalog output (24 articles).

Raw axe JSON and PNG screenshots are local-only under the Git-ignored `screenshots/remeasure-raw/` directory. The committed script is reproducible with the existing dependencies; no production or test files were changed.

## Contrast state matrix

Rows are included for every reproduced contrast state only. Approval remains pending for every row; dates remain blank until Bret decides.

| Finding | Route | Viewport | Color scheme | Element/selector | Property | Foreground | Effective background | Font size/weight | Observed ratio | Minimum ratio | Approval | Approval date |
|---|---|---:|---|---|---|---|---|---|---:|---:|---|---|
| UX-01 | `/404.html` | 390px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | pending |  |
| UX-01 | `/404.html` | 390px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | pending |  |
| UX-01 | `/404.html` | 768px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | pending |  |
| UX-01 | `/404.html` | 768px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | pending |  |
| UX-01 | `/404.html` | 1440px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | pending |  |
| UX-01 | `/404.html` | 1440px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | light | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | dark | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | light | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | dark | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | light | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | dark | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | pending |  |

## Finding results

### UX-01 — reproduced

Route: `/404.html`; requested selector: `.mast .kicker, .kicker`. Evidence covers 390, 768, and 1440 CSS px in light and dark color schemes.

The measured color and contrast properties were identical under emulated light and dark schemes; no matching dark-mode override changed these targets.

| Viewport | Scheme | Element/selector | Foreground | Effective background | Font size/weight | Ratio | Minimum | Axe color-contrast nodes | Result |
|---:|---|---|---|---|---|---:|---:|---:|---|
| 390px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63 | 4.5 | 1 | reproduced |
| 390px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63 | 4.5 | 1 | reproduced |
| 768px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63 | 4.5 | 1 | reproduced |
| 768px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63 | 4.5 | 1 | reproduced |
| 1440px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63 | 4.5 | 1 | reproduced |
| 1440px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63 | 4.5 | 1 | reproduced |


### UX-02 — reproduced

Route: `/token-unlock-liquidity-illusion-90-day-calendar/`; requested selector: `.mast span:last-child`. Evidence covers 390, 768, and 1440 CSS px in light and dark color schemes.

The measured color and contrast properties were identical under emulated light and dark schemes; no matching dark-mode override changed these targets.

| Viewport | Scheme | Element/selector | Foreground | Effective background | Font size/weight | Ratio | Minimum | Axe color-contrast nodes | Result |
|---:|---|---|---|---|---|---:|---:|---:|---|
| 390px | light | `html > body > header.mast > span:nth-of-type(2)` | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13 | 4.5 | 2 | reproduced |
| 390px | dark | `html > body > header.mast > span:nth-of-type(2)` | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13 | 4.5 | 2 | reproduced |
| 768px | light | `html > body > header.mast > span:nth-of-type(2)` | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13 | 4.5 | 2 | reproduced |
| 768px | dark | `html > body > header.mast > span:nth-of-type(2)` | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13 | 4.5 | 2 | reproduced |
| 1440px | light | `html > body > header.mast > span:nth-of-type(2)` | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13 | 4.5 | 2 | reproduced |
| 1440px | dark | `html > body > header.mast > span:nth-of-type(2)` | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13 | 4.5 | 2 | reproduced |


### UX-03 — reproduced

Route: `/token-unlock-liquidity-illusion-90-day-calendar/`; requested selector: `.kicker`. Evidence covers 390, 768, and 1440 CSS px in light and dark color schemes.

The measured color and contrast properties were identical under emulated light and dark schemes; no matching dark-mode override changed these targets.

| Viewport | Scheme | Element/selector | Foreground | Effective background | Font size/weight | Ratio | Minimum | Axe color-contrast nodes | Result |
|---:|---|---|---|---|---|---:|---:|---:|---|
| 390px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26 | 4.5 | 2 | reproduced |
| 390px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26 | 4.5 | 2 | reproduced |
| 768px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26 | 4.5 | 2 | reproduced |
| 768px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26 | 4.5 | 2 | reproduced |
| 1440px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26 | 4.5 | 2 | reproduced |
| 1440px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26 | 4.5 | 2 | reproduced |


### UX-04 — not reproduced

Route: `/aero-at-0-68/`; wrapper: `.table-scroll`.

| Viewport | Role | Accessible name | Tab-reachable | Programmatic tabindex | Scroll width / client width | Overflow | :focus-visible | Outline | scrollLeft before→after five ArrowRight presses | Axe scroll-region nodes | Result |
|---:|---|---|---|---|---:|---|---|---|---:|---:|---|
| 390px | missing | missing | true | false | 610 / 346 | true | true | rgb(40, 107, 92) solid 3px | 0 → 200 | 1 | not reproduced |
| 768px | missing | missing | false | false | 704 / 704 | false | false | none | 0 → 0 | 0 | not reproduced |
| 1440px | missing | missing | false | false | 704 / 704 | false | false | none | 0 → 0 | 0 | not reproduced |

### UX-05 — not reproduced

Route: `/bitcoin-buying-imbalance/`; wrapper: `.tablewrap`.

| Viewport | Role | Accessible name | Tab-reachable | Programmatic tabindex | Scroll width / client width | Overflow | :focus-visible | Outline | scrollLeft before→after five ArrowRight presses | Axe scroll-region nodes | Result |
|---:|---|---|---|---|---:|---|---|---|---:|---:|---|
| 390px | missing | missing | true | false | 540 / 366 | true | true | rgb(32, 94, 84) solid 3px | 0 → 174 | 1 | not reproduced |
| 768px | missing | missing | false | false | 718 / 718 | false | false | none | 0 → 0 | 0 | not reproduced |
| 1440px | missing | missing | false | false | 870 / 870 | false | false | none | 0 → 0 | 0 | not reproduced |

### UX-06 — not reproduced

Route: `/token-unlock-liquidity-illusion-90-day-calendar/`; wrapper: `.scroll`.

| Viewport | Role | Accessible name | Tab-reachable | Programmatic tabindex | Scroll width / client width | Overflow | :focus-visible | Outline | scrollLeft before→after five ArrowRight presses | Axe scroll-region nodes | Result |
|---:|---|---|---|---|---:|---|---|---|---:|---:|---|
| 390px | missing | missing | true | false | 590 / 354 | true | true | rgb(16, 16, 16) auto 1px | 0 → 200 | 1 | not reproduced |
| 768px | missing | missing | false | false | 718 / 718 | false | false | none | 0 → 0 | 0 | not reproduced |
| 1440px | missing | missing | false | false | 1078 / 1078 | false | false | none | 0 → 0 | 0 | not reproduced |

## Out of scope — awaiting Bret

Axe reports `scrollable-region-focusable` for the three named wrappers at 390 px, and none exposes `role=region` or a non-empty accessible name at any measured width. Chromium itself moves focus to each 390 px overflow wrapper with Tab and ArrowRight scrolls it; 768/1440 px have no overflow and those wrappers are not Tab-reachable. The missing region semantics/name are recorded as a new accessibility issue for Bret; no production edit or test is made in Slice 1.
