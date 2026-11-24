"""
ring_model.py - A beginner-friendly ring attractor model
=========================================================

This file implements the firing-rate ring attractor models used in

    Kim, Rouault, Druckmann & Jayaraman (2017),
    "Ring attractor dynamics in the Drosophila central brain", Science 356:849.

It is a Python translation of the authors' C++ code
(https://github.com/hrouault/RingAttractor, file ring_attractor/src/dyna.cpp),
written to be READ and UNDERSTOOD, not to be as fast as possible.
Original code Copyright (c) 2016 Howard Hughes Medical Institute, BSD-3
license (see the NOTICE file at the root of this repository).

THE BIG IDEA
------------
Imagine N neurons arranged on a circle. Neuron i "prefers" the heading angle

    theta_i = 2*pi*i / N        (0 ... 2*pi)

Each neuron has a firing rate u_i(t) >= 0 that obeys

    tau * du_i/dt = -u_i + [ sum_j W_ij u_j  +  b  +  I_i(t) ]_+

    - "-u_i"       : leak. Without input, activity decays back to 0.
    - W_ij         : recurrent connection from neuron j to neuron i.
                     It depends only on the angular distance between i and j.
    - b = 1        : constant background drive (same for every neuron).
    - I_i(t)       : external input (visual landmark, or optogenetic laser).
    - [x]_+        : "threshold-linear" = max(x, 0). Rates can't be negative.

We measure time in units of tau (so tau = 1).

With the right W, the network has a stable "bump" of activity that can sit
anywhere on the ring -> the bump position IS the fly's heading estimate.

THE THREE CONNECTIVITY PROFILES (what the paper compares)
---------------------------------------------------------
1. LOCAL model  (paper Fig. 4D top, fig. S3D)
       each neuron excites itself (alpha) and its immediate neighbours
       (diffusion-like coupling D), and EVERY neuron inhibits every other
       neuron equally (flat inhibition beta).
       -> "local excitation + global (flat) inhibition"  <- the paper's winner

2. GLOBAL model (paper Fig. 4D bottom, fig. S3B)
       W_ij = J0 + J1*cos(theta_i - theta_j)
       a smooth cosine profile: excitation spreads over the whole ring.

3. WINNER-TAKE-ALL (WTA) model (fig. S3A)
       self-excitation alpha, uniform inhibition -beta to all others.
       It has a unique bump but NO notion of "neighbours" -> bumps can't flow.

Parameter values below are the ones in the authors' code (para_sweep.cpp).
"""

import numpy as np

# Reference ring size used by the authors. We keep the *continuous* model the
# same when you change N, so N=64 or N=128 gives (almost) the same results,
# just faster.
N_REF = 256


# ---------------------------------------------------------------------------
# Helper: angles and angular distances
# ---------------------------------------------------------------------------
def ring_angles(N):
    """Preferred angles of the N neurons, in radians, from 0 to 2*pi (excl.)."""
    return 2 * np.pi * np.arange(N) / N


def wrap_angle(x):
    """Wrap any angle into the interval (-pi, pi]."""
    return (x + np.pi) % (2 * np.pi) - np.pi


def von_mises(x, mu, kappa):
    """
    Bell-shaped bump on a circle, peak value 1 at x = mu.

    kappa controls the width: big kappa = narrow, small kappa = broad.
    The authors parametrise width w through kappa = 1 / w**2.
    (Same formula as `vonmises()` in dyna.cpp.)
    """
    if kappa > 5:
        return np.exp(kappa * (np.cos(x - mu) - 1))
    # for broad profiles they rescale so the minimum is exactly 0
    return (np.exp(kappa * (np.cos(x - mu) + 1)) - 1) / (np.exp(2 * kappa) - 1)


# ---------------------------------------------------------------------------
# Connectivity matrices
# ---------------------------------------------------------------------------
def _circulant(profile):
    """
    Build an N x N matrix W with W[i, j] = profile[(i - j) mod N].
    i.e. the weight only depends on the distance between neurons i and j.
    """
    N = len(profile)
    idx = (np.arange(N)[:, None] - np.arange(N)[None, :]) % N
    return profile[idx]


