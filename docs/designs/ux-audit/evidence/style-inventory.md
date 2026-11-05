# Style inventory

**Provenance and retention:** This inventory was derived from `evidence/scripts/style-inventory.mjs`, `build.py`, `assets/design-system.css`, `assets/search.js`, `content/articles.json`, and the 20 catalog HTML sources under `content/`. Raw PNG and JSON capture output is local-only and ignored by Git.

## Generated shared chrome

`build.py` copies `assets/design-system.css` to `dist/design-system.css`; articles link it after their source styles, and generated home/404 pages also link it. Search behavior is in `assets/search.js`; it changes visibility/order and URL parameters, while its visual rules remain in the shared stylesheet.

### Tokens (`:root`)

| Token group | Values |
| --- | --- |
| Colors | `--cr-bg: #f6f3ec`; `--cr-ink: #1b2422`; `--cr-muted: #5c6a65`; `--cr-accent: #1d5c55`; `--cr-line: #e3dbd0`; `--cr-bar: #172420`; `--cr-bar-text: #f4f1ea`; `--cr-bar-muted: #d5ddd8`; focus: `#1d5c55` / bar focus `#e6d3ae` |
| Type | Serif: Iowan Old Style, Palatino Linotype, Palatino, Georgia; sans: system-ui, -apple-system, Segoe UI |
| Measures | `--cr-measure: 47.5rem`; `--cr-container: 72.5rem`; breakpoint `--cr-break: 640px` |

### Site bar

Dark `#172420` bar; system sans 13px/1.3 with 0.01em letter spacing. Inner container max 72.5rem, centered, 10px 20px padding, 16px gap. Text #f4f1ea, secondary link #d5ddd8, 2px visible focus outline #e6d3ae.

### Home and 404 base

Paper background `#f6f3ec`, ink `#1b2422`, serif 18px/1.55, top border 6px dark. Main content measure 55rem with 20px side gutters (mobile: 16px); mobile breakpoint 640px. Masthead, archive, card grid and the filters share this scoped stylesheet. The masthead is dark; controls use system sans. Search form is grid based and collapses to one column below 640px; empty-state uses 22px padding and a 1px decorative border.

### Search behavior and presentation

The generated form exposes a text query, topic select, research-type select and reset. `search.js` matches ticker/title/dek/topic, applies combined filters, updates a live status/count and empty state, and reflects current controls in query parameters. All visual control and state rules are under `body.cr-home` in `design-system.css`; there is no separate search stylesheet.

## Article source style blocks

Values below are unique declarations found in each source article's inline `<style>` blocks. Lists omit a category only if the source has no declaration for it. Exact values are retained; `var()` references depend on that article's local custom properties. This is a source inventory, not a claim that every declared rule is active at every viewport.

### [aero-at-0-68.html](../../../../content/aero-at-0-68.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `var(--cr-ink,#202a2a)`; `--muted`: `var(--cr-muted,#65706d)`; `--accent`: `var(--cr-accent,#9c503a)`; `--paper`: `var(--cr-bg,#fcfaf6)`; `--line`: `var(--cr-line,#d9d9d2)`; `--shade`: `#f1f0e9`; `--green`: `#286b5c`; `--serif`: `var(--cr-serif,Georgia,'Times New Roman',serif)`; `--sans`: `var(--cr-sans,Arial,Helvetica,sans-serif)`
- **Font sizes:** `4.3em`, `11px`, `17px`, `18px`, `clamp(41px,11vw,64px)`, `32px`, `25px`, `10px`, `3.4em`, `clamp(23px,6vw,32px)`, `clamp(34px,10.5vw,41px)`
- **Line heights:** `.81`, `1.6`, `1.65`
- **Text colors:** `var(--ink)`, `var(--cr-accent,#80513e)`, `var(--cr-ink,#482e27)`, `var(--muted)`, `var(--accent)`, `#4e5854`, `#3a4741`
- **Backgrounds:** `var(--paper)`, `white`, `var(--shade)`, `#f3f1eb`
- **Max widths:** `1140px`, `890px`, `780px`, `var(--cr-measure,760px)`, `1050px`, `800px`, `100%`
- **Margins:** `0`, `auto`, `20px 0 25px`, `32px auto 0`, `0 auto`, `0 0 24px`, `63px 0 23px`, `40px 0 15px`, `36px auto 48px`, `37px 0 47px`, `44px 0`, `36px 0`, `32px 0 42px`, `0 0 14px`, `0 0 10px`
- **Margin top:** `27px`, `8px`, `60px`, `70px`, `10px`, `47px`
- **Margin right:** `auto`
- **Margin bottom:** `10px`
- **Margin left:** `auto`
- **Padding:** `17px 5%`, `78px 28px 43px`, `0 28px`, `0 26px`, `5px 0 5px 27px`, `24px 15px 24px 0`, `14px 13px`, `32px 5%`, `22px 25px`, `55px 21px 29px`, `0 22px`, `0 12px`, `15px 20px`, `10px 14px`, `16px 0`, `0 18px`
- **Padding top:** `12px`, `24px`
- **Padding right:** `10px`, `18px`
- **Padding left:** `24px`, `20px`, `0`, `18px`, `16px`
- **Gaps:** `0`, `24px`, `10px`, `12px`

### [bitcoin-buying-imbalance.html](../../../../content/bitcoin-buying-imbalance.html)

