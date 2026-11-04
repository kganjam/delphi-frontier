"""Claim 225 entailment checks. Every output is CALCULATED, not observed.
Run: python3 docs/research/fish/claim_225_entail.py
Inputs: S29 = taken from S29-organism.md as stated; READ = literature (read-level in the .md); ASSUMED = mine/S29's.
"""
W = 11.83e-3            # S29: stored energy, central case, J
M = 0.40e-3             # S29: body mass, kg
RHO = 1050.0            # S29 ASSUMED body (and muscle) density, kg/m3
VB = M / RHO            # body volume, m3
E_KER = 1.65e9          # READ via S29 (Ker 1981, abstract): sheep tendon modulus
E_ZF = 515e6            # READ (Shah et al. 2015, search-summary): zebrafish craniofacial tendon linear modulus
SIG_ISO = 186e3         # READ via challenge-225 (Altringham & Johnston 1982, search-summary): cod fast fibre isometric stress, Pa

print(f"body volume {VB*1e9:.1f} mm3")
# C1: energy density band implied by the claim
u_lo = W / (0.239 * VB); u_hi = W / (0.0102 * VB)
print(f"C1 required u for 23.9% .. 1.02% of body: {u_lo/1e6:.3f} .. {u_hi/1e6:.2f} MJ/m3")
for E, tag in ((1.2e9, "tuna 1.2 GPa"), (0.65e9, "tuna 0.65 GPa"), (E_ZF, "zebrafish 0.515 GPa")):
    u = 0.5 * E * 0.02**2
    print(f"   {tag} at 2% strain: u {u/1e6:.3f} MJ/m3 -> {100*W/u/VB:.1f}% of body")
# C5: strain needed to reach the mammal-grade energy densities
for s in (50e6, 100e6):
    u = s*s/(2*E_KER)
    print(f"C5 mammal branch {s/1e6:.0f} MPa: strain at E_Ker {100*s/E_KER:.2f}%; "
          f"same u at E_zf needs strain {100*(2*u/E_ZF)**0.5:.1f}% and stress {E_ZF*(2*u/E_ZF)**0.5/1e6:.0f} MPa")
# C3: muscle strain needed to put W into the spring in one loading stroke
for f in (0.30, 0.60):
    Vm = f * VB
    e_rect = W / (SIG_ISO * Vm)      # ideal: constant max force throughout loading
    e_lin = 2 * e_rect               # linear spring: force rises 0 -> max
    print(f"C3 muscle fraction {f:.0%}: Vm {Vm*1e9:.0f} mm3, required fibre strain "
          f"{100*e_rect:.0f}% (constant force) .. {100*e_lin:.0f}% (linear spring)")
for e in (0.16, 0.24):
    print(f"   work density cap at sigma_iso and strain {e:.0%}: {SIG_ISO*e/RHO:.0f} J/kg muscle (constant force)")
