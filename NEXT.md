# NEXT — the handover, for a fresh session or a swarm

State at 2026-09-19T02:30+01:00. Read [README.md](README.md) first — its first 3,000 characters are
the law. Then this. Everything below was measured, not remembered.

## Done and live

`globalgrid2050.com/testcode/wafer-development-environment/202609190230-kuiper-belt/`
Homepage → The Translator of Systems → **Kuiper**.

- **19,257 bodies**, one per distinct blob SHA, from **66 repositories** and **41,658 tracked paths**
  (41,647 appeared in an earlier note and matches no run — the file says 41,658).
- Drawn with the wafer's own **250,174 numbered lines**, 245,170 placed.
- Radius is age in the estate, angle is the golden angle, class is a property and never a position,
  no edges because an unmeasured edge would be a claim without a key.
- Generator: `tools/estate.py`. Reproducible byte for byte from a printed seed.

## Committed locally, NOT pushed — branch `stage/kuiper-belt` in `_wt-estate`

Push with: `cd _wt-estate ; git push origin HEAD:main`

- **The pulse.** `pulse` / `inject` / `pulse <blob SHA>` / `pulse <x,y>` / `pulse stop`. The engine has
  no per-point colour hook, so light is made by dust share: `s = 1 + 14·f·g·copies`, front crosses in
  9 s, total dust conserved every frame. Distance is **geometric, not electrical**, stated on the card
  so it is never mistaken for `draw fault`, which is a real pandapower IEC 60909 study.
  Proof: in the front band a duplicated body averages **453.2 dots against 43.5** for a unique one.
- **The readable card.** Root cause was two cards in one region: `#panel` at z-index 4 under the
  narration log `#plog` at 19, transparent, same pixels. Now 21 > 20 > 19 with separate lanes.
  Real context ±10 lines, fetched from `raw.githubusercontent.com` at the recorded commit, shown
  **only if that file's line N matches the LINES.md row for the key**. Two keyed sources must agree.
  No neighbour is ever composed. Link is `github.com/<repo>/blob/<commit>/<path>#L<line>`, or no link.
- **The menu**, borrowed from `gridatlas/atlas/modules/202609031958-menu-bar.js`. Five titles, all
  panels hidden at rest, all 17 old presets present plus 14 more. At rest 12.8 per cent of the frame
  is not canvas.
- **Overnight Coding Runs** — a new homepage nest for the hourly iterations.

## Open, in priority order

1. **Re-run the host pairing** with the corrected refspec (`8c2950b`):
   `node tools/entangle_hosts.mjs --roots <dir> --namespace <ns> --push` then `node tools/twin_register.mjs`.
   Last measured 55 matched, 9 divergent, 74.75 per cent of keys certified, below the 95 per cent
   threshold. All 9 were staleness the old push behaviour created. The GitLab captain exits 1 every
   hour until this is done — that is the gate working, not a fault.
2. **Recalibrate the classes.** 14,524 of 19,257 in `scattered`. `SCATTER_RATIO = 4.0` is too
   permissive. Derive thresholds from the observed distribution, not in advance. Until then no
   meaning may be read from a class colour.
3. **The V9.6.1 frozen file**, red since 2026-09-18T03:03Z, not re-run.
   `uk_renewables_pipeline/v9.6.1/tests/check_v9_5_1.mjs` is `e82fd469…`; the gate expects `bc9aff1e…`.
4. **Openness (L8).** Every body is `dim 19,257 of 19,257` because no destination probe ran. The
   address is derivable from repo, commit and path — the card now proves those exist. Fetch it,
   record the status, and the dim count becomes the belt's real score.
5. **`flyTo` zoom floor.** `Math.max(view.zoom, 9)` in `app.mjs` fires whenever a line is selected and
   the camera stays there. One line changes it; it alters the beam's behaviour, so it is a decision.
6. **Count the estate honestly.** Sum `git log --numstat` additions across all 66 repositories, with
   data paths reported separately, so every coverage claim finally has a denominator. One repository
   alone holds 17,300 blobs and 5.7 GB at a mean of 329 kB — history is dominated by republished data,
   not authorship.
7. **`repositories: 66` vs 64** distinct `home` values among the bodies. Both are recorded. Reconcile.