Inline style blocks: 1.
- **Local custom properties:** `--paper`: `var(--cr-bg,#faf9f6)`; `--ink`: `var(--cr-ink,#202923)`; `--muted`: `var(--cr-muted,#5d6a62)`; `--line`: `var(--cr-line,#d8ded8)`; `--green`: `#2e7167`; `--rust`: `#ac6959`; `--wash`: `#eff2ed`; `--serif`: `var(--cr-serif,Georgia,"Iowan Old Style","Palatino Linotype",serif)`; `--sans`: `var(--cr-sans,Arial,Helvetica,sans-serif)`
- **Fonts:** `var(--serif)`, `var(--sans)`, `Georgia,serif`
- **Font sizes:** `12px`, `11px`, `clamp(3.25rem,7vw,6.35rem)`, `clamp(1.2rem,2.5vw,1.65rem)`, `19px`, `3.3em`, `clamp(2rem,4vw,2.8rem)`, `1.55rem`, `clamp(1.5rem,3.3vw,2.1rem)`, `24px`, `10px`, `clamp(3rem,11.5vw,4.3rem)`, `17.5px`, `15px`, `clamp(2.65rem,10.5vw,4.3rem)`
- **Line heights:** `1.06`, `1.4`, `1.84`, `.88`, `1.19`, `1.75`, `1.7`
- **Text colors:** `var(--ink)`, `var(--cr-accent,#25655b)`, `var(--cr-ink,#173f39)`, `var(--muted)`, `var(--green)`, `#526157`, `#31544c`, `#526158`, `#53635a`, `#233c34`
- **Backgrounds:** `var(--paper)`, `var(--green)`, `var(--rust)`, `#edf1eb`
- **Max widths:** `1180px`, `1050px`, `970px`, `790px`, `var(--cr-measure,740px)`, `1060px`, `870px`, `100%`, `920px`, `1000px`, `740px`, `720px`
- **Margins:** `0`, `auto`, `0 auto`, `0 0 23px`, `0 0 25px`, `0 0 32px`, `42px 0 0`, `0 0 26px`, `68px 0 24px`, `39px 0 18px`, `48px 0`, `60px auto`, `0 0 52px`, `16px auto 0`, `0 0 16px`, `50px auto`, `15px 0`, `0 auto 50px`, `70px 0 0`, `0 0 21px`, `0 0 15px`
- **Margin top:** `6px`
- **Margin right:** `7px`, `14px`
- **Margin bottom:** `6px`
- **Margin left:** `14px`
- **Padding:** `22px 28px`, `85px 28px 64px`, `0 25px`, `4px 0 4px 29px`, `17px 15px`, `15px`, `24px 25px`, `14px 12px`, `58px 25px`, `0`, `62px 25px 100px`, `17px 20px`, `58px 22px 40px`, `0 22px`, `13px 22px`, `0 10px`, `0 12px`, `45px 0`, `45px 22px 70px`, `12px 16px`
- **Padding top:** `20px`
- **Padding right:** `10px`, `18px`
- **Padding left:** `19px`, `18px`
- **Gaps:** `18px`, `22px`, `0`

### [bitcoin-holding-up.html](../../../../content/bitcoin-holding-up.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `var(--cr-ink,#17242a)`; `--muted`: `var(--cr-muted,#596a70)`; `--paper`: `var(--cr-bg,#fbfaf7)`; `--rule`: `var(--cr-line,#d7ddd9)`; `--teal`: `#245d59`; `--red`: `#a54b42`; `--ochre`: `#9d7237`; `--pale`: `#eef2ef`; `--wide`: `1080px`; `--serif`: `var(--cr-serif,Georgia,'Times New Roman',serif)`; `--sans`: `var(--cr-sans,system-ui,sans-serif)`
- **Fonts:** `var(--serif)`, `var(--sans)`
- **Font sizes:** `19px`, `clamp(3.1rem,7vw,6.1rem)`, `clamp(1.3rem,2.35vw,1.7rem)`, `4.8em`, `clamp(2rem,4vw,3rem)`, `clamp(1.5rem,3vw,2rem)`, `12px`, `1.8rem`, `31px`, `17px`, `10px`, `clamp(2.75rem,13vw,4.2rem)`, `1.23rem`, `11px`, `4em`, `1.45rem`
- **Line heights:** `1.72`, `1.03`, `1.47`, `.8`, `1.14`, `1.38`, `1.7`
- **Text colors:** `var(--ink)`, `var(--teal)`, `#153f3c`, `var(--muted)`, `#45575c`, `var(--red)`, `inherit`, `#46565a`, `var(--cr-accent,#245d59)`, `#526064`, `#111`
- **Backgrounds:** `var(--paper)`, `#f0f3f0`, `var(--teal)`, `#ad7653`, `#dce5df`, `var(--red)`, `#e1eae5`, `#bfd5cb`, `#9cc3b5`, `#d8e5df`, `#fff`, `#f4f4f4`
- **Max widths:** `var(--wide)`, `980px`, `900px`, `760px`, `var(--cr-measure,730px)`, `none`, `100%`
- **Margins:** `0`, `auto`, `0 auto`, `22px 0 28px`, `0 0 1.42em`, `2.5em 0 .7em`, `2em 0 .8em`, `56px -90px 62px`, `0 0 8px`, `0 0 24px`, `2.1em -55px`, `35px 0 50px`, `15px 0`, `34px 0`, `100px auto 65px`, `0 0 18px`, `60px 0 20px`
- **Margin top:** `34px`, `16px`, `65px`
- **Margin right:** `6px`
- **Margin bottom:** `10px`, `12px`
- **Margin inline:** `-18px`, `0`, `-20px`
- **Padding:** `24px 28px 18px`, `82px 28px 55px`, `0 28px`, `.09em .1em 0 0`, `28px 30px 23px`, `12px 13px 12px 0`, `13px 13px 13px 0`, `23px 0 24px 30px`, `20px 18px`, `13px 7px`, `18px 0`, `20px 28px 50px`, `22px 18px`, `16px 18px`, `55px 20px 30px`, `0 20px`, `15px 10px`, `20px`, `10px 4px`, `10px 14px`, `12px 14px`, `18px 12px`, `9px 7px`
- **Padding top:** `18px`, `28px`
- **Padding left:** `0`, `22px`
- **Gaps:** `20px`, `10px 22px`, `0`, `16px`, `12px`, `7px`, `4px 16px`, `5px`

### [bitcoin-quiet-divergence.html](../../../../content/bitcoin-quiet-divergence.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `#172934`; `--muted`: `#54646b`; `--paper`: `#f7f5f0`; `--line`: `#d4d9d7`; `--accent`: `#876344`; `--negative`: `#9c4d43`; `--positive`: `#315f62`
- **Fonts:** `Georgia,'Times New Roman',serif`, `system-ui,sans-serif`
- **Font sizes:** `clamp(2.7rem,6vw,5.4rem)`, `clamp(1.9rem,3.5vw,2.7rem)`, `1.35rem`, `clamp(1.15rem,2vw,1.5rem)`, `4.6em`, `clamp(1.5rem,3vw,2rem)`, `11px`, `17px`
- **Line heights:** `1.12`, `1.45`, `.78`, `1.35`
- **Text colors:** `var(--ink)`, `#275c69`, `var(--muted)`, `var(--accent)`, `#465960`, `var(--negative)`, `var(--positive)`, `#4c5c63`, `inherit`
- **Backgrounds:** `var(--paper)`, `#eeede7`, `#ecece6`, `white`
- **Max widths:** `900px`, `790px`, `1120px`, `760px`, `100%`
- **Margins:** `0`, `72px auto 30px`, `18px 0 22px`, `64px 0 22px`, `38px 0 14px`, `0 auto 50px`, `9px 0 0`, `0 auto`, `0 0 25px`, `58px 0`, `50px -40px`, `40px 0 44px`, `40px 0`, `50px 0`
- **Margin top:** `26px`, `10px`, `90px`, `42px`
- **Margin bottom:** `12px`, `0`, `34px`
- **Margin inline:** `auto`, `0`
- **Padding:** `20px 0`, `.11em .1em 0 0`, `12px 0 12px 26px`, `14px 10px`, `24px 28px`, `28px 0 70px`, `20px`

