"""
TASK (owner: Luiz) - model version of Fig. 4E-G, plus a parameter study

    python scripts/fig4G_jump_threshold.py

The experiment (Fig. 4E-G): the authors stimulated two small spots
(22.5 deg wide) one after the other, separated by 90 deg or 180 deg, and
measured how much laser power was needed to make the bump JUMP.
Result: the same power for 90 and 180 deg -> matches the LOCAL model,
where the jump threshold doesn't depend on distance (red dashed line in
Fig. 4D is flat), and not the GLOBAL model (threshold increases).

Our full Fig. 4D script already exists (scripts/fig4_jump_vs_flow.py).
Your job is to UNDERSTAND it and build the simpler, sharper Fig. 4G version.

Steps:
  [ ] 1. Read rm.jump_or_flow and rm.normalized_input_strength line by line.
         Explain them to the team (Week 2 meeting). Why does the code call
         it a jump when the peak first appears beyond 45 deg?
  [ ] 2. For each model ('local', 'global') and distance in [90, 180] deg,
         find the smallest input amplitude that causes a JUMP, for a narrow
         input (inflection width ~22.5 deg -> width parameter ~0.2, check
         with rm.inflection_width). Use a fine amplitude grid (batched!) or
         bisection.
  [ ] 3. Convert the threshold amplitude to normalized strength
         (rm.normalized_input_strength) and plot it like Fig. 4G: x = distance,
         one line per model. Expected: local flat, global increasing.
  [ ] 4. Parameter study: how does the local-model threshold change with
         beta (global inhibition) and D (local coupling)? Vary each by
         x0.5 and x2 (check the bump still exists and has 1 peak!).
  [ ] 5. Run the full Fig. 4D (python scripts/fig4_jump_vs_flow.py) and put
         it side by side with the paper's Fig. 4D for the presentation.
  [ ] 6. Save figures/fig4G_jump_threshold.png

Expected numbers from the full Fig. 4D run (N=64), as a check:
  local : threshold ~1.37 at 60/90/120/150 deg
  global: ~2.5, 4.5, 6.9, 8.8
"""
import os
import sys

import matplotlib.pyplot as plt  # noqa: F401
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import ring_model as rm  # noqa: E402

N = 64


def jump_threshold(model, distance_deg, width=0.2, n_amp=60):
    """TODO: return the smallest amplitude (absolute) that gives a JUMP."""
    W = rm.make_connectivity(model, N=N)
    u_bump = rm.settle_bump(W)
    top = 12 if model == "local" else 150
    amps = u_bump.max() * np.logspace(np.log10(0.5), np.log10(top), n_amp)
    out = rm.jump_or_flow(W, u_bump, np.radians(distance_deg), amps, width)
    # TODO: find the first index where out == rm.JUMP, return that amplitude
    raise NotImplementedError


if __name__ == "__main__":
    raise NotImplementedError("Steps 2-6")
