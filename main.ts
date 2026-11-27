// main.ts — entry for make.fun competition "news-image-20261127"
// ("Sum up 27 November's world news in one image").
//
// The entry image is the newspaper front page stored beside this file as
// entry.png ("THE WORLD TODAY", Friday 27 November 2026). This program:
//
//   1. loads entry.png from the bot directory (MAKEFUN_BOT_DIR, else /bot),
//   2. checks it against the competition gate by hand — PNG signature,
//      a 1 MiB size cap, and a CRC-32 pass over *every* chunk in the file,
//      so a truncated or corrupted image fails here rather than at judging,
//   3. writes the bytes unchanged to MAKEFUN_OUTPUT_DIR/entry.png
//      (default /output), creating the directory if needed,
//   4. reads the written file back and compares it byte for byte,
//   5. prints a short report of what it did.
//
// Any failed check exits with code 1 and a message on stderr.
//
// makefun anchor 70dff4c1b47b2d719ca3be5b55361e3a743164ca round 34315818

import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const LIMIT_BYTES = 1_048_576; // the gate's 1 MiB cap on the entry image
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const srcPath = join(botDir, "entry.png");
const dstPath = join(outDir, "entry.png");

function die(message: string): never {
  console.error(`entry error: ${message}`);
  process.exit(1);
}

// --- CRC-32 (the PNG chunk checksum), table-driven -------------------------
const crcTable = new Uint32Array(256);
for (let n = 0; n < 256; n++) {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  crcTable[n] = c >>> 0;
}

function crc32(buf: Buffer, start: number, end: number): number {
  let crc = 0xffffffff;
  for (let i = start; i < end; i++) {
    crc = crcTable[(crc ^ buf[i]) & 0xff] ^ (crc >>> 8);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

// --- load and validate -------------------------------------------------------
if (!existsSync(srcPath)) die(`no entry image at ${srcPath}`);
const png = readFileSync(srcPath);

if (png.length === 0) die("entry image is empty");
if (png.length > LIMIT_BYTES) die(`entry image is ${png.length} bytes, over the 1 MiB cap`);
if (!PNG_MAGIC.every((b, i) => png[i] === b)) die("entry image lacks the PNG signature");

// Walk the chunk list: 4-byte length, 4-byte type, data, 4-byte CRC.
// The walk must land exactly on the end of the file, with an IEND seen.
let offset = 8;
let sawIend = false;
let width = 0;
let height = 0;
while (offset < png.length) {
  if (offset + 12 > png.length) die(`chunk header runs past end of file at ${offset}`);
  const length = png.readUInt32BE(offset);
  const type = png.toString("ascii", offset + 4, offset + 8);
  const dataEnd = offset + 8 + length;
  if (dataEnd + 4 > png.length) die(`chunk ${type} runs past end of file`);
  if (crc32(png, offset + 4, dataEnd) !== png.readUInt32BE(dataEnd)) {
    die(`chunk ${type} has a bad CRC-32`);
  }
  if (type === "IHDR") {
    width = png.readUInt32BE(offset + 8);
    height = png.readUInt32BE(offset + 12);
  }
  if (type === "IEND") sawIend = true;
  offset = dataEnd + 4;
}
if (offset !== png.length) die("trailing bytes after the last PNG chunk");
if (!sawIend) die("no IEND chunk: the PNG is truncated");
if (width === 0 || height === 0) die("IHDR reports a zero dimension");
if (width > 1024 || height > 1024) die(`image is ${width}x${height}, over the 1024x1024 cap`);

// --- copy, then verify the copy ----------------------------------------------
mkdirSync(outDir, { recursive: true });
writeFileSync(dstPath, png);

const back = readFileSync(dstPath);
if (!back.equals(png)) die("the written copy differs from the source image");

// The report includes the image's SHA-256 so a run's output can be matched
// against the file in the repository without comparing bytes by eye.
const digest = createHash("sha256").update(png).digest("hex");
console.log(`entry image: ${srcPath}`);
console.log(`size: ${png.length} bytes, ${width}x${height}`);
console.log(`sha256: ${digest}`);
console.log(`written to: ${dstPath} (byte-identical)`);