### [bitcoin-rebound-spot-demand.html](../../../../content/bitcoin-rebound-spot-demand.html)

Inline style blocks: 1.
- **Local custom properties:** `--paper`: `#f8f7f3`; `--ink`: `#202722`; `--muted`: `#667068`; `--rule`: `#d7d9d2`; `--rust`: `#8f4c36`; `--teal`: `#286f71`; `--white`: `#fff`; `--sand`: `#efeee8`
- **Font sizes:** `clamp(21px,2.5vw,26px)`, `3.1em`, `clamp(25px,3vw,33px)`, `12px`, `13px`, `11px`, `26px`, `17px`, `29px`, `20px`, `27px`, `31px`, `11pt`, `clamp(35px,9vw,52px)`
- **Line heights:** `1.58`, `.85`, `1.65`, `1.7`, `1.9`
- **Text colors:** `var(--ink)`, `#3c5146`, `var(--muted)`, `var(--rust)`, `#52615a`, `#abb1a9`, `var(--teal)`, `#35463d`, `#68716a`, `#56645a`, `#5a685d`, `#526259`, `var(--white)`
- **Backgrounds:** `var(--paper)`, `#d8e8df`, `var(--rule)`, `#edeee8`, `#eeefea`, `#fff`, `var(--ink)`
- **Max widths:** `1180px`, `990px`, `1040px`, `790px`, `810px`, `735px`, `1020px`, `800px`, `1010px`, `970px`, `100%`
- **Margins:** `0`, `0 auto`, `91px auto 76px`, `24px auto 27px`, `0 auto 34px`, `52px auto 0`, `0 0 27px`, `7px 9px 0 0`, `77px 0 29px`, `45px 0 18px`, `56px -48px`, `60px auto 69px`, `10px 0 24px`, `8px 0 10px`, `8px 0 20px`, `58px auto 68px`, `46px auto 53px`, `31px 0 36px`, `47px auto 50px`, `0 0 15px`, `88px auto 58px`, `0 0 20px`, `58px auto 43px`, `44px 0`, `32px auto`
- **Margin top:** `9px`, `68px`, `60px`, `39px`
- **Margin right:** `8px`, `0`
- **Margin bottom:** `9px`, `11px`, `12px`
- **Margin left:** `0`
- **Padding:** `21px 25px`, `0 28px`, `0 12px`, `4px 0 5px 29px`, `35px 35px 25px`, `30px 0`, `17px 18px`, `14px 16px 17px`, `6px 0 6px 20px`, `22px 25px`, `39px 0 14px`, `25px`, `0 21px`, `17px`, `0 6px`, `27px 0 19px`, `22px`, `10px`, `10px 16px`, `0 4px`
- **Padding top:** `11px`, `28px`
- **Padding bottom:** `18px`
- **Padding left:** `20px`
- **Gaps:** `16px`, `22px`, `30px`, `28px`, `18px`, `9px`

### [bitcoin-recovery-beneath-resistance.html](../../../../content/bitcoin-recovery-beneath-resistance.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `#182532`; `--muted`: `#506171`; `--paper`: `#fcfbf8`; `--line`: `#d9dedf`; `--accent`: `#97602b`
- **Font sizes:** `clamp(2.5rem,6vw,4.5rem)`, `clamp(1.65rem,3vw,2.15rem)`, `1.25rem`, `1.3rem`, `17px`, `1.1rem`
- **Line heights:** `1.08`, `1.2`, `1.35`, `1.48`
- **Text colors:** `var(--ink)`, `#255a72`, `var(--accent)`, `var(--muted)`, `#263d49`, `#3d4e5a`
- **Backgrounds:** `var(--paper)`, `#edf0ed`
- **Max widths:** `1140px`, `770px`
- **Margins:** `0`, `auto`, `0 auto`, `14px 0 24px`, `54px 0 18px`, `30px 0 12px`, `0 0 24px`, `0 0 34px`, `0 0 46px`, `0 0 23px`, `35px 0`, `28px 0 30px`, `38px 0`
- **Margin top:** `9px`
- **Padding:** `0 28px`, `20px 0`, `60px 0 110px`, `6px 0 6px 23px`, `0 0 12px`, `12px 13px`, `18px 0`, `0 18px`
- **Padding top:** `24px`, `35px`

### [bitcoin-selloff-leverage.html](../../../../content/bitcoin-selloff-leverage.html)

Inline style blocks: 1.
- **Local custom properties:** `--paper`: `#f7f5f0`; `--ink`: `#202723`; `--muted`: `#626b65`; `--rule`: `#d6d9d1`; `--accent`: `#7e3e2e`; `--soft`: `#ebe9e1`; `--green`: `#365b4a`
- **Fonts:** `Georgia,'Times New Roman',serif`
- **Font sizes:** `clamp(3rem,6.6vw,6.3rem)`, `clamp(1.25rem,2.2vw,1.7rem)`, `19px`, `24px`, `clamp(2rem,3.8vw,3rem)`, `11px`, `clamp(1.6rem,3vw,2.2rem)`, `23px!important`, `17px`, `21px`, `25px`, `20px`, `10px`, `clamp(2.55rem,10vw,3.25rem)`, `clamp(1.85rem,8vw,2.4rem)`, `1.65rem`
- **Line heights:** `1.035`, `1.43`, `1.77`, `1.59`, `1.13`, `1.34`, `1.58!important`, `1.75`
- **Text colors:** `var(--ink)`, `var(--accent)`, `#54281e`, `var(--muted)`, `#505b54`, `#4d5851`, `inherit`, `var(--paper)`
- **Backgrounds:** `var(--paper)`, `var(--ink)`, `#e5e4dc`, `var(--accent)`, `var(--green)`, `#fff`
- **Max widths:** `1160px`, `950px`, `790px`, `760px`, `740px`, `100%`
- **Margins:** `0`, `auto`, `88px auto 55px`, `0 0 24px`, `0 0 27px`, `0 0 34px`, `0 auto`, `65px auto 90px`, `0 0 25px`, `75px 0 23px`, `42px 0 16px`, `48px -90px 55px`, `0 0 8px`, `0 0 26px`, `30px 0`, `14px 0`, `10px 0 20px`, `36px -50px 44px`, `52px -60px`, `0 0 18px`, `54px auto 40px`, `45px auto 60px`, `-1px`
- **Margin top:** `20px`, `7px`, `80px`, `55px`, `35px`
- **Margin right:** `6px`, `0`
- **Margin bottom:** `15px`, `13px`
- **Margin left:** `0`
- **Padding:** `18px 28px`, `0 28px`, `0 25px`, `24px 0 20px`, `4px 0 4px 16px`, `15px 13px`, `28px 0 29px 28px`, `30px 28px 50px`, `15px 18px`, `0 19px`, `0 20px`, `12px 16px`, `0`
- **Padding top:** `18px`, `22px`
- **Padding left:** `21px`, `18px`
- **Gaps:** `25px`, `14px`, `20px`, `18px`, `8px`, `10px`, `7px`

