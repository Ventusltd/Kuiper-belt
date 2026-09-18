# NEXT — for whoever picks this up, including a fresh session

State at 2026-09-19T00:35+01:00. Read [README.md](README.md) first, then this.

## Where it stands

`tools/estate.py` works at blob depth and has been run. Output committed:

- `estate-network.json` at the repository root, 3,112,373 bytes,
  digest `bd049860f0aba89659cfbcbbf9681fdc83e52e001a59c6005200708cfc8868a8`
- 66 repositories, 41,623 tracked paths, **19,222 bodies**, one per distinct blob SHA
- shepherd computed, not declared: `globalgrid2050`, scoring 2.0000
- placement is the estate's own law: `r` from the body's ordinal among sorted keys,
  `theta = k * 2.399963229728653`. Class is a property, never a position.
- `data/<run>/rules.txt` carries every constant used
- `proof/<run>-estate.json` carries the digest and the counts

Regenerate at any time with:

```
python tools/estate.py --roots <dir containing the clones> --seed kuiper-2026-09-18
```

## The four jobs, in order, each with its proof

### 1. Openness (L8). Highest value, smallest change.

Every body is currently `dim 19,222 of 19,222`, because no destination probe ran. The address is
already derivable from data `estate.py` collects and discards: the home repository, the commit, and
the path. Compose the public URL, fetch it, record the status on the body as `open` and `href`.

**Proof:** the dim count falls to a real number, and that number is the belt's own score.
**Why first:** under L8 a body that cannot be opened has failed. Until this runs, the belt is a
picture rather than an instrument.

### 2. Render on the existing wafer. Do not build a new renderer.

`SPEC.md` says the belt produces nothing new to render, and that rule was broken once already:
`preview-kuiper-belt.html` in this repository is a 2D canvas scatter that violates the colour law,
has no physics, and should be treated as a scratch file, not a destination.

The real contract, verified from live source: `pilot.mjs` does
`fetch(new URL(name + '-network.json'))` and reads `.stations`, `.edges`, `.w`, `.x`, `.y`.
So stage `estate-network.json` beside the other `<name>-network.json` files in a wafer version and
add one `<option value="estate">`.

**Proof:** `draw estate` answers on the wafer, the HUD shows the count, `release` returns the dust.
**Note:** staging is mechanical. Publishing to the live site is Vikram's word, after review.

### 3. Recalibrate the classes. They are wrong and it is recorded.

14,537 of 19,222 bodies fall into `scattered` and only 16 across both classical bands. The cause is
`SCATTER_RATIO = 4.0`, which is far too permissive for a repository holding one long quiet interval
relative to its median. The thresholds were chosen in advance instead of derived from the observed
distribution. That was the error.

**Proof:** no class holds more than roughly a third, and each class names repositories a human
recognises as belonging there.
**Until then:** no meaning may be read into a class colour, and any page drawing them must say so.

### 4. The join that makes zoom real.

The key index maps `key -> repo, commit, path, line`. A body is a blob, and a blob is a file. So for
any body you can list the numbered lines it contains, and from those the families, and from those
the gates.

**Proof:** select a body, get its keys, and `entangle` resolves every one of them. That is the
moment belt view becomes wafer mode, and it needs no new concepts, only the join.

## Also open, from the same session

- Re-run the host pairing with the corrected refspec:
  `node tools/entangle_hosts.mjs --roots <dir> --namespace <ns> --push`, then
  `node tools/twin_register.mjs`. Last measured: 55 matched, 9 divergent, 2 not evaluated, and
  74.75 per cent of keys certified, below the 95 per cent threshold. All 9 divergences were
  staleness created by the old push behaviour, which `8c2950b` fixed.
- The hourly `Ventus-GitLab-Captain` will keep exiting 1 until that re-run happens. That is the
  gate working, not a fault.
- `estate.py` is not yet in the hourly lane. Adding it is what makes the belt track new code
  automatically. Blob keys need no issuance, so this is safe to automate.
- Line keys are different and are **not** automatic. The key index is dated 2026-09-16T21:08:57Z
  and 121,805 numbered lines have no family. Issuing keys is a governed act, not a script run, and
  the ordering rule is Vikram's to set.

## Things not to repeat

- Do not build a second renderer.
- Do not colour without a function, and do not move a body on account of its class.
- Do not push the local working copy to a second host; push the origin reference.
- Do not read a percentage without the date of the index it was measured against.
