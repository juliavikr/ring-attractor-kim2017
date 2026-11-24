"""
Reproduce paper Fig. 4A, 4B (example flow / jump) and Fig. 4D (phase diagrams).

    python scripts/fig4_jump_vs_flow.py            # full version (~2-4 min)
    python scripts/fig4_jump_vs_flow.py --quick    # coarse grid (~20 s)

Outputs (in figures/):
    fig4AB_flow_and_jump_examples.png
    fig4D_phase_diagrams.png
    results/fig4D_phase_diagrams.npz   (raw numbers, so you can re-plot)

What to look for (compare with the paper):
  * Local model (top row): the red dashed line = smallest input strength that
    makes a NARROW input cause a jump. It is (almost) flat across shift
    distances 60 -> 150 deg.
  * Global model (bottom row): the same threshold climbs a lot with distance,
    and you need much stronger inputs overall (y axis goes much higher).
"""
import argparse
import os
import sys
import warnings

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import ring_model as rm  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
FIG_DIR = os.path.join(ROOT, "figures")
RES_DIR = os.path.join(ROOT, "results")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

# Colours roughly like the paper: grey = no effect, red = flow, green = jump
warnings.filterwarnings("ignore", message=".*not monotonically.*")
CMAP = ListedColormap(["#d9d9d9", "#f4a6a6", "#b9e3b0"])
SHIFTS_DEG = [60, 90, 120, 150]
Y_MAX = {"local": 1.8, "global": 13.0}          # y-axis limits of the paper


def example_traces(model, N=64, dt=0.005):
    """Fig. 4A/B: one flow example and one jump example (local model)."""
    W = rm.make_connectivity(model, N=N)
    u_bump = rm.settle_bump(W, dt=dt)
    th = rm.ring_angles(N)
    shift = np.radians(90)

    examples = {
        "flow (weak, broad input)": 1.0 * u_bump.max() * rm.von_mises(th, shift, 1 / 1.0**2),
        "jump (strong, narrow input)": 4.0 * u_bump.max() * rm.von_mises(th, shift, 1 / 0.2**2),
    }
    fig, axes = plt.subplots(2, 2, figsize=(10, 5), sharex=True,
                             gridspec_kw={"height_ratios": [2, 1]})
    for col, (name, I) in enumerate(examples.items()):
        # 3 tau of baseline, then the input is switched on (like the visual
        # bar shifting abruptly at t = 0 in the experiment)
        inputs = lambda t, I=I: I if t >= 3 else 0 * I
        t, u = rm.simulate(W, u_bump, inputs, T=15, dt=dt, record_every=4)
        t = t - 3
        ax = axes[0, col]
        # neurons go 0..2pi; roll by N/2 so the image runs from -pi to pi
        ax.imshow(np.roll(u, N // 2, axis=1).T, aspect="auto", origin="lower",
                  cmap="Blues", extent=[t[0], t[-1], -np.pi, np.pi])
        pva, _ = rm.population_vector(u)
        ax.plot(t, pva, "r", lw=1.5, label="PVA estimate")
        ax.axhline(rm.wrap_angle(shift), color="tab:blue", ls="--", lw=1,
                   label="input position")
        ax.set_title(f"{model} model: {name}")
        ax.set_ylabel("neuron (preferred angle, rad)")
        ax.legend(loc="lower right", fontsize=8)
        axes[1, col].plot(t, u.max(axis=1), "k")
        axes[1, col].set_ylabel("bump peak")
        axes[1, col].set_xlabel(r"time ($\tau$), input on at 0")
    fig.tight_layout()
    path = os.path.join(FIG_DIR, "fig4AB_flow_and_jump_examples.png")
    fig.savefig(path, dpi=150)
    print("saved", path)


def phase_diagrams(N=64, n_width=24, n_amp=28, dt=0.005):
    """Fig. 4D: outcome (no effect / flow / jump) vs input width and strength."""
    widths = np.linspace(0.12, 2.4, n_width)        # von Mises width parameter
    results = {}
    for model in ["local", "global"]:
        W = rm.make_connectivity(model, N=N)
        u_bump = rm.settle_bump(W, dt=dt)
        # amplitudes in units of the bump's own peak; log-spaced
        top = 12 if model == "local" else 150
        amps = u_bump.max() * np.logspace(np.log10(0.05), np.log10(top), n_amp)
        for s in SHIFTS_DEG:
            print(f"  {model:6s} shift {s:3d} deg ...", flush=True)
            results[(model, s)] = rm.jump_flow_phase_diagram(
                W, u_bump, np.radians(s), amps, widths, dt=dt)

    np.savez(os.path.join(RES_DIR, "fig4D_phase_diagrams.npz"),
             **{f"{m}_{s}_{k}": v for (m, s), d in results.items()
                for k, v in d.items()})

    fig, axes = plt.subplots(2, 4, figsize=(13, 6), sharex=True)
    for r, model in enumerate(["local", "global"]):
        for c, s in enumerate(SHIFTS_DEG):
            d = results[(model, s)]
            ax = axes[r, c]
            ax.pcolormesh(d["x_width"], d["strength"], d["outcome"],
                          cmap=CMAP, vmin=-0.5, vmax=2.5, shading="nearest")
            # jump threshold for the narrowest input (first row of the grid)
            jumps = np.where(d["outcome"][0] == rm.JUMP)[0]
            if len(jumps):
                y = d["strength"][0, jumps[0]]
                ax.plot(d["x_width"][0, 0], y, "o", color="#d62728", ms=7,
                        clip_on=False, zorder=5)
                results[(model, s)]["threshold_narrow"] = y
            ax.set_ylim(1, Y_MAX[model])
            ax.set_xlim(0, 3 * np.pi / 4 + 0.3)
            ax.set_xticks([np.pi / 4, np.pi / 2, 3 * np.pi / 4])
            ax.set_xticklabels([r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$"])
            if r == 0:
                ax.set_title(f"{s}$^\\circ$ shift")
            if c == 0:
                ax.set_ylabel(f"{model} model\ninput strength\n(normalized bump amp.)")
            if r == 1:
                ax.set_xlabel("input width (inflection points, rad)")
    # red dashed line connecting the narrow-input thresholds (paper style)
    for r, model in enumerate(["local", "global"]):
        ys = [results[(model, s)].get("threshold_narrow", np.nan) for s in SHIFTS_DEG]
        print(f"{model}: jump threshold for narrow input at 60/90/120/150 deg =",
              np.round(ys, 2))
        for c in range(4):
            axes[r, c].axhline(ys[c], color="#d62728", ls="--", lw=1)
    handles = [plt.Rectangle((0, 0), 1, 1, color=CMAP(i)) for i in range(3)]
    fig.legend(handles, ["no effect", "flow", "jump"], loc="upper right", ncol=3)
    fig.suptitle("Jump vs flow phase diagrams (cf. Kim et al. 2017, Fig. 4D)")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    path = os.path.join(FIG_DIR, "fig4D_phase_diagrams.png")
    fig.savefig(path, dpi=150)
    print("saved", path)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--quick", action="store_true", help="coarse grid, fast")
    args = p.parse_args()
    example_traces("local")
    if args.quick:
        phase_diagrams(n_width=10, n_amp=12)
    else:
        phase_diagrams()
