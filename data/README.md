# 📦 Data (optional, stretch goal)

**Our project does not need any data.** All required figures come from simulations.
The original data is only for the optional Fig. 1 stretch task (Julia).

Source: https://research.janelia.org/jayaraman/KimRouaultScience2017_Downloads/

| Archive | Size (preprocessed) | Relevant to |
|---|---|---|
| `01. visual environments.zip` | ~2 GB | Fig. 1 (bump in different visual scenes & darkness) |
| `04. powerbox bump shifting.zip` | ~5.6 GB | Fig. 2–3 (optogenetic stimulation) |
| `10. powerbox-flow2.zip` | ~6.4 GB | Fig. 4 (jump/flow) |
| `12. powerbox-behavior03.zip` | ~1.8 GB | behaviour controls |
| `ringattractor.zip` (code, 0.8 MB) | — | the authors' analysis code + README + data agreement |

The **raw** data is ~450 GB: don't download it.

If you try it:
1. Download `ringattractor.zip` first and read its README and **data agreement**.
2. Download only `01. visual environments.zip` and extract to `data/processed_data/` (git-ignored).
3. Expect MATLAB-style files; `scipy.io.loadmat` (or `h5py` for v7.3 files) can read them.
4. Write your loader in `scripts/load_janelia_data.py`. Never commit the data itself.
