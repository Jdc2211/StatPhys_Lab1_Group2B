import time
from src.microstates import generate_microstates

print("Starting microstate benchmarking from N = 20...\n")
print(f"{'N':<3} | {'Total States (2^N)':<20} | {'Time (s)':<10} | {'RAM (MB)':<10}")
print("-" * 52)

for N in range(20, 32):
    # Call the imported function
    count, elapsed_time, peak_ram = generate_microstates(N)

    print(f"{N:<3} | {count:<20,d} | {elapsed_time:<10.4f} | {peak_ram:<10.4f}")

    # Stop if execution time exceeds 300 seconds (5 minutes)
    if elapsed_time > 300:
        print("\n[!] Time limit threshold of 300s exceeded. Stopping.")
        break