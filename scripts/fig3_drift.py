"""
TASK (owner: Elizabeth, with Luiz as reviewer) - model version of Fig. 3 (B-D)

    python scripts/fig3_drift.py

The experiment: after the laser creates an artificial bump and is switched
off (in darkness), the bump stays for a while and then slowly DRIFTS to
nearby positions. It never jumps to random far-away places.
Why it matters: a winner-take-all (WTA) network would make the bump
disappear / reappear at random positions. Gradual drift = neighbours excite
each other = ring attractor (paper fig. S3E vs Fig. 3B-D).

Steps:
  [ ] 1. Local model, N=64: settle a bump, then run 30 noisy trials at once
         (u0 = np.tile(u_bump, (30, 1))) with
             rm.simulate(..., T=600, dt=0.005, noise_std=0.04 * peak)
         Hint (checked): the bump survives and drifts ~5-35 deg over 600 tau,
         in small steps. Noise >= 0.1 * peak KILLS the bump. Try it, and
         explain why on a slide (the network has a second, near-silent
         stable state).
  [ ] 2. Plot the PVA position of every trial over time (like Fig. 3B top,
         one coloured line per trial).
  [ ] 3. Fig. 3D: split time into bins (e.g. every 5 tau), compute the drift
         distance |wrap_angle(pos[k+1] - pos[k])| and plot its histogram.
  [ ] 4. Same with the WTA model ('wta'; start from one active neuron:
         u0 = 2.0 at neuron 0, 0 elsewhere). For WTA use rm.bump_peak(U)
         instead of the PVA. Find a noise level where the winner switches
         now and then. Compare the two histograms: small steps vs jumps.
         WARNING: WTA is touchy. Scan noise_std from 0.005 to 0.03 (x2.0).
  [ ] 5. Save figures/fig3_drift.png

Slide questions:
  - What in the connectivity makes drift gradual?
  - The model's noise is a stand-in for what in the real fly?
"""
import os
import sys

import matplotlib.pyplot as plt  # noqa: F401
import numpy as np  # noqa: F401

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import ring_model as rm  # noqa: E402,F401

N = 64
rng = np.random.default_rng(42)   # fixed seed -> reproducible figures

if __name__ == "__main__":
    raise NotImplementedError("Start with step 1 in the docstring above")
