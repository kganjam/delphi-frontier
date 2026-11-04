"""S24-D-D: attack the f_max input of S24-D. Every output is a CALCULATION, not an observation.
Inputs: M = measured (literature, see S24-D-deepen.md), A = assumption, I = inherited from S24/S24-D.
Run: python3 S24-D-deepen_calc.py
"""
U = 1.95                 # m/s, 3-BL glide target (I)
U1 = 5.84                # m/s, 1-BL glide target (I)
L = 0.040                # m, project premise (I)
LAM = (0.6, 0.7, 0.8)    # stride, body lengths per beat (M, Wardle 1975 via S24-D, search-summary)
FMAX = 52.0              # Hz (M, Kyriakatos 2011, full-text: max across animals, EMG, intact fish)

def freq(U, lam, L): return U / (lam * L)

print("1. Sensitivity of S24-D's conclusion (ratio f_req/f_max), one input at a time")
base = [freq(U, l, L) / FMAX for l in (0.8, 0.6)]
print(f"  base ratio: {base[0]:.2f}-{base[1]:.2f}")
for name, fac in (("f_max x2", ("f", 2)), ("f_max /2", ("f", .5)), ("lambda x2", ("l", 2)),
                  ("L x2", ("L", 2)), ("U /2", ("U", .5))):
    k, v = fac
    r = []
    for l in (0.8, 0.6):
        f = freq(U * (v if k == "U" else 1), l * (v if k == "l" else 1), L * (v if k == "L" else 1))
        r.append(f / (FMAX * (v if k == "f" else 1)))
    print(f"  {name:10s}: {r[0]:.2f}-{r[1]:.2f}  {'FLIPS (<1)' if max(r) < 1 else ('flips at one end' if min(r) < 1 else 'holds (>1)')}")
print(f"  break-even f_max* = {freq(U,0.8,L):.0f}-{freq(U,0.6,L):.0f} Hz (needs x{freq(U,0.8,L)/FMAX:.2f}-{freq(U,0.6,L)/FMAX:.2f})")
print(f"  break-even lambda* = {U/(FMAX*L):.2f} L/beat")

print("\n2. Independent kinematic check: tail-beat frequency implied by the Danos & Lauder 2012 peak speed")
for Ub, lab in ((0.842, "TL basis (calc in S24)"), (1.05, "SL basis (calc in S24)")):
    for Lf in (0.033,):
        fs = [freq(Ub, l, Lf) for l in (0.8, 0.7, 0.6)]
        print(f"  U={Ub} m/s {lab}, L={Lf*1e3:.0f} mm: f = {fs[0]:.0f}/{fs[1]:.0f}/{fs[2]:.0f} Hz at lambda 0.8/0.7/0.6")

print("\n3. Size correction of the 52 Hz maximum (fish 18-30 mm) to the 40 mm premise, f ~ L^-b (b ASSUMED)")
for b in (0.0, 0.5, 1.0):
    lo, hi = FMAX * (0.030 / L) ** b, FMAX * (0.018 / L) ** b
    print(f"  b={b}: 52 Hz recorded in a 30 mm fish -> {lo:.0f} Hz at 40 mm; in an 18 mm fish -> {hi:.0f} Hz")

print("\n4. Temperature: Q10 that would lift 52 Hz to the requirement if recorded at 22 C and used at 28 C")
for target in (freq(U, 0.8, L), freq(U, 0.6, L)):
    for dT in (6, 8):
        q10 = (target / FMAX) ** (10 / dT)
        print(f"  to {target:.0f} Hz over {dT} C: Q10 = {q10:.2f}")

print("\n5. Recomputed ratio with the improved f_max band")
for fm, lab in ((52, "EMG max across 8 fish (upper bound)"), (42, "'slightly >40 Hz', single-animal escape"),
                (36, "D&L kinematic, lambda 0.7, TL basis"), (30, "lowest typical escape ('30 Hz')")):
    r = [freq(U, l, L) / fm for l in (0.8, 0.6)]
    print(f"  f_max {fm} Hz ({lab}): {r[0]:.2f}-{r[1]:.2f}x")
print(f"  tuna-like lambda 1.0 corner: f_req {freq(U,1.0,L):.0f} Hz vs 52 -> {freq(U,1.0,L)/52:.2f}x, vs 42 -> {freq(U,1.0,L)/42:.2f}x")
print(f"  1-BL: f_req {freq(U1,1.0,L):.0f}-{freq(U1,0.6,L):.0f} Hz vs 52 -> {freq(U1,1.0,L)/52:.1f}-{freq(U1,0.6,L)/52:.1f}x")

print("\n6. Muscle check (Idoux 2022, 20-22 C): Ca2+ decay tau 8.8 ms; half-period at required f")
for f in (52, 61, 81):
    print(f"  f={f} Hz: half-period {1000/(2*f):.1f} ms = {1000/(2*f)/8.8:.2f} tau")
