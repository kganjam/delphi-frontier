import itertools, math
g, rho = 9.81, 1.2
rows=[]
for m_g, R_mm, Phi, k in itertools.product([0.25,0.4,0.6],[4,5,6,8],[2.0,math.pi],[1.0,1.2,2.0]):
    m=m_g/1000; R=R_mm/1000; A=Phi*R**2
    vi=math.sqrt(m*g/(2*rho*A)); Pb=k*g*vi
    rows.append((Pb,m_g,R_mm,Phi,k))
rows.sort()
print("min",rows[0]);print("max",rows[-1])
c=[r for r in rows if r[1]==0.4 and r[2]==5 and r[3]==math.pi and r[4]==1.2][0]
print("central",c)
for f in (0.0069,0.0138):
    print(f, "min %.0f central %.0f max %.0f W/kg muscle"%(rows[0][0]/f,c[0]/f,rows[-1][0]/f))
print("ideal induced only, central geom, k=1:", g*math.sqrt(0.4e-3*g/(2*rho*math.pi*0.005**2)))
