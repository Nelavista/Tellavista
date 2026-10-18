#!/usr/bin/env node
/**
 * Enforce the web first-load budget (B12).
 *
 * A measured number is not an enforced one: this reads the built `index.html`,
 * gzips every script and stylesheet it references, and fails when the total goes
 * over budget. Lazy route chunks are deliberately not counted — they are not part
 * of the first load, and counting them would make the budget meaningless.
 *
 * Usage: node tools/check_web_budget.mjs [distDir]
 * Default dist: apps/web/dist (override with WEB_DIST for another environment).
 */
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { gzipSync } from 'node:zlib';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dist = resolve(root, process.argv[2] ?? process.env.WEB_DIST ?? 'apps/web/dist');

// Budgets are gzip bytes for the first load. ADR-0001 sets the JS budget; the CSS
// budget exists so styles cannot creep up unnoticed either. The env overrides are
// for measuring a candidate budget locally — CI sets neither, so a pull request
// can never relax its own limit.
function budgetFromEnv(name, fallbackKb) {
  const raw = process.env[name];
  if (!raw) return fallbackKb * 1024;
  const kb = Number(raw);
  if (!Number.isFinite(kb) || kb <= 0) {
    console.error(`[budget] ${name} must be a positive number of KB.`);
    process.exit(2);
  }
  return Math.round(kb * 1024);
}

const BUDGETS = {
  js: budgetFromEnv('WEB_BUDGET_JS_KB', 150),
  css: budgetFromEnv('WEB_BUDGET_CSS_KB', 20),
};

if (!existsSync(join(dist, 'index.html'))) {
  console.error(`[budget] no build at ${dist}. Run the web build first.`);
  process.exit(2);
}

const html = readFileSync(join(dist, 'index.html'), 'utf8');
const referenced = [...html.matchAll(/(?:src|href)="([^"]+\.(?:js|css))"/g)].map((match) => match[1]);
if (referenced.length === 0) {
  console.error('[budget] index.html references no JS or CSS. Refusing to pass a build it cannot read.');
  process.exit(2);
}

const totals = { js: 0, css: 0 };
for (const asset of referenced) {
  const file = join(dist, asset.replace(/^\//, ''));
  if (!existsSync(file)) {
    console.error(`[budget] ${asset} is referenced by index.html but missing from the build.`);
    process.exit(1);
  }
  const raw = readFileSync(file);
  const gzipped = gzipSync(raw, { level: 9 }).length;
  const kind = asset.endsWith('.css') ? 'css' : 'js';
  totals[kind] += gzipped;
  console.log(
    `[budget] ${asset.padEnd(40)} ${(raw.length / 1024).toFixed(1)} KB raw → ${(gzipped / 1024).toFixed(1)} KB gzip`,
  );
}

let failed = false;
for (const kind of ['js', 'css']) {
  const used = totals[kind];
  const budget = BUDGETS[kind];
  const verdict = used <= budget ? 'ok' : 'OVER BUDGET';
  console.log(
    `[budget] first-load ${kind}: ${(used / 1024).toFixed(1)} KB gzip of ${(budget / 1024).toFixed(0)} KB — ${verdict}`,
  );
  if (used > budget) {
    failed = true;
    console.error(
      `::error::web first-load ${kind} is ${(used / 1024).toFixed(1)} KB gzip, over the ${(budget / 1024).toFixed(0)} KB budget. Split or trim before merging.`,
    );
  }
}

process.exit(failed ? 1 : 0);
