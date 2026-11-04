import pytest
from src.microstates import (
    generate_microstates_baseline,
    generate_microstates_bitwise,
    measure_microstates_optimized
)

def test_baseline_microstates():
    states, t, mem = generate_microstates_baseline(3)
    assert len(states) == 8

def test_bitwise_microstates():
    states = list(generate_microstates_bitwise(3))
    assert len(states) == 8

def test_optimized_microstates():
    total, t, mem = measure_microstates_optimized(3)
    assert total == 8