# PROPOSAL 001: why the 6 mm² conductor is not drawn as a circle, and how to make it one

Status: PROPOSAL ONLY. `conductor.html` is not changed by this. Raised by Vikram on 19 September
2026, looking at the 6 mm² class 5 section beside a real 6 mm² solar cable from a manufacturer's
catalogue, whose conductor is plainly round.

## What the page does now

The 400 mm² conductor is round because it is built from a law that makes circles: one wire, then
rings of 6, 12, 18, 24 around it. Every ring is a circle, so the outline is a circle.

The 6 mm² class 5 conductor is 84 wires of 0.30 mm, bunched. Bunched wires have no fixed places, so
the page had to invent places, and it uses the sunflower law (`conductor.html`, the line that
pushes to `o.wires` for bunched conductors):

    r = (D/2 - d/2) x sqrt((i + 0.5) / n)        angle = i x 137.5 degrees

This is the same law that places every key on the Kuiper. It is excellent at spreading points
evenly over a disc. It is poor at two things a conductor needs:

1. **The rim is ragged.** Only the very last wire reaches the full radius. The few before it sit a
   little further in, each at a different angle, so the outline has steps in it. On 38 billion keys
   nobody can see that. On 84 wires everybody can.
2. **It knows nothing about touching.** The law places centres; it does not know the wires have a
   diameter. At an assumed fill of 0.75 some neighbours overlap and some leave gaps. Real wires
   cannot overlap.

So the honest answer is: it is not round because we used a law for counting points to draw a thing
made of touching circles. The page already says "this arrangement is an idealisation". This
proposal is to choose a better one.

## Why the real one is round

A bunched conductor is twisted together and then the insulation is extruded round it through a
round die, under pressure. The wires are free to move, and they move until the wall stops them.
The outline is a circle because the wall is a circle; inside it the wires settle wherever they
touch. That is a physical process, and it can be computed.

## Three ways to draw it, cheapest first

**A. Put the outer wires on the rim (one line).** The known correction to the sunflower law: the
outermost wires, about 2 x sqrt(n) of them, which is 18 of the 84, are placed exactly at the full radius and only the
rest follow the square root. The outline becomes a circle at once. Wires can still overlap inside.
Cost: one line. Truth: better outline, same idealisation.

**B. Let the wires settle against a round wall (recommended).** Start from the sunflower places.
Then repeat a few hundred times: any two wires closer than one wire diameter are pushed apart
equally; any wire outside the wall is pushed back in. Stop when nothing overlaps. This is what the
die does. The result is round, nothing overlaps, and the inside is slightly irregular, which is
what a cut end looks like under a lens. It must start from the same places every time so the
drawing is the same on every machine: no random numbers.
The page can then MEASURE the fill it achieved instead of assuming 0.75, which removes one
CANDIDATE from the title block, or shows that 0.75 was too tight for round wires in that circle.

**C. Bunches of bunches.** Larger flexible conductors are made as several bunches laid up
together, for example 7 bunches of 12, which is 84. Whether a 6 mm² class 5 conductor is one bunch
or several is the maker's choice and is not fixed by the standard. CANDIDATE until a maker's
datasheet that may be cited says so. Do not draw this as fact.

## The tests that would show the change is right

Added to `window.__selftest` on the page, and failing closed:

1. the number of wires drawn equals n (84, or 189 for class 6);
2. no two centres are closer than the wire diameter, less a stated tolerance;
3. every wire lies inside the circle of diameter D;
4. at least a stated share of the rim is occupied by a wire within a tenth of a wire diameter of the wall, which is what "round" means
   when it has to be measured;
5. the same input gives the same places on a second run.

## What is still not known, and says so

- The diameter D comes from an assumed fill. The standard gives a maximum wire diameter (0.31 mm,
  class 5) and a maximum resistance; whether its informative annex of maximum conductor diameters
  covers this size should be checked against the private copy and, if so, keyed by table and value only.
- Lay length and lay direction are not drawn at all: a section cannot show them. A side view could.
- The tinned coating is a hatch, not a thickness.

