"""Recover the sweep result from a Nebius job's stdout.

The job writes gzip+base64 between BEGIN_RESULT_B64 and END_RESULT_B64 because the
S3 volume was refused by the API (`spec.volumes[0].s3_config.endpoint: value is
required`) and no endpoint was available. Reads a log file on stdin or by path.
"""
import base64, gzip, json, re, sys

text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
m = re.search(r"BEGIN_RESULT_B64 len=(\d+)\n(.*?)\nEND_RESULT_B64", text, re.S)
if not m:
    sys.exit("no BEGIN_RESULT_B64 .. END_RESULT_B64 block found in the log")
declared = int(m.group(1))
blob = re.sub(r"\s+", "", m.group(2))
if len(blob) != declared:
    sys.exit(f"blob is {len(blob)} chars, the job said {declared}: the log is truncated")
obj = json.loads(gzip.decompress(base64.b64decode(blob)))
out = sys.argv[2] if len(sys.argv) > 2 else "control-channels-raw.json"
json.dump(obj, open(out, "w"))
print(f"wrote {out}: {len(obj['rows'])} rows, K={obj['K']}, "
      f"{len(obj['n_values'])} N-values, {obj['elapsed_s']:.0f}s wall clock, "
      f"{len(obj.get('controls', []))} controls")
