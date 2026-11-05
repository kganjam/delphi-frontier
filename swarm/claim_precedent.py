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


def stem(w: str) -> str:
    """Crudest possible suffix stripping, and it was not optional.

    Without it the must-find control FAILED on its first run: the query said "frequency" and
    "conflicts" where entailment e38 says "frequencies" and "conflict", so two of the shared
    terms never matched and the hit fell below the three-rare-term floor. A precedent checker
    that misses a record because of an English plural is not a precedent checker. No stemmer
    library is used, because the only job here is collapsing inflections that would otherwise
    split one concept into two tokens.
    """
    for suf in ("ies", "ing", "ed", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)] + ("y" if suf == "ies" else "")
    return w


def toks(s: str) -> set[str]:
    return {stem(w) for w in re.findall(r"[a-z0-9]+", (s or "").lower())
            if w not in STOP and len(w) > 3}


def corpus():
    """Claims AND entailments. The first version searched claims only, and missed.

    Measured 2026-11-05, the same day this module was written to stop exactly this: claim 1145
    reported a conflict in flying-fish tail-beat frequency as a finding, and entailment e38
    already held all three figures -- Davenport 1994, Deng 2019 and the APS 2024 13.5 Hz -- in
    its satisfied_by field. A propositions-level checker that reads only one of the two tables
    where this project records propositions is a checker with a blind spot the size of the other
    table. 381 entailment rows carry prose nobody was searching.
    """
    claims = q(f"""select 'claim ' || id, coalesce(superseded_by::text,''),
               replace(left(coalesce(statement,''),700), chr(10), ' ')
               from claim where project_id = {lit(PROJECT)}""")
    ents = q(f"""select 'entailment e' || id, '',
             replace(left(coalesce(statement,'') || ' ' || coalesce(satisfied_by,''), 700),
                     chr(10), ' ')
             from constraint_entailed where project_id = {lit(PROJECT)}""")
    return claims + ents


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
    print(f"  {len(rows)} records in {PROJECT} (claims + entailments); {len(real)} share "
          f"{MIN_RARE}+ rare terms with the query")
    print(f"  CONTROL, same-size query of equally rare but unrelated terms: {len(null)} hits "
          f"= {ratio:.0%} of the real rate (ceiling {NULL_CEILING:.0%})")
    # A RATIO ON A HANDFUL OF HITS IS NOT A MEASUREMENT. Measured on its own must-find control:
    # 3 real hits against 1 null reads as 33%, just under the ceiling -- but one hit either way
    # moves it to 0% or 67%. Saying so is cheaper than pretending the number means something.
    if real and len(real) < 8:
        print(f"  (that ratio rests on {len(real)} real hits; one hit either way moves it by "
              f"{1/len(real):.0%}, so read it as a smell test and not a measurement)")
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
        print(f"  {cid}  [{tag}]  score {score:.2f}  via {','.join(rare[:5])}")
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
