"""Probe the Nebius job-log transport: which line lengths survive, and how many lines are retained."""
import hashlib, os
for i in range(150):
    print(f"PROBE-SEQ {i}", flush=True)
for n in (4096, 65536, 262144, 1048576, 2097152):
    s = (hashlib.sha256(str(n).encode()).hexdigest() * (n // 64 + 1))[:n]
    print(f"PROBE-LEN {n} {hashlib.sha256(s.encode()).hexdigest()[:16]} {s}", flush=True)
print("PROBE-END", flush=True)