Provided as is, without warranty of any kind; a chart, not a design.

## Addendum: what the cable standard itself says (19 September 2026)

Read in a privately held copy of BS EN 50618:2014, Electric cables for photovoltaic systems. The
standard is copyright and is not reproduced here; clauses and single values are cited so that
anyone with their own copy can check them.

| what | value | where |
|---|---|---|
| the conductor wires are tin coated, with no visible gaps in the coating | required | 5.1.1 |
| the conductor is class 5 to EN 60228 | required | 5.1.2 |
| the sheath gives the finished cable a practically circular shape | required | 5.3.2 |
| ovality: any two overall diameters at one cross-section differ by no more than | 15 % | 7.3.3 |
| 1 x 6 mm², insulation thickness, specified value | 0.7 mm | Table 1 |
| 1 x 6 mm², sheath thickness, specified value | 0.8 mm | Table 1 |
| 1 x 6 mm², mean overall diameter, upper limit (informative) | 7.4 mm | Table 1 |

**So the question is settled by the standard, not by taste.** Round is a requirement, and it has a
number: 15 %. The standard puts that requirement on the finished cable, through the sheath. It is
the extrusion that makes the cable round, which is the physical argument for option B above: let
the wires settle against a round wall.

**This gives the page a whole cable to draw, and a check to fail.** Around the conductor of
diameter D go 0.7 mm of insulation and 0.8 mm of sheath, so

    overall diameter = D + 2 x (0.7 + 0.8) = D + 3.0 mm

With the page's present D of 3.17 mm (84 wires of 0.30 mm at an assumed fill of 0.75) that is
**6.17 mm, inside the 7.4 mm upper limit**. Turned round, the limit allows a conductor of up to
4.4 mm, which a bundle of 84 wires of 0.30 mm reaches only at a fill of 0.39: far looser than any
real bunch. The assumed fill is therefore not contradicted by the standard, and not confirmed
by it either. It stays CANDIDATE until option B measures it.

**Tests to add to the five above:**

6. the drawn overall diameter is no more than the Table 1 upper limit for that size;
7. the ovality of the drawn outline, measured across at least eight diameters, is within 15 %;
8. the insulation and sheath are drawn at their specified thicknesses, and hatched as materials,
   not coloured.

**What this changes elsewhere.** Law L8 in Ventusltd/law must use the metal coated class 5
resistance for a solar cable, because 5.1.1 requires tin: that correction was already pending and
this is its authority. The cable database rows whose source is this standard can be checked
against Table 1 one size at a time, from a private copy, publishing only pass or fail.

## Addendum 2: a maker's published datasheet measures our assumption (19 September 2026)

Source: a cable maker's public datasheet for a 1500 V DC photovoltaic string cable from the maker's own product page. Cited as a published key; their drawings and text are not copied here. Makers reserve the
right to change values: check the current sheet.

| 1 x 6 mm², as published by the maker | value | what it checks |
|---|---|---|
| conductor | tinned fine copper strand, IEC 60228 class 5 | agrees with EN 50618, 5.1.1 and 5.1.2 |
| conductor diameter | 3.00 mm | our page draws 3.17 mm |
| resistance | 3.39 milliohm per metre | exactly the IEC 60228 Table 3 maximum for metal coated class 5 |
| outer diameter | 6.1 mm | under the EN 50618 Table 1 upper limit of 7.4 mm |
| weight | 82 kg per km | a future check on metal plus polymer |
| bending radius | 4 x outer diameter fixed, 5 x occasionally moved | the cable database carries these multiples |

**Check 1, the whole cable.** 3.00 + 2 x (0.7 + 0.8) = 6.0 mm against a published 6.1 mm. The
standard's thicknesses and the maker's diameters agree to a tenth of a millimetre. The chain
conductor, insulation, sheath can be drawn from arithmetic and checked against a catalogue.