def connectivity_local(N=128, alpha=3.0, beta=20.0, D=0.1):
    """
    LOCAL model: self-excitation alpha, nearest-neighbour coupling D
    (a discrete second derivative, like diffusion), flat inhibition beta.

        sum_j W_ij u_j = alpha*u_i + D * d2u/dtheta2 - beta * (integral of u)

    Matches init_connect_delta() in dyna.cpp.
    """
    dx = 2 * np.pi / N
    profile = np.full(N, -beta * dx)       # flat inhibition (everyone)
    profile[0] += alpha                    # self-excitation
    profile[1] += D / dx**2                # neighbour on one side
    profile[-1] += D / dx**2               # neighbour on the other side
    profile[0] -= 2 * D / dx**2            # (completes the Laplacian)
    return _circulant(profile)


def connectivity_global(N=128, J0=-0.2, J1=0.15):
    """
    GLOBAL model: cosine-shaped connectivity W = J0 + J1*cos(dtheta).

    J0 < 0 : uniform inhibition,  J1 > 0 : cosine-shaped excitation.
    The authors used N=256; we rescale by N_REF/N so the total synaptic
    weight (and therefore the behaviour) does not depend on N.
    Matches init_connect_cosine() in dyna.cpp.
    """
    profile = (J0 + J1 * np.cos(ring_angles(N))) * (N_REF / N)
    return _circulant(profile)


def connectivity_wta(N=128, alpha=0.5, beta=1.0):
    """
    WINNER-TAKE-ALL: self-excitation alpha, inhibition -beta from every
    other neuron. No neighbour interactions (same structure as
    init_connect_wta() in dyna.cpp).

    Our own parameter choice (the paper gives none for this model):
    alpha < 1 keeps the winner stable: it settles at u* = b / (1 - alpha) = 2,
    and beta * u* > b silences every other neuron.
    Note: the WTA "bump" is a single neuron wide - it has no shape.
    """
    profile = np.full(N, -beta)
    profile[0] = alpha
    return _circulant(profile)


MODELS = {
    "local": connectivity_local,
    "global": connectivity_global,
    "wta": connectivity_wta,
}


def make_connectivity(model="local", N=128, **params):
    """Convenience wrapper: make_connectivity('local', N=128)."""
    return MODELS[model](N=N, **params)


# ---------------------------------------------------------------------------
# Dynamics
# ---------------------------------------------------------------------------
def rate_derivative(u, W, I, b=1.0):
    """
    du/dt for the threshold-linear network.

    u : array (..., N)   current firing rates (can be a batch of networks)
    W : array (N, N)     connectivity
    I : array (..., N)   external input
    """
    recurrent = u @ W.T                      # sum_j W_ij u_j
    return -u + np.maximum(recurrent + b + I, 0.0)


def simulate(W, u0, inputs, T, dt=0.005, noise_std=0.0, record_every=10,
             rng=None, b=1.0):
    """
    Integrate the network forward in time.

    Parameters
    ----------
    W          : (N, N) connectivity matrix
    u0         : (N,) or (B, N) initial rates  (B = several networks at once)
    inputs     : either a fixed array (N,) / (B, N),
                 or a function  inputs(t) -> array  (for time-varying input)
    T          : total simulated time (in units of tau)
    dt         : time step. 0.005 is safe for N <= 128.
                 Use smaller dt (e.g. 0.001) for N=256 with the local model.
    noise_std  : strength of white noise added to the firing rates
                 (used for drift simulations, Fig. 3). 0 = deterministic.
                 Tip: keep it SMALL (around 0.02-0.05 x the bump peak).
                 Too much noise does not make the bump drift faster - it
                 kills the bump (the network falls into a near-silent state).
    record_every : store the state every this many steps

    Returns
    -------
    t_rec : (n_rec,) recorded times
    u_rec : (n_rec, N) or (n_rec, B, N) recorded rates

    Method: 4th-order Runge-Kutta (like the authors) when noise_std == 0,
            Euler-Maruyama when there is noise:
                u <- u + dt * du/dt + noise_std * sqrt(dt) * gaussian
            followed by u <- max(u, 0) so rates stay non-negative.
    """
    rng = np.random.default_rng() if rng is None else rng
    u = np.array(u0, dtype=float)
    n_steps = int(round(T / dt))
    get_I = inputs if callable(inputs) else (lambda t: inputs)

    t_rec, u_rec = [0.0], [u.copy()]
    for k in range(n_steps):
        t = k * dt
        I = get_I(t)
        if noise_std > 0:
            # Euler-Maruyama. The sqrt(dt) makes the noise strength
            # independent of the time step you choose.
            xi = rng.normal(0.0, 1.0, size=u.shape)
            u = u + dt * rate_derivative(u, W, I, b) + noise_std * np.sqrt(dt) * xi
            u = np.maximum(u, 0.0)
        else:
            # classic RK4
            k1 = rate_derivative(u, W, I, b)
            k2 = rate_derivative(u + 0.5 * dt * k1, W, I, b)
            k3 = rate_derivative(u + 0.5 * dt * k2, W, I, b)
            k4 = rate_derivative(u + dt * k3, W, I, b)
            u = u + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        if (k + 1) % record_every == 0 or k == n_steps - 1:
            t_rec.append((k + 1) * dt)
            u_rec.append(u.copy())
    return np.array(t_rec), np.array(u_rec)


