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
