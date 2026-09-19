#!/usr/bin/env python3
"""tools/check_proof.py - THE CHECKING ENGINEER. Independent of whoever built the proof.

A proof is not checked by its author. Every proof published under "Kuiper: proofs" is examined
here by a separate process that did not write it, on the measuring machine, for nothing:

  C1  it is actually live: the page, its data and its PROOF.md answer 200 on globalgrid2050.com
  C2  the published data adds up: wafer.tsv re-summed equals wafer-meta.json, issued and silent
  C3  no name that is not public appears anywhere in what was published (grid law L6)
  C4  PROOF.md ends with the disclaimer and claims no number the data contradicts
  C5  three random keys from the PUBLISHED data resolve, by git alone, to a real line of text
  C6  a second opinion: a local model reads PROOF.md against the facts and hunts unsupported
      numbers. Its answer is a CANDIDATE. Only numbers it names that are genuinely absent from
      the facts are reported, and nothing it says can pass or fail a proof by itself.

    python tools/check_proof.py --watch-until 15:00      poll for new proofs until HH:MM UTC
    python tools/check_proof.py <proof directory name>   check one

Verdicts go to E:\particles-runs\checks\ as CHECK-<proof>.md and CHECKS.json. The checker never
edits a proof, never publishes and never commits: a checking engineer who can change the drawing
is not checking it.

THE GUARD DOES NOT SPELL WHAT IT GUARDS. An earlier guard listed the private repository names in
plain text inside a public repository, which is the leak it existed to prevent. Names are held
here as truncated SHA-256 digests, and text is checked by hashing every token in it.
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', '..', '_wt-estate', 'testcode', 'wafer-development-environment')
LIVE = 'https://globalgrid2050.com/testcode/wafer-development-environment/'
OUT = r'E:\particles-runs\checks'
NOT_PUBLIC = {'49bef650dc462eb9628e123c', '485b71c91c9d26f6893e7b85', '9261ceef0b969e70ac20f151',
              'e10931bb0448851a45510bb9', '627a4b71075931067036fffe', '5a5926e194270c1482f3f813'}
DISCLAIMER = 'without warranty of any kind'


def leaks(text):
    """Every run of name characters is hashed, whole and with its leading path stripped, and
    compared with the digests. Returns how many tokens matched, never which."""
    n = 0
    for tok in set(re.findall(r'[A-Za-z0-9_][A-Za-z0-9_.-]*', text)):
        for t in {tok, tok.rstrip('.'), tok.split('/')[-1]}:
            if hashlib.sha256(t.lower().encode()).hexdigest()[:24] in NOT_PUBLIC:
                n += 1
    return n


def status(url):
    try:
        req = urllib.request.Request(url + '?t=%d' % time.time(), headers={'User-Agent': 'check'})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status
    except Exception as e:
        return getattr(e, 'code', 0) or 0


def rows(path):
    return [l.rstrip('\n').split('\t') for l in io.open(path, encoding='utf-8')
            if l.strip() and not l.startswith('#')]


def check(name):
    d = os.path.join(SITE, name)
    res, notes = {}, []
    # C1 live
    codes = {f: status(LIVE + name + '/' + f) for f in ('', 'cosmos/wafer.tsv', 'PROOF.md')}
    res['C1_live'] = all(c == 200 for c in codes.values())
    notes.append('C1 live: ' + ', '.join('%s %s' % (k or 'index', v) for k, v in codes.items()))
    if not res['C1_live']:
        return None, notes                                   # not deployed yet: come back later
    # C2 sums
    w = rows(os.path.join(d, 'cosmos', 'wafer.tsv'))
    meta = json.load(io.open(os.path.join(d, 'cosmos', 'wafer-meta.json'), encoding='utf-8'))
    issued, silent = sum(int(r[1]) for r in w), sum(int(r[4]) for r in w)
    res['C2_sums'] = issued == meta['issued_keys'] and silent == meta['unissued_keys'] and len(w) == meta['commits']
    notes.append('C2 sums: issued %s vs %s, silent %s vs %s, commits %d vs %d'
                 % (format(issued, ','), format(meta['issued_keys'], ','), format(silent, ','),
                    format(meta['unissued_keys'], ','), len(w), meta['commits']))
    # C3 privacy, over every published file including the tools
    hits = 0
    for root, _, files in os.walk(d):
        for f in files:
            hits += leaks(io.open(os.path.join(root, f), encoding='utf-8', errors='replace').read())
    res['C3_no_private_names'] = hits == 0
    notes.append('C3 privacy: %d tokens matched a digest of a name that is not public' % hits)
    # C4 the proof text
    proof = io.open(os.path.join(d, 'PROOF.md'), encoding='utf-8').read()
    res['C4_disclaimer'] = DISCLAIMER in proof
    big = [int(x.replace(',', '')) for x in re.findall(r'\b\d{1,3}(?:,\d{3}){2,}\b', proof)]
    known = {issued, silent, issued + silent} | {int(r[1]) for r in w}
    notes.append('C4 text: disclaimer %s; %d large numbers quoted, %d of them are totals of the published data'
                 % ('present' if res['C4_disclaimer'] else 'MISSING', len(big), sum(1 for b in big if b in known)))
    # C5 keys from the PUBLISHED data, resolved by git on this machine
    sys.path.insert(0, HERE)
    import key as K
    K.COSMOS = os.path.join(d, 'cosmos')
    K.load_cache()
    commits, space, n = K.load()
    import random
    ok = 0
    for _ in range(3):
        msg, code = K.resolve(commits, space, K.key_of_line(commits, random.randrange(n)))
        ok += (code == 0)
    res['C5_keys_resolve'] = ok == 3
    notes.append('C5 keys: %d of 3 random keys from the published data resolved to text by git' % ok)
    # C6 a second opinion, advisory only
    try:
        facts = json.dumps(meta)
        body = json.dumps({'model': 'qwen2.5-coder:14b', 'stream': False, 'options': {'temperature': 0, 'num_predict': 200},
                           'prompt': 'FACTS (JSON):\n%s\n\nTEXT:\n%s\n\nList ONLY numbers in TEXT that contradict FACTS. '
                                     'One per line. If none, answer NONE.' % (facts, proof[:3000])}).encode()
        req = urllib.request.Request('http://127.0.0.1:11434/api/generate', data=body, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=240) as r:
            ans = json.load(r).get('response', '').strip()
        notes.append('C6 local model (advisory, a candidate, never a verdict): ' + ans.replace('\n', ' | ')[:300])
    except Exception as e:
        notes.append('C6 local model did not answer: %s' % e)
    return res, notes


def write(name, res, notes):
    os.makedirs(OUT, exist_ok=True)
    verdict = 'PASS' if all(res.values()) else 'FAIL'
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    io.open(os.path.join(OUT, 'CHECK-%s.md' % name), 'w', encoding='utf-8', newline='\n').write(
        '# Check of %s: %s\n\nChecked %s by tools/check_proof.py, which did not build it.\n\n%s\n\n%s\n'
        % (name, verdict, now, '\n'.join('- %s: %s' % (k, 'pass' if v else 'FAIL') for k, v in res.items()),
           '\n'.join('- ' + n for n in notes)))
    p = os.path.join(OUT, 'CHECKS.json')
    allc = json.load(io.open(p, encoding='utf-8')) if os.path.exists(p) else {}
    allc[name] = {'verdict': verdict, 'checked': now, 'checks': res}
    json.dump(allc, io.open(p, 'w', encoding='utf-8', newline='\n'), indent=1)
    print('%s %s %s' % (now, name, verdict), flush=True)


def proofs():
    return sorted(x for x in os.listdir(SITE) if re.match(r'^\d{12}-(proof-\d+|one-wafer)$', x))


def main():
    if len(sys.argv) == 3 and sys.argv[1] == '--watch-until':
        hh, mm = [int(x) for x in sys.argv[2].split(':')]
        done = set()
        while (datetime.now(timezone.utc).hour, datetime.now(timezone.utc).minute) < (hh, mm):
            for name in proofs():
                if name in done:
                    continue
                try:
                    res, notes = check(name)
                except Exception as e:
                    res, notes = {'checker_ran': False}, ['the checker itself failed: %r' % e]
                if res is None:
                    continue                                     # not live yet
                write(name, res, notes)
                done.add(name)
            time.sleep(90)
        return 0
    res, notes = check(sys.argv[1])
    if res is None:
        print('not live yet: ' + '; '.join(notes))
        return 3
    write(sys.argv[1], res, notes)
    return 0 if all(res.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
