"""
Main entry point for Statistical Physics Lab 1: Microstates Execution & Benchmark.
"""
from src.microstates import (
    generate_microstates_baseline,
    generate_microstates_bitwise,
    measure_microstates_optimized,
)

def run_benchmarks(n_values=(10, 14, 18, 22, 26)):
    print("=" * 72)
    print("        MICROSTATE GENERATION BENCHMARK (METHODS 1, 2 & 3)")
    print("=" * 72)
    print(f"{'N':<4} | {'2^N Microstates':<16} | {'Method':<20} | {'Time (s)':<12} | {'RAM (MiB)':<10}")
    print("-" * 72)

    methods = [
        ("Method 1 (Itertools)", generate_microstates_baseline),
        ("Method 2 (Bitwise Gen)", generate_microstates_bitwise),
        ("Method 3 (Optimized)", measure_microstates_optimized),
    ]

    for N in n_values:
        for name, func in methods:
            count, exec_time, ram_mb = func(N)
            print(f"{N:<4} | {count:<16} | {name:<20} | {exec_time:<12.6f} | {ram_mb:<10.4f}")
        print("-" * 72)

if __name__ == "__main__":
    run_benchmarks()