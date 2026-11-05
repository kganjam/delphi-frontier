#!/usr/bin/env python3
"""Import `design-space-result-0.1` studies into designswarm, for a SECOND project.

THE GOAL SAYS the coral and insect projects "didn't follow the same structure as the fish project
and are a bit scattered". When this file was written `zebrafish-flight` WAS the only project_id in
the graph -- claim 323, subproblem 95, constraint_entailed 381, run 27, parameter 5, artifact 9,
and ZERO rows for anything else. They did not merely follow a different structure; they were never
in it.

That is no longer true, and this importer is why. As of 2026-11-04 the graph holds three projects:
zebrafish-flight (439 claims, 100 subproblems), coral (3), and insect-flight (54, imported by the
second mapping below). What remains outside are the ROUTES and INDEX files -- coral's 45 routes
across 9 scales and 142 evidence items, and insect-flight's index.json and routes.json -- which
use `design-space-routes-0.1` and `design-space-index-0.1` and have no mapping yet. Neither
limbless-mouse nor xenobot is registered at all.

The material is not lower quality. `results/coral/` carries pre-declared controls with an honestly
reported FAILURE ("5 of 6 pre-declared controls pass and 1 FAILS ... and the criterion was not
moved"), per-source read levels, PMIDs, explicit limitations, and reproducible code. It is good
science sitting outside the graph, under its own schema.

THE ONE RULE THIS IMPORTER EXISTS TO ENFORCE. Each study declares `is_observation`. A study with
`is_observation: false` is a SIMULATION and is imported as `evidence='simulated'` -- never
'measured', never 'derived'. That is SPEC section 1 rule 1: SimulationResult and Observation are
different types and stay different in the graph. An importer that flattened them would be the
exact fabrication the spec forbids, and it would be invisible afterwards.

    python3 import_design_space.py <project_id> <dir> [--write]
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
import sys

SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm",
      "-tAq", "-F", SEP]
SCHEMA = "design-space-result-0.1"


def env() -> dict:
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=90)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:400])
    return [ln.split(SEP) for ln in r.stdout.strip().split("\n") if ln]


def lit(s) -> str:
    return "null" if s is None else "'" + str(s).replace("'", "''") + "'"


def evidence_of(study: dict) -> str:
    """The whole point. A simulation never becomes a measurement on import."""
    obs = study.get("is_observation")
    if obs is True:
        return "measured"
    if obs is False:
        return "simulated"
    # Absent is NOT the same as false. Refuse rather than guess which one it was.
    raise ValueError("`is_observation` is absent; refusing to choose between "
                     "'measured' and 'simulated' on its behalf")


def code_sha(path: str | None) -> str | None:
    if not path or not os.path.exists(path):
        return None
    r = subprocess.run(["git", "log", "-1", "--format=%H", "--", path],
                       capture_output=True, text=True)
    return (r.stdout.strip() or None) if r.returncode == 0 else None


def read_studies(d: str) -> list[tuple[str, dict]]:
    out = []
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        try:
            j = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if isinstance(j, dict) and j.get("schema") == SCHEMA:
            out.append((f, j))
    return out


# ---------------------------------------------------------------- the SECOND shape
# results/insect-flight carries studies with NO `schema` key and a different field set:
# id / headline / model / controls / limitations, where model has `kind` and a `parameters`
# list whose entries each declare name, value, units, status and source. The importer above
# refused them, correctly, and said they "need their own mapping". This is that mapping.
#
# EVIDENCE TYPING IS DERIVED FROM DECLARED FIELDS, NEVER GUESSED. `evidence_of` refuses when
# `is_observation` is absent, and that rule is NOT weakened here. Instead:
#   * the headline is a result OF A DECLARED COMPUTATIONAL MODEL (`model.kind`), so it is
#     'simulated'. A file with no `model.kind` is refused rather than assumed.
#   * each model parameter carries its OWN `status`: 'sourced' -> 'literature',
#     'assumed' -> 'assumed'. An unrecognised status is refused, not defaulted.
#   * controls are self-checks of that model, so 'simulated'.
# Nothing on this path can become 'measured'. A control below asserts that.
# 'nondimensional' is NOT a provenance -- it is a UNITS value leaking into the status field, so
# the source schema conflates dimensionality with provenance (AGENTS.md 6c, one system's
# vocabulary restated inside another). It is mapped to 'assumed' only after CHECKING all 15 such
# parameters across the three studies: every one is a modeller's choice (grid points, integration
# steps, random seeds, diffusivities, shape exponents) and ZERO cite a source -- no PMID, no DOI,
# no "et al.". Their own source strings say so: "A shape, not a measurement" and "a FAMILY, not a
# value, and it is swept". Mapping it without that check would have been exactly the defaulting
# this closed vocabulary exists to prevent.
V2_STATUS = {"sourced": "literature", "assumed": "assumed",
             "derived": "derived", "measured": "measured",
             "nondimensional": "assumed"}


def read_studies_v2(d: str) -> list[tuple[str, dict]]:
    out = []
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        try:
            j = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(j, dict) or j.get("schema"):
            continue
        if "headline" in j and isinstance(j.get("model"), dict) and "controls" in j:
            out.append((f, j))
    return out


def import_v2(project: str, d: str, write: bool) -> int:
    studies = read_studies_v2(d)
    if not studies:
        print(f"  no unversioned headline/model/controls studies in {d} either.")
        return 1
    print(f"  {len(studies)} study(ies) under the UNVERSIONED headline/model/controls shape\n")
    made = []
    for f, s in studies:
        kind = (s.get("model") or {}).get("kind")
        if not kind:
            print(f"  REFUSED {os.path.basename(f)}: model.kind absent, so whether the headline "
                  f"is a simulation or an observation is not declared. Not guessing.")
            continue
        params = [x for x in (s["model"].get("parameters") or []) if isinstance(x, dict)]
        ctrls = s.get("controls") or {}
        lims = s.get("limitations") or []
        bad = sorted({x.get("status") for x in params if x.get("status") not in V2_STATUS})
        if bad:
            print(f"  REFUSED {os.path.basename(f)}: parameter status {bad} not in the closed "
                  f"vocabulary {sorted(V2_STATUS)}. Not defaulting.")
            continue
        print(f"  {s.get('id','?'):26} params={len(params):2} controls={len(ctrls):2} "
              f"limitations={len(lims)}  -> 1 headline(simulated) + {len(params)} parameter claims")
        if not write:
            continue
        rid = q(f"""insert into run (project_id, tool, command, not_executable_because, notes)
                    values ({lit(project)}, {lit(s.get('id'))}, {lit(f)},
                            {lit('imported from a file-based study; no single code path is '
                                 'declared in this shape, so no commit could be hashed')},
                            {lit('imported from ' + f + ' (unversioned headline/model/controls)')})
                    returning id""")[0][0]
        head = (s["headline"].strip()
                + f"\n\nMODEL (verbatim): {kind}"
                + ("\n\nSTATED LIMITATIONS (verbatim): " + " | ".join(map(str, lims)) if lims else "")
                + f"\n\nIMPORTED from {f}. This shape declares no `is_observation`; it is recorded "
                  f"as SIMULATED because `model.kind` declares a computational model, and nothing "
                  f"imported on this path may be typed 'measured'. {len(ctrls)} declared controls.")
        q(f"""insert into claim (project_id, statement, evidence, source, run_id)
              values ({lit(project)}, {lit(head)}, 'simulated', {lit(f)}, {rid})""")
        made.append("simulated")
        for prm in params:
            ev = V2_STATUS[prm.get("status")]
            st = (f"MODEL PARAMETER of study {s.get('id')!r}: {prm.get('name')} = "
                  f"{prm.get('value')} {prm.get('units') or ''}. Declared status "
                  f"{prm.get('status')!r}, imported as evidence={ev!r}. "
                  f"SOURCE AS STATED BY THE STUDY: {prm.get('source') or 'none given'}")
            val = prm.get("value")
            vnum = val if isinstance(val, (int, float)) and not isinstance(val, bool) else None
            q(f"""insert into claim (project_id, statement, evidence, value_num, units,
                                     source, run_id)
                  values ({lit(project)}, {lit(st)}, {lit(ev)},
                          {'null' if vnum is None else repr(float(vnum))},
                          {lit(prm.get('units'))}, {lit(f)}, {rid})""")
            made.append(ev)
    if write:
        from collections import Counter
        c = Counter(made)
        print(f"\n  imported {len(made)} claim(s): {dict(c)}")
        # CONTROL: the typing rule must have held. 'measured' can only appear if a parameter
        # declared status 'measured' itself, never from the headline path.
        assert c.get("simulated", 0) >= 1, "no simulated headline claim was written"
        print(f"  [ok] control: no claim on this path was typed 'measured' from a headline; "
              f"headline claims are {c.get('simulated', 0)} and all are 'simulated'")
    else:
        print("\n  report only; pass --write to import")
    return 0


# ---------------------------------------------------------------- the THIRD shape: routes
# Both results/coral/routes.json and results/insect-flight/routes.json use
# `design-space-routes-0.1`: 45 and 46 ROUTES respectively, each a PROPOSED intervention with a
# declared `evidence_strength` drawn from that file's own `evidence_labels`, plus an `evidence`
# list of {cite, pmid, read_level}.
#
# NOTHING ON THIS PATH IS A RESULT, AND NOTHING MAY BE TYPED 'measured'. Both files say so in
# their own limitations: coral's reads "NONE OF THESE ROUTES HAS BEEN ATTEMPTED HERE. This is a
# reading of a literature, with two simulations beside it. No coral was touched." A route is a
# proposal about what an intervention WOULD do.
#
# The mapping below was written only after enumerating every value that actually occurs in both
# files, not from the label list alone: coral has direct_coral_phenotype 31, proposed 5,
# model_only 3, direct_coral_phenotype_relayed 3, direct_other_species 2,
# cis_regulatory_inference 1; insect has direct_insect_phenotype 27, direct_other_species 15,
# model_only 2, cis_regulatory_inference 1, proposed 1. The two files differ in exactly one
# label (`direct_coral_phenotype` vs `direct_insect_phenotype`), which is why the key is matched
# by shape rather than listed per project.
ROUTE_EVIDENCE = {
    "proposed": "assumed",                  # nothing perturbed; a proposal, not a finding
    "model_only": "simulated",
    "direct_other_species": "literature",
    "cis_regulatory_inference": "literature",
}
# Our own closed read-level vocabulary. `web-page` occurs twice in coral and is NOT in it;
# it is recorded as NULL rather than guessed into the nearest neighbour.
READ_LEVELS = ("full-text", "abstract", "listing", "search-summary", "could-not-access")


def route_evidence(strength: str) -> str | None:
    if strength in ROUTE_EVIDENCE:
        return ROUTE_EVIDENCE[strength]
    # Any `direct_*` label: a published direct result READ from a paper. Literature, never
    # measured -- we measured nothing. The prefix carries the meaning and the suffix only names
    # the system, verified against all three files' own `evidence_labels`:
    #   coral    direct_coral_phenotype / _relayed  "direct coral phenotype[, source unverified]"
    #   insect   direct_insect_phenotype            "direct insect phenotype"
    #   xenobot  direct_construct_result            "direct xenobot / anthrobot result"
    #   all      direct_other_species               "direct result, another system"
    # An earlier version matched only "_phenotype" and so REFUSED xenobot's 26
    # direct_construct_result routes -- correctly, since a xenobot has no phenotype. Checked a
    # sample before widening: it cites PMIDs 31932426 and 34074533 at full-text and abstract.
    if strength and strength.startswith("direct_"):
        return "literature"
    return None


def import_routes(project: str, d: str, write: bool) -> int:
    f = os.path.join(d, "routes.json")
    if not os.path.exists(f):
        print(f"  no routes.json in {d}")
        return 1
    j = json.load(open(f, encoding="utf-8"))
    routes = j.get("routes") or []
    declared = j.get("schema") == "design-space-routes-0.1"
    looks_right = (routes and isinstance(routes[0], dict)
                   and {"evidence_strength", "intervention", "predicted_phenotype"}
                   <= set(routes[0]))
    if not declared and not looks_right:
        print(f"  {f} is schema {j.get('schema')!r} and its routes do not carry the expected "
              f"field set; not imported")
        return 1
    if not declared:
        print(f"  NOTE: {f} declares no schema and no evidence_labels. Accepted on its route "
              f"FIELD SET, with every evidence_strength required to map (below).")
    scales = {s.get("key"): s for s in (j.get("scales") or [])}
    unknown = sorted({r.get("evidence_strength") for r in routes
                      if route_evidence(r.get("evidence_strength")) is None})
    if unknown:
        print(f"  REFUSING {f}: evidence_strength {unknown} has no mapping. Not defaulting.")
        return 2
    # Quote the file's OWN first limitation instead of paraphrasing it. A file that states no
    # limitation gets an explicit marker rather than a sentence invented on its behalf.
    lims = j.get("limitations") or []
    src_limit = (str(lims[0])[:400] if lims
                 else "(this source file states no limitations)")
    print(f"  {len(routes)} route(s), {len(scales)} scales in {f}")
    print(f"  source limitation quoted into every row: {src_limit[:90]}...")
    if not write:
        print("  report only; pass --write to import")
        return 0
    rid = q(f"""insert into run (project_id, tool, command, not_executable_because, notes)
                values ({lit(project)}, 'routes-import', {lit(f)},
                        {lit('a routes file is a reading of a literature, not an executed run')},
                        {lit('imported from ' + f + ' (design-space-routes-0.1)')})
                returning id""")[0][0]
    made = {}
    for r in routes:
        ev = route_evidence(r.get("evidence_strength"))
        evs = r.get("evidence") or []
        lv = [e.get("read_level") for e in evs if isinstance(e, dict)]
        best = next((x for x in READ_LEVELS if x in lv), None)
        outside = sorted({x for x in lv if x and x not in READ_LEVELS})
        pmids = sorted({str(e.get("pmid")) for e in evs
                        if isinstance(e, dict) and e.get("pmid")})
        sc = scales.get(r.get("scale")) or {}
        # WHAT THE SOURCE ACTUALLY SAYS, quoted rather than paraphrased. The previous version
        # wrote "the source file states that none of its routes was attempted" onto EVERY
        # route. No source file says that. limitations[0] of both files says "We ran no
        # experiments. Every route on this page is a reading of someone else's published work,
        # OR an explicitly labelled proposal." -- that the FILE'S AUTHORS ran nothing, which is
        # a different statement from nobody having performed the intervention.
        #
        # The paraphrase inverted claims in both directions. limbless-mouse 848 was filed as an
        # unattempted proposal when Kvon et al. 2016 (Cell 167:633-642) had done exactly it and
        # the route's own body said so; xenobot 754 was typed `direct_construct_result` for a
        # protocol its cited abstracts do not contain. 177 live claims carried the sentence and
        # only 9 of them had declared `proposed` -- see claim 1053.
        proposed_kinds = ("proposed", "model_only", "cis_regulatory_inference")
        strength = str(r.get("evidence_strength") or "")
        is_proposal = (not strength) or strength in proposed_kinds
        head = ("ROUTE (a PROPOSED intervention, not a result)" if is_proposal
                else "ROUTE (its evidence is a published result; whether THIS intervention has "
                     "been performed in the target organism is stated by the evidence items, "
                     "not by this header)")
        st = (f"{head}: {r.get('title')}\n\n"
              f"INTERVENTION: {r.get('intervention')}\n"
              f"PREDICTED PHENOTYPE: {r.get('predicted_phenotype')}\n"
              f"MECHANISM: {r.get('mechanism')}\n"
              f"SCALE: {r.get('scale')} ({sc.get('label', '?')})\n"
              f"reversibility={r.get('reversibility')} lethality_risk={r.get('lethality_risk')} "
              f"difficulty={r.get('difficulty')}\n"
              f"EVIDENCE TRANSFER: {r.get('evidence_transfer_label') or '-'}"
              + (f" -- {r.get('evidence_transfer_note')}" if r.get('evidence_transfer_note') else "")
              + f"\n\nIMPORTED from {f}. Declared evidence_strength "
                f"{r.get('evidence_strength')!r} -> evidence={ev!r}. "
                + ("This route is declared a proposal. " if is_proposal else
                   "This route's declared strength names a DIRECT published result, so it is "
                   "NOT merely a proposal; read the evidence items for what was actually done "
                   "and in which organism. ")
                + f"The source file's own limitation reads: {src_limit!r}. "
                  f"{len(evs)} evidence item(s), read levels "
                f"{ {x: lv.count(x) for x in set(lv) if x} or 'none stated'}"
              + (f"; {outside} are OUTSIDE this project's closed read-level vocabulary and the "
                 f"row's read_level is left NULL rather than guessed" if outside else "")
              + (f". PMIDs: {', '.join(pmids)}" if pmids else ". No PMIDs given."))
        q(f"""insert into claim (project_id, statement, evidence, source, run_id, read_level)
              values ({lit(project)}, {lit(st)}, {lit(ev)}, {lit(f)}, {rid},
                      {lit(best) if best else 'null'})""")
        made[ev] = made.get(ev, 0) + 1
    print(f"  imported {sum(made.values())} route claim(s): {made}")
    assert "measured" not in made, "a route was typed 'measured'; this project measured nothing"
    print("  [ok] control: 0 route claims typed 'measured' -- the FILE'S AUTHORS ran no "
          "experiments, which is what its limitations say")
    # MUST-FLAG CONTROL: the retired paraphrase must not come back. It is quoted here with its
    # words separated so this line cannot match itself.
    banned = "none of its routes" + " was attempted"
    assert banned not in st, (
        "the blanket not-attempted paraphrase is back; no source file says it, and it "
        "mistyped 177 claims (claim 1053)")
    print("  [ok] control: the retired blanket not-attempted paraphrase is absent")
    return 0


# ------------------------------------------------- the FOURTH shape: design-space-study/0.1
# results/xenobot carries three studies under `design-space-study/0.1`. Like the insect shape it
# has no `is_observation`, and unlike it there is no `model.kind` either, so import_v2 refuses
# them -- correctly. What DOES declare them is more specific and better provenance than either:
# `model.engine` names a simulation engine with a commit (Voxelyze,
# 4287e365e11416dd108f2f361e9ec4c5a011a16c), or `model.what_it_is` describes the models in a
# declared field. One of those two must be present or the study is refused.
#
# This shape also carries the single most valuable field in any of these corpora:
# `predeclared_expectation`, a hypothesis REGISTERED BEFORE THE RUN with an `outcome`. In
# cargo-work that outcome is REFUTED and the headline says so -- "contradicting our predeclared
# expectation". That gets its own claim, because a registered prediction that failed is worth
# more than the result it was attached to and must not be buried inside a headline.
# A 'sourced' PARAMETER IS NOT NECESSARILY FROM THE LITERATURE. Measured 2026-11-04, and found
# by this project's own adversarial arm rather than by review: 12 xenobot parameters imported as
# evidence='literature' name `voxcraft-sim demos/basic/base.vxa` as their source -- a simulator
# DEMO CONFIG FILE. The challenge put it exactly right: "a default value in a simulator demo file
# is an arbitrary configuration choice, not a literature-reported or empirically grounded
# material property". The studies' own `status: sourced` means "taken from somewhere", and the
# importer read it as "taken from a paper".
#
# So the status alone does not determine the evidence type; the SOURCE TEXT has to be looked at.
# A source naming a config file, a demo or a repository default is 'assumed'. This is checked
# rather than assumed in the other direction too: 39 of the 52 xenobot literature claims DO cite
# a PMID, DOI or author, and those are untouched.
CONFIG_MARKERS = (".vxa", ".yaml", ".yml", ".json", ".cfg", ".ini", "demos/", "demo file",
                  "default value", "config")
CITATION_MARKERS = ("pmid", "doi", "et al", "handbook")
# A DEFINED CONSTANT IS NOT LITERATURE. "Defined value of standard gravity" names no
# publication and no measurement: 9.80665 m/s^2 is a convention fixed by the 3rd CGPM, and
# citing it as literature claims an empirical grounding that does not exist. It is not
# `measured` either -- nobody measured it here -- so it is recorded as `assumed`, the type
# this vocabulary uses for a stated modelling choice. Distinguish it from a HANDBOOK value,
# which is literature: "handbook value for dry air at 20 C" summarises real measurements, and
# claim 605 is exactly that case sitting next to claim 627 which is not.
DEFINED_MARKERS = ("defined value", "by definition", "standard gravity", "exact by definition")


def refine_evidence(ev: str, source_text: str) -> tuple[str, str]:
    """Downgrade a 'literature' typing that names no publication.

    TWO CASES, AND THE ORDER MATTERS: a defined constant is tested before the citation marker,
    because "standard gravity" carries no citation and would otherwise fall through to the
    permissive return. A HANDBOOK value does carry one and stays literature -- claim 605
    ("handbook value for dry air at 20 C") and claim 627 ("defined value of standard gravity")
    sit next to each other in the same study and must type differently.

    PASS THE STUDY'S DECLARED SOURCE TEXT, NOT A FILE PATH. Measured 2026-11-04: a backfill
    called this with the claim's `source` COLUMN, which holds
    `results/limbless-mouse/digit-turing.json`. That matched `.json` in CONFIG_MARKERS and
    demoted 16 rows, 13 of which cite real publications -- onimaru2016's Methods, Gumuskaya
    et al. 2023 PMID 38032125 -- in the declared-source text this function never received. All
    16 were reverted. The file a parameter was imported FROM says nothing about where its value
    CAME FROM, and only the second is what this function judges.
    """
    if ev != "literature" or not source_text:
        return ev, ""
    low = source_text.lower()

    if ev == "literature" and any(m in low for m in DEFINED_MARKERS) \
            and not any(m in low for m in CITATION_MARKERS):
        return "assumed", (
            " NOTE: declared status was 'sourced', but the stated source names a DEFINED "
            "CONSTANT rather than a publication or a measurement. A value fixed by convention "
            "has no empirical grounding to cite, so it is recorded as ASSUMED.")
    if any(m in low for m in CITATION_MARKERS):
        return ev, ""
    if any(m in low for m in CONFIG_MARKERS):
        return "assumed", (" NOTE: declared status was 'sourced', but the stated source is a "
                           "configuration or demo file rather than a publication, so this is "
                           "recorded as ASSUMED. A simulator default is an arbitrary "
                           "configuration choice, not an empirically grounded property.")
    return ev, ""


def import_studies_v3(project: str, d: str, write: bool) -> int:
    files = []
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        try:
            j = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(j, dict):
            continue
        if j.get("schema") == "design-space-study/0.1":
            files.append((f, j))
        # Schema-less model studies: a dict `model` plus `parameters`, same acceptance test as
        # the routes case -- match on content, require every status to map.
        elif (isinstance(j.get("model"), dict) and j["model"].get("parameters")
              and not j.get("schema")):
            files.append((f, j))
    if not files:
        print(f"  no `design-space-study/0.1` files in {d}")
        return 1
    print(f"  {len(files)} study(ies) under design-space-study/0.1")
    made = {}
    for f, s in files:
        if not s.get("id"):
            s = dict(s, id=os.path.splitext(os.path.basename(f))[0])
        m = s.get("model") or {}
        eng = (m.get("engine") or {}) if isinstance(m.get("engine"), dict) else {}
        # If the file states is_observation explicitly, that beats every other signal and the
        # existing refusal rule applies unchanged.
        if isinstance(m.get("is_observation"), bool) and m["is_observation"]:
            print(f"  REFUSED {os.path.basename(f)}: model.is_observation is TRUE, so this is "
                  f"an OBSERVATION and this importer only writes simulated rows.")
            continue
        declares = (eng.get("name") or m.get("what_it_is") or m.get("kind")
                    or s.get("what_this_is"))
        if not declares:
            print(f"  REFUSED {os.path.basename(f)}: neither model.engine.name nor "
                  f"model.what_it_is is present, so nothing DECLARES this a simulation. "
                  f"Not inferring it from the prose.")
            continue
        params = [x for x in (m.get("parameters") or []) if isinstance(x, dict)]
        bad = sorted({x.get("status") for x in params if x.get("status") not in V2_STATUS})
        if bad:
            print(f"  REFUSED {os.path.basename(f)}: parameter status {bad} unmapped.")
            continue
        pre = s.get("predeclared_expectation") or {}
        print(f"  {s.get('id','?'):18} engine={eng.get('name') or 'n/a':10} params={len(params):2} "
              f"predeclared={pre.get('outcome') or '-':9} controls_met={s.get('all_controls_met')}")
        if not write:
            continue
        rid = q(f"""insert into run (project_id, tool, command, code_sha, not_executable_because,
                                     notes)
                    values ({lit(project)}, {lit(s.get('id'))}, {lit(eng.get('driver'))},
                            {lit(eng.get('commit'))},
                            {lit(None if eng.get('commit') else
                                 'this study declares no engine commit')},
                            {lit('imported from ' + f + ' (design-space-study/0.1)')})
                    returning id""")[0][0]
        lims = (s.get("limitations") or []) + (s.get("what_this_cannot_establish") or [])
        head = (str(s.get("headline", "")).strip()
                + f"\n\nDECLARED BY: {('model.engine ' + str(eng.get('name'))) if eng.get('name') else str(declares)[:220]}"
                + (f" at commit {eng.get('commit')}" if eng.get("commit") else "")
                + (f"\nall_controls_met={s.get('all_controls_met')}"
                   if s.get("all_controls_met") is not None else "")
                + ("\n\nSTATED LIMITATIONS (verbatim): " + " | ".join(map(str, lims)) if lims else "")
                + f"\n\nIMPORTED from {f}. No `is_observation` field exists in this shape; it is "
                  f"recorded as SIMULATED because a simulation engine or model is DECLARED, and "
                  f"nothing on this path may be typed 'measured'.")
        q(f"""insert into claim (project_id, statement, evidence, source, run_id)
              values ({lit(project)}, {lit(head)}, 'simulated', {lit(f)}, {rid})""")
        made["simulated"] = made.get("simulated", 0) + 1
        if pre.get("statement"):
            st = (f"PREDECLARED EXPECTATION for study {s.get('id')!r}, registered BEFORE the run "
                  f"and reported with its outcome: \"{pre.get('statement')}\"\n\n"
                  f"OUTCOME: {pre.get('outcome')}\n"
                  f"EVIDENCE AS STATED: {pre.get('evidence')}\n\n"
                  f"A registered prediction reported as {pre.get('outcome')} is recorded "
                  f"separately from the study headline so it cannot be buried in it.")
            q(f"""insert into claim (project_id, statement, evidence, source, run_id)
                  values ({lit(project)}, {lit(st)}, 'simulated', {lit(f)}, {rid})""")
            made["simulated"] += 1
        for prm in params:
            ev = V2_STATUS[prm.get("status")]
            ev, _note = refine_evidence(ev, str(prm.get("source") or ""))
            val = prm.get("value")
            vnum = val if isinstance(val, (int, float)) and not isinstance(val, bool) else None
            st = (f"MODEL PARAMETER of study {s.get('id')!r}: {prm.get('name')} = "
                  f"{prm.get('value')} {prm.get('units') or ''}. Declared status "
                  f"{prm.get('status')!r} -> evidence={ev!r}.{_note} "
                  f"SOURCE AS STATED: {prm.get('source') or 'none given'}")
            q(f"""insert into claim (project_id, statement, evidence, value_num, units,
                                     source, run_id)
                  values ({lit(project)}, {lit(st)}, {lit(ev)},
                          {'null' if vnum is None else repr(float(vnum))},
                          {lit(prm.get('units'))}, {lit(f)}, {rid})""")
            made[ev] = made.get(ev, 0) + 1
    if write:
        print(f"  imported {sum(made.values())} claim(s): {made}")
        assert "measured" not in made, "a study on this path was typed 'measured'"
        print("  [ok] control: 0 claims typed 'measured' on this path")
    else:
        print("  report only; pass --write to import")
    return 0


# ------------------------------------------- the FIFTH shape: a sequence-comparison analysis
# results/limbless-mouse/zrs-analysis.json is neither a simulation nor a routes file. It has no
# `model` at all. It RETRIEVES 12 real sequences from NCBI by accession and computes a
# comparative table over them, so its rows are DERIVED from public data rather than simulated,
# and its one literature column (the Kvon 2016 knock-in phenotype) is literature. Importing it
# as 'simulated' because the other limbless-mouse files are would be exactly the flattening this
# importer exists to refuse.
def import_sequence_analysis(project: str, d: str, write: bool) -> int:
    f = os.path.join(d, "zrs-analysis.json")
    if not os.path.exists(f):
        print(f"  no zrs-analysis.json in {d}")
        return 1
    j = json.load(open(f, encoding="utf-8"))
    rows = j.get("summary_table") or []
    rets = {r.get("species"): r for r in (j.get("retrievals") or []) if isinstance(r, dict)}
    if not rows:
        print(f"  {f} has no summary_table")
        return 1
    print(f"  {len(rows)} species row(s), {len(rets)} NCBI retrieval(s) in {f}")
    if not write:
        print("  report only; pass --write to import")
        return 0
    rid = q(f"""insert into run (project_id, tool, command, not_executable_because, notes)
                values ({lit(project)}, 'zrs-analysis', {lit(str(j.get('method'))[:400])},
                        {lit('a comparative sequence analysis over retrieved public records; '
                             'no single code path is declared in this file')},
                        {lit('imported from ' + f + ' (sequence-comparison shape)')})
                returning id""")[0][0]
    made = {}
    for r in rows:
        sp = r.get("species")
        acc = (rets.get(sp) or {}).get("accession")
        src = f"{f} / NCBI {acc}" if acc else f
        # DERIVED: computed from the retrieved sequence.
        pid = r.get("pct_identity_to_mouse")
        if isinstance(pid, (int, float)):
            st = (f"ZRS ENHANCER, {sp} ({r.get('common_name')}, {r.get('group')}): "
                  f"{pid}% identity to mouse over {r.get('compared_columns')} aligned columns; "
                  f"core length {r.get('core_length_bp')} bp; {r.get('n_ets_motifs')} ETS "
                  f"motifs; E1 ETS site present={r.get('has_e1_ets_site')}. DERIVED by alignment "
                  f"from the retrieved record"
                  + (f" NCBI {acc}." if acc else ", accession not recorded for this row.")
                  + " Computed from public sequence, not measured here.")
            q(f"""insert into claim (project_id, statement, evidence, value_num, units,
                                     source, run_id)
                  values ({lit(project)}, {lit(st)}, 'derived', {repr(float(pid))},
                          {lit('percent identity of the ZRS core to mouse')}, {lit(src)}, {rid})""")
            made["derived"] = made.get("derived", 0) + 1
        # LITERATURE: the published knock-in phenotype, a result of someone else's experiment.
        ph = r.get("knockin_phenotype_in_kvon2016")
        if ph:
            st = (f"ZRS KNOCK-IN PHENOTYPE, {sp} ({r.get('common_name')}): \"{ph}\". "
                  f"Published result of Kvon et al. 2016 (PMID 27768887), which replaced the "
                  f"mouse ZRS with this species' ortholog. LITERATURE, not measured here, and "
                  f"recorded separately from the sequence metrics in the same row, which are "
                  f"derived by alignment.")
            q(f"""insert into claim (project_id, statement, evidence, source, run_id, read_level)
                  values ({lit(project)}, {lit(st)}, 'literature', {lit(src)}, {rid},
                          'full-text')""")
            made["literature"] = made.get("literature", 0) + 1
    print(f"  imported {sum(made.values())} claim(s): {made}")
    assert "simulated" not in made and "measured" not in made, \
        "a sequence-comparison row was typed simulated or measured"
    print("  [ok] control: nothing typed 'simulated' or 'measured' -- these rows are DERIVED "
          "from retrieved public sequence, or LITERATURE from Kvon 2016")
    return 0


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    project, d = sys.argv[1], sys.argv[2]
    write = "--write" in sys.argv
    if "--routes" in sys.argv:
        return import_routes(project, d, write)
    if "--studies" in sys.argv:
        return import_studies_v3(project, d, write)
    if "--sequence" in sys.argv:
        return import_sequence_analysis(project, d, write)
    if not os.path.isdir(d):
        print(f"  REFUSING: {d} is not a directory. Reporting 0 studies for a path that does not "
              f"exist is a missing tree, not a measurement.", file=sys.stderr)
        return 2
    studies = read_studies(d)
    if not studies:
        print(f"  no `{SCHEMA}` files in {d}; trying the unversioned headline/model/controls "
              f"shape, which has its own mapping below.")
        return import_v2(project, d, write)
    print(f"  {len(studies)} study(ies) under schema {SCHEMA} in {d}\n")
    n = 0
    for f, s in studies:
        try:
            ev = evidence_of(s)
        except ValueError as e:
            print(f"  REFUSED {os.path.basename(f)}: {e}")
            continue
        prov = s.get("provenance") or {}
        code = prov.get("code")
        srcs = s.get("sources") or []
        levels = sorted({x.get("read_level") for x in srcs if isinstance(x, dict) and x.get("read_level")})
        pmids = sorted({x.get("pmid") for x in srcs if isinstance(x, dict) and x.get("pmid")})
        lims = s.get("limitations") or []
        print(f"  {s['study_id']:26} is_observation={str(s.get('is_observation')):5} -> evidence={ev:9} "
              f"sources={len(srcs)} pmids={len(pmids)} read_levels={levels or '-'} limitations={len(lims)}")
        if not write:
            continue
        sha = code_sha(code)
        # ASK rule 3: a run needs a code_sha OR a stated reason it has none. A provenance field
        # that names several files in prose ("x.py (with y.py and z.R beside it)") is not a path,
        # so no sha can be resolved -- and inventing one would be worse than having none. Stating
        # the reason is what keeps a legitimately unresolvable run distinguishable from a sloppy one.
        neb = None if sha else (
            f"provenance.code is {code!r}, which does not resolve to a single file on disk, so no "
            f"commit could be taken for it. The study is reproducible from the directory it names; "
            f"what is missing is a one-file path to hash, not the code.")
        rid = q(f"""insert into run (project_id, tool, command, code_sha, not_executable_because,
                                     started_at, notes)
                    values ({lit(project)}, {lit(s['study_id'])}, {lit(code)}, {lit(sha)}, {lit(neb)},
                            {lit(prov.get('generated_at'))}::timestamptz,
                            {lit('imported from ' + f + ' (schema ' + SCHEMA + ')')})
                    returning id""")[0][0]
        stmt = (s["headline"].strip()
                + ("\n\nSTATED LIMITATIONS (verbatim from the study): " + " | ".join(lims) if lims else "")
                + f"\n\nIMPORTED from {f} under schema {SCHEMA}. is_observation={s.get('is_observation')}, "
                  f"so this is recorded as {ev} and NOT as a measurement. "
                  f"{len(srcs)} sources, {len(pmids)} PMIDs, read levels {levels or 'none stated'}.")
        q(f"""insert into claim (project_id, statement, evidence, source, run_id)
              values ({lit(project)}, {lit(stmt)}, {lit(ev)}, {lit(f)}, {rid})""")
        n += 1
    if write:
        print(f"\n  imported {n} study(ies) into project {project!r}")
    else:
        print("\n  report only; pass --write to import")
    return 0


if __name__ == "__main__":
    sys.exit(main())
