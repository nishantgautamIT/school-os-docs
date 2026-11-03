// Canonical copy lives in school-os-docs. Also shipped in each HTTP service.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import ts from 'typescript';

export const digest = value => createHash('sha256').update(value).digest('hex');
const verbs = new Set(['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']);
function files(directory) {
  if (!existsSync(directory)) return [];
  return readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? files(path) : /\.[cm]?[jt]s$/.test(path) ? [path] : [];
  });
}
function literal(node) {
  if (!node) return '';
  assert(ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node),
    'Dynamic route/controller metadata requires explicit support in the API coverage checker');
  return node.text;
}
export function inventory(root) {
  const routes = [], handlers = [], native = [];
  for (const path of files(join(root, 'src'))) {
    const source = readFileSync(path, 'utf8'), name = relative(root, path).replaceAll('\\', '/');
    const tree = ts.createSourceFile(name, source, ts.ScriptTarget.Latest, true);
    const imports = new Map();
    for (const statement of tree.statements) {
      if (ts.isImportDeclaration(statement) && statement.moduleSpecifier.text === '@nestjs/common') {
        const bindings = statement.importClause?.namedBindings;
        if (bindings && ts.isNamedImports(bindings)) {
          for (const binding of bindings.elements) imports.set(binding.name.text, (binding.propertyName ?? binding.name).text);
        }
      }
    }
    const decorators = node => (ts.canHaveDecorators(node) ? ts.getDecorators(node) ?? [] : [])
      .filter(d => ts.isCallExpression(d.expression))
      .map(d => ({ name: imports.get(d.expression.expression.getText(tree)), args: d.expression.arguments }));
    let isHandler = false;
    function visit(node) {
      if (ts.isClassDeclaration(node)) {
        const controller = decorators(node).find(d => d.name === 'Controller');
        if (controller) {
          isHandler = true;
          const prefix = literal(controller.args[0]);
          for (const member of node.members) {
            for (const d of decorators(member)) {
              const method = d.name?.toLowerCase();
              assert(method !== 'all', '@All requires explicit methods in the API contract');
              if (!verbs.has(method)) continue;
              const path = ('/' + [prefix, literal(d.args[0])].filter(Boolean).join('/'))
                .replace(/:([A-Za-z_][A-Za-z0-9_]*)/g, '{$1}');
              assert(!/[?*]/.test(path), 'Wildcard/optional routes require explicit checker support');
              routes.push(`${method.toUpperCase()} ${path}`);
              if (method === 'get') routes.push(`HEAD ${path}`); // Current FastifyAdapter defaults.
            }
          }
        }
      }
      ts.forEachChild(node, visit);
    }
    visit(tree);
    if (isHandler) handlers.push(name);
    // Native listeners cannot be derived from decorators. Any changed routing
    // code must be reviewed against the manifest and OpenAPI; hashes fail closed.
    if (/\bcreate(?:Secure)?Server\s*\(/.test(source) ||
        /(?:from\s*|require\s*\()\s*['"](?:fastify|express|koa|hono)['"]/.test(source) ||
        /\.(?:route|register|setGlobalPrefix|enableVersioning)\s*\(/.test(source)) native.push(name);
  }
  return { routes: [...new Set(routes)].sort(), handlers: handlers.sort(), native: native.sort() };
}
export function checkContract(root, spec, manifest) {
  assert.equal(spec.openapi, '3.0.3');
  assert(spec.info?.title && spec.info?.version && spec.paths, 'OpenAPI metadata is required');
  const documented = [], ids = new Set();
  for (const [path, item] of Object.entries(spec.paths)) {
    assert(path.startsWith('/'), 'Paths must start with /');
    for (const [method, operation] of Object.entries(item)) {
      if (!verbs.has(method)) continue;
      assert(operation.summary && operation.description && operation.operationId, `${method} ${path}: description required`);
      assert(!ids.has(operation.operationId), 'operationId must be unique'); ids.add(operation.operationId);
      assert(Object.keys(operation.responses ?? {}).some(c => /^2\d\d$/.test(c)), 'Success response required');
      assert(Array.isArray(operation.security), 'Explicit public/private security required');
      for (const match of path.matchAll(/\{([^}]+)\}/g)) {
        assert([...(item.parameters ?? []), ...(operation.parameters ?? [])].some(p => p.in === 'path' && p.name === match[1] && p.required), `Missing path parameter ${match[1]}`);
      }
      documented.push(`${method.toUpperCase()} ${path}`);
    }
  }
  const found = inventory(root);
  assert.deepEqual(found.native, [...manifest.nativeFiles].sort(), 'New/removed native HTTP surface: review and update API coverage manifest');
  for (const path of new Set([...found.handlers, ...found.native])) {
    assert(manifest.sources[path], `Missing reviewed API source: ${path}`);
  }
  for (const [path, expected] of Object.entries(manifest.sources)) {
    assert(!path.includes('..') && (path.startsWith('src/') || path.startsWith('db/migrations/')), 'Invalid API source path');
    assert.equal(digest(readFileSync(join(root, path))), expected,
      `${path}: API source changed. Review schemas/security/responses and refresh api-coverage.json in the same PR.`);
  }
  assert.deepEqual(documented.sort(), [...new Set([...found.routes, ...manifest.nativeRoutes])].sort(),
    'HTTP routes and OpenAPI differ; document new routes and remove stale paths');
  return documented.length;
}
