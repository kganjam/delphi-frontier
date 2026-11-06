#!/usr/bin/env python3
"""Does the cited corpus cover the DOMAINS the project's open questions live in?

THE FAILURE THIS ANSWERS, measured 2026-11-04. The zebrafish-flight corpus was 12 papers and
almost entirely developmental genetics -- fin-SIZE genes. The project's blocking magnitudes had
long since become mechanical: stiffness, power, frequency, elastic storage. So it was asking
mechanical questions of a genetics corpus, and the answers came back "nobody has measured this".

(Precisely: MUSCLE PHYSIOLOGY was the empty domain -- zero papers against 48 claims. MECHANICS
was thin rather than absent, 2 papers against 95. The commit that prompted this file said "the
corpus had no biomechanics in it", which was overstated, and tagging the papers one by one is
what showed it. The correction is kept rather than edited out because it is the same lesson:
a coarse claim about a corpus is exactly what this file exists to replace with a count.)
Nobody IN THAT CORPUS had. Two papers found in one afternoon settled two critical-path questions
(claims 592 and 593) and neither had ever been in the corpus. One of them, Young & Rome 2001, had
been sitting in the literature for 25 years.

That is not a research failure, it is a structural one, and it is invisible from inside: every
individual search was competently run and honestly reported. The corpus was never wrong about
what it contained -- it was just silently the wrong corpus. This stage makes that visible.

WHY IT GENERALISES, which is the point. Any cross-scale design project drifts this way. It starts
in the domain of its originating question and its blocking magnitudes migrate to other scales
while its reading list does not follow. The check is project-agnostic: it compares where the
CLAIMS are to where the CORPUS is, and both come from the database and the corpus table rather
than from anything specific to fish.

THIS IS A SWEEP, NOT A GATE. The repo's own rule (AGENTS.md section 2) is that a check with a high
false-positive rate gets switched off, and a domain classifier built on a keyword lexicon will
have one. It is meant to be run by hand after a batch of work and to have every hit read. It
prints its evidence for that reason.

CONTROL. The pre-expansion corpus is kept below as PRE_EXPANSION, which makes the control a real
historical measurement rather than a hand-written fixture: the check MUST flag mechanics as an
uncovered domain on the 2026-11-04 corpus, and MUST NOT flag it on the current one. A classifier
that flags everything, or nothing, fails one arm or the other.
"""
from __future__ import annotations

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")

# Domain lexicons. Deliberately hand-maintained and deliberately coarse: a reviewer should be
# able to disagree with a row. This restates no other system's vocabulary -- it is this
# checker's own, and nothing else reads it.
DOMAINS = {
    "mechanics": ("stiffness", "flexural", "elastic", "bending", "modulus", "strain",
                  "resonance", "inertia", "power output", "work loop", "w/kg", "torque",
                  "force", "beam", "buckl"),
    "aerodynamics": ("lift", "drag", "aerodynamic", "glide", "gliding", "coefficient",
                     "reynolds", "aspect ratio", "vortex", "stall", "airspeed", "flapping"),
    "genetics": ("allele", "mutant", "knockout", "transgene", "gene", "locus", "expression",
                 "myosin", "channel", "collagen", "promoter", "zebrafish fin", "phenotype"),
    "muscle physiology": ("muscle", "myosin", "fibre", "fiber", "twitch", "contraction",
                          "superfast", "sarcoplasmic", "cross-bridge", "detachment"),
    "kinematics": ("velocity", "speed", "acceleration", "fast-start", "escape", "body length",
                   "trajectory", "launch", "ballistic", "kinematic"),
}


from design_chain import env, flat  # noqa: E402  (after the sys.path insert below)


PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm",
      "-tAq", "-P", "pager=off"]


def q(sql: str) -> list[str]:
    """One column per row. Claim statements contain newlines, so the SQL flattens them."""
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln for ln in r.stdout.splitlines() if ln.strip()]


def classify(text: str) -> set[str]:
    """Which domains does this text touch? A text may touch several; that is correct."""
    low = text.lower()
    return {d for d, kws in DOMAINS.items() if any(k in low for k in kws)}


