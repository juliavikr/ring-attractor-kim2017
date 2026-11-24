"""
TASK (owner: Elizabeth) - model version of paper Fig. 2 (C, D, F)

    python scripts/fig2_competition.py

The experiment: the fly already has a bump. The authors shine a laser
(optogenetics, CsChrimson) on ONE spot of the ring -> a new, artificial bump
appears there and the OLD bump disappears. When the laser is switched off,
the new bump stays (it is "adopted" by the network).
Interpretation: E-PG neurons compete through recurrent inhibition.

In the model, the laser = a strong, NARROW input at a chosen location:
    I = amp * rm.von_mises(th, stim_angle, 1 / width**2)

Steps:
  [ ] 1. Settle a bump at 0 (rm.settle_bump). Switch the stimulus on at
         t = 2 for 5 tau at stim_angle = pi, then off. Simulate 30 tau.
         Hint (checked): local model, N=64, width = 0.2, amp = 3 * bump peak
         -> the old bump dies and the new one survives after the laser.
  [ ] 2. Plot the heatmap + PVA (like Fig. 2C), and the activity at the
         STIMULATED neuron vs the OLD bump neuron over time (like Fig. 2D,
         red vs blue curves).
  [ ] 3. Fig. 2F: repeat for stim_angle in [pi/8, pi/4, pi/2, 3pi/4, pi]
         and plot "activity of old bump during stim / before stim" vs
         distance. (Careful at pi/8: the bump might just FLOW instead.)
  [ ] 4. Repeat step 1 with the GLOBAL model using the same amp. What
         happens? How strong must amp be for the global model?
         (Connect this to Fig. 4: the global model needs much more input.)
  [ ] 5. Save figures/fig2_competition.png

Slide questions:
  - Why does creating a new bump destroy the old one? Which term in W?
  - Why does the new bump survive after the laser is off?
"""
import os
import sys

import matplotlib.pyplot as plt  # noqa: F401
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import ring_model as rm  # noqa: E402

N = 64
th = rm.ring_angles(N)


def stimulation_trial(model="local", stim_angle=np.pi, amp_rel=3.0,
                      width=0.2, t_on=2.0, t_off=7.0, T=30.0):
    W = rm.make_connectivity(model, N=N)
    u_bump = rm.settle_bump(W)
    I_stim = amp_rel * u_bump.max() * rm.von_mises(th, stim_angle, 1 / width**2)

    def inputs(t):
        # TODO: return I_stim during [t_on, t_off), zeros otherwise
        raise NotImplementedError

    t, U = rm.simulate(W, u_bump, inputs, T=T, record_every=20)
    return t, U


if __name__ == "__main__":
    t, U = stimulation_trial()
    # TODO steps 2-5
