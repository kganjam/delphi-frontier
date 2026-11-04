"""Independent re-implementation of FoldIndex (Prilusky et al. 2005, Bioinformatics 21:3435).

FoldIndex = 2.785 * <H> - |<R>| - 1.151
  <H> = mean Kyte-Doolittle hydropathy scaled to [0,1] via (KD + 4.5) / 9
  <R> = mean net charge per residue = (K + R - D - E) / N

Positive -> predicted folded; negative -> predicted intrinsically unfolded.
Written from the published formula; no code or intermediate value copied from the
claim under review.
"""
import sys

KD = {  # Kyte & Doolittle 1982 hydropathy
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2,
}
POS = set('KR')
NEG = set('DE')


def read_fasta(path):
    name, seq = None, []
    for line in open(path):
        line = line.strip()
        if line.startswith('>'):
            name = line[1:]
        elif line:
            seq.append(line)
    return name, ''.join(seq).upper()


def h_scaled(aa):
    return (KD[aa] + 4.5) / 9.0


def foldindex(seq):
    n = len(seq)
    H = sum(h_scaled(a) for a in seq) / n
    R = (sum(1 for a in seq if a in POS) - sum(1 for a in seq if a in NEG)) / n
    return 2.785 * H - abs(R) - 1.151, H, R


def window_fraction(seq, w=51):
    """Fraction of residues covered by at least one window with FoldIndex < 0,
    and fraction of window CENTRES that are negative. Both reported because the
    original FoldIndex server colours residues, while a naive script often
    counts centres."""
    n = len(seq)
    if n < w:
        return None
    neg_centre = 0
    covered = set()
    nwin = n - w + 1
    for i in range(nwin):
        fi, _, _ = foldindex(seq[i:i + w])
        if fi < 0:
            neg_centre += 1
            covered.update(range(i, i + w))
    return neg_centre / nwin, len(covered) / n, nwin


if __name__ == '__main__':
    for path in sys.argv[1:]:
        name, seq = read_fasta(path)
        acc = name.split('|')[1] if '|' in name else name
        fi, H, R = foldindex(seq)
        print(f'{acc}  len={len(seq)}')
        print(f'  <H>={H:.5f}  <R>={R:+.5f}  FoldIndex={fi:+.4f}')
        for w in (21, 31, 41, 51, 75, 101):
            res = window_fraction(seq, w)
            if res:
                c, cov, nwin = res
                print(f'  w={w:3d}  neg-centre={c*100:5.1f}%  neg-covered={cov*100:5.1f}%  (n={nwin})')
        comp = {a: seq.count(a) / len(seq) * 100 for a in set(seq)}
        top = sorted(comp.items(), key=lambda kv: -kv[1])[:6]
        print('  top residues: ' + ', '.join(f'{a} {v:.1f}%' for a, v in top))
        print(f'  G+P = {comp.get("G",0)+comp.get("P",0):.1f}%   '
              f'charged(KRDE) = {sum(comp.get(a,0) for a in "KRDE"):.1f}%')
        print()