**Check 2, the fill, and a thing worth knowing.** If the conductor were 84 wires of 0.30 mm inside
a 3.00 mm circle, the fill would be 84 x 0.30² / 3.00² = **0.84**. Round wires in a round wall
cannot reach that: even perfect honeycomb packing with no wall is 0.907, and a wall costs several
points. So at least one of our two inputs, 84 or 0.30, is not what is inside this cable, and the
standard allows that: **IEC 60228 does not define a conductor by its wires or its area. It defines
it by its resistance** and, for class 5, a maximum wire diameter. "6 mm²" is a name. A conductor
that just meets 3.39 ohm per km needs only about 5.1 mm² of copper before lay and tin are allowed
for. Metal of about 5.3 mm² in a 3.00 mm circle is a fill of **0.75**, which is the figure the page
assumed. The assumption was right; the wire count and diameter we fed it were nominal, not real.

**What this changes in the proposal.**

- The page should take the conductor diameter as an INPUT when a published one exists (3.00 mm
  here) and DERIVE the wire diameter that fits n wires at the settled fill, flagged as derived,
  instead of taking nominal wires and deriving a diameter nobody published.
- Test 9: where a published conductor diameter is keyed, the drawn conductor matches it within 0.05 mm.
- Test 10: the drawn metal area times the resistivity of copper gives a resistance no greater than the
  Table 3 maximum. This is the test that matters electrically, and it ties the drawing to law L7.
- The maker's own illustration of the section is a spiral of dots with the outer ring seated on a
  round wall. That is option A. Option B remains the recommendation because it can be measured,
  but A is evidently good enough for a maker's catalogue, and is one line.

## Addendum 3: why the shape of a conductor has to be known precisely

Reference: "DC Cable: The Overlooked Risk Of The $2 Trillion Solar Sector", Forbes Technology
Council, 24 July 2025,
https://www.forbes.com/councils/forbestechcouncil/2025/07/24/dc-cable-the-overlooked-risk-of-the-2-trillion-solar-sector/
The article is not reproduced here. Its argument, in our words: direct current does not cross zero,
so a fault does not put itself out; the usual protection often cannot see a small arc; there are
tens of millions of kilometres of this cable, most of it 6 mm²; and the weak point is where cable
meets connector, because a connector has to match the geometry of the cable and the crimp cannot
be inspected by eye afterwards.

That last point is a question about shape, and shape is arithmetic. The same "6 mm²" is several
different objects:

| conductor | how it is made | fill (metal over circle) | diameter for 6 mm² | status |
|---|---|---|---|---|
| solid, class 1 | one wire | 1.00 | 2.76 mm | exact: sqrt(4 x 6 / pi) |
| concentric round, class 2, 7 wires | 1 + 6 | 7/9 = 0.778 | 3.13 mm | derived, exact, for nominal metal |
| concentric round, many layers | 1 + 6 + 12 + 18 ... | tends to 3/4 exactly | - | derived: see below |
| compacted round | the above, squeezed through a die | about 0.90 | about 8 % smaller than uncompacted | CANDIDATE fill |
| bunched, class 5 | fine wires twisted with no fixed places | about 0.75 | 3.00 mm published by one maker | published, and derived from it |
| bunched, class 6 | finer wires, more of them | not yet keyed | not yet keyed | CANDIDATE |
| sector shaped | for multicore power cable, not solar string cable | - | - | not drawn |

**The exact part.** A concentric conductor with k layers has n = 3k² + 3k + 1 wires across a width
of 2k + 1 wires, so its fill is (3k² + 3k + 1) / (2k + 1)². That is 7/9, 19/25, 37/49, 61/81, and
it falls towards **3/4 and never below it**. Every round stranded conductor that has not been
compacted is about one quarter empty space. That quarter is what a crimp has to close.

**Why a connector cares.**

1. **Diameter.** The barrel is made for a diameter. From solid to stranded the same nominal size
   runs from 2.76 mm to over 3.1 mm, and between makers of the same class it differs again,
   because the standard fixes resistance, not diameter (Addendum 2).
2. **Empty space.** A crimp works by squeezing the space out until metal bears on metal. At a fill
   of 0.75 a quarter of the barrel is air before the tool closes. A tool set for one conductor and
   used on another of a different fill closes too little or too much, and neither can be seen afterwards.
