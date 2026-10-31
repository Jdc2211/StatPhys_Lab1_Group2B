import time
import tracemalloc

def generate_microstates(N):
    """
    Generator yielding binary integer microstates from 0 to (2^N - 1).
    Uses bitwise shift 1 << N to calculate total state bound.
    """
    total_states = 1 << N  # Bitwise calculation of 2^N
    for state in range(total_states):
        yield state  # Yields state as integer bit pattern

def measure_microstates(N):
    """
    Measures microstate generation speed and RAM usage.
    """
    # 1. Start memory tracking and timer
    tracemalloc.start()
    start_time = time.perf_counter()  # High-precision timer
    
    # 2. Fast C-level consumption of generator (avoids Python frame overhead)
    count = sum(1 for _ in generate_microstates(N))
    
    # 3. Stop timer and memory tracking
    elapsed_time = time.perf_counter() - start_time
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    peak_ram_mb = peak_bytes / (1024 * 1024)
    
    return count, elapsed_time, peak_ram_mb