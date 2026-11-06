import { readFileSync } from "node:fs";
import { expect, test, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

type Article = { slug: string; topic: string; assets: string[]; research_type: string };
const articles = JSON.parse(readFileSync("content/articles.json", "utf8")) as Article[];
const routes = ["/", ...articles.map((article) => `/${article.slug}/`), "/404.html"];
const widths = [390, 768, 1440];
const homepageWidths = [320, ...widths, 1024];
const visualTargets = [
  ["home", "/"],
  ["bitcoin-buying-imbalance", "/bitcoin-buying-imbalance/"],
  ["venice-ai-privacy", "/venice-ai-privacy/"],
  ["aero-at-0-68", "/aero-at-0-68/"],
];
const homepageBaselineSlugs = new Set([
  "bitcoin-rebound-spot-demand",
  "bitcoin-selloff-leverage",
  "solz-launch-investigation",
  "bitcoin-holding-up",
  "aero-at-0-68",
  "bitcoin-buying-imbalance",
  "weft-first-week",
  "virtual-alpha-risk",
  "rune-quiet-repricing",
  "pyth-revenue-unlock",
  "venice-ai-privacy",
  "crypto-buybacks",
]);

type KnownDefects = {
  notes: string;
  horizontalOverflow: { route: string; width: number; overflow: number }[];
  accessibility: { route: string; id: string; impact: string; target: string }[];
};

const known = JSON.parse(readFileSync("tests/fixtures/known-defects.json", "utf8")) as KnownDefects;
const knownAxe = new Set(known.accessibility.map((item) => `${item.route}|${item.id}|${item.target}`));
const knownOverflow = new Set(known.horizontalOverflow.map((item) => `${item.route}|${item.width}`));

async function prepare(page: Page, route: string): Promise<void> {
  if (route === "/404.html") {
    // The 404 deliberately uses canonical URLs at arbitrary request depths.
    // Preview its locally built assets, not whatever is currently in production.
    const site = JSON.parse(readFileSync("site.json", "utf8")) as { url: string };
    for (const asset of ["design-system.css", "favicon.svg", "feed.xml"]) {
      await page.route(`${site.url.replace(/\/$/, "")}/${asset}`, (request) =>
        request.fulfill({ path: `dist/${asset}` }));
    }
  }
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
    const routeWidths = route === "/" ? homepageWidths : widths;
    for (const width of routeWidths) {
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

test("every catalog article appears on the homepage", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await prepare(page, "/");
  for (const article of articles) {
    const link = page.locator(`a[href="${article.slug}/"]`).first();
    await expect(link, `homepage is missing ${article.slug}`).toBeVisible();
  }
});

test.describe("research archive search", () => {
  test("filtered featured result spans the desktop archive", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await prepare(page, "/");
    await page.getByRole("searchbox").fill("DEEP");
    const result = page.locator("[data-featured-search]");
    await expect(result).toBeVisible();
    await expect(result).toHaveCSS("grid-column", "1 / -1");
    const grid = await page.locator(".archive-grid").boundingBox();
    const box = await result.boundingBox();
    expect(box).not.toBeNull();
    expect(Math.abs(box!.width - grid!.width)).toBeLessThanOrEqual(1);
    expect(Math.abs(box!.x - grid!.x)).toBeLessThanOrEqual(1);
  });

  test("combines ticker, topic, and research type filters and clears them", async ({ page }) => {
    await page.setViewportSize({ width: 1024, height: 900 });
    await prepare(page, "/");
    await page.getByRole("searchbox", { name: "Search by topic, asset ticker, or title" }).fill("BTC");
    await page.getByLabel("Filter by topic").selectOption("bitcoin");
    await page.getByLabel("Filter by research type").selectOption("market-snapshot");
    const expected = articles.filter((article) => article.topic === "bitcoin"
      && article.assets.includes("BTC")
      && article.research_type === "market-snapshot").length;
    const plural = expected === 1 ? "investigation" : "investigations";
    await expect(page.locator(".entry:visible")).toHaveCount(expected);
    await expect(page.locator("[data-search-status]")).toContainText(`${expected} ${plural} found`);
    await page.getByRole("button", { name: "Clear" }).click();
    await expect(page.locator(".entry:visible")).toHaveCount(articles.length - 1);
    await expect(page.locator("[data-search-status]")).toContainText(`${articles.length} investigations`);
  });

  test("normalizes punctuation and announces empty results", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await prepare(page, "/");
    await page.getByRole("searchbox", { name: "Search by topic, asset ticker, or title" }).fill("deepbook’s supply question");
    await expect(page.locator("[data-featured-search]")).toBeVisible();
    await expect(page.locator(".entry:visible")).toHaveCount(1);
    await expect(page.locator("[data-search-status]")).toContainText("1 investigation found");
    await page.getByRole("searchbox", { name: "Search by topic, asset ticker, or title" }).fill("unmatched query xyz");
    await expect(page.locator(".entry:visible")).toHaveCount(0);
    await expect(page.locator("[data-empty-state]")).toBeVisible();
  });

  test("matches multiple words across asset and topic fields", async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 900 });
    await prepare(page, "/");
    await page.getByRole("searchbox", { name: "Search by topic, asset ticker, or title" }).fill("AERO tokenomics");
    await expect(page.locator('.entry[data-slug="aero-at-0-68"]')).toBeVisible();
    await expect(page.locator(".entry:visible")).toHaveCount(1);
  });

  test("all article links remain in server-rendered HTML without the search script", async ({ page }) => {
    await page.route("**/search.js", (route) => route.abort());
    await page.setViewportSize({ width: 768, height: 900 });
    await prepare(page, "/");
    for (const article of articles) {
      await expect(page.locator(`a[href="${article.slug}/"]`).first()).toBeVisible();
    }
  });
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
  for (const route of routes) {
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
        if (name === "home") {
          // Keep homepage paint baselines focused on the approved article set.
          // New notes are independently checked for homepage visibility, overflow, and accessibility.
          await page.evaluate((slugs) => {
            for (const entry of document.querySelectorAll<HTMLElement>(".entry[data-slug]")) {
              const slug = entry.dataset.slug;
              if (!slug || !slugs.includes(slug)) entry.remove();
            }
            const count = document.querySelector(".count");
            if (count) count.textContent = "9 investigations";
            const status = document.querySelector("[data-search-status]");
            if (status) status.textContent = "9 investigations";
          }, [...homepageBaselineSlugs]);
        }
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

for (const route of ["/", "/404.html"]) {
  test(`shared skip link reaches main ${route}`, async ({ page }) => {
    await prepare(page, route);
    await page.keyboard.press("Tab");
    await expect(page.locator(".skip")).toBeFocused();
    await page.keyboard.press("Enter");
    await expect(page).toHaveURL(/#main-content$/);
    await expect(page.locator("main#main-content")).toHaveCount(1);
    expect(await page.evaluate(() => document.activeElement?.id)).toBe("main-content");
  });
}
