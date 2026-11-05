#!/usr/bin/env python3
"""Has this project already claimed this -- and did it REFUTE it? Run before recording a claim.

WHY, measured 2026-11-05. Claim 1150 argued that the fin levers hit a ceiling because they
summate in resting membrane potential. Claim 597 had argued exactly that, from the same paper,
and claim 598 had refuted it: "LANNI'S EPISTASIS EXPERIMENT IS A REVERSION, NOT A COMBINATION,
AND ITS AUTHORS FAVOUR AN ADDITIVE MODEL -- SO THE SINGLE-PATHWAY CEILING IS NOT SUPPORTED BY
IT." I re-derived a refuted proposition without knowing it existed. At 500+ live claims and
another 400 superseded, that is no longer an unlikely accident.

THE SUPERSEDED CLAIMS ARE THE POINT, not an afterthought. A live claim that says what you are
about to say is a duplicate and mildly wasteful. A SUPERSEDED one is a trap: it is the exact
proposition someone already took seriously, wrote down, and then had knocked over -- so it is
the one most likely to look novel when you rediscover it, because the reasoning that produced it
was good enough to convince a previous reader. This ranks superseded hits ABOVE live ones for
that reason, and prints what superseded them.

THE MATCHER IS THE ONE THE ENTAILMENT WORK ARRIVED AT (claim 1131): units are not available here,
so it is inverse-document-frequency weighting over rare shared terms, with a shuffled null run on
every invocation. The null matters more here than it did there, because a claim corpus shares a
large vocabulary -- every claim in this project says "fin", "zebrafish" and "measured" -- and a
matcher keying on that would return the whole corpus for any query and be worse than nothing.
"""

from __future__ import annotations

import os
import pathlib
import random
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from dbq import q, lit  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
STOP = {"the", "a", "of", "in", "at", "to", "for", "and", "or", "per", "by", "its", "that",
        "must", "be", "is", "are", "with", "from", "on", "it", "this", "an", "as", "not",
        "which", "was", "were", "has", "have", "but", "so", "than", "then", "claim"}
RARE_DF = 25          #: a term in more than this many claims cannot discriminate
MIN_RARE = 3          #: at least this many rare terms shared before a hit is reported
NULL_CEILING = 0.34

DF: dict[str, int] = {}


def toks(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower())
            if w not in STOP and len(w) > 3}


def corpus():
    return q(f"""select id, coalesce(superseded_by::text,''),
             replace(left(coalesce(statement,''),700), chr(10), ' ')
             from claim where project_id = {lit(PROJECT)}""")


def build_df(rows) -> None:
    DF.clear()
    for _cid, _sup, stmt in rows:
        for t in toks(stmt):
            DF[t] = DF.get(t, 0) + 1


def search(query: str, rows, shuffled=False):
    want = toks(query)
    if shuffled:
        # A null that keeps the SIZE and the rarity profile of the query but destroys its
        # meaning: sample the same number of terms, from the same document-frequency band.
        band = [t for t, n in DF.items() if n <= RARE_DF]
        rng = random.Random(20261105)
        want = set(rng.sample(band, min(len(want), len(band))))
    out = []
    for cid, sup, stmt in rows:
        shared = want & toks(stmt)
        rare = {t for t in shared if DF.get(t, 0) <= RARE_DF}
        if len(rare) < MIN_RARE:
            continue
        score = sum(1.0 / (1 + DF.get(t, 0)) for t in rare)
        # A superseded claim is the dangerous kind, so it outranks a live one at equal score.
        out.append((score * (1.6 if sup else 1.0), cid, sup, sorted(rare), stmt))
    out.sort(reverse=True)
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print("  usage: claim_precedent.py '<the proposition you are about to record>'")
        return 2
    query = " ".join(a for a in sys.argv[1:] if not a.startswith("--"))
    rows = corpus()
    build_df(rows)
    real = search(query, rows)
    null = search(query, rows, shuffled=True)
    ratio = len(null) / len(real) if real else 0.0
    print(f"  {len(rows)} claims in {PROJECT}; {len(real)} share {MIN_RARE}+ rare terms "
          f"with the query")
    print(f"  CONTROL, same-size query of equally rare but unrelated terms: {len(null)} hits "
          f"= {ratio:.0%} of the real rate (ceiling {NULL_CEILING:.0%})")
    if real and ratio > NULL_CEILING:
        print("  TREAT THE HITS BELOW AS NOISE -- a meaningless query of equally rare terms "
              "matches nearly as often, so the vocabulary is doing the work, not the meaning.")
    print()
    if not real:
        print("  No precedent found. That is not proof of novelty: this matches on shared rare\n"
              "  words, so a claim making the same point in different vocabulary is invisible\n"
              "  to it.")
        return 0
    sup_hits = [r for r in real if r[2]]
    print(f"  {len(sup_hits)} of the top hits are SUPERSEDED claims -- read those first.\n")
    for score, cid, sup, rare, stmt in real[:8]:
        tag = f"SUPERSEDED by {sup}" if sup else "live"
        print(f"  claim {cid}  [{tag}]  score {score:.2f}  via {','.join(rare[:5])}")
        print(f"     {stmt[:170]}")
        if sup:
            why = q(f"select replace(left(coalesce(statement,''),200), chr(10), ' ') "
                    f"from claim where id = {sup}")
            if why:
                print(f"     WHAT SUPERSEDED IT: {why[0][0][:160]}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
