import json, subprocess, sys
REPO = "/home/ubuntu/git/delphi-evolve"
REF = "work/rethink-critic"
def rec(cid):
    path = f"scopedesk/scorecard/records/{cid}.json"
    raw = subprocess.run(["git","-C",REPO,"show",f"{REF}:{path}"],capture_output=True,check=True).stdout
    import hashlib
    blob = subprocess.run(["git","-C",REPO,"rev-parse",f"{REF}:{path}"],capture_output=True,text=True,check=True).stdout.strip()
    commit = subprocess.run(["git","-C",REPO,"rev-parse",REF],capture_output=True,text=True,check=True).stdout.strip()
    return json.loads(raw), hashlib.sha256(raw).hexdigest(), blob, commit, path
R = "claude-fseries agent (single reader, Claude)"
ST = "proposed, not applied"
out = {"schema":"record-corrections/v1","version":"v1","created":"2026-11-01 (Seattle time, PST)",
       "reviewer":R,"scope":"F004 bounded action: fisher-ftns and hamilton-rule only",
       "note":"Each entry keeps the old value verbatim. Records were not edited. 'record_sha256' is sha256 of the bytes of `git show <commit>:<path>`. Source ids refer to receipts/sources-v1.json. 'NOT READ' sources are never quoted.",
       "records":{}, "corrections":[]}
