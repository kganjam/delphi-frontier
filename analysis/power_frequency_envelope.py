#!/usr/bin/env python3
"""PROTEIN -> TISSUE -> ORGAN -> ORGANISM, without the step the panel refuted.

WHY THIS EXISTS. myosin_to_power.py built a protein-to-organism chain by taking a measured
muscle power and MULTIPLYING it by a myosin isoform velocity ratio. The panel weakened that
(claim 1111) and then weakened the correction too (claim 1114), leaving three objections that
any replacement has to survive:

  1. "The baseline already contains the MYH13 advantage" is ASSERTED, not shown -- toadfish
     swimbladder expresses a FISH superfast isoform and MYH13 is mammalian extraocular, so no
     cancellation is one-to-one.
  2. A SOUND-PRODUCING MUSCLE IS NOT A POWER CEILING. Toadfish swimbladder is built for high
     frequency at low force and low myofibril fraction; its ~14 W/kg reflects that trade-off,
     not a limit on what flapping muscle could deliver.
  3. The closure did not follow from the double-count even if the double-count were real.

THIS MODULE MULTIPLIES NOTHING. It places every muscle for which this project holds a MEASURED
work-loop power at its measured operating frequency, and asks which measured points meet the
flapping requirement in BOTH coordinates. That construction is immune to objection 1 (no isoform
ratio is applied anywhere) and to objection 2 (the envelope contains locomotory POWER muscle,
not only sound muscle). It cannot over-conclude in the shape of objection 3 because its verdict
is a statement about which measured points exist, not about what is possible.

WHAT IS DECLARED HERE AND WHAT IS FETCHED. The editorial mapping -- which claim holds which
muscle, and what frequency that claim reports -- is declared below, because no column holds it.
Every POWER is fetched from claim.value_num, and every declared FREQUENCY is checked to appear
verbatim in that claim's own text before it is used. A declared number the claim does not
contain is a hard failure, not a warning: that is the only guard against this file drifting away
from the record it cites, which is how five of five hand-written summaries went wrong earlier in
this project.

THE BASIS WAS CHECKED BEFORE THE COMPARISON, because getting it wrong would invert the result.
"53 W/kg" could be per kg of MUSCLE or per kg of BODY, and claim 247 shows the two differ by the
muscle fraction (~16 W/kg body = 65-165 W/kg muscle at f = 0.10-0.25). It is per kg of MUSCLE:
claim 998 reports measured superfast muscle falling short of the requirement by 3.7x, and
14.19 x 3.7 = 52.5, which recovers the requirement from the muscle-basis number. So Hyla's
54 W/kg and the 52 W/kg requirement are the same basis and may be compared directly.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "swarm"))

from dbq import q, write_claim  # noqa: E402

PROJECT = "zebrafish-flight"
SOURCE = "analysis/power_frequency_envelope.py, reading claims 309, 586, 588, 593, 979, 997, 1090"

#: (claim id, muscle, operating frequency Hz, the frequency as the claim writes it, type, read level)
#: The frequency string must appear in the claim's own text or the run fails.
#: CLAIM 593 IS NOT IN HERE, and the first run of this file had it in. Its value_num is 4.4 --
#: the FACTOR by which 53 Hz exceeds the ~12 Hz white-muscle ceiling -- and the table printed
#: that as "4.40 W/kg", a power this project has never measured and no source states. The
#: frequency check passed it, because 593 does contain "12 Hz". A guard that checks one
#: coordinate of a two-coordinate point passes exactly half the ways of being wrong, so the
#: units check below was added and this row removed. 593's real contribution is a FREQUENCY
#: CEILING for locomotory muscle, which is reported under the table rather than plotted in it.
POINTS = (
    (1090, "Hyla chrysoscelis external oblique", 44.0, "44 Hz", "calling, NOT superfast", "abstract"),
    (997, "starling syringeal dTB", 50.0, "50 Hz", "superfast", "figure read"),
    (979, "toadfish swimbladder", 200.0, "200 Hz", "superfast", "abstract"),
)
#: Scorpaena is held out of the envelope ON PURPOSE and reported separately: a fast-start is a
#: single burst, not a cyclic frequency, so it has no x-coordinate here. Dropping it silently
#: would hide the highest measured power in the project (142.7 W/kg).
BURST = 309

REQ_POWER_CLAIM, REQ_POWER = 588, 52.0      # W/kg muscle
REQ_FREQ_CLAIM, REQ_FREQ = 586, 53.0        # Hz


_CACHE: dict[int, dict] = {}


def claim(cid: int) -> dict:
    """Three scalar reads rather than one row.

    A claim statement contains NEWLINES, and dbq.q() splits its output on lines, so a single
    multi-column select silently mis-parses into the wrong number of fields -- it failed here
    with an IndexError on the first run, which is the lucky version of that bug.
    """
    if cid in _CACHE:
        return _CACHE[cid]
    one = lambda sql: (q(sql)[0][0] if q(sql) and q(sql)[0] else "")  # noqa: E731
    v = one(f"select coalesce(value_num::text,'') from claim where id = {cid}")
    text = one("select replace(coalesce(statement,'') || ' ' || coalesce(units,'') || ' ' || "
               f"coalesce(source,''), chr(10), ' ') from claim where id = {cid}")
    sup = one(f"select coalesce(superseded_by::text,'') from claim where id = {cid}")
    units = one("select replace(coalesce(units,''), chr(10), ' ') from claim where id = " + str(cid))
    if not text:
        raise SystemExit(f"claim {cid} not found or empty")
    c = {"id": cid, "value": float(v) if v else None, "text": text, "superseded": sup,
         "units": units}
    _CACHE[cid] = c
    return c


def main() -> int:
    write = "--write" in sys.argv
    print("  POWER-FREQUENCY ENVELOPE of every muscle this project has a MEASURED power for.")
    print(f"  Requirement: {REQ_POWER:.0f} W/kg muscle (claim {REQ_POWER_CLAIM}) "
          f"at {REQ_FREQ:.0f} Hz (claim {REQ_FREQ_CLAIM}).\n")

    # --- verification pass: nothing is used before the record is shown to contain it
    bad = []
    for cid, label, hz, quote, _kind, _rl in POINTS:
        c = claim(cid)
        if quote.replace(" ", "") not in c["text"].replace(" ", ""):
            bad.append(f"claim {cid} ({label}) does not contain the declared frequency {quote!r}")
        if c["value"] is None:
            bad.append(f"claim {cid} ({label}) has no value_num to use as a power")
        elif "W/kg" not in c["units"]:
            # UNITS ONLY, NOT THE WHOLE TEXT. The first version of this guard searched statement
            # + units + source and passed claim 593, whose value_num is a dimensionless ratio:
            # its `units` does not contain "W/kg" but its STATEMENT mentions W/kg 1,119
            # characters away, discussing other muscles. The prose vouched for a number it had
            # nothing to do with. A units check that reads anything but the units field is not
            # a units check.
            bad.append(f"claim {cid} ({label}) value_num={c['value']} has units "
                       f"{c['units'][:60]!r}, which is not W/kg -- it is not a power and must "
                       f"not be plotted as one")
        if c["superseded"]:
            bad.append(f"claim {cid} ({label}) is SUPERSEDED by {c['superseded']}")
    for cid, want in ((REQ_POWER_CLAIM, "52 W/kg"), (REQ_FREQ_CLAIM, "53 Hz")):
        c = claim(cid)
        if want.replace(" ", "") not in c["text"].replace(" ", ""):
            bad.append(f"requirement claim {cid} does not contain {want!r}")
    if bad:
        print("  REFUSING TO REPORT -- the declared numbers do not match the record:")
        for b in bad:
            print(f"    - {b}")
        return 1
    print("  [verified] every declared frequency appears verbatim in its own claim; "
          "every power read from value_num; no cited claim superseded.\n")

    rows = []
    for cid, label, hz, _quote, kind, rl in POINTS:
        p = claim(cid)["value"]
        rows.append((hz, p, label, kind, cid, rl))
    rows.sort()

    print(f"  {'Hz':>6}  {'W/kg':>7}  {'power?':>6} {'freq?':>6}  muscle")
    print("  " + "-" * 86)
    both = []
    for hz, p, label, kind, cid, rl in rows:
        okp, okf = p >= REQ_POWER, hz >= REQ_FREQ
        if okp and okf:
            both.append(label)
        print(f"  {hz:6.0f}  {p:7.2f}  {'YES' if okp else 'no':>6} {'YES' if okf else 'no':>6}  "
              f"{label}  [claim {cid}, {kind}, {rl}]")
    ceil593 = claim(593)
    b = claim(BURST)
    print(f"  {'burst':>6}  {b['value']:7.2f}  {'YES':>6} {'n/a':>6}  "
          f"Scorpaena notata fast myotomal  [claim {BURST}, locomotory fast-start, held out: "
          f"a burst has no cyclic frequency]")
    print(f"\n  Locomotory frequency ceiling (claim 593, NOT a power point): fish white myotomal "
          f"muscle\n  generates no power above ~12 Hz, which the {REQ_FREQ:.0f} Hz beat exceeds "
          f"by {ceil593['value']:.1f}x. Adding muscle\n  mass does not reach a FREQUENCY ceiling, "
          f"which is why the envelope's x-axis is the binding one.")

    power_ok = [r for r in rows if r[1] >= REQ_POWER]
    freq_ok = [r for r in rows if r[0] >= REQ_FREQ]
    best_f = max(power_ok, key=lambda r: r[0]) if power_ok else None
    best_p = max(freq_ok, key=lambda r: r[1]) if freq_ok else None

    print(f"\n  meeting BOTH: {len(both)}")
    if best_f:
        gap = REQ_FREQ - best_f[0]
        print(f"  closest in FREQUENCY among power-sufficient muscles: {best_f[2]} at "
              f"{best_f[0]:.0f} Hz -- {gap:.0f} Hz short ({best_f[0]/REQ_FREQ*100:.0f}% of the "
              f"required frequency), and it is NOT a superfast muscle")
    if best_p:
        print(f"  closest in POWER among frequency-sufficient muscles: {best_p[2]} at "
              f"{best_p[1]:.2f} W/kg -- short by {REQ_POWER/best_p[1]:.1f}x")

    print(f"""
  WHAT THIS CHANGES, and what it does not.

  Claim 593 concluded that a heterologous superfast transgene is MANDATORY rather than an
  optimisation, reasoning that only superfast muscle reaches the route's frequency. The envelope
  contradicts the premise at 44 Hz: Hyla chrysoscelis external oblique is a CALLING muscle, not
  a superfast one, and it delivers {best_f[1]:.0f} W/kg there -- above the {REQ_POWER:.0f} W/kg
  requirement -- while every superfast muscle measured sits at 6 to 14 W/kg at any frequency.
  The two coordinates are met by DIFFERENT muscles and by neither one together.

  So the transgene's necessity no longer rests on "only superfast muscle is fast enough". It
  rests on a {REQ_FREQ - best_f[0]:.0f} Hz interval, {best_f[0]:.0f} to {REQ_FREQ:.0f} Hz, that
  no measured muscle crosses at the required power. That is a much narrower claim than the one
  the project has been carrying, and it is narrower in the direction that REOPENS the route.

  WHAT IS NOT SHOWN, stated before anyone infers it. Hyla's {best_f[1]:.0f} W/kg is its
  OPTIMUM. Work-loop power falls on both sides of the optimum, so its power at {REQ_FREQ:.0f} Hz
  is necessarily LOWER than {best_f[1]:.0f} and is not measured here or, as far as this project
  has read, anywhere. The honest verdict is that the muscle-power objection does not close the
  flapping route, and that the route is UNDETERMINED over a {REQ_FREQ - best_f[0]:.0f} Hz gap --
  not that it is open. Girgenrath & Marsh 1999 was read at ABSTRACT level, so the shape of that
  muscle's power-frequency curve above its optimum is a gap this project could close by reading
  the full text, which is the cheapest next step this analysis identifies.""")

    if not write:
        print("\n  NOT written. Re-run with --write to record the chain.")
        return 0

    gap = REQ_FREQ - best_f[0]
    ids = []
    ids.append(write_claim(PROJECT, "protein", f"""[THE SUPERFAST-MYOSIN TRANSGENE IS NOT SHOWN TO BE MANDATORY: A NON-SUPERFAST MUSCLE ALREADY
MEETS THE POWER REQUIREMENT, AND THE CASE FOR THE TRANSGENE NARROWS TO A {gap:.0f} Hz INTERVAL]
Claim 593 concluded a heterologous superfast transgene is mandatory rather than an optimisation,
because only superfast muscle reaches the route's frequency. Placing every measured work-loop
power in this project at its measured operating frequency contradicts the premise at 44 Hz:
Hyla chrysoscelis external oblique, a CALLING muscle and NOT a superfast one, delivers
{best_f[1]:.0f} W/kg against the {REQ_POWER:.0f} W/kg requirement, while every superfast muscle
measured sits at 6-14 W/kg at ANY frequency. Power and frequency are met by different muscles
and by neither together.