## Fragile — one machine only, fix these first if anything

- `cvaa` detached at `6df14ed`, 48 uncommitted lines including 3 in `vaccines.lock`.
- `galaxies-wafers-layers-wt`, branch `layers/learned-and-proofs` at `37c939f`, nowhere else.
- `globalgrid2050` local main, one unpushed commit `4f3ff4f4`, modified README, three `r*.json`.

## Fixed tonight, so nobody re-finds it

`E:/particles-runs/verify-iterations.mjs` did one `page.goto` and called a Pages deploy lag a
failure, every hour. It now retries for up to 12 minutes, matching what the Wafer Development
Environment workflow already does.

## Things not to repeat

- Do not build a second renderer. The belt is a dataset; the engine already exists.
- Read the **producer** for a contract, never infer it from the consumer.
- Open the page before describing it. Every error in this project's worst night came from reasoning
  instead of looking, and each was settled in seconds once someone looked.
- Do not colour without a function, and never move a body on account of its class.
- Push `origin`'s ref to a second host, never the local working copy.
- No percentage without the date of the index it was measured against.
- Publishing is Vikram's word. Agents commit; they do not push.

## Cable cross-sections — the next build, with its sources

`draw cable` is live on the kuiper version: a single core 800 mm2 aluminium 19/33 kV section,
3,086 nodes, overall 63.0 mm, from stated inputs carried inside the file. It has one known defect.

**DEFECT: the conductor is drawn as five smooth concentric rings. It should be individual strands.**
A compacted stranded aluminium conductor is roughly 61 wires in five layers with alternating lay,
squashed from round into keystones. Under a saw cut you see a mosaic, not rings. Fix needs four
inputs per size: wires per layer, wire diameter, lay direction, compaction factor.

**What an X-ray would show, as the target for the drawing:** the copper wire screen blazes, because
copper is far denser than anything around it — a ring of brilliant evenly spaced points, the
brightest thing in the image. The aluminium core sits mid-grey. XLPE, both semicons, the bedding and
the MDPE are nearly invisible, so the insulation is defined by the GAP between the bright screen ring
and the grey core. The two things an engineer looks for are eccentricity, the gap measured all the
way round, and voids, a dark crescent at a screen interface where there should be none.

**Sources for the inputs, per voltage:**
- **Conductor classes, strands and cross sections, all sizes** — **IEC 60228**, already in the estate
  (Vikram: in my repo). This is the one that gives wires per class and nominal areas, so it is the
  primary input for the strand fix above, not BS 7870.
- **EN 50618** — further sections and stranding, for the sizes IEC 60228 does not cover in the form needed.
- **11 kV and 33 kV** — BS 7870-4.10, Vikram's licensed copy in Dropbox.
- **132 kV** — TF Kable, Poland. Published manufacturer datasheets.

## DO NOT PUBLISH — an exclusion list is required before the openness job runs

The estate holds material that is paid for or commercially private, named by the owner: engineering
reports he purchased (Braintree among them) and his entire order book since 2012. **None of it may
be published, listed, named or probed.**

The exposure is not file contents. The belt publishes coordinates and blob SHAs, and a SHA reveals
nothing. The exposure is **names**:

1. `bodies.json` carries `home`, the repository name, and the card resolves `repo, commit, path`.
   A path such as a client report filename discloses what is held even when nobody can open it.
2. **Job 4, openness (L8), derives a public URL for every body and fetches it.** Run without an
   exclusion list, that tool is pointed straight at private material. Do not run it until the list
   exists.

**Required before openness runs:**

- An explicit exclusion list of repositories and path patterns, held in this repo, that
  `tools/estate.py` honours: excluded bodies are not keyed, not named and never probed.
- The count of excluded bodies is published; the names are not. An exclusion that hides its own
  existence cannot be audited.
- Default deny for anything not positively matched as publishable, because a denylist fails open and
  a path nobody anticipated is exactly how this leaks.

The `stones` repository already excludes commercial and contractual detail by policy, enforced by
`tools/check-policy.mjs`. The belt has no equivalent yet. That gap is this item.

## Cable sections for accessory selection — the commercial use, and its rule

