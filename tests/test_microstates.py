import pytest
from src.microstates import generate_microstates

# ------------------------------------------------------------------
# 1. Fast Unit Tests (Automated CI / Regular `pytest` runs)
# ------------------------------------------------------------------

@pytest.mark.parametrize("N, expected_count", [
    (0, 1),      # 2^0 = 1 state: empty tuple ()
    (1, 2),      # 2^1 = 2 states: ('H',), ('T',)
    (2, 4),      # 2^2 = 4 states: ('H','H'), ('H','T'), ...
    (5, 32),     # 2^5 = 32 states
    (10, 1024),  # 2^10 = 1024 states
])
def test_generate_microstates_count(N, expected_count):
    """Verify that generate_microstates calculates correct microstate count (2^N)."""
    count, elapsed_time, peak_ram = generate_microstates(N)

    # Core functional assertions
    assert count == expected_count
    assert count == 2**N

    # Sanity checks for metadata return values
    assert elapsed_time >= 0.0
    assert peak_ram >= 0.0


# ------------------------------------------------------------------
# 2. Performance / Benchmark Test (Skipped by default unless requested)
# ------------------------------------------------------------------

@pytest.mark.slow
def test_generate_microstates_performance_benchmark():
    """
    Benchmarking test for N = 20..31.
    Run explicitly with: pytest -m slow
    """
    max_time_threshold_seconds = 10.0

    for N in range(20, 26):
        count, elapsed_time, peak_ram = generate_microstates(N)

        # Assert correct count calculation even under scale
        assert count == 2**N

        # Ensure performance threshold isn't breached
        assert elapsed_time <= max_time_threshold_seconds, (
            f"Execution time for N={N} exceeded {max_time_threshold_seconds}s threshold!"
        )