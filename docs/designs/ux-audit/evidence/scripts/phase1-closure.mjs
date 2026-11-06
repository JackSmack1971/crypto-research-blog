import { mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { chromium } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const baseURL = process.env.PHASE1_BASE_URL ?? "http://127.0.0.1:4173";
const rawDir = resolve("docs/designs/ux-audit/evidence/axe/phase1-closure-raw");
const widths = [390, 768, 1440];
const schemes = ["light", "dark"];
const contrastTargets = [
  { finding: "UX-01", route: "/404.html", selector: ".kicker" },
  { finding: "UX-02", route: "/token-unlock-liquidity-illusion-90-day-calendar/", selector: "header.mast span:last-child" },
  { finding: "UX-03", route: "/token-unlock-liquidity-illusion-90-day-calendar/", selector: ".kicker" },
  { finding: "UX-09", route: "/binance-four-hour-wallet-takeover/", selector: "header.mast span:last-child" },
  { finding: "UX-09", route: "/binance-four-hour-wallet-takeover/", selector: ".kicker" },
  { finding: "UX-09", route: "/binance-four-hour-wallet-takeover/", selector: "footer.foot" },
];
const axeTargets = [
  { route: "/404.html" },
  { route: "/token-unlock-liquidity-illusion-90-day-calendar/" },
  { route: "/binance-four-hour-wallet-takeover/" },
];
const scrollTargets = [
  { finding: "UX-04", route: "/aero-at-0-68/", selector: ".table-scroll" },
  { finding: "UX-05", route: "/bitcoin-buying-imbalance/", selector: ".tablewrap" },
  { finding: "UX-06", route: "/token-unlock-liquidity-illusion-90-day-calendar/", selector: ".scroll" },
];

await mkdir(rawDir, { recursive: true });

const parseColor = (value) => {
  const match = value.match(/rgba?\(([^)]+)\)/);
  if (!match) return null;
  const channels = match[1].split(/[\s,\/]+/).filter(Boolean).map(Number);
  return channels.length >= 3 ? [channels[0], channels[1], channels[2], channels[3] ?? 1] : null;
};
const toCss = (color) => `rgb(${color.slice(0, 3).map((channel) => Math.round(channel)).join(", ")})`;

const browser = await chromium.launch({ headless: true });
const result = {
  generatedAt: new Date().toISOString(),
  baseURL,
  environment: { node: process.version, playwright: null, chromium: browser.version() },
  contrast: [],
  axe: [],
  scroll: [],
};

