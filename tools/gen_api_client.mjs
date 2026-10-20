#!/usr/bin/env node
/**
 * Regenerate packages/api-client/src/generated from the API's OpenAPI schema.
 *
 * Usage:
 *   node tools/gen_api_client.mjs                 # fetch from a running API
 *   node tools/gen_api_client.mjs --schema <file> # use a saved openapi.json (CI)
 *
 * CI runs this and fails if the committed client differs (ADR-0001 freshness check).
 * Requires `openapi-typescript`, a root devDependency.
 *
 * The CLI is executed with the current Node binary rather than through a package
 * manager: on Windows `pnpm` is a `.cmd` shim, which `execFileSync` cannot spawn
 * (ENOENT). Running the resolved JS entry point works on every OS.
 */
import { execFileSync } from 'node:child_process';
import { mkdirSync, existsSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const cli = resolve(dirname(require.resolve('openapi-typescript/package.json')), 'bin/cli.js');
const out = resolve(root, 'packages/api-client/src/generated/schema.d.ts');
mkdirSync(dirname(out), { recursive: true });

const schemaFlagIndex = process.argv.indexOf('--schema');
const baseUrl = process.env.API_BASE_URL || 'http://localhost:8000';
const source = schemaFlagIndex !== -1 ? process.argv[schemaFlagIndex + 1] : `${baseUrl}/openapi.json`;

if (!process.env.API_BASE_URL && schemaFlagIndex === -1) {
  console.warn(`[gen_api_client] No API_BASE_URL set; assuming ${baseUrl}`);
}

if (schemaFlagIndex !== -1 && !existsSync(source)) {
  console.error(`[gen_api_client] schema file not found: ${source}`);
  process.exit(2);
}

try {
  execFileSync(process.execPath, [cli, source, '-o', out], { stdio: 'inherit', cwd: root });
  console.log(`[gen_api_client] wrote ${out}`);
} catch (err) {
  console.error(`[gen_api_client] generation failed: ${err.message}`);
  process.exit(1);
}
