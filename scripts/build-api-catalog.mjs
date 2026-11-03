import { readFileSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { join, resolve } from 'node:path';
export const root = fileURLToPath(new URL('../', import.meta.url));
export const services = ['campus-api-gateway', 'tenant-user-service', 'campus-core-api', 'campus-engagement-api', 'campus-operations-api'];
const json = path => JSON.parse(readFileSync(path, 'utf8'));
export function render() {
  const specs = Object.fromEntries(services.map(name => [name, json(join(root, 'api', name + '.json'))]));
  return readFileSync(join(root, 'source/api-catalog.html'), 'utf8')
    .replace('/*API_CONTRACTS*/', JSON.stringify(specs).replaceAll('<', '\\u003c'));
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.includes('--sync')) {
    for (const name of services.filter(s => s !== 'campus-operations-api')) {
      copyFileSync(join(root, '..', name, 'docs/openapi.json'), join(root, 'api', name + '.json'));
      copyFileSync(join(root, '..', name, 'docs/api-coverage.json'), join(root, 'api', name + '.coverage.json'));
    }
  }
  const assets = join(root, 'previews/api-assets');
  mkdirSync(assets, { recursive: true });
  for (const name of ['swagger-ui-bundle.js', 'swagger-ui.css', 'LICENSE', 'NOTICE']) {
    copyFileSync(join(root, 'node_modules/swagger-ui-dist', name), join(assets, name));
  }
  writeFileSync(join(root, 'previews/school-api-swagger.html'), render());
  console.log('Built offline Swagger catalogue for five services. No runtime APIs changed.');
}
