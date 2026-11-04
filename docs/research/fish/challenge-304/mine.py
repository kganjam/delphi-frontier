import sys,numpy as np
sys.path.insert(0,sys.argv[1]); from slicer import load,slice_mesh
import secs
P,T=load(sys.argv[2])
def props(loops):
    import matplotlib.path as mp
    paths=[mp.Path(l) for l in loops]; A=Su=Sv=Iuu=Ivv=Iuv=0.0
    for i,l in enumerate(loops):
        depth=sum(paths[j].contains_point(l[0]) for j in range(len(loops)) if j!=i)
        u,v=l[:-1,0],l[:-1,1]; u1,v1=np.roll(u,-1),np.roll(v,-1); c=u*v1-u1*v
        a=c.sum()/2; s=(1 if depth%2==0 else -1)*np.sign(a)
        A+=s*a; Su+=s*((u+u1)*c).sum()/6; Sv+=s*((v+v1)*c).sum()/6
        Iuu+=s*((u*u+u*u1+u1*u1)*c).sum()/12; Ivv+=s*((v*v+v*v1+v1*v1)*c).sum()/12
        Iuv+=s*((u*v1+2*u*v+2*u1*v1+u1*v)*c).sum()/24
    cu,cv=Su/A,Sv/A; Iuu-=A*cu*cu; Ivv-=A*cv*cv; Iuv-=A*cu*cv
    pts=np.concatenate(loops); du=pts[:,0]-cu; dv=pts[:,1]-cv
    # u = y (lateral), v = z (AP). Moment about z => stress along u.
    Z_naive=Iuu/np.abs(du).max()
    a,b=np.linalg.solve([[Iuu,Iuv],[Iuv,Ivv]],[1.0,0.0])   # unrestrained: sigma=a du + b dv, int sigma du =M=1, int sigma dv =0
    Z_unsym=1/np.abs(a*du+b*dv).max()
    # minimum over moment directions
    Zs=[]
    for th in np.linspace(0,np.pi,181):
        m=np.array([np.cos(th),np.sin(th)]); a2,b2=np.linalg.solve([[Iuu,Iuv],[Iuv,Ivv]],m); Zs.append(1/np.abs(a2*du+b2*dv).max())
    ang=0.5*np.degrees(np.arctan2(-2*Iuv,Iuu-Ivv))
    return A,Z_naive,Z_unsym,min(Zs),ang,(np.ptp(pts[:,0]),np.ptp(pts[:,1]))
side=sys.argv[3]; ylo,yhi=map(float,sys.argv[4].split(',')); zlo,zhi=map(float,sys.argv[5].split(','))
k=0.968
for x in np.arange(float(sys.argv[6]),float(sys.argv[7])+1,float(sys.argv[8])):
    r=secs.section(P,T,0,x,{1:(ylo,yhi),2:(zlo,zhi)},1)
    if r['A']<=0: print(side,x,'empty cut',r['cut']); continue
    A,Zn,Zu,Zm,ang,ext=props(r['loops'])
    f=k**3/1e9
    print(f"{side} x={x:.0f} loops={len(r['loops'])} cut={r['cut']} A={A*k*k/1e6:.4f} Znaive={Zn*f:.3e} Zunsym={Zu*f:.3e} Zmin_anydir={Zm*f:.3e} pr_ang={ang:.0f} ext_y,z={ext[0]*k/1e3:.3f},{ext[1]*k/1e3:.3f} loopA={[round(abs(0.5*(l[:-1,0]*np.roll(l[:-1,1],-1)-np.roll(l[:-1,0],-1)*l[:-1,1]).sum())*k*k/1e6,4) for l in r['loops']]}")