items = {
 "fisher-ftns":[
  ("C-F1","fields.dct:description","units_time_scale",
   "The partial rate of change in mean fitness due to natural selection (average effects of genes held fixed) equals the additive genetic variance in fitness at that time, when fitness is measured as the Malthusian parameter m in continuous time. With discrete generations and Wrightian fitness w, the per-generation partial change is V_A(w)/w̄, equivalently w̄·V_A(w/w̄).",
   "fisher1930 p. 34: the definitions are applied to 'the special characteristic m which measures the relative rate of increase or decrease'; p. 35: 'The rate of increase in fitness of any organism at any time is equal to its genetic variance in fitness at that time.' frank1998 p. 21, eq. 2.10: Δ_f w̄ = Cov(w,g)/w̄ = V_g/w̄.",
   "The old text equates a rate with V_A without naming the fitness measure. That is right only for Malthusian m. For Wrightian w the discrete form needs the 1/w̄ factor, which the record's own math field has."),
  ("C-F2","fields.skos:notation (and search_row.math)","mathematical_object",
   "\\Delta_{NS}\\bar{w} := \\sum_i (q_i^{*}-q_i)\\,g_i = V_A(w)/\\bar{w}, with q_i^{*}=q_i w_i/\\bar{w} and g the q-weighted least-squares projection of w on gene counts, average effects fixed at the parental generation (discrete generations; form as in Frank 1998 eq. 2.10, attributed there to Price 1972b and Ewens 1989); \\left.\\frac{d\\bar{m}}{dt}\\right|_{NS} = V_A(m) for Malthusian fitness m (Fisher 1930 p. 35)",
   "fisher1930 p. 32 (X fixed by Σ X(x−X)=0), p. 33 (variance of X is W = Σ(pqaα), 'the genetic variance'), p. 35 (Σ(αdp) = Σ(pqaα)dt = W dt). Formulas are transcriptions from OCR, where Σ and α appear as 'Z'/'S' and 'a'; the same reading appears in two independent scans (receipts fisher1930, fisher1930_dli). frank1998 pp. 20-22.",
   "The old notation leaves Δ_NS and V_A undefined. The discrete Wrightian form does not appear in the cited dct:source (Fisher 1930 states the continuous m form), so its provenance should be recorded."),
  ("C-F3","fields.delphi:context (sentence 'Formal status: proved in this partial-change reading.')","scope",
   "Literature status: proved as a mathematical statement in the partial-change reading (Price 1972b; Ewens 1989, whose abstract states the theorem 'is correct as a mathematical statement, but of less biological value than was claimed by Fisher'). Project formal status: no machine-checked proof of the additive-genetic form exists in this project. The project's Lean Price files prove the total-variance selection identity (fitness_selection), which is a different statement (see F001 target-spec-v0 §6).",
   "ewens1989 abstract; delphi-evolve b4e60db9 experiments/price_probe/README.md ('fitness_selection is total-variance selection ... it is not additive-genetic Fisher FTNS'); SCORECARD row fisher-ftns = (c) FORMAL-NODE-ONLY.",
   "'Formal status: proved' can be read as a project formal proof. None exists for V_A."),
  ("C-F4","fields.delphi:context (assumption list)","scope",
   "Assumptions: V_A is the variance of additive genetic values (least-squares projection of fitness on gene counts; Fisher 1930 p. 32-33). The partial change holds the average effects fixed, and with them every other cause of change Fisher calls environment (Price 1972, Ewens 1989, per Frank 1998 pp. 20-21). Exact only for idealized populations without stochastic fluctuation (Fisher 1930 p. 35). In age-structured populations gene frequencies must be weighted by reproductive value (Fisher 1930 p. 35). One generation (discrete) or one instant (continuous); no claim about dynamics.",
   "fisher1930 p. 35: 'the ratio p : q should strictly be evaluated ... of all individuals having reproductive value, weighted according to the reproductive value of each' and 'the theorem is exact only for idealized populations, in which fortuitous fluctuations in genetic composition have been excluded'.",
   "The old context drops the reproductive-value weighting, the no-fluctuation condition and the definition of V_A as a projection."),
  ("C-F5","fields.delphi:context (sentence 'Read as a claim about the total change in mean fitness it is false under dominance, epistasis, frequency dependence or a changing environment.')","quantifiers",
   "Read as a claim about the total change in mean fitness, it does not hold in general under dominance, epistasis, frequency dependence or a changing environment. Example (one diploid locus, complete dominance, fitnesses 1, 1, 1/2, p = 1/2, Hardy-Weinberg): total change 13/392 vs V_A/w̄ = 1/28. With multiple loci, mean fitness can decrease (Ewens 1989 abstract). It can coincide even with dominance, e.g. overdominance at its internal equilibrium, where both are 0 (F001 witness W2). Without dominance at a single diploid locus, the total and partial changes coincide (F001 control C1, Hardy-Weinberg start: both 1/42).",
   "ewens1989 abstract ('difficulties with cases arising in a multi-locus system for which mean fitness can decrease'); F001/variance_witness.py output W1, C1.",
   "'False under X' reads as false whenever X is present. The correct quantifier is 'not in general'."),
  ("C-F6","fields.delphi:proposedTest","scope",
   "In a pedigreed population, estimate additive genetic values for relative fitness (animal model) and compare V_A(w)/w̄ with the selection-caused per-generation change in mean breeding value for fitness, evaluated with average effects fixed at the parental generation, separately from environmental change. Note: the theorem is an identity within the model. Such a study tests the estimation chain and the model's adequacy, not the theorem.",
   "frank1998 p. 18 (Price form for breeding values, eq. 2.8: Δḡ = Cov(w,g)/w̄ + transmission term; Robertson 1966 derived the covariance term) and p. 20 (Fisher's partial change).",
   "The old test compares V_A with the 'observed per-generation response of breeding values', which is a total change and includes transmission. Δ_NS is defined, not directly observed."),
  ("C-F7","fields.delphi:context (clause 'V_A is the additive genetic variance in fitness.')","mathematical_object",
   "V_A is the additive genetic variance in fitness, defined as the variance of the least-squares projection of fitness on gene counts (for one diploid locus in Hardy-Weinberg proportions, 2pqα²). Note: Fisher 1930 writes the genetic variance as W = Σ pqaα (pp. 32-33) and the selection increment as αdp (p. 35). The factor relating Fisher's 1930 accounting to the regression convention for diploids has not been reviewed.",
   "fisher1930 p. 32 ('the contribution of that factor to the genetic variance is represented by the expression pqaα'; OCR 'pqaa'), p. 33, p. 35; same reading in fisher1930_dli. F001/variance_witness.py W1: regression V_A = 1/32 = 2pqα² with p = 1/2, α = 1/4.",
   "The record silently uses the modern regression convention. The cited source's own formula differs by a factor of 2 for diploids under random mating if a = α. That needs a reviewer, not a silent choice. (A Gemini critique asserted that Fisher 1930 writes 2pqaα. Both 1930 scans read pqaα. The 1958 edition was not read.)"),
 ],
 "hamilton-rule":[
  ("C-H1","fields.dct:source (provenance of skos:notation)","mathematical_object",
   "Keep dct:source = 'W. D. Hamilton (1964) The genetical evolution of social behaviour. I'. Add a provenance note for the math: 'Regression (covariance) form: Hamilton 1970 and Queller 1992 (neither read by this reviewer), as presented in Frank 1998 §3.2-3.3 with r = Cov(G,g)/Var(g), −C = β_{wg·G}, B = β_{wG·g}.'",
   "frank1998 p. 47 ('I begin with Hamilton's (1970) derivation. I then turn to Queller's (1992a, 1992b) ... quantitative formulation'), p. 53. hamilton1964 NOT READ.",
   "The math field is the Queller/Price regression form, and the record says so. The only cited source is the 1964 paper, which this reviewer could not read. Frank 1998 credits the covariance (Price-equation) derivation to Hamilton 1970 and the partial-regression separation of B and C to Queller 1992."),
  ("C-H2","fields.skos:notation (and search_row.math)","quantifiers",
   "Over one generation, with w̄ > 0, Var(g) > 0, b and −c the coefficients of the joint least-squares regression (with intercept) of a focal individual's fitness on its partners' genetic value G and its own genetic value g (so the residual is orthogonal to g), and r = Cov(G,g)/Var(g): Δḡ > 0 ⟺ rb − c > 0 holds when the transmission term E(wΔg) is zero (average effects held fixed / no transmission bias). In general (exact, total): w̄Δḡ = Var(g)(rb − c) + E(wΔg), so Δḡ > 0 ⟺ rb − c > −E(wΔg)/Var(g).",
   "frank1998 p. 24-25 and p. 54 eq. 3.6 ('rB − C > −E(wΔg)/V_g ... an exact, total result'; 'If we use the Fisherian definition of partial change ... then the right side is zero and we recover the standard form of Hamilton's rule'); delphi-evolve b4e60db9 Price.lean hamilton_regression (hypotheses hvar, hres, hrel, hw; perfectly transmitted trait).",
   "The old notation states an unconditional ⟺. It needs the zero-transmission condition, Var(g) > 0 and w̄ > 0, which the project's own compiled theorem carries as hypotheses."),
  ("C-H3","fields.delphi:context (clause 'b and c are partial regressions of fitness on the actor's and the partner's genotype')","mathematical_object",
   "In the general (neighbour-modulated) form, −c is the partial regression of a focal individual's fitness on its own genetic value (holding partners' fixed), b is the partial regression of the focal's fitness on its partners' genetic value (holding its own fixed), and r is the regression of partners' genetic value on the focal's. The description's actor-centred wording (benefit to recipient, cost to actor) is the inclusive-fitness reading of the same coefficients.",
   "frank1998 p. 24 and p. 53 (Queller's regression w = β_{wg·G} g + β_{wG·g} G + ε, −C = β_{wg·G}, B = β_{wG·g}).",
   "Read in order, the old clause pairs b with the actor's genotype and c with the partner's. That is the reverse of the Queller assignment (c with own genotype, b with partners'). Read loosely, it is ambiguous. It also leaves unstated whose fitness is regressed (the focal individual's) and that the regressors are genetic values."),
  ("C-H4","fields.delphi:context (sentence 'Formal status: proved; exact in the regression form (Gardner, West and Wild 2011).')","scope",
   "Literature status: exact in the regression form as a statement about partial change (average effects held fixed), with an exact total version that adds −E(wΔg)/Var(g) (Frank 1998 eq. 3.6); Gardner, West and Wild 2011 argue for its generality (abstract only read). Project formal status: hamilton_regression compiled in delphi-evolve experiments/price_probe (one Codex session) under perfect transmission, residual orthogonality, positive trait variance and positive mean fitness; no independent statement-fidelity review.",
   "frank1998 p. 54; gww2011 abstract ('we use Fisher's genetical paradigm to demonstrate the generality of Hamilton's rule'); price_probe README.",
   "'Exact' without the partial-change qualifier overstates. 'Proved' mixes literature and project formal status."),
  ("C-H5","fields.dct:description","units_time_scale",
   "Over one generation, a gene for social behaviour increases in frequency (more precisely, the population mean of its genetic value increases) if and only if rb − c > 0, where r, b, c are regression coefficients defined in the current population and transmission adds no bias; b and c are in units of fitness, and the sign condition is unchanged by rescaling fitness by a positive constant. For a polygenic genetic value, the object is the change in mean genetic value, not the frequency of a single gene.",
   "frank1998 pp. 24-25, 53-54.",
   "The old description has no time scale ('increases ... when'), no iff/if direction and no condition on transmission."),
  ("C-H6","fields.delphi:proposedTest","scope",
   "Estimate r from genotypes and b, c as partial regressions of measured fitness on own and partners' genetic values within one generation, and test whether sign(rb − c) matches the sign of the measured change in frequency (or mean breeding value) of the helping genotype across that generation, reporting the transmission term separately.",
   "frank1998 p. 46 ('Hamilton's rule states that a behavior increases in frequency when rB − C > 0').",
   "The old test asks whether rb > c 'predicts which individuals help'. That is an individual-level behavioural prediction. The rule as recorded is a population-level condition on change in gene frequency."),
  ("C-H7","fields.delphi:context (clause 'in Hamilton's original derivation, additive fitness effects and weak selection')","scope",
   "Keep the clause, marked: 'attribution to Hamilton 1964 not verified (source not read by this reviewer); Frank 1998 p. 46 states that Hamilton (1970, 1972) emphasized weak selection, additivity of costs and benefits, and a statistical definition of relatedness.'",
   "frank1998 p. 46: 'Hamilton (1970, 1972) emphasized that the rule depends on several assumptions, including weak selection, additivity of costs and benefits of fitness components, and a special definition of relatedness that uses statistical correlations among individuals rather than genealogy'. hamilton1964 NOT READ.",
   "Not a demonstrated disagreement. A verification gap: the secondary source read attributes these conditions to later Hamilton papers. The statistical-relatedness condition is missing from the record."),
  ("C-H8","fields.delphi:context (sentence 'Critics argue that the general form is close to an identity with little predictive content (Nowak, Tarnita and Wilson 2010).')","scope",
   "Nowak, Tarnita and Wilson 2010 (main text) argue that 'Hamilton's rule almost never holds' when b and c are model parameters, and that inclusive fitness theory 'is only another method of accounting ... Hence, there are no predictions that are specific to inclusive fitness theory'. Their treatment of the regression form is in the Supplementary Information, which this reviewer did not read.",
   "nowak2010 main text (PMC3279739), section headed 'Hamilton's rule almost never holds' and the paragraph on testing predictions.",
   "The old sentence attributes an 'identity' critique of the general (regression) form. The main text does not use the word 'identity' or discuss regression (keyword search: 0 hits for 'regression'). Its stance on the parameter form ('almost never holds') is stronger than the record suggests."),
 ]}
for cid, entries in items.items():
    r, sha, blob, commit, path = rec(cid)
    out["records"][cid] = {"repo":"kganjam/delphi-evolve","commit":commit,"path":path,"record_sha256":sha,"git_blob":blob,"raw_text_sha256":r["raw_text_sha256"]}
    f = r["record"]["fields"]
    for (eid, field, axis, new, loc, why) in entries:
        key = field.split(" ")[0].replace("fields.","")
        old = f.get(key)
        if key == "delphi:context":
            frag = field.split("'")[1] if "'" in field else None
            if frag:
                assert frag in old, (eid, frag)
                old = frag
        out["corrections"].append({"id":eid,"record_id":cid,"record_sha256":sha,"field":field,
            "old_value":old,"proposed_value":new,"axis":axis,"source_locator":loc,"rationale":why,
            "reviewer":R,"status":ST,"version_note":"v1 (2026-11-01): first proposal; old value retained; no record edited"})
json.dump(out, open(sys.argv[1],"w"), indent=2, ensure_ascii=False)
print(len(out["corrections"]), "corrections")
