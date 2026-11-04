#!/usr/bin/env python3
"""Generate work so the frontier cannot run dry.

The monitor could only CONSUME a fixed list of subproblems. With 19 of them it ran dry in five
hours and then polled an empty queue while ~$928 of credit expired. A swarm that only consumes a
frontier is not a swarm; it is a batch job with a cron.

Four generators, in descending order of what they are worth:
  1. CHALLENGE   -- every unchallenged claim gets an adversary. Adopted first in the patterns doc
                    because an unchallenged assertion is worth little, and we have 31 claims and
                    3 challenges.
  2. REPLICATE   -- every DERIVED number gets an independent re-derivation by an agent that is not
                    shown the original. This is the cheapest hallucination detector there is.
  3. LAW         -- fill the law library from a named list. Each entry is bounded, checkable by
                    check_laws.py, and useful whether or not the fish works.
  4. DEEPEN      -- each answered subproblem's "what would change this" becomes a new subproblem.
"""
import json, os, subprocess, sys, textwrap
sys.path.insert(0, "/data/swarm")
from swarm import q, sql_lit, HONESTY, accounts_with_credit, dispatch  # noqa: E402

PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")
WORKDIR = "/data/worktrees/delphi-frontier/foundation"

LAWS = [
    ("strouhal", "Strouhal number and the 0.2-0.4 cruising band measured across swimming and flying animals"),
    ("wing-loading", "Wing loading versus body mass scaling, and the measured ceiling on powered flight"),
    ("elastic-similarity", "Elastic versus geometric similarity (McMahon) and buckling-limited scaling"),
    ("second-moment", "Second moment of area for a spar, and how bending stiffness scales with span"),
    ("kleiber", "Kleiber's law, entered WITH the 2/3 versus 3/4 controversy intact and unreconciled"),
    ("pennycuick-power", "The Pennycuick flight power curve and its U-shape"),
    ("cost-of-transport", "Cost of transport versus body mass across swimming, flying and running"),
    ("turing-conditions", "Turing's conditions for diffusion-driven instability, and when real tissue meets them"),
    ("hagen-poiseuille", "Hagen-Poiseuille flow and the r^-4 dissipation that Murray's law rests on"),
    ("froude-efficiency", "Froude propulsive efficiency and the Froude number for a surface-piercing body"),
    ("lighthill-ebt", "Lighthill elongated-body theory for undulatory swimming thrust"),
    ("von-bertalanffy", "Von Bertalanffy growth, and where it fails for indeterminate growers"),
    ("wolff", "Wolff's law of bone remodelling, and what is actually measured versus asserted"),
    ("allometry-huxley", "Huxley allometry y = a x^b: what the exponent means and how it is estimated"),
    ("weis-fogh", "Weis-Fogh clap and fling, and the measured lift augmentation at low Reynolds number"),
    ("reynolds-stokes", "The Stokes regime boundary and what changes below Re ~1"),
    ("mcmahon-elastic", "McMahon elastic similarity for limb and spar proportions"),
    ("euler-buckling", "Euler buckling of a slender column, and the slenderness ratio where it governs"),
    ("gompertz", "Gompertz growth and where it departs from von Bertalanffy"),
    ("surface-area-volume", "The surface-area-to-volume scaling constraint and its consequences for exchange"),
    ("fick-diffusion", "Fick diffusion and the length scale beyond which diffusive supply fails"),
    ("hill-muscle", "The Hill force-velocity relation for muscle, and its measured parameters"),
    ("muscle-power-density", "Maximum mass-specific mechanical power of vertebrate muscle, by fibre type"),
    ("bone-safety-factor", "Measured safety factors in vertebrate skeletal elements"),
    ("phyllotaxis", "Phyllotaxis and the golden divergence angle: what is explained and what is not"),
    ("fractal-branching", "Fractal dimension of branching structures in corals and trees"),
    ("adder-cell-size", "The adder model of cell-size homeostasis"),
    ("lift-coefficient-lowre", "Measured maximum lift coefficient for thin plates at Re 1e3-1e4"),
    ("induced-drag", "Induced drag and why aspect ratio dominates glide ratio"),
    ("glide-ratio", "Glide ratio as lift-to-drag, and the sink-rate relation"),
    ("takeoff-stall-speed", "Stall speed from wing loading, and its sensitivity to CL_max"),
]


