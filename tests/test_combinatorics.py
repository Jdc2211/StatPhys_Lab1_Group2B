import math
import numpy as np
import pytest

from src.combinatorics import (
    ln_omega_logspace,
    ln_omega_stirling,
    ln_prob_asymptotic,
    omega_exact,
    omega_logspace,
)

LN2 = float(np.log(2.0))
FLOAT64_BYTES = 8

def relative_width(N):
    return 1.0 / float(np.sqrt(N))
    
def array_memory_bytes(N: int, itemsize: int = FLOAT64_BYTES) -> int:
    return (int(N) + 1) * itemsize

#corrections
def test_omega_exact_small_N():
    """Verifies exact known values for combinations for N=7"""
    assert [omega_exact(7, k) for k in range(8)] == [1, 7, 21, 35, 35, 21, 7, 1]

def test_omega_exact_matches_math_comb():
    """Verifies exact method matches math.comb for various N."""
    for N in range(0, 200, 7):
        for k in range(N + 1):
            assert omega_exact(N, k) == math.comb(N, k)

def test_omega_exact_out_of_range():
    """Verifies impossibility boundaries for physical states."""
    assert omega_exact(10, -1) == 0
    assert omega_exact(10, 11) == 0

def test_sum_of_multiplicities_is_2N():
    """sum_k Omega(N,k) = 2^N"""
    for N in (5, 7, 100, 150):
        assert sum(omega_exact(N, k) for k in range(N + 1)) == 2 ** N

def test_logspace_matches_exact():
    """Verifies that the logarithmic method (gammaln) matches the exact method for small N."""
    for N in [7, 10, 20, 100]:
        for k in range(N + 1):
            assert omega_logspace(N, k) == pytest.approx(omega_exact(N, k), rel=1e-10)

def test_logspace_scalar_and_vector_agree():
    """Verifies vectorization support for numpy arrays."""
    N = 60
    vec = ln_omega_logspace(N, np.arange(N + 1))
    for k in range(N + 1):
        assert vec[k] == pytest.approx(ln_omega_logspace(N, k))

def test_out_of_range_is_minus_inf():
    """Verifies out-of-bounds log-space probability evaluates to -inf."""
    assert ln_omega_logspace(10, -1) == -np.inf
    assert ln_omega_logspace(10, 11) == -np.inf
    vec = ln_omega_logspace(10, np.array([-1, 0, 5, 11]))
    assert vec[0] == -np.inf and vec[3] == -np.inf and np.isfinite(vec[1:3]).all()

