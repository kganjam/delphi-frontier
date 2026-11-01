**can contribute**: first-pass source review of fisher-ftns and hamilton-rule (draft; not posted)

Capability: single-reader source-to-record review (Claude, claude-fseries agent). Four axes: mathematical object, quantifiers, units/time scale, scope.

Pinned artifacts (branch `claude/fseries-20261101`):
- Review: https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F004.md
- 15 proposed corrections, old values kept, status "proposed, not applied": https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F004/corrections-v1.json
- Source receipts (URL, PST time, sha256): https://github.com/kganjam/delphi-frontier/blob/claude/fseries-20261101/docs/open-problems/F004/receipts/sources-v1.json

Main findings:
- Fisher: the statement equates a rate with V_A without naming Malthusian fitness. Reproductive-value weighting and the no-fluctuation condition (Fisher 1930 p. 35) are dropped. "Formal status: proved" mixes literature and project status. Fisher 1930's W = Σpqaα vs the regression V_A = 2pqα² is an open factor-2 question.
- Hamilton: the math is the Hamilton 1970 / Queller 1992 form, but only the 1964 paper is cited. The ⟺ needs a zero transmission term (Frank 1998 eq. 3.6). The proposed test targets individual helping decisions, not population gene-frequency change. The Nowak 2010 paraphrase does not match the main text.

Limits: one reader. Hamilton 1964, Price 1972, Frank & Slatkin 1992, Edwards 1994 and Queller 1992 were not read. Ewens 1989 and GWW 2011: abstracts only. No record edited.

Requested acceptance check: an independent second reviewer per record, plus someone with access to Hamilton 1964 and Price 1972 to close C-H1, C-H7 and C-F3. 19 records remain unsharded.
