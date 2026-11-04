import sys, struct, numpy as np
def load(fn):
    d=open(fn,'rb').read(); p=0
    while p+12<=len(d):
        t,ds,ms=struct.unpack_from('<III',d,p); body=d[p+12:p+12+ds]
        if t==0xFFFFFF3B:
            L=struct.unpack_from('<H',body,0)[0]; o=2+L+4
            F,P,N,D,S,T=struct.unpack_from('<6I',body,o); o+=24
            V=np.frombuffer(body,dtype='<f4',count=3*P,offset=o).reshape(P,3).astype(float); o+=12*P
            Fc=np.frombuffer(body,dtype='<u4',count=3*F,offset=o).reshape(F,3)
            return V,Fc,body[o+12*F:]
        p+=12+ds+((4-ds%4)%4)+ms+((4-ms%4)%4)
if __name__=='__main__':
    V,F,tail=load(sys.argv[1])
    print(V.shape,F.shape,'maxidx',F.max(),'tail',len(tail),tail[:16].hex())
    print('min',V.min(0),'max',V.max(0),'ext',V.max(0)-V.min(0))
    # edge manifoldness
    e=np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1)
    u,c=np.unique(e,axis=0,return_counts=True)
    print('edge use counts',np.bincount(c)[:5])
    el=np.linalg.norm(V[F[:,0]]-V[F[:,1]],axis=1); print('median edge',np.median(el))
    np.save(sys.argv[1]+'.V.npy',V); np.save(sys.argv[1]+'.F.npy',F)
