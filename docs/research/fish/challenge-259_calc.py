"""Challenge 259: independent re-derivation of S30-D numbers and relaxation tests.
All outputs are CALCULATED, not observed. Run: python3 docs/research/fish/challenge-259_calc.py"""
import math
M0=0.25e-3; NEED=10.17; F=0.30; ES=0.93; EH=0.37; RHO=1060.0
def R0(w,f=F): return f*w*ES*EH/NEED
def ms(w,beta=1/3,f=F): return M0*R0(w,f)**(1/beta)
def wb(sig,eps,shape=0.5): return shape*sig*eps/RHO
print("R0(53)=%.4f m*(53)=%.2f mg"%(R0(53),ms(53)*1e6))
for lab,s,e in (("lo",200e3,.10),("c",250e3,.13),("hi",300e3,.15),("ceil",300e3,.24)):
    w=wb(s,e); print(lab,"w=%.2f"%w, " ".join("b%.3f:%.3f mg"%(b,ms(w,b)*1e6) for b in (1/3,.36,.40,.533)))
print("zebrafish/m*: central %.0f, range %.0f-%.0f"%(0.4e-3/ms(wb(250e3,.13)),0.4e-3/ms(wb(300e3,.15),.533),0.4e-3/ms(wb(200e3,.10))))
Re0=4.37*0.0062/1.5e-5; floor=M0*(700/Re0)**2; print("Re0=%.0f floor=%.2f mg"%(Re0,floor*1e6))
# w needed to reach floor
for b in (1/3,.36,.40,.533):
    r=(floor/M0)**b; print("w to reach floor at beta %.3f: %.1f J/kg"%(b,r*NEED/(F*ES*EH)))
print("--- relaxation A: constant-force loading (shape 1.0 instead of 0.5) ---")
for lab,s,e in (("lo",200e3,.10),("c",250e3,.13),("hi",300e3,.15)):
    w=wb(s,e,1.0); print(lab,"w=%.1f"%w," ".join("b%.3f:%.2f mg"%(b,ms(w,b)*1e6) for b in (1/3,.36,.40,.533)))
print("--- relaxation B: fibre strain not capped at C-start value (linear spring) ---")
for e in (.20,.25,.30,.35):
    w=wb(250e3,e); print("eps %.2f w=%.1f"%(e,w)," ".join("b%.3f:%.2f mg"%(b,ms(w,b)*1e6) for b in (1/3,.533)))
print("--- calibration: same in-vivo-strain bound applied to frog (Rana pipiens in-vivo plantaris) ---")
for lab,e in (("pre-movement 7.8%",.078),("total 14.6%",.146)):
    for s in (200e3,250e3,300e3):
        print(lab,"sig %d kPa -> w=%.1f J/kg (vs isolated-prep 22/37/53)"%(s/1e3,wb(s,e)))
