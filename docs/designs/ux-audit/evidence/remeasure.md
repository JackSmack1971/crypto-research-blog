# Slice 1 remeasurement — UX-01–06; follow-up CI contrast evidence UX-09

Measured: 2026-11-05T06:11:19.991Z against `http://127.0.0.1:4173`; build: current catalog output (24 articles).

Raw axe JSON and PNG screenshots are local-only under the Git-ignored `screenshots/remeasure-raw/` directory. The committed script is reproducible with the existing dependencies; no production or test files were changed.

## Contrast state matrix

Rows are included for every reproduced contrast state. UX-01 is approved below with its decision date; UX-02, UX-03, and UX-09 remain pending and have blank approval dates.

UX-09 rows record the pre-fix values from `origin/main` baseline `550cce4`, observed by PR #10 styling-check CI. This is historical evidence; the current main article already has a later contrast correction. UX-09 proposals are for Bret's review and do not authorize reverting or changing current source styles.

| Finding | Route | Viewport | Color scheme | Element/selector | Property | Foreground | Effective background | Font size/weight | Observed ratio | Minimum ratio | Proposed foreground (projected ratio) | Approval | Approval date |
|---|---|---:|---|---|---|---|---|---|---:|---:|---|---|---|
| UX-01 | `/404.html` | 390px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | rgb(217, 189, 138) → rgb(29, 92, 85) (`--cr-accent`) / 6.98:1 | approved | 2026-11-05 |
| UX-01 | `/404.html` | 390px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | Same as light; 404 has no dark-specific styles | approved | 2026-11-05 |
| UX-01 | `/404.html` | 768px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | rgb(217, 189, 138) → rgb(29, 92, 85) (`--cr-accent`) / 6.98:1 | approved | 2026-11-05 |
| UX-01 | `/404.html` | 768px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | Same as light; 404 has no dark-specific styles | approved | 2026-11-05 |
| UX-01 | `/404.html` | 1440px | light | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | rgb(217, 189, 138) → rgb(29, 92, 85) (`--cr-accent`) / 6.98:1 | approved | 2026-11-05 |
| UX-01 | `/404.html` | 1440px | dark | `main.wrap.missing > p.kicker:nth-of-type(1)` | color | rgb(217, 189, 138) | rgb(246, 243, 236) | 18px / 700 | 1.63:1 | 4.5:1 | Same as light; 404 has no dark-specific styles | approved | 2026-11-05 |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | light | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | `#6b7e86` → `#64767e` / 4.61:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | dark | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | Same as light; no dark-specific essay styles | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | light | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | `#6b7e86` → `#64767e` / 4.61:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | dark | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | Same as light; no dark-specific essay styles | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | light | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | `#6b7e86` → `#64767e` / 4.61:1 | pending |  |
| UX-02 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | dark | `html > body > header.mast > span:nth-of-type(2)` | color | rgb(107, 126, 134) | rgb(252, 252, 250) | 12px / 700 | 4.13:1 | 4.5:1 | Same as light; no dark-specific essay styles | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | `#c55646` → `#c24d3d` / 4.62:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 390px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | Same as light; no dark-specific essay styles | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | `#c55646` → `#c24d3d` / 4.62:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 768px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | Same as light; no dark-specific essay styles | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | light | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | `#c55646` → `#c24d3d` / 4.62:1 | pending |  |
| UX-03 | `/token-unlock-liquidity-illusion-90-day-calendar/` | 1440px | dark | `html > body > main > article > header.hero > div.kicker:nth-of-type(1)` | color | rgb(197, 86, 70) | rgb(252, 252, 250) | 12px / 700 | 4.26:1 | 4.5:1 | Same as light; no dark-specific essay styles | pending |  |

