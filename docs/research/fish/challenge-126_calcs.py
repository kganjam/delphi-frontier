# Challenge 126 recompute. COMPUTED only. Needs S2DD_calcs.py + S2D_calcs.py (branch claude/deepen-s2-d-imobtp) in this directory.
import math, importlib.util, sys
sp=importlib.util.spec_from_file_location("dd",__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),"S2DD_calcs.py")); dd=importlib.util.module_from_spec(sp); sp.loader.exec_module(dd)
s2d=dd.s2d
# independent flying-fish check
nu=1.5e-5; U=12; c=2e4*nu/U
for ar in (9,10.7):
  for body in ((0.2,0.025),(0.2,0.035)):
    A=ar*c*c; L,D=body
    cdA=1.5*1.328/math.sqrt(U*L/nu)*0.75*math.pi*D*L
    cw=1.4*2*1.328/math.sqrt(2e4); cd0=cw+cdA/A
    ld=0.5*math.sqrt(math.pi*0.7*ar/cd0); clstar=math.sqrt(cd0*math.pi*0.7*ar)
    print(f"AR{ar} body{D}: c={c*1e3:.1f}mm cw={cw:.4f} cb={cdA/A:.4f} LDmax={ld:.2f} CL*={clstar:.2f}")
    for meas in (4.4,5.9):
      eAR=(2*meas)**2*cd0/math.pi
      print(f"   meas {meas}: eAR={eAR:.2f} e={eAR/ar:.3f} CL*_A={math.sqrt(cd0*math.pi*eAR):.2f}  ; B CD0tot={math.pi*0.7*ar/(2*meas)**2:.3f} CL*_B={math.sqrt(math.pi*0.7*ar/(2*meas)**2*math.pi*0.7*ar):.2f}")
# B under the CL cap 0.9 (consistency with S2-D final model)
ar=9; A=ar*c*c; L,D=0.2,0.025
cb=1.5*1.328/math.sqrt(U*L/nu)*0.75*math.pi*D*L/A; cw=1.4*2*1.328/math.sqrt(2e4); k=1/(math.pi*0.7*ar)
for meas in (4.4,5.9):
  cd0w=0.9/meas-k*0.81-cb; f=cd0w/cw
  print(f"B with cap, meas {meas}: CD0_wing={cd0w:.3f} = {f:.2f}x ; zebrafish AR:",[round(dd.solve(ar=a,cd0f=f)[0],2) for a in (1.5,2,4,8)])
base=dd.solve()[0]; print("base",base)
# transfer variants for attribution A
for eAR_ff,lab in ((0.902,"4.4"),(1.62,"5.9")):
  print("meas",lab)
  print("  T1 author e mult at AR4:", round(dd.solve(ar=4,e=eAR_ff/9)[0],2))
  print("  T2 fixed absolute eAR at zebrafish:", round(dd.solve(ar=1,e=eAR_ff)[0],2))
  for X in (0.3,0.6,1.0):
    e=eAR_ff/(9/(1+X)); arz=36/(9+1.76)  # zebrafish total-planform AR
    print(f"  T3 total-planform AR, extra area {X}: e={e:.3f}, zf eAR={e*arz:.2f} LD={dd.solve(ar=arz,e=e)[0]:.2f}")
  # e at AR 10.7
  print("  T1 with AR10.7 ff:", round(dd.solve(ar=4,e=eAR_ff*1/10.7)[0],2))
for r in (0.27,0.45,0.36,0.60): print("T4 ratio",r, round(r*base,2))
