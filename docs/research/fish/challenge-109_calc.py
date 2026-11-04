"""Challenge 109: independent recomputation. Every printed number is CALCULATED.
Inputs as stated by S22-D-D / S22-D-D-D (figure-reads, proxy, search-summary); none measured here."""
FF = (0.65, 0.77)                       # flying-fish pectoral/SL target (search-summary)
P0 = {"60% resected": 0.104 / 0.6, "50% (adopted)": 0.104 / 0.5, "40% resected": 0.104 / 0.4}
F = (1.74, 2.05)                        # alf/+ proxy fold-overgrowth
print("Shortfall S = FF/(p0*f); elasticity of ln S to ln FF, ln p0, ln f = +1, -1, -1 (exact for a ratio)")
for k, p in P0.items():
    print(f"p0={p:.3f} ({k}): shortfall {FF[0]/(p*F[1]):.2f}-{FF[1]/(p*F[0]):.2f}x; "
          f"break-even f {FF[0]/p:.2f}-{FF[1]/p:.2f}x")
lo, hi = FF[0] / max(P0.values()), FF[1] / min(P0.values())
print(f"Break-even f over full p0 bracket: {lo:.2f}-{hi:.2f}x")
print(f"Gap between break-even low end and proxy high end: {lo/F[1]:.2f}x")
for s in (0.9, 0.8):
    print(f"nr21/+ shortening s={s} (illustrative): break-even f {lo/s:.2f}-{hi/s:.2f}x")
