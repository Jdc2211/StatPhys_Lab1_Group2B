import pytest
from src.microstates_improved2 import measure_microstates


# ------------------------------------------------------------------
# Register custom marker to prevent PytestUnknownMarkWarning
# ------------------------------------------------------------------
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as a slow benchmark loop")


# ------------------------------------------------------------------
# 1. Fast Unit Tests (Automated CI / Regular `pytest` runs)
# ------------------------------------------------------------------

@pytest.mark.parametrize("N, expected_count", [
    (0, 1),       # 2^0 = 1
    (1, 2),       # 2^1 = 2
    (2, 4),       # 2^2 = 4
    (5, 32),      # 2^5 = 32
    (10, 1024),   # 2^10 = 1024
])
def test_measure_microstates_count(N, expected_count):
    """Verify state count calculation using binary bitwise shift (1 << N)."""
    count, elapsed_time, peak_ram = measure_microstates(N)

    # Assert accurate state counts
    assert count == expected_count
    assert count == 2**N

    # Sanity checks for returned performance metadata
    assert elapsed_time >= 0.0
    assert peak_ram >= 0.0


# ------------------------------------------------------------------
# 2. Performance / Benchmark Test (Skipped by default unless requested)
# ------------------------------------------------------------------

@pytest.mark.slow
def test_microstates_performance_benchmark():
    """
    Benchmarking loop for N = 20..25 using direct C-level range iteration.
    Run explicitly with: pytest -m slow
    """
    max_time_threshold_seconds = 300.0

    for N in range(20, 26):
        count, elapsed, ram = measure_microstates(N)

        assert count == 2**N
        assert elapsed <= max_time_threshold_seconds, (
            f"Execution time for N={N} exceeded {max_time_threshold_seconds}s threshold!"
        )