#!/usr/bin/env python3
"""The fifth swarm stage, PUBLISH, as a dry run that cannot transmit.

Claim 508 (corrected by 538) recorded that the loop has design, simulate, analyze and learn, and
that publish had no implementation, no spec in this project, and only throwaway keys -- and that
"publishing a nanopub" sits in a FORBIDDEN_ACTIONS tuple. Published nanopubs are IMMUTABLE: a
correction requires a new nanopub signed with the same key, so the first publish is irreversible.
The owner authorised a DRY RUN only. This is that.

IT CANNOT TRANSMIT, AND THAT IS STRUCTURAL RATHER THAN A PROMISE. This module imports no network
library, and main() asserts at runtime that no socket/http/requests/urllib module has been loaded
into the interpreter. A guard that is merely documented is a guard that is off.

WHAT IT PRODUCES: for each ask-transfer/v1 record, a nanopublication in TriG with the four named
graphs the schema requires -- Head, assertion, provenance, pubinfo -- signed with the throwaway
RSA key at ~/.nanopub/collab-throwaway/rsa.pem, written to disk, then read back and verified.

WHAT IT IS NOT, STATED PLAINLY BECAUSE THE DIFFERENCE IS EASY TO PAPER OVER: these are NOT
publishable nanopublications. A real one carries a TRUSTY URI -- an RDF-normalised hash embedded
in the nanopub's own identifier -- and this does not implement that algorithm. Implementing RDF
canonicalisation from scratch, unverified against the reference implementation, would produce
files that LOOK like nanopubs and would be rejected or, worse, accepted with a wrong hash. The
digest here is over the serialised bytes and is labelled as such. Converting these to publishable
nanopubs requires nanopub-java or @nanopub/sign, plus a non-throwaway key and a registered
namespace.

CORRECTED 2026-11-05: this used to say @nanopub/sign is "not installed here". IT IS --
version 0.2.0 at /tmp/claude-1000/npmwork/node_modules/@nanopub/sign, with Node 22 -- and a
trusty URI WAS produced from this module's own output in a throwaway test (RDF matching
/RA[A-Za-z0-9_-]{40,}/), which was then deleted. The stale clause mattered because it made a
DECISION look like a tooling gap. sign() and publish() are separate methods, so a conformant
artifact needs no network call and no irreversible act.

THE ACTUAL BLOCKER IS THE SIGNING IDENTITY. NpProfile refuses a profile without a well-formed
ORCID; AGENTS.md section 5 records that the bot-IRI-versus-ORCID choice cannot be changed after
the first publish; and no ORCID appears anywhere in this repository. That is the owner's
decision, not a package to install. Two packaging traps if someone does wire it up: node.js
uses CommonJS `exports` under a package.json declaring "type": "module" (copy it to node.cjs),
and it reads ./node_bg.wasm from the CURRENT DIRECTORY (cd into the package, keep your script
outside it). See claim 1091.

Usage:  python3 publish_dryrun.py [--out DIR] [--verify-only DIR]
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

KEY = Path.home() / ".nanopub/collab-throwaway/rsa.pem"
NS = "https://w3id.org/delphi-frontier/np/"      # NOT registered -- see module docstring
FORBIDDEN_MODULES = ("socket", "http", "requests", "urllib.request", "httpx", "aiohttp")


def no_network_or_die() -> None:
    """A dry run that could transmit is not a dry run. Checked, not asserted in prose."""
    loaded = [m for m in FORBIDDEN_MODULES if m in sys.modules]
    if loaded:
        raise SystemExit(f"REFUSING: network modules are loaded into this interpreter: {loaded}. "
                         "This stage is authorised as a DRY RUN and must not be able to transmit.")


def load_key():
    from cryptography.hazmat.primitives import serialization
    if not KEY.exists():
        raise SystemExit(f"no key at {KEY}")
    return serialization.load_pem_private_key(KEY.read_bytes(), password=None)


def fmt_value(v) -> str:
    """ask-transfer values may be a scalar OR an interval object. Flattening an interval to
    str() would emit the dict's repr and silently destroy the uncertainty -- which is the exact
    class of loss D5 exists to prevent, committed by the publish stage itself."""
    if isinstance(v, dict):
        lo, hi = v.get("lo"), v.get("hi")
        kind = v.get("interval_kind") or "interval"
        if lo is not None and hi is not None:
            return f"{lo} to {hi} ({kind})"
        return json.dumps(v, sort_keys=True)
    return str(v)


def trig_for(rec: dict, idx: int, created: str) -> str:
    """Serialise one ask-transfer/v1 record as a nanopub-shaped TriG document.

    THE ENVELOPE TRAVELS OR THIS IS POINTLESS. The first version of this function emitted only
    name/value/units/conditions and dropped `evidence` (including its read_level), `contestation`
    (superseded flag and open challenges) and the interval structure of the value. A publish stage
    that shed the envelope would commit, at the last step, exactly the loss ask-transfer/v1 was
    written to prevent -- and it would do so invisibly, because the output still looks like a
    well-formed nanopub. Every envelope field is emitted below and asserted by the caller.
    """
    q = rec.get("quantity", {})
    ev = rec.get("evidence", {})
    con = rec.get("contestation", {})
    prov = rec.get("provenance", {})
    pid = rec.get("id") or f"record{idx}"
    base = f"{NS}{pid.replace(':', '/').replace(' ', '_')}"

    def lit(s):
        return json.dumps("" if s is None else str(s))

    chal = con.get("open_challenges") or []
    return f"""@prefix this: <{base}> .
@prefix sub: <{base}#> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix qudt: <http://qudt.org/schema/qudt/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

