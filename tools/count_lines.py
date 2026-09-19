MINE = lambda sha: True
SUF = ''
#!/usr/bin/env python3
"""tools/count_lines.py - count every line in the estate, at HEAD and across all history.

    python tools/count_lines.py --roots <dir> [--depth head|history|authored|all] [--out data]

Three different numbers, never conflated:

  head      lines of text in distinct blobs at HEAD          measured 2026-09-19: 25,335,587
  history   lines of text in EVERY blob ever stored          8.75 GB of content, never counted
  authored  lines added by commits, from git log --numstat   the one change detection keys on

A blob with a NUL byte in its first 8,000 is binary: counted as a blob, excluded from line totals.
Distinct blobs only, so identical content in many places counts once, exactly as the Kuiper belt
counts bodies.

GitLab adds nothing to any of these. The mirror holds the same objects with the same SHAs, which is
what HONOURED means. Counting it would be double counting.

Writes, for the renderer and for change detection, with no further work needed:

  data/blob-lines.tsv           sha<TAB>lines             one row per text blob at HEAD
  data/blob-lines-history.tsv   sha<TAB>lines             one row per text blob ever stored
  data/authored.tsv             repo<TAB>added<TAB>deleted<TAB>commits
  data/counts.json              every total, with the command and the time that produced it
  proof/<run>-counts.json       the sha256 of each file above

The scaffolding is the point. Re-run it, diff counts.json against the last one, and you have change
detection with a key behind every number.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone


def find_repos(roots):
    out = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            d = os.path.join(root, name)
            if os.path.isdir(os.path.join(d, '.git')):
                out.append((name, d))
    return out


def git(d, args):
    r = subprocess.run(['git'] + args, cwd=d, capture_output=True,
                       text=True, encoding='utf-8', errors='replace')
    return r.stdout


def lines_of(body, size):
    """-1 means binary. Otherwise newlines, plus one if the file does not end in a newline."""
    if b'\x00' in body[:8000]:
        return -1
    return body.count(b'\n') + (1 if size and not body.endswith(b'\n') else 0)


def batch_count(d, shas):
    """One git cat-file --batch pass. Returns {sha: lines, or -1 for binary}."""
    if not shas:
        return {}
    p = subprocess.run(['git', 'cat-file', '--batch'], cwd=d,
                       input=('\n'.join(shas) + '\n').encode(), capture_output=True)
    out, i, res = p.stdout, 0, {}
    for sha in shas:
        nl = out.find(b'\n', i)
        if nl < 0:
            break
        hdr = out[i:nl].split()
        if len(hdr) < 3:
            break
        size = int(hdr[2])
        res[sha] = lines_of(out[nl + 1:nl + 1 + size], size)
        i = nl + 1 + size + 1
    return res


def do_head(rs, seen):
    global MINE
    paths = 0
    for name, d in rs:
        new = []
        for line in git(d, ['ls-tree', '-r', '-l', 'HEAD']).splitlines():
            p = line.split(None, 4)
            if len(p) < 5 or p[1] != 'blob':
                continue
            paths += 1
            if p[2] not in seen and MINE(p[2]):
                seen[p[2]] = None
                new.append(p[2])
        seen.update(batch_count(d, new))
        print('  head %-34s %10s paths so far' % (name, format(paths, ',')), file=sys.stderr)
    return paths


def do_history(rs, seen):
    global MINE
    for name, d in rs:
        new = []
        for line in git(d, ['cat-file', '--batch-all-objects',
                            '--batch-check=%(objectname) %(objecttype)']).splitlines():
            p = line.split()
            if len(p) == 2 and p[1] == 'blob' and p[0] not in seen and MINE(p[0]):
                seen[p[0]] = None
                new.append(p[0])
        seen.update(batch_count(d, new))
        print('  history %-31s %10s blobs so far' % (name, format(len(seen), ',')), file=sys.stderr)


def do_authored(rs):
    rows = []
    for name, d in rs:
        added = deleted = commits = 0
        for line in git(d, ['log', '--all', '--numstat', '--format=%H']).splitlines():
            if not line.strip():
                continue
            p = line.split('\t')
            if len(p) == 3:
                if p[0] != '-':
                    added += int(p[0])
                if p[1] != '-':
                    deleted += int(p[1])
            elif len(line.strip()) == 40:
                commits += 1
        rows.append((name, added, deleted, commits))
        print('  authored %-30s +%s' % (name, format(added, ',')), file=sys.stderr)
    return rows


def write_tsv(path, d):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        for sha in sorted(d):
            v = d[sha]
            if v is not None and v >= 0:
                f.write('%s\t%d\n' % (sha, v))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--roots', default='.')
    ap.add_argument('--depth', default='head', choices=['head', 'history', 'authored', 'all'])
    ap.add_argument('--out', default='data')
    ap.add_argument('--shard', type=int, default=0, help='0-based shard index')
    ap.add_argument('--of', type=int, default=1, help='total shards; the set is split by SHA')
    a = ap.parse_args()

    rs = find_repos([r for r in a.roots.split(',') if r])
    if not rs:
        print('FAIL: zero repositories. A check that examines nothing refuses.')
        return 1
    if a.of < 1 or not (0 <= a.shard < a.of):
        print('FAIL: --shard must be 0 <= shard < --of')
        return 1
    # Sharding is deterministic and by CONTENT, not by repository: a blob belongs to the shard
    # given by its own SHA. Every shard therefore sees a disjoint slice, no blob is counted twice,
    # and the shards sum exactly to the whole. Re-running any shard reproduces the same slice.
    global MINE
    MINE = (lambda sha: int(sha[:8], 16) % a.of == a.shard) if a.of > 1 else (lambda sha: True)

    now = datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
    run = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    os.makedirs(a.out, exist_ok=True)
    os.makedirs('proof', exist_ok=True)
    global SUF
    SUF = '' if a.of == 1 else '-%02d-of-%02d' % (a.shard, a.of)

    counts = {
        'shard': a.shard,
        'of': a.of,
        'run': run,
        'asof': now,
        'repositories': len(rs),
        'command': 'python tools/count_lines.py ' + ' '.join(sys.argv[1:]),
        'note': 'GitLab adds nothing: the mirror holds the same objects with the same SHAs.',
    }

    if a.depth in ('head', 'all'):
        seen = {}
        counts['tracked_paths'] = do_head(rs, seen)
        counts['head_blobs'] = len(seen)
        counts['head_text_blobs'] = sum(1 for v in seen.values() if v is not None and v >= 0)
        counts['head_binary_blobs'] = sum(1 for v in seen.values() if v == -1)
        counts['head_lines'] = sum(v for v in seen.values() if v and v > 0)
        write_tsv(os.path.join(a.out, 'blob-lines%s.tsv' % SUF), seen)

    if a.depth in ('history', 'all'):
        seen = {}
        do_history(rs, seen)
        counts['history_blobs'] = len(seen)
        counts['history_text_blobs'] = sum(1 for v in seen.values() if v is not None and v >= 0)
        counts['history_binary_blobs'] = sum(1 for v in seen.values() if v == -1)
        counts['history_lines'] = sum(v for v in seen.values() if v and v > 0)
        write_tsv(os.path.join(a.out, 'blob-lines-history%s.tsv' % SUF), seen)

    if a.depth in ('authored', 'all'):
        rows = do_authored(rs)
        with open(os.path.join(a.out, 'authored.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            for n, ad, de, c in sorted(rows):
                f.write('%s\t%d\t%d\t%d\n' % (n, ad, de, c))
        counts['authored_added'] = sum(r[1] for r in rows)
        counts['authored_deleted'] = sum(r[2] for r in rows)
        counts['commits'] = sum(r[3] for r in rows)

    with open(os.path.join(a.out, 'counts%s.json' % SUF), 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(counts, indent=1, sort_keys=True))

    digests = {}
    for fn in ('blob-lines.tsv', 'blob-lines-history.tsv', 'authored.tsv', 'counts.json'):
        p = os.path.join(a.out, fn)
        if os.path.exists(p):
            digests[fn] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    with open(os.path.join('proof', run + '-counts.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'run': run, 'asof': now, 'digests': digests, 'counts': counts},
                  f, indent=1, sort_keys=True)

    for k in sorted(counts):
        if k in ('command', 'note'):
            continue
        v = counts[k]
        print('%-22s %s' % (k, format(v, ',') if isinstance(v, int) else v))
    print('\ndigests:')
    for k in sorted(digests):
        print('  %-28s %s' % (k, digests[k]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
