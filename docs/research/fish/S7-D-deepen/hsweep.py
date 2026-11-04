"""Horizontal-plane (normal x) sweep: bending about z, stress varies with y. CALCULATED."""
import sys, json, numpy as np; sys.path.insert(0, sys.argv[1]); from section import section
P=np.load(sys.argv[2])["P"]; y0,y1,z0,z1=[float(v) for v in sys.argv[3].split(",")]; xs=[float(v) for v in sys.argv[4].split(",")]; label=sys.argv[5]
P=P[(P[:,1]>y0)&(P[:,1]<y1)&(P[:,2]>z0)&(P[:,2]<z1)]
rows=[]
for hw in (15,30):
  for x in xs:
    Q=P[abs(P[:,0]-x)<hw]; c=sorted(section(np.c_[Q[:,1],Q[:,2]]),key=lambda c:-c['Z_mm3'])
    r=dict(fish=label,hw=hw,x=x,n=len(c),sumZ=sum(k['Z_mm3'] for k in c),maxZ=c[0]['Z_mm3'] if c else 0,maxZ_t=c[0]['tmax_um'] if c else 0,
           maxZ_ext=[list(map(float,c[0]['u_ext'])),list(map(float,c[0]['v_ext']))] if c else None)
    rows.append(r); print(f"{label} hw{hw} x={x:.0f} n={r['n']} sumZ={r['sumZ']:.2e} maxZ={r['maxZ']:.2e} t={r['maxZ_t']:.0f} ext(y,z)={r['maxZ_ext']}")
json.dump(rows,open(f"hsweep_{label}.json","w"),indent=0)
