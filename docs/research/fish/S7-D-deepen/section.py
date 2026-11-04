"""Section properties of bone cut by a plane, from a surface-vertex cloud. CALCULATED."""
import numpy as np
from scipy import ndimage as ndi
def section(Q2, px=10.0, close_um=30.0):
    """Q2: (n,2) in-plane points (u=bending-stress direction, v=other). Returns list of component dicts."""
    if len(Q2)<10: return []
    lo=Q2.min(0)-80; idx=np.floor((Q2-lo)/px).astype(int); sh=idx.max(0)+8
    g=np.zeros(sh,bool); g[idx[:,0],idx[:,1]]=True
    r=int(round(close_um/px)); st=ndi.generate_binary_structure(2,1); st=ndi.iterate_structure(st,r)
    # dilate -> fill -> erode (robust closing of a sampled outline)
    f=ndi.binary_erosion(ndi.binary_fill_holes(ndi.binary_dilation(g,structure=st)),structure=st,border_value=0)
    f|=g
    lab,n=ndi.label(f); out=[]
    dt=ndi.distance_transform_edt(f)*px
    for k in range(1,n+1):
        m=lab==k; A=m.sum()*px*px
        if A<2000: continue   # <0.002 mm^2 ignored (noise)
        ii,jj=np.nonzero(m); u=(ii+0.5)*px+lo[0]; v=(jj+0.5)*px+lo[1]
        uc=u.mean(); vc=v.mean(); I=((u-uc)**2).sum()*px*px; c=np.abs(u-uc).max()+px/2
        out.append(dict(A_mm2=A*1e-6, uc=uc, vc=vc, I_mm4=I*1e-12, Z_mm3=I/c*1e-9, c_um=c,
                        tmax_um=2*dt[m].max(), u_ext=(u.min(),u.max()), v_ext=(v.min(),v.max())))
    return out
if __name__=="__main__":
    # validation on synthetic surfaces: solid rod d=260 um, plate 100x1000 um, sampled like the mesh (26 um spacing)
    rng=np.random.default_rng(0)
    th=rng.uniform(0,2*np.pi,400); R=130; circ=np.c_[R*np.cos(th),R*np.sin(th)]
    s=section(circ); Zt=np.pi*260**3/32*1e-9
    print("rod d=260: Z est %.3e true %.3e ; A est %.4f true %.4f ; tmax %.0f"%(s[0]['Z_mm3'],Zt,s[0]['A_mm2'],np.pi*R*R*1e-6,s[0]['tmax_um']))
    for t in (60,100,200):
        L=1000; per=[]
        for x in np.arange(-L/2,L/2,26/2): per += [[t/2,x],[-t/2,x]]
        for y in np.arange(-t/2,t/2,13): per += [[y,-L/2],[y,L/2]]
        s=section(np.array(per)); Zt=L*t*t/6*1e-9
        print(f"plate t={t} (bending across thickness): Z est {s[0]['Z_mm3']:.3e} true {Zt:.3e}; A {s[0]['A_mm2']:.4f} true {L*t*1e-6:.4f}; tmax {s[0]['tmax_um']:.0f}")
