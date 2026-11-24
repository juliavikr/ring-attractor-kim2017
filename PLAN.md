# 📋 Project plan & checklist

**Paper:** Kim, Rouault, Druckmann & Jayaraman (2017). *Ring attractor dynamics in the Drosophila central brain.* Science 356:849–853.
**Team:** Julia · Luiz · Elizabeth
**Deadline:** 🎤 **Tuesday 15 December 2026**, 20-minute presentation

> **How to use this file**
> - This is the single source of truth. If it's not in here, it isn't planned.
> - Tick a box by changing `[ ]` to `[x]` and commit (`git commit -m "plan: tick Fig 2 step 1"`).
> - Every task has **one owner** (responsible) and **one reviewer** (checks it and must understand it).
>   The reviewer is how all three of us keep control of the whole project.
> - Running late? Write it under **⚠️ Blockers** at the bottom *the same day*. Don't wait for the meeting.

---

## 👥 Roles

Each person **leads** one area but **reviews** another, so everyone touches everything.

| | Leads | Reviews | Presents (≈ 6 min) |
|---|---|---|---|
| **Julia** | 🧠 Biology & background · Fig. 1 (tracking + darkness) · slide deck assembly | Luiz's Fig. 4 work | Intro: heading, central complex, imaging + optogenetics, ring attractors, Fig. 1 |
| **Luiz** | ⚙️ Model & code · Fig. 4 (jump vs flow, phase diagrams, thresholds) · tests | Elizabeth's Fig. 2/3 work | The model + Fig. 4 (jump vs flow, the key result) |
| **Elizabeth** | ⚡ Perturbation experiments · Fig. 2 (competition) · Fig. 3 (drift, WTA) | Julia's Fig. 1 work | Fig. 2, Fig. 3, limitations + conclusions |

Swap roles freely if you prefer, but change this table when you do.

**Shared by everyone:** read the paper, do Tutorial 01, come to meetings, review PRs, rehearse.

---

## 🗓️ Timeline at a glance

| Week | Dates | Phase | Milestone (end of week) |
|---|---|---|---|
| 1 | Tue 24 Nov → Sun 29 Nov | 🔎 **Understand**: setup, background, read paper, tutorial | **M1**: everyone can explain the model and Figs 1–4 |
| 2 | Mon 30 Nov → Sun 6 Dec | 🧪 **Simulate**: each owner reproduces their figure | **M2**: all model figures exist (draft quality) |
| 3 | Mon 7 Dec → Mon 14 Dec | 🎤 **Present**: polish figures, slides, 2 rehearsals | **M3**: final slides, rehearsed at ≤ 20 min |
| — | **Tue 15 Dec** | 🎉 Presentation | |

**Fixed meetings** (30–45 min, notes in `docs/meetings/`):
- 🟢 **Fri 27 Nov**: Kick-off follow-up: everyone explains one figure of the paper
- 🟢 **Wed 2 Dec**: Mid-simulation check: show first plots, unblock
- 🟢 **Sun 6 Dec**: M2 review: all figures on the table, decide the story of the talk
- 🟢 **Thu 10 Dec**: Slides review + Rehearsal 1 (timed)
- 🟢 **Mon 14 Dec**: Rehearsal 2 (final, timed, with questions)

---

## 🔎 Phase 0: Setup (Tue 24 – Wed 25 Nov)

| ✓ | Task | Owner | Reviewer |
|---|---|---|---|
| [ ] | Create the GitHub repo, push this folder, invite the other two (see README §"Put it on GitHub") | Julia | — |
| [ ] | Run `tools/setup_github.sh` once to create the issues + milestones board | Julia | Luiz |
| [ ] | Clone, install (`pip install -r requirements.txt`), run `pytest -q` → all green | **Julia** | — |
| [ ] | (same) | **Luiz** | — |
| [ ] | (same) | **Elizabeth** | — |
| [ ] | Everyone reads `docs/GIT_WORKFLOW.md` and makes one test commit (add your name to `docs/meetings/2026-11-24_kickoff.md`) | all | — |
| [ ] | Put the paper PDF in `papers/` locally (it's git-ignored; **do not** push it, it's copyrighted) | all | — |
| [ ] | Download the supplementary materials (has the model equations: fig. S3, S4 + Supplementary Text) | Luiz | — |

