import itertools
import time

def generate_microstates(N):
    # Record the start time
    start_time = time.time()
    
    # Create an iterator for all 2^N microstates (e.g., ('H', 'H', 'T', ...))
    microstates = itertools.product(['H', 'T'], repeat=N)
    
    # Iterate through all microstates and count them
    count = sum(1 for _ in microstates)
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Print results
    print(f"N = {N}")
    print(f"Total microstates (2^{N}): {count:,}")
    print(f"Execution time: {elapsed_time:.4f} seconds")