| UX-09 | `/binance-four-hour-wallet-takeover/` | 390px | light | `header.mast span` | color | rgb(102, 119, 129) | rgb(248, 247, 243) | 13px / 700 | 4.33:1 | 4.5:1 | rgb(102, 119, 129) → `#62727c` / 4.65:1 | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 390px | dark | `header.mast span` | color | rgb(102, 119, 129) | rgb(248, 247, 243) | 13px / 700 | 4.33:1 | 4.5:1 | Same as light; Binance source has no dark-specific styles | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 768px | light | `header.mast span` | color | rgb(102, 119, 129) | rgb(248, 247, 243) | 13px / 700 | 4.33:1 | 4.5:1 | rgb(102, 119, 129) → `#62727c` / 4.65:1 | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 768px | dark | `header.mast span` | color | rgb(102, 119, 129) | rgb(248, 247, 243) | 13px / 700 | 4.33:1 | 4.5:1 | Same as light; Binance source has no dark-specific styles | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 1440px | light | `header.mast span` | color | rgb(102, 119, 129) | rgb(248, 247, 243) | 13px / 700 | 4.33:1 | 4.5:1 | rgb(102, 119, 129) → `#62727c` / 4.65:1 | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 1440px | dark | `header.mast span` | color | rgb(102, 119, 129) | rgb(248, 247, 243) | 13px / 700 | 4.33:1 | 4.5:1 | Same as light; Binance source has no dark-specific styles | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 390px | light | `.kicker` | color | rgb(104, 121, 134) | rgb(248, 247, 243) | 12px / 700 | 4.20:1 | 4.5:1 | rgb(104, 121, 134) → `#62727f` / 4.63:1 | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 390px | dark | `.kicker` | color | rgb(104, 121, 134) | rgb(248, 247, 243) | 12px / 700 | 4.20:1 | 4.5:1 | Same as light; Binance source has no dark-specific styles | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 768px | light | `.kicker` | color | rgb(104, 121, 134) | rgb(248, 247, 243) | 12px / 700 | 4.20:1 | 4.5:1 | rgb(104, 121, 134) → `#62727f` / 4.63:1 | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 768px | dark | `.kicker` | color | rgb(104, 121, 134) | rgb(248, 247, 243) | 12px / 700 | 4.20:1 | 4.5:1 | Same as light; Binance source has no dark-specific styles | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 1440px | light | `.kicker` | color | rgb(104, 121, 134) | rgb(248, 247, 243) | 12px / 700 | 4.20:1 | 4.5:1 | rgb(104, 121, 134) → `#62727f` / 4.63:1 | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 1440px | dark | `.kicker` | color | rgb(104, 121, 134) | rgb(248, 247, 243) | 12px / 700 | 4.20:1 | 4.5:1 | Same as light; Binance source has no dark-specific styles | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 390px | light | `footer.foot` | color | rgb(107, 123, 132) | rgb(248, 247, 243) | 13px / 400 | 4.09:1 | 4.5:1 | rgb(107, 123, 132) → `#64727b` / 4.63:1 | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 390px | dark | `footer.foot` | color | rgb(107, 123, 132) | rgb(248, 247, 243) | 13px / 400 | 4.09:1 | 4.5:1 | Same as light; Binance source has no dark-specific styles | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 768px | light | `footer.foot` | color | rgb(107, 123, 132) | rgb(248, 247, 243) | 13px / 400 | 4.09:1 | 4.5:1 | rgb(107, 123, 132) → `#64727b` / 4.63:1 | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 768px | dark | `footer.foot` | color | rgb(107, 123, 132) | rgb(248, 247, 243) | 13px / 400 | 4.09:1 | 4.5:1 | Same as light; Binance source has no dark-specific styles | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 1440px | light | `footer.foot` | color | rgb(107, 123, 132) | rgb(248, 247, 243) | 13px / 400 | 4.09:1 | 4.5:1 | rgb(107, 123, 132) → `#64727b` / 4.63:1 | pending |  |
| UX-09 | `/binance-four-hour-wallet-takeover/` | 1440px | dark | `footer.foot` | color | rgb(107, 123, 132) | rgb(248, 247, 243) | 13px / 400 | 4.09:1 | 4.5:1 | Same as light; Binance source has no dark-specific styles | pending |  |

### Proposed Slice 2 values and decisions

* UX-01: **approved 2026-11-05**. Change `rgb(217, 189, 138)` to `#1d5c55`, yielding 6.98:1 on the measured `#f6f3ec` background. The exact value previously proposed from `--cr-accent` is approved.
* UX-02: re-propose literal `#6b7e86` → `#64767e`, yielding 4.61:1 on `#fcfcfa`. This is a slight darkening in the same blue-gray hue, with no `var(--cr-*)` reference.
* UX-03: re-propose literal `#c55646` → `#c24d3d`, yielding 4.62:1 on `#fcfcfa`. This darkens the existing rust hue slightly, with no `var(--cr-*)` reference.

* UX-09: proposals are literal same-hue hex values for the three Binance declarations: `#667781` → `#62727c` (4.65:1), `#687986` → `#62727f` (4.63:1), and `#6b7b84` → `#64727b` (4.63:1), each against `#f8f7f3`. UX-09 rows document the pre-fix state from CI base `550cce4`; current `main` already uses `#53636b` for all three declarations after later contrast corrections.

The token-unlock and Binance sources have no dark-specific color styles, so dark-scheme proposals are identical to light. UX-02/03 and UX-09 remain pending Bret approval; their approval dates are blank. Slice 2 is gated on approval of each proposal.

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

### UX-09 — reproduced from PR #10 CI baseline

Route: `/binance-four-hour-wallet-takeover/`; the historical `550cce4` main build failed axe `color-contrast` for the masthead span, `.kicker`, and `footer.foot`. Matrix values are reconstructed from that baseline's article CSS and the CI findings; the current `origin/main` article already uses `#53636b` for all three selectors after a later contrast correction. All three selectors use the same colors at 390/768/1440 px and light/dark emulation because the source has no dark-specific color rules.

The old-to-new values are proposals only. Do not revert or alter the current article source without Bret approving the proposals and checking its current declarations.


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
