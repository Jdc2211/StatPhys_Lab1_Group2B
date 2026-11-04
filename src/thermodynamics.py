"""
Thermodynamics module additions for Questions 10 & 11.
Analyzes relative fluctuations, micro-reversibility, and the thermodynamic limit (N -> 10^23).
"""

import numpy as np


def relative_fluctuation(N: float) -> float:
	"""
	Computes the relative fluctuation sigma / mu for a binary system of size N.
	For a binomial distribution B(N, 0.5):
		mu = N / 2
		sigma = sqrt(N) / 2
		sigma / mu = 1 / sqrt(N)
	"""
	return 1.0 / np.sqrt(N)


def log_spontaneous_ordering_prob(N: float) -> float:
	"""
	Computes natural log of probability of full spontaneous ordering (e.g. k = N).
	P(k = N) = (1/2)^N  =>  ln(P) = -N * ln(2)
	Prevents floating-point underflow for macroscopic N (N -> 10^23).
	"""
	return -N * np.log(2.0)


def analyze_thermodynamic_limit(N_values: list[float]) -> dict:
	"""
	Evaluates system scaling from finite sizes to the thermodynamic limit (N ~ 10^23).
	Returns mean, std, relative fluctuation, and log probability of extreme state.
	"""
	results = {
		"N": N_values,
		"mean_mu": [N / 2.0 for N in N_values],
		"std_sigma": [0.5 * np.sqrt(N) for N in N_values],
		"rel_fluctuation": [relative_fluctuation(N) for N in N_values],
		"ln_prob_extreme": [log_spontaneous_ordering_prob(N) for N in N_values],
	}
	return results
