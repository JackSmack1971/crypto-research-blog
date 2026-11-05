# Slice 1 remeasurement — UX-01–06

Measured: 2026-11-05T06:11:19.991Z against `http://127.0.0.1:4173`; build: current catalog output (24 articles).

Raw axe JSON and PNG screenshots are local-only under the Git-ignored `screenshots/remeasure-raw/` directory. The committed script is reproducible with the existing dependencies; no production or test files were changed.

## Contrast state matrix

Rows are included for every reproduced contrast state only. Proposed values below are proposals for Slice 2, not approved changes. Approval remains pending for every row; dates remain blank until Bret decides.

| Finding | Route | Viewport | Color scheme | Element/selector | Property | Foreground | Effective background | Font size/weight | Observed ratio | Minimum ratio | Proposed foreground (projected ratio) | Approval | Approval date |
|---|---|---:|---|---|---|---|---|---|---:|---:|---|---|---|
| UX-01 | `/404.html` | 390px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | rgb(217, 189, 138) → rgb(29, 92, 85) (`--cr-accent`) / 6.98:1 | pending |  |
| UX-01 | `/404.html` | 390px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | Same as light; 404 has no dark-specific styles | pending |  |
| UX-01 | `/404.html` | 768px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | rgb(217, 189, 138) → rgb(29, 92, 85) (`--cr-accent`) / 6.98:1 | pending |  |
| UX-01 | `/404.html` | 768px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | Same as light; 404 has no dark-specific styles | pending |  |
| UX-01 | `/404.html` | 1440px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | rgb(217, 189, 138) → rgb(29, 92, 85) (`--cr-accent`) / 6.98:1 | pending |  |
| UX-01 | `/404.html` | 1440px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | Same as light; 404 has no dark-specific styles | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | light | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | rgb(107, 126, 134) → rgb(92, 106, 101) (`--cr-muted`) / 5.52:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | dark | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | Same as light; essay has no dark-specific styles | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | light | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | rgb(107, 126, 134) → rgb(92, 106, 101) (`--cr-muted`) / 5.52:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | dark | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | Same as light; essay has no dark-specific styles | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | light | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | rgb(107, 126, 134) → rgb(92, 106, 101) (`--cr-muted`) / 5.52:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | dark | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | Same as light; essay has no dark-specific styles | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | rgb(197, 86, 70) → rgb(29, 92, 85) (`--cr-accent`) / 7.53:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | Same as light; essay has no dark-specific styles | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | rgb(197, 86, 70) → rgb(29, 92, 85) (`--cr-accent`) / 7.53:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | Same as light; essay has no dark-specific styles | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | rgb(197, 86, 70) → rgb(29, 92, 85) (`--cr-accent`) / 7.53:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | Same as light; essay has no dark-specific styles | pending |  |

### Proposed Slice 2 values (pending Bret approval)

* UX-01: change `rgb(217, 189, 138)` to existing `--cr-accent` (`#1d5c55`), yielding 6.98:1 on the measured `#f6f3ec` background. This reuses the existing accent token and meets the 4.5:1 minimum.
* UX-02: change `rgb(107, 126, 134)` to existing `--cr-muted` (`#5c6a65`), yielding 5.52:1 on the measured `#fcfcfa` background. The token article's muted color resolves to this shared token; it meets the 4.5:1 minimum.
* UX-03: change `rgb(197, 86, 70)` to existing `--cr-accent` (`#1d5c55`), yielding 7.53:1 on the measured `#fcfcfa` background. It meets the 4.5:1 minimum.

The token article defines no dark-specific color styles, so its proposed dark-scheme values are identical to the light-scheme values. No value is approved yet; Slice 2 remains gated on Bret recording approval and date for each matrix row.

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


### UX-04 — reproduced

Route: `/aero-at-0-68/`; wrapper: `.table-scroll`.

| Viewport | Role | Accessible name | Tab-reachable | Programmatic tabindex | Scroll width / client width | Overflow | :focus-visible | Outline | scrollLeft before→after five ArrowRight presses | Axe scroll-region nodes | Result |
|---:|---|---|---|---|---:|---|---|---|---:|---:|---|
| 390px | missing | missing | true | false | 610 / 346 | true | true | rgb(40, 107, 92) solid 3px | 0 → 200 | 1 (`scrollable-region-focusable`) | reproduced: missing region role/name |
| 768px | missing | missing | false | false | 704 / 704 | false | false | none | 0 → 0 | 0 | reproduced: missing region role/name; no overflow |
| 1440px | missing | missing | false | false | 704 / 704 | false | false | none | 0 → 0 | 0 | reproduced: missing region role/name; no overflow |

### UX-05 — reproduced

Route: `/bitcoin-buying-imbalance/`; wrapper: `.tablewrap`.

| Viewport | Role | Accessible name | Tab-reachable | Programmatic tabindex | Scroll width / client width | Overflow | :focus-visible | Outline | scrollLeft before→after five ArrowRight presses | Axe scroll-region nodes | Result |
|---:|---|---|---|---|---:|---|---|---|---:|---:|---|
| 390px | missing | missing | true | false | 540 / 366 | true | true | rgb(32, 94, 84) solid 3px | 0 → 174 | 1 (`scrollable-region-focusable`) | reproduced: missing region role/name |
| 768px | missing | missing | false | false | 718 / 718 | false | false | none | 0 → 0 | 0 | reproduced: missing region role/name; no overflow |
| 1440px | missing | missing | false | false | 870 / 870 | false | false | none | 0 → 0 | 0 | reproduced: missing region role/name; no overflow |

### UX-06 — reproduced

Route: `/token-unlock-liquidity-illusion-90-day-calendar/`; wrapper: `.scroll`.

| Viewport | Role | Accessible name | Tab-reachable | Programmatic tabindex | Scroll width / client width | Overflow | :focus-visible | Outline | scrollLeft before→after five ArrowRight presses | Axe scroll-region nodes | Result |
|---:|---|---|---|---|---:|---|---|---|---:|---:|---|
| 390px | missing | missing | true | false | 590 / 354 | true | true | rgb(16, 16, 16) auto 1px | 0 → 200 | 1 (`scrollable-region-focusable`) | reproduced: missing region role/name |
| 768px | missing | missing | false | false | 718 / 718 | false | false | none | 0 → 0 | 0 | reproduced: missing region role/name; no overflow |
| 1440px | missing | missing | false | false | 1078 / 1078 | false | false | none | 0 → 0 | 0 | reproduced: missing region role/name; no overflow |

## Out of scope — awaiting Bret

No additional out-of-scope findings were recorded in this pass.
