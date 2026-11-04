"""Unit tests for src/thermodynamics.py, checked against exact integer values."""
from math import comb, log

import pytest

from src.thermodynamics import (
    prob_log_scale,
    cumulative_prob,
    entropy_change,
    likelihood_ratio,
    waiting_time,
    compute_results,
)


@pytest.mark.parametrize("N", [7, 20, 50, 100, 123, 199])
def test_prob_matches_exact(N):
    for k in range(N + 1):
        assert prob_log_scale(N, k) == pytest.approx(comb(N, k) / 2**N, rel=1e-10)


@pytest.mark.parametrize("N", [7, 100, 123])
def test_probabilities_sum_to_one(N):
    assert cumulative_prob(N, 0, N) == pytest.approx(1.0, abs=1e-12)


@pytest.mark.parametrize("N", [7, 100, 123])
def test_symmetry(N):
    for k in range(N + 1):
        assert prob_log_scale(N, k) == pytest.approx(prob_log_scale(N, N - k), rel=1e-10)


def test_maximum_at_half():
    N = 123
    probs = [prob_log_scale(N, k) for k in range(N + 1)]
    # N is odd, so k = 61 and k = 62 tie for the maximum
    assert probs.index(max(probs)) in (N // 2, N // 2 + 1)


def test_out_of_range_is_zero():
    assert prob_log_scale(10, 11) == 0.0
    assert prob_log_scale(10, -1) == 0.0


def test_cumulative_matches_exact_sum():
    N, half = 123, 61
    exact = sum(comb(N, k) for k in range(half - 10, half + 11)) / 2**N
    assert cumulative_prob(N, half - 10, half + 10) == pytest.approx(exact, rel=1e-10)


def test_entropy_change_matches_exact():
    N = 123
    assert entropy_change(N, 86, 61) == pytest.approx(log(comb(N, 86) / comb(N, 61)), rel=1e-10)


def test_entropy_change_same_state_is_zero():
    assert entropy_change(123, 40, 40) == pytest.approx(0.0, abs=1e-12)


def test_likelihood_ratio_matches_exact():
    N = 123
    assert likelihood_ratio(N, 61, 51) == pytest.approx(comb(N, 61) / comb(N, 51), rel=1e-10)


def test_waiting_time_matches_exact():
    N = 123
    assert waiting_time(N, 8) == pytest.approx(2**N / comb(N, 8), rel=1e-10)


def test_compute_results_reference_values():
    r = compute_results()
    assert r["N"] == 123
    assert r["half"] == 61
    assert r["prob_30"] == pytest.approx(3.7226e-09, rel=1e-3)
    assert r["prob_half"] == pytest.approx(0.071508, rel=1e-3)
    assert r["cumulative_c"] == pytest.approx(0.94112, rel=1e-3)
    assert r["dS_g"] == pytest.approx(30.3446, rel=1e-3)
