/**
 * GateForge Lane A — Playwright config
 * Reference: GateForge UI Auto-Test Standard § 8.1
 *
 * This file is the deterministic, committed configuration for Lane A.
 * Do NOT generate it at runtime. Edit, commit, review via PR.
 */

import { defineConfig, devices } from '@playwright/test';

const SUT_URL = process.env.SUT_URL ?? 'http://localhost:3000';

export default defineConfig({
  // Test root — every project keeps Gherkin features here.
  testDir: './features',

  // Discover compiled step files alongside the .feature files.
  testMatch: '**/*.feature.ts',

  // Per-test timeout. Increase only with explicit Architect approval.
  timeout: 30_000,
  expect: { timeout: 5_000 },

  // No flake tolerance: a flaky test is a defect, not a retry.
  retries: 0,
  fullyParallel: true,
  workers: process.env.CI ? 4 : '50%',

  // Reporters required by gates G-UI-1 through G-UI-4.
  reporter: [
    ['list'],
    ['junit', { outputFile: 'reports/laneA-junit.xml' }],
    ['html', { outputFolder: 'reports/laneA-html', open: 'never' }],
    ['allure-playwright', { resultsDir: 'reports/laneA-allure' }],
  ],

  use: {
    baseURL: SUT_URL,
    headless: true,
    viewport: { width: 1280, height: 800 },
    ignoreHTTPSErrors: false,
    actionTimeout: 5_000,
    navigationTimeout: 10_000,

    // Page-ready signal — every page exposes data-testid="page-ready"
    // after hydration; the suite polls for it.
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',

    // Force reduced motion to keep visual diffs deterministic.
    contextOptions: {
      reducedMotion: 'reduce',
      colorScheme: 'light',
    },
  },

  projects: [
    {
      name: 'chromium-desktop',
      use: {
        ...devices['Desktop Chrome'],
        // GateForge headless flags — see UI Auto-Test Standard § 9.1.
        launchOptions: {
          args: [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--headless=new',
          ],
        },
      },
    },
    {
      name: 'mobile-pixel',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'visual',
      testMatch: '**/*.visual.feature.ts',
      use: {
        screenshot: { mode: 'on', fullPage: true },
      },
      // Visual regression compares against qa/visual-baselines/*.png
      // Pixel diff threshold 0.1 % — Gate G-UI-2.
    },
    {
      name: 'a11y',
      testMatch: '**/*.a11y.feature.ts',
      // Each test runs axe-core via @axe-core/playwright; critical
      // issue count must be 0 — Gate G-UI-3.
    },
    {
      name: 'smoke',
      // PR-blocking smoke profile — runs in < 90 s on the QC runner.
      grep: /@smoke/,
    },
  ],
});
