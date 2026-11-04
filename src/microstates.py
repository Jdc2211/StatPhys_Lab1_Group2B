import itertools
import time
import tracemalloc

# Method 1: Baseline (itertools.product)
def generate_microstates_baseline(N):
    tracemalloc.start()
    start_time = time.perf_counter()
    # Ensure count is an integer count of states
    microstates = list(itertools.product(['H', 'T'], repeat=N))
    count = len(microstates)
    elapsed_time = time.perf_counter() - start_time
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return count, elapsed_time, peak_bytes / (1024 * 1024)

# Method 2: Bitwise generator
def generate_microstates_bitwise(N):
    tracemalloc.start()
    start_time = time.perf_counter()
    count = sum(1 for _ in range(1 << N))
    elapsed_time = time.perf_counter() - start_time
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return count, elapsed_time, peak_bytes / (1024 * 1024)

# Method 3: Direct range sum measurement
def measure_microstates_optimized(N):
    total_states = 1 << N
    tracemalloc.start()
    start_time = time.perf_counter()
    count = sum(1 for _ in range(total_states))
    elapsed_time = time.perf_counter() - start_time
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return count, elapsed_time, peak_bytes / (1024 * 1024)

# Default fallback entry point
def generate_microstates(N):
    return generate_microstates_baseline(N)