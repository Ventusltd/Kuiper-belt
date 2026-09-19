# SPEC-INFINITE — the universe is everything git logged

**The universe is everything git logged. The simulation is the whole of it, at once, in one view.**

That is not a metaphor placed on top of a visualisation. It is the specification, and every rule
below follows from it.

**Distance is time, exactly as in the night sky.** Every star you see is a different past arriving
in the same instant: Proxima four years old, Andromeda two and a half million. Look further out,
look further back. The belt now obeys this: newest at the pupil where the observer stands, oldest at
the rim. Flying outward is flying backward through the estate.

**Everything git logged is in scope.** Not the working tree, not HEAD, not the tracked files. Every
object git has ever recorded: 42,549 blobs, 9,396,220,285 bytes, 124,905,502 lines, across 9,887
commits and 66 repositories. Deleted files are still there. Abandoned branches are still there.
A line written once in 2024 and removed the next day is still a star, and it still shines from the
distance its age puts it at.

**Nothing is created and nothing is destroyed, only recomputed.** Positions come from ordinals,
ordinals from a prefix sum over blob sizes, sizes from git's own headers. The simulation stores no
coordinate and holds no truth of its own. Git is the universe; this is the telescope.

**The honest limit, which the sky shares.** You cannot see every star: dust hides most of the
galaxy, faint things fall below the eye's threshold, and there is a horizon beyond which light has
not arrived. So the view shows an enormous, layered, incomplete truth and says nothing false about
the part it shows. Draw everything. Resolve what the screen can resolve. Never pretend the dim part
is empty.

The next instrument. Every line of every tracked file in every repository, zoomable to the
individual line, without storing a single coordinate. Target order: tens of millions.

Read [README.md](README.md) first. Its laws are binding here, especially: no claim without a key,
positions are computed and never stored, and a check that examines nothing refuses.

## Why this is possible now

**The renderer is proven.** `spiral_vs_stack.py` placed **67,108,864 particles in 21.03 seconds** on
the MSI. That was a benchmark of capacity, generated from a seed, standing for nothing. The task is
to bind that capacity to real lines.

**The keys are free.** A line has a derivable identity: `(blob SHA, line number)`. Content addressed,
permanent, never repeating, issued by git. No issuance ceremony, unlike the 250,174 numbered lines
which required governed integers. So every line in the estate is keyable today.

**The placement law is invertible, and this is the whole trick.** The wafer places by
`r = sqrt(k)`, `theta = k * 2.399963229728653`. Given a screen position you can invert it and recover
`k` directly. No spatial index. No lookup table. No stored coordinates for tens of millions of
points. Zoom to a particle, invert the law, get the ordinal, resolve it to a line.

## The design

**1. THE INDEX IS BYTES, AND GIT ALREADY HAS IT. NOTHING IS COUNTED.**

Git knows every blob's SHA and every blob's size, and both come from the object header without
reading a single byte of content:

    git cat-file --batch-all-objects --batch-check='%(objectname) %(objecttype) %(objectsize)'

That is the whole index. 45,082 blobs, 9,396,220,285 bytes, obtained in seconds. It is live: ask git
again and it is current, with no cache to go stale and no count to re-run.

**Git has no concept of a line.** Newlines live inside the bytes, so a line count means reading every
byte of 8.75 GB. The renderer must therefore never be built on line counts. It is built on bytes.

**The ordinal space is a prefix sum over blob sizes.** Sort the blobs by SHA, take the running total
of their sizes, and every byte in the estate has a global ordinal. Position follows from the ordinal
by the placement law, and the law inverts, so a screen position gives the ordinal back and the
ordinal gives `(blob, byte offset)` by binary search over the prefix sums. **No coordinate is
stored, no count is precomputed, and nothing can drift out of date.**

**Line numbers are resolved lazily, one blob at a time.** When a reader zooms to a particle you have
its blob and its offset. Read that one blob, which is kilobytes, count newlines up to the offset, and
you have the line number and the code. Never read the estate to draw the estate.