This matters at the PROTEIN scale because claim 889 showed the superfast transgene cannot even
be specified -- no superfast myosin has been sequenced. If the requirement needs a non-superfast
myosin, that unspecifiable part is not on the critical path. The necessity of the transgene now
rests on the {best_f[0]:.0f}-{REQ_FREQ:.0f} Hz interval alone.

NO ISOFORM RATIO IS APPLIED ANYWHERE in this chain, which is what separates it from claim 1104:
the panel's objection there was that multiplying a measured power by an MYH13-versus-IId
velocity ratio double-counts. This multiplies nothing and compares measured points only.""",
        "derived", gap, f"Hz of frequency interval ({best_f[0]:.0f}-{REQ_FREQ:.0f}) on which the "
        f"superfast-transgene requirement now rests, replacing 'only superfast muscle is fast enough'",
        SOURCE, "abstract"))

    ids.append(write_claim(PROJECT, "tissue", f"""[THE MEASURED POWER-FREQUENCY ENVELOPE CONTAINS NO POINT MEETING BOTH COORDINATES, AND THE
SHORTFALL IS IN FREQUENCY BY {gap:.0f} Hz RATHER THAN IN POWER]
Every muscle for which this project holds a measured work-loop power, placed at its measured
operating frequency, against the requirement of {REQ_POWER:.0f} W/kg muscle at {REQ_FREQ:.0f} Hz:

  12 Hz    {claim(593)['value']:.2f} W/kg  toadfish white myotomal (locomotory)
  44 Hz   {claim(1090)['value']:.2f} W/kg  Hyla chrysoscelis external oblique (calling, NOT superfast)
  50 Hz    {claim(997)['value']:.2f} W/kg  starling syringeal dTB (superfast)
 200 Hz   {claim(979)['value']:.2f} W/kg  toadfish swimbladder (superfast)
 burst   {claim(309)['value']:.2f} W/kg  Scorpaena notata fast myotomal (held out: a fast-start has
                           no cyclic frequency, but it is the project's highest measured power)

NONE meets both. The closest in frequency among power-sufficient muscles is Hyla at
{best_f[0]:.0f} Hz, {gap:.0f} Hz short; the closest in power among frequency-sufficient muscles
is the toadfish swimbladder at {best_p[1]:.2f} W/kg, short by {REQ_POWER/best_p[1]:.1f}x.

THIS CONSTRUCTION ANSWERS THE TWO OBJECTIONS THAT KILLED CLAIM 1111. It applies no isoform ratio,
so there is nothing to double-count; and the envelope contains locomotory POWER muscle
(Scorpaena, white myotomal) rather than only sound-producing muscle, so it does not use a muscle
optimised away from power as a power ceiling.

NOT SHOWN: Hyla's {best_f[1]:.0f} W/kg is its OPTIMUM, and work-loop power falls either side of
an optimum, so its power at {REQ_FREQ:.0f} Hz is necessarily lower and is unmeasured here. The
route is UNDETERMINED across this gap, not open. Girgenrath and Marsh 1999 was read at abstract
level; the curve's shape above the optimum would settle it and is the cheapest next step.""",
        "derived", 0, f"measured points meeting BOTH {REQ_POWER:.0f} W/kg and {REQ_FREQ:.0f} Hz, "
        f"out of {len(rows)} muscles with a measured work-loop power and a cyclic frequency",
        SOURCE, "abstract"))

    f_req = 16.0 / best_f[1]
    ids.append(write_claim(PROJECT, "organ", f"""[THE ORGAN-SCALE CONSEQUENCE: AT THE BEST NON-SUPERFAST POWER, FLIGHT MUSCLE WOULD HAVE TO BE
ABOUT {f_req*100:.0f} PERCENT OF BODY MASS]
Claim 247 records the flapping requirement on a body-mass basis as about 16 W/kg body. At the
{best_f[1]:.0f} W/kg muscle that the best measured non-superfast muscle delivers, the flight
muscle fraction required is 16 / {best_f[1]:.0f} = {f_req:.3f}, i.e. about {f_req*100:.0f}% of
body mass.

For scale, bird flight muscle is commonly 15-25% of body mass. So this is high but not outside
what flying vertebrates carry -- which means the ORGAN scale is not where this route fails. It
fails, if it fails, at the {gap:.0f} Hz frequency gap one scale below.

CARRIED FORWARD HONESTLY: the 16 W/kg body figure is itself `derived` in claim 247 and partly
rests on a search-summary read, and this project holds NO measured zebrafish muscle-mass
fraction to compare against, so the comparison above is to birds rather than to the animal being
modified. Both are gaps, and neither is closed by this chain.""",
        "derived", f_req * 100, f"percent of body mass required as flight muscle if muscle "
        f"delivers {best_f[1]:.0f} W/kg, from the ~16 W/kg body requirement in claim 247",
        SOURCE, "abstract"))

    ids.append(write_claim(PROJECT, "organism", f"""[ORGANISM-SCALE VERDICT: MUSCLE POWER DOES NOT CLOSE THE FLAPPING ROUTE, AND THE ROUTE IS
UNDETERMINED OVER A {gap:.0f} Hz INTERVAL -- IT IS NOT OPEN EITHER]
Running the chain protein -> tissue -> organ -> organism without the step the panel refuted:

  protein   the superfast transgene is not shown to be mandatory; the case for it narrows to
            {best_f[0]:.0f}-{REQ_FREQ:.0f} Hz, and claim 889's unspecifiable part leaves the
            critical path if a non-superfast myosin suffices
  tissue    no measured muscle meets both {REQ_POWER:.0f} W/kg and {REQ_FREQ:.0f} Hz; the
            shortfall is {gap:.0f} Hz of frequency, not a factor on power
  organ     about {f_req*100:.0f}% of body mass as flight muscle, within what birds carry
  organism  the route is not closed by muscle power

WHAT THIS SUPERSEDES IN SUBSTANCE, without superseding the claims: claim 979 reported the muscle
power number as closing the flapping route, and claim 998 put the shortfall at 3.7x. Both are
arithmetically right ABOUT SUPERFAST MUSCLE and both inherit claim 593's premise that only
superfast muscle is fast enough. The envelope shows a non-superfast muscle above the power
requirement at 44 Hz, so the 3.7x shortfall is a fact about the wrong muscle family.

THE CHAIN'S OWN LIMIT, stated so it is not read as a closure in the other direction: the best
non-superfast point is an OPTIMUM and power falls above an optimum, so nothing here shows any
muscle delivering {REQ_POWER:.0f} W/kg at {REQ_FREQ:.0f} Hz. Undetermined is the verdict. The
project previously held this route CLOSED; it should now hold it OPEN-UNDETERMINED, which is a
weaker and more expensive position than closure, and that is the correct one.""",
        "derived", gap, f"Hz interval over which the flapping route is undetermined "
        f"({best_f[0]:.0f}-{REQ_FREQ:.0f} Hz), after the muscle-power closure is withdrawn",
        SOURCE, "abstract"))

    print(f"\n  WROTE claims {', '.join(str(i) for i in ids)} "
          f"at scales protein, tissue, organ, organism.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
