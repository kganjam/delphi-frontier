"""Controls for the live-pool burn projection: a case it MUST flag, one it must NOT,
and the historical bug as a must-flag fixture."""
import io, json, sys, time, contextlib, os
sys.path.insert(0, "swarm")
import progress

NOW = time.time()
def run(crows, ctotal, csoon, state):
    progress.console_credit = lambda: (crows, ctotal, csoon)
    progress.credit = lambda: 0.0                      # the dead cloud pool, as in reality
    progress.q1 = lambda s: 0
    progress.sh = lambda *a, **k: "0"
    progress.STATE = state
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try: progress.main()
        except Exception as e: buf.write(f"ERROR {e}\n")
    return buf.getvalue()

EXP = "2026-11-07T00:00:00+00:00"
soon = {"tenant": "api_outlook2", "left": 195.69, "expires": EXP, "on": True}
rows = [soon]

# --- Arm A: MUST show a burn and a projection once a baseline exists -------------
st = f"{os.environ['TMPDIR'] if 'TMPDIR' in os.environ else '/tmp'}/ctl_a.json"
json.dump({"cbase_t": NOW - 3600, "cbase_total": 295.69, "claims": 0}, open(st, "w"))
a = run(rows, 195.69, soon, st)
bl = [l for l in a.splitlines() if "burn" in l or "EXPIRES" in l or "expire" in l]
okA = any("100.00/h observed" in l for l in a.splitlines())
print("A must show burn $100/h  ->", "PASS" if okA else "FAIL")
for l in bl: print("     ", l.strip())

# --- Arm B: MUST flag a burn too slow to finish ----------------------------------
json.dump({"cbase_t": NOW - 3600, "cbase_total": 195.79, "claims": 0}, open(st, "w"))
b = run(rows, 195.69, soon, st)
okB = any("live burn" in l and "below" in l for l in b.splitlines())
print("B must flag slow burn    ->", "PASS" if okB else "FAIL")
for l in b.splitlines():
    if "live burn" in l or "EXPIRES UNUSED" in l: print("     ", l.strip())

# --- Arm C: must NOT claim on-track when there is no readable deadline -----------
json.dump({"claims": 0}, open(st, "w"))
c = run([], 0.0, None, st)
okC = ("NOT reported as on-track" in c) and ("leftover $0" not in c)
print("C no deadline -> no on-track claim ->", "PASS" if okC else "FAIL")

# --- Arm D: the HISTORICAL BUG as a fixture. The old line read the cloud pool,
#            so with $195 live and $0 cloud it printed "$0/h NEEDED ... leftover $0".
#            The new line must never say that while money is at risk.
json.dump({"cbase_t": NOW - 3600, "cbase_total": 195.69, "claims": 0}, open(st, "w"))
d = run(rows, 195.69, soon, st)
okD = ("$0/h NEEDED" not in d) and ("leftover $0" not in d) and ("4.6" in d or "needed to spend" in d)
print("D old bug must not recur ->", "PASS" if okD else "FAIL")

print("\nCONTROLS", "PASS" if all([okA, okB, okC, okD]) else "FAIL")
sys.exit(0 if all([okA, okB, okC, okD]) else 1)