A buyer uses the section to choose accessories: a separable T connector or elbow is matched to the
**over-insulation diameter**, a compression lug to the **conductor diameter and material**, a screen
connection to the **wire count and size**. Those dimensions are the product, not decoration.

**Expose on the card, computed from the inputs already in the file:** conductor diameter,
over conductor screen, over insulation, over insulation screen, screen wire count and size, over
bedding, and overall. The 800 mm2 already carries every one of these as inputs; they are not shown.

**THE RULE, and it is a safety and commercial one.** No dimension may be invented. A diameter
guessed by a model, shown on a page where someone orders a connector against it, is the exact failure
this project exists to prevent. Every size drawn must come from a document the author holds, and the
card must name which one. Where a figure is missing, draw nothing rather than a plausible ring.

**Sizes to add, with their sources:**
- **110 kV** — the author's own document in Dropbox. Not yet read; do not draw until it is.
- **132 kV** — the **UKPN open public tender specification**, which is public and citable, so this one
  may be published complete with the spec named. Also TF Kable, Poland, for manufacturer construction.
- **11 kV and 33 kV** — BS 7870-4.10, licensed copy. Publish the drawing and its own inputs, cite the
  standard, never the tables.
- **Strands, all sizes** — IEC 60228, already in the estate. EN 50618 beside it.

**Then the join:** each drawn layer should offer the app that computes it, so the section becomes the
front door to work that already exists — `cable_selection`, `star-cable-derating-star`,
`cable-trench-or-drill`. Click the conductor, land on the derating maths.

## Taking dimensions from the author's own project documents — permitted, with a strict filter

The author has given permission: technical specifications inside his own project records may be used
to set the inputs of a drawing. He paid for that engineering and it is his.

**Carry across ONLY the engineering:**
conductor size and material, stranding and class, screen construction, wire count and size, layer
thicknesses, overall diameter, voltage designation, and the standard the construction conforms to.

**NEVER carry across, in any file, card, commit message or record:**
client or counterparty names, project names, purchase order or invoice numbers, quantities, prices,
delivery terms, contacts, or anything identifying a commercial relationship. The documents sit inside
an order book covering 2012 onward and that book is private, in full.

**In practice:** open the document, read the construction table, write the numbers into the cable
inputs, and cite the *standard* the construction follows, never the project it came from. If a
dimension can only be attributed by naming a client, leave it out.

This is the same rule the estate already applies elsewhere: the drawing carries its inputs, the
inputs carry their standard, and nothing carries a counterparty.

## 132 kV: aluminium wire screen, not copper

The 132 kV construction the author worked on was drafted by HES Kablo with an **aluminium wire
screen**, not copper. He has already named that supplier publicly in ABOUT.md, so the name may be
used; the pricing and commercial terms may not.

Three consequences for the drawing, none of them cosmetic:

1. **The screen stops being the brightest ring.** Copper is far denser than aluminium, so on the
   X-ray reading of a section a copper screen blazes against a grey aluminium core. With an
   aluminium screen, screen and conductor sit at nearly the same density and the section reads
   almost flat. Whatever encodes material must show that, or the picture lies about what a
   radiograph would reveal.
2. **Wire count and size differ.** Aluminium's conductivity is about 61 per cent of copper's, so an
   equivalent screen cross section needs materially more aluminium. The wire count and diameter must
   come from the document, not from scaling the copper values.
3. **The material belongs in the data.** `cable-network.json` currently names layers only. Each layer
   should carry its material, so a drawing can be read correctly and an accessory can be matched:
   a lug for aluminium is not a lug for copper, and that is a real ordering distinction.

Source: the tender the author prepared, with its pricing spreadsheet and hyperlinks to every
datasheet. **Not found in the Dropbox searched on 19 September** — looked for by folder name, file
extension, keyword across all PDFs and spreadsheets, and by listing QuoteLog directly. It is
elsewhere. One line from the author gives the path, and the drawing follows in minutes.

Do not draw the 132 kV until that document is open. No dimension may be invented.

## The UKPN 132 kV documents — found, and how to finish the drawing

**Archive:** `C:/Users/vikra/Downloads/UKPN HES.zip`, 944,002 bytes, six files:

- `ETS 02-4000 1x1600 132 kV - HDPE.pdf` — the specification, Appendix A Schedule of Technical
  Particulars, single core 132 kV XLPE
