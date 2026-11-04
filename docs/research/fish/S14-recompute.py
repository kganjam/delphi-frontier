import math
# Parallel-conductance (two-branch) model of resting Vm.
# Vm = (gK*EK + gB*EB)/(gK+gB);  EB = 0 mV (non-selective background) -- ASSUMPTION, flagged.
# EK = -100 mV, taken from Perathoner et al. 2014 full text: K+ equilibrium
# potential in Xenopus oocytes stated as "-90 to -100 mV".
EK, EB = -100.0, 0.0

def vm(r):           # r = gK/gB
    return (r*EK + EB)/(r+1.0)
def r_from_vm(v):    # invert
    return (v-EB)/(EK-v)

print("SIMULATION (not an observation). Parallel-conductance model.")
print("EK=-100 mV, EB=0 mV (assumed), Vm_wt swept because the source does not state it.\n")

print("A. Effect of a gK fold-change R on Vm, for several assumed Vm_wt")
print(f"{'Vm_wt':>7} {'r_wt':>7} | " + " | ".join(f"R={R:<4g} dVm" for R in (1.41,2.0,4.0)))
for v0 in (-20,-30,-40,-50,-60):
    r0 = r_from_vm(v0); row=[]
    for R in (1.41,2.0,4.0):
        row.append(f"{vm(r0*R):8.1f} {vm(r0*R)-v0:+6.1f}")
    print(f"{v0:>7} {r0:>7.3f} | " + " | ".join(row))

print("\n   (dVm in mV. 'Available swing' from Vm_wt to EK = |EK - Vm_wt|.)")
for v0 in (-20,-30,-40,-50,-60):
    r0=r_from_vm(v0); d=vm(r0*2.0)-v0
    print(f"   Vm_wt={v0:>4} mV: 2-fold gK buys {d:+6.1f} mV of the {abs(EK-v0):4.0f} mV available = {100*abs(d)/abs(EK-v0):4.1f}%")

print("\nB. Compressiveness: successive doublings of gK from Vm_wt = -40 mV")
r0=r_from_vm(-40.0); prev=-40.0
for k in range(0,6):
    v=vm(r0*(2.0**k))
    print(f"   gK x{2**k:<3d} -> Vm {v:7.2f} mV   step {v-prev:+6.2f} mV")
    prev=v

print("\nC. Resolvable grades inside the measured window, as a function of")
print("   the Vm discrimination step sigma_V (UNMEASURED in fin tissue):")
for v0,R in ((-40,2.0),):
    r0=r_from_vm(v0); window=abs(vm(r0*R)-v0)
    print(f"   window from R={R} at Vm_wt={v0} mV is {window:.1f} mV")
    for s in (2,5,10,15):
        print(f"      sigma_V={s:>2} mV -> {window/s:5.2f} distinguishable levels")

print("\nD. Sensitivity of the grade count to the key number R (sigma_V = 5 mV):")
r0=r_from_vm(-40.0)
for R in (1.0,1.41,2.0,2.83,4.0):
    w=abs(vm(r0*R)-(-40.0))
    print(f"   R={R:<5g} -> window {w:5.1f} mV -> {w/5.0:5.2f} levels")