### [crypto-breadth-beneath-bitcoin.html](../../../../content/crypto-breadth-beneath-bitcoin.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `#17282c`; `--muted`: `#526267`; `--paper`: `#faf8f3`; `--accent`: `#915a32`; `--rule`: `#d8d9d1`
- **Font sizes:** `clamp(2.65rem,6vw,5.5rem)`, `clamp(1.7rem,3vw,2.4rem)`, `clamp(1.2rem,2vw,1.5rem)`, `4.1em`, `32px`, `12px`, `1.45em`, `17px`, `1.22em`
- **Line heights:** `1.08`, `1.19`, `1.5`, `.85`, `1.2`, `1.4`
- **Text colors:** `var(--ink)`, `#79502d`, `var(--muted)`, `var(--accent)`, `#425359`, `#20383a`, `#4b6062`
- **Backgrounds:** `var(--paper)`
- **Max widths:** `1120px`, `890px`, `760px`, `100%`
- **Margins:** `0`, `auto`, `64px auto 32px`, `19px 0 22px`, `2.4em 0 .65em`, `2em 0 .6em`, `0 0 26px`, `35px auto 0`, `10px 0`, `55px auto 100px`, `0 0 1.3em`, `36px 0`, `6px 0`, `40px 0`, `2.5em 0`
- **Margin top:** `14px`, `65px`, `38px`, `2em`
- **Margin bottom:** `10px`
- **Padding:** `0 28px`, `22px 0`, `9px 10px 0 0`, `12px`, `4px 0 4px 24px`, `30px 0`
- **Padding top:** `18px`
- **Padding right:** `18px`
- **Padding left:** `18px`
- **Gaps:** `1em`

### [crypto-buybacks.html](../../../../content/crypto-buybacks.html)

Inline style blocks: 1.
- **Local custom properties:** `--paper`: `var(--cr-bg,#f8f6f0)`; `--ink`: `var(--cr-ink,#242824)`; `--muted`: `var(--cr-muted,#5d645e)`; `--line`: `var(--cr-line,#d9d9cf)`; `--accent`: `var(--cr-accent,#30584c)`; `--soft`: `#edf0e9`; `--serif`: `var(--cr-serif,Georgia,'Times New Roman',serif)`; `--sans`: `var(--cr-sans,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif)`
- **Fonts:** `var(--sans)`, `var(--serif)`
- **Font sizes:** `19px`, `11px`, `12px`, `clamp(45px,6.8vw,88px)`, `24px`, `77px`, `18px`, `21px`, `64px`, `26px`
- **Line heights:** `1.045`, `1.58`, `.81`, `1.72`
- **Text colors:** `var(--ink)`, `var(--accent)`, `var(--muted)`, `#4c544e`, `inherit`
- **Backgrounds:** `var(--paper)`, `var(--soft)`, `var(--line)`, `white`
- **Max widths:** `var(--cr-container,1160px)`, `1050px`, `1010px`, `780px`, `var(--cr-measure,740px)`
- **Margins:** `0`, `auto`, `0 auto`, `0 0 26px`, `29px 0 31px`, `0 0 25px`, `76px 0 25px`, `38px 0 17px`, `60px -65px`, `48px 0 15px`, `12px 0 34px!important`, `38px 0 15px`, `46px 0`, `55px 0`, `0 0 18px`, `0 0 11px`, `-1px`, `38px 0 12px`, `24px 0`, `28px 0`
- **Margin top:** `3px`, `8px`, `76px`, `23px`, `7px`
- **Margin right:** `0`
- **Margin bottom:** `15px`, `11px`, `7px`
- **Margin left:** `0`
- **Padding:** `22px 32px`, `0 24px`, `92px 0 64px`, `65px 0 100px`, `10px 12px 0 0`, `26px 0 26px 29px`, `24px 16px 24px 0`, `16px 0`, `15px 14px 15px 0`, `28px 30px`, `28px 24px 45px`, `0`, `0 19px`, `18px 19px`, `22px 20px`, `14px 10px 14px 0`, `22px 24px`, `18px`
- **Padding top:** `28px`, `68px`, `48px`, `57px`, `35px`
- **Padding bottom:** `45px`, `25px`
- **Padding left:** `20px`, `22px`, `0`, `19px`
- **Gaps:** `16px`, `18px`, `0`, `10px 16px`, `10px`, `12px`

### [deepbook-supply-transparency.html](../../../../content/deepbook-supply-transparency.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `#182a33`; `--muted`: `#53636a`; `--paper`: `#fbfaf7`; `--rule`: `#d7dbd9`; `--gold`: `#916a35`; `--navy`: `#12212c`
- **Font sizes:** `clamp(2.45rem,6vw,4.5rem)`, `3.8em`, `clamp(1.75rem,4vw,2.45rem)`, `1.35rem`, `1.15rem`, `30px`, `17px`
- **Line heights:** `1.11`, `.8`, `1.2`, `1.3`, `1.7`
- **Text colors:** `var(--ink)`, `#135a71`, `#943f28`, `var(--gold)`, `var(--muted)`, `#f5f0e5`, `#d0dadd`, `#c9d2d5`
- **Backgrounds:** `var(--paper)`, `#f1efe8`, `#eeefeb`, `#172a35`, `#354a54`, `#d6b47d`, `var(--navy)`
- **Max widths:** `1130px`, `850px`, `760px`
- **Margins:** `0`, `auto`, `18px 0 23px`, `28px 0 32px`, `0 0 36px`, `58px 0 18px`, `34px 0 12px`, `0 0 23px`, `38px 0`, `28px 0 12px`, `36px 0`, `0 0 15px`, `0 0 12px`, `40px`
- **Margin top:** `55px`, `10px`, `14px`, `38px`, `15px`, `43px`
- **Margin bottom:** `5px`
- **Padding:** `24px 28px`, `0 26px 80px`, `14px 0`, `9px 9px 0 0`, `20px 25px`, `15px 13px`, `25px`, `28px`, `0 18px 50px`, `18px`, `17px`
- **Padding top:** `20px`
- **Padding left:** `22px`
- **Gaps:** `15px`, `12px`

