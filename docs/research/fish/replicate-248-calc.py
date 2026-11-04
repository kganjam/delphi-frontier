# Replication 248: independent recompute of S23-D lenient-corner margin and flip threshold.
# COMPUTATION ONLY. Inputs: S23-protein.md grid (parent) + search-summary moduli.
W = 0.4e-3 * 9.81
EI_meas = {"low": 1.5e-9, "high": 4e-9}          # Puri 2018 via parent (full-text there)
grid = [(L, t) for L in (0.02, 0.04) for t in (0.05, 0.10, 0.20)]
def EIreq(L, t): return (W/2) * L**2 / (8*t)
S = {}
for L, t in grid:
    for k, e in EI_meas.items():
        S[(L, t, k)] = EIreq(L, t) / e
        print(f"L={L*100:.0f}cm tol={t:.2f} EImeas={e:.1e}: EI_req={EIreq(L,t):.3e}  S={S[(L,t,k)]:.1f}")
Smin, Smax = min(S.values()), max(S.values())
print(f"S range {Smin:.1f} .. {Smax:.1f}")
E_target = (5e9, 10e9)    # dry collagen, dragline silk (parent sec 3.2)
for Et in E_target:
    print(f"flip E0* = E_target/S, E_target={Et/1e9:.0f} GPa: lenient {Et/Smin/1e6:.1f} MPa, strict {Et/Smax/1e6:.2f} MPa")
E0 = {"AFM hydrated fibril, Hertz (Yadavally)": 1.2e6,
      "AFM hydrated fibril, DMT low": 5e6, "AFM hydrated fibril, DMT high": 10e6,
      "AFM hydrated fibril PBS low": 0.2e9, "AFM hydrated fibril PBS high": 0.5e9,
      "wet tendon fascicle low (review)": 0.48e9, "wet rat-tail fibre (Kato 1989)": 0.57e9,
      "hydrated fibre (Gentleman 2003)": 1.17e9}
print("\nLenient corner (S = Smin), E_target = 10 GPa  [and 5 GPa]:")
for k, e in E0.items():
    m10 = Smin / (10e9/e); m5 = Smin / (5e9/e)
    print(f"  E0={e/1e6:8.1f} MPa {k:42s} C10={10e9/e:8.1f} margin10={m10:7.3f}  margin5={m5:7.3f}")
print(f"\nParent pairings: C=25 -> margin {Smin/25:.2f};  C=20 -> margin {Smin/20:.2f}")
