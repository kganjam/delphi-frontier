can contribute: an assay audit for one specified system, done before proposing any BioNeMo computation. No model was run.

**System:** zebrafish blastula BMP2b/Chordin (Pomreinke et al. 2017 eLife, PMC5658070, full text read).
- Measured: D_eff by FRAP (BMP2b 2.0–2.6, Chordin 6.0–7.3 µm²/s), D_free by FCS (46 and 59 µm²/s), k1 by FDAP (8.9 and 9.6 ×10⁻⁵ /s), and gradient extent from transplanted clones.
- Not measured: BMP–Chordin or receptor Kd, production rate, source geometry, extracellular volume fraction.
- This is not a fin system. I found no fin-stage transport measurement.

**Check:** arithmetic on the published values (`sdd_check.py`).
- Steady-state λ = √(D/k) does not apply, because k·t ≈ 0.3 at 60 min.
- A held-out x50 check passes or fails depending only on the assumed clone radius, which was not measured.

**Project structures:** the OpenFold2 fin-protein monomers have mean pLDDT 41–56. None of the structure outputs gives Kd, turnover or D_eff.

**Verdict:** no BioNeMo run is justified until matched fin measurements exist and a pre-registered output-to-measurement mapping passes a negative control.

Files (branch `claude/fseries-20261101`):
- [F002.md](https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F002.md)
- [assay-audit-v1.json](https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F002/assay-audit-v1.json)
- [sdd_check.py](https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F002/sdd_check.py)

**Limits:** unreviewed; the per-embryo profiles were not digitised; the authors' 3D model was not re-run.

**Blocked on:** a wet lab for fin FRAP/FDAP, and a transport reviewer.
