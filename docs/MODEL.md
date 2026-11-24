# ⚙️ The model: equations, parameters, and how our code maps to the authors'

Owner: **Luiz** (keep this file correct; everyone should understand it)

## 1. The equation

N rate neurons on a ring, neuron *i* prefers angle θᵢ = 2πi/N:

```
τ du_i/dt = −u_i + [ Σ_j W_ij u_j + b + I_i(t) ]₊          b = 1,  τ = 1
```

`[x]₊ = max(x, 0)` (threshold-linear). Time is in units of τ.
Integration: 4th-order Runge–Kutta, like the authors (`dynamics_rk4step_fft` in `dyna.cpp`).

## 2. The connectivities

W_ij depends only on the distance θᵢ − θⱼ (it is *circulant*; the authors use an FFT for speed, we just use a matrix).

| Model | Weight profile | Parameters (authors' `para_sweep.cpp`) | Our function |
|---|---|---|---|
| **Local** (fig. S3D) | self α, neighbours D/dx² (a discrete Laplacian), everyone −β·dx | α = 3, β = 20, D = 0.1 | `connectivity_local` |
| **Global** (fig. S3B) | J₀ + J₁ cos(Δθ) | J₀ = −0.2, J₁ = 0.15 (for N = 256) | `connectivity_global` |
| **WTA** (fig. S3A) | self α, everyone else −β | *our choice:* α = 0.5, β = 1 | `connectivity_wta` |

In continuous form, the local model's recurrent input is
`α u(θ) + D ∂²u/∂θ² − β ∫u dθ`, i.e. **local excitation + flat global inhibition**.

**N-independence.** The authors use N = 256. We scale the weights (dx factors, and N_REF/N for the global model) so N = 64 or 128 gives the same bump. Our tests check that. N = 64 is ~10× faster than 256 and is what the scripts use.

**Time step.** The local model has stiff neighbour coupling (D/dx²). dt = 0.005 is stable for N ≤ 128; use dt = 0.001 for N = 256.

## 3. The jump-vs-flow protocol (Fig. 4D)

Translated from `input_inner_loop()` / `jump_vs_flow_input()` in `dyna.cpp`:

1. Settle a bump centred at 0 (seed 3 neurons, run 20 τ with no input).
2. Switch on a von Mises input `I = A · vM(θ; shift, κ = 1/w²)`.
3. Track the peak (argmax). The first time it leaves the ±22.5° zone (N/16 neurons) and before 20 τ:
   - if it is beyond 45° (N/8) → **JUMP**
   - otherwise → **FLOW**
   - never leaves → **NO EFFECT**
4. **y-axis** ("input strength, normalized bump amplitude"): apply the same input *at the bump location* and report `peak_with_input / peak_without`.
5. **x-axis** ("input width"): distance between the inflection points of the von Mises input profile.

## 4. Things that are *our* choices (say so in the talk!)
- The WTA parameters (the paper gives none).
- Noise: additive white noise on the rates, then rectified (`simulate(noise_std=...)`). The authors' `noisy_simu` puts Gaussian noise on the input instead. Ours was more stable for small N.
- Coarser parameter grids than the authors (they used 160 widths × 40 amplitudes + refinement).
- Time is in units of τ, so we don't claim real seconds.

## 5. Results check (N = 64)

| | 60° | 90° | 120° | 150° |
|---|---|---|---|---|
| Local: normalized jump threshold (narrow input) | 1.37 | 1.37 | 1.37 | 1.37 |
| Global: normalized jump threshold (narrow input) | 2.5 | 4.5 | 6.9 | 8.8 |

The paper's Fig. 4D shows the same qualitative pattern (local flat at ≈1.35; global increasing).
