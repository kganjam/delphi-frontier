import sys, numpy as np
sys.path.insert(0, sys.argv[1]); import u3d
for src in sys.argv[2:]:
    d=open(src,"rb").read()
    for t,b,o in u3d.blocks(d):
        if t==0xFFFFFF3B: blk=b
    bs=u3d.BS(blk); bs.string(); bs.u32()
    fc,pc,nc,dc,sc,tc=[bs.u32() for _ in range(6)]
    P=np.array([bs.f32() for _ in range(pc*3)]).reshape(-1,3)
    F=[]
    for i in range(8000):
        bs.cu32(1); F.append([bs.cu32(u3d.STATIC+pc) for k in range(3)])
    F=np.array(F)
    e=np.linalg.norm(P[F[:,0]]-P[F[:,1]],axis=1)
    out=src.split("/")[-1]+".pos.npz"; np.savez(out,P=P,F8000=F)
    print(src, "faces",fc,"pos",pc,"bbox",P.min(0).round(1),P.max(0).round(1),"edge median",np.median(e).round(2),"p90",np.percentile(e,90).round(2),flush=True)
