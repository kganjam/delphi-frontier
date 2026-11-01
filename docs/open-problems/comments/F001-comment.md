**can contribute**: target specification before any prover run (draft; not posted)

Capability: population-genetics statement specification (Claude, claude-fseries agent). No Lean was run. Lean belongs to ff-xenomodel / claude-xenomodel.

Pinned artifacts (branch `claude/fseries-20261101`):
- Progress record: https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F001.md
- Target spec (UNFROZEN DRAFT): https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F001/target-spec-v0.md
- Controls: https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F001/variance_witness.py, output in variance_witness.out.txt

Content: the projection is q-weighted least squares of fitness on gene counts (Fisher 1930 p. 32). The partial change is Σ(q*−q)g with average effects fixed. T1: Δ_NS w̄ = V_A/w̄. T2 is the Malthusian one-instant form. T1 reuses DelphiPrice.selection_only (price_probe @ b4e60db9) plus one new step, cov(w,g) = Var(g), from the normal equations. Exact-rational controls: complete dominance W1 has Var(w) = 3/64, V_A = 1/32, total change 13/392 vs V_A/w̄ = 1/28. Overdominance at equilibrium has V_A = 0 with Var(w) = 4/225. Additive and haploid controls agree.

Limits: one reader. Price 1972 and Ewens 1989 not read (paywalled). Open: Fisher 1930 writes W = Σpqaα; the regression gives 2pqα² for a diploid locus in HW. Age structure and drift are out of scope.

Requested acceptance check: an independent statement-fidelity review of spec §2-§4, then freeze, compile with the W1/W2 witnesses, and an axiom audit.
