#!/usr/bin/env python3
"""tools/estate.py - draw the estate as a belt, at blob depth.

    python tools/estate.py --roots <dir> --out data/<run-id>/ [--depth blob|repo]

A body is a distinct blob SHA, not a path. Git issued every one of those keys already, derived
from content, permanent, never repeating, so no key issuance is required and the whole estate is
covered. Identical content in many places is ONE body whose mass carries its membership count:
copies are brightness, not clutter.

Positions are computed, never stored. Every constant used is printed to rules.txt. The same commits
and the same flags produce a byte identical estate-network.json on any machine.

Emits the shape the existing wafer already fetches: {stations, edges}, x and y in the unit square.
"""
import argparse, hashlib, json, math, os, statistics, subprocess, sys
from datetime import datetime, timezone

# ---- constants, all printed with every run ----
A_MIN, A_MAX = 0.16, 0.92        # the drawable annulus, in unit square radii
GOLDEN = 2.399963229728653       # the angle the estate's own law already uses
E_CLAMP = 0.95                   # L3
RES_MAX_PQ, RES_TOL = 8, 0.05    # L6
COLD_DAYS, HOT_DAYS, DETACHED_DAYS = 14, 7, 60
SCATTER_RATIO = 4.0

def git(cwd, args):
    try:
        return subprocess.run(['git'] + args, cwd=cwd, capture_output=True, text=True,
                              encoding='utf-8', errors='replace').stdout.strip()
    except Exception:
        return ''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--roots', default='.')
    ap.add_argument('--out', default=None)
    ap.add_argument('--depth', default='blob', choices=['blob', 'repo', 'file', 'commit'])
    ap.add_argument('--seed', default=None)
    ap.add_argument('--asof', default=None)
    args = ap.parse_args()

    if args.depth in ('file', 'commit'):
        print(f'REFUSED: depth {args.depth} is not yet built. A partial answer is worse than none.')
        return 2

    asof = args.asof or datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
    now = datetime.now(timezone.utc)
    roots = [r for r in args.roots.split(',') if r]
    run_id = now.strftime('%Y%m%dT%H%M%SZ')
    out = args.out or os.path.join('data', run_id)
    seed = args.seed or run_id

    # ---- gather ----
    repos = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            d = os.path.join(root, name)
            if os.path.isdir(os.path.join(d, '.git')):
                repos.append((name, d))
    if not repos:
        print('FAIL: zero repositories. A check that examines nothing refuses.')
        return 1

    blobs = {}      # sha -> {size, copies, repos:set, name}
    repo_info = {}
    for name, d in repos:
        tree = git(d, ['ls-tree', '-r', '-l', 'HEAD'])
        n_paths = 0
        for line in tree.splitlines():
            parts = line.split(None, 4)
            if len(parts) < 5 or parts[1] != 'blob':
                continue
            sha, size, path = parts[2], parts[3], parts[4]
            try:
                size = int(size)
            except ValueError:
                size = 0
            n_paths += 1
            b = blobs.setdefault(sha, {'size': size, 'copies': 0, 'repos': set(), 'name': path})
            b['copies'] += 1
            b['repos'].add(name)
        # cadence, for the repo's class, which its blobs inherit
        log = git(d, ['log', '--date=unix', '--format=%cd', '-n', '400'])
        stamps = sorted(int(x) for x in log.split() if x.isdigit())
        gaps = [b - a for a, b in zip(stamps, stamps[1:])] if len(stamps) > 2 else []
        med = statistics.median(gaps) if gaps else 0
        ecc = min(E_CLAMP, statistics.pstdev(gaps) / med) if med else None
        last = stamps[-1] if stamps else 0
        age_days = (now.timestamp() - last) / 86400 if last else 9e9
        repo_info[name] = {'paths': n_paths, 'commits': len(stamps), 'median_gap': med,
                           'e': ecc, 'age_days': age_days,
                           'max_gap_ratio': (max(gaps) / med) if gaps and med else 0}

    if not blobs:
        print('FAIL: zero bodies. A check that examines nothing refuses.')
        return 1

    # ---- the shepherd is computed, never declared (L1) ----
    max_c = max(r['commits'] for r in repo_info.values()) or 1
    max_p = max(r['paths'] for r in repo_info.values()) or 1
    scores = sorted(((r['commits'] / max_c + r['paths'] / max_p, n) for n, r in repo_info.items()),
                    reverse=True)
    shepherd = scores[0][1]
    shep = repo_info[shepherd]

    def classify(name):
        r = repo_info[name]
        if name == shepherd:
            return 'shepherd'
        if r['age_days'] > DETACHED_DAYS:
            return 'detached'
        if r['max_gap_ratio'] > SCATTER_RATIO:
            return 'scattered'
        if shep['median_gap'] and r['median_gap']:
            ratio = r['median_gap'] / shep['median_gap']
            for q in range(1, RES_MAX_PQ + 1):
                for p in range(1, RES_MAX_PQ + 1):
                    if abs(ratio - p / q) / (p / q) <= RES_TOL:
                        return 'resonant'
        if r['age_days'] <= HOT_DAYS:
            return 'classical-hot'
        if r['age_days'] >= COLD_DAYS:
            return 'classical-cold'
        return 'classical-hot'

    # ---- place, deterministically, from each body's own key ----
    stations = []
    bodies = []
    n_bodies = len(blobs)
    for i, sha in enumerate(sorted(blobs)):
        b = blobs[sha]
        home = sorted(b['repos'])[0]
        cls = classify(home)
        # The estate's own placement law, unchanged: r from the body's ordinal among sorted
        # keys, theta by the golden angle. Position encodes identity, neighbours are related,
        # and density is uniform. Class is a property of a body, never a position: moving a
        # body because of its class would be colouring without a function.
        k = i
        r = A_MIN + (A_MAX - A_MIN) * math.sqrt((k + 0.5) / n_bodies)
        theta = (k * GOLDEN) % (2 * math.pi)
        x = round(0.5 + r * math.cos(theta) * 0.5, 6)
        y = round(0.5 + r * math.sin(theta) * 0.5, 6)
        # The renderer's contract, taken from tools/networks.py in the drawing engine and not
        # inferred: stations are [x, y, name], edges are [i, j] index pairs. The name is the key.
        stations.append([x, y, sha])
        bodies.append({'k': i, 'id': sha, 'x': x, 'y': y, 'm': b['size'],
                       'copies': b['copies'], 'class': cls, 'home': home, 'open': False})

    # A belt needs no edges. Bodies orbit independently, and an invented edge would be a claim
    # without a key. Stated rather than implied.
    edges = []

    os.makedirs(out, exist_ok=True)
    law = ('one body per distinct blob SHA; r = a_min + (a_max - a_min) * sqrt((k + 0.5) / n) '
           'with k the body ordinal among sorted keys; theta = k * ' + str(GOLDEN) + '; '
           'class is a property and never a position; no edges, because an unmeasured edge '
           'would be a claim without a key')
    net = {'name': 'estate', 'source': 'the tracked files of every repository under --roots, by blob SHA',
           'attribution': 'content identifiers issued by git; no third party data',
           'law': law, 'stations': stations, 'edges': edges}
    net_json = json.dumps(net, sort_keys=True, separators=(',', ':'))
    with open(os.path.join(out, 'estate-network.json'), 'w', newline='\n') as f:
        f.write(net_json)

    with open(os.path.join(out, 'estate-bodies.json'), 'w', newline='\n') as f:
        json.dump({'schema': 'estate-bodies-v1', 'run': run_id, 'bodies': bodies},
                  f, separators=(',', ':'), sort_keys=True)
    by_class = {}
    for s in bodies:
        by_class[s['class']] = by_class.get(s['class'], 0) + 1
    total_paths = sum(r['paths'] for r in repo_info.values())

    rules = [
        f'asof {asof}', f'seed {seed}', f'depth {args.depth}',
        f'roots {args.roots}', f'a_min {A_MIN}', f'a_max {A_MAX}',
        f'golden_angle {GOLDEN}', f'e_clamp {E_CLAMP}',
        f'resonance_tolerance {RES_TOL}', f'resonance_max_pq {RES_MAX_PQ}',
        f'cold_days {COLD_DAYS}', f'hot_days {HOT_DAYS}', f'detached_days {DETACHED_DAYS}',
        f'scatter_ratio {SCATTER_RATIO}',
        f'shepherd {shepherd}',
        'shepherd_top_three ' + '; '.join(f'{n} {s:.4f}' for s, n in scores[:3]),
        f'git {git(repos[0][1], ["--version"])}',
        'open_probe none, every body recorded dim',
    ]
    with open(os.path.join(out, 'rules.txt'), 'w', newline='\n') as f:
        f.write('\n'.join(rules) + '\n')

    bodies_path = os.path.join(out, 'bodies.json')
    with open(bodies_path, 'w', newline='\n') as f:
        json.dump({'run': run_id, 'shepherd': shepherd, 'repositories': len(repos),
                   'tracked_paths': total_paths, 'bodies': len(stations),
                   'by_class': by_class}, f, indent=1, sort_keys=True)

    os.makedirs('proof', exist_ok=True)
    digest = hashlib.sha256(net_json.encode()).hexdigest()
    proof = {'run': run_id, 'asof': asof, 'digest': digest,
             'bodies': len(stations), 'tracked_paths': total_paths,
             'repositories': len(repos), 'shepherd': shepherd, 'by_class': by_class,
             'dim': len(stations), 'score_dim_over_all': 1.0,
             'command': 'python tools/estate.py ' + ' '.join(sys.argv[1:])}
    with open(os.path.join('proof', f'{run_id}-estate.json'), 'w', newline='\n') as f:
        json.dump(proof, f, indent=1, sort_keys=True)

    print(f'repositories {len(repos)}  tracked paths {total_paths}  bodies {len(stations)}')
    print(f'shepherd {shepherd}  ({scores[0][0]:.4f})')
    for k in sorted(by_class):
        print(f'  {k:<16} {by_class[k]}')
    print(f'estate-network.json digest {digest}')
    print(f'dim {len(stations)} of {len(stations)}: no destination probe ran, so nothing is open')
    return 0

if __name__ == '__main__':
    sys.exit(main())
