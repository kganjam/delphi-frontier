"""Challenge 171: independent recomputation for the S10-D-D claim.
Every printed number is a CALCULATION (Rankine-Froude hover, S10 inputs). None is an observation."""
import math
g, rho, k = 9.81, 1.2, 1.2
m = 0.4e-3
P_FAST = 134.4  # W/kg muscle, Mead et al. 2020 via S10 (measured, larval, 80 Hz)

def p_ind(R):
    W = m * g
    A = math.pi * R * R
    return k * (W ** 1.5) / math.sqrt(2 * rho * A)

geoms = [(0.04, 1.5), (0.04, 2.0), (0.02, 1.5), (0.02, 2.0)]
body = [M * p_ind(R) / m for R, M in geoms]
print("W/kg body per geometry:", [round(b, 2) for b in body])

# Abudefduf saxatilis, % body mass per fin (Mansuit & Herrel 2021 Table 1, as quoted by challenge-77 and the author)
AbS, AbP, AdS, AdP = 0.13, 0.23, 0.15, 0.18
four = AbS + AbP + AdS + AdP
cases = {
    "four-group sum (S10-D)": 2 * four / 100,
    "bluegill ratio by RANK (two largest in Abudefduf: AbP+AdP) x2": 2 * 2 * (AbP + AdP) / 100,
    "bluegill ratio by IDENTITY (AbS+AdP, bluegill main muscles) x2": 2 * 2 * (AbS + AdP) / 100,
    "author upper bracket (four-group sum x2)": 2 * 2 * four / 100,
}
for lab, f in cases.items():
    req = [b / f for b in body]
    print(f"f={f:.4f} {lab}: req " + "/".join(f"{r:.0f}" for r in req)
          + f"  shortfall x{req[0]/P_FAST:.2f}..x{req[-1]/P_FAST:.2f}")

# share of the four-group sum that the 'two largest' make up under each reading
print(f"two largest (rank) share of four-group sum: {(AbP+AdP)/four:.2f}")
print(f"identity pair share of four-group sum:      {(AbS+AdP)/four:.2f}")
print(f"author upper bracket implies two-largest share of girdle = {(AbP+AdP)/(2*four):.2f} (bluegill: 0.50)")

# f-independent check
for pm in (0.15, 0.21, 0.30, 0.42):
    print(f"Pmech {pm} W/kg body -> generous hover x{body[0]/pm:.0f}")
