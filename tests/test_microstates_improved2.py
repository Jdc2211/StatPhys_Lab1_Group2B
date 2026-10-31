from src.microstates_improved2 import measure_microstates

print("N  | Total States (2^N) | Time (s)")
print("-" * 35)

for N in range(20, 35):
    count, elapsed = measure_microstates(N)
    print(f"{N:2d} | {count:18,d} | {elapsed:8.2f}s")
    
    # Stop if a single N takes longer than 5 minutes (300 seconds)
    if elapsed > 300:
        print("\nReached 5-minute limit!")
        break