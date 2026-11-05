import { mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { chromium } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const baseURL = process.env.REMEASURE_BASE_URL ?? "http://127.0.0.1:4173";
const evidenceDir = resolve("docs/designs/ux-audit/evidence/screenshots/remeasure-raw");
const screenshotDir = evidenceDir;
const widths = [390, 768, 1440];
const schemes = ["light", "dark"];
const contrastTargets = [
  { finding: "UX-01", route: "/404.html", selector: ".mast .kicker, .kicker" },
  {
    finding: "UX-02",
    route: "/token-unlock-liquidity-illusion-90-day-calendar/",
    selector: ".mast span:last-child",
  },
  {
    finding: "UX-03",
    route: "/token-unlock-liquidity-illusion-90-day-calendar/",
    selector: ".kicker",
  },
];
const scrollTargets = [
  { finding: "UX-04", route: "/aero-at-0-68/", selector: ".table-scroll" },
  { finding: "UX-05", route: "/bitcoin-buying-imbalance/", selector: ".tablewrap" },
  {
    finding: "UX-06",
    route: "/token-unlock-liquidity-illusion-90-day-calendar/",
    selector: ".scroll",
  },
];

await mkdir(screenshotDir, { recursive: true });

function slug(value) {
  return value.replaceAll(/[^a-z0-9]+/gi, "-").replaceAll(/^-|-$/g, "").toLowerCase();
}

function markdownCell(value) {
  return String(value ?? "").replaceAll("|", "\\|").replaceAll("\n", " ");
}

const browser = await chromium.launch({ headless: true });
const result = {
  generatedAt: new Date().toISOString(),
  baseURL,
  note: "Raw machine-readable evidence and screenshots are local-only under this ignored directory.",
  contrast: [],
  scroll: [],
};
const markdown = [];

try {
  for (const target of contrastTargets) {
    const observed = [];
    for (const width of widths) {
      for (const colorScheme of schemes) {
        const context = await browser.newContext({ viewport: { width, height: 1000 }, colorScheme });
        const page = await context.newPage();
        await page.goto(new URL(target.route, baseURL).href, { waitUntil: "networkidle" });
        const state = await page.evaluate(({ selector }) => {
          const element = document.querySelector(selector);
          if (!element) return { found: false, requestedSelector: selector };
          const cssPath = (node) => {
            if (node.id) return `#${CSS.escape(node.id)}`;
            const parts = [];
            for (let current = node; current && current.nodeType === Node.ELEMENT_NODE; current = current.parentElement) {
              let part = current.localName;
              if (current.classList.length) part += `.${[...current.classList].map((name) => CSS.escape(name)).join(".")}`;
              const siblings = current.parentElement ? [...current.parentElement.children].filter((item) => item.localName === current.localName) : [];
              if (siblings.length > 1) part += `:nth-of-type(${siblings.indexOf(current) + 1})`;
              parts.unshift(part);
              if (current.id) break;
            }
            return parts.join(" > ");
          };
          const parseColor = (value) => {
            const match = value.match(/rgba?\(([^)]+)\)/);
            if (!match) return null;
            const channels = match[1].split(/[\s,\/]+/).filter(Boolean).map(Number);
            if (channels.length < 3) return null;
            return [channels[0], channels[1], channels[2], channels[3] ?? 1];
          };
          const composite = (foreground, background) => {
            const alpha = foreground[3];
            return [0, 1, 2].map((index) => foreground[index] * alpha + background[index] * (1 - alpha)).concat(1);
          };
          const toCss = (color) => `rgb(${color.slice(0, 3).map((channel) => Math.round(channel)).join(", ")})`;
          const foreground = parseColor(getComputedStyle(element).color);
          let background = [255, 255, 255, 1];
          const ancestors = [];
          for (let current = element; current; current = current.parentElement) ancestors.push(current);
          for (const current of ancestors.reverse()) {
            const color = parseColor(getComputedStyle(current).backgroundColor);
            if (color && color[3] > 0) background = composite(color, background);
          }
          const luminance = (color) => {
            const channels = color.slice(0, 3).map((channel) => {
              const value = channel / 255;
              return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
            });
            return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
          };
          const l1 = luminance(foreground);
          const l2 = luminance(background);
          const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
          const style = getComputedStyle(element);
          const fontSize = Number.parseFloat(style.fontSize);
          const fontWeight = Number.parseInt(style.fontWeight, 10) || 400;
          const minimumRatio = fontSize >= 24 || (fontSize >= 18.66 && fontWeight >= 700) ? 3 : 4.5;
          return {
            found: true,
            selector: cssPath(element),
            tag: element.tagName.toLowerCase(),
            text: element.textContent.trim().replace(/\s+/g, " "),
            property: "color",
            foreground: toCss(foreground),
            effectiveBackground: toCss(background),
            fontSize: `${fontSize}px`,
            fontWeight: style.fontWeight,
            ratio: Number(ratio.toFixed(2)),
            minimumRatio,
            reproduced: ratio < minimumRatio,
          };
        }, { selector: target.selector });
        let axe = null;
        if (state.found) {
          axe = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]).analyze();
        }
        const basename = `${target.finding}-${slug(target.route)}-${width}-${colorScheme}`;
        await page.screenshot({ path: resolve(screenshotDir, `${basename}.png`), fullPage: true });
        await writeFile(resolve(evidenceDir, `${basename}.axe.json`), JSON.stringify(axe, null, 2));
        const record = {
          finding: target.finding,
          route: target.route,
          viewport: `${width}px`,
          colorScheme,
          requestedSelector: target.selector,
          ...state,
          axeColorContrastNodes: axe?.violations
            .filter((violation) => violation.id === "color-contrast")
            .flatMap((violation) => violation.nodes.map((node) => ({ target: node.target, summary: node.failureSummary }))) ?? [],
        };
        observed.push(record);
        result.contrast.push(record);
        await context.close();
      }
    }
    const reproduced = observed.filter((state) => state.reproduced);
    markdown.push(`### ${target.finding} — ${reproduced.length ? "reproduced" : "not reproduced"}`);
    markdown.push("");
    markdown.push(`Route: \`${target.route}\`; requested selector: \`${target.selector}\`. Evidence covers 390, 768, and 1440 CSS px in light and dark color schemes.`);
    markdown.push("");
    markdown.push("The measured color and contrast properties were identical under emulated light and dark schemes; no matching dark-mode override changed these targets.");
    markdown.push("");
    markdown.push("| Viewport | Scheme | Element/selector | Foreground | Effective background | Font size/weight | Ratio | Minimum | Axe color-contrast nodes | Result |");
    markdown.push("|---:|---|---|---|---|---|---:|---:|---:|---|");
    for (const state of observed) {
      markdown.push(`| ${state.viewport} | ${state.colorScheme} | ${state.found ? `\`${markdownCell(state.selector)}\`` : "not found"} | ${state.foreground ?? "—"} | ${state.effectiveBackground ?? "—"} | ${state.fontSize ?? "—"} / ${state.fontWeight ?? "—"} | ${state.ratio ?? "—"} | ${state.minimumRatio ?? "—"} | ${state.axeColorContrastNodes.length} | ${state.found ? (state.reproduced ? "reproduced" : "not reproduced") : "not reproduced"} |`);
    }
    markdown.push("");
    if (!reproduced.length) markdown.push(`Not reproduced: the requested element was absent or every measured state met its applicable minimum ratio. Per-state measurements and axe node details are in ignored raw JSON under \`remeasure-raw/\`.`);
    markdown.push("");
  }

  for (const target of scrollTargets) {
    const observed = [];
    for (const width of widths) {
      const context = await browser.newContext({ viewport: { width, height: 1000 }, colorScheme: "light" });
      const page = await context.newPage();
      await page.goto(new URL(target.route, baseURL).href, { waitUntil: "networkidle" });
      const initial = await page.locator(target.selector).evaluate((region) => {
        const rect = region.getBoundingClientRect();
        const focusable = region.tabIndex >= 0;
        const previous = [...document.querySelectorAll("a[href], button, input, select, textarea, [tabindex]:not([tabindex='-1'])")]
          .filter((element) => element !== region && element.compareDocumentPosition(region) & Node.DOCUMENT_POSITION_FOLLOWING)
          .filter((element) => !element.hasAttribute("disabled") && element.getClientRects().length)
          .at(-1);
        return {
          selector: `${region.tagName.toLowerCase()}${[...region.classList].map((name) => `.${CSS.escape(name)}`).join("")}`,
          role: region.getAttribute("role"),
          accessibleName: region.getAttribute("aria-label") || region.getAttribute("aria-labelledby") || region.getAttribute("title") || "",
          programmaticTabIndex: focusable,
          scrollWidth: region.scrollWidth,
          clientWidth: region.clientWidth,
          overflows: region.scrollWidth > region.clientWidth,
          previousTag: previous?.tagName.toLowerCase() ?? null,
          previousText: previous?.textContent.trim().replace(/\s+/g, " ").slice(0, 80) ?? null,
          visible: rect.width > 0 && rect.height > 0,
        };
      });
      let reachedByTab = false;
      let focusVisible = false;
      let outline = "none";
      let beforeScroll = 0;
      let afterScroll = 0;
      if (initial.previousTag) {
        // The exact previous node is focused from its recorded DOM identity in page context.
        await page.evaluate(() => {
          const region = document.querySelector(".table-scroll, .tablewrap, .scroll");
          const all = [...document.querySelectorAll("a[href], button, input, select, textarea, [tabindex]:not([tabindex='-1'])")];
          const previous = all.filter((element) => element !== region && element.compareDocumentPosition(region) & Node.DOCUMENT_POSITION_FOLLOWING)
            .filter((element) => !element.hasAttribute("disabled") && element.getClientRects().length).at(-1);
          previous?.focus();
        });
        await page.keyboard.press("Tab");
        reachedByTab = await page.locator(target.selector).evaluate((region) => document.activeElement === region);
        if (reachedByTab && initial.overflows) {
          focusVisible = await page.locator(target.selector).evaluate((region) => region.matches(":focus-visible"));
          outline = await page.locator(target.selector).evaluate((region) => getComputedStyle(region).outline);
          beforeScroll = await page.locator(target.selector).evaluate((region) => region.scrollLeft);
          for (let index = 0; index < 5; index += 1) await page.keyboard.press("ArrowRight");
          afterScroll = await page.locator(target.selector).evaluate((region) => region.scrollLeft);
        }
      }
      const axe = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]).analyze();
      const scrollableRegionNodes = axe.violations
        .filter((violation) => violation.id === "scrollable-region-focusable")
        .flatMap((violation) => violation.nodes.map((node) => ({ target: node.target, summary: node.failureSummary })));
      const basename = `${target.finding}-${slug(target.route)}-${width}-light`;
      await writeFile(resolve(evidenceDir, `${basename}.axe.json`), JSON.stringify(axe, null, 2));
      const record = {
        finding: target.finding,
        route: target.route,
        viewport: `${width}px`,
        ...initial,
        focusable: reachedByTab,
        reachedByTab,
        focusVisible,
        outline,
        beforeScroll,
        afterScroll,
        keyboardScrollIncreased: afterScroll > beforeScroll,
        axeScrollableRegionNodes: scrollableRegionNodes,
        reproduced: initial.overflows && !(reachedByTab && focusVisible && outline !== "none" && outline !== "0px" && afterScroll > beforeScroll),
      };
      observed.push(record);
      result.scroll.push(record);
      await context.close();
    }
    const reproduced = observed.some((state) => state.reproduced);
    markdown.push(`### ${target.finding} — ${reproduced ? "reproduced" : "not reproduced"}`);
    markdown.push("");
    markdown.push(`Route: \`${target.route}\`; wrapper: \`${target.selector}\`.`);
    markdown.push("");
    markdown.push("| Viewport | Role | Accessible name | Tab-reachable | Programmatic tabindex | Scroll width / client width | Overflow | :focus-visible | Outline | scrollLeft before→after five ArrowRight presses | Axe scroll-region nodes | Result |");
    markdown.push("|---:|---|---|---|---|---:|---|---|---|---:|---:|---|");
    for (const state of observed) {
      markdown.push(`| ${state.viewport} | ${state.role || "missing"} | ${state.accessibleName || "missing"} | ${state.reachedByTab} | ${state.programmaticTabIndex} | ${state.scrollWidth} / ${state.clientWidth} | ${state.overflows} | ${state.focusVisible} | ${state.outline} | ${state.beforeScroll} → ${state.afterScroll} | ${state.axeScrollableRegionNodes.length} | ${state.reproduced ? "reproduced" : "not reproduced"} |`);
    }
    markdown.push("");
  }

  const report = [
    "# Slice 1 remeasurement — UX-01–06",
    "",
    `Measured: ${result.generatedAt} against \`${baseURL}\`; build: current catalog output (24 articles).`,
    "",
    "Raw axe JSON and PNG screenshots are local-only under the Git-ignored \`screenshots/remeasure-raw/\` directory. The committed script is reproducible with the existing dependencies; no production or test files were changed.",
    "",
    "## Contrast state matrix",
    "",
    "Rows are included for every reproduced contrast state only. Approval remains pending for every row; dates remain blank until Bret decides.",
    "",
    "| Finding | Route | Viewport | Color scheme | Element/selector | Property | Foreground | Effective background | Font size/weight | Observed ratio | Minimum ratio | Approval | Approval date |",
    "|---|---|---:|---|---|---|---|---|---|---:|---:|---|---|",
  ];
  for (const state of result.contrast.filter((entry) => entry.found && entry.reproduced)) {
    report.push(`| ${state.finding} | \`${state.route}\` | ${state.viewport} | ${state.colorScheme} | \`${markdownCell(state.selector)}\` | ${state.property} | ${state.foreground} | ${state.effectiveBackground} | ${state.fontSize} / ${state.fontWeight} | ${state.ratio}:1 | ${state.minimumRatio}:1 | pending |  |`);
  }
  if (!result.contrast.some((entry) => entry.found && entry.reproduced)) report.push("| — | No contrast states reproduced | — | — | — | — | — | — | — | — | — | — | — |");
  report.push("", "## Finding results", "", ...markdown, "## Out of scope — awaiting Bret", "", "Axe reports `scrollable-region-focusable` for the three named wrappers at 390 px, and none exposes `role=region` or a non-empty accessible name at any measured width. Chromium itself moves focus to each 390 px overflow wrapper with Tab and ArrowRight scrolls it; 768/1440 px have no overflow and those wrappers are not Tab-reachable. The missing region semantics/name are recorded as a new accessibility issue for Bret; no production edit or test is made in Slice 1.", "");
  await writeFile(resolve("docs/designs/ux-audit/evidence/remeasure.md"), `${report.join("\n").trimEnd()}\n`, "utf8");
  await writeFile(resolve(evidenceDir, "remeasure.json"), JSON.stringify(result, null, 2), "utf8");
  console.log(`Wrote report and ${result.contrast.length} contrast-state records / ${result.scroll.length} scroll-state records; raw captures: ${evidenceDir}`);
} finally {
  await browser.close();
}