### [institutional-adoption-token-demand.html](../../../../content/institutional-adoption-token-demand.html)

Inline style blocks: 1.
- **Local custom properties:** `--paper`: `#f8f7f3`; `--ink`: `#202725`; `--muted`: `#58645f`; `--line`: `#d7dcd5`; `--accent`: `#245c52`; `--wash`: `#e9efea`; `--red`: `#a64d40`
- **Fonts:** `Georgia,"Times New Roman",serif`, `Arial,Helvetica,sans-serif`, `"Courier New",monospace`
- **Font sizes:** `12px`, `clamp(38px,6vw,76px)`, `clamp(20px,2.3vw,28px)`, `19px`, `82px`, `clamp(31px,3.4vw,43px)`, `24px`, `11px`, `15px`, `clamp(24px,3vw,32px)`, `30px`, `24px!important`, `10px`, `clamp(34px,9vw,43px)`, `18px`, `clamp(21px,6vw,27px)`, `66px`
- **Line heights:** `1.08`, `1.43`, `1.7`, `.78`, `1.15`, `1.55`, `1.6`, `1.35`, `1.55!important`
- **Text colors:** `var(--ink)`, `var(--accent)`, `var(--muted)`, `#45514c`, `var(--red)`
- **Backgrounds:** `var(--paper)`, `#e4e8e2`, `var(--accent)`, `var(--red)`, `#8ca79b`, `var(--wash)`
- **Max widths:** `1120px`, `1030px`, `810px`, `70ch`, `100%`
- **Margins:** `0`, `auto`, `24px 0 26px`, `0 0 26px`, `65px 0 23px`, `36px 0 15px`, `12px 0`, `42px 0 44px`, `0 0 8px`, `0 0 23px`, `36px 0`, `10px 0`, `35px 0 14px`, `48px 0`, `27px 0`, `26px 0`, `0 0 20px`
- **Margin top:** `32px`, `15px`, `68px`, `65px`
- **Margin bottom:** `35px`, `12px`, `6px`
- **Padding:** `0 34px`, `12px 18px`, `22px 0 18px`, `80px 0 56px`, `10px 9px 0 0`, `27px 0`, `13px 10px 13px 0`, `10px 0 10px 28px`, `19px 22px`, `22px 0 50px`, `55px 0 40px`, `0 24px`, `0 19px`, `43px 0 34px`
- **Padding top:** `56px`, `10px`, `15px`, `14px`, `11px`, `25px`, `0`
- **Padding left:** `20px`
- **Gaps:** `15px`, `clamp(28px,5vw,75px)`, `17px`, `13px`, `18px`, `10px`, `20px`, `8px`

### [pyth-revenue-unlock.html](../../../../content/pyth-revenue-unlock.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `var(--cr-ink,#192532)`; `--soft`: `#4e5a66`; `--dim`: `var(--cr-muted,#667480)`; `--paper`: `var(--cr-bg,#fbfaf7)`; `--line`: `var(--cr-line,#dedbd4)`; `--accent`: `var(--cr-accent,#1c625e)`; `--light`: `#e7efeb`; `--ochre`: `var(--cr-focus,#ad5c2f)`; `--white`: `#fff`; `--serif`: `var(--cr-serif,Georgia,'Times New Roman',serif)`; `--sans`: `var(--cr-sans,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif)`
- **Fonts:** `var(--serif)`
- **Font sizes:** `12px`, `1.25em`, `11px`, `.92em`, `clamp(2.9rem,12vw,4.7rem)`, `1.22rem`, `17px`, `4.7rem`, `2.15rem`, `1.38rem`, `clamp(2.55rem,12vw,3.4rem)`
- **Line heights:** `1.65`, `1.77`
- **Text colors:** `var(--ink)`, `var(--accent)`, `var(--cr-ink,#113d3b)`, `var(--white)`, `var(--dim)`, `var(--soft)`, `#435864`, `inherit`
- **Backgrounds:** `var(--paper)`, `var(--ink)`, `white`, `#ecefeb`
- **Max widths:** `1000px`, `960px`, `790px`, `1030px`, `none`, `900px`, `720px`
- **Margins:** `0`, `auto`, `0 auto`, `23px 0 28px`, `52px auto`, `0 0 1.45em`, `2.25em 0 .68em`, `2em 0 .7em`, `0 0 17px`, `2.6em 0`, `2.45em 0 2.5em`, `2em 0`, `1.7em 0 2em`, `40px`
- **Margin top:** `30px`, `8px`, `32px`
- **Margin bottom:** `10px`
- **Margin left:** `50%`, `0`
- **Padding:** `10px 14px`, `17px 28px`, `82px 0 56px`, `12px 12px 0 0`, `11px 0`, `24px 3px 28px`, `11px 2px`, `19px 12px 16px 0`, `12px 14px`, `8px 0 8px 21px`, `35px 0 65px`, `22px 24px`, `14px 15px`, `52px 0 35px`
- **Padding top:** `19px`, `25px`
- **Padding left:** `18px`, `0`
- **Gaps:** `20px`, `84px`, `0`, `8px 18px`

