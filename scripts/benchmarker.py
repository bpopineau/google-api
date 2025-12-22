"""
Simple benchmarking harness for functions that are hard to profile directly via CLI.
Usage: python scripts/benchmarker.py
"""

import cProfile
import pstats
import timeit

# from mygooglib import get_clients


def target_function():
    # REPLACE THIS with the function you want to optimize
    # clients = get_clients()
    # example: clients.drive.list_files()
    pass


def benchmark():
    print("Running Benchmark...")

    # 1. Wall clock time
    start = timeit.default_timer()
    target_function()
    end = timeit.default_timer()
    print(f"Total Execution Time: {end - start:.4f}s")

    # 2. Detailed Profile
    print("\nGenerating Profile...")
    profiler = cProfile.Profile()
    profiler.enable()
    target_function()
    profiler.disable()

    stats = pstats.Stats(profiler).sort_stats("cumulative")
    stats.print_stats(10)


if __name__ == "__main__":
    benchmark()

