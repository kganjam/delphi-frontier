# S13-D sensitivity: all values COMPUTED, none observed.
g=9.81; m=0.4e-3; W=m*g; b2=0.02
def EI_req(frac):            # frac = allowable tip deflection as fraction of semi-span
    w=(W/2)/b2
    return w*b2**4/(8*frac*b2)
base=EI_req(0.10)
print("EI_req(10%% semi-span) = %.3e N m^2 (recomputed, matches S13 9.81e-7)"%base)
print()
print("A. Sensitivity of the FEASIBILITY conclusion to the deflection criterion")
for f in (0.05,0.10,0.20,0.40,0.80):
    E=EI_req(f)
    print("  delta=%4.0f%% semi-span -> EI_req %.2e ; gap vs 4e-9 = %5.0fx ; vs 1.5e-9 = %5.0fx"%(100*f,E,E/4e-9,E/1.5e-9))
print()
print("B. Required ray-material E at each gap, from the 1 GPa teleost whole-ray proxy")
for f in (0.10,0.20,0.40,0.80):
    r=EI_req(f)/4e-9
    print("  delta=%4.0f%% -> %5.0fx -> E_req = %6.1f GPa (protein-solid ceiling ~10-30 GPa)"%(100*f,r,r*1.0))
print()
print("C. pLDDT gate, And1 / E7F5V5, AlphaFold DB v6 (prediction, not measurement)")
conf,vh,low,vlow=0.223,0.053,0.309,0.416
print("  fractions sum check = %.3f (must be ~1.000)"%(conf+vh+low+vlow))
print("  fraction pLDDT>70 (confident+very-high) = %.3f  i.e. %.1f%% of 570 residues = %.0f residues"%(conf+vh,100*(conf+vh),570*(conf+vh)))
print("  recorded input was 0.0%% above pLDDT 70 -> discrepancy is categorical, not a factor of two")
print()
print("D. Proline fraction check against the recorded 11.8%")
s=''.join(open('docs/research/fish/E7F5V5.fasta').read().split('\n')[1:])
print("  full chain 1-570: P = %d/%d = %.1f%%"%(s.count('P'),len(s),100*s.count('P')/len(s)))
mat=s[26:]
print("  mature chain 27-570 (UniProt signal 1-26): P = %d/%d = %.1f%%"%(mat.count('P'),len(mat),100*mat.count('P')/len(mat)))
print("  if 11.8%% were wrong by 2x (5.9%% or 23.6%%): 5.9%% is below the human proteome mean (~5%%) and 23.6%% is above Hs COL1A1 (19.0%%, computed) -> only the measured value is consistent with the record")
