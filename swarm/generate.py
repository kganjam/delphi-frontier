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
  5. ENTAIL      -- each claim is propagated to its neighbouring scales, and the requirements it
                    makes there are written down and CHECKED. The only generator that can refute a
                    claim from below, using a measurement instead of a simulation.
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


def unchallenged_claims(limit=30):
    return q(f"""select c.id, c.statement, c.evidence, coalesce(c.value_num::text,'n/a'), coalesce(c.units,''),
                        coalesce(c.source,'')
                 from claim c where c.project_id={sql_lit(PROJECT)} and c.superseded_by is null
                 and not exists (select 1 from challenge ch where ch.claim_id=c.id)
                 and c.statement not like 'LAWENTRY %'
                 order by c.id limit {limit}""")


def underived_claims(limit=8):
    """Derived numbers nobody has re-derived. The agent is given the INPUTS, never the answer."""
    return q(f"""select c.id, c.statement, coalesce(c.source,'')
                 from claim c where c.project_id={sql_lit(PROJECT)} and c.evidence='derived'
                 and c.superseded_by is null
                 and not exists (select 1 from challenge ch where ch.claim_id=c.id
                                 and ch.attack like 'independent re-derivation%')
                 and c.statement not like 'LAWENTRY %'
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
              "corrected_value": "<value with units, or null>",
              "depends_on": ["<each input YOUR verdict rests on>"]}}
            ```

            `depends_on` is required. A verdict rests on inputs exactly as the claim it judges does,
            and when one of those is later refuted your verdict must be flagged too.
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
    # GROUND TRUTH IS THE FILESYSTEM. Two earlier versions of this check were wrong in the same
    # direction -- they asked the database what had been dispatched, and re-dispatched laws that
    # already existed as entries. strouhal, wing-loading and elastic-similarity were each sent out
    # again while sitting in library/laws/. An entry that exists is done, whatever any ledger says.
    import glob as _glob
    existing = {os.path.basename(f)[:-5] for f in
                _glob.glob("/data/worktrees/delphi-frontier/swarm-arch/library/laws/*.yaml")}
    existing |= {r[0] for r in q("select ref from work_log where kind='dispatched'")}
    n = 0
    for slug, desc in LAWS:
        if n >= limit: break
        # Name-tolerant match. The LAWS slugs and the on-disk filenames drifted apart --
        # `pennycuick-power` vs `pennycuick`, `hagen-poiseuille` vs `poiseuille`,
        # `turing-conditions` vs `turing` -- so an exact check would have re-dispatched four laws
        # that exist, landing DUPLICATE entries under different names. A duplicate law is worse
        # than a missing one: two entries can disagree and neither knows about the other.
        tokens = set(slug.split("-"))
        if slug in existing or any(tokens & set(e.split("-")) for e in existing): continue
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
        q(f"""insert into work_log (project_id, kind, ref, detail)
              values ({sql_lit(PROJECT)},'dispatched',{sql_lit(slug)},{sql_lit(d['session_id'])})
              on conflict do nothing""")
        # Dispatch bookkeeping does NOT go in `claim`. It did, and the consequence was not cosmetic:
        # unchallenged_claims() picked the markers up as claims, so the swarm spent 31 adversarial
        # sessions attacking strings like "LAWENTRY strouhal dispatched". agent_session already
        # records every dispatch; the marker was pure duplication with a cost.
        pass
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
    # DEPTH CAP, SET AT 2 ON EVIDENCE RATHER THAN AT 1 ON INTUITION.
    # Unbounded, this deepens its own deepenings: S21-D-D-D existed within the hour. The first cap
    # was depth 1, on the assumption that deeper levels are thin. Harvesting then showed two
    # depth-2 results that are NOT thin: S23-D-D found that a conclusion was sensitive to E0 only
    # because f=1 silently assumed actinotrichia span the whole fin, when in adult zebrafish they
    # occupy only the distal 200-300 um of a ray; and S7-D-D measured a bending section from
    # published uCT imagery. Both are real corrections that depth 1 would never have reached.
    # So the cap is 2: deep enough for an assumption buried under an answer, shallow enough that
    # S21-D-D-D cannot recur.
    rows = q(f"""select sp.id, sp.question, coalesce(sp.answer,''), sp.scale_id
                 from subproblem sp where sp.project_id={sql_lit(PROJECT)}
                 and sp.status in ('answered','refuted')
                 and sp.id not like '%-D-D%'
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
              "key_number": "<the improved input, with units>", "verdict": "stands|strengthens|falls",
              "read_level": "full-text|abstract|listing|search-summary|could-not-access",
              "depends_on": ["<each input your conclusion rests on: a law id, a claim, a measured value>"]}}
            ```

            `read_level` is how you READ the source, and it is required when your evidence is
            `literature`. Listing a paper is not reading it and a search summary is a lead, not
            evidence. Say which you did; "abstract" is an honest answer and a common one.

            `depends_on` is NOT optional and is not bookkeeping. When an input is later refuted, the
            graph walks these edges to flag every conclusion that rested on it. An omitted edge means
            your conclusion keeps standing on a premise that has been withdrawn, and nothing will
            notice. List every input, including the ones you think are safe.
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


ADJACENT = {"dna": ["protein"], "protein": ["dna", "cell"], "cell": ["protein", "tissue"],
            "tissue": ["cell", "organ"], "organ": ["tissue", "organism"],
            "organism": ["organ", "behaviour"], "behaviour": ["organism", "ecology"],
            "ecology": ["behaviour"]}


def gen_entail(accts, i=0, limit=10):
    """Propagate each claim DOWN to its neighbouring scales and check what must be true there.

    This is the central idea of docs/architecture/cross-scale-constraints.md, which says in its own
    closing section that NOTHING AUTOMATES ENTAILMENT and that the valuable outcome -- refuting a
    high-scale claim with a low-scale measurement -- HAS NEVER HAPPENED HERE. The `constraint_entailed`
    table was created with exactly the six kinds and four statuses that document specifies, and has
    held six rows ever since: the worked example, entered by hand.

    So this generator is not new scope. It is the one piece of that architecture that was specified,
    given a schema, and then never connected to anything.

    It is also the answer to a practical problem. CHALLENGE, REPLICATE and DEEPEN all run out: there
    are finitely many claims to attack and the depth cap is 2. Entailment does not run out in the
    same way, because each claim entails constraints at two neighbouring scales and an unsatisfied
    constraint is itself a question. But the reason to run it is that it can REFUTE FROM BELOW, which
    is cheaper and more decisive than any simulation -- not that it keeps the queue full.
    """
    rows = q(f"""select c.id, c.scale_id, c.statement, c.evidence from claim c
                 where c.project_id={sql_lit(PROJECT)} and c.superseded_by is null
                 and c.scale_id is not null
                 and not exists (select 1 from constraint_entailed e where e.source_claim = c.id)
                 order by case c.evidence when 'measured' then 0 when 'derived' then 1 else 2 end,
                          c.id desc
                 limit {limit}""")
    n = 0
    for cid, scale, stmt, ev in rows:
        acct = accts[i % len(accts)][0]; i += 1
        nbrs = ", ".join(ADJACENT.get(scale, []))
        prompt = textwrap.dedent(f"""
            PROPAGATE A CLAIM TO ITS NEIGHBOURING SCALES AND CHECK WHAT MUST BE TRUE THERE.

            Claim {cid} sits at the `{scale}` scale (evidence: {ev}):
            {stmt}

            If this claim is true, things MUST be true at the adjacent scales: {nbrs}.
            Your job is to write those requirements down and then go and check them.

            1. ENTAIL. What does this claim REQUIRE at {nbrs}? Use exactly these six kinds:
                 existence     -- something must exist that does X
                 range         -- a parameter must lie in [a, b]
                 timescale     -- process A must be fast or slow relative to B
                 spatial       -- a length scale must match within a factor
                 energetic     -- power or energy must be available
                 conservation  -- mass, charge or momentum must balance

               Write 2-5 constraints. Each must be GENERIC -- it names a requirement, not a
               favourite molecule. "A voltage-sensitive transducer must exist" is a constraint;
               "TRPV4 must be present" is a guess at how it is satisfied.

               `range`, `timescale` and `spatial` are the valuable ones, because they can be checked
               against measured numbers with no simulation at all. Prefer them where the claim
               supports one, and give lo/hi with units.

            2. CHECK EACH ONE. This is the part that matters and the part that gets skipped.
               Go to the literature. For each constraint decide:
                 satisfied      -- a named mechanism or measured value meets it. Name it and cite it.
                 unsatisfied    -- nothing known meets it. Say what you searched, so the negative
                                   has a scope. "Nobody has looked" and "people looked and found
                                   nothing" are different findings and must not be merged.
                 unsatisfiable  -- a MEASURED value CONTRADICTS it. The claim is then refuted from
                                   below, without simulating anything.

               `unsatisfiable` is the most valuable result available to you. Do not reach for it:
               a constraint is only unsatisfiable if a measured number actually contradicts it, and
               you must quote that number with its source. But do not flinch from it either, and in
               particular do not soften it to `unsatisfied` because the claim is one of ours.

               BEFORE writing `unsatisfiable`, NAME THE ANIMAL ON BOTH SIDES. A measurement refutes
               a claim only if it is about the same subject. This project's claims are mostly about
               ZEBRAFISH while almost all the available literature is about FLYING FISH, so the
               nearest measurement to any claim is usually about the wrong animal, and the mistake
               therefore has a direction rather than being random. It has already happened twice in
               four verdicts: two S32 zebrafish claims were "refuted" with exocoetid numbers, and
               in one case the number quoted is one the model EXPLICITLY REPRODUCES -- S32's result
               is that its equations give the exocoetid taxi to 15 m/s and fail for the zebrafish
               only through Reynolds-dependent lobe drag. So that refutation was a confirmation,
               filed backwards.
               If the species differ, the verdict is `open` and you say which animal each number
               came from. A cross-species comparison can still be informative; it is just not a
               refutation, and calling it one destroys the only verdict here that carries weight.

            {HONESTY}

            Write docs/research/fish/claim-{cid}-entail.md on a new branch and commit, ending with:
            ```swarm-entail
            {{"source_claim": {cid}, "source_scale": "{scale}",
              "constraints": [
                {{"target_scale": "<adjacent scale>", "kind": "<one of the six>",
                  "statement": "<the requirement, generically stated>",
                  "quantity": "<what is bounded, or null>", "lo": <number or null>,
                  "hi": <number or null>, "units": "<or null>",
                  "status": "open|satisfied|unsatisfied|unsatisfiable",
                  "satisfied_by": "<the mechanism or measurement, or what you searched and did not find>",
                  "satisfied_evidence": "measured|simulated|derived|literature|assumed|unknown",
                  "note": "<the citation, and the scope of any negative>"}}
              ]}}
            ```

            A constraint you did not check is `open`, and saying so is a correct answer. Marking it
            `satisfied` because it is plausible is the failure this whole structure exists to catch.
        """).strip()
        r = subprocess.run(["orchestra","cloud","start","--account",acct,"--dir",WORKDIR,"--prompt",prompt],
                           capture_output=True, text=True, timeout=300)
        try: d = json.loads(r.stdout)
        except Exception: print(f"  entail {cid} failed"); continue
        q(f"""insert into agent_session (id, project_id, harness, account, status)
              values ({sql_lit(d['session_id'])}, {sql_lit(PROJECT)}, 'cloud', {sql_lit(acct)},
                      'running') on conflict (id) do nothing""")
        print(f"  entail     claim {cid:>4}  {scale:<9} {acct}"); n += 1
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
    if running + total < want:
        n, i = gen_entail(accts, i, limit=want - running - total); total += n
    print(f"dispatched {total}")