**1b. DRAW EVERYTHING, FETCH ONE. The GridAtlas pattern, already proven in this estate.**

The reader never looks at more than one thing at a time. GridAtlas has worked this way since before
the belt existed: the map shows the whole country, and it pulls a satellite scene and a project
record only for the site you flew to. The REPD database is never shipped to the browser.

The belt is the same shape, and it is stronger, because **drawing needs no data at all**:

| | what crosses the wire |
|---|---|
| drawing every particle | **nothing.** Positions are computed from the ordinal by the placement law |
| the index | blob SHAs and sizes from git's object headers, seconds, no content read |
| looking at one particle | **one blob**, kilobytes, fetched at the moment of the click |

So 9.4 GB is rendered without 9.4 GB ever being transferred, and the one file under the cursor is
fetched the way GridAtlas fetches one scene. Everything is drawn; almost nothing is loaded.

This is why the index must be bytes and not content, and why the engine must never wait on a count.

**2. Counting is for the claim, not for the picture.**

"This estate holds N lines" is a public assertion, and under the first law an assertion needs a
measurement with a key behind it. `tools/count_lines.py` exists for exactly that: run it, publish the
number, diff `counts.json` between runs for change detection. It is sharded across twelve runners by
content SHA because it is a real pass over 8.75 GB.

**The engine must never wait for it.** The count answers a question about the estate. The renderer
answers a question about a pixel. They do not depend on each other.

**3. EVERYTHING. THERE IS NO SAMPLING.**

This is an engine for modelling grids, not a picture of one. A sample cannot model anything, so
sampling is not a feature, a fallback or a compromise. It is out of the specification.

Every particle is drawn. If the device cannot hold the whole population in one buffer, the answer is
to render the same complete population in **passes** over regions, not to show less of it. Paging is
honest because the set is unchanged; sampling is a lie because the set is not.

**What full costs, measured rather than assumed.** Two float32 coordinates per point puts 200 million
particles at about 1.6 GB of GPU buffer. Options that keep the population whole, in order of
preference:

- **render in passes** by radial band, accumulating into one framebuffer, so every particle is drawn
  and nothing is discarded
- **narrow the type**: float16 coordinates halve the buffer to roughly 0.8 GB, and at screen scale
  the precision loss is below a pixel
- **generate per pass from the ordinal**, holding no global buffer at all, which is what the
  invertible placement law already makes possible

A device that genuinely cannot render the whole estate must say so and stop, not quietly draw a
fraction. Refusing is honest. Truncating is not.

**4. Resolution on click.**
Invert the law to `k`, prefix-sum to `(blob, line)`, then resolve through the existing key index to
`repo, commit, path, line` and fetch the real line the way the card already does, verifying the
fetched file's line N matches before displaying it. No twin record, no link, and say so.

## What must be measured before any of it

The estate's true line count has never been established. One repository alone holds 17,300 blobs and
5,697,731,454 bytes at a mean of 329 kB, which means stored history is dominated by regenerated data
rather than authored work. So:

- Count **tracked text lines** across all 66 repositories, with binary and data paths reported
  separately, so the denominator is honest.
- Count **authored lines** via `git log --numstat` additions, which is the different and more
  meaningful figure.
- Publish both. Never quote one as the other.

Until that runs, **do not claim 67 million**. It is a benchmark number, not a measurement of this
estate, and repeating it as though it were the line count would be the same error as reporting the
wafer's dust count for the Kuiper belt.

## Acceptance

1. The blob table reproduces byte identically from the same commits on any machine.
2. Ordinal to line and line to ordinal agree in both directions for a random sample of ten thousand.
3. A zoomed view resolves a clicked particle to a line whose fetched text matches the index.
4. The HUD states the drawn count, the total, and the stride, every frame.
5. Memory does not grow with the addressable population, only with what is in view.
6. `release` still returns the wafer to its own law.

## Not in scope for version 1

Colour, 3D, the time axis, and any use of a language model anywhere in the pipeline. The population
is computed by arithmetic over git.