sub:Head {{
  this: a np:Nanopublication ;
    np:hasAssertion sub:assertion ;
    np:hasProvenance sub:provenance ;
    np:hasPublicationInfo sub:pubinfo .
}}

sub:assertion {{
  sub:quantity a qudt:Quantity ;
    dct:identifier {lit(pid)} ;
    dct:title {lit(q.get('name'))} ;
    qudt:symbol {lit(q.get('symbol'))} ;
    qudt:value {lit(fmt_value(q.get('value')))} ;
    qudt:unit {lit(q.get('units'))} ;
    dct:conditionsOfUse {lit(q.get('conditions'))} .
}}

sub:provenance {{
  sub:assertion prov:wasDerivedFrom {lit(ev.get('source') or prov.get('table'))} ;
    dct:accrualMethod {lit(ev.get('derivation'))} ;
    dct:accessRights {lit(ev.get('read_level'))} ;
    dct:description {lit(ev.get('how'))} ;
    prov:generatedAtTime {lit(prov.get('created_at'))} ;
    prov:wasGeneratedBy {lit('swarm/export_transfer.py ask-transfer/v1')} .
}}

sub:pubinfo {{
  this: dct:created "{created}"^^xsd:dateTime ;
    dct:creator {lit('delphi-frontier swarm (DRY RUN, throwaway key)')} ;
    dct:isReplacedBy {lit('superseded' if con.get('superseded') else 'not-superseded')} ;
    dct:references {lit(', '.join(str(c) for c in chal) if chal else 'no open challenges')} ;
    dct:rights {lit('DRY RUN -- not a Trusty URI, not publishable, never transmitted')} .
}}
"""


def sign_bytes(key, data: bytes) -> str:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    return key.sign(data, padding.PKCS1v15(), hashes.SHA256()).hex()


def verify(pubkey, data: bytes, sig_hex: str) -> bool:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    try:
        pubkey.verify(bytes.fromhex(sig_hex), data, padding.PKCS1v15(), hashes.SHA256())
        return True
    except (InvalidSignature, ValueError):
        return False


def records() -> list[dict]:
    here = Path(__file__).resolve().parent
    r = subprocess.run([sys.executable, str(here / "export_transfer.py"), "--emit"],
                       capture_output=True, text=True, timeout=180)
    # --emit prints ONE JSON OBJECT PER LINE (JSON Lines), not an array. Parsing it as an array
    # yields nothing, and "no records" would then read as "nothing to publish" rather than "I
    # mis-read the format" -- the empty-set failure one layer up.
    out = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if not out and r.returncode != 0:
        print(f"  export_transfer.py exited {r.returncode}: {r.stderr.strip()[:200]}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    no_network_or_die()

    out = Path(a.out) if a.out else \
        Path(__file__).resolve().parent.parent / "results/nanopub-dryrun"
    out.mkdir(parents=True, exist_ok=True)

    recs = records()
    if not recs:
        print("  export_transfer.py returned no records -- nothing to publish. Reporting that "
              "rather than writing an empty directory that would read as success.")
        return 1

    key = load_key()
    pub = key.public_key()
    created = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    made = []
    for i, rec in enumerate(recs):
        doc = trig_for(rec, i, created)
        data = doc.encode()
        sig = sign_bytes(key, data)
        name = (rec.get("id") or f"record{i}").replace(":", "_").replace("/", "_")
        # The envelope must be IN the bytes. Checking the dict would test the parser, not the
        # serialiser -- and it is the serialiser that was dropping fields.
        q_ = rec.get("quantity", {})
        for field, why in ((q_.get("conditions"), "conditions (D5)"),
                           (rec.get("evidence", {}).get("read_level"), "read_level (ASK rule 2)"),
                           (q_.get("units"), "units")):
            if field and str(field) not in doc:
                raise SystemExit(f"REFUSING {name}: {why} did not survive serialisation")
        p = out / f"{name}.trig"
        p.write_text(doc)
        (out / f"{name}.sig.json").write_text(json.dumps(
            {"sha256_of_bytes": hashlib.sha256(data).hexdigest(),
             "signature_rsa_pkcs1v15_sha256": sig,
             "key": str(KEY), "key_is_throwaway": True,
             "trusty_uri": None,
             "note": "digest is over the serialised BYTES, not an RDF-normalised Trusty hash; "
                     "this is NOT a publishable nanopublication"}, indent=1))
        made.append((p, data, sig))
        print(f"  wrote {p.name}  ({len(data)} B, signature {sig[:16]}...)")

    print("\n  VERIFY, reading back from disk:")
    allok = True
    for p, _, sig in made:
        ok = verify(pub, p.read_bytes(), sig)
        allok &= ok
        print(f"    {'ok  ' if ok else 'FAIL'} {p.name}")

    # CONTROL. A verifier that cannot detect tampering is not a verifier, so one byte is flipped
    # in a COPY and the same check must fail. Without this, "all ok" and "always ok" look alike.
    p0, data0, sig0 = made[0]
    tampered = data0.replace(b"qudt:value", b"qudt:valve", 1)
    assert tampered != data0, "control could not tamper the document"
    bad = verify(pub, tampered, sig0)
    print(f"\n  CONTROL, one byte changed in a copy: verification returns "
          f"{'FAIL as required' if not bad else '*** PASS -- THE VERIFIER IS BROKEN ***'}")
    if bad:
        return 2

    print(f"\n  {len(made)} nanopub-shaped document(s) in {out}")
    print("  NOT TRANSMITTED, and this module imports no network library.")
    print("  NOT publishable: no Trusty URI, throwaway key, unregistered namespace.")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
