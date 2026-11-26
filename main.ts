// news-image-20261126 entrypoint (Node 22, standard library only).
//
// The picture for Thursday 26 November 2026 is the entry.png sitting next to
// this file. The job here is small: prove the file really is a PNG, then put
// a byte-for-byte copy where the grader looks for it.
//
// In the grading container the destination is /output; anywhere else the
// MAKEFUN_OUTPUT_DIR environment variable names the folder to use instead:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const here = fileURLToPath(new URL('.', import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');

const bytes = readFileSync(source);

const looksLikePng =
  bytes.length > PNG_MAGIC.length &&
  PNG_MAGIC.every((b, i) => bytes[i] === b);
if (!looksLikePng) {
  throw new Error(`entry.png does not start with the PNG signature`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(dest, bytes);

console.log(`entry.png: ${bytes.length} bytes -> ${dest}`);
