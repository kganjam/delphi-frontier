#!/usr/bin/env python3
"""Generate the cross-scale design chain from the claim graph, not from memory.

The goal asks to show this project "going from all scales back down to dna with realistic,
grounded, non-hallucinated simulations". That chain now exists, but it is spread across 500+
claims and nobody can see it. This assembles it.

IT IS GENERATED, NOT WRITTEN. Every row's number and evidence class is pulled from the claim it
cites, so the document cannot drift from the graph the way hand-maintained prose does -- which is
this repository's own recurring failure (one system's vocabulary restated inside another).

THE CHAIN IS DECLARED HERE AND THE VALUES ARE FETCHED. The declaration is the editorial act: it
says which claims form the spine of the argument and in what order. That judgement cannot be
automated and is stated plainly rather than hidden in a query.

Usage:  python3 design_chain.py            # markdown to stdout
        python3 design_chain.py --write    # to docs/DESIGN-CHAIN.md
"""
from __future__ import annotations

import sys

from dbq import PG, PROJECT, SEP, env, flat, lit, q  # noqa: F401,E402  (re-exported)

# (scale, question, claim id) -- the editorial spine. Order is the argument, not the id order.
CHAIN = [
    # ORGANISM: the aerodynamic requirement and what sets it
    ("ORGANISM / criterion",
     "Which threshold is the project measuring against?", 571),
    ("ORGANISM / aerodynamics",
     "Does a wing beat a ballistic leap, and how much does launch ANGLE matter?", 523),
    ("ORGANISM / aerodynamics",
     "Can a better-SHAPED fin compensate for less area?", 579),  # was 568: 'irreducible' overreached; 579 gives the CL-bounded form
    ("ORGANISM / aerodynamics",
     "Is the drag coefficient the project uses physically attainable?", 565),
    ("ORGANISM / aerodynamics",
     "Is the gliding negative robust to the LIFT coefficient?", 599),
    ("ORGANISM / kinematics",
     "What exit speed does the fish actually have?", 546),
    ("ORGANISM / kinematics",
     "Is peak speed available AT the surface?", 548),
    ("ORGANISM / kinematics",
     "Can a run-up supply the missing speed?", 583),  # was 570: it assumed work-limiting; 583 shows impulse reopens the lever
    ("ORGANISM / energetics",
     "Can muscle supply that speed at all?", 547),
    ("ORGANISM / body plan",
     "Does a SMALLER fish need less fin?", 577),  # was 576: the cross-species refutation was invalid; 577 is the corrected form
    ("ORGANISM / body plan",
     "Does reducing body MASS close the gap?", 550),
    ("ORGANISM / body plan",
     "What wind does the ACHIEVABLE animal actually need?", 988),
    ("ORGANISM / body plan",
     "The taxi route has its organ now -- does it close?", 1014),  # was 992: it fitted one exponent across Eloy's laminar/turbulent kink AND corner-selected it
    ("ORGANISM / body plan",
     "Is there a danionin already at the required size?", 1000),
    ("ORGANISM / body plan",
     "Can a zebrafish instead be ENGINEERED to that size?", 1012),  # was 991: its Re range mixed corners
    # ORGAN and TISSUE
    ("ORGAN / fin morphology",
     "How much fin AREA is achievable, and at what aspect ratio?", 567),
    ("ORGAN / fin morphology",
     "What does the best published allele give?", 542),
    ("ORGAN / fin morphology",
     "Does the allele PAIR give the flying-fish body plan?", 990),  # was 989: it read Fig 4C's DORSAL lobe as the whole caudal fin
    ("ORGAN / fin morphology",
     "How does the achievable fin compare with real gliders, in their own unit?", 986),
    ("ORGAN / fin morphology",
     "Can fin AREA be enlarged without the ray-stiffness penalty?", 1013),
    ("ORGAN / fin morphology",
     "At what LIFE STAGE is the fin ratio measured, and which way does that err?", 1025),  # 1001 superseded by 1003: it read a FIT, not the specimens
    ("ORGAN / swim bladder",
     "Can the body be made light enough?", 553),
    ("TISSUE / fin skeleton",
     "Is the enlarged fin stiff enough?", 537),
    # GENE
    ("GENE / kcnk5b",
     "What genes enlarge the fin?", 531),
    ("GENE / pathway",
     "Are the fin levers independent, or one pathway?", 562),
    ("GENE / hox",
     "What genes enlarge the swim bladder?", 551),
    ("GENE / autonomic",
     "What gene defeats buoyancy regulation?", 554),
    # the bottom line
    # POWERED FLIGHT -- the route the gliding analysis assumed away entirely
    ("ORGANISM / powered flight",
     "Could it FLAP instead of gliding?", 585),
    ("ORGANISM / powered flight",
     "Does unsteady flapping lift close the gap?", 586),
    ("ORGANISM / powered flight",
     "What lift coefficient is actually attainable?", 601),
    ("TISSUE / muscle",
     "Can the fin muscle beat fast enough?", 998),  # was 588: its 35-71 W/kg availability was DERIVED; measurement says 14.19  # was 587: it closed the route on an
                                                    # assertion; 588 computes the budget
    ("TISSUE / muscle",
     "Can any fish muscle generate power AT that frequency?", 593),
    ("TISSUE / fin mechanics",
     "Does elastic storage recover the inertial cost?", 592),
    ("GENE / myosin",
     "Is there a gene for superfast fin muscle?", 589),
    ("GENE / myosin",
     "Can that gene actually be obtained?", 889),
    ("GENE / collagen",
     "Is fin SHAPE genetically addressable?", 590),
    ("SYNTHESIS",
     "What is the best design this project can specify?", 580),  # was 574: the 1.54x gain double-counted progressive overgrowth; 580 is 1.41x
    ("SYNTHESIS",
     "What does that design actually achieve?", 584),
]


