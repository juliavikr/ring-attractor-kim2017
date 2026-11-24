"""
TASK (owner: Julia) - model version of paper Fig. 1G, 1H (and 1I-K stats)

    python scripts/fig1_tracking_and_darkness.py

Goal: show that the model bump (1) tracks a moving visual cue and
(2) stays put when the cue disappears ("darkness").
Start from Tutorial 01, section 4. It already does the core simulation.

Steps (tick them in PLAN.md as you go):
  [ ] 1. Copy the section-4 simulation from the tutorial into `run_trial()`.
  [ ] 2. Instead of a constant turning speed, make the cue follow a
         "random walk" heading (like a real fly turning left/right):
             heading = np.cumsum(rng.normal(0, 0.05, n_steps))  (rad)
         and interpolate it inside visual_input(t).
  [ ] 3. Make a 3-row figure like Fig. 1G: heatmap / PVA vs cue / unwrapped
         angles (np.unwrap). Put a "darkness" period at the end.
  [ ] 4. Compute the paper's summary numbers for the "visual" part and the
         "darkness" part (Fig. 1I-K): number of bumps, bump width (deg),
         correlation between PVA and cue heading (use circular difference:
         rm.wrap_angle(pva - cue)).
  [ ] 5. Add noise (noise_std = 0.04 * bump peak) in darkness and show the
         bump slowly drifts, but does NOT disappear or split.
  [ ] 6. Save to figures/fig1_tracking_and_darkness.png

Questions to answer on your slide:
  - Why does the bump lag behind the cue? What sets the lag?
  - What would a "fake" ring attractor (no recurrent connections, W = 0) do
    in darkness? Try it: W = np.zeros((N, N)). Great slide!

STRETCH (optional, only if Fig 2/3/4 are done): the real data.
  See data/README.md -> "01. visual environments" (2 GB preprocessed).
  Compute the PVA from the 16 ROI traces exactly like rm.population_vector
  and plot it against the arena position.
"""
import os
import sys

import matplotlib.pyplot as plt  # noqa: F401
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import ring_model as rm  # noqa: E402,F401

N = 64
rng = np.random.default_rng(0)


def run_trial(T_visual=60.0, T_dark=40.0, noise=0.0):
    """TODO: return t, U (rates), cue (rad, nan in darkness)."""
    raise NotImplementedError("Step 1: start from Tutorial 01, section 4")


if __name__ == "__main__":
    t, U, cue = run_trial()
    # TODO steps 3-6
