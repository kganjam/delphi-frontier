"""Challenge 272 probe. Re-runs S32 equations with alternative lobe C_D(Re) models.
Usage: git show origin/claude/s32-multi-stroke-launch-qpq9g2:docs/research/fish/S32_taxi.py > S32_taxi.py
       python3 -I docs/research/fish/challenge-272_probe.py S32_taxi.py
"""
import io, contextlib, math, runpy, sys
with contextlib.redirect_stdout(io.StringIO()):
    M = runpy.run_path(sys.argv[1])
NU=1e-6; C6=2.55
lam=lambda Re: 2*1.328/math.sqrt(Re)
tur=lambda Re: 2*0.074/Re**0.2
FORM=0.08-lam(4780)
models={
 "S32 const": lambda Re: 0.08,
 "S32 scaled (Re^-1/2 all of C_D)": lambda Re: 0.08*math.sqrt(min(1,9560/Re)) if Re>9560 else (0.08*math.sqrt(4780/Re) if Re<4780 else 0.08),
 "fixed form + laminar friction": lambda Re: FORM+lam(Re),
 "fixed form + turbulent friction (Re>5e5? used always above 1e5)": lambda Re: FORM+(tur(Re) if Re>1e5 else lam(Re)),
 "thin plate laminar friction only": lambda Re: lam(Re),
 "thin plate turb friction above 1e5": lambda Re: tur(Re) if Re>1e5 else lam(Re),
}
print(f"form part if 0.08 = form + laminar friction at Re 4780: {FORM:.4f}")
g=M['__builtins__']
def run(name, fn):
    M['cd_lobe'].__globals__['cd_lobe']=lambda U,c,mode: fn(max(U,1e-6)*c/NU)
    out=[]
    # zebrafish GENEROUS, recalibrated G with the same C_D model
    s=M['SCEN']['GENEROUS']; G=M['G_calibrated'](s['Cdb'],'x')
    p=M['zf_params'](s['m'],s['phi'],G,'x',s['CD0'],s['costh'],s['dcos'])
    ue=M['u_eq'](p); out.append(f"ZF gen U_eq {ue:.2f} = {ue/p['Vto']:.2f} V_to (C_D@Ueq {fn(ue*6e-3/NU):.4f})")
    s=M['SCEN']['CENTRAL']; G=M['G_calibrated'](s['Cdb'],'x')
    p=M['zf_params'](s['m'],s['phi'],G,'x',s['CD0'],s['costh'],s['dcos'])
    ue=M['u_eq'](p); out.append(f"ZF cen {ue/p['Vto']:.2f}")
    for Mx,A in ((0.191,0.026),(0.191,0.031),(0.300,0.031)):
        p,WL,S=M['exo'](Mx,0.5,A,'x'); ue=M['u_eq'](p)
        out.append(f"exo {Mx*1e3:.0f}g/{A*100:.1f}cm {ue/p['Vto']:.2f} (C_D {fn(ue*0.025/NU):.4f})")
    print(f"{name:45s} | "+" | ".join(out))
for k,v in models.items(): run(k,v)
# foil-alone independent ratio
print("foil-alone U_max/V_to = (fA/V_to)*sqrt(c6/C_D):")
for lab,r,cd in (("ZF lo",0.095,0.08),("ZF hi",0.103,0.06),("exo lo",0.087,0.011),("exo hi",0.095,0.010)):
    print(lab, round(r*math.sqrt(C6/cd),3))