def unchallenged_claims(limit=12):
    return q(f"""select c.id, c.statement, c.evidence, coalesce(c.value_num::text,'n/a'), coalesce(c.units,''),
                        coalesce(c.source,'')
                 from claim c where c.project_id={sql_lit(PROJECT)} and c.superseded_by is null
                 and not exists (select 1 from challenge ch where ch.claim_id=c.id)
                 order by c.id limit {limit}""")


def underived_claims(limit=8):
    """Derived numbers nobody has re-derived. The agent is given the INPUTS, never the answer."""
    return q(f"""select c.id, c.statement, coalesce(c.source,'')
                 from claim c where c.project_id={sql_lit(PROJECT)} and c.evidence='derived'
                 and c.superseded_by is null
                 and not exists (select 1 from challenge ch where ch.claim_id=c.id
                                 and ch.attack like 'independent re-derivation%')
                 order by c.id limit {limit}""")


def gen_challenges(accts, i=0):
    n = 0
    for cid, st, ev, val, un, src in unchallenged_claims():
        acct = accts[i % len(accts)][0]; i += 1
        prompt = textwrap.dedent(f"""
            ADVERSARIAL REVIEW of a claim you did not write. Try hard to break it.

            CLAIM: "{st}"
            recorded evidence level: {ev}   value: {val} {un}
            source: {src}

            1. Redo any arithmetic INDEPENDENTLY from the stated inputs. Do not copy the author's working.
            2. Is a PROXY standing in for the quantity that matters? Name it and find the right one.
            3. What hidden assumption carries the result? Test it relaxed.
            4. Is the EVIDENCE LEVEL honest? A derived number presented as measured is a defect even
               when the number is right.
            5. Is there a regime, taxon or published counter-example the author missed?

            {HONESTY}

            If after genuinely trying you cannot break it, say SURVIVED and give your reasoning. A
            manufactured fault is worse than none, because it will be believed. Your value is the
            honest verdict, not the body count.

            Write docs/research/fish/challenge-{cid}.md on a new branch and commit, ending with:
            ```swarm-challenge
            {{"claim_id": {cid}, "outcome": "survived|refuted|weakened", "reason": "<one sentence>",
              "corrected_value": "<value with units, or null>"}}
            ```
        """).strip()
        r = subprocess.run(["orchestra","cloud","start","--account",acct,"--dir",WORKDIR,"--prompt",prompt],
                           capture_output=True, text=True, timeout=300)
        try: d = json.loads(r.stdout)
        except Exception: print(f"  challenge {cid} failed on {acct}"); continue
        q(f"""insert into challenge (claim_id, challenger, attack, outcome)
              values ({cid}, {sql_lit(d['session_id'])}, 'adversarial cloud review', 'not-run')""")
        q(f"""insert into agent_session (id, project_id, harness, account, status)
              values ({sql_lit(d['session_id'])}, {sql_lit(PROJECT)}, 'cloud', {sql_lit(acct)}, 'running')
              on conflict (id) do nothing""")
        print(f"  challenge  claim {cid:>3}  {acct}"); n += 1
    return n, i


