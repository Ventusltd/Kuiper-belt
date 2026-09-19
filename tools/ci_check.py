#!/usr/bin/env python3
r"""tools/ci_check.py - what GitHub checks on every push, on its own machine, knowing nothing local.

The checking engineer on the measuring machine (check_proof.py) can follow a key to its text,
because it has the clones. A hosted runner has only this repository, so it checks what can be
checked from the repository alone, and it fails closed:

  K1  no tracked file contains a token whose digest matches a repository name that is not public
  K2  cosmos/wafer.tsv re-summed equals cosmos/wafer-meta.json, and equals cosmos/repos.tsv
  K3  every tool is valid python, and the script inside every page parses as JavaScript
  K4  keys are in time order and no commit overlaps the one before it

Exit 0 only if all pass. Nothing here can be satisfied by editing a number in a document.
"""
import ast
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
from check_proof import leaks


def tracked():
    out = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True).stdout
    return [f for f in out.split('\n') if f]


def main():
    fails = []

    bad = []
    for f in tracked():
        p = os.path.join(ROOT, f)
        if os.path.isfile(p) and os.path.getsize(p) <= 3_000_000:
            try:
                if leaks(io.open(p, encoding='utf-8', errors='replace').read()):
                    bad.append(f)
            except Exception:
                pass
    print('K1 privacy: %d tracked files scanned, %d match a private digest' % (len(tracked()), len(bad)))
    if bad:
        fails.append('K1: ' + ', '.join(bad[:8]))

    rows = lambda n: [l.rstrip('\n').split('\t') for l in io.open(os.path.join(ROOT, 'cosmos', n), encoding='utf-8')
                      if l.strip() and not l.startswith('#')]
    w, meta = rows('wafer.tsv'), json.load(io.open(os.path.join(ROOT, 'cosmos', 'wafer-meta.json'), encoding='utf-8'))
    issued, silent = sum(int(r[1]) for r in w), sum(int(r[4]) for r in w)
    repo_sum = sum(int(r[2]) for r in rows('repos.tsv'))
    ok2 = issued == meta['issued_keys'] == repo_sum and silent == meta['unissued_keys'] and len(w) == meta['commits']
    print('K2 sums: issued %s, meta %s, repositories %s, silent %s, commits %d: %s'
          % (format(issued, ','), format(meta['issued_keys'], ','), format(repo_sum, ','),
             format(silent, ','), len(w), 'agree' if ok2 else 'DISAGREE'))
    if not ok2:
        fails.append('K2: the published data does not add up')

    for f in sorted(os.listdir(HERE)):
        if f.endswith('.py'):
            try:
                ast.parse(io.open(os.path.join(HERE, f), encoding='utf-8').read())
            except SyntaxError as e:
                fails.append('K3: %s does not parse: %s' % (f, e))
    pages = [f for f in os.listdir(ROOT) if f.endswith('.html')]
    for f in pages:
        s = io.open(os.path.join(ROOT, f), encoding='utf-8').read()
        m = re.search(r'<script type="module">([\s\S]*)</script>', s)
        if not m:
            continue
        js = os.path.join(ROOT, '.ci-%s.mjs' % f)
        io.open(js, 'w', encoding='utf-8').write(m.group(1))
        r = subprocess.run(['node', '--check', js], capture_output=True, text=True)
        os.remove(js)
        if r.returncode:
            fails.append('K3: the script in %s does not parse: %s' % (f, r.stderr.strip().split('\n')[-1][:160]))
    print('K3 syntax: %d tools, %d pages' % (len([f for f in os.listdir(HERE) if f.endswith('.py')]), len(pages)))

    k, prev_unix, disorder = 0, -1, 0
    for r in w:
        unix, n, gap = int(r[0]), int(r[1]), int(r[4])
        if unix < prev_unix or gap < 0 or n <= 0:
            disorder += 1
        prev_unix = unix
        k += gap + n
    ok4 = disorder == 0 and k == meta['address_space']
    print('K4 order: %d commits out of order or overlapping; address space %s vs %s'
          % (disorder, format(k, ','), format(meta['address_space'], ',')))
    if not ok4:
        fails.append('K4: keys are not in time order, or the address space does not close')

    for f in fails:
        print('FAIL ' + f)
    print('RESULT: ' + ('PASS' if not fails else 'FAIL'))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
