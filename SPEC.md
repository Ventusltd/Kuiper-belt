# SPEC: `tools/estate.py`, the belt cartridge

The contract for the first buildable piece. It is a cartridge in the sense the wafer already uses:
one small module, its own data, its own proof, loaded on demand. It does not grow for ever, and it
does not know about any other cartridge. Read [README.md](README.md) and [LAWS.md](LAWS.md) first.

## Command

```
python tools/estate.py \
  --depth repo|file|commit \
  --roots <path>[,<path>...] \
  --org <name> \
  --asof <ISO-8601 with offset> \
  --seed <string> \
  --out data/<run-id>/
```

`--asof` defaults to now with the machine's offset, always printed. `--seed` defaults to the run
id. Depth `repo` is the only depth required for version 1; `file` and `commit` must fail with a
clear "not yet built" rather than a partial answer.

## Inputs

Git, and nothing that needs a network at depth `repo`:

- `git log --date=iso-strict` per body, timestamps with offsets, for `C(b)`, L3, L6, L7.
- `git ls-files` with sizes, for `m`, L5.
- Reference extraction, for `refs(b)`, L1, L2, L4. A reference is a resolved link to another body
  in the estate, found in tracked files. A name that merely resembles a body is not a reference.
- Destination probe, for L8. At depth `repo`, the recorded destination is fetched and its status
  recorded. An unfetched destination is `dim`, never assumed open.

No input may be a human summary, a README's prose, or a model's text.

## Outputs

```
data/<run-id>/estate.json      { stations, edges } exactly as the wafer contract requires
data/<run-id>/bodies.json      one record per body: key, name, six elements, class, destination
data/<run-id>/rules.txt        every constant used, printed in full
proof/<run-id>.json            digests, counts, score, and the exact command line
```

`stations[].id` is the body's key: at depth `repo`, the SHA-1 of `origin/HEAD` at `--asof`; at file
depth, the blob SHA. Never a name. Names live in `bodies.json` beside the key, for humans.

`rules.txt` prints, at minimum: `--asof`, `--seed`, the annulus bounds `a_min`/`a_max`, the `e`
clamp, the resonance tolerance and `p, q` ceiling, the openness timeout, the shepherd and the two
normalised terms that chose it, and the git version.

`proof/<run-id>.json` carries the SHA-256 of every file in `data/<run-id>/`, the body count by
class, the dim/all score from L8, and the full command line. A belt that cannot be rebuilt from
this file did not happen.

## Behaviour that is not negotiable

1. **Refuse rather than guess.** Fewer than 3 commits → `e_undefined`, not an invented `e`. No
   resonance within tolerance → *no resonance*, not the nearest ratio. Destination unfetchable →
   `dim`, not `open`.
2. **A check that examines nothing refuses.** If the roots resolve to zero bodies, exit non-zero
   and say so. Do not write an empty belt and report success.
3. **Determinism.** Same commits, same flags, any machine → byte-identical `estate.json`. Sort
   every collection before writing. Never iterate a set without sorting it.
4. **Offsets always.** Every timestamp written carries its offset.
5. **No publishing.** The cartridge writes files. It does not push, deploy, or post.

## Registration with the Spider

When `estate.json` exists, one entry is added to the receiver manifest
(`spider/manifest.json`, schema `receiver-manifest-v1`) in the engine repository, in the same shape
as the sixteen graphs already listed:

```json
{
  "id": "kuiper-belt",
  "title": "Kuiper belt: the estate as orbiting bodies",
  "path": "./spider/data/kuiper-belt.json",
  "edges_path": null,
  "source_spider": "Kuiper-belt/tools/estate.py --depth repo",
  "description": "Every repository as a body: distance from the shepherd, cadence as eccentricity, resonance with the hourly tick, and whether it can be opened."
}
```

That entry is a proposal. Adding it to the engine repository is a separate, reviewed change.

## Acceptance: how we know version 1 works

A run at depth `repo` is accepted when all of the following hold, each checkable by a third party:

1. `proof/<run-id>.json` exists and its digests match the files in `data/<run-id>/`.
2. Re-running with the same flags on a second machine yields byte-identical `estate.json`.
3. Every `stations[].id` is a key, and every `edges[]` endpoint resolves to a station.
4. The shepherd is printed with both normalised terms for the top three candidates.
5. At least one body is classified in each of: resonant, classical, scattered, detached, or the
   run states plainly which classes are empty and why.
6. The L8 score is printed, and every `open` body's destination returned a status at run time.
7. `rules.txt` contains every constant the run used.

Nothing above requires the drawing to look good. The drawing comes after the numbers are true.

## Explicitly out of scope for version 1

Depth `file` and depth `commit`; the time slider; 3D; any writing to the engine repository; any
network call beyond the openness probe; any use of a language model anywhere in the pipeline. The
belt is computed by arithmetic over git. Models may comment on it afterwards, and their comments
are candidates.