def gen_replications(accts, i=0):
    n = 0
    for cid, st, src in underived_claims():
        acct = accts[i % len(accts)][0]; i += 1
        prompt = textwrap.dedent(f"""
            INDEPENDENT RE-DERIVATION. You are NOT being shown the answer, deliberately.

            Someone derived a number for this question. Your job is to derive it yourself, from
            primary sources, WITHOUT looking for their result. If you encounter their working in the
            repository, stop reading it and say so.

            THE QUESTION, with the answer removed: {st.split(':')[0] if ':' in st else st[:160]}
            Context for where the inputs live: {src}

            {HONESTY}

            Report: your value with its uncertainty, every input with its source and read-level, and
            the arithmetic in full. Then and only then, compare with the recorded value if you can
            find it, and state whether you AGREE, DISAGREE or CANNOT TELL.

            Two independent derivations agreeing is evidence. One agent agreeing with itself is not.

            Write docs/research/fish/replicate-{cid}.md on a new branch and commit, ending with:
            ```swarm-replication
            {{"claim_id": {cid}, "my_value": "<value with units>", "agrees": true|false|null,
              "note": "<one sentence>"}}
            ```
        """).strip()
        r = subprocess.run(["orchestra","cloud","start","--account",acct,"--dir",WORKDIR,"--prompt",prompt],
                           capture_output=True, text=True, timeout=300)
        try: d = json.loads(r.stdout)
        except Exception: print(f"  replicate {cid} failed"); continue
        q(f"""insert into challenge (claim_id, challenger, attack, outcome)
              values ({cid}, {sql_lit(d['session_id'])}, 'independent re-derivation', 'not-run')""")
        q(f"""insert into agent_session (id, project_id, harness, account, status)
              values ({sql_lit(d['session_id'])}, {sql_lit(PROJECT)}, 'cloud', {sql_lit(acct)}, 'running')
              on conflict (id) do nothing""")
        print(f"  replicate  claim {cid:>3}  {acct}"); n += 1
    return n, i


def gen_laws(accts, i=0, limit=8):
    done = {r[0] for r in q("select distinct coalesce(statement,'') from claim where statement like 'LAWENTRY %'")}
    n = 0
    for slug, desc in LAWS:
        if n >= limit: break
        marker = f"LAWENTRY {slug}"
        if any(marker in d for d in done): continue
        acct = accts[i % len(accts)][0]; i += 1
        prompt = textwrap.dedent(f"""
            Write ONE law-library entry: {desc}

            Read `library/laws/reynolds.yaml` and `library/laws/murray.yaml` first -- they are the
            template and the standard. Write `library/laws/{slug}.yaml` in exactly that schema and
            commit it on a new branch.

            MANDATORY fields, and the build REJECTS an entry missing any of them:
              id, name, usability (constraining|descriptive), equation, latex, symbols (each with
              dimension, units, description), constants (value AND interval where measured),
              mechanism, domain_of_validity, where_it_breaks, worked_examples, sources (each with a
              read_level).

            TWO FIELDS CARRY MOST OF THE VALUE:
            - `where_it_breaks`: the regime, taxon or scale where the law DEMONSTRABLY FAILS. Every
              textbook gives the law; almost none gives the failure boundary, and the boundary is the
              only part an engineer needs. An entry without it is rejected.
            - `usability`: `constraining` if it yields a number a design can be checked against,
              `descriptive` if it only describes a pattern. Be honest; most laws are descriptive.

            DIMENSIONS MUST BALANCE. `python3 library/tools/check_laws.py` dimension-checks your
            equation against your declared symbols and fails the build if it does not balance. Run it
            before committing. Quote any value containing a comma -- a YAML flow mapping splits on
            commas and silently makes a junk key.

            If the law is CONTESTED, record the disagreement in `contested_by` and do not reconcile it.

            {HONESTY}
        """).strip()
        r = subprocess.run(["orchestra","cloud","start","--account",acct,"--dir",WORKDIR,"--prompt",prompt],
                           capture_output=True, text=True, timeout=300)
        try: d = json.loads(r.stdout)
        except Exception: print(f"  law {slug} failed"); continue
        q(f"""insert into claim (project_id, statement, evidence, source)
              values ({sql_lit(PROJECT)}, {sql_lit(marker+' dispatched')}, 'unknown', {sql_lit(d['session_id'])})""")
        q(f"""insert into agent_session (id, project_id, harness, account, status)
              values ({sql_lit(d['session_id'])}, {sql_lit(PROJECT)}, 'cloud', {sql_lit(acct)}, 'running')
              on conflict (id) do nothing""")
        print(f"  law        {slug:<20} {acct}"); n += 1
    return n, i


