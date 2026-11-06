#!/usr/bin/env python3
"""One psql access layer for the swarm scripts, and one place to make a value row-safe.

WHY THIS EXISTS. `env()` and `q()` were byte-identical in `api_challenge.py` and
`design_chain.py`, and five files carried six SLIGHTLY DIFFERENT hand-written versions of the
same scrub -- the expression that stops a stored value from breaking psql's row framing. The
differences were the bug. `q()` returns `[ln.split(SEP) for ln in stdout.split("\n")]`, so a
newline inside a column ends the row early and every column after it disappears:

    api_challenge.py  replace(replace(col, SEP, ' '), chr(10), ' ')   -- SEP + LF
    design_spec.py    replace(col, chr(10), ' ')                      -- LF only
    design_chain.py   replace(left(replace(col, chr(10),' '),150), chr(13), ' ')
    api_frontier.py   replace(col, SEP, ' ')                          -- SEP only  <- CRASHED

The last one is how this module came to exist: `api_frontier.py` scrubbed the field separator
and not the newline, so `select id, question` returned a row of ONE field for each of the 4
subproblems whose question contains a newline, and indexing `r[1]` raised IndexError.

THE CRASH WAS THE LUCKY HALF. The same function's other query selected ONE column from `claim`,
where 84 of 531 statements contain a newline. A short row still has `r[0]`, so nothing raised:
the model was handed 18 "recent findings" of which several were mid-sentence fragments of a
longer statement, presented as separate settled results. A framing bug that crashes is visible;
the same bug one column narrower is a silent corruption of what the model is told. Both came
from the same missing `replace`.

So: build every text column that reaches `q()` with `flat()`, and never hand-write the scrub.
"""
from __future__ import annotations

import os
import subprocess

SEP = "\x01"
PG = ["psql", "-h", "127.0.0.1", "-p", "5436", "-U", "morphoswarm", "-d", "designswarm",
      "-tAq", "-F", SEP]
PROJECT = os.environ.get("SWARM_PROJECT", "zebrafish-flight")

#: Characters that would break q()'s framing: the field separator, LF and CR.
#: SEP is chr(1); naming it that way keeps the SQL free of a literal control byte.
FRAMING = ("chr(1)", "chr(10)", "chr(13)")


def env() -> dict:
    e = dict(os.environ)
    if "PGPASSWORD" not in e:
        for line in open("/home/ubuntu/git/morphoswarm/.env"):
            if line.startswith("MORPHOSWARM_PG_PASSWORD="):
                e["PGPASSWORD"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    return e


def q(sql: str) -> list[list[str]]:
    r = subprocess.run(PG + ["-c", sql], capture_output=True, text=True, env=env(), timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:300])
    return [ln.split(SEP) for ln in r.stdout.strip().split("\n") if ln]


def lit(s) -> str:
    return "null" if s is None else "'" + str(s).replace("'", "''") + "'"


def flat(expr: str, limit: int | None = None) -> str:
    """SQL wrapping `expr` so its value cannot break q()'s row and field framing.

    `limit` truncates AFTER scrubbing, which is the order that matters: truncating first can
    leave a trailing fragment, but scrubbing first guarantees the result is single-line
    whatever the limit does.
    """
    # CAST FIRST. `replace()` is text-only, so flat('criteria') on a jsonb column fails with
    # `function replace(jsonb, text, unknown) does not exist` -- a cryptic error for what is
    # just a column of the wrong type. q() returns psql's text serialisation of every column
    # anyway, so casting here is what the caller wanted in every case, and on a text column
    # `col::text` is a no-op.
    out = f"({expr})::text"
    for ch in FRAMING:
        out = f"replace({out}, {ch}, ' ')"
    return f"left({out}, {int(limit)})" if limit is not None else out


def write_claim(project: str, scale: str | None, statement: str, evidence: str,
                value_num: float | None, units: str | None, source: str,
                read_level: str | None = None) -> int:
    """Insert one claim and return its id.

    ADDED because there was no shared writer and every module that needed one carried its own
    INSERT. `scripts` already holds twelve copies of the read path for the same reason; this is
    the write path, consolidated before it reached two.
    """
    cols = ["project_id", "scale_id", "statement", "evidence", "value_num", "units", "source"]
    vals = [lit(project), lit(scale), lit(statement), lit(evidence),
            "null" if value_num is None else repr(float(value_num)), lit(units), lit(source)]
    if read_level is not None:
        cols.append("read_level")
        vals.append(lit(read_level))
    sql = (f"insert into claim ({', '.join(cols)}) values ({', '.join(vals)}) returning id")
    rows = q(sql)
    return int(rows[0][0])
