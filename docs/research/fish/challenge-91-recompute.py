# INDEPENDENT recomputation. Written from the stated inputs only.
# Two-branch resting-potential divider: Vm = (gK*EK + gB*EB)/(gK+gB)
# Let x = gK/gB.  Vm(x) = (x*EK + EB)/(x+1)
# Invert: x = (Vm - EB)/(EK - Vm)
EK = -100.0
EB = 0.0

def Vm(x, EK=EK, EB=EB): return (x*EK + EB)/(x+1.0)
def x_of(V, EK=EK, EB=EB): return (V-EB)/(EK-V)

print("== A. independent check of the author's 17.1 mV ==")
for V0 in (-20,-30,-40,-50,-60):
    x0 = x_of(V0)
    V2 = Vm(2.0*x0)
    print(f"  Vm_wt={V0:>4} mV  x0={x0:.6f}  Vm(R=2)={V2:9.5f}  dVm={V2-V0:+8.4f} mV  avail={abs(EK-V0):4.0f}  pct={100*abs(V2-V0)/abs(EK-V0):5.2f}%")

print("\n== B. closed form check at Vm_wt=-40 ==")
# x0 = (-40-0)/(-100+40) = -40/-60 = 2/3 ; 2x0 = 4/3
# Vm = ((4/3)(-100)+0)/((4/3)+1) = (-400/3)/(7/3) = -400/7
print("  exact -400/7 =", -400/7, " dVm =", -400/7 + 40, " (=-120/7)")
print("  -120/7 =", -120/7)
print("  |dVm|/sigma at sigma=5:", abs(-120/7)/5.0)

print("\n== C. intervals vs setpoints (off-by-one test) ==")
w = abs(-120/7)
for s in (2,5,10,15):
    print(f"  sigma={s:>2}: intervals={w/s:6.3f}   setpoints(=intervals+1)={w/s+1:6.3f}   integer setpoints={int(w//s)+1}")

print("\n== D. RELAXED: include the measured gK->0 arm (GFG->AAA, author's own §3b series {0,1,~2}) ==")
x0 = x_of(-40.0)
for R in (0.0,0.25,0.5,1.0,2.0):
    print(f"  R={R:<5} gK/gB={R*x0:7.4f}  Vm={Vm(R*x0):9.4f} mV")
full = abs(Vm(0.0) - Vm(2*x0))
print(f"  full two-sided window (R=0 .. R=2) = {full:.4f} mV")
for s in (2,5,10,15):
    print(f"     sigma={s:>2}: intervals={full/s:6.3f}  setpoints={full/s+1:6.3f}")

print("\n== E. RELAXED: E_B is not 0 mV (author's flagged assumption) ==")
print("  one-sided window (R=1->2) at Vm_wt=-40, EK=-100, varying EB:")
for eb in (0.0,-10.0,-20.0,-30.0,-40.0,+10.0,+20.0):
    if abs(eb - (-40.0)) < 1e-9:
        print(f"    EB={eb:+6} : undefined (Vm_wt==EB implies gK=0)"); continue
    x0b = x_of(-40.0, EK, eb)
    if x0b <= 0:
        print(f"    EB={eb:+6} : x0={x0b:.3f} non-physical"); continue
    d = Vm(2*x0b, EK, eb) - (-40.0)
    print(f"    EB={eb:+6} : x0={x0b:7.4f}  dVm={d:+8.3f} mV  -> {abs(d)/5:5.2f} intervals at sigma=5")

print("\n== F. RELAXED: sigma_V as tissue-mean error rather than single-cell scatter ==")
import math
w = abs(-120/7)
for sc in (5.0,10.0,15.0):
    for N in (1,10,100,1000,10000):
        print(f"    sigma_cell={sc:>4} mV, N={N:>5} cells -> sigma_mean={sc/math.sqrt(N):8.4f} -> intervals={w/(sc/math.sqrt(N)):10.2f}")
    print()

print("== G. sensitivity in R, my own numbers, sigma=5 ==")
x0 = x_of(-40.0)
for R in (1.0,1.41,2.0,2.83,4.0):
    w = abs(Vm(R*x0) - (-40.0))
    print(f"  R={R:<5} window={w:6.3f} mV  intervals={w/5:5.3f}  setpoints={w/5+1:5.3f}")
