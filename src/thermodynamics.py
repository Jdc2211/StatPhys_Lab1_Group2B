import numpy as np
from src.combinatorics import ln_omega_logspace


"""Probability of macrostate computed in log-space"""
def prob_log_scale(N: int, k: int) -> float: 
    return float(np.exp(ln_omega_logspace(N,k) - N * np.log(2) ))

"""Cumulative probability: Sum of probabilities of macrostates from k_1 to k_2"""
def cumulative_prob(N: int, k_1: int, k_2: int) -> float:
    return sum(prob_log_scale(N, k) for k in range(k_1, k_2 + 1))

"""Entropy change delta S over Kb"""
def entropy_change(N: int, k_1: int, k_2: int) -> float:
    return float(ln_omega_logspace(N, k_1) - ln_omega_logspace(N, k_2))

def likelihood_ratio(N: int, k_1: int, k_2: int) -> float:
    return float(np.exp(entropy_change(N, k_1, k_2)))

"""Expected waiting time in seconds at one toss of the N coins per second"""
def waiting_time(N: int, k: int) -> float:
    return float(np.exp(N * np.log(2) - ln_omega_logspace(N, k)))


def compute_results(last_digits=(50, 96, 10, 23)) -> dict:
    """Compute M, N and every quantity of the Table 3 (questions a-i)."""
    M = len(last_digits) / sum(1 / d for d in last_digits)
    N = round(100 + M)
    half = N // 2
    return {
        "M": M, "N": N, "half": half,
        "prob_30": prob_log_scale(N, 30),
        "prob_half": prob_log_scale(N, half),
        "cumulative_c": cumulative_prob(N, half - 10, half + 10),
        "cumulative_d": cumulative_prob(N, half - 20, half + 20),
        "dS_e": entropy_change(N, half + 25, half),
        "dS_f": entropy_change(N, half + 10, half),
        "dS_g": entropy_change(N, half, 20),
        "t_8_seconds": waiting_time(N, 8),
        "ratio_minus": likelihood_ratio(N, half, half - 10),
        "ratio_plus": likelihood_ratio(N, half, half + 10),
    }
