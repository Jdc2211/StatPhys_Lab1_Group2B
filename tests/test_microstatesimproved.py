import pytest
from src.microstates_improved import generate_microstates, measure_microstates


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
def test_generate_microstates_generator(N, expected_count):
    """Verify that the generator produces exactly 2^N microstates."""
    states = list(generate_microstates(N))
    assert len(states) == expected_count
    assert states == list(range(expected_count))


@pytest.mark.parametrize("N", [0, 1, 5, 10])
def test_measure_microstates_metrics(N):
    """Verify state count, execution time, and memory tracking metrics."""
    count, elapsed_time, peak_ram = measure_microstates(N)

    assert count == 2**N
    assert elapsed_time >= 0.0
    assert peak_ram >= 0.0


# ------------------------------------------------------------------
# 2. Performance / Benchmark Test (Skipped by default unless requested)
# ------------------------------------------------------------------

@pytest.mark.slow
def test_microstates_performance_benchmark():
    """
    Benchmarking loop for N = 20..25.
    Run explicitly with: pytest -m slow
    """
    max_time_threshold_seconds = 300.0

    for N in range(20, 26):
        count, elapsed, ram = measure_microstates(N)
        assert count == 2**N
        assert elapsed <= max_time_threshold_seconds, (
            f"Execution time for N={N} exceeded {max_time_threshold_seconds}s threshold!"
        )