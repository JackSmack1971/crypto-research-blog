import { readFileSync } from "node:fs";
import { expect, test, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const articles = JSON.parse(readFileSync("content/articles.json", "utf8")) as { slug: string }[];
const routes = ["/", ...articles.map((article) => `/${article.slug}/`), "/404.html"];
const widths = [390, 768, 1440];
const visualTargets = [
  ["home", "/"],
  ["bitcoin-buying-imbalance", "/bitcoin-buying-imbalance/"],
  ["venice-ai-privacy", "/venice-ai-privacy/"],
  ["aero-at-0-68", "/aero-at-0-68/"],
];

type KnownDefects = {
  notes: string;
  horizontalOverflow: { route: string; width: number; overflow: number }[];
  accessibility: { route: string; id: string; impact: string; target: string }[];
};

const known = JSON.parse(readFileSync("tests/fixtures/known-defects.json", "utf8")) as KnownDefects;
const knownAxe = new Set(known.accessibility.map((item) => `${item.route}|${item.id}|${item.target}`));
const knownOverflow = new Set(known.horizontalOverflow.map((item) => `${item.route}|${item.width}`));

async function prepare(page: Page, route: string): Promise<void> {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto(route, { waitUntil: "networkidle" });
  await page.evaluate(async () => {
    const images = [...document.images];
    for (const image of images) {
      image.loading = "eager";
      image.scrollIntoView();
    }
    await Promise.all(
      images.map(
        (image) =>
          new Promise<void>((resolve) => {
            if (image.complete && image.naturalWidth > 0) {
              resolve();
              return;
            }
            const done = () => resolve();
            image.addEventListener("load", done, { once: true });
            image.addEventListener("error", done, { once: true });
            setTimeout(done, 8000);
          }),
      ),
    );
    document.documentElement.style.overflowY = "scroll";
    // Overlay scrollbars (where the baselines were captured) take no gutter.
    // A classic scrollbar narrows the page and makes a 100vw breakout report
    // about 16px of overflow. Hide the gutter so both environments measure
    // the same content box.
    document.documentElement.style.scrollbarWidth = "none";
    window.scrollTo(0, 0);
  });
}

test.describe("layout", () => {
  for (const route of routes) {
    for (const width of widths) {
      test(`no unexpected overflow ${route} @ ${width}`, async ({ page }) => {
        await page.setViewportSize({ width, height: 900 });
        await prepare(page, route);
        const overflow = await page.evaluate(() => {
          const doc = document.documentElement;
          const gutter = Math.max(0, window.innerWidth - doc.clientWidth);
          return doc.scrollWidth - doc.clientWidth - gutter;
        });
        const allowed = knownOverflow.has(`${route}|${width}`);
        if (!allowed) {
          expect(overflow, `${route} overflows by ${overflow}px at ${width}px`).toBeLessThanOrEqual(1);
        }
      });
    }
  }

  for (const route of articles.map((article) => `/${article.slug}/`)) {
    test(`site bar is visible ${route}`, async ({ page }) => {
      await page.setViewportSize({ width: 390, height: 844 });
      await prepare(page, route);
      const bar = page.locator("#cr-sitebar");
      await expect(bar).toBeVisible();
      const box = await bar.boundingBox();
      expect(box).not.toBeNull();
      expect(box!.y).toBeGreaterThanOrEqual(0);
      expect(box!.x).toBeGreaterThanOrEqual(-1);
      expect(box!.x + box!.width).toBeLessThanOrEqual(392);
      const background = await bar.evaluate((element) => getComputedStyle(element).backgroundColor);
      expect(background).toBe("rgb(23, 36, 32)");
    });
  }
});

test.describe("keyboard", () => {
  test("homepage skip link receives focus", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await prepare(page, "/");
    await page.keyboard.press("Tab");
    const focused = await page.evaluate(() => {
      const element = document.activeElement as HTMLElement | null;
      if (!element) return null;
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return {
        text: element.textContent?.trim() ?? "",
        outlineStyle: style.outlineStyle,
        outlineWidth: style.outlineWidth,
        top: rect.top,
      };
    });
    expect(focused?.text).toContain("Skip");
    expect(focused!.top).toBeGreaterThanOrEqual(0);
    expect(focused!.outlineStyle === "none" && focused!.outlineWidth === "0px").toBe(false);
  });

  test("article site bar link receives focus", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await prepare(page, "/venice-ai-privacy/");
    await page.keyboard.press("Tab");
    const focused = await page.evaluate(() => {
      const element = document.activeElement as HTMLElement | null;
      if (!element) return null;
      const style = getComputedStyle(element);
      return {
        inBar: Boolean(element.closest("#cr-sitebar")),
        outlineStyle: style.outlineStyle,
        outlineWidth: style.outlineWidth,
      };
    });
    expect(focused?.inBar).toBe(true);
    expect(focused!.outlineStyle === "none" && focused!.outlineWidth === "0px").toBe(false);
  });
});

test.describe("accessibility", () => {
  for (const route of ["/", ...articles.map((article) => `/${article.slug}/`)]) {
    test(`no new serious issues ${route}`, async ({ page }) => {
      await page.setViewportSize({ width: 1440, height: 900 });
      await prepare(page, route);
      const results = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
        .analyze();
      const serious = results.violations.filter(
        (violation) => violation.impact === "critical" || violation.impact === "serious",
      );
      const unexpected = [];
      for (const violation of serious) {
        for (const node of violation.nodes) {
          const target = node.target.join(" ");
          const key = `${route}|${violation.id}|${target}`;
          if (!knownAxe.has(key)) {
            unexpected.push({ route, id: violation.id, impact: violation.impact, target, help: violation.help });
          }
        }
      }
      expect(unexpected, JSON.stringify(unexpected, null, 2)).toEqual([]);
    });
  }
});

test.describe("visual baseline", () => {
  for (const [name, route] of visualTargets) {
    for (const width of widths) {
      test(`${name} @ ${width}`, async ({ page }) => {
        await page.setViewportSize({ width, height: 900 });
        await prepare(page, route);
        await expect(page).toHaveScreenshot(`${name}-${width}.png`, {
          fullPage: true,
          timeout: 30_000,
        });
      });
    }
  }
});

test("shared tokens load without changing paint", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  for (const route of ["/", "/venice-ai-privacy/"]) {
    await prepare(page, route);
    const tokens = await page.evaluate(() => {
      const style = getComputedStyle(document.documentElement);
      return {
        bg: style.getPropertyValue("--cr-bg").trim(),
        ink: style.getPropertyValue("--cr-ink").trim(),
        accent: style.getPropertyValue("--cr-accent").trim(),
      };
    });
    expect(tokens, route).toEqual({ bg: "#f6f3ec", ink: "#1b2422", accent: "#1d5c55" });
  }
});

test("representative images decode", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  for (const route of ["/aero-at-0-68/", "/pyth-revenue-unlock/", "/bitcoin-buying-imbalance/"]) {
    await prepare(page, route);
    const broken = await page.evaluate(() =>
      [...document.images]
        .filter((image) => !image.complete || image.naturalWidth === 0)
        .map((image) => image.alt.slice(0, 80)),
    );
    expect(broken, route).toEqual([]);
  }
});
