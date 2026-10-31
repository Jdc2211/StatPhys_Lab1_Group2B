import itertools
import time
import tracemalloc

def generate_microstates(N):
    # Start tracking memory and record start time
    tracemalloc.start()
    start_time = time.time()
    
    # Create an iterator for all 2^N microstates (e.g., ('H', 'H', 'T', ...))
    microstates = itertools.product(['H', 'T'], repeat=N)
    
    # Iterate through all microstates and count them
    count = sum(1 for _ in microstates)
    
    # Calculate elapsed time and peak RAM usage
    elapsed_time = time.time() - start_time
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_ram_mb = peak_bytes / (1024 * 1024)
    
    # Return metrics for structured table printing in the runner script
    return count, elapsed_time, peak_ram_mb