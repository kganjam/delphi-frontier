import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import sys,subprocess,numpy as np
from base import basemesh
for fn in sys.argv[1:]:
    m=basemesh(fn); end=m['P']+m['ds']; fs=m['face_start']
    of=fn.replace('.u3d','.faces')
    r=subprocess.run(['./ac',fn,str(fs),str(end-fs),str(m['F']),str(m['Np']),of],capture_output=True,text=True); print(fn,r.stderr.strip())
    np.save(fn.replace('.u3d','_pos.npy'),m['pos'])
    T=np.fromfile(of,dtype='<u4').reshape(-1,3)
    if T.max()<m['Np']:
        e=np.sort(np.concatenate([T[:,[0,1]],T[:,[1,2]],T[:,[2,0]]]),axis=1)
        _,c=np.unique(e[:,0].astype(np.int64)*10**7+e[:,1],return_counts=True)
        print('  edge-share histogram',np.bincount(c)[:5],'unused verts',m['Np']-len(np.unique(T)))
