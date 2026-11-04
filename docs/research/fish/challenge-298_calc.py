import math
# inputs read from origin/main artifacts/print/design/{C,B}.json biological_design_SI
D={"Cyp":dict(b=0.274524,S=0.00889333,share=0.7599,w=0.03351169717517026,T3=8.737449351660992),
   "Exo":dict(b=0.322657,S=0.00835137,share=0.9183,w=0.02792218494101567,T3=14.941748211720746)}
for n,d in D.items():
    A=d["share"]*d["S"]/2            # one pectoral fin area, recomputed from Table I S and Table IV share
    for wf in (0,0.5,1.0,1.5):
        w=d["w"]*wf; L=(d["b"]-w)/2; s=L*L/A; k=d["T3"]/s
        print(f"{n} w x{wf}: A={A:.7f} L={L:.5f} single={s:.3f} k={k:.3f} bar3.0={3/k:.3f} bar9={9/k:.2f} theta_meanfin={math.degrees(2/s):.1f}")
    print(f"{n} pair={d['b']**2/(2*A):.3f} whole={d['b']**2/d['S']:.3f}")
# pure-doubling hypothesis
print("k=2 exact: bar3.0 =",3/2, "theta", math.degrees(2/1.5))
for ar in (3/2.638,3/2.033): print("theta", round(math.degrees(2/ar),1))