3. **Surface.** The surface of the wires, per unit of metal, goes as one over the wire diameter.
   84 wires of 0.30 mm and 189 wires of 0.20 mm carry the same metal, but the finer one has 1.5
   times the surface: 1.5 times the tin, 1.5 times the area that can oxidise if the tin is
   breached, and more, smaller contacts inside a crimp.
4. **Roundness.** A cable gland and a connector seal grip the sheath. The standard allows the
   overall diameter to vary by up to 15 % across one section (EN 50618, 7.3.3). A seal has to work
   across that whole range, and a drawing that shows a perfect circle hides it.

**What the engine should therefore be able to draw, and measure, for any conductor:** its
diameter, its fill, its empty space, its wire surface per unit of metal, and its roundness, each
marked exact, standard, published, derived or CANDIDATE. None of that is a connector design or
an installation instruction. It is the geometry a person needs in front of them before they choose one.

Provided as is, without warranty of any kind; a chart, not a design.

See also https://github.com/Ventusltd/pv-arc-protection-circuit, the public repository that holds the engineering work on this subject; its commit history is a dated record.

## Addendum 4: a nominal size is a resistance, checked across three sizes (19 September 2026)

Vikram's point, from 22 years of selling this cable: makers work to the resistance the standard
sets, not to a weight or an area, so a "6 mm²" conductor may hold less than 6 mm² of copper. The
same maker's public datasheet () gives three sizes, which is enough to test it.

Copper at 20 °C has a resistivity of 17.241 ohm mm² per km (the international annealed copper
standard, 100 % IACS). The least copper that meets a resistance R is therefore 17.241 / R, before
any allowance for the wires being longer than the cable because they are twisted.

| size | published R | least copper | share of nominal | published conductor Ø | circle | fill at least copper | fill if nominal |
|---|---|---|---|---|---|---|---|
| 4 mm² | 5.09 ohm/km | 3.39 mm² | 85 % | 2.45 mm | 4.71 mm² | 0.72 | 0.85 |
| 6 mm² | 3.39 ohm/km | 5.09 mm² | 85 % | 3.00 mm | 7.07 mm² | 0.72 | 0.85 |
| 10 mm² | 1.95 ohm/km | 8.84 mm² | 88 % | 3.90 mm | 11.95 mm² | 0.74 | 0.84 |

**What the geometry says.** Round wires bunched in a round wall settle at a fill of about 0.75; this
page measured that. A fill of 0.84 or 0.85 would need almost perfect honeycomb packing right up to
the wall, which bunched wires do not do. So the published diameters are consistent with a metal
area near the least the resistance allows, a few per cent above it for twist and tin, and are not
consistent with the full nominal area. All three sizes say the same thing. The observation stands.

**What does most of the work, and what does a little.** The standard does most of it: IEC 60228
sets a maximum resistance for each nominal size and says nothing about area or weight, and those
maxima can be met with roughly 85 to 90 % of the nominal area in good copper. Purity does a little:
the best copper is about 1 to 2 % more conductive than the 100 % IACS reference, which saves 1 to
2 % of metal, not 15 %. Tin works the other way: a tinned wire has slightly less copper for its
diameter, which is why the standard allows tinned class 5 a higher resistance (3.39 against 3.30).

**What the published weight cannot settle.** Taking the published weight and subtracting copper
leaves the polymer. With least copper the polymer comes out at about 1.6 g/cm³ for all three sizes;
with full nominal copper, about 1.25 g/cm³ for all three. Both are steady across the sizes and both
are believable densities for a flame retardant halogen free compound, so weight alone does not
decide it. A published compound density would. CANDIDATE until then. The geometry above is the
stronger evidence.

**What this changes in the engine.** A conductor is entered by its nominal size and its class. The
engine looks up the maximum resistance, derives the least metal, and draws THAT metal inside the
published or derived diameter. The title block shows three numbers side by side, never one:
nominal area (a name), metal area (derived from resistance), and fill (measured from the drawing).
