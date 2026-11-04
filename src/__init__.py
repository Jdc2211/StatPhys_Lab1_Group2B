"""
Statistical Physics Lab 1 Package.

This package provides modules for:
- combinatorics: Multiplicity and permutation calculations.
- microstates: Microstate generation and performance benchmarking.
- thermodynamics: Entropy and state variable evaluations.
"""

from .microstates import generate_microstates

__all__ = ["generate_microstates"]