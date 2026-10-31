import time
import tracemalloc

def measure_microstates(N):
    """
    Measures microstate counting speed using binary shift bounds (1 << N)
    and direct C-level iteration, bypassing generator frame overhead.
    """
    total_states = 1 << N  # Binary bitwise shift calculation of 2^N
    
    # 1. Start memory tracking and high-precision timer
    tracemalloc.start()
    start_time = time.perf_counter()
    
    # 2. Direct C-level loop (bypasses yield frame context switching)
    count = sum(1 for _ in range(total_states))
    
    # 3. Stop timer and memory tracking
    elapsed_time = time.perf_counter() - start_time
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    peak_ram_mb = peak_bytes / (1024 * 1024)
    
    return count, elapsed_time, peak_ram_mb