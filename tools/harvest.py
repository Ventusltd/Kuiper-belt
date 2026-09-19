#!/usr/bin/env python3
r"""tools/harvest.py - the engine that runs with nobody paying and nobody watching.

    python tools/harvest.py [--limit N]

Run by .github/workflows/engine.yml on GitHub's own machine, on a timer. It needs no local clone,
no graphics card and no assistant. It asks GitHub which repositories of this account are PUBLIC,
takes the newest snapshot of each, counts the files and the lines standing in it now, and writes:

    cosmos/standing.tsv   one row per public repository: name, head, time of head, files, lines
    cosmos/pulse.tsv      one row added per run: time, repositories, files, lines

pulse.tsv is the record of the future arriving: every run adds one row and never rewrites an old
one, so the growth of the estate is measured from the day this was switched on.

SAFEGUARDS. It asks only for public repositories and skips anything marked private anyway. Before
writing, everything it is about to write is passed through the digest guard; one match and it
writes nothing and exits 2. A repository that cannot be cloned is recorded as missed, not guessed.
If more than a fifth are missed the run fails and writes nothing, so a bad night cannot look like
the estate shrinking.
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
OWNER = 'Ventusltd'
sys.path.insert(0, HERE)
from check_proof import leaks


def public_repos():
    out, page = [], 1
    while True:
        req = urllib.request.Request('https://api.github.com/users/%s/repos?type=owner&per_page=100&page=%d' % (OWNER, page),
                                     headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'kuiper-harvest'})
        tok = os.environ.get('GITHUB_TOKEN')
        if tok:
            req.add_header('Authorization', 'Bearer ' + tok)
        rows = json.load(urllib.request.urlopen(req, timeout=60))
        if not rows:
            break
        out += [r for r in rows if not r.get('private') and r.get('visibility', 'public') == 'public' and r.get('size', 0) > 0]
        page += 1
    return sorted(out, key=lambda r: r['name'].lower())


def force_rm(path):
    def on_err(fn, p, _):
        os.chmod(p, 0o700)
        fn(p)
    shutil.rmtree(path, onerror=on_err)


def measure(repo, tmp):
    d = os.path.join(tmp, 'r')
    if os.path.exists(d):
        force_rm(d)
    r = subprocess.run(['git', 'clone', '-q', '--depth', '1', repo['clone_url'], d], capture_output=True, text=True, timeout=900)
    if r.returncode:
        return None
    g = lambda *a: subprocess.run(['git'] + list(a), cwd=d, capture_output=True, text=True).stdout.strip()
    head, when = g('rev-parse', 'HEAD')[:12], int(g('log', '-1', '--format=%ct') or 0)
    files = lines = 0
    for f in subprocess.run(['git', 'ls-files', '-z'], cwd=d, capture_output=True).stdout.split(b'\0'):
        p = os.path.join(d.encode(), f)
        if not f or os.path.islink(p) or not os.path.isfile(p):
            continue
        body = open(p, 'rb').read()
        if b'\0' in body[:8192]:
            continue                                            # not text: it has no lines
        files += 1
        lines += body.count(b'\n') + (1 if body and not body.endswith(b'\n') else 0)
    force_rm(d)
    return head, when, files, lines


def main():
    a = sys.argv[1:]
    limit = int(a[a.index('--limit') + 1]) if '--limit' in a else 0
    repos = public_repos()
    if limit:
        repos = repos[:limit]
    tmp = tempfile.mkdtemp(prefix='harvest-')
    rows, missed = [], []
    for r in repos:
        try:
            m = measure(r, tmp)
        except Exception:
            m = None
        if m:
            rows.append((r['name'],) + m)
        else:
            missed.append(r['name'])
    force_rm(tmp)
    print('%d public repositories, %d measured, %d missed' % (len(repos), len(rows), len(missed)))
    if not rows or len(missed) * 5 > len(repos):
        print('FAIL: too many missed to call this a measurement; nothing written')
        return 1

    now = int(time.time())
    standing = '# repository\thead\thead_unix\tfiles\tlines\n' + ''.join('%s\t%s\t%d\t%d\t%d\n' % r for r in rows)
    standing += ''.join('# missed\t%s\n' % n for n in missed)
    pulse = '%d\t%d\t%d\t%d\t%d\n' % (now, len(rows), len(missed), sum(r[3] for r in rows), sum(r[4] for r in rows))
    if leaks(standing):
        print('REFUSED (L6): a name that is not public is in the result; nothing written')
        return 2
    if limit:
        print(standing + pulse + 'dry run with --limit: nothing written')
        return 0
    io.open(os.path.join(ROOT, 'cosmos', 'standing.tsv'), 'w', encoding='utf-8', newline='\n').write(standing)
    p = os.path.join(ROOT, 'cosmos', 'pulse.tsv')
    if not os.path.exists(p):
        io.open(p, 'w', encoding='utf-8', newline='\n').write('# unix\trepositories\tmissed\tfiles\tlines_standing\n')
    io.open(p, 'a', encoding='utf-8', newline='\n').write(pulse)
    print('lines standing now: %s in %s files' % (format(sum(r[4] for r in rows), ','), format(sum(r[3] for r in rows), ',')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