def initial_bump(N, center=0.0, height=10.0, half_width_neurons=1):
    """
    A tiny 'seed' of activity at `center`, like the authors use
    (they set 3 neurons to 10 and everything else to 0).
    Run `settle_bump` afterwards to let the network shape the real bump.
    """
    u0 = np.zeros(N)
    i0 = int(round(center / (2 * np.pi) * N)) % N
    for d in range(-half_width_neurons, half_width_neurons + 1):
        u0[(i0 + d) % N] = height
    return u0


def settle_bump(W, center=0.0, T=20.0, dt=0.005):
    """Create a seed at `center` and let the network relax (no input)."""
    N = W.shape[0]
    u0 = initial_bump(N, center)
    _, u = simulate(W, u0, np.zeros(N), T=T, dt=dt, record_every=10**9)
    return u[-1]


# ---------------------------------------------------------------------------
# Read-outs (what experimentalists compute from imaging data)
# ---------------------------------------------------------------------------
def population_vector(u):
    """
    Population Vector Average (PVA), the read-out used in the paper (Fig. 1F).

    Each neuron is an arrow pointing at its preferred angle with length equal
    to its activity; summing the arrows gives the bump position (direction)
    and strength (length).

    Returns (angle in (-pi, pi], amplitude)   - works on (..., N) arrays.
    """
    u = np.asarray(u)
    N = u.shape[-1]
    th = ring_angles(N)
    z = (u * np.exp(1j * th)).sum(axis=-1)
    return np.angle(z), np.abs(z) / N


def bump_peak(u):
    """Angle (in (-pi, pi]) of the most active neuron."""
    N = np.asarray(u).shape[-1]
    return wrap_angle(ring_angles(N)[np.argmax(u, axis=-1)])


def bump_width(u, threshold=1e-6):
    """
    Full width of the active region (radians): number of neurons with
    activity above `threshold`, times the angular spacing.
    The paper's bump is ~90 degrees wide (pi/2).
    """
    u = np.asarray(u)
    N = u.shape[-1]
    return (u > threshold).sum(axis=-1) * 2 * np.pi / N


def count_bumps(u, rel_threshold=0.1):
    """Number of separate active regions (local maxima above 10% of the max)."""
    u = np.asarray(u)
    left, right = np.roll(u, 1), np.roll(u, -1)
    peaks = (u > left) & (u >= right) & (u > rel_threshold * u.max())
    return int(peaks.sum())


# ---------------------------------------------------------------------------
# The "jump vs flow" experiment (paper Fig. 4)
# ---------------------------------------------------------------------------
NO_EFFECT, FLOW, JUMP = 0, 1, 2
OUTCOME_NAMES = {NO_EFFECT: "no effect", FLOW: "flow", JUMP: "jump"}


