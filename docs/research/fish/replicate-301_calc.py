from math import sqrt
g=9.81; rho=1.225; mb=0.40e-3; WM=142.7; S=1070e-6
sc=(0.8*1050+0.2*1557)*120e-6
def short(CL=1.07,s_bl=2,eta=0.37,fm=0.6,sig=sc,wm=WM):
    M=mb+sig*S; V=sqrt(2*M*g/(rho*S*CL)); Pb=V**3/(4*s_bl*0.04*eta); return V,Pb,Pb*M/(fm*mb),Pb*M/(fm*mb)/wm,M
for CL in (1.0,1.07,1.1):
    V,Pb,Pm,r,M=short(CL); print(f'CL {CL}: M={M*1e3:.4f} g V={V:.4f} Pb={Pb:.2f} W/kg Pm={Pm:.1f} W/kg ratio={r:.3f}')
b=short()[3]; print('closure CL',1.07*b**(2/3), ' ratio to 1.1:',1.07*b**(2/3)/1.1)
print('factor-2 tests at CL1.07 baseline',b)
print(' CL x2',short(CL=2.14)[3]); print(' s x2',short(s_bl=4)[3]); print(' WM x2',short(wm=2*WM)[3])
print(' eta x2 (0.74)',short(eta=0.74)[3]); print(' sigma /2',short(sig=sc/2)[3]); print(' sigma 0',short(sig=0)[3])
print(' fm ->1.0 (max)',short(fm=1.0)[3])
