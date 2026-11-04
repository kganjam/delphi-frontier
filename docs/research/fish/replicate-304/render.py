import sys, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def render(V,F,keepF,view,res,out,title='',marks=None,lab=None):
    # view: (right_vec, up_vec) ; depth = cross ; viewer looks along -depth
    r,u=np.array(view[0],float),np.array(view[1],float); d=np.cross(r,u)
    Fk=F[keepF]
    # sample points on triangles: centroids + vertices + edge midpoints
    A,B,C=V[Fk[:,0]],V[Fk[:,1]],V[Fk[:,2]]
    n=np.cross(B-A,C-A); n/=np.linalg.norm(n,axis=1,keepdims=True)+1e-12
    pts=[];nrm=[]
    for w in [(1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6),(.5,.5,0),(0,.5,.5),(.5,0,.5)]:
        pts.append(w[0]*A+w[1]*B+w[2]*C); nrm.append(n)
    P=np.concatenate(pts); N=np.concatenate(nrm)
    X=P@r; Y=P@u; D=P@d
    x0,y0=X.min(),Y.min(); W=int((X.max()-x0)/res)+3; H=int((Y.max()-y0)/res)+3
    ix=((X-x0)/res).astype(int); iy=((Y-y0)/res).astype(int)
    shade=np.abs(N@d)*0.8+0.2
    zb=np.full((H,W),-np.inf); img=np.ones((H,W))
    o=np.argsort(D)  # far to near; later writes win
    for dx in (0,1):
        for dy in (0,1):
            jx=np.clip(ix+dx,0,W-1); jy=np.clip(iy+dy,0,H-1)
            img[jy[o],jx[o]]=shade[o]
    fig=plt.figure(figsize=(W/60+2,H/60+2)); a=fig.gca()
    a.imshow(img,cmap='gray',origin='lower',extent=[x0,x0+W*res,y0,y0+H*res],vmin=0,vmax=1)
    if marks is not None:
        for p,t in marks: a.plot(p@r,p@u,'r+',ms=12); a.text(p@r,p@u,t,color='r')
    a.grid(True,alpha=0.4); a.set_title(title); plt.xticks(rotation=90)
    a.xaxis.set_major_locator(plt.MultipleLocator(250)); a.yaxis.set_major_locator(plt.MultipleLocator(250))
    plt.tight_layout(); plt.savefig(out,dpi=60); plt.close()
if __name__=='__main__':
    fn=sys.argv[1]; V=np.load(fn+'.V.npy'); F=np.load(fn+'.F.npy')
    box=[float(x) for x in sys.argv[2].split(',')]  # xmin,xmax,ymin,ymax,zmin,zmax
    c=V[F].mean(1)
    keep=(c[:,0]>box[0])&(c[:,0]<box[1])&(c[:,1]>box[2])&(c[:,1]<box[3])&(c[:,2]>box[4])&(c[:,2]<box[5])
    views={'latR':([0,0,-1],[-1,0,0]),'latL':([0,0,1],[-1,0,0]),'ven':([0,0,-1],[0,1,0]),'front':([0,-1,0],[-1,0,0]),'back':([0,1,0],[-1,0,0]),'medR':([0,0,1],[-1,0,0])}
    v=sys.argv[3]; render(V,F,keep,views[v],float(sys.argv[5]) if len(sys.argv)>5 else 8,sys.argv[4],v)
