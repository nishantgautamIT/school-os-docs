import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import SwaggerParser from '@apidevtools/swagger-parser';
import { checkContract } from './api-contract-guard.mjs';
import { root, render, services } from './build-api-catalog.mjs';
for (const name of services) {
  const specPath = join(root, 'api', name + '.json');
  const spec = JSON.parse(readFileSync(specPath, 'utf8'));
  await SwaggerParser.validate(spec);
  if (process.argv.includes('--sources')) {
    const repo = join(root, '..', name);
    const manifest = JSON.parse(readFileSync(join(root, 'api', name + '.coverage.json'), 'utf8'));
    const count = checkContract(repo, spec, manifest);
    if (name !== 'campus-operations-api') {
      assert.equal(readFileSync(specPath, 'utf8'), readFileSync(join(repo, 'docs/openapi.json'), 'utf8'), `${name}: catalogue snapshot is stale`);
      assert.equal(readFileSync(join(root, 'scripts/api-contract-guard.mjs'), 'utf8'), readFileSync(join(repo, 'scripts/api-contract-guard.mjs'), 'utf8'), `${name}: guard version differs`);
    }
    console.log(`${name}: ${count} operations match current source`);
  } else console.log(`${name}: valid OpenAPI 3.0.3`);
}
assert.equal(readFileSync(join(root, 'previews/school-api-swagger.html'), 'utf8'), render(), 'Rebuild HTML catalogue');
for (const name of ['swagger-ui-bundle.js', 'swagger-ui.css', 'LICENSE', 'NOTICE']) {
  assert.deepEqual(readFileSync(join(root, 'previews/api-assets', name)), readFileSync(join(root, 'node_modules/swagger-ui-dist', name)), 'Vendored Swagger UI differs from pinned dependency');
}
