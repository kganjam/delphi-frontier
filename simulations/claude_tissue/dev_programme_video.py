"""Short video for the developmental-programme card: body (SL) and pectoral fin (L = a + c*SL, fitted per group)
drawn to scale as SL grows from 2 to 25 cm, for flying fish, flying halfbeak, halfbeak and needlefish, with the
observed specimens appearing as SL passes them.  Fitted model curves are computed; dots are observed specimens.
Schematic bars, not fish anatomy.  Single-thread render (ffmpeg -threads 1)."""
import json, sys, time, csv, pathlib, subprocess, tempfile, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from claude_tissue.common import ROOT, write_receipt
from claude_tissue.dev_programme import load, GROUPS

OUT = ROOT/"artifacts/simulations/claude-tissue-dev-programme"
COLS = {"flying fish": "tab:blue", "flying halfbeak": "tab:purple", "halfbeak": "tab:orange", "needlefish": "tab:gray"}

if __name__ == "__main__":
    t0 = time.time(); prog = json.loads((OUT/"programme.json").read_text()); D = load()
    sls = np.geomspace(2.0, 25.0, 96); tmp = tempfile.mkdtemp(prefix="devvid-")
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.8), gridspec_kw=dict(width_ratios=[1.3, 1]))
    for f, SL in enumerate(sls):
        for a in ax: a.clear()
        for j, g in enumerate(GROUPS):
            p = prog["groups"][g]["programme_fit"]; L = max(p["a_cm"] + p["c"]*SL, 0.0); y = 3 - j
            ax[0].plot([0, 1], [y, y], color="0.75", lw=7, solid_capstyle="round")
            lo, hi = D[g][:, 0].min(), D[g][:, 0].max(); inr = lo <= SL <= hi
            ax[0].plot([0.25, 0.25 + L/SL], [y + 0.22, y + 0.22], color=COLS[g], lw=4, solid_capstyle="round", alpha=1.0 if inr else 0.3)
            if not inr: ax[0].text(0.25, y + 0.42, "extrapolated (outside observed SL range)", fontsize=6, color=COLS[g])
            ax[0].text(-0.05, y, g, ha="right", va="center", fontsize=8)
            ax[0].text(1.32, y + 0.1, f"fin/SL {L/SL:.2f}", va="center", fontsize=8, color=COLS[g])
            x = D[g][:, 0]; m = x <= SL; sg = np.linspace(lo, min(SL, hi), 50)
            ax[1].scatter(x[m], D[g][m, 1]/x[m], s=10, color=COLS[g])
            if SL >= lo: ax[1].plot(sg, p["c"] + p["a_cm"]/sg, color=COLS[g], lw=1.2)
        ax[0].set_xlim(-0.75, 1.6); ax[0].set_ylim(-0.6, 3.7); ax[0].axis("off")
        ax[0].set_title(f"body length normalised to 1 (grey); fin (colour) from fitted programme, SL = {SL:.1f} cm", fontsize=8)
        ax[1].set_xlim(1.5, 26); ax[1].set_ylim(0, 0.9); ax[1].set_xlabel("SL (cm)"); ax[1].set_ylabel("pectoral fin / SL")
        ax[1].set_title("dots: OBSERVED specimens; lines: fitted L/SL = c + a/SL (observed range only)", fontsize=8)
        fig.suptitle("Developmental programme model (computed fit, cross-sectional data; not a growth recording)", fontsize=9)
        fig.savefig(f"{tmp}/f{f:03d}.png", dpi=90)
    plt.close(fig)
    mp4 = OUT/"programme.mp4"; poster = OUT/"poster.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-threads", "1", "-framerate", "16", "-i", f"{tmp}/f%03d.png",
                    "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-pix_fmt", "yuv420p", "-c:v", "libx264", str(mp4)], check=True)
    subprocess.run(["cp", f"{tmp}/f{len(sls)-1:03d}.png", str(poster)], check=True)
    write_receipt(OUT, "claude-tissue-dev-programme-video", "python3 simulations/claude_tissue/dev_programme_video.py", "deterministic (no RNG)",
                  ["artifacts/observed-allometry/source-observations.csv", "artifacts/simulations/claude-tissue-dev-programme/programme.json"], [mp4, poster], t0)