### [rune-quiet-repricing.html](../../../../content/rune-quiet-repricing.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `var(--cr-ink,#202b31)`; `--muted`: `var(--cr-muted,#52646b)`; `--paper`: `var(--cr-bg,#faf9f5)`; `--line`: `var(--cr-line,#d6d9d5)`; `--accent`: `var(--cr-accent,#1f5960)`; `--tint`: `#edf1ee`; `--serif`: `var(--cr-serif,Georgia,'Times New Roman',serif)`; `--sans`: `var(--cr-sans,system-ui,sans-serif)`
- **Fonts:** `var(--serif)`
- **Font sizes:** `19px`, `clamp(2.7rem,7vw,5.15rem)`, `clamp(1.2rem,2.35vw,1.48rem)`, `1.15em`, `clamp(1.75rem,3.2vw,2.35rem)`, `1.25rem`, `1.32em`, `11px`, `17px`, `1.22em`, `12pt`
- **Line heights:** `1.72`, `1.07`, `1.53`, `1.2`, `1.3`, `1.43`, `1.66`
- **Text colors:** `var(--ink)`, `var(--accent)`, `var(--cr-ink,#113c41)`, `var(--paper)`, `var(--muted)`, `inherit`
- **Backgrounds:** `var(--paper)`, `var(--ink)`, `white`
- **Max widths:** `1120px`, `var(--cr-measure,760px)`, `790px`, `680px`, `760px`
- **Margins:** `0`, `auto`, `0 auto`, `0 0 26px`, `29px 0 27px`, `0 0 1.35em`, `2.0em 0 .7em`, `1.7em 0 .6em`, `53px 0`, `38px 0 42px`, `38px 0 38px`, `35px 0 43px`, `0 0 18px`
- **Margin top:** `51px`, `17px`, `10px`, `-15px`, `78px`, `35px`, `1.8em`
- **Margin bottom:** `10px`
- **Padding:** `10px 14px`, `20px 28px`, `84px 26px 105px`, `13px 0`, `8px 0 7px 24px`, `26px 0`, `16px 14px 16px 0`, `23px 26px 48px`, `57px 22px 70px`, `18px 22px`, `30px 0`, `12px 0`
- **Padding top:** `10px`, `25px`
- **Padding left:** `21px`, `6px`, `17px`
- **Gaps:** `24px`, `8px 22px`, `20px`, `25px 14px`

### [small-cap-crypto-liquidity-illusion.html](../../../../content/small-cap-crypto-liquidity-illusion.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `#20313a`; `--sub`: `#53626a`; `--paper`: `#fbfaf6`; `--line`: `#d9ded9`; `--accent`: `#a66f38`; `--forest`: `#426b69`; `--wide`: `1050px`
- **Font sizes:** `11px`, `12px`, `17px`, `2.6rem`, `1.35rem`
- **Text colors:** `var(--ink)`, `#376763`, `var(--forest)`, `#7c542f`, `#45565c`, `#677575`, `var(--sub)`, `var(--accent)`, `#344e51`, `#344e4d`, `#435157`
- **Backgrounds:** `var(--paper)`, `#f3f3ed`, `#eef0e9`
- **Max widths:** `800px`, `680px`
- **Margins:** `0`, `auto`, `17px 0 20px`, `13px 0 38px`, `0 0 1.3em`, `2.4em 0 .65em`, `1.7em 0 .6em`, `38px 0`, `38px -20px`, `31px 0 10px`, `0 0 12px`, `34px 0`, `-1px`, `28px -8px`
- **Margin top:** `10px`, `60px`
- **Padding:** `18px 20px`, `0 26px 95px`, `62px 0 25px`, `.07em .1em 0 0`, `7px 0 7px 24px`, `23px 17px`, `13px 12px`, `0`, `0 18px 70px`, `14px 8px`
- **Padding top:** `22px`, `39px`
- **Padding bottom:** `12px`
- **Padding left:** `23px`

### [solz-launch-investigation.html](../../../../content/solz-launch-investigation.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `#20251f`; `--muted`: `#60685e`; `--paper`: `#f8f7f2`; `--line`: `#d8d9d0`; `--accent`: `#385b49`; `--soft`: `#e9eee8`; `--gold`: `#967445`
- **Fonts:** `Georgia,'Times New Roman',serif`, `Arial,Helvetica,sans-serif`
- **Font sizes:** `19px`, `12px`, `11px`, `clamp(45px,7vw,92px)`, `clamp(21px,2.4vw,28px)`, `4.3em`, `clamp(31px,4vw,44px)`, `clamp(24px,3vw,34px)`, `14px`, `17px`, `10px`
- **Line heights:** `1.7`, `1.02`, `1.45`, `.8`, `1.16`, `1.35`
- **Text colors:** `var(--ink)`, `var(--accent)`, `#183d29`, `var(--muted)`, `#475247`, `inherit`
- **Backgrounds:** `var(--paper)`, `var(--soft)`, `#fbfbf8`, `#e3e6df`, `var(--accent)`, `#a87d51`, `#eceee7`, `#fff`
- **Max widths:** `1060px`, `1000px`, `820px`, `740px`, `780px`
- **Margins:** `0`, `0 auto`, `0 0 28px`, `0 0 34px`, `0 0 25px`, `72px 0 24px`, `42px 0 14px`, `42px 0 44px`, `42px 0`, `48px 0`, `38px 0`, `0 0 20px`
- **Margin top:** `12px`, `7px`, `65px`
- **Margin bottom:** `24px`, `11px`
- **Padding:** `19px 24px`, `90px 28px 48px`, `0 24px 100px`, `9px 10px 0 0`, `22px 16px`, `14px 12px`, `13px 12px`, `10px 0 10px 28px`, `25px 30px`, `25px`, `2px 4px`, `56px 22px 32px`, `0 22px 70px`, `16px`
- **Padding top:** `20px`, `45px`
- **Padding left:** `21px`, `17px`
- **Gaps:** `16px`, `0`, `19px`, `12px`, `7px`

### [token-unlock-liquidity-illusion-90-day-calendar.html](../../../../content/token-unlock-liquidity-illusion-90-day-calendar.html)

Inline style blocks: 2.
- **Local custom properties:** `--ink`: `#142b36`; `--muted`: `#536771`; `--rust`: `#c55646`; `--border`: `#dce3e5`; `--paper`: `#fcfcfa`; `--shade`: `#f2f5f5`
- **Fonts:** `Georgia,serif`
- **Font sizes:** `clamp(43px,6.3vw,82px)`, `clamp(29px,3.3vw,44px)`, `26px`, `clamp(21px,2.4vw,27px)`, `23px`, `12px`, `17px`, `20px`
- **Line heights:** `1.15`, `1.45`
- **Text colors:** `var(--ink)`, `#a74132`, `#6b7e86`, `var(--rust)`, `var(--muted)`, `white`
- **Backgrounds:** `var(--paper)`, `#f8f1ef`, `#19313e`, `#f3f6f5`, `white`, `var(--shade)`
- **Max widths:** `1180px`, `1000px`, `950px`, `780px`, `760px`, `1080px`, `860px`
- **Margins:** `0`, `auto`, `76px auto 54px`, `18px 0`, `64px 0 18px`, `30px 0 14px`, `24px 0 28px`, `38px 0`, `20px 0`, `28px 0`, `58px auto`, `36px 0`, `12px 0 16px`, `44px auto 36px`, `42px 0`, `48px 0 16px`
- **Margin top:** `56px`
- **Padding:** `14px clamp(20px,5vw,84px)`, `0 24px 100px`, `10px 12px 0 0`, `16px 24px`, `13px 14px`, `12px 14px`, `20px`, `18px 20px`, `9px`, `34px 0`, `0 17px 65px`, `12px 16px`, `8px`, `12px 17px`
- **Padding top:** `20px`
- **Gaps:** `15px`, `16px`, `24px`, `8px`

