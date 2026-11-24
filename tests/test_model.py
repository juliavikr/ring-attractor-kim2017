"""
Sanity checks for the ring attractor model.   Run with:   pytest -q

If you change src/ring_model.py and a test fails, you probably broke
something. These tests encode facts from the paper that our model
must respect.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import ring_model as rm  # noqa: E402

N = 64


@pytest.mark.parametrize("model", ["local", "global"])
def test_single_bump_about_90_degrees(model):
    """Paper: ONE bump, roughly 90 degrees wide (Fig. 1I, 1J)."""
    W = rm.make_connectivity(model, N=N)
    u = rm.settle_bump(W)
    assert rm.count_bumps(u) == 1
    width_deg = np.degrees(rm.bump_width(u))
    assert 60 < width_deg < 100, width_deg


@pytest.mark.parametrize("model", ["local", "global"])
@pytest.mark.parametrize("center", [0.0, 1.0, 2.5, 4.0])
def test_bump_persists_anywhere(model, center):
    """Ring attractor = bump stays wherever it is put, with NO input."""
    W = rm.make_connectivity(model, N=N)
    u = rm.settle_bump(W, center=center, T=40)
    angle, _ = rm.population_vector(u)
    assert abs(rm.wrap_angle(angle - center)) < 2 * np.pi / N


def test_local_jump_threshold_is_constant():
    """Paper Fig. 4D/G: in the LOCAL model the input needed to make a narrow
    input cause a jump does not depend on the shift distance."""
    W = rm.make_connectivity("local", N=N)
    u = rm.settle_bump(W)
    amps = u.max() * np.linspace(1, 6, 21)
    first_jump = []
    for shift_deg in [90, 150]:
        out = rm.jump_or_flow(W, u, np.radians(shift_deg), amps, 0.2)
        first_jump.append(np.argmax(out == rm.JUMP))
    assert first_jump[0] == first_jump[1]


def test_global_needs_more_input_for_far_jumps():
    """Paper Fig. 4D: in the GLOBAL model far jumps need stronger input."""
    W = rm.make_connectivity("global", N=N)
    u = rm.settle_bump(W)
    amps = u.max() * np.linspace(1, 30, 30)
    first_jump = []
    for shift_deg in [60, 150]:
        out = rm.jump_or_flow(W, u, np.radians(shift_deg), amps, 0.2)
        first_jump.append(np.argmax(out == rm.JUMP))
    assert first_jump[1] > first_jump[0]


def test_population_vector_finds_angle():
    th = rm.ring_angles(N)
    u = rm.von_mises(th, 1.234, 5.0)
    angle, amp = rm.population_vector(u)
    assert abs(angle - 1.234) < 1e-6 and amp > 0
