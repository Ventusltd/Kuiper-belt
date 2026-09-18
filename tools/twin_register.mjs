#!/usr/bin/env node
// tools/twin_register.mjs
// Join the repository level host verdicts to the key level twins, so every key knows
// which universes it exists in.
//
//   node tools/twin_register.mjs [--twins data/twins-<run>.json] [--entangle <path to entangle.json>]
//
// No per key network work and no per key hashing. A commit SHA is a Merkle root over the
// tree, so one matching commit certifies every key inside it. Keys inherit the certification
// of the tree that contains them. Comparing them individually would be a check that cannot
// fail, and a check that cannot fail examines nothing.

import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i < 0 ? d : argv[i + 1]; };

const latestTwins = () => {
  if (!existsSync('data')) return null;
  const f = readdirSync('data').filter(n => /^twins-.*\.json$/.test(n)).sort();
  return f.length ? join('data', f[f.length - 1]) : null;
};

const TWINS = arg('--twins', latestTwins());
const ENTANGLE = arg('--entangle', 'C:/Users/vikra/Documents/GitHub/star-electron-star/entangle.json');

if (!TWINS || !existsSync(TWINS)) { console.error('FAIL: no twins record. Run entangle_hosts.mjs first.'); process.exit(1); }
if (!existsSync(ENTANGLE)) { console.error(`FAIL: no entangle.json at ${ENTANGLE}`); process.exit(1); }

const twins = JSON.parse(readFileSync(TWINS, 'utf8'));
const ent = JSON.parse(readFileSync(ENTANGLE, 'utf8'));
const perRepo = ent.per_repo || {};
if (Object.keys(perRepo).length === 0) { console.error('FAIL: entangle.json carries no per_repo. Refusing.'); process.exit(1); }

// The key index names repositories as "<owner>/<name>". The twin record names them "<name>".
const byName = new Map();
for (const [full, v] of Object.entries(perRepo)) byName.set(full.split('/').pop().toLowerCase(), { full, ...v });

const rows = [];
let certified = 0, suspect = 0, uncertified = 0, orphanKeys = 0;

for (const b of twins.bodies) {
  const k = byName.get(b.body.toLowerCase());
  const keys = k ? (k.resolved ?? k.keys ?? 0) : 0;
  // A key is only as entangled as the tree that carries it.
  let state;
  if (!k) state = 'NO KEYS';
  else if (b.verdict === 'HONOURED') { state = 'CERTIFIED'; certified += keys; }
  else if (b.verdict === 'OVERREACHED') { state = 'SUSPECT'; suspect += keys; }   // pink, per the protocol
  else { state = 'UNCERTIFIED'; uncertified += keys; }

  rows.push({
    body: b.body,
    keys,
    key_source: k ? k.full : null,
    state,
    verdict: b.verdict,
    commit: b.github?.commit ?? null,
    tree: b.github?.tree ?? null,
    hosts: [b.github ? 'github' : null, b.gitlab ? 'gitlab' : null].filter(Boolean),
    observed_at: b.github?.observed_at ?? twins.rules?.asof ?? null,
  });
}

// Keys whose repository was not observed at all are named, never merely counted.
const observed = new Set(twins.bodies.map(b => b.body.toLowerCase()));
const missing = [...byName.entries()].filter(([n]) => !observed.has(n)).map(([, v]) => v.full);
for (const m of missing) orphanKeys += (byName.get(m.split('/').pop().toLowerCase()).resolved ?? 0);

const total = ent.keys ?? (certified + suspect + uncertified + orphanKeys);
const register = {
  schema: 'twin-register-v1',
  run: twins.run,
  law: 'Keys inherit the host certification of the tree that contains them. One commit SHA certifies every key inside it.',
  rules: { ...twins.rules, key_index: ENTANGLE, key_index_generated: ent.generated_utc ?? null },
  totals: { keys_in_index: total, certified, suspect, uncertified, in_repos_not_observed: orphanKeys },
  repositories_with_keys_not_observed: missing.sort(),
  bodies: rows.sort((a, b) => b.keys - a.keys),
};

const json = JSON.stringify(register, null, 1);
mkdirSync('data', { recursive: true }); mkdirSync('proof', { recursive: true });
writeFileSync(join('data', `register-${twins.run}.json`), json);
const digest = createHash('sha256').update(json).digest('hex');
writeFileSync(join('proof', `${twins.run}-register.json`), JSON.stringify({
  run: twins.run, digest, totals: register.totals,
  command: 'node tools/twin_register.mjs ' + argv.join(' '),
}, null, 1));

const pct = total ? ((certified / total) * 100).toFixed(2) : '0.00';
console.log(`key index ${ENTANGLE}`);
console.log(`generated  ${ent.generated_utc ?? 'unstated'}`);
console.log(`keys       ${total}`);
console.log(`CERTIFIED  ${certified}  (${pct}% present and identical in both universes)`);
console.log(`SUSPECT    ${suspect}   (repository diverged between hosts; draw pink)`);
console.log(`UNCERTIFIED ${uncertified}  (one host only, so far)`);
if (missing.length) console.log(`repositories with keys but no observation: ${missing.join(', ')}`);
console.log(`\nregister digest ${digest}`);

// Below 95 per cent the protocol refuses to write a claim of entanglement.
if (total && certified / total < 0.95) {
  console.log('\nBELOW THRESHOLD: under 95 per cent certified. This is a report, not a claim of entanglement.');
  process.exit(1);
}
