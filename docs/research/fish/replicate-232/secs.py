import sys,json,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, matplotlib.path as mp
sys.path.insert(0,'.'); from slicer import load,slice_mesh
def section(P,T,axis,val,crop,ax_bend,tol=1e-4):
    """axis: plane normal index; crop: dict idx->(lo,hi) on in-plane coords; ax_bend: in-plane coord index along which bending depth is measured"""
    n=np.eye(3)[axis]; sg=slice_mesh(P,T,n,val)
    o=[i for i in range(3) if i!=axis]
    s2=sg[:,:,o]
    # chain
    from collections import defaultdict
    q=lambda p:(int(round(p[0]/tol)),int(round(p[1]/tol)))
    adj=defaultdict(list)
    for i,(a,b) in enumerate(s2): adj[q(a)].append((i,0)); adj[q(b)].append((i,1))
    used=np.zeros(len(s2),bool); loops=[]; openl=0
    for i in range(len(s2)):
        if used[i]: continue
        used[i]=True; poly=[s2[i][0],s2[i][1]]; cur=s2[i][1]; st=q(s2[i][0]); closed=False
        for _ in range(10**6):
            k=q(cur)
            if k==st: closed=True; break
            nx=next(((j,e) for j,e in adj[k] if not used[j]),None)
            if nx is None: break
            j,e=nx; used[j]=True; cur=s2[j][1-e]; poly.append(cur)
        if closed: loops.append(np.array(poly))
        else: openl+=1
    # crop
    keep=[];cut=0
    for l in loops:
        ins=np.ones(len(l),bool)
        for k,(lo,hi) in crop.items():
            c=o.index(k); ins&=(l[:,c]>=lo)&(l[:,c]<=hi)
        if ins.all(): keep.append(l)
        elif ins.any(): cut+=1
    paths=[mp.Path(l) for l in keep]
    A=Sx=Sy=Ixx=Iyy=Ixy=0.0
    for i,l in enumerate(keep):
        depth=sum(paths[j].contains_point(l[0]) for j in range(len(keep)) if j!=i)
        x,y=l[:-1,0],l[:-1,1]; x1,y1=np.roll(x,-1),np.roll(y,-1); c=x*y1-x1*y
        a=c.sum()/2; sgn=(1 if depth%2==0 else -1)*np.sign(a)
        A+=sgn*a; Sx+=sgn*((x+x1)*c).sum()/6; Sy+=sgn*((y+y1)*c).sum()/6
        Iyy+=sgn*((x*x+x*x1+x1*x1)*c).sum()/12; Ixx+=sgn*((y*y+y*y1+y1*y1)*c).sum()/12
        Ixy+=sgn*((x*y1+2*x*y+2*x1*y1+x1*y)*c).sum()/24
    if A<=0: return dict(A=0,loops=keep,cut=cut,open=openl,o=o)
    cx,cy=Sx/A,Sy/A
    Ic_x2=Iyy-A*cx*cx   # int (u-cx)^2 dA  (u = first in-plane coord o[0])
    Ic_y2=Ixx-A*cy*cy   # int (v-cy)^2 dA  (v = o[1])
    Ic_xy=Ixy-A*cx*cy
    avg=(Ic_x2+Ic_y2)/2; R=np.sqrt(((Ic_x2-Ic_y2)/2)**2+Ic_xy**2)
    allp=np.concatenate(keep)
    if ax_bend==o[0]: I=Ic_x2; cmax=np.abs(allp[:,0]-cx).max()
    else: I=Ic_y2; cmax=np.abs(allp[:,1]-cy).max()
    return dict(A=A,c=(cx,cy),I=I,cmax=cmax,Z=I/cmax,Imin=avg-R,Imax=avg+R,loops=keep,cut=cut,open=openl,o=o,
                ext=(np.ptp(allp[:,0]),np.ptp(allp[:,1])))
def deq(Z): return (32*Z/np.pi)**(1/3)
if __name__=='__main__':
    cfg=json.load(open(sys.argv[1])); P,T=load(cfg['stem']); k=cfg['um_per_unit']
    res=[]; n=len(cfg['vals']); fig,axs=plt.subplots(1,n,figsize=(5*n,5),squeeze=False)
    for a,v in zip(axs[0],cfg['vals']):
        r=section(P,T,cfg['axis'],v,{int(i):tuple(b) for i,b in cfg['crop'].items()},cfg['bend'])
        for l in r['loops']: a.plot(l[:,1],l[:,0],'k-',lw=0.7)
        a.set_aspect('equal'); a.set_xlabel('xyz'[r['o'][1]]); a.set_ylabel('xyz'[r['o'][0]]); a.invert_yaxis()
        if r['A']>0:
            Aum=r['A']*k*k; Zum=r['Z']*k**3; d=deq(Zum)
            a.plot(r['c'][1],r['c'][0],'r+'); a.set_title(f"{'xyz'[cfg['axis']]}={v} A={Aum/1e6:.4f}mm2 Z={Zum/1e9:.2e}mm3 deq={d/1e3:.3f}mm",fontsize=8)
            res.append(dict(val=v,A_mm2=Aum/1e6,I_mm4=r['I']*k**4/1e12,c_mm=r['cmax']*k/1e3,Z_mm3=Zum/1e9,deq_mm=d/1e3,
                            Imin_mm4=r['Imin']*k**4/1e12,Imax_mm4=r['Imax']*k**4/1e12,ext_mm=[e*k/1e3 for e in r['ext']],nloops=len(r['loops']),cut=r['cut'],open=r['open']))
        else: res.append(dict(val=v,A_mm2=0,cut=r['cut'],open=r['open']))
    fig.savefig(cfg['png'],dpi=70)
    for r in res: print(json.dumps({k:(round(v,5) if isinstance(v,float) else v) for k,v in r.items()}))