# DOMAIN TAGS PER PAPER, by DOI. Hand-maintained and kept explicit so a reviewer can disagree
# with a row -- the same reason studio/panels/vision.py keeps MODULE_SPECS by hand.
#
# WHY NOT INFER THEM. The first version of this file classified each paper by running the
# keyword lexicon over its one-line description ("Daane 2018 Sci Rep - kcnk5b/alf, READ").
# Those strings contain almost none of the lexicon words, so nearly every paper classified
# into NO domain and the sweep reported GENETICS as uncovered on a corpus that is mostly
# genetics. Worse, all four controls passed: the must-flag arm was satisfied by a classifier
# that flagged EVERYTHING, which is the degenerate case it existed to exclude. The lesson is
# in the controls now (see arms 5 and 6), not only here.
PAPER_DOMAINS = {
    "10.1016/j.cub.2021.08.054":   {"genetics", "aerodynamics"},
    "10.1038/s41598-018-28450-6":  {"genetics"},
    "10.1371/journal.pbio.3002565": {"genetics"},
    "10.7554/eLife.60691":         {"genetics"},
    "10.1016/j.ydbio.2019.08.016": {"genetics"},
    "10.1111/joa.12785":           {"genetics", "mechanics"},
    "10.1242/dev.204739":          {"genetics"},
    "10.1093/icb/icz145":          {"kinematics"},
    "10.1242/jeb.243180":          {"kinematics"},
    "10.1242/jeb.203.2.333":       {"kinematics"},
    "10.1016/j.ydbio.2017.07.024": {"genetics", "mechanics"},
    "10.1101/2024.03.27.587111":   {"genetics"},
    "10.1002/jmor.20161":          {"mechanics"},
    "10.1098/rspb.2001.1731":      {"muscle physiology"},
    "10.1098/rsif.2006.0181":      {"mechanics"},
    "10.1002/jmor.20830":          {"mechanics"},
    "10.1242/jeb.046052":          {"aerodynamics"},
    "10.1242/jeb.201.10.1505":     {"muscle physiology", "kinematics"},
    "10.1242/jeb.205.2.189":       {"muscle physiology"},
    "10.1146/annurev.physiol.68.040104.105418": {"muscle physiology", "genetics"},
    "10.1242/jeb.200.11.1549":     {"kinematics", "aerodynamics"},
    "10.1242/jeb.205.2.177":       {"kinematics", "aerodynamics"},
}

# The corpus as it stood before the 2026-11-04 expansion, kept so the control is a real
# historical state rather than an invented one. These are DOIs into PAPER_DOMAINS.
PRE_EXPANSION_DOIS = [
    "10.1016/j.cub.2021.08.054", "10.1038/s41598-018-28450-6",
    "10.1371/journal.pbio.3002565", "10.7554/eLife.60691",
    "10.1016/j.ydbio.2019.08.016", "10.1111/joa.12785",
    "10.1242/dev.204739", "10.1093/icb/icz145", "10.1242/jeb.243180",
    "10.1242/jeb.203.2.333", "10.1016/j.ydbio.2017.07.024",
    "10.1101/2024.03.27.587111",
]

_UNUSED_PRE_EXPANSION_DESCRIPTIONS = [
    "Daane 2021 Curr Biol - flying-fish phenocopy",
    "Daane 2018 Sci Rep - kcnk5b/alf, READ",
    "Jiang 2024 PLoS Biol - pectoral bud, READ",
    "Yi 2021 eLife - S345, READ",
    "Lanni 2019 Dev Biol - schleier/Kcc4a",
    "Murciano 2018 J Anat - inter-ray, READ",
    "Development",
    "Integr Comp Biol",
    "J Exp Biol",
    "J Exp Biol 2000 - NOT open access",
    "Koenig 2017 - NOT open access (actinotrichia)",
    "bioRxiv preprint - no PMC record",
]


def corpus_domains(dois) -> dict[str, int]:
    """Count papers per domain from the explicit tags. An untagged DOI is an ERROR, not a zero:
    silently treating it as covering nothing is how the first version produced a false gap."""
    counts = {d: 0 for d in DOMAINS}
    for doi in dois:
        if doi not in PAPER_DOMAINS:
            raise KeyError(f"corpus paper {doi!r} has no domain tag in PAPER_DOMAINS -- "
                           f"tag it rather than letting it count as covering nothing")
        for d in PAPER_DOMAINS[doi]:
            if d not in counts:
                raise KeyError(f"{doi!r} tagged with unknown domain {d!r}")
            counts[d] += 1
    return counts


