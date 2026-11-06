import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";

const root = process.cwd();
const out = path.join(root, "docs/designs/ux-audit/evidence/axe");
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
const rows = [];
for (const width of [390, 1440]) {
  const context = await browser.newContext({ viewport: { width, height: 900 }, deviceScaleFactor: 1, colorScheme: "light" });
  const page = await context.newPage();
  for (const item of cases) {
    try {
      const response = await page.goto(`http://127.0.0.1:4173${item.route}`, { waitUntil: "domcontentloaded", timeout: 60000 });
      if (item.name !== "404" && !response?.ok()) throw new Error(`HTTP ${response?.status()}`);
      if (item.state === "btc") await page.locator('input[name="q"]').fill("BTC");
      if (item.state === "topic") await page.locator('select[name="topic"]').selectOption("bitcoin");
      if (item.state === "empty") await page.locator('input[name="q"]').fill("no-match-ux-audit-8734");
      await page.waitForTimeout(250);
      const report = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]).analyze();
      const raw = { route: item.route, scenario: item.name, viewport: { width, height: 900 }, url: page.url(), ...report };
      writeFileSync(path.join(out, `${item.name}-${width}.json`), `${JSON.stringify(raw, null, 2)}\n`);
      rows.push({ scenario: item.name, route: item.route, width, report });
    } catch (error) {
      rows.push({ scenario: item.name, route: item.route, width, error: String(error) });
    }
  }
  await context.close();
}
await browser.close();
writeFileSync(path.join(out, "_run-index.json"), `${JSON.stringify(rows.map((row) => ({ scenario: row.scenario, route: row.route, width: row.width, error: row.error ?? null, violationCount: row.report?.violations.length ?? null })), null, 2)}\n`);
console.log(JSON.stringify(rows.map((row) => ({ scenario: row.scenario, width: row.width, error: row.error ?? null, violations: row.report?.violations.length ?? null })), null, 2));
if (rows.some((row) => row.error)) process.exitCode = 1;
