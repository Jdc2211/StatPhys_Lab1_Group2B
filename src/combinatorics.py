import numpy as np
from scipy.special import gammaln
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

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

# 2. Log-space (Required for N >= 100 to avoid overflow)
def ln_omega_logspace(N, k):
    """
    Calculate ln(Omega(N, k)) in logarithmic space using gammaln.
    Supports both a single value k and vectors/arrays of NumPy.
    """
    k_array = np.asarray(k, dtype=float)
    invalid = (k_array < 0) | (k_array > N)
    k_safe = np.where(invalid, 0.0, k_array)
    res = gammaln(N + 1) - gammaln(k_safe + 1) - gammaln(N - k_safe + 1)
    
    if np.isscalar(k):
        if k < 0 or k > N:
            return -np.inf
        return float(res)
    else:
        res = res.astype(float)
        res[invalid] = -np.inf
        return res

def omega_logspace(N, k):
    """Returns the multiplicity Omega(N, k) by converting from logarithmic space."""
    return np.exp(ln_omega_logspace(N, k))

# 3. Stirling Approximation
def ln_stirling(N):
    """
    Complete Stirling approximation: ln(N!) ≈ N ln(N) - N + 0.5*ln(2*pi*N).
    """
    if np.isscalar(N):
        if N <= 0:
            return 0.0
        return N * np.log(N) - N + 0.5 * np.log(2 * np.pi * N)
    else:
        N_array=np.asarray(N, dtype=float)
        res = np.zeros_like(N_array)
        mask = N_array>0
        res[mask] = N_array[mask] * np.log(N_array[mask]) - N_array[mask] + 0.5 * np.log(2 * np.pi * N_array[mask])
        return res

def ln_omega_stirling(N, k):
    """Calculate ln(Omega(N, k)) applying the Stirling approximation."""
    if np.isscalar(k):
        if k <= 0 or k >= N:
            return 0.0
    return ln_stirling(N) - ln_stirling(k) - ln_stirling(N - k)

# 4. Thermodynamic Limit (N -> 10^23)
def ln_prob_asymptotic(N, k):
    """
    Log-probability for the thermodynamic limit (N ~ 10^23).
    Derived from Stirling, yielding a continuous Gaussian distribution centered at mu = N/2 
    """
    N = float(N)
    k = np.asarray(k, dtype=float)
    # Gaussian approximation in logarithmic space
    return 0.5 * np.log(2 / (np.pi * N)) - (2 * (k - N / 2)**2) / N

# 5. Plotting
def plot_probability_distribution_fraction(N_list=[20, 50, 80, 100]):
    """Plots the distribution P(k) in logarithmic space for N = 20, 50, 80, 100."""
    fig=plt.figure(figsize=(8, 5))
    for N in N_list:
        k_vals = np.arange(N + 1)
        ln_probs = ln_omega_logspace(N, k_vals) - N * np.log(2)
        probs = np.exp(ln_probs)
        plt.plot(k_vals / N, probs, label=f"N = {N}")
    
    plt.xlabel("Heads Fraction (k / N)")
    plt.ylabel("Probability P(k)")
    plt.title("Distribution of Probability of Macrostates (Logarithmic Space)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return fig


def plot_probability_distributions(N_list=[20, 50, 80, 100]):
    """Plots probability P(k) in linear space against absolute k."""
    fig=plt.figure(figsize=(8, 5))
    for N in N_list:
        k_vals = np.arange(N + 1)
        ln_probs = ln_omega_logspace(N, k_vals) - N * np.log(2)
        probs = np.exp(ln_probs)
        plt.plot(k_vals, probs, '.-', label=f"N = {N}")
    
    plt.xlabel("k (Number of Heads)")
    plt.ylabel("Probability P(k)")
    plt.title("Distribution of Probability of Macrostates")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return fig


def plot_multiplicity(N_list=[20, 50, 80, 100]):
    """Plots multiplicity Omega(N,k) in logarithmic space against absolute k."""
    fig = plt.figure(figsize=(8, 5))
    for N in N_list:
        k_vals = np.arange(N + 1)
        ln_omega = ln_omega_logspace(N, k_vals)
        plt.semilogy(k_vals, np.exp(ln_omega), '.-', label=f"N = {N}")
        
    plt.xlabel("k (Number of Heads)")
    plt.ylabel(r"Multiplicity $\Omega(N,k)$")
    plt.title("Multiplicity of Macrostates (Logarithmic Scale)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    output_path = "report/figures/combined_figures.pdf"

    
    with PdfPages(output_path) as pdf:
        fig1 = plot_multiplicity()
        pdf.savefig(fig1)
        plt.close(fig1) 
        fig2 = plot_probability_distributions()
        pdf.savefig(fig2)
        plt.close(fig2)
        
        fig3 = plot_probability_distribution_fraction()
        pdf.savefig(fig3)
        plt.close(fig3)
