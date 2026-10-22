/**
 * Generates the PWA icons with no image dependencies.
 *
 * Installability needs real PNGs (192 + 512, plus a maskable variant), so this
 * writes them from a tiny RGBA rasteriser. Placeholder artwork only: replace the
 * files in apps/web/public/icons when design ships the real mark.
 *
 * Usage: node tools/gen-pwa-icons.mjs
 */
import { deflateSync } from 'node:zlib';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const OUT_DIR = resolve(dirname(fileURLToPath(import.meta.url)), '../apps/web/public/icons');

const BG = [5, 8, 16, 255]; // #050810 — colors.bg
const ACCENT = [0, 209, 255, 255]; // #00d1ff — colors.accent

const CRC_TABLE = (() => {
  const table = new Int32Array(256);
  for (let n = 0; n < 256; n += 1) {
    let c = n;
    for (let k = 0; k < 8; k += 1) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c;
  }
  return table;
})();

function crc32(buf) {
  let c = 0xffffffff;
  for (const byte of buf) c = CRC_TABLE[(c ^ byte) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function chunk(type, data) {
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length);
  const body = Buffer.concat([Buffer.from(type, 'ascii'), data]);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(body));
  return Buffer.concat([len, body, crc]);
}

function png(size, pixelAt) {
  const raw = Buffer.alloc(size * (size * 4 + 1));
  for (let y = 0; y < size; y += 1) {
    const rowStart = y * (size * 4 + 1);
    raw[rowStart] = 0; // filter: none
    for (let x = 0; x < size; x += 1) {
      const [r, g, b, a] = pixelAt(x, y);
      const i = rowStart + 1 + x * 4;
      raw[i] = r;
      raw[i + 1] = g;
      raw[i + 2] = b;
      raw[i + 3] = a;
    }
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(size, 0);
  ihdr.writeUInt32BE(size, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 6; // RGBA
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk('IHDR', ihdr),
    chunk('IDAT', deflateSync(raw, { level: 9 })),
    chunk('IEND', Buffer.alloc(0)),
  ]);
}

/** Dark tile with an accent ring — the standard icon. */
function ringIcon(size) {
  const c = (size - 1) / 2;
  const outer = size * 0.36;
  const inner = size * 0.2;
  return png(size, (x, y) => {
    const d = Math.hypot(x - c, y - c);
    if (d <= inner) return ACCENT;
    if (d <= outer && d >= inner + size * 0.06) return ACCENT;
    return BG;
  });
}

/** Maskable: full-bleed accent, mark kept inside the 80% safe zone. */
function maskableIcon(size) {
  const c = (size - 1) / 2;
  const outer = size * 0.28;
  const inner = size * 0.16;
  return png(size, (x, y) => {
    const d = Math.hypot(x - c, y - c);
    if (d <= inner) return ACCENT;
    if (d <= outer && d >= inner + size * 0.05) return ACCENT;
    return BG;
  });
}

mkdirSync(OUT_DIR, { recursive: true });
const files = [
  ['icon-192.png', ringIcon(192)],
  ['icon-512.png', ringIcon(512)],
  ['maskable-512.png', maskableIcon(512)],
];
for (const [name, data] of files) {
  writeFileSync(resolve(OUT_DIR, name), data);
  console.log(`wrote ${name} (${data.length} bytes)`);
}
