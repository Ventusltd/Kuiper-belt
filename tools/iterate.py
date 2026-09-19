#!/usr/bin/env python3
r"""tools/iterate.py - run many iterations LOCALLY, test each one unattended, keep the best ten.

A hundred iterations overnight must not mean a hundred pushes. An iteration lives on the E: drive
and nowhere else until it has earned its place: it is served from its own folder, its self tests
are run in headless Chrome with nobody watching, the checks that need no browser are run on its
data, and it is given a score made only of things that passed or failed. The best ten are then
published by a person or a captain through tools/publish_proof.py, which has its own ten minute
rule and its own privacy guard. NOTHING IN E:\kuiper-iterations IS EVER COMMITTED.

    python tools/iterate.py new  "what this iteration tries"     copy the current engine into a new numbered folder
    python tools/iterate.py test <n>                            serve it, run its self tests headless, score it
    python tools/iterate.py test-all                            every untested iteration
    python tools/iterate.py rank                                the table, best first

An iteration folder holds: index.html (and any other page), cosmos/ (copied), NOTE.md (the
intent, one paragraph), selftests.txt (one query string per line, for example selftest=2026-07;
a line may end with "  wait=6" for a test that animates in real time), and after testing
verdict.json. Edit index.html in the folder, then test. That is the whole loop.

THE SCORE CANNOT BE ARGUED WITH. One point for each self test whose page title ends PASS, one for
the data summing, one for no private digest anywhere in the folder, one for every script
parsing. A self test that does not finish scores nothing. There is no point for looking good:
eyes are for the ten that survive, not for the hundred.
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
KB = os.path.join(HERE, '..')
ROOT = r'E:\kuiper-iterations'
sys.path.insert(0, HERE)
from check_proof import leaks

CHROME = [p for p in (r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                      r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                      r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe') if os.path.exists(p)]
DEFAULT_TESTS = ['selftest=2026-07', 'selftest=new  wait=6']


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


def folder(n):
    return os.path.join(ROOT, '%04d' % int(n))


def new(note):
    os.makedirs(ROOT, exist_ok=True)
    taken = [int(d) for d in os.listdir(ROOT) if re.match(r'^\d{4}$', d)]
    n = (max(taken) + 1) if taken else 1
    d = folder(n)
    os.makedirs(d)
    for f in os.listdir(KB):
        if f.endswith('.html'):
            shutil.copy(os.path.join(KB, f), d)
    shutil.copytree(os.path.join(KB, 'cosmos'), os.path.join(d, 'cosmos'), ignore=shutil.ignore_patterns('commits', 'belt.tsv'))
    io.open(os.path.join(d, 'NOTE.md'), 'w', encoding='utf-8', newline='\n').write(note.strip() + '\n')
    io.open(os.path.join(d, 'selftests.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(DEFAULT_TESTS) + '\n')
    print('iteration %04d at %s' % (n, d))
    return n


def headless(url, wait):
    """The page sets its own title to 'selftest PASS' or 'selftest FAIL'. A test that animates in
    real time is given real seconds, because virtual time does not move requestAnimationFrame."""
    prof = os.path.join(ROOT, '_profile')
    args = [CHROME[0], '--headless=new', '--disable-gpu-sandbox', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
            '--user-data-dir=' + prof, '--window-size=1280,900']
    args += ['--timeout=%d' % (wait * 1000)] if wait else ['--virtual-time-budget=9000']
    try:
        out = subprocess.run(args + ['--dump-dom', url], capture_output=True, text=True, timeout=60 + wait,
                             encoding='utf-8', errors='replace').stdout
    except subprocess.TimeoutExpired:
        return 'TIMEOUT'
    m = re.search(r'<title>([^<]*)</title>', out or '')
    return m.group(1).strip() if m else 'NO TITLE'


def test(n):
    d = folder(n)
    if not CHROME:
        print('REFUSED: no Chrome or Edge found, so no self test can run')
        return 2
    srv = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=d))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = 'http://127.0.0.1:%d/' % srv.server_address[1]
    v = {'iteration': int(n), 'tested': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'selftests': {}, 'checks': {}}
    lines = [l.strip() for l in io.open(os.path.join(d, 'selftests.txt'), encoding='utf-8') if l.strip()]
    for line in lines:
        m = re.match(r'^(\S+)(?:\s+wait=(\d+))?$', line)
        q, wait = m.group(1), int(m.group(2) or 0)
        page = 'index.html'
        if ':' in q and q.split(':')[0].endswith('.html'):
            page, q = q.split(':', 1)
        t0 = time.time()
        title = headless(base + page + '?' + q, wait)
        v['selftests'][line] = {'title': title, 'pass': title.endswith('PASS'), 'seconds': round(time.time() - t0, 1)}
    srv.shutdown()
    # checks that need no browser
    try:
        rows = [l.split('\t') for l in io.open(os.path.join(d, 'cosmos', 'wafer.tsv'), encoding='utf-8') if l.strip() and l[0] != '#']
        meta = json.load(io.open(os.path.join(d, 'cosmos', 'wafer-meta.json'), encoding='utf-8'))
        v['checks']['data_sums'] = sum(int(r[1]) for r in rows) == meta['issued_keys'] and sum(int(r[4]) for r in rows) == meta['unissued_keys']
    except Exception as e:
        v['checks']['data_sums'] = False
        v['data_error'] = repr(e)
    hits = 0
    parses = True
    for root, _, files in os.walk(d):
        if '_profile' in root:
            continue
        for f in files:
            body = io.open(os.path.join(root, f), encoding='utf-8', errors='replace').read()
            hits += leaks(body)
            if f.endswith('.html'):
                m = re.search(r'<script type="module">([\s\S]*)</script>', body)
                if m:
                    js = os.path.join(d, '.check.mjs')
                    io.open(js, 'w', encoding='utf-8').write(m.group(1))
                    parses = parses and subprocess.run(['node', '--check', js], capture_output=True).returncode == 0
                    os.remove(js)
    v['checks']['no_private_digest'] = hits == 0
    v['checks']['scripts_parse'] = parses
    v['score'] = sum(1 for t in v['selftests'].values() if t['pass']) + sum(1 for c in v['checks'].values() if c)
    v['out_of'] = len(v['selftests']) + len(v['checks'])
    json.dump(v, io.open(os.path.join(d, 'verdict.json'), 'w', encoding='utf-8', newline='\n'), indent=1)
    print('%04d  %d of %d   %s' % (int(n), v['score'], v['out_of'],
                                   '  '.join('%s:%s' % (k.split()[0], 'PASS' if t['pass'] else t['title'][:18]) for k, t in v['selftests'].items())))
    return 0


def rank():
    table = []
    for dname in sorted(os.listdir(ROOT)) if os.path.isdir(ROOT) else []:
        p = os.path.join(ROOT, dname, 'verdict.json')
        if os.path.exists(p):
            v = json.load(io.open(p, encoding='utf-8'))
            note = io.open(os.path.join(ROOT, dname, 'NOTE.md'), encoding='utf-8').read().strip().split('\n')[0][:70]
            table.append((v['score'] / max(1, v['out_of']), v['score'], v['out_of'], dname, note))
    for i, (_, s, o, dname, note) in enumerate(sorted(table, key=lambda t: (-t[0], -t[1], t[3]))):
        print('%s %s  %d/%d  %s' % ('*' if i < 10 else ' ', dname, s, o, note))
    print('%d tested. The starred ten are candidates for publishing; a person still looks at them first.' % len(table))


def main():
    a = sys.argv[1:]
    if a[:1] == ['new'] and len(a) == 2:
        return 0 if new(a[1]) else 1
    if a[:1] == ['test'] and len(a) == 2:
        return test(a[1])
    if a == ['test-all']:
        for dname in sorted(os.listdir(ROOT)):
            if re.match(r'^\d{4}$', dname) and not os.path.exists(os.path.join(ROOT, dname, 'verdict.json')):
                test(dname)
        return 0
    if a == ['rank']:
        rank()
        return 0
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
