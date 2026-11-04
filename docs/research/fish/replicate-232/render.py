import sys,numpy as np; from PIL import Image
sys.path.insert(0,'.'); from slicer import load
stem=sys.argv[1]; box=[float(v) for v in sys.argv[2].split(',')]  # xmin,xmax,ymin,ymax,zmin,zmax
view=sys.argv[3]; out=sys.argv[4]; scale=float(sys.argv[5]) if len(sys.argv)>5 else 4
P,T=load(stem)
C=P[T].mean(1); m=np.all((C>=[box[0],box[2],box[4]])&(C<=[box[1],box[3],box[5]]),1); T=T[m]
# view: 'lat' looks along +y (image axes z right, x down); 'dors' looks along x; 'front' looks along z
ax={'lat':(2,0,1),'latR':(2,0,-1),'dors':(2,1,0),'front':(1,0,2)}[view]
iu,iv,iw=ax[0],ax[1],abs(ax[2]); sgnw=-1 if ax[2]<0 else 1
V=P[T]; n=np.cross(V[:,1]-V[:,0],V[:,2]-V[:,0]); n/=np.linalg.norm(n,axis=1,keepdims=True)+1e-12
shade=np.abs(n[:,iw])
u0,v0=box[[0,2,4][iu]//1] if False else None,None
lo=np.array([box[0],box[2],box[4]]); hi=np.array([box[1],box[3],box[5]])
W=int((hi[iu]-lo[iu])*scale)+1; H=int((hi[iv]-lo[iv])*scale)+1
zb=np.full((H,W),-np.inf); img=np.ones((H,W))
# sample points on triangles densely
k=6; 
for a in range(k+1):
  for b in range(k+1-a):
    w=np.array([a,b,k-a-b])/k; p=(V*w[None,:,None]).sum(1)
    u=((p[:,iu]-lo[iu])*scale).astype(int); v=((p[:,iv]-lo[iv])*scale).astype(int); d=sgnw*p[:,iw]
    ok=(u>=0)&(u<W)&(v>=0)&(v<H); u,v,d,s=u[ok],v[ok],d[ok],shade[ok]
    o=np.argsort(d); u,v,d,s=u[o],v[o],d[o],s[o]
    upd=d>zb[v,u]; zb[v[upd],u[upd]]=d[upd]; img[v[upd],u[upd]]=0.15+0.85*s[upd]
Image.fromarray((img*255).astype(np.uint8)).save(out); print(W,H,'pixels per unit',scale)
