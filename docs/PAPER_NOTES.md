# 📄 Paper notes: Kim, Rouault, Druckmann & Jayaraman (2017)

*Science* 356:849–853 · doi:10.1126/science.aal4835
Also get the **Supplementary Materials** (Science website): Materials & Methods, Supplementary Text, figs. S1–S4. The model details (fig. S3, S4) are only there.

---

## 1. How to read it (reading guide)

**Pass 1 (30 min, alone):** abstract → last paragraph → look at every figure and read only the captions. Write down: *what is the question? what is the answer?*

**Pass 2 (1–2 h, alone):** read the whole text. Use the vocabulary in `LEARNING_GUIDE.md` A3. For each figure, answer the guiding question below.

**Pass 3 (together, Fri 27 Nov):** each person presents their figure(s) in 5 min.

### Guiding questions per figure
| Figure | Question to answer in your own words |
|---|---|
| **Fig. 1** | How do they measure the bump and its position? What changes between "visual scene" and "darkness"? |
| **Fig. 2** | What exactly does the laser do? What happens to the *old* bump, and what does that tell us about connectivity? |
| **Fig. 3** | After the laser is off, where does the bump go? Why does *gradual* drift argue against winner-take-all? |
| **Fig. 4** | What's the difference between "jump" and "flow"? Why does the *threshold for jumping* distinguish local vs global models? |

## 2. The story in 6 steps (our summary, to check against your own)

1. **Question.** Theory predicted ring attractors for heading, but nobody had shown one *in a brain* with its key properties.
2. **Fig. 1:** E-PG neurons have a **single bump** (~90° wide) that tracks the visual scene in closed-loop flight and **persists in darkness** (but in darkness it doesn't follow the fly's turns well during flight).
3. **Fig. 2:** Optogenetically creating a bump elsewhere **suppresses the existing bump**, and the new one stays after the laser stops → the population is not just a mirror of its input; it *is* part of the attractor. Suppression through recurrent connections (mutual inhibition).
4. **Fig. 3:** The artificial bump later **drifts gradually** to nearby positions. A winner-take-all network would make it vanish/jump randomly → neighbours must excite each other → **ring** attractor.
5. **Fig. 4:** Abrupt visual shifts make the bump **flow** (short shifts) or **jump** (long shifts). Two models, **local** (local excitation + flat inhibition) and **global** (cosine), both produce jumps and flows, but:
   - the global model needs a much wider range of input strengths, and its jump threshold **grows with distance**;
   - with optogenetics (narrow 22.5° spots, 90° vs 180° apart), the threshold to jump is the **same** for both distances → **local model**.
6. **Conclusion:** the effective connectivity is **narrow local excitation + flat long-range inhibition**, a motif seen in many species.

## 3. Biology cheat sheet *(Julia, fill in, 5–8 bullets)*
- 
- 

## 4. The model in plain words *(Luiz, fill in)*
- 
- 

## 5. The experiments in plain words *(Elizabeth, fill in)*
- 
- 

## 6. Questions for the professor
- 