## 🔎 Phase 1: Understand (Tue 24 – Sun 29 Nov) → **M1**

| ✓ | Task | Owner | Reviewer |
|---|---|---|---|
| [ ] | Work through `docs/LEARNING_GUIDE.md` part A (background) | all | — |
| [ ] | Read the paper with the reading guide in `docs/PAPER_NOTES.md` | all | — |
| [ ] | Tutorial 01 done (`notebooks/01_tutorial_first_bump.ipynb`): **Julia** | Julia | Elizabeth |
| [ ] | Tutorial 01 done: **Luiz** | Luiz | Julia |
| [ ] | Tutorial 01 done: **Elizabeth** | Elizabeth | Luiz |
| [ ] | Write 5–8 bullet "biology cheat sheet" (fly, central complex, E-PG, EB, PB, GCaMP, CsChrimson) in `docs/PAPER_NOTES.md` | Julia | Elizabeth |
| [ ] | Write "model in plain words" (equation, 3 connectivities, what jump/flow means) in `docs/PAPER_NOTES.md` | Luiz | Julia |
| [ ] | Write "the experiments in plain words" (Fig. 2, 3, 4E–G protocols) in `docs/PAPER_NOTES.md` | Elizabeth | Luiz |
| [ ] | 🟢 **Fri 27 Nov meeting**: each person explains one figure (Julia: Fig 1 · Elizabeth: Fig 2+3 · Luiz: Fig 4) | all | — |
| [ ] | Make a list of questions for the professor (anything unclear in the paper) | all | — |
| [ ] | **M1 ✅**: each of us can answer the 4 questions at the end of Tutorial 01 *without notes* | all | — |

## 🧪 Phase 2: Simulate (Mon 30 Nov – Sun 6 Dec) → **M2**

Each figure task has a starter script with step-by-step TODOs and *checked* hint values.
Work on a branch, open a Pull Request, reviewer approves → merge. (See `docs/GIT_WORKFLOW.md`.)

### Fig. 1: tracking & persistence in darkness · Owner **Julia** · Reviewer **Elizabeth**
`scripts/fig1_tracking_and_darkness.py`
- [ ] 1. Core simulation (from Tutorial 01 §4)
- [ ] 2. Random-walk heading for the visual cue
- [ ] 3. 3-row figure like Fig. 1G (heatmap / PVA vs cue / unwrapped)
- [ ] 4. Summary stats: number of bumps, width, PVA–cue correlation (Fig. 1I–K)
- [ ] 5. Noise in darkness: slow drift, no disappearance
- [ ] 6. Bonus slide: same simulation with `W = 0` (no ring attractor)
- [ ] ⭐ Stretch: real data PVA from the Janelia "visual environments" dataset (`data/README.md`)

### Fig. 2: competition between bumps (optogenetics) · Owner **Elizabeth** · Reviewer **Luiz**
`scripts/fig2_competition.py`
- [ ] 1. Stimulation trial: new bump replaces old bump
- [ ] 2. Heatmap + PVA (Fig. 2C) and stimulated vs old-bump activity (Fig. 2D)
- [ ] 3. Suppression vs distance (Fig. 2F)
- [ ] 4. Same with the global model: compare
- [ ] 5. Final figure saved

### Fig. 3: drift after stimulation, local vs WTA · Owner **Elizabeth** · Reviewer **Luiz**
`scripts/fig3_drift.py`
- [ ] 1. 30 noisy trials, local model: bump survives and drifts
- [ ] 2. Position-vs-time plot (Fig. 3B)
- [ ] 3. Drift-distance histogram (Fig. 3D)
- [ ] 4. WTA comparison (fig. S3E idea)
- [ ] 5. Final figure saved

