import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
const root = process.cwd();
const css = readFileSync(path.join(root, "assets/design-system.css"), "utf8");
const files = readdirSync(path.join(root, "content")).filter((name) => name.endsWith(".html")).sort();
const selectors = [...new Set(css.match(/(?:^|\n)\s*([^\n{}]+)\s*\{/g)?.map((s) => s.trim().replace(/^\s*/, "").replace(/\s*\{$/, "")) ?? [])];
function declarations(source, properties) {
  const values = Object.fromEntries(properties.map((name) => [name, new Set()]));
  const re = /(?:^|[;{])\s*([\w-]+)\s*:\s*([^;}]+)\s*(?=[;}])/g;
  for (const match of source.matchAll(re)) {
    const key = match[1].toLowerCase();
    if (values[key]) values[key].add(match[2].trim().replace(/\s+/g, " "));
  }
  return Object.fromEntries(properties.map((key) => [key, [...values[key]]]));
}
function customProperties(source) {
  const values = new Map();
  const re = /(?:^|[;{])\s*(--[\w-]+)\s*:\s*([^;}]+)\s*(?=[;}])/g;
  for (const match of source.matchAll(re)) {
    const key = match[1];
    if (!values.has(key)) values.set(key, new Set());
    values.get(key).add(match[2].trim().replace(/\s+/g, " "));
  }
  return [...values].map(([key, entries]) => `\`${key}\`: ${[...entries].map((value) => `\`${value.replaceAll("`", "\\`")}\``).join(" / ")}`);
}
const properties = ["font-family", "font-size", "line-height", "color", "background", "background-color", "max-width", "margin", "margin-top", "margin-right", "margin-bottom", "margin-left", "margin-inline", "padding", "padding-top", "padding-right", "padding-bottom", "padding-left", "gap"];
const articles = files.map((file) => {
  const html = readFileSync(path.join(root, "content", file), "utf8");
  const styleBlocks = [...html.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style\s*>/gi)].map((match) => match[1].replace(/\/\*[\s\S]*?\*\//g, ""));
  return { file, count: styleBlocks.length, values: declarations(styleBlocks.join("\n"), properties), custom: customProperties(styleBlocks.join("\n")) };
});
const lines = [
  "# Style inventory",
  "",
  "## Generated shared chrome",
  "",
  "`build.py` copies `assets/design-system.css` to `dist/design-system.css`; articles link it after their source styles, and generated home/404 pages also link it. Search behavior is in `assets/search.js`; it changes visibility/order and URL parameters, while its visual rules remain in the shared stylesheet.",
  "",
  "### Tokens (`:root`)",
  "",
  "| Token group | Values |",
  "| --- | --- |",
  "| Colors | `--cr-bg: #f6f3ec`; `--cr-ink: #1b2422`; `--cr-muted: #5c6a65`; `--cr-accent: #1d5c55`; `--cr-line: #e3dbd0`; `--cr-bar: #172420`; `--cr-bar-text: #f4f1ea`; `--cr-bar-muted: #d5ddd8`; focus: `#1d5c55` / bar focus `#e6d3ae` |",
  "| Type | Serif: Iowan Old Style, Palatino Linotype, Palatino, Georgia; sans: system-ui, -apple-system, Segoe UI |",
  "| Measures | `--cr-measure: 47.5rem`; `--cr-container: 72.5rem`; breakpoint `--cr-break: 640px` |",
  "",
  "### Site bar",
  "",
  "Dark `#172420` bar; system sans 13px/1.3 with 0.01em letter spacing. Inner container max 72.5rem, centered, 10px 20px padding, 16px gap. Text #f4f1ea, secondary link #d5ddd8, 2px visible focus outline #e6d3ae.",
  "",
  "### Home and 404 base",
  "",
  "Paper background `#f6f3ec`, ink `#1b2422`, serif 18px/1.55, top border 6px dark. Main content measure 55rem with 20px side gutters (mobile: 16px); mobile breakpoint 640px. Masthead, archive, card grid and the filters share this scoped stylesheet. The masthead is dark; controls use system sans. Search form is grid based and collapses to one column below 640px; empty-state uses 22px padding and a 1px decorative border.",
  "",
  "### Search behavior and presentation",
  "",
  "The generated form exposes a text query, topic select, research-type select and reset. `search.js` matches ticker/title/dek/topic, applies combined filters, updates a live status/count and empty state, and reflects current controls in query parameters. All visual control and state rules are under `body.cr-home` in `design-system.css`; there is no separate search stylesheet.",
  "",
  "## Article source style blocks",
  "",
  "Values below are unique declarations found in each source article's inline `<style>` blocks. Lists omit a category only if the source has no declaration for it. Exact values are retained; `var()` references depend on that article's local custom properties. This is a source inventory, not a claim that every declared rule is active at every viewport.",
];
const labels = [
  ["font-family", "Fonts"], ["font-size", "Font sizes"], ["line-height", "Line heights"],
  ["color", "Text colors"], ["background", "Backgrounds"], ["background-color", "Background colors"],
  ["max-width", "Max widths"], ["margin", "Margins"], ["margin-top", "Margin top"], ["margin-right", "Margin right"], ["margin-bottom", "Margin bottom"], ["margin-left", "Margin left"], ["margin-inline", "Margin inline"],
  ["padding", "Padding"], ["padding-top", "Padding top"], ["padding-right", "Padding right"], ["padding-bottom", "Padding bottom"], ["padding-left", "Padding left"], ["gap", "Gaps"],
];
for (const article of articles) {
  lines.push("", `### [${article.file}](../../../../content/${article.file})`, "", `Inline style blocks: ${article.count}.`);
  if (article.custom.length) lines.push(`- **Local custom properties:** ${article.custom.join("; ")}`);
  for (const [property, label] of labels) {
    const values = article.values[property];
    if (values.length) lines.push(`- **${label}:** ${values.map((v) => `\`${v.replaceAll("`", "\\`")}\``).join(", ")}`);
  }
}
lines.push("", "## Observed chrome/article differences", "", "- The shared chrome has a single tokenized palette, a 72.5rem outer container, and a 47.5rem reading measure. The article sources retain independent palettes, typography, width limits, and spacing values; several define their own paper/ink/accent variables and some also reference shared `--cr-*` fallbacks.", "- Article max-width declarations range across article-specific values (for example 620px, 700–900px, and 1000px+) and sometimes switch to `--cr-measure` with per-article fallbacks. Values apply to different selectors, so they are not directly equivalent reading-column measurements.", "- Typography is heterogeneous by design in source: article families include Georgia/Times and local `--serif` variables, while the shared chrome uses its serif/sans token stacks. Article font sizes and spacing are specified independently, often with `clamp()` and viewport breakpoints.", "- Generated site bar resets are scoped to `#cr-sitebar`; the rest of each essay remains controlled by its inline source CSS. The source inventory therefore shows a shared navigation layer over intentionally varied essay presentation.", "");
writeFileSync(path.join(root, "docs/designs/ux-audit/evidence/style-inventory.md"), lines.join("\n"));
console.log(JSON.stringify({ articles: articles.length, cssSelectors: selectors.length, stylesheet: "assets/design-system.css" }));
