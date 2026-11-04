"""Challenge 127 independent arithmetic. EVERY output is a CALCULATION, not an observation.
Inputs (read-levels in challenge-127.md):
  EI_fin 1.5-4e-9 N m^2 (Puri 2018, full-text); clamp-corrected 2.1-7.8e-9 (sibling S9-D-D, calc)
  N 16-18 rays; w = D = 100-200 um (Puri 2018)
  t caudal 19.0-20.4 um, bars 16.3-25.3 um (Azevedo 2011 fig read by claim author, not re-read by me)
  E vertebral >=23 GPa (search-summary via S9)
  E_r fin ray, zebrafish caudal, nanoindentation 4.57-8.68 GPa (Bohns 2021 JBMR Plus, PMC7872341, full-text)
"""
def I(w,t): return 2*w*t**3/12          # two uncoupled flat plates
def E_impl(EIfin,N,w,t): return EIfin/N/I(w,t)
u=1e-6
# implied E envelope
for lab,(tlo,thi) in {"dorsal":(11,16.5),"caudal mean":(19.0,20.4),"caudal bar":(16.3,25.3)}.items():
    lo=E_impl(1.5e-9,18,200*u,thi*u); hi=E_impl(4e-9,16,100*u,tlo*u)
    print(f"{lab:12s} implied E {lo/1e9:.3f}-{hi/1e9:.2f} GPa; 23/hi={23e9/hi:.1f}")
# sensitivity flip at t/2
print("t=5.5um E_max", E_impl(4e-9,16,100*u,5.5*u)/1e9)
# t_crit for various E_ref and EI
for E in (23e9,8.68e9,4.57e9):
    for EIhi in (4e-9,7.8e-9):
        tc=(12*EIhi/16/(2*100e-6*E))**(1/3)
        print(f"E_ref={E/1e9:5.2f} GPa EIfin_hi={EIhi:.1e}: t_crit={tc/u:.1f} um")
# forward: predicted fin EI / measured
def fwd(E,t,w,N=17): return E*I(w,t*u)*N
for E in (23e9,8.68e9,4.57e9):
    lo=fwd(E,16.3,100*u); hi=fwd(E,25.3,200*u)
    print(f"E={E/1e9:5.2f}: pred {lo:.2e}-{hi:.2e}; /measured(Puri) {lo/4e-9:.2f}-{hi/1.5e-9:.0f}x; "
          f"/clamp-corrected {lo/7.8e-9:.2f}-{hi/2.1e-9:.0f}x; at caudal means w=100: "
          f"{fwd(E,19.0,100*u)/4e-9:.2f}x(Puri hi) {fwd(E,19.0,100*u)/7.8e-9:.2f}x(corr hi)")
# E_r -> E (nu=0.3, rigid tip)
print("E from E_r (nu=0.3):", [round(x*(1-0.09),2) for x in (4.57,8.68)])
# hypothetical osteoblast inclusion: subtract 2x2um, 2x4um from 19 um
for d in (4,8):
    t=19-d; print(f"t={t} um: margin vs 23 GPa (EI 4e-9, w=100) = {23e9/E_impl(4e-9,16,100*u,t*u):.2f}x")
