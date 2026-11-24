# 🧪 Results log

One section per figure. Write it when the figure is done (part of "definition of done" in PLAN.md).
This file becomes the "what we learned / limitations" slide.

## Fig. 4D: jump vs flow phase diagrams (Luiz) ✅ draft
**What we did.** Python port of the authors' local and global models (N = 64, RK4, dt = 0.005 τ). For 4 shift distances, swept 24 input widths × 28 input amplitudes and classified the outcome like the authors' code.
**Matches the paper.**
- Local model: the jump threshold for a narrow input is constant across shift distances (1.37 normalized strength at 60/90/120/150°). The paper's red dashed line is flat at ≈1.35.
- Global model: the threshold increases with shift distance (2.5 → 4.5 → 6.9 → 8.8) and the y-range needed is ~10× larger, as in the paper.
- Broad inputs produce flows; narrow strong inputs produce jumps; flow region shrinks with distance.
**Differences / why.** Coarser grid → staircase edges. TODO (Luiz): compare region shapes in detail.

## Fig. 1: tracking & darkness (Julia)
**What we did.**
**Matches the paper.**
**Differences / why.**

## Fig. 2: competition (Elizabeth)
**What we did.**
**Matches the paper.**
**Differences / why.**

## Fig. 3: drift (Elizabeth)
**What we did.**
**Matches the paper.**
**Differences / why.**

## Fig. 4G: jump threshold 90° vs 180° (Luiz)
**What we did.**
**Matches the paper.**
**Differences / why.**
