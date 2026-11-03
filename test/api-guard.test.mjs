import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { checkContract, digest } from '../scripts/api-contract-guard.mjs';

function fixture(t, source = "import { Controller, Get } from '@nestjs/common'; @Controller('items') class C { @Get(':id') read() {} }") {
  const root = mkdtempSync(join(tmpdir(), 'api-guard-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  mkdirSync(join(root, 'src'));
  writeFileSync(join(root, 'src/app.ts'), source);
  const operation = method => ({ operationId: method, summary: 'Read', description: 'Read a thing', parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }], security: [], responses: { 200: { description: 'OK' } } });
  return { root, source, spec: { openapi: '3.0.3', info: { title: 'Test', version: '1' }, paths: { '/items/{id}': { get: operation('get'), head: operation('head') } } }, manifest: { nativeFiles: [], nativeRoutes: [], sources: { 'src/app.ts': digest(source) } } };
}
test('extracts controller paths, parameters and implicit HEAD', t => {
  const f = fixture(t); assert.equal(checkContract(f.root, f.spec, f.manifest), 2);
});
test('missing operation fails even after source hashes are acknowledged', t => {
  const f = fixture(t); delete f.spec.paths['/items/{id}'].get;
  assert.throws(() => checkContract(f.root, f.spec, f.manifest), /routes and OpenAPI differ/);
});
test('invented operation fails', t => {
  const f = fixture(t); f.spec.paths['/phantom'] = { post: { ...f.spec.paths['/items/{id}'].get, operationId: 'phantom' } };
  assert.throws(() => checkContract(f.root, f.spec, f.manifest), /routes and OpenAPI differ/);
});
test('changed handler semantics require contract review', t => {
  const f = fixture(t); writeFileSync(join(f.root, 'src/app.ts'), f.source.replace('read() {}', 'read() { return {changed:true}; }'));
  assert.throws(() => checkContract(f.root, f.spec, f.manifest), /API source changed/);
});
test('new native listener fails closed', t => {
  const f = fixture(t); writeFileSync(join(f.root, 'src/new.ts'), "import {createServer} from 'node:http'; createServer(() => {});");
  assert.throws(() => checkContract(f.root, f.spec, f.manifest), /native HTTP surface/);
});
test('new decorated route in a new file is detected', t => {
  const f = fixture(t); writeFileSync(join(f.root, 'src/new.ts'), "import {Controller,Post} from '@nestjs/common'; @Controller('other') class C { @Post() create(){} }");
  assert.throws(() => checkContract(f.root, f.spec, f.manifest), /Missing reviewed API source/);
});
test('aliases of Nest decorators are extracted', t => {
  const f = fixture(t, "import {Controller as Ctl,Get as Read} from '@nestjs/common'; @Ctl('items') class C { @Read(':id') read(){} }");
  assert.equal(checkContract(f.root, f.spec, f.manifest), 2);
});
test('dynamic route declarations require extending checker', t => {
  const f = fixture(t, "import {Controller,Get} from '@nestjs/common'; const path='items'; @Controller(path) class C { @Get(':id') read(){} }");
  assert.throws(() => checkContract(f.root, f.spec, f.manifest), /Dynamic route/);
});
test('missing security annotation fails', t => {
  const f = fixture(t); delete f.spec.paths['/items/{id}'].get.security;
  assert.throws(() => checkContract(f.root, f.spec, f.manifest), /security required/);
});
test('missing path parameter fails', t => {
  const f = fixture(t); delete f.spec.paths['/items/{id}'].get.parameters;
  assert.throws(() => checkContract(f.root, f.spec, f.manifest), /Missing path parameter/);
});
test('operator-only service can have an empty contract', t => {
  const f = fixture(t, 'export class Fees {}'); f.spec.paths = {};
  assert.equal(checkContract(f.root, f.spec, f.manifest), 0);
});
