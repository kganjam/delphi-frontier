import sys
for f in ["boltz2.cif","esmfold2.cif"]:
    hdr=[];rows=[];inl=False
    for l in open(f):
        if l.startswith("_atom_site."): hdr.append(l.strip().split(".")[1]); inl=True; continue
        if inl and (l.startswith("ATOM") or l.startswith("HETATM")): rows.append(l.split())
        elif inl and rows and not l.startswith(("ATOM","HETATM")): break
    i=hdr.index; ca={}
    for r in rows:
        ca.setdefault(int(r[i("label_seq_id")]),[]).append(float(r[i("B_iso_or_equiv")]))
    pr={k:sum(v)/len(v) for k,v in ca.items()}
    cA={int(r[i("label_seq_id")]):float(r[i("B_iso_or_equiv")]) for r in rows if r[i("label_atom_id")]=="CA"}
    v=list(cA.values()); s=1 if max(v)>1.5 else 100
    v=[x*s for x in v]
    print(f,len(v),"meanCA %.1f"%(sum(v)/len(v)),">70 %.1f%%"%(100*sum(x>70 for x in v)/len(v)),
      "TIGYG %.1f"%(sum(cA[k]*s for k in range(98,103))/5),"TVGFG %.1f"%(sum(cA[k]*s for k in range(203,208))/5),
      "1-250 %.1f"%(sum(cA[k]*s for k in range(1,251))/250),"261-448 %.1f"%(sum(cA[k]*s for k in range(261,449))/188))
