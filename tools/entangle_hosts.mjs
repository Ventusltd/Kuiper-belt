#!/usr/bin/env node
// tools/entangle_hosts.mjs
// Pair every repository across two hosts and reconcile them under LAWS.md L10.
//
//   node tools/entangle_hosts.mjs --roots <dir> --namespace <gitlab-namespace> [--push] [--asof <iso>]
//
// Without --push it observes and reconciles only. Nothing is ever force pushed:
// a divergence is evidence, and overwriting evidence destroys the witness.

import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readdirSync, existsSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { join, basename } from 'node:path';

const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i < 0 ? d : argv[i + 1]; };
const has = (k) => argv.includes(k);

const ROOTS = (arg('--roots', 'C:/Users/vikra/Documents/GitHub')).split(',');
const NS = arg('--namespace', '');
const PUSH = has('--push');
const ASOF = arg('--asof', new Date().toISOString());
const RULES = { host_a: 'github', host_b: 'gitlab', tolerance: 'exact', push: PUSH, asof: ASOF };

if (!NS) { console.error('FAIL: --namespace is required'); process.exit(1); }

const git = (cwd, args) =>
  execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
const tryGit = (cwd, args) => { try { return git(cwd, args); } catch { return null; } };

// A body is a repository with a git directory and a github origin.
const bodies = [];
for (const root of ROOTS) {
  for (const name of readdirSync(root)) {
    const dir = join(root, name);
    if (!existsSync(join(dir, '.git'))) continue;
    const origin = tryGit(dir, ['remote', 'get-url', 'origin']);
    if (!origin || !/github\.com/i.test(origin)) continue;
    bodies.push({ name, dir, origin });
  }
}
if (bodies.length === 0) { console.error('FAIL: zero bodies. A check that examines nothing refuses.'); process.exit(1); }

// Observe one host: the ref, the commit, and the tree, which is the Merkle root over the contents.
const observe = (dir, remote, branch) => {
  const ls = tryGit(dir, ['ls-remote', remote, `refs/heads/${branch}`]);
  if (!ls) return null;
  const commit = ls.split(/\s+/)[0];
  if (!commit) return null;
  const tree = tryGit(dir, ['rev-parse', `${commit}^{tree}`]); // null if not fetched locally
  return { host: remote, ref: branch, commit, tree, observed_at: ASOF };
};

const results = [];
for (const b of bodies) {
  const branch = tryGit(b.dir, ['rev-parse', '--abbrev-ref', 'HEAD']) || 'main';
  const gl = `git@gitlab.com:${NS}/${b.name.toLowerCase()}.git`;

  if (!tryGit(b.dir, ['remote', 'get-url', 'gitlab'])) tryGit(b.dir, ['remote', 'add', 'gitlab', gl]);
  else tryGit(b.dir, ['remote', 'set-url', 'gitlab', gl]);

  let pushed = null;
  if (PUSH) {
    // Non destructive. GitLab push-to-create makes the project on first push.
    try { git(b.dir, ['push', 'gitlab', `${branch}:${branch}`]); git(b.dir, ['push', '--tags', 'gitlab']); pushed = 'ok'; }
    catch (e) { pushed = 'refused: ' + String(e.stderr || e.message).split('\n')[0]; }
  }

  const a = observe(b.dir, 'origin', branch);
  const bb = observe(b.dir, 'gitlab', branch);

  // L10. The verdict is settled by pinned evidence, never by recency or plausibility.
  let verdict, detail;
  if (!a || !bb) { verdict = 'NOT EVALUATED'; detail = !a ? 'no observation from github' : 'no observation from gitlab'; }
  else if (a.commit === bb.commit) { verdict = 'HONOURED'; detail = `both hosts at ${a.commit}`; }
  else { verdict = 'OVERREACHED'; detail = `github ${a.commit} against gitlab ${bb.commit}; first deviation is the ref itself`; }

  results.push({ body: b.name, branch, verdict, detail, pushed, github: a, gitlab: bb });
  console.log(`${verdict.padEnd(13)} ${b.name}  ${detail}`);
}

// Record, then hash the record. The digest is the key the claim carries.
mkdirSync('data', { recursive: true }); mkdirSync('proof', { recursive: true });
const runId = ASOF.replace(/[-:]/g, '').slice(0, 15) + 'Z';
const record = { schema: 'twin-register-v1', rules: RULES, run: runId, bodies: results.sort((x, y) => x.body.localeCompare(y.body)) };
const json = JSON.stringify(record, null, 1);
writeFileSync(join('data', `twins-${runId}.json`), json);

const sha256 = (s) => createHash('sha256').update(s).digest('hex');
const counts = results.reduce((m, r) => (m[r.verdict] = (m[r.verdict] || 0) + 1, m), {});
const proof = { run: runId, asof: ASOF, digest: sha256(json), bodies: results.length, verdicts: counts,
  command: 'node tools/entangle_hosts.mjs ' + argv.join(' '), rules: RULES };
writeFileSync(join('proof', `${runId}.json`), JSON.stringify(proof, null, 1));

// The drift log, written between markers so it is idempotent and revertible.
const START = '<!-- DRIFT:START -->', END = '<!-- DRIFT:END -->';
const drift = [START,
  `### Host entanglement, ${ASOF}`, '',
  `Run \`${runId}\`, digest \`${proof.digest}\`. ${results.length} bodies. ` +
  Object.entries(counts).map(([k, v]) => `${v} ${k}`).join(', ') + '.', '',
  ...results.filter(r => r.verdict !== 'HONOURED').map(r => `- **${r.verdict}** \`${r.body}\`: ${r.detail}`),
  results.every(r => r.verdict === 'HONOURED') ? 'No divergence. Every body is paired on both hosts.' : '',
  '', `Reconciled under LAWS.md L10: settled by pinned evidence, never by recency or plausibility.`, END].join('\n');

for (const r of results) {
  const readme = join(bodies.find(b => b.name === r.body).dir, 'README.md');
  if (!existsSync(readme)) continue;
  const cur = readFileSync(readme, 'utf8');
  const one = [START, `### Host entanglement, ${ASOF}`, '',
    `**${r.verdict}.** ${r.detail}`, '', `Run \`${runId}\`, digest \`${proof.digest}\`. LAWS.md L10.`, END].join('\n');
  const next = cur.includes(START) ? cur.replace(new RegExp(`${START}[\s\S]*?${END}`), one) : cur.trimEnd() + '\n\n' + one + '\n';
  if (next !== cur) writeFileSync(readme, next);
}
writeFileSync('DRIFT.md', drift + '\n');

const bad = results.filter(r => r.verdict === 'OVERREACHED').length;
console.log(`\nrun ${runId} digest ${proof.digest}`);
console.log(Object.entries(counts).map(([k, v]) => `${k}: ${v}`).join('  |  '));
process.exit(bad > 0 ? 1 : 0);
