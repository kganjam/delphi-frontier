#!/usr/bin/env python3
"""What a zebrafish must actually achieve to fly, assembled from the constraint layer.

The project holds 327 distinct cross-scale constraints. 92 are `unsatisfied` and 7 are
`unsatisfiable` -- evaluated and FAILING -- and each failing row records WHY in its
`satisfied_by` field. Nobody had ever read them together, so the project could say how many
constraints were open but not what the animal is actually short of.

THIS INVENTS NOTHING AND PARSES NO PROSE. Bounds, units, scales and status are structured
columns; the refutation is quoted verbatim from the row that recorded it. The one judgement here
is the GROUPING -- which failing constraints are about the same physical quantity -- and it is
declared in QUANTITY_GROUPS below rather than inferred, so a reader can disagree with a line
instead of with an algorithm. Extracting numbers from the refutation text was deliberately NOT
done: that is exactly the "a matcher cannot read prose" failure this project measured twice.

WHAT IT FOUND ON FIRST RUN, and the reason this file exists: FIVE of the seven `unsatisfiable`
constraints are the same fact wearing five statements -- e194, e224, e258, e316 and e353 all
assert a higher adult burst speed than Demesmay et al. 2025 measured (157 +/- 27 cm/s). The
project's hardest blocker is not five problems. It is one number, recorded five times.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "swarm"))

from dbq import q, lit  # noqa: E402

PROJECT = "zebrafish-flight"

#: EDITORIAL, and the only judgement in this file: which failing constraints are about one
#: physical quantity. A label here claims nothing about the physics -- it says "these rows are
#: about the same thing", and the rows are printed under it so the grouping can be checked.
QUANTITY_GROUPS = (
    ("adult burst / escape speed",
     ("burst", "escape", "fast-start", "maximal speed", "peak speed")),
    ("muscle power and work density",
     ("muscle mass-specific power", "work per kg", "work density", "spring-loading work",
      "isotonic power", "cyclic power")),
    ("beat frequency and contraction timing",
     ("tail-beat", "beat frequency", "cycle frequency", "activation-relaxation",
      "decay time constant", "half-cycle")),
    ("muscle and body mass budget",
     ("muscle mass / body", "mass fraction", "muscle fraction", "body mass")),
    ("fin and lobe aerodynamics",
     ("lobe", "foil", "drag coefficient", "A_pp", "aspect", "wing")),
    ("molecular part availability",
     ("transmembrane", "residue", "numbering offset", "product", "ortholog")),
)


#: A FAILING CONSTRAINT FAILS IN ONE OF TWO WAYS AND THEY ARE NOT THE SAME NEWS. Either a
#: measurement CONTRADICTS it -- the design must change -- or nobody has measured the quantity,
#: which says nothing about the design and names an experiment. The first run of this file merged
#: them and reported 99 "failing constraints", which reads as 99 reasons a zebrafish cannot fly.
#: Most are literature gaps. The phrases below are taken from how the refutations are actually
#: written in this corpus, not invented.
CONTRADICTED = ("contradicted by", "measured contradiction", "contradicts", "refuted by")
UNMEASURED = ("not found", "no measured", "nobody has looked", "no adult", "no zebrafish",
              "none found", "no occupant", "not been measured", "no published", "searched")
#: Constraints that are not about the animal at all. Infrastructure rows leaked into the
#: biological project and would otherwise be counted as design blockers.
INFRA = ("admission", "operation", "idempotency", "slot", "sha256", "endpoint", "api ",
         "commit", "repository", "branch")


def failure_mode(why: str) -> str:
    low = (why or "").lower()
    if any(k in low for k in CONTRADICTED):
        return "CONTRADICTED"
    if any(k in low for k in UNMEASURED):
        return "UNMEASURED"
    return "unclassified"


def is_infra(text: str) -> bool:
    low = (text or "").lower()
    return sum(1 for k in INFRA if k in low) >= 2


def group_of(text: str) -> str:
    low = (text or "").lower()
    for label, keys in QUANTITY_GROUPS:
        if any(k in low for k in keys):
            return label
    return "other"


def main() -> int:
    rows = q(f"""select id, coalesce(status,''), coalesce(source_scale,'?'),
             coalesce(target_scale,'?'), coalesce(quantity,''),
             coalesce(lo::text,''), coalesce(hi::text,''), coalesce(units,''),
             replace(left(coalesce(statement,''),200), chr(10), ' '),
             replace(left(coalesce(satisfied_by,''),300), chr(10), ' ')
             from constraint_entailed
             where project_id = {lit(PROJECT)} and status in ('unsatisfied','unsatisfiable')
             order by status desc, id""")
    if not rows:
        print("  no failing constraints recorded.")
        return 0

    infra = [r for r in rows if is_infra(r[4] + " " + r[8] + " " + r[9])]
    rows = [r for r in rows if r not in infra]
    buckets: dict[str, list] = {}
    for r in rows:
        buckets.setdefault(group_of(r[4] + " " + r[8]), []).append(r)

    modes = {m: sum(1 for r in rows if failure_mode(r[9]) == m)
             for m in ("CONTRADICTED", "UNMEASURED", "unclassified")}
    print("  WHAT A ZEBRAFISH MUST ACHIEVE TO FLY, and where the record says it falls short.")
    print(f"  {len(rows)} failing biological constraints "
          f"({len(infra)} infrastructure rows excluded -- they are about the compute service, "
          f"not the animal, and counting them as design blockers would be wrong).\n")
    hard = sum(1 for r in rows if r[1] == "unsatisfiable")
    print("  THE CURATED SPLIT, from the `status` column, which is the one to trust:")
    print(f"     {hard:>3}  UNSATISFIABLE -- a measurement contradicts the constraint. The "
          f"design must change,")
    print("          or the constraint was wrong. No further evidence rescues these.")
    print(f"     {len(rows)-hard:>3}  unsatisfied -- evaluated, and the evidence held did not "
          f"meet it.\n")
    print("  A HEURISTIC READ OF THE REFUTATION TEXT, OFFERED AS A HINT AND NOT AS DATA.")
    print("  It is phrase-matching over prose, which this project has measured twice as")
    print("  unreliable, and here it leaves 41 of 96 unclassified and gets at least one wrong:")
    print("  e27 reads UNMEASURED although its own text says 'measured adult maximum is 52 Hz'")
    print("  against a required 72-117 Hz, which is a contradiction. Use it to triage reading")
    print("  order, never to count:")
    print(f"     {modes['CONTRADICTED']:>3}  CONTRADICTED by a measurement -- the design must "
          f"change, or the constraint was wrong")
    print(f"     {modes['UNMEASURED']:>3}  UNMEASURED -- nobody has made the measurement. This "
          f"says NOTHING about whether the design works;")
    print("          it names an experiment. Most of this project's 'failures' are of this kind.")
    print(f"     {modes['unclassified']:>3}  unclassified -- the refutation text matches neither "
          f"pattern; read these by hand\n")

    order = sorted(buckets, key=lambda k: (-sum(1 for r in buckets[k] if r[1] == "unsatisfiable"),
                                           -len(buckets[k])))
    for label in order:
        rs = buckets[label]
        hard = [r for r in rs if r[1] == "unsatisfiable"]
        print(f"  === {label.upper()}  ({len(rs)} constraints, {len(hard)} contradicted by "
              f"measurement) ===")
        for r in rs[:6]:
            eid, st, ss, ts, qty, lo, hi, un, stmt, why = r
            bound = (f"[{lo or '-'}, {hi or '-'}] {un}".strip()) if (lo or hi or un) else ""
            mode = failure_mode(why)
            mark = {"CONTRADICTED": "XX", "UNMEASURED": "??"}.get(mode, "  ")
            print(f"   {mark} e{eid:<4} [{ss}->{ts}] {qty[:46] if qty else stmt[:46]}")
            if bound:
                print(f"           requires {bound}")
            if why:
                print(f"           {mode}: {why[:145]}")
        if len(rs) > 6:
            print(f"      ... and {len(rs)-6} more in this group")
        print()

    hard_all = [r for r in rows if r[1] == "unsatisfiable"]
    by_group: dict[str, int] = {}
    for r in hard_all:
        by_group[group_of(r[4] + " " + r[8])] = by_group.get(group_of(r[4] + " " + r[8]), 0) + 1
    print("  THE HARD BLOCKERS ARE NOT SEVEN PROBLEMS. Grouped by physical quantity, the "
          f"{len(hard_all)} contradicted constraints are:")
    for lab, n in sorted(by_group.items(), key=lambda kv: -kv[1]):
        print(f"     {n:>2}  {lab}")
    print("""
  READ THIS AS A WORK LIST, NOT A VERDICT. `unsatisfied` means the project evaluated the
  constraint and the evidence it had did not meet it -- which can mean the design fails, or
  that the right measurement has not been made. `unsatisfiable` is stronger: a measurement
  CONTRADICTS the constraint, so no further evidence will rescue it and the design must change
  or the constraint was wrong. Those are different states and merging them would overstate
  how blocked the project is.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
