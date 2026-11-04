import numpy as np
def load(stem):
    P=np.load(stem+'_pos.npy').astype(np.float64); T=np.fromfile(stem+'.faces',dtype='<u4').reshape(-1,3).astype(np.int64); return P,T
def slice_mesh(P,T,n,d):
    """intersect mesh with plane n.x=d; returns segments array (k,2,3)"""
    n=np.asarray(n,float); n/=np.linalg.norm(n)
    s=P@n-d; S=s[T]
    sg=np.sign(S); sg[sg==0]=1e-9
    cross=~((S>0).all(1)|(S<0).all(1))
    Tc=T[cross]; Sc=S[cross]
    segs=[]
    for k,(a,b) in enumerate([(0,1),(1,2),(2,0)]):
        pass
    pts=[]
    E=[(0,1),(1,2),(2,0)]
    out=np.zeros((len(Tc),2,3)); cnt=np.zeros(len(Tc),int)
    for a,b in E:
        sa=Sc[:,a]; sb=Sc[:,b]; m=(sa>0)!=(sb>0)
        t=sa[m]/(sa[m]-sb[m]); pa=P[Tc[m,a]]; pb=P[Tc[m,b]]
        x=pa+(pb-pa)*t[:,None]; idx=np.where(m)[0]
        out[idx,np.minimum(cnt[idx],1)]=x; cnt[idx]+=1
    return out[cnt==2]
def frame(n):
    n=np.asarray(n,float); n/=np.linalg.norm(n)
    a=np.array([1,0,0.]) if abs(n[0])<0.9 else np.array([0,1,0.])
    u=np.cross(n,a); u/=np.linalg.norm(u); v=np.cross(n,u); return u,v
def to2d(segs,n,origin=None):
    u,v=frame(n); return np.stack([segs@u,segs@v],-1),u,v
def loops(seg2,tol=1e-6):
    """chain segments into closed loops using endpoint hashing"""
    from collections import defaultdict
    key=lambda p:(round(p[0]/tol),round(p[1]/tol))
    adj=defaultdict(list)
    for i,(a,b) in enumerate(seg2):
        adj[key(a)].append((i,0)); adj[key(b)].append((i,1))
    used=np.zeros(len(seg2),bool); L=[]
    for i in range(len(seg2)):
        if used[i]: continue
        used[i]=True; poly=[seg2[i][0],seg2[i][1]]; cur=seg2[i][1]; start=key(seg2[i][0])
        while True:
            k=key(cur)
            if k==start: break
            nxt=None
            for j,e in adj[k]:
                if not used[j]: nxt=(j,e); break
            if nxt is None: break
            j,e=nxt; used[j]=True; cur=seg2[j][1-e]; poly.append(cur)
        L.append(np.array(poly))
    return L
def secprops(L):
    """area-weighted props with signed shoelace; loops orientation arbitrary -> use even-odd via nesting"""
    # compute signed area per loop, then determine nesting depth by point-in-polygon
    import matplotlib.path as mp
    closed=[l for l in L if len(l)>3 and np.allclose(l[0],l[-1],atol=1e-3)]
    paths=[mp.Path(l) for l in closed]
    res=[]
    for i,l in enumerate(closed):
        depth=sum(paths[j].contains_point(l[0]) for j in range(len(closed)) if j!=i)
        x,y=l[:-1,0],l[:-1,1]; x1,y1=np.roll(x,-1),np.roll(y,-1); c=x*y1-x1*y
        A=c.sum()/2; Sx=((x+x1)*c).sum()/6; Sy=((y+y1)*c).sum()/6
        Ixx=((y*y+y*y1+y1*y1)*c).sum()/12; Iyy=((x*x+x*x1+x1*x1)*c).sum()/12; Ixy=((x*y1+2*x*y+2*x1*y1+x1*y)*c).sum()/24
        sgn=(1 if depth%2==0 else -1)*np.sign(A)
        res.append(dict(loop=l,depth=depth,A=sgn*A,Sx=sgn*Sx,Sy=sgn*Sy,Ixx=sgn*Ixx,Iyy=sgn*Iyy,Ixy=sgn*Ixy))
    return res,len(L)-len(closed)