### Fig. 4: jump vs flow · Owner **Luiz** · Reviewer **Julia**
`scripts/fig4_jump_vs_flow.py` (✅ runs already) + `scripts/fig4G_jump_threshold.py` (TODO)
- [ ] 1. Run `fig4_jump_vs_flow.py`, explain every function to Julia (she must be able to re-explain it)
- [ ] 2. Jump threshold at 90° vs 180°, narrow input, both models
- [ ] 3. Fig. 4G-style plot
- [ ] 4. Parameter study: beta and D in the local model
- [ ] 5. Side-by-side "paper vs ours" image for Fig. 4D
- [ ] 6. Keep `pytest -q` green after any change to `src/ring_model.py`

### Phase 2 checkpoints
- [ ] 🟢 **Wed 2 Dec**: everyone shows at least step 1–2 of their figure
- [ ] Every figure PR reviewed + merged by **Sat 5 Dec**
- [ ] `results/RESULTS_LOG.md`: one paragraph per figure: what we did, what matched the paper, what didn't, and why
- [ ] 🟢 **Sun 6 Dec / M2 ✅**: all figures exist; we agree on the **story** of the talk (`docs/PRESENTATION_OUTLINE.md`)

## 🎤 Phase 3: Presentation (Mon 7 – Mon 14 Dec) → **M3**

| ✓ | Task | Owner | Reviewer | Due |
|---|---|---|---|---|
| [ ] | Create the shared slide deck and the template (one style for all) | Julia | — | Mon 7 Dec |
| [ ] | Slides: intro + background + Fig. 1 (≈ 6 min) | Julia | Elizabeth | Wed 9 Dec |
| [ ] | Slides: the model + Fig. 4 + our phase diagrams (≈ 6 min) | Luiz | Julia | Wed 9 Dec |
| [ ] | Slides: Fig. 2 + Fig. 3 + conclusions (≈ 6 min) | Elizabeth | Luiz | Wed 9 Dec |
| [ ] | Final figure polish: same font sizes, colours, labels in all our plots | Luiz | Elizabeth | Wed 9 Dec |
| [ ] | 🟢 **Thu 10 Dec**: slides review + Rehearsal 1 (timed, note what's too long) | all | — | Thu 10 Dec |
| [ ] | Fix slides after rehearsal 1 | all | — | Sat 12 Dec |
| [ ] | Prepare 5 likely questions + answers (`docs/PRESENTATION_OUTLINE.md`) | Elizabeth | all | Sat 12 Dec |
| [ ] | 🟢 **Mon 14 Dec**: Rehearsal 2 (final, ≤ 20 min, with Q&A) | all | — | Mon 14 Dec |
| [ ] | Export slides to PDF + push to `presentation/`; tag the repo `v1.0` | Julia | — | Mon 14 Dec |
| [ ] | 🎉 **Tue 15 Dec: present!** | all | — | Tue 15 Dec |

---

## ✅ Definition of done (for any figure)
1. Script runs from a fresh clone with one command and saves the PNG in `figures/`.
2. Axes labelled with units, a title, and the paper figure it corresponds to.
3. A paragraph in `results/RESULTS_LOG.md`: matches the paper? differences? why?
4. The reviewer has run it and can explain it in 1 minute.

## ⚠️ Blockers / risks (write here as soon as something goes wrong)
| Date | Who | Problem | Help needed from |
|---|---|---|---|
| | | | |

**Known risks & fallbacks**
- *A figure doesn't work by Wed 2 Dec* → ask in the group the same day; reduce scope (e.g., skip Fig. 3 WTA part). Fig. 4 already works, so we always have a core result.
- *Someone is sick in week 3* → every part has a reviewer who understands it and can present it.
- *Real data too big / unclear format* → it's a stretch goal; skip it without guilt.
