// The World in One Day — 25 November 2026. Node 22, standard library only.
// This entry's image is drawn once, by render_frontpage.py, and shipped in
// this repository as entry.png; the program below only copies that file into
// the grader's output directory. It never touches the network, never reads
// the clock, and never writes anything but those same bytes, so two runs of
// it produce byte-identical output. The copy is done with an explicit read
// and write (rather than copyFileSync) so the program also works when the
// output directory does not exist yet: it creates it first.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
writeFileSync(
  join(outDir, 'entry.png'),
  readFileSync(new URL('./entry.png', import.meta.url)),
);
