/**
 * Generates the mobile app icon and splash with no image dependencies (D4).
 *
 * The store requires real PNGs at exact sizes, so this writes them from a tiny
 * RGBA rasteriser — the same approach as tools/gen-pwa-icons.mjs. Placeholder
 * artwork only: replace the files in apps/mobile/assets when design ships the
 * real mark. Keep the dimensions; Expo reads them from app.config.js.
 *
 * Usage: node tools/gen-mobile-assets.mjs
 */
import { deflateSync } from 'node:zlib';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const OUT_DIR = resolve(dirname(fileURLToPath(import.meta.url)), '../apps/mobile/assets');

const BG = [5, 8, 16, 255]; // #050810 — colors.bg
const ACCENT = [0, 209, 255, 255]; // #00d1ff — colors.accent
const CLEAR = [0, 0, 0, 0];

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

function png(width, height, pixelAt) {
  const stride = width * 4 + 1;
  const raw = Buffer.alloc(height * stride);
  for (let y = 0; y < height; y += 1) {
    const rowStart = y * stride;
    raw[rowStart] = 0; // filter: none
    for (let x = 0; x < width; x += 1) {
      const [r, g, b, a] = pixelAt(x, y);
      const i = rowStart + 1 + x * 4;
      raw[i] = r;
      raw[i + 1] = g;
      raw[i + 2] = b;
      raw[i + 3] = a;
    }
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 6; // RGBA
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk('IHDR', ihdr),
    chunk('IDAT', deflateSync(raw, { level: 9 })),
    chunk('IEND', Buffer.alloc(0)),
  ]);
}

/** Dark tile, accent ring and a solid centre: the app icon. */
function icon(size) {
  const c = (size - 1) / 2;
  const outer = size * 0.33;
  const inner = size * 0.18;
  return png(size, size, (x, y) => {
    const d = Math.hypot(x - c, y - c);
    if (d <= inner) return ACCENT;
    if (d <= outer && d >= inner + size * 0.055) return ACCENT;
    return BG;
  });
}

/**
 * Android adaptive foreground: the mark alone on transparent, kept inside the
 * 66% safe zone so no launcher mask clips it.
 */
function adaptiveForeground(size) {
  const c = (size - 1) / 2;
  const outer = size * 0.22;
  const inner = size * 0.12;
  return png(size, size, (x, y) => {
    const d = Math.hypot(x - c, y - c);
    if (d <= inner) return ACCENT;
    if (d <= outer && d >= inner + size * 0.04) return ACCENT;
    return CLEAR;
  });
}

/**
 * Splash: portrait, mark centred, background from the dark token. Expo scales
 * `contain`, so the mark sits inside the middle 40% on any device.
 */
function splash(width, height) {
  const cx = (width - 1) / 2;
  const cy = (height - 1) / 2;
  const outer = Math.min(width, height) * 0.16;
  const inner = Math.min(width, height) * 0.09;
  return png(width, height, (x, y) => {
    const d = Math.hypot(x - cx, y - cy);
    if (d <= inner) return ACCENT;
    if (d <= outer && d >= inner + Math.min(width, height) * 0.028) return ACCENT;
    return BG;
  });
}

mkdirSync(OUT_DIR, { recursive: true });
const files = [
  ['icon.png', icon(1024)],
  ['adaptive-icon.png', adaptiveForeground(1024)],
  ['splash.png', splash(1284, 2778)],
  ['favicon.png', icon(48)],
];
for (const [name, data] of files) {
  writeFileSync(resolve(OUT_DIR, name), data);
  console.log(`wrote ${name} (${data.length} bytes)`);
}