def gen_deepen(accts, i=0, limit=10):
    """Turn each answered subproblem's weakest input into its own new subproblem.

    Documented in this module's own docstring from the start and never implemented, which is why the
    queue ran dry a second time. An answered question is not a finished one: every answer rests on an
    input that could move, and that input is the next question.
    """
    rows = q(f"""select sp.id, sp.question, coalesce(sp.answer,''), sp.scale_id
                 from subproblem sp where sp.project_id={sql_lit(PROJECT)}
                 and sp.status in ('answered','refuted')
                 and not exists (select 1 from subproblem d where d.id = sp.id || '-D')
                 order by sp.id limit {limit}""")
    n = 0
    for sid, question, answer, scale in rows:
        acct = accts[i % len(accts)][0]; i += 1
        prompt = textwrap.dedent(f"""
            DEEPEN an answered subproblem by attacking its weakest input.

            {sid} ({scale}) asked: {question}
            The recorded answer: {answer}

            An answered question is not a finished one. Every answer rests on an input that could
            move, and that input is the next question.

            1. Identify the single input the answer is MOST SENSITIVE to -- the number that, if it
               were wrong by a factor of two, would change the conclusion. Show the sensitivity by
               recomputing, not by asserting it.
            2. How well is that input actually established? Give its evidence level and read-level
               honestly. Is it measured, a proxy for something else, or an assumption that has been
               repeated until it reads as measured?
            3. GO AND IMPROVE IT. Find the primary source. If the number is a proxy, find the real
               quantity. If it is unmeasured, say what measurement would settle it and what it would
               cost.
            4. Recompute the original conclusion with your improved input and state whether it
               STANDS, STRENGTHENS or FALLS.

            {HONESTY}

            Write docs/research/fish/{sid}-deepen.md on a new branch and commit, ending with:
            ```swarm-result
            {{"subproblem": "{sid}-D", "evidence": "<level>", "answer": "<one sentence>",
              "key_number": "<the improved input, with units>", "verdict": "stands|strengthens|falls"}}
            ```
        """).strip()
        r = subprocess.run(["orchestra","cloud","start","--account",acct,"--dir",WORKDIR,"--prompt",prompt],
                           capture_output=True, text=True, timeout=300)
        try: d = json.loads(r.stdout)
        except Exception: print(f"  deepen {sid} failed"); continue
        q(f"""insert into subproblem (id, project_id, scale_id, question, acceptance, status)
              values ({sql_lit(sid+'-D')}, {sql_lit(PROJECT)}, {sql_lit(scale)},
                      {sql_lit('Deepen '+sid+': attack its most sensitive input')},
                      {sql_lit('The sensitive input is improved from a primary source and the conclusion recomputed')},
                      'running') on conflict (id) do nothing""")
        q(f"""insert into agent_session (id, project_id, subproblem_id, harness, account, status)
              values ({sql_lit(d['session_id'])}, {sql_lit(PROJECT)}, {sql_lit(sid+'-D')}, 'cloud',
                      {sql_lit(acct)}, 'running') on conflict (id) do nothing""")
        print(f"  deepen     {sid:>5}  {acct}"); n += 1
    return n, i


if __name__ == "__main__":
    accts = accounts_with_credit()
    if not accts:
        sys.exit("no account has unexpired cloud credit")
    want = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    running = int(q(f"""select count(*) from agent_session where project_id={sql_lit(PROJECT)}
                        and status in ('running','working')""")[0][0])
    print(f"running={running} target={want}")
    i = 0
    total = 0
    if running + total < want:
        n, i = gen_challenges(accts, i); total += n
    if running + total < want:
        n, i = gen_replications(accts, i); total += n
    if running + total < want:
        n, i = gen_laws(accts, i, limit=want - running - total); total += n
    if running + total < want:
        n, i = gen_deepen(accts, i, limit=want - running - total); total += n
    print(f"dispatched {total}")
