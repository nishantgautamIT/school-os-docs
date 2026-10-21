const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');
const root = path.resolve(__dirname, '..');
const file = path.join(root, 'previews/school-architecture-review.html');
const html = fs.readFileSync(file, 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/);
assert(script, 'missing inline application');
new vm.Script(script[1]);
const modules = JSON.parse(html.match(/const MODULES = (\[[\s\S]*?\]);\nconst \$/)[1]);
assert.equal(modules.length, 40, 'review scope changed; update and inspect the catalogue');
assert.equal(new Set(modules.map(m => m.id)).size, modules.length, 'duplicate module ids');
for (const m of modules) {
  assert(m.steps.length >= 5 && m.tables.length && m.endpoints.length && m.guard, `incomplete architecture: ${m.id}`);
  assert(html.includes(`case '${m.preview}':`), `missing screen: ${m.id}`);
}
for (const marker of ['/*MODULE_DATA*/', '/*SCHOOL_WEBSITE_CODE*/', '/*SCHOOL_WEBSITE_CSS*/']) assert(!html.includes(marker), `unexpanded source ${marker}`);
for (const match of html.matchAll(/href="([^"]+)"/g)) {
  const href = match[1];
  if (/^(https?:|#)/.test(href)) continue;
  assert(fs.existsSync(path.resolve(path.dirname(file), decodeURIComponent(href.split('#')[0]))), `broken local link: ${href}`);
}
assert(html.includes('School website editor') && html.includes('School admin login'), 'latest workflows missing');
console.log(`Review artifact valid: ${modules.length} sections, ${modules.reduce((n,m)=>n+m.steps.length,0)} flow steps, inline JS syntax and local links.`);
