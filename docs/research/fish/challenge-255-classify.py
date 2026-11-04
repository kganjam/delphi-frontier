A="2 4 6 7 8 23 38 39 40 73 74 75 77 80 86 147 160 179 182 198 202 204 205 209 215 219 229 233 237 238 239 243".split()
D="9 10 14 15 16 18 21 25 30 69 70 71 87 88 110 139 175 188 200 236".split()
C="17 19 20 22 26 27 79 81 83 185 186 187 207 208 210 211 216 217 218 222 223 242".split()
import re
ids=[l.split('|')[1].strip() for l in open(__import__('sys').argv[1]) if re.match(r'^\| \d',l)]
B=[i for i in ids if i not in A+D+C]
assert not set(A)&set(D) and not set(A)&set(C) and not set(D)&set(C)
assert all(i in ids for i in A+D+C)
n=len(ids)
for k,v in [('A literature-checkable biology',A),('D computed property of a natural object',D),('C method/tool/scope/audit',C),('B design-specific computed',B)]:
    print(f"{k}: {len(v)}/{n} = {100*len(v)/n:.1f}%")
# selector from swarm/evidence.py
rows={l.split('|')[1].strip():l.split('|')[3].strip() for l in open(__import__('sys').argv[1]) if re.match(r'^\| \d',l)}
excl=[i for i,s in rows.items() if re.search(r'(scoped to|could not|we searched|this project|recomputed here|verified here|SCOPE:|LIMITATION)',s,re.I) or re.search(r'(despite|although|notwithstanding)',s,re.I)]
print("selector excludes (on truncated text):",len(excl), excl)
neg=[i for i in A if re.search(r'\b(NOT|NO|never|cannot|absent)\b',rows[i],re.I)]
print("A claims with negation in stated text:",len(neg),"/",len(A),neg)
lit=[i for i in B if re.search(r'(measured|\b[A-Z][a-z]+( et al\.?| &| and)? ?\(?(19|20)\d\d|Ucrit|U_crit|EMG|published|bluegill|Daane|Kyriakatos|Alben)',rows[i])]
print("B claims whose stated text names a measured/published input:",len(lit),"/",len(B))