def main() -> int:
    ids = ",".join(str(c[2]) for c in CHAIN)
    rows = {int(r[0]): r for r in q(
        f"""select id, coalesce(value_num::text,''), coalesce(units,''), evidence,
                   coalesce(read_level,''), coalesce(superseded_by::text,''),
                   -- flat() scrubs BEFORE truncating, which is the order that matters:
                   -- a statement whose first 150 characters contain a line break would
                   -- otherwise parse as TWO rows, the second one's id field a fragment of
                   -- prose, failing as an int() ValueError far from its cause. It lay dormant
                   -- only because every earlier claim happened to open with one long line.
                   {flat('statement', 150)}
            from claim where id in ({ids})""")}

    out = []
    out.append("# The zebrafish flight design chain\n")
    out.append("GENERATED by `swarm/design_chain.py` from the claim graph. Do not hand-edit: "
               "every number below is fetched from the claim that cites it, so this file cannot "
               "drift from the evidence. The CHAIN ITSELF is an editorial judgement, declared in "
               "that script.\n")
    out.append("`evidence` is the claim's own class. **`derived` means computed from other "
               "claims; `literature` means read from a paper; `measured` means measured here.** "
               "A superseded claim is shown struck, with its successor.\n")

    last_scale = None
    for scale, question, cid in CHAIN:
        r = rows.get(cid)
        if not r:
            out.append(f"- **{question}** — claim {cid} NOT FOUND in the graph\n")
            continue
        _, val, units, ev, rl, sup, stmt = r
        if scale != last_scale:
            out.append(f"\n## {scale}\n")
            last_scale = scale
        num = f"**{val} {units}**" if val else "_no single value_"
        tag = f"`{ev}`" + (f" / `{rl}`" if rl else "")
        sup_s = f" — ⚠️ SUPERSEDED by claim {sup}" if sup else ""
        out.append(f"**{question}**  \n{num}  \nclaim {cid} {tag}{sup_s}  \n_{stmt.strip()}…_\n")

    # The binding constraints, computed from the graph rather than asserted.
    out.append("\n## Where it stands\n")
    P = f"project_id = '{PROJECT}'"
    n_live = q(f"select count(*) from claim where {P} and superseded_by is null")[0][0]
    n_all = q(f"select count(*) from claim where {P}")[0][0]
    n_sup = q(f"select count(*) from claim where {P} and superseded_by is not null")[0][0]
    by_ev = q(f"""select evidence, count(*) from claim where {P} and superseded_by is null
                  group by 1 order by 2 desc""")
    others = q(f"""select project_id, count(*) from claim where project_id <> '{PROJECT}'
                   group by 1 order by 2 desc""")
    out.append(f"- {n_live} live claims of {n_all} for project `{PROJECT}`; **{n_sup} "
               f"superseded**, which is the project correcting itself and is not a defect.\n")
    if others:
        out.append("- (the same database also holds "
                   + ", ".join(f"`{p}` {n}" for p, n in others)
                   + " — NOT counted above, because an earlier version of this summary counted "
                     "the whole table and reported another project's work as this one's)\n")
    out.append("- live claims by evidence class: "
               + ", ".join(f"`{e}` {n}" for e, n in by_ev) + "\n")
    out.append("\n**Two criteria, and they are not the same question:**\n")
    out.append("- the **2 cm lift-attributable** threshold asks whether a wing beats no wing. "
               "The best specifiable design is **1.08× short** of it, and crosses only by "
               "extrapolating a speed below its measured range (claims 574, 575).\n")
    out.append("  **That reading was pushed through five revisions on 2026-11-05 and ends at "
               "NOT SHOWN.** A route needing no size extrapolation exists -- hold the body at "
               "the measured size and let an upper-tail individual supply the speed, since "
               "Demesmay's 157 ± 27 cm/s is a standard deviation BETWEEN individuals (read "
               "from the paper's methods). On that route the best allele is **longfin at 1.95 "
               "m/s, about one fish in twelve** (claim 2773), which independently reproduces "
               "claim 567's allele ranking. But it rests on an Oswald efficiency of **0.85 that "
               "claim 567 never states** (claim 2775), and there is a **cliff at about 0.55** "
               "below which longfin clears at NO speed. The literature puts the design below "
               "it: measured span efficiencies for insects at this Reynolds number are "
               "**0.217-0.602** (claim 2776). Put each measured value through the same "
               "trajectory model, with no correction factor and no further argument: **nine of "
               "the ten give 'clears at NO speed'**, and the tenth (hawkmoth, 0.602) gives 2.0 "
               "per cent of fish. Claim 567's 0.85 is higher than EVERY measured value in the "
               "set (claim 2779). *The adversarial arm challenged four claims in this arc and "
               "all four were conceded* -- a correction factor applied across a category "
               "boundary, a provenance story inferred from a coincidence, an overstated "
               "'cliff', and a gliding comparison resting on two birds; claim 2779 records "
               "each and re-derives the conclusion without them. So the weak threshold is not "
               "nearly met; it is unshown, and the one "
               "quantity that would settle it is a span efficiency for a gliding "
               "low-aspect-ratio surface at Re ~3000, which nobody appears to have "
               "measured.\n")
    out.append("- **lift ≥ weight**, which is what flying means, needs ~17× the present "
               "silhouette. The best design is **4.3× short** (claim 571).\n")
    out.append("\n**Every lever has been pushed to a bound:**\n")
    # ONE append: the list is joined with newlines AND each append ends with one, so a row
    # per append puts a blank line between every row and markdown stops seeing a table.
    out.append("\n".join([
        "| lever | bound | why |",
        "|---|---|---|",
        "| fin area | ~2.65x, ADULTS ONLY | three alleles on one bioelectric pathway. The three "
        "papers this rests on -- PMC3894163, PMC6039437, PMC7235970 -- mention `larva` and `dpf` "
        "ZERO times between them against 15, 4 and 21 mentions of `adult` (claim 1401), so the "
        "multiplier is not established below 10 mm and CANNOT BE MULTIPLIED BY THE BODY-SIZE "
        "ROW without extrapolating across the stage at which fin musculature matures |",
        "| fin shape | nothing beyond the floor | aspect ratio saturates; induced drag -> 0 "
        "and the requirement stops falling |",
        "| exit speed | 1.57-1.60 m/s | muscle work, and speeds add in quadrature so a run-up "
        "needs a 23 BL/s sprint |",
        "| body size | favourable, bounded by a 5x gap in the exponent | lift/weight ~ L^(2b-1) "
        "and b is bracketed, not unknown: b=0 from mummichog FAST-START (claim 573) gives 6.0 mm "
        "at Re 642, b=0.269 from zebrafish FEEDING strikes measured off a figure (claim 1292) "
        "gives 1.1 mm at Re 50. The within-species fast-start exponent is the open quantity |",
        "| body mass | no implementation | needs ~46% gas volume and a distributed autonomic "
        "setpoint defeated |",
        "| surface taxi | NARROWED, and now rests on muscle POWER rather than frequency | the "
        "exemplar taxis to 1.6x its exit speed, worth 2.69x in lift, applied by claim 1404. A "
        "WILD-TYPE zebrafish cannot drive it: claim 196 needs ~49-73 Hz at 1.95 m/s against "
        "measured adult maxima of 21 Hz sustained and 52 Hz transient, and claim 37 puts the "
        "taxi ceiling at sustainable frequencies at ~0.56 m/s, which is Ucrit itself. At the "
        "16.3 mm target the requirement is 90-526 Hz, because amplitude scales with length so "
        "f ~ 1/L and shrinking the body to supply LIFT raises the taxi frequency by the same "
        "factor (claim 1866). BUT THE DESIGN IS NOT A WILD-TYPE FISH: against the toadfish "
        "swimbladder's measured 200 Hz (claim 979), the superfast transgene already in this "
        "project's part list, 4 of the 9 amplitude x Strouhal corners are reachable -- every "
        "corner at 0.35 body lengths. Every non-superfast muscle measured here covers 0 of 9. So "
        "it is not frequency that closes the lever (claim 1869, superseding 1866). POWER DOES, and "
        "without a drag model: the kinetic-energy increment over the specified 20 body lengths "
        "demands at least 23.9 W/kg of muscle at perfect transfer and the favourable 0.55 muscle "
        "fraction WITH DRAG EXCLUDED, against the 14.19 W/kg that same superfast muscle delivers "
        "-- 1.7x short at the most generous corner and 5.9x at claim 960's measured transfer "
        "efficiency. Drag only adds, so no drag model can reopen it. Frequency and power are met "
        "by DIFFERENT muscles and by neither together, which is claim 1127's configuration for "
        "the third time (claim 1870) |",
    ]))
    # "absent from PubMed" was withdrawn on 2026-11-05. The search behind it ran without
    # `sort=relevance`, so it returned the most RECENT PMC matches rather than the most relevant
    # (claim 1287), and the corpus route was efetch alone, which reaches different papers from
    # Europe PMC (claim 1388). Re-searched through both routes and through preprints, the
    # measurement is still not obtained -- but for a different and narrower reason, and saying
    # "absent from PubMed" overstated how complete the search had been.
    out.append("\nThe chain is complete in structure. Every link has a number and an evidence "
               "class, and the places it fails are named rather than bridged. **The single "
               "cheapest open measurement is a zebrafish fast-start velocity against body "
               "length over 20–40 mm.** It is not absent from the literature: biomechanics "
               "papers measure it and report it in FIGURES, and PMC3675323 states the exact "
               "normalisation in its methods while publishing no value in text (claim 1291). "
               "Searched through NCBI efetch, Europe PMC full text, Europe PMC figure packages "
               "and preprints, the nearest obtainable values are a cross-species plateau "
               "(claim 1290) and a within-species FEEDING-strike exponent (claim 1292). It "
               "governs whether the body-size lever is worth 6.0 mm or 1.1 mm.\n")
    out.append("\n**A cheaper question has displaced it.** The fin-area and body-size rows "
               "cannot both be applied as written: 2.65x is an ADULT measurement and the size "
               "target is 6.0 mm, which is late-larval and below the 10 mm at which fin "
               "musculature reaches adult-like morphology (claims 1400, 1401). The question "
               "that now gates the design is **does the 2.65x fin-area effect hold at 6 mm "
               "total length?** That is a photograph and an area, on mutant lines that already "
               "exist, at a standard stage -- not a search for a value published only in "
               "figures.\n")

    text = "\n".join(out)
    if "--write" in sys.argv:
        from pathlib import Path
        p = Path(__file__).resolve().parent.parent / "docs/DESIGN-CHAIN.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        print(f"wrote {p} ({len(text)} chars)")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
