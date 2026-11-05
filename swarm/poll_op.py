"""Poll a Nebius operation, reading the status wherever that tool puts it.

The batch submit_* tools put it at the top level as `status`; the *_native tools nest it under
`operation.status` and leave the top-level key absent. A poller that reads only the top level
prints `None` forever for a native job that has already succeeded -- measured on
op-6b0768352aa8cfa5, which was SUCCEEDED while the poller logged None.
"""
import sys, json, time
sys.path.insert(0, '/tmp/claude-1000/-home-ubuntu-git-morphoswarm/507442cb-0fa9-4ade-b46c-d7b940105d10/scratchpad')
import nbx
op = sys.argv[1]
for i in range(300):
    try:
        r = nbx.call("get_operation", {"operation_id": op})
    except Exception as e:
        print(f"{time.strftime('%H:%M:%S')} poll error {type(e).__name__}", flush=True)
        time.sleep(30); continue
    st = r.get("status") or r.get("state") or (r.get("operation") or {}).get("status")
    print(f"{time.strftime('%H:%M:%S')} {st} {r.get('phase','')}".rstrip(), flush=True)
    if str(st).upper() in ("SUCCEEDED","FAILED","CANCELLED","COMPLETED"):
        print(json.dumps(r)[:600], flush=True); break
    time.sleep(25)
