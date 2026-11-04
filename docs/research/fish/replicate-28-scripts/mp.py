import metapredict as meta, numpy as np
def rd(f): return ''.join(l.strip() for l in open(f) if not l.startswith('>'))
k=rd('dl/Q6PFU3.fasta'); a=rd('dl/A0ACM8QEN9.fasta')
for lab,s in (('kcnk5b',k),('and2',a),('and2 24-end',a[23:]),('kcnk5b 251-end',k[250:])):
    d=np.array(meta.predict_disorder(s))
    idr=meta.predict_disorder_domains(s).disordered_domain_boundaries
    print(lab,len(s),'mean=%.3f frac>=0.5=%.3f'%(d.mean(),(d>=0.5).mean()),'IDRs',idr)
