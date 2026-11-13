// PROTOTYPE — throwaway. Inlines assets/ into one self-contained page.
// Run: node prototypes/art-direction/build.mjs   → writes prototypes/art-direction/index.html
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const mime = { png: 'image/png', woff2: 'font/woff2' };
const src = readFileSync(join(here, 'src.html'), 'utf8');
const out = src.replace(/__ASSET_([A-Za-z0-9_.-]+)__/g, (_, name) => {
  const ext = name.split('.').pop();
  const b64 = readFileSync(join(here, 'assets', name)).toString('base64');
  return `data:${mime[ext]};base64,${b64}`;
});
writeFileSync(join(here, 'index.html'), out);
console.log(`index.html: ${(out.length / 1024).toFixed(0)} KB`);