def test_symmetry():
    """Verifies the physical property of symmetry: Omega(N, k) == Omega(N, N - k)."""
    N = 50
    for k in range(N // 2 + 1):
        assert ln_omega_logspace(N, k) == pytest.approx(ln_omega_logspace(N, N - k))

def test_probability_normalization():
    """Verifies that the sum of all probabilities P(k) for a given N equals 1."""
    N = 80
    k = np.arange(N + 1)
    assert np.exp(ln_omega_logspace(N, k) - N * LN2).sum() == pytest.approx(1.0, rel=1e-12)

#starling approximation tests
def test_stirling_close_to_gammaln_and_improves_with_N():
    """Verifies Stirling approximation converges as N increases."""
    errs = []
    for N in (10, 100, 1000):
        exact = ln_omega_logspace(N, N // 2)
        errs.append(abs(ln_omega_stirling(N, N // 2) - exact))
    assert errs[0] > errs[1] > errs[2]          # Absolute error decreases with N
    assert errs[1] < 0.05                       # N=100 bound

def test_stirling_edges_are_exact():
    """Verifies boundary condition precision in Stirling's formula."""
    assert ln_omega_stirling(100, 0) == 0.0
    assert ln_omega_stirling(100, 100) == 0.0

#N limits 

def test_factorial_float_limit_N170():
    """N! does not fit in float64 up from N = 171."""
    assert np.isfinite(float(math.factorial(170)))
    with pytest.raises(OverflowError):
        float(math.factorial(171))
    assert np.isfinite(ln_omega_logspace(171, 85))    # log-space avoids this issue

def test_ln_omega_matches_math_comb_at_1029():
    """Checks exact log match up to the maximum float limit."""
    N, k = 1029, 514
    assert ln_omega_logspace(N, k) == pytest.approx(math.log(math.comb(N, k)), rel=1e-12)

def test_omega_float_limit_N1029_vs_N1030():
    """Omega(N, N/2) stops fitting in float64 between N = 1029 y N = 1030."""
    assert np.isfinite(omega_logspace(1029, 514))
    assert omega_logspace(1029, 514) == pytest.approx(math.comb(1029, 514), rel=1e-10)
    with pytest.warns(RuntimeWarning):
        assert np.isinf(omega_logspace(1030, 515))

def test_ln_omega_never_overflows_for_huge_scalar_N():
    """ln(Omega) order N ln2: finite while N << 1e300."""
    assert np.isfinite(ln_omega_logspace(1e200, 5e199))

def test_memory_of_distribution_array():
    """storing N+1 points of P(k) costs 8(N+1) bytes."""
    assert array_memory_bytes(10 ** 8) == pytest.approx(8e8, rel=1e-6)       # 0.8 GB
    assert array_memory_bytes(10 ** 12) == pytest.approx(8e12, rel=1e-6)     # 8 TB
    assert array_memory_bytes(10 ** 23) > 1e23                               # ~8e23 B: impossible

#thermodynamic limit tests

def test_ln_omega_gaussian_peak():
    """Verifies log-space converges to expected Gaussian peak."""
    for N in (100, 1000, 100000):
        expected = N * LN2 - 0.5 * np.log(np.pi * N / 2)
        assert ln_omega_logspace(N, N // 2) == pytest.approx(expected, rel=1e-3)

def test_naive_logspace_fails_for_probability_at_avogadro():
    """Demonstrates that naive subtraction in log-space encounters precision issues at N=1e23."""
    N = 1e23
    exact = -0.5 * np.log(np.pi * N / 2)
    naive = ln_omega_logspace(N, N / 2) - N * LN2
    assert abs(naive - exact) > 1.0
    assert np.isfinite(ln_omega_logspace(N, N / 2)) and ln_omega_logspace(N, N / 2) > 0

def test_asymptotic_probability_at_avogadro():
    """Validates the correct analytical asymptotic function at the thermodynamic limit."""
    N = 1e23
    expected = -0.5 * np.log(np.pi * N / 2)                  # ~ -27.1
    assert ln_prob_asymptotic(N, N / 2) == pytest.approx(expected, rel=1e-10)
    assert np.exp(ln_prob_asymptotic(N, N / 2)) == pytest.approx(np.sqrt(2 / (np.pi * N)), rel=1e-10)

def test_asymptotic_matches_gammaln_for_moderate_N():
    """Checks continuous Gaussian approximation matches exact log-space values."""
    N = 1000
    for k in (300, 450, 500, 560):
        ref = ln_omega_logspace(N, k) - N * LN2
        assert ln_prob_asymptotic(N, k) == pytest.approx(ref, abs=2.5)

def test_gaussian_limit_near_peak():
    """Checks probability values within the 3-sigma region for massive N."""
    N = 1e23
    delta = 3 * np.sqrt(N) / 2                               # 3 sigma offset
    gauss = 0.5 * np.log(2 / (np.pi * N)) - 2 * delta ** 2 / N
    assert ln_prob_asymptotic(N, N / 2 + delta) == pytest.approx(gauss, abs=1e-3)

def test_relative_fluctuation_vanishes():
    """Proves the thermodynamic limit fluctuation ratio sigma/mu approaches zero."""
    assert relative_width(100) == pytest.approx(0.1)
    assert relative_width(1e23) == pytest.approx(3.16e-12, rel=1e-2)
    assert relative_width(1e23) < 1e-11

def test_one_percent_deviation_unlikely():
    """k = 0.51 N con N = 1e23: ln P ~ -2 N x^2/2 ~ -1e19 (P close to 0)."""
    N = 1e23
    assert ln_prob_asymptotic(N, 0.51 * N) < -1e18