### [uni-rebound-liquidity-test.html](../../../../content/uni-rebound-liquidity-test.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `#172337`; `--muted`: `#596779`; `--paper`: `#f9fafb`; `--line`: `#d9dfe5`; `--accent`: `#ac3255`; `--pale`: `#f1e8ec`; `--deep`: `#101829`
- **Fonts:** `Georgia,'Times New Roman',serif`, `system-ui,sans-serif`
- **Font sizes:** `19px`, `clamp(2.6rem,6vw,5rem)`, `clamp(1.15rem,2.7vw,1.55rem)`, `1.25em`, `clamp(1.65rem,3.5vw,2.45rem)`, `1.3rem`, `1.05rem`, `.83em`, `1.45rem`, `17px`
- **Line heights:** `1.74`, `1.05`, `1.48`, `1.65`, `1.17`, `1.3`, `1.45`
- **Text colors:** `var(--ink)`, `#8d2849`, `#fff`, `var(--accent)`, `#4a586b`, `var(--muted)`
- **Backgrounds:** `var(--paper)`, `var(--deep)`, `var(--pale)`, `#e9edf1`, `#f0f3f5`, `#fff`
- **Max widths:** `1050px`, `900px`, `820px`, `1200px`, `760px`
- **Margins:** `0`, `0 auto`, `17px 0 20px`, `0 0 24px`, `20px auto 0`, `auto`, `0 0 1.25em`, `2.1em 0 .6em`, `1.65em 0 .5em`, `30px 0`, `25px 0 33px`, `25px 0`, `0 0 15px`, `32px 0`
- **Margin top:** `50px`
- **Margin bottom:** `10px`, `9px`
- **Padding:** `17px max(24px,calc((100vw - 1120px)/2))`, `64px 24px 28px`, `10px 24px`, `38px 24px 80px`, `16px 21px`, `12px 14px`, `20px`, `15px 0 15px 22px`, `26px 24px`, `12px`
- **Padding top:** `15px`, `20px`, `18px`, `38px`, `25px`

### [venice-ai-privacy.html](../../../../content/venice-ai-privacy.html)

Inline style blocks: 1.
- **Local custom properties:** `--paper`: `var(--cr-bg,#f8f6f0)`; `--ink`: `var(--cr-ink,#202c2a)`; `--muted`: `var(--cr-muted,#52605c)`; `--rule`: `var(--cr-line,#cdd3ca)`; `--accent`: `var(--cr-accent,#205448)`; `--accent-soft`: `#e6ede7`; `--white`: `#fffefa`; `--focus`: `var(--cr-focus,#8b4e21)`; `--serif`: `var(--cr-serif,Georgia,"Times New Roman",serif)`; `--sans`: `var(--cr-sans,system-ui,sans-serif)`
- **Fonts:** `var(--serif)`
- **Font sizes:** `1.125rem`, `clamp(2.65rem,6.1vw,5.75rem)`, `clamp(1.23rem,2.3vw,1.65rem)`, `3.6em`, `clamp(1.8rem,3.5vw,2.65rem)`, `1.42rem`, `1.28rem`, `clamp(1.3rem,2.5vw,1.8rem)`, `1.0625rem`, `clamp(2.38rem,11vw,3.5rem)`, `.77rem`
- **Line heights:** `1.72`, `1.045`, `1.46`, `.84`, `1.19`, `1.55`, `1.38`, `1.68`
- **Text colors:** `var(--ink)`, `var(--accent)`, `var(--muted)`, `#3d4d47`, `#000`, `inherit`
- **Backgrounds:** `var(--paper)`, `var(--white)`, `#fff`
- **Max widths:** `59rem`, `17ch`, `44rem`, `var(--cr-measure,45rem)`, `100%`
- **Margins:** `0`, `.85rem 0 1.55rem`, `0 0 2rem`, `0 0 1.45rem`, `3.55rem 0 1.2rem`, `2.25rem 0 .75rem`, `0 0 1rem`, `2.4rem 0`, `2rem 0`, `2rem 0 2.4rem`
- **Margin top:** `1rem`, `3rem`
- **Margin right:** `1rem`
- **Margin bottom:** `.4rem`, `.8rem`, `.5rem`
- **Margin inline:** `auto`
- **Padding:** `.65rem 1rem`, `clamp(3.2rem,7vw,7rem) 0 3.25rem`, `.07em .12em 0 0`, `.4rem 0`, `1.15rem 0 1.15rem 1.45rem`, `1.2rem 0`, `0 0 .75rem`, `.85rem .9rem .85rem 0`, `1.1rem 0`, `0`, `.75rem .45rem .3rem 0`, `1.5rem 0 3rem`
- **Padding top:** `.6rem`, `1rem`, `1.3rem`, `2.5rem`, `2.8rem`
- **Padding bottom:** `.8rem`, `2.5rem`
- **Padding left:** `1.2rem`, `1rem`
- **Gaps:** `1rem`, `clamp(2rem,7vw,7rem)`, `.7rem`, `.3rem 1.1rem`, `.25rem`

### [virtual-alpha-risk.html](../../../../content/virtual-alpha-risk.html)

