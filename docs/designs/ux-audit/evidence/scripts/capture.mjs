import { chromium } from "playwright";
import { readFileSync, existsSync, mkdirSync } from "node:fs";
import path from "node:path";

const root = process.cwd();
const out = path.join(root, "docs/designs/ux-audit/evidence/screenshots");
mkdirSync(out, { recursive: true });
const catalog = JSON.parse(readFileSync(path.join(root, "content/articles.json"), "utf8"));
const cases = [
  { name: "home-default", route: "/", state: "default" },
  { name: "home-search-btc", route: "/", state: "btc" },
  { name: "home-topic-bitcoin", route: "/", state: "topic" },
  { name: "home-empty", route: "/", state: "empty" },
  { name: "404", route: "/404.html", state: "default" },
  ...["bitcoin-buying-imbalance", "venice-ai-privacy", "aero-at-0-68", "pyth-revenue-unlock", catalog[0].slug]
    .map((slug) => ({ name: slug, route: `/${slug}/`, state: "default" })),
];
const browser = await chromium.launch({ headless: true });
const errors = [];
for (const width of [390, 768, 1440]) {
  const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 1, colorScheme: "light" });
  for (const item of cases) {
    const file = path.join(out, `${item.name}-${width}.png`);
    if (existsSync(file)) continue;
    try {
      const response = await page.goto(`http://127.0.0.1:4173${item.route}`, { waitUntil: "domcontentloaded", timeout: 60000 });
      if (item.name !== "404" && !response?.ok()) throw new Error(`HTTP ${response?.status()}`);
      if (item.state === "btc") {
        await page.locator('input[name="q"]').fill("BTC");
        await page.waitForTimeout(300);
      } else if (item.state === "topic") {
        await page.locator('select[name="topic"]').selectOption("bitcoin");
        await page.waitForTimeout(300);
      } else if (item.state === "empty") {
        await page.locator('input[name="q"]').fill("no-match-ux-audit-8734");
        await page.waitForTimeout(300);
      }
      await page.evaluate(() => {
        for (const image of document.images) image.loading = "eager";
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(500);
      await page.screenshot({ path: file, fullPage: true, animations: "disabled" });
    } catch (error) {
      errors.push({ name: item.name, width, error: String(error) });
    }
  }
  await page.close();
}
await browser.close();
console.log(JSON.stringify({ captured: cases.length * 3 - errors.length, errors }, null, 2));
if (errors.length) process.exitCode = 1;
