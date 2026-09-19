# PROPOSAL 002: a 132 kV cable being laid is a public, early signal that grid capacity is coming

Status: PROPOSAL. Raised by Vikram, 19 September 2026. The purpose is plain: more people should be
able to connect to the grid, and the first thing they need to know is where capacity is about to appear.

## The arithmetic

A three phase circuit carries

    power = 1.732 x voltage x current        (1.732 is the square root of 3)

| current in each phase | at 132 kV |
|---|---|
| 1000 A | 229 MVA |
| 1100 A | 251 MVA |
| 1200 A | 274 MVA |
| 1312 A | 300 MVA |

A single circuit of single core 76/132 (145) kV XLPE cable with a 1600 mm² aluminium conductor, a
size widely used by distribution network operators, is therefore worth roughly **a quarter of a
gigawatt**. What it carries continuously when buried depends on how it is laid: depth, spacing,
flat or trefoil, ducts or direct, how the screens are bonded, and the soil. CANDIDATE: 230 to
280 MVA continuous, 300 MVA only in favourable conditions. The real figure for a real route is a
calculation to IEC 60287, which this engine should be able to do and show; until then the range
above is an estimate and says so.

One more piece of physics that matters on long routes: a cable is also a capacitor, and charging it
takes current whether or not any load is connected. That current grows with every kilometre and
comes off the top of the rating. A long cable delivers less than a short one of the same size.

## The signal

Nobody lays a quarter of a gigawatt of cable by accident. Before it goes in the ground it appears
in PUBLIC records: planning applications, streetworks permits, consent and wayleave notices, and a
network operator's own published development plans. Those records carry a route and usually a
voltage, and often a cable size. They appear months or years before a capacity map changes.

So: **route + voltage + cable size -> capacity arriving, where, and roughly when.**

## What to build

1. A GridAtlas layer of public notices of new high voltage cable routes, each with its source and date.
2. For each, the engine draws the cable section from arithmetic and states the capacity range, marked CANDIDATE
   until an IEC 60287 calculation replaces it.
3. PipelineNews carries the same signal as news: capacity is coming here.
4. A line on the Kuiper for every one of them, so the record of what was known, and when, is permanent.

## What this must never use

Only public records, published standards and physics. No maker's tender reply, no guaranteed
particulars supplied in confidence, no prices, no trademarks, nobody's proprietary data. If a
figure cannot be traced to a public source or derived in the open, it is left out or marked CANDIDATE.

Provided as is, without warranty of any kind; a chart, not a design.
