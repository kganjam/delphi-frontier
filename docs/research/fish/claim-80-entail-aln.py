import json,sys
from Bio import SeqIO
from Bio.Align import PairwiseAligner, substitution_matrices
D=sys.argv[1]
def rd(f): return str(next(SeqIO.parse(f'{D}/{f}','fasta')).seq)
a=rd('UPI000188A62B.fa'); a2=rd('UPI00062E34B4.fa'); b=rd('NP_001008585.fa'); bq=rd('Q5PR35.fa')
h4=rd('Q8N370.fa'); h3=rd('O75387.fa'); h43=rd('Q8NBI5.fa'); s=rd('Q7ZUS0.fa')
print('lens a571',len(a),'a577',len(a2),'b(NP)',len(b),'b(Q5PR35)',len(bq),'hLAT4',len(h4),'hLAT3',len(h3),'hSLC43A3',len(h43),'short',len(s))
print('a[199]',a[194:205],a[199],'a2[199]',a2[199],'b[199]',b[194:205],b[199],'bq[199]',bq[199])
al=PairwiseAligner(); al.substitution_matrix=substitution_matrices.load('BLOSUM62'); al.open_gap_score=-10; al.extend_gap_score=-0.5; al.mode='global'
def aln(x,y):
    A=al.align(x,y)[0]; m={}; ident=0; cols=0
    for (s1,e1),(s2,e2) in zip(*A.aligned):
        for i,j in zip(range(s1,e1),range(s2,e2)):
            m[i]=j; cols+=1; ident+= x[i]==y[j]
    return m,ident,cols
for name,y in [('hLAT4 SLC43A2',h4),('hLAT3 SLC43A1',h3),('hSLC43A3',h43),('zf slc43a2b',b)]:
    for qn,q in [('chr15 a(571)',a),('chr10 b(NP_001008585)',b)]:
        if q is y: continue
        m,i,c=aln(q,y)
        print(f'{qn} vs {name}: identity {i}/{c} aligned = {100*i/c:.1f}% ; /query len {100*i/len(q):.1f}% ; /shorter {100*i/min(len(q),len(y)):.1f}%')
        if qn.startswith('chr15'):
            j=m.get(199); print('   pos200 ->',None if j is None else (j+1,y[j]), ' window a',a[192:207],' target',None if j is None else y[j-7:j+8])
            w=[(k,m.get(k)) for k in range(192,207)]; idw=sum(1 for k,jj in w if jj is not None and a[k]==y[jj]); print('   15-res window identity',idw,'/15')
# TM features human LAT4
for acc in ['Q8N370','O75387']:
    J=json.load(open(f'{D}/{acc}.json'))
    tm=[(f['location']['start']['value'],f['location']['end']['value'],f.get('description','')) for f in J['features'] if f['type'] in('Transmembrane','Topological domain')]
    print(acc,tm)