try {
  result.environment.playwright = (await import("@playwright/test/package.json", { with: { type: "json" } })).default.version;

  for (const target of contrastTargets) {
    for (const width of widths) {
      for (const colorScheme of schemes) {
        const context = await browser.newContext({ viewport: { width, height: 1000 }, colorScheme });
        const page = await context.newPage();
        await page.goto(new URL(target.route, baseURL).href, { waitUntil: "networkidle" });
        const state = await page.evaluate(({ selector }) => {
          const parseColor = (value) => {
            const match = value.match(/rgba?\(([^)]+)\)/);
            if (!match) return null;
            const channels = match[1].split(/[\s,\/]+/).filter(Boolean).map(Number);
            return channels.length >= 3 ? [channels[0], channels[1], channels[2], channels[3] ?? 1] : null;
          };
          const toCss = (color) => `rgb(${color.slice(0, 3).map((channel) => Math.round(channel)).join(", ")})`;
          const element = document.querySelector(selector);
          if (!element) return { found: false, requestedSelector: selector };
          const cssPath = (node) => {
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
          const foreground = parseColor(getComputedStyle(element).color);
          let background = [255, 255, 255, 1];
          const ancestors = [];
          for (let current = element; current; current = current.parentElement) ancestors.push(current);
          for (const current of ancestors.reverse()) {
            const color = parseColor(getComputedStyle(current).backgroundColor);
            if (color && color[3] > 0) {
              background = [0, 1, 2].map((index) => color[index] * color[3] + background[index] * (1 - color[3])).concat(1);
            }
          }
          const luminance = (color) => color.slice(0, 3).map((channel) => {
            const value = channel / 255;
            return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
          }).reduce((sum, value, index) => sum + value * [0.2126, 0.7152, 0.0722][index], 0);
          const ratio = (Math.max(luminance(foreground), luminance(background)) + 0.05) /
            (Math.min(luminance(foreground), luminance(background)) + 0.05);
          const style = getComputedStyle(element);
          const fontSize = Number.parseFloat(style.fontSize);
          const fontWeight = Number.parseInt(style.fontWeight, 10) || 400;
          const minimumRatio = fontSize >= 24 || (fontSize >= 18.66 && fontWeight >= 700) ? 3 : 4.5;
          return {
            found: true,
            selector: cssPath(element),
            tag: element.tagName.toLowerCase(),
            foreground: toCss(foreground),
            effectiveBackground: toCss(background),
            fontSize: `${fontSize}px`,
            fontWeight: style.fontWeight,
            ratio: Number(ratio.toFixed(2)),
            minimumRatio,
            passed: ratio >= minimumRatio,
          };
        }, { selector: target.selector });
        result.contrast.push({ finding: target.finding, route: target.route, viewport: width, colorScheme, requestedSelector: target.selector, ...state });
        await context.close();
      }
    }
  }

  for (const target of axeTargets) {
    for (const width of widths) {
      for (const colorScheme of schemes) {
        const context = await browser.newContext({ viewport: { width, height: 1000 }, colorScheme });
        const page = await context.newPage();
        await page.goto(new URL(target.route, baseURL).href, { waitUntil: "networkidle" });
        const axe = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]).analyze();
        const nodes = axe.violations.filter((violation) => violation.id === "color-contrast")
          .flatMap((violation) => violation.nodes.map((node) => ({ target: node.target, summary: node.failureSummary })));
        result.axe.push({ route: target.route, viewport: width, colorScheme, colorContrastNodes: nodes, passed: nodes.length === 0 });
        await context.close();
      }
    }
  }

  for (const target of scrollTargets) {
    for (const width of widths) {
      const context = await browser.newContext({ viewport: { width, height: 1000 }, colorScheme: "light" });
      const page = await context.newPage();
      await page.goto(new URL(target.route, baseURL).href, { waitUntil: "networkidle" });
      const initial = await page.locator(target.selector).evaluate((region) => ({
        found: true,
        tabindex: region.getAttribute("tabindex"),
        role: region.getAttribute("role"),
        ariaLabel: region.getAttribute("aria-label"),
        scrollWidth: region.scrollWidth,
        clientWidth: region.clientWidth,
        overflows: region.scrollWidth > region.clientWidth,
        scrollLeft: region.scrollLeft,
      })).catch(() => ({ found: false, selector: target.selector }));
      let reachedByTab = false;
      let focusVisible = false;
      let outline = null;
      let beforeScroll = initial.scrollLeft ?? 0;
      let afterArrowRight = beforeScroll;
      let afterEnd = beforeScroll;
      if (initial.found) {
        await page.locator(target.selector).evaluate((region) => {
          const candidates = [...document.querySelectorAll("a[href], button, input, select, textarea, [tabindex]:not([tabindex='-1'])")];
          const previous = candidates.filter((element) => element !== region && element.compareDocumentPosition(region) & Node.DOCUMENT_POSITION_FOLLOWING)
            .filter((element) => !element.hasAttribute("disabled") && element.getClientRects().length).at(-1);
          (previous ?? document.body).focus();
        });
        await page.keyboard.press("Tab");
        reachedByTab = await page.locator(target.selector).evaluate((region) => document.activeElement === region);
        if (reachedByTab) {
          const focus = await page.locator(target.selector).evaluate((region) => ({
            visible: region.matches(":focus-visible"),
            outline: getComputedStyle(region).outline,
            scrollLeft: region.scrollLeft,
          }));
          focusVisible = focus.visible;
          outline = focus.outline;
          beforeScroll = focus.scrollLeft;
          await page.keyboard.press("ArrowRight");
          await page.keyboard.press("ArrowRight");
          await page.keyboard.press("ArrowRight");
          afterArrowRight = await page.locator(target.selector).evaluate((region) => region.scrollLeft);
          await page.keyboard.press("End");
          afterEnd = await page.locator(target.selector).evaluate((region) => region.scrollLeft);
        }
      }
      const attrsPassed = initial.found && initial.tabindex === "0" && initial.role === "region" && Boolean(initial.ariaLabel?.trim());
      const keyboardScrollIncreased = afterArrowRight > beforeScroll || afterEnd > beforeScroll;
      result.scroll.push({
        finding: target.finding,
        route: target.route,
        viewport: width,
        selector: target.selector,
        ...initial,
        attrsPassed,
        reachedByTab,
        focusVisible,
        outline,
        beforeScroll,
        afterArrowRight,
        afterEnd,
        keyboardScrollIncreased,
        passed: Boolean(attrsPassed && reachedByTab && (!initial.overflows || (focusVisible && keyboardScrollIncreased))),
      });
      await context.close();
    }
  }

  const failed = [
    ...result.contrast.filter((row) => !row.found || !row.passed).map((row) => ({ kind: "contrast", ...row })),
    ...result.axe.filter((row) => !row.passed).map((row) => ({ kind: "axe", ...row })),
    ...result.scroll.filter((row) => !row.passed).map((row) => ({ kind: "scroll", ...row })),
  ];
  result.failed = failed;
  const rawPath = resolve(rawDir, "phase1-closure.json");
  await writeFile(rawPath, `${JSON.stringify(result, null, 2)}\n`, "utf8");

  console.log(`RAW_JSON ${rawPath}`);
  console.log("CONTRAST | viewport | scheme | selector | foreground | effective background | font size/weight | ratio | required | result");
  for (const row of result.contrast) console.log(`${row.finding} | ${row.viewport} | ${row.colorScheme} | ${row.selector ?? "NOT FOUND"} | ${row.foreground ?? "—"} | ${row.effectiveBackground ?? "—"} | ${row.fontSize ?? "—"}/${row.fontWeight ?? "—"} | ${row.ratio ?? "—"} | ${row.minimumRatio ?? "—"} | ${row.passed ? "PASS" : "FAIL"}`);
  console.log("AXE | viewport | scheme | route | color-contrast nodes | result");
  for (const row of result.axe) console.log(`${row.viewport} | ${row.colorScheme} | ${row.route} | ${row.colorContrastNodes.length} | ${row.passed ? "PASS" : "FAIL"}`);
  console.log("SCROLL | viewport | finding | route | attrs | overflow (scroll/client) | Tab | focus-visible | outline | scrollLeft before/ArrowRight/End | result");
  for (const row of result.scroll) console.log(`${row.viewport} | ${row.finding} | ${row.route} | ${row.tabindex}/${row.role}/${row.ariaLabel ?? "missing"} | ${row.scrollWidth ?? "—"}/${row.clientWidth ?? "—"} (${row.overflows ?? "—"}) | ${row.reachedByTab} | ${row.focusVisible} | ${row.outline ?? "—"} | ${row.beforeScroll}/${row.afterArrowRight}/${row.afterEnd} | ${row.passed ? "PASS" : "FAIL"}`);
  console.log(`SUMMARY contrast=${result.contrast.length} axe=${result.axe.length} scroll=${result.scroll.length} failures=${failed.length}`);
  if (failed.length) process.exitCode = 1;
} finally {
  await browser.close();
}
