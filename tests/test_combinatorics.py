import pytest
import numpy as np
import math




from src.combinatorics import (
    omega_exact,
    ln_omega_logspace,
    omega_logspace,
    ln_omega_stirling,
)

def test_omega_exact_small_N():
    """Verifies exact known values for combinations for N=7"""
    assert omega_exact(7, 0) == 1
    assert omega_exact(7, 1) == 7
    assert omega_exact(7, 3) == 35
    assert omega_exact(7, 7) == 1

def test_logspace_matches_exact():
    """Verifies that the logarithmic method (gammaln) matches the exact method for small N."""
    for N in [7, 10, 20]:
        for k in range(N + 1):
            exact_val = omega_exact(N, k)
            logspace_val = omega_logspace(N, k)
            assert logspace_val == pytest.approx(exact_val, rel=1e-6)

def test_symmetry():
    """Verifies the physical property of symmetry: Omega(N, k) == Omega(N, N - k)."""
    N = 50
    for k in range(N // 2 + 1):
        assert ln_omega_logspace(N, k) == pytest.approx(ln_omega_logspace(N, N - k))

def test_probability_normalization():
    """Verifies that the sum of all probabilities P(k) for a given N equals 1."""
    N = 80
    k_vals = np.arange(N + 1)
    ln_probs = ln_omega_logspace(N, k_vals) - N * np.log(2)
    probs = np.exp(ln_probs)
    assert np.sum(probs) == pytest.approx(1.0, rel=1e-5)

# ==============================================================================
# 1. PRUEBAS DE PRECISIÓN Y EXACTITUD HASTA EL LÍMITE DE COMA FLOTANTE
# ==============================================================================

def test_stirling_approximation():
    """Verifica que la aproximación de Stirling coincide con gammaln para N = 100."""
    N = 100
    k = 50
    ln_gammaln_val = ln_omega_logspace(N, k)
    ln_stirling_val = ln_omega_stirling(N, k)
    assert ln_stirling_val == pytest.approx(ln_gammaln_val, rel=5e-2)


def test_ln_omega_large_N_exact_boundary():
    """
    Verifica que ln_omega_logspace coincide exactamente con math.comb en N = 1029, k = 514,
    que es el límite superior absoluto antes de que la multiplicidad supere 1.79e308.
    """
    N = 1029
    k = 514
    
    # math.comb maneja enteros de precisión arbitraria sin desbordar
    exact_omega = math.comb(N, k)
    expected_ln_omega = math.log(exact_omega)
    
    calculated_ln_omega = ln_omega_logspace(N, k)
    assert calculated_ln_omega == pytest.approx(expected_ln_omega, rel=1e-5)


def test_omega_logspace_against_math_comb_max_finite():
    """
    Verifica que omega_logspace reconstruye la multiplicidad exacta para N = 1029, k = 514
    (Omega ~ 1.42 e308), el máximo valor finito representable en float64.
    """
    N = 1029
    k = 514
    exact_omega = math.comb(N, k)
    calculated_omega = omega_logspace(N, k)
    assert calculated_omega == pytest.approx(exact_omega, rel=1e-4)


def test_ln_omega_large_N_asymptotics():
    """
    Verifica que ln_omega_logspace funciona sin overflow para N muy grandes
    comprobando la distribución Gaussiana central en el pico k = N/2.
    """
    for N in [100, 1000, 100000]:
        k = N // 2
        ln_omega = ln_omega_logspace(N, k)
        expected_approx = N * np.log(2) - 0.5 * np.log(np.pi * N / 2)
        assert ln_omega == pytest.approx(expected_approx, rel=1e-3)


def test_thermodynamic_limit_avogadro():
    """
    Verifica que el código calcula en espacio logarítmico para el número de Avogadro N = 10^23
    sin desbordamiento numérico.
    """
    N = 1e23
    k = N / 2
    ln_omega = ln_omega_logspace(N, k)
    assert np.isfinite(ln_omega)
    assert ln_omega > 0


# ==============================================================================
# 2. PRUEBAS DE FRONTERAS COMPUTACIONALES (LIMITING FACTORS)
# ==============================================================================

def test_overflow_without_logspace_limit():
    """
    Demuestra la frontera de N! en float64:
    - N = 170 es el MÁXIMO N donde float(N!) no desborda (~7.25 e306).
    - N = 171 es el UMBRAL EXACTO donde float(N!) supera 1.79 e308 y lanza OverflowError.
    """
    # 1. En N = 170 float() aún no desborda
    assert np.isfinite(float(math.factorial(170)))
    
    # 2. En N = 171 desborda estrictamente
    with pytest.raises(OverflowError):
        _ = float(math.factorial(171))
    
    # 3. Tu función en espacio logarítmico maneja N = 171 sin problemas
    assert np.isfinite(ln_omega_logspace(171, 85))


def test_omega_logspace_exp_overflow():
    """
    Demuestra la frontera de la función exponencial exp(ln_omega):
    - N = 1029, k = 514 es el MÁXIMO estado donde Omega es finito (~1.42 e308).
    - N = 1030, k = 515 es el UMBRAL EXACTO donde exp() desborda a inf (~2.85 e308).
    """
    # N = 1029: Finito
    assert np.isfinite(omega_logspace(1029, 514))
    
    # N = 1030: Desborda a inf
    with pytest.warns(RuntimeWarning):
        val = omega_logspace(1030, 515)
        assert np.isinf(val)


def test_ram_limit_for_probability_array():
    """
    Demuestra el límite práctico de memoria RAM para el apartado d:
    Intentar instanciar el array discreto de puntos para N = 10^12 requiere ~8 Terabytes de RAM,
    provocando un MemoryError inmediato en NumPy.
    """
    N_huge = 1_000_000_000_000  # 1 billón de elementos (8 TB de RAM)
    with pytest.raises(MemoryError):
        _ = np.zeros(N_huge + 1, dtype=np.float64)