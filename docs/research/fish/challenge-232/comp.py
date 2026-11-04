import sys, numpy as np; sys.path.insert(0, sys.argv[1]); from section import section
P=np.load(sys.argv[2])["P"]; x0,x1,z0,z1=map(float,sys.argv[3].split(",")); ys=[float(v) for v in sys.argv[4].split(",")]; hw=float(sys.argv[5])
# midline estimate from trunk ribs/vertebrae
T=P[(P[:,2]>8000)&(P[:,2]<14000)]; print("trunk mean y %.0f median %.0f"%(T[:,1].mean(),np.median(T[:,1])))
P=P[(P[:,0]>x0)&(P[:,0]<x1)&(P[:,2]>z0)&(P[:,2]<z1)]
for y in ys:
    Q=P[abs(P[:,1]-y)<hw]; c=sorted(section(np.c_[Q[:,0],Q[:,2]]),key=lambda c:-c['Z_mm3'])
    print(f"y={y:.0f}: "+" | ".join(f"Z{k['Z_mm3']:.1e} x{k['u_ext'][0]:.0f}-{k['u_ext'][1]:.0f} z{k['v_ext'][0]:.0f}-{k['v_ext'][1]:.0f} t{k['tmax_um']:.0f}" for k in c[:5]))
