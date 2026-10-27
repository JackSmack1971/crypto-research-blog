import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  testMatch: "**/*.spec.ts",
  snapshotDir: "visual-baselines",
  snapshotPathTemplate: "{snapshotDir}/{arg}{ext}",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 1 : 2,
  timeout: 120_000,
  reporter: "list",
  expect: {
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.001,
      animations: "disabled",
      caret: "hide",
    },
  },
  use: {
    baseURL: "http://127.0.0.1:4173",
    locale: "en-US",
    timezoneId: "UTC",
    colorScheme: "light",
    launchOptions: {
      args: [
        "--font-render-hinting=none",
        "--disable-font-subpixel-positioning",
        "--disable-lcd-text",
      ],
    },
  },
  webServer: {
    command: "python3 build.py && python3 -m http.server 4173 --bind 127.0.0.1 -d dist",
    url: "http://127.0.0.1:4173",
    reuseExistingServer: false,
    timeout: 120_000,
  },
});
