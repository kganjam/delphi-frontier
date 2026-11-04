import sys,numpy as np; from scipy.spatial import cKDTree
B=np.load(sys.argv[1]).astype(float); H=np.load(sys.argv[2]).astype(float); s0=float(sys.argv[3])
rng=np.random.default_rng(0)
Hs=H[rng.choice(len(H),40000,replace=False)]
# init: scale s0, align min z (snout) and centre in x,y of head region
Bh=B[B[:,2]<B[:,2].min()+(H[:,2].max()-H[:,2].min())*s0]
R=np.eye(3); s=s0; t=np.array([np.median(Bh[:,0])-s*np.median(H[:,0]), np.median(Bh[:,1])-s*np.median(H[:,1]), Bh[:,2].min()-s*H[:,2].min()])
tree=cKDTree(Bh)
for it in range(60):
    X=s*Hs@R.T+t; d,i=tree.query(X); thr=np.percentile(d,80); m=d<thr
    A=Hs[m]; Y=Bh[i[m]]
    mA=A.mean(0); mY=Y.mean(0); Ac=A-mA; Yc=Y-mY
    U,S,Vt=np.linalg.svd(Yc.T@Ac); D=np.eye(3); D[2,2]=np.sign(np.linalg.det(U@Vt))
    R=U@D@Vt; s=(S*np.diag(D)).sum()/(Ac**2).sum(); t=mY-s*R@mA
    if it%10==0 or it==59: print(it,'scale',round(s,3),'median dist',round(np.median(d),1),'p80',round(thr,1))
print('R',np.round(R,3)); np.save('icp_'+sys.argv[4]+'.npy',np.concatenate([[s],t,R.ravel()]))
