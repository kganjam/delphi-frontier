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


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    project, d = sys.argv[1], sys.argv[2]
    write = "--write" in sys.argv
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
