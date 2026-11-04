import numpy as np
from scipy.special import gammaln
import matplotlib.pyplot as plt

def omega_exact(N, k):
    """Calcula la multiplicidad Omega(N, k) exacta mediante enteros (para N pequeños)."""
    if k < 0 or k > N:
        return 0
    if k == 0 or k == N:
        return 1
    num, den = 1, 1
    for i in range(1, k + 1):
        num *= (N - (k - i))
        den *= i
    return num // den

def ln_omega_logspace(N, k):
    """
    Calcula ln(Omega(N, k)) en espacio logarítmico usando gammaln.
    Soporta tanto un único valor k como vectores/arrays de NumPy.
    """
    k_arr = np.asarray(k)
    res = gammaln(N + 1) - gammaln(k_arr + 1) - gammaln(N - k_arr + 1)
    
    if np.isscalar(k):
        if k < 0 or k > N:
            return -np.inf
        return float(res)
    else:
        invalid = (k_arr < 0) | (k_arr > N)
        res = res.astype(float)
        res[invalid] = -np.inf
        return res

def omega_logspace(N, k):
    """Devuelve la multiplicidad Omega(N, k) convirtiendo desde espacio logarítmico."""
    return np.exp(ln_omega_logspace(N, k))

def ln_stirling(N):
    """
    Aproximación de Stirling completa: ln(N!) ≈ N ln(N) - N + 0.5*ln(2*pi*N).
    """
    if np.isscalar(N):
        if N <= 0:
            return 0.0
        return N * np.log(N) - N + 0.5 * np.log(2 * np.pi * N)
    else:
        N_arr = np.asarray(N, dtype=float)
        res = np.zeros_like(N_arr)
        mask = N_arr > 0
        res[mask] = N_arr[mask] * np.log(N_arr[mask]) - N_arr[mask] + 0.5 * np.log(2 * np.pi * N_arr[mask])
        return res

def ln_omega_stirling(N, k):
    """Calcula ln(Omega(N, k)) aplicando la aproximación de Stirling."""
    if np.isscalar(k):
        if k <= 0 or k >= N:
            return 0.0
    return ln_stirling(N) - ln_stirling(k) - ln_stirling(N - k)

def plot_probability_distributions(N_list=[20, 50, 80, 100]):
    """Grafica la distribución P(k) en espacio logarítmico para N = 20, 50, 80, 100."""
    plt.figure(figsize=(8, 5))
    for N in N_list:
        k_vals = np.arange(N + 1)
        ln_probs = ln_omega_logspace(N, k_vals) - N * np.log(2)
        probs = np.exp(ln_probs)
        plt.plot(k_vals / N, probs, label=f"N = {N}")
    
    plt.xlabel("Heads Fraction(k / N)")
    plt.ylabel("Probabilidad P(k)")
    plt.title("Distribución de Probabilidad de Macroestados (Espacio Logarítmico)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_probability_distributions()