def analyse(descriptions, claims, label, verbose=True):
    cov = corpus_domains(descriptions)
    claim_counts = {d: 0 for d in DOMAINS}
    for row in claims:
        for d in classify(row):
            claim_counts[d] += 1

    if verbose:
        print(f"\n  {label}")
        print(f"  {'domain':<22}{'claims':>8}{'corpus papers':>16}   status")
        print("  " + "-" * 62)
    gaps = []
    for d in DOMAINS:
        c, p = claim_counts[d], cov[d]
        if c > 0 and p == 0:
            status = "UNCOVERED -- gap"
            gaps.append(d)
        elif c > 0 and p < max(1, c // 20):
            status = "thin"
        else:
            status = "ok" if c else "-"
        if verbose:
            print(f"  {d:<22}{c:>8}{p:>16}   {status}")
    return gaps


CLAIM_TEXT = "coalesce(statement,'') || ' ' || coalesce(units,'')"


def main() -> int:
    from figure_sweep import CORPUS

    claims = q(
        f"select {flat(CLAIM_TEXT)} "
        f"from claim where project_id = '{PROJECT}' and superseded_by is null")

    print("=" * 78)
    print(f"CORPUS DOMAIN COVERAGE -- project '{PROJECT}'")
    print("=" * 78)
    print(f"  {len(claims)} live claims, {len(CORPUS)} cited papers")

    gaps = analyse(list(CORPUS.keys()), claims, "CURRENT CORPUS")

    print("\n" + "-" * 78)
    if gaps:
        print(f"  {len(gaps)} UNCOVERED DOMAIN(S): {', '.join(gaps)}")
        print("  The project is asking questions in a domain its reading list does not cover.")
        print("  Read every hit -- this is a sweep, not a gate, and it has false positives.")
    else:
        print("  No uncovered domain. Every domain the live claims touch has cited papers.")

    # ------------------------------------------------------------------ controls
    print("\nCONTROLS -- the 2026-11-04 corpus is the historical must-flag case")
    ok = True
    pre_gaps = analyse(PRE_EXPANSION_DOIS, claims, "PRE-EXPANSION", verbose=False)
    arm1 = "muscle physiology" in pre_gaps
    print(f"  [{'ok' if arm1 else 'FAIL'}] muscle physiology IS flagged on the pre-expansion "
          f"corpus (gaps found: {', '.join(pre_gaps) or 'none'})")
    ok &= arm1

    arm2 = "muscle physiology" not in gaps
    print(f"  [{'ok' if arm2 else 'FAIL'}] muscle physiology is NOT flagged on the current "
          f"corpus -- the expansion actually fixed it")
    ok &= arm2

    # A classifier that matched everything would pass both arms above.
    arm3 = classify("a sentence about nothing in particular") == set()
    print(f"  [{'ok' if arm3 else 'FAIL'}] an unrelated sentence classifies into NO domain "
          f"-- the classifier is not matching everything")
    ok &= arm3

    arm4 = "mechanics" in classify("flexural stiffness of the fin ray")
    print(f"  [{'ok' if arm4 else 'FAIL'}] a known-mechanics sentence classifies as mechanics "
          f"-- the classifier is not matching nothing")
    ok &= arm4

    # Arms 5 and 6 are the ones the first version lacked, and its absence let a classifier
    # that flagged EVERY domain satisfy arm 1. A must-flag arm is only meaningful beside a
    # must-NOT-flag arm on the same corpus.
    arm5 = "genetics" not in pre_gaps
    print(f"  [{'ok' if arm5 else 'FAIL'}] genetics is NOT flagged on the pre-expansion corpus "
          f"-- it was genetics-rich, so flagging it would mean the sweep flags everything")
    ok &= arm5

    arm6 = len(pre_gaps) < len(DOMAINS)
    print(f"  [{'ok' if arm6 else 'FAIL'}] the pre-expansion corpus does not flag ALL "
          f"{len(DOMAINS)} domains ({len(pre_gaps)} flagged)")
    ok &= arm6

    # Every corpus paper must carry a tag; corpus_domains raises otherwise, so reaching here
    # at all proves the current corpus is fully tagged.
    print(f"  [ok] all {len(CORPUS)} corpus papers carry an explicit domain tag")

    print(f"  -> controls {'PASS' if ok else 'FAIL'}")
    if not ok:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