def jump_or_flow(W, u_bump, shift, input_amp, input_width, T=20.0, dt=0.005):
    """
    Reproduces the classification used in the authors' code
    (input_inner_loop in dyna.cpp):

    1. Start from a settled bump centred at angle 0 (u_bump).
    2. Switch on an input bump centred at `shift` (radians), with peak
       `input_amp` and width `input_width` (von Mises, kappa = 1/width^2).
    3. Watch where the PEAK of the activity is:
         - stays within 22.5 deg of 0 for the whole time  -> NO EFFECT
         - first leaves the 22.5 deg zone at a place < 45 deg -> FLOW
           (it moved continuously through neighbouring neurons)
         - first appears beyond 45 deg                    -> JUMP
           (it disappeared and re-appeared at the input location)

    Works on a batch: input_amp and input_width can be arrays of the same
    shape; then all those networks are simulated in parallel (fast!).
    Returns an int array of outcomes (0/1/2).
    """
    N = W.shape[0]
    th = ring_angles(N)
    amps = np.atleast_1d(np.asarray(input_amp, dtype=float))
    widths = np.atleast_1d(np.asarray(input_width, dtype=float))
    amps, widths = np.broadcast_arrays(amps, widths)
    shape = amps.shape
    amps, widths = amps.ravel(), widths.ravel()
    B = amps.size

    I = np.stack([a * von_mises(th, shift, 1.0 / w**2)
                  for a, w in zip(amps, widths)])
    u = np.tile(u_bump, (B, 1))
    outcome = np.full(B, NO_EFFECT)
    decided = np.zeros(B, dtype=bool)

    lo, mid, hi = N // 16, N // 8, 7 * N // 8   # 22.5 deg, 45 deg, 315 deg
    for _ in range(int(round(T / dt))):
        k1 = rate_derivative(u, W, I)
        k2 = rate_derivative(u + 0.5 * dt * k1, W, I)
        k3 = rate_derivative(u + 0.5 * dt * k2, W, I)
        k4 = rate_derivative(u + dt * k3, W, I)
        u = u + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        pos = np.argmax(u, axis=1)
        moved = (pos > lo) & (pos < hi) & ~decided
        outcome[moved] = np.where(pos[moved] > mid, JUMP, FLOW)
        decided |= moved
        if decided.all():
            break
    return outcome.reshape(shape)


def inflection_width(input_width, N=1024):
    """
    The paper's x-axis in Fig. 4D is the "distance between the inflection
    points" of the von Mises input profile. Convert our width parameter
    (kappa = 1/width^2) into that distance (radians).
    """
    th = np.linspace(-np.pi, np.pi, N, endpoint=False)
    f = von_mises(th, 0.0, 1.0 / input_width**2)
    d2 = np.gradient(np.gradient(f, th), th)
    centre = N // 2
    # walk outward from the peak until the curvature changes sign
    right = np.argmax(d2[centre:] > 0)
    if right == 0:          # very broad: no inflection point inside the ring
        return 2 * np.pi
    return 2 * th[centre + right]


def normalized_input_strength(W, u_bump, input_amp, input_width, T=20.0,
                              dt=0.005):
    """
    The paper's y-axis in Fig. 4D: "input strength (normalized bump amplitude)".

    The authors measure how strong an input is by putting it ON TOP of the
    existing bump (same location, angle 0) and asking how much taller the bump
    becomes:  strength = (peak with input) / (peak without input).
    1 = no effect, 2 = input doubles the bump amplitude, etc.
    This lets you compare inputs between models AND with experiments, where
    the bump amplitude (Delta F / F) is what you can actually measure.

    Batched like jump_or_flow (input_amp, input_width arrays).
    """
    N = W.shape[0]
    th = ring_angles(N)
    amps, widths = np.broadcast_arrays(np.atleast_1d(input_amp).astype(float),
                                       np.atleast_1d(input_width).astype(float))
    shape = amps.shape
    I = np.stack([a * von_mises(th, 0.0, 1.0 / w**2)
                  for a, w in zip(amps.ravel(), widths.ravel())])
    u0 = np.tile(u_bump, (I.shape[0], 1))
    _, u = simulate(W, u0, I, T=T, dt=dt, record_every=10**9)
    return (u[-1].max(axis=1) / u_bump.max()).reshape(shape)


def jump_flow_phase_diagram(W, u_bump, shift, amps, widths, dt=0.005):
    """
    Full Fig. 4D panel for one model and one shift distance.

    amps, widths : 1D arrays of input peak amplitudes and width parameters.
    Returns a dict with 2D arrays (len(widths) x len(amps)):
        'outcome'   : 0 no effect / 1 flow / 2 jump
        'strength'  : normalized input strength (y-axis of the paper)
        'x_width'   : distance between inflection points (x-axis, radians)
    """
    A, Wd = np.meshgrid(amps, widths)
    return {
        "outcome": jump_or_flow(W, u_bump, shift, A, Wd, dt=dt),
        "strength": normalized_input_strength(W, u_bump, A, Wd, dt=dt),
        "x_width": np.vectorize(inflection_width)(Wd),
    }
