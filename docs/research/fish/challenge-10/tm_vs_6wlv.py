import numpy as np, tmtools, sys
three={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V','MSE':'M'}
def pdb(f,chain=None):
    c=[];s=[];seen=set()
    for l in open(f):
        if l.startswith(("ATOM","HETATM")) and l[12:16].strip()=="CA" and (chain is None or l[21]==chain):
            k=(l[21],l[22:27])
            if k in seen: continue
            seen.add(k); c.append([float(l[30:38]),float(l[38:46]),float(l[46:54])]); s.append(three.get(l[17:20],'X'))
        if l.startswith("ENDMDL"): break
    return np.array(c),"".join(s)
def cif(f):
    h=[];c=[];s=[];inl=False
    for l in open(f):
        if l.startswith("_atom_site."): h.append(l.strip().split(".")[1]); inl=True; continue
        if inl and l.startswith(("ATOM","HETATM")):
            r=l.split(); i=h.index
            if r[i("label_atom_id")]=="CA": c.append([float(r[i("Cartn_x")]),float(r[i("Cartn_y")]),float(r[i("Cartn_z")])]); s.append(three[r[i("label_comp_id")]])
    return np.array(c),"".join(s)
ref,rs=pdb(sys.argv[1] if len(sys.argv)>1 else "dl/6WLV.pdb","A")
print("6WLV chain A CA:",len(ref))
for name,(c,s) in [("OpenFold2 single-seq (bioservices run)",pdb("of2_bios.pdb")),("Boltz2+PDB70 MSA",cif("boltz2.cif")),("ESMFold2",cif("esmfold2.cif"))]:
    r=tmtools.tm_align(c,ref,s,rs)
    # core 1-250 only
    r2=tmtools.tm_align(c[:250],ref,s[:250],rs)
    print(f"{name}: TM(norm by 6WLV-A)={r.tm_norm_chain2:.3f} TM(norm by model)={r.tm_norm_chain1:.3f} RMSD={r.rmsd:.2f} | core1-250 TM(norm 6WLV-A)={r2.tm_norm_chain2:.3f}")
c,s=cif("esmfold2.cif"); r=tmtools.tm_align(c,ref,s,rs)
a,b=r.seqxA,r.seqyA; pairs=[(x,y) for x,y in zip(a,b) if x!='-' and y!='-']
print("aligned",len(pairs),"identity %.1f%%"%(100*sum(x==y for x,y in pairs)/len(pairs)))