- `320241-B0918.681.1.01.pdf` through `320245-B0918.681.1.05.pdf` — five HES drawings

**Already drawn** from page 1, live as `draw cable132`: 76/132(145) kV, 1600 mm2 aluminium Class 2
Milliken compacted, 50.3 mm over conductor, 0.3 mm swellable semiconductive barrier tape, 53.3 mm
over the extruded semiconductive XLPE conductor screen, 17 mm nominal XLPE, **87.3 mm over the
insulation**. Conductor drawn as six Milliken segments with strand layers, not rings.

**Still missing, and on pages 2 to 6:** the core screen, the **aluminium wire screen** (wire count
and diameter), any binder or swellable tape over it, the bedding, and the **HDPE sheath** thickness
and overall diameter. Without those the section stops at the insulation, which is how it currently
ships, on purpose.

**The blocker is a tool, not the document.** The PDF has 24 compressed streams and 370,345 bytes of
decompressed content, but the fonts are subset encoded and simple text extraction returns nothing.
There is no `pdftotext` or `pdftoppm` on this machine. Install poppler, or use a Python PDF library,
and pages 2 to 6 read in seconds. Alternatively the Read tool renders PDF pages once poppler exists.

**Then:** add the outer layers to `cable132-network.json`, and give every layer a material, because
the screen here is aluminium and not copper, so it must not be drawn as the brightest ring.

Every value goes in the file. No table is reproduced. Nothing is invented.

## 132 kV screen: UKPN changed CWS to a larger AWS — check which revision each drawing shows

UK Power Networks changed the screen on this construction from a **copper wire screen (CWS)** to an
**aluminium wire screen (AWS)**, and the AWS is **larger**. That is expected: aluminium carries about
61 per cent of copper's conductivity, so an equivalent screen cross section needs materially more
metal. The change is a revision, not an alternative.

**Consequence for the documents.** The six files in `UKPN HES.zip` were produced around that change,
so **the schedule and the five HES drawings may not agree** on the screen. Before drawing anything
outside the insulation, establish for each file which screen it shows and which revision it belongs
to. Do not merge values across files that disagree.

**Consequence for the drawing.** The screen must carry its material, and an AWS must not be rendered
the way a CWS would be. Copper is far denser than aluminium, so on a radiograph a copper screen
blazes against the conductor while an aluminium screen sits at nearly the same density and the
section reads almost flat. Drawing an AWS as a bright ring would be a picture of a cable that does
not exist.

**Consequence for a buyer.** A lug or a screen connection for aluminium is not the one for copper.
If the section is ever used to select accessories, the screen material is not a detail, it is the
answer.

## Three asked for at the end of the night, 19 September

**1. A preset for the light show.** `pulse` has a button in the preset bar but the picker list should
carry it too, and the belt version should offer `pulse` the way it offers `draw kuiper`. One option
and one entry. Trivial, just not done.

**2. Does the pulse work zoomed in?** Unknown and untested. The pulse recomputes every body's dust
share each frame from geometric distance, which is independent of camera zoom, so it should hold,
but `flyTo` sets a zoom floor of 9 and nobody has watched a pulse while zoomed. **Candidate, not a
fact.** Test it before claiming it.

**3. Gravity separation into TWINS, not to one side.** The owner's correction, and it is the better
idea. The estate already has the vocabulary: a twin is the pair of a key and the real code it names,
and the Quantum Twin Star already draws a principal star and its twin as two instanced populations,
every point reflected through the centre. So `twins` as a command on the belt would split the
population into two mirrored bodies by a **measured** predicate and let gravity separate them.

The honest candidates for the predicate, all already measured per body:
- `copies > 1` against `copies == 1` — duplicated against unique, 2,152 against 17,105
- `open` against `dim` — reachable against unreachable, once the openness probe runs
- host agreement — confirmed pair against broken pair, from the twin register

**The rule that governs it:** the split must be by something measured, never by a guess, and the two
populations must be labelled so a reader knows which is which. A separation that cannot say what
divided it is decoration. And `release` must bring them back together.

This is the most interesting of the three, because it makes the belt answer a question rather than
just show a shape: *how much of this estate is duplicated, and where does it sit.*
