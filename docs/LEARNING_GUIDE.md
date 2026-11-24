# 🧠 Learning guide (for complete beginners)

Do **Part A** in week 1 (≈ 4–6 h each). Part B is for when you want to go deeper.
Don't read everything. Each item says *why* it's here.

## Part A: the minimum you need

### A1. Firing-rate models (≈ 1 h)
The whole project uses one kind of model: each neuron (or group of neurons) is described by a single number, its **firing rate**, that changes in time according to its inputs.
- 📖 Gerstner et al., *Neuronal Dynamics* (free online book, neuronaldynamics.epfl.ch). Read **Ch. 15.3** (rate models) and **Ch. 18.1–18.3** (continuum/"field" models: this is our ring!).
- 🎓 Neuromatch Academy, *Computational Neuroscience* course (free, compneuro.neuromatch.io): **W2D4 "Dynamic Networks"**, tutorial 1 (Wilson–Cowan / rate models). Do the interactive parts.
- ✅ You're done when you can say what `τ du/dt = −u + f(input)` does when the input is constant.

### A2. Attractors (≈ 1 h)
An **attractor** is a state the network settles into and stays in. A **ring attractor** (or continuous attractor) has a whole *circle* of such states: the bump can rest anywhere on the ring. That's why it can store a continuous variable like heading.
- 📖 Khona & Fiete (2022), *Attractor and integrator networks in the brain*, Nat. Rev. Neurosci. 23:744. Read the intro and the box on ring attractors.
- 📖 Zhang (1996), *Representation of spatial orientation by the intrinsic dynamics of the head-direction cell ensemble*, J. Neurosci. 16:2112 (ref. 13 in our paper). The classic theory paper: skim the figures.
- ✅ You're done when you can explain why a ring attractor needs both excitation (to keep the bump alive) and inhibition (to keep it to one bump).

### A3. The fly heading system (≈ 1 h)
- 📖 Seelig & Jayaraman (2015), *Neural dynamics for landmark orientation and angular path integration*, Nature 521:186 (ref. 16). The discovery of the bump that our paper builds on. Look at Fig. 1–2.
- 🔤 Vocabulary to learn (put it in the cheat sheet in `PAPER_NOTES.md`):
  - **central complex**: brain region for navigation; contains the **EB** (ellipsoid body, a ring) and **PB** (protocerebral bridge)
  - **E-PG neurons**: dendrites in one EB wedge, axons to the PB; *our ring neurons*
  - **GCaMP6f**: calcium indicator; fluorescence ≈ neural activity (ΔF/F₀)
  - **CsChrimson**: light-activated channel; red/2-photon light → neuron fires (optogenetics)
  - **tethered flight / closed loop / VR arena**: fly glued in place, its wing beats rotate the LED scene
  - **PVA (population vector average)**: how they read bump position (Fig. 1F)

### A4. Our code (≈ 1–2 h)
- Do `notebooks/01_tutorial_first_bump.ipynb`.
- Read `src/ring_model.py` top to bottom. It's written to be read.
- Read `docs/MODEL.md`.

## Part B: go deeper (optional)
- Ben-Yishai, Bar-Or & Sompolinsky (1995), PNAS 92:3844 (ref. 11): the "global" cosine model, analytically.
- Skaggs et al. (1995), NIPS 7 (ref. 12): ring attractor + path integration idea.
- Turner-Evans et al. (2017), eLife 6:e23496, and Green et al. (2017), Nature 546:101: how the bump is *moved* when the fly turns (P-EN neurons). Useful for "what's next" slide.
- Hulse et al. (2021), eLife 10:e66039: the full connectome of the central complex. It shows the real wiring we can only infer here.
- Dayan & Abbott, *Theoretical Neuroscience*, Ch. 7.4 (recurrent networks, "network stability", continuous attractors).

## Python skills you'll use
`numpy` arrays and broadcasting, `matplotlib` (`plt.plot`, `plt.imshow`), writing a function, a `for` loop over time steps. If any is new: Neuromatch **W0D1 Python workshop** is a good 2-hour refresher.
