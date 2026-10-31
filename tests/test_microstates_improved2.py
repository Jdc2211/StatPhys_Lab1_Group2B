import time
from src.microstates_improved2 import measure_microstates

print("N  | Total States (2^N)   | Time (s)   | RAM (MB)")
print("-" * 52)

for N in range(20, 35):
    count, elapsed, peak_ram = measure_microstates(N)
    print(f"{N:2d} | {count:18,d} | {elapsed:8.4f}s | {peak_ram:8.4f}")
    
    # Stop if a single N takes longer than 5 minutes (300 seconds)
    if elapsed > 300:
        print("\nReached 5-minute limit!")
        break