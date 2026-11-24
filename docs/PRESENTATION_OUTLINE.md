# 🎤 Presentation outline: 20 minutes, 15 December

Rule of thumb: **1 slide ≈ 1 minute**. Target **18 min** of talking, so we have a 2-min buffer.
Each person presents ≈ 6 min. Handovers are one sentence ("…and Luiz will now show how we model this").

| # | Slide | Content | Speaker | Time | Figure source |
|---|---|---|---|---|---|
| 1 | Title | paper, our names | Julia | 0:20 | — |
| 2 | The problem | How do you know which way you're facing in the dark? A heading signal must be **unique**, **persistent**, **updatable** | Julia | 1:00 | drawing |
| 3 | Ring attractor idea | neurons on a ring, bump = heading; theory since 1995 | Julia | 1:30 | our tutorial §3 plot |
| 4 | The fly + the tools | central complex, EB, E-PG; 2-photon imaging (GCaMP) **and** optogenetics (CsChrimson) | Julia | 1:30 | paper Fig. 1A–D, 2A (cite) |
| 5 | Fig. 1: result + ours | bump tracks the scene, persists in darkness; our simulation next to theirs | Julia | 1:30 | paper 1G/H + `fig1_tracking_and_darkness.png` |
| 6 | The model | equation term by term; local vs global vs WTA connectivity | Luiz | 1:30 | tutorial §2 plot |
| 7 | Jump vs flow | what they are; our example | Luiz | 1:15 | `fig4AB_flow_and_jump_examples.png` |
| 8 | Phase diagrams | paper Fig. 4D vs ours, side by side | Luiz | 2:00 | paper 4D + `fig4D_phase_diagrams.png` |
| 9 | The decisive test | jump threshold at 90° vs 180°: model vs experiment | Luiz | 1:30 | paper 4F/G + `fig4G_jump_threshold.png` |
| 10 | Fig. 2: competition | laser creates a bump, the old one dies | Elizabeth | 1:15 | paper 2C/D + `fig2_competition.png` |
| 11 | Fig. 3: drift | gradual drift → not winner-take-all | Elizabeth | 1:15 | paper 3B/D + `fig3_drift.png` |
| 12 | What we learned / limitations | what matched; our own choices (WTA params, noise, time in units of τ) | Elizabeth | 1:30 | `results/RESULTS_LOG.md` |
| 13 | Conclusions + outlook | local excitation + global inhibition; connectome; how the bump is rotated (P-EN) | Elizabeth | 1:00 | — |
| 14 | Thanks / questions | | all | — | — |
| | | | | **≈ 17–18 min** | |

Story: **Julia** sets up the question and the fly → **Luiz** shows the model and how jump/flow tells local from global → **Elizabeth** shows the other perturbation experiments that support the same conclusion, then wraps up. Only two handovers.

## Likely questions (prepare answers, owner Elizabeth)
1. Why is it called an *attractor*? What is attracted to what?
2. Why can't you just look at the anatomy to decide local vs global?
3. Your model has no real time units: how do you compare with experiments?
4. What would happen with two equal stimuli at the same time?
5. How does the bump *move* when the fly turns (not covered by this paper)? → P-EN neurons, Turner-Evans 2017, Green 2017.

## Rehearsal log
| Date | Total time | Too long | Unclear | Fix by |
|---|---|---|---|---|
| Thu 10 Dec | | | | |
| Mon 14 Dec | | | | |
