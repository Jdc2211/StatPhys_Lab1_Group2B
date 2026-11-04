import matplotlib.pyplot as plt

def omega(N, k):
    if k == 0:
        return 1
    num, den = 1, 1
    for i in range(k):
        num *= (N - i)
        den *= (k - i)
    return num // den

for N in [20, 50, 80, 100]:
    k_vals = list(range(N + 1))
    probs = [omega(N, k) / (2**N) for k in k_vals]
    plt.plot(k_vals, probs, label=f"N = {N}")

plt.xlabel("k (Number of Heads)")
plt.ylabel("Probability P(k)")
plt.legend()
plt.grid(True)
plt.show()


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
    Calcula ln(Omega(N, k)) en espacio logarítmico usando gammaln
    para evitar el desbordamiento numérico (integer overflow) cuando N >= 100.
    Aprovecha la propiedad: ln(N!) = gammaln(N + 1)
    """
    if k < 0 or k > N:
        return -np.inf
    return gammaln(N + 1) - gammaln(k + 1) - gammaln(N - k + 1)

def omega_logspace(N, k):
    """Devuelve la multiplicidad Omega(N, k) convirtiendo desde espacio logarítmico."""
    return np.exp(ln_omega_logspace(N, k))

def ln_stirling(N):
    """Aproximación de Stirling para ln(N!) ≈ N ln(N) - N (límite termodinámico)."""
    if N <= 0:
        return 0.0
    return N * np.log(N) - N

def ln_omega_stirling(N, k):
    """Calcula ln(Omega(N, k)) aplicando la aproximación de Stirling."""
    if k <= 0 or k >= N:
        return 0.0
    return ln_stirling(N) - ln_stirling(k) - ln_stirling(N - k)

def plot_probability_distributions(N_list=[20, 50, 80, 100]):
    """Grafica la distribución P(k) en espacio logarítmico para N = 20, 50, 80, 100."""
    plt.figure(figsize=(8, 5))
    for N in N_list:
        k_vals = np.arange(N + 1)
        # ln P(k) = ln Omega(N, k) - N * ln(2)
        ln_probs = ln_omega_logspace(N, k_vals) - N * np.log(2)
        probs = np.exp(ln_probs)
        plt.plot(k_vals / N, probs, label=f"N = {N}")
    
    plt.xlabel("Fracción de Caras (k / N)")
    plt.ylabel("Probabilidad P(k)")
    plt.title("Distribución de Probabilidad de Macroestados (Espacio Logarítmico)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_probability_distributions()

    
