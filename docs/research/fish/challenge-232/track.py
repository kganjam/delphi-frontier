import sys, numpy as np; sys.path.insert(0, sys.argv[1]); from section import section
P=np.load(sys.argv[2])["P"]; x0,x1,z0,z1=map(float,sys.argv[3].split(",")); ys=[float(v) for v in sys.argv[4].split(",")]; band=list(map(float,sys.argv[5].split(",")))
P=P[(P[:,0]>x0)&(P[:,0]<x1)&(P[:,2]>z0)&(P[:,2]<z1)]
for hw in (15,30):
  for y in ys:
    Q=P[abs(P[:,1]-y)<hw]; c=section(np.c_[Q[:,0],Q[:,2]])
    v=[k for k in c if (k['uc']>band[0]) and (k['uc']<band[1])]; v=sorted(v,key=lambda k:-k['Z_mm3'])
    print(f"hw{hw} y={y:.0f}: ventral-band comps (centroid x in {band}): "+" | ".join(f"Z{k['Z_mm3']:.1e} x{k['u_ext'][0]:.0f}-{k['u_ext'][1]:.0f} z{k['v_ext'][0]:.0f}-{k['v_ext'][1]:.0f}" for k in v[:3]))
