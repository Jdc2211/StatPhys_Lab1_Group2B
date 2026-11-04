import pytest
import numpy as np




from src.combinatorics import (
    omega_exact,
    ln_omega_logspace,
    omega_logspace,
    ln_omega_stirling,
)

def test_omega_exact_small_N():
    """Verifica valores exactos conocidos de combinaciones para N = 7."""
    assert omega_exact(7, 0) == 1
    assert omega_exact(7, 1) == 7
    assert omega_exact(7, 3) == 35
    assert omega_exact(7, 7) == 1

def test_logspace_matches_exact():
    """Verifica que el método logarítmico (gammaln) coincida con el exacto en N pequeños."""
    for N in [7, 10, 20]:
        for k in range(N + 1):
            exact_val = omega_exact(N, k)
            logspace_val = omega_logspace(N, k)
            assert logspace_val == pytest.approx(exact_val, rel=1e-6)

def test_symmetry():
    """Comprueba la propiedad física de simetría: Omega(N, k) == Omega(N, N - k)."""
    N = 50
    for k in range(N // 2 + 1):
        assert ln_omega_logspace(N, k) == pytest.approx(ln_omega_logspace(N, N - k))

def test_probability_normalization():
    """Verifica que la suma de todas las probabilidades P(k) para un N sea igual a 1."""
    N = 80
    k_vals = np.arange(N + 1)
    ln_probs = ln_omega_logspace(N, k_vals) - N * np.log(2)
    probs = np.exp(ln_probs)
    assert np.sum(probs) == pytest.approx(1.0, rel=1e-5)

def test_stirling_approximation():
    """Comprueba que la aproximación de Stirling concuerde con gammaln en N = 100."""
    N = 100
    k = 50
    ln_gammaln_val = ln_omega_logspace(N, k)
    ln_stirling_val = ln_omega_stirling(N, k)
    assert ln_stirling_val == pytest.approx(ln_gammaln_val, rel=5e-2)