Inline style blocks: 1.
- **Local custom properties:** `--ink`: `var(--cr-ink,#202823)`; `--muted`: `var(--cr-muted,#59635c)`; `--paper`: `var(--cr-bg,#faf9f5)`; `--rule`: `var(--cr-line,#d9ddd5)`; `--accent`: `var(--cr-accent,#315b4c)`; `--soft`: `#eef1e9`; `--negative`: `#9b503c`; `--positive`: `#2f6955`; `--serif`: `var(--cr-serif,Georgia,'Times New Roman',serif)`
- **Fonts:** `var(--serif)`, `system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif`
- **Font sizes:** `19px`, `12px`, `clamp(45px,6.6vw,86px)`, `clamp(21px,2.4vw,27px)`, `4.5em`, `clamp(31px,3.7vw,45px)`, `25px`, `clamp(25px,3vw,35px)`, `11px`, `16px`, `17px`, `clamp(42px,12vw,62px)`, `20px`, `10px`, `13px`, `clamp(37px,10.5vw,62px)`
- **Line heights:** `1.72`, `1.04`, `1.45`, `.79`, `1.17`, `1.3`, `1.65`, `1.35`, `1.5`
- **Text colors:** `var(--ink)`, `var(--accent)`, `var(--cr-ink,#193e31)`, `var(--muted)`, `#4c554e`, `#294c3d`, `var(--negative)`, `var(--positive)`, `#48534a`, `inherit`
- **Backgrounds:** `var(--paper)`, `#e6e9e1`, `var(--accent)`, `#879c8e`, `#b5c2b7`, `var(--soft)`, `#edf1e9`, `linear-gradient(to right,#f2e7e3 0%,#f2e7e3 40%,#e0e5dc 40%,#e0e5dc 100%)`, `var(--negative)`, `white`
- **Max widths:** `1120px`, `870px`, `850px`, `750px`, `var(--cr-measure,70ch)`
- **Margins:** `0`, `auto`, `90px auto 60px`, `0 0 29px`, `0 0 34px`, `0 0 1.45em`, `2em 0 .7em`, `1.6em 0 .6em`, `12px 0`, `55px 0 58px`, `0 0 8px`, `0 0 24px`, `18px 0 0`, `50px 0`, `40px 0`, `35px 0 12px`, `0 0 20px`, `0 0 12px`, `66px auto 42px`, `52px auto 34px`, `38px 0`, `0 0 30px`, `3px 16px 3px 0`
- **Margin top:** `28px`, `65px`, `35px`, `44px`
- **Margin right:** `14px`, `0`
- **Margin bottom:** `24px`, `14px`, `10px`, `0`, `8px`
- **Padding:** `19px max(24px,calc((100vw - 1100px)/2))`, `0 24px`, `11px 12px 0 0`, `24px 0 18px`, `3px 0 3px 26px`, `24px 27px`, `14px 12px`, `15px 12px`, `30px 0 80px`, `28px 24px 45px`, `0 19px`, `20px`, `10px 14px`, `5px 0`, `14px 0 16px`, `7px 0`, `17px 19px`
- **Padding top:** `16px`, `17px`
- **Padding left:** `18px`
- **Gaps:** `16px`, `9px 25px`, `70px`, `17px`, `12px`, `13px`, `10px`, `7px`, `6px`, `0`

### [weft-first-week.html](../../../../content/weft-first-week.html)

Inline style blocks: 1.
- **Local custom properties:** `--paper`: `var(--cr-bg,#f6f3ec)`; `--ink`: `var(--cr-ink,#1d292c)`; `--dim`: `var(--cr-muted,#536363)`; `--line`: `var(--cr-line,#d8d8d0)`; `--accent`: `var(--cr-accent,#92542d)`; `--dark`: `#17252a`; `--darkmuted`: `#adc2be`; `--serif`: `var(--cr-serif,Georgia,'Times New Roman',serif)`; `--sans`: `var(--cr-sans,Inter,'Helvetica Neue',Arial,sans-serif)`
- **Font sizes:** `15px`, `10px`, `22px`, `78px`, `clamp(48px,9vw,75px)`, `16px`, `clamp(43px,10.8vw,61px)`, `20px`, `25px`
- **Line heights:** `1.58`, `.77`, `1.75`
- **Text colors:** `var(--ink)`, `var(--cr-accent,#87512f)`, `var(--cr-ink,#56361f)`, `var(--dim)`, `var(--accent)`, `#405053`, `var(--dark)`, `#eff4ef`, `#dce8e2`, `#36484b`, `#ebf1ea`, `#b9cbc6`, `#eaf0e9`, `#65401f`
- **Backgrounds:** `var(--paper)`, `#d7d8d1`, `#864d31`, `#d2a178`, `#9aadaa`, `var(--dark)`, `#e9e8e0`, `#e6d7c7`, `white`
- **Max widths:** `var(--cr-container,1160px)`, `1000px`, `830px`, `1030px`, `68ch`
- **Margins:** `0`, `auto`, `22px 0`, `27px 0 24px`, `0 auto`, `0 0 25px`, `11px 12px 0 0`, `75px 0 26px`, `41px 0 17px`, `46px 0`, `45px 0 48px`, `0 0 17px`, `52px 0 43px`, `35px 0 45px`, `25px 0 32px`, `76px calc((min(710px,100vw - 68px) - 100vw)/2)`, `0 0 21px`, `30px 0`, `82px 0 80px`, `0 0 20px`, `0 0 32px`
- **Margin top:** `16px`, `13px`, `15px`, `10px`, `41px`, `55px`
- **Margin right:** `7px`, `-34px`, `-21px`
- **Margin left:** `4px`, `-34px`, `-21px`
- **Padding:** `0 34px`, `25px 0 19px`, `74px 0 48px`, `60px 0 0`, `8px 0`, `0 0 0 26px`, `27px 28px 16px`, `25px 0`, `0 17px`, `15px 13px`, `12px 14px`, `62px max(34px,calc((100vw - 750px)/2))`, `0 0 13px 6px`, `3px 6px`, `28px 0 48px`, `46px 34px`, `0 21px`, `42px 0 35px`, `0 0 18px!important`, `18px 10px 6px`, `43px 21px`, `12px 0`, `10px 0`, `9px 4px`, `20px 0`
- **Padding top:** `14px`, `25px`, `40px`, `52px`, `36px`
- **Padding bottom:** `0!important`
- **Padding left:** `0`, `18px`, `22px`
- **Gaps:** `15px`, `12px 26px`, `60px`, `9px 24px`, `0`, `20px`

## Observed chrome/article differences

- The shared chrome has a single tokenized palette, a 72.5rem outer container, and a 47.5rem reading measure. The article sources retain independent palettes, typography, width limits, and spacing values; several define their own paper/ink/accent variables and some also reference shared `--cr-*` fallbacks.
- Article max-width declarations range across article-specific values (for example 620px, 700–900px, and 1000px+) and sometimes switch to `--cr-measure` with per-article fallbacks. Values apply to different selectors, so they are not directly equivalent reading-column measurements.
- Typography is heterogeneous by design in source: article families include Georgia/Times and local `--serif` variables, while the shared chrome uses its serif/sans token stacks. Article font sizes and spacing are specified independently, often with `clamp()` and viewport breakpoints.
- Generated site bar resets are scoped to `#cr-sitebar`; the rest of each essay remains controlled by its inline source CSS. The source inventory therefore shows a shared navigation layer over intentionally varied essay presentation.
