// news-image-20261118 entry point (Node 22, standard library only).
//
// The front page itself is baked into entry.png, composed by compose.py
// (PIL) from four AI-generated editorial illustrations in assets/ plus
// five hand-drawn flat icons; every headline and label on the page was
// rendered by that script, so the image carries no garbled AI text.
// This program only delivers the finished image to the grader: it reads
// entry.png beside this file, creates the output directory, writes the
// bytes unchanged to entry.png there, and refuses to finish unless the
// written file is byte-for-byte the same size as the source.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const targetPath = join(outDir, 'entry.png');

const bytes: Buffer = readFileSync(sourcePath);
mkdirSync(outDir, { recursive: true });
writeFileSync(targetPath, bytes);

const written = statSync(targetPath);
if (written.size !== bytes.length) {
  throw new Error(
    `entry.png copy mismatch: wrote ${written.size} bytes, ` +
    `source is ${bytes.length} bytes`,
  );
}
console.log(`wrote ${targetPath} (${written.size} bytes)`);
