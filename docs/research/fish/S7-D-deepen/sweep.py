"""Sagittal-plane sweep of bone bending section modulus about the AP (z) axis. CALCULATED from published mesh vertices."""
import sys, json, numpy as np; sys.path.insert(0, sys.argv[1]); from section import section
P=np.load(sys.argv[2])["P"]; x0,x1,z0,z1=[float(v) for v in sys.argv[3].split(",")]; ys=[float(v) for v in sys.argv[4].split(",")]
mid=float(sys.argv[5]); label=sys.argv[6]
P=P[(P[:,0]>x0)&(P[:,0]<x1)&(P[:,2]>z0)&(P[:,2]<z1)]
rows=[]
for hw in (15,30):
  for y in ys:
    c=sorted(section(np.c_[P[abs(P[:,1]-y)<hw][:,0],P[abs(P[:,1]-y)<hw][:,2]]),key=lambda c:-c['Z_mm3'])
    rows.append(dict(fish=label,hw=hw,y=y,off_mid=abs(mid-y),n=len(c),sumZ=sum(k['Z_mm3'] for k in c),maxZ=c[0]['Z_mm3'] if c else 0,
       maxZ_A=c[0]['A_mm2'] if c else 0, maxZ_t=c[0]['tmax_um'] if c else 0, maxZ_h=(c[0]['u_ext'][1]-c[0]['u_ext'][0]) if c else 0))
    r=rows[-1]; print(f"{label} hw{hw} y={y:.0f} off={r['off_mid']:.0f} n={r['n']} sumZ={r['sumZ']:.2e} maxZ={r['maxZ']:.2e} (A={r['maxZ_A']:.3f} t={r['maxZ_t']:.0f} h={r['maxZ_h']:.0f})")
json.dump(rows,open(f"sweep_{label}.json","w"),indent=0)
