import cProfile
import io
import os
import pstats
import sys
import time

# Ensure the scripts directory is in the path
sys.path.append(os.path.dirname(__file__))

import smoke_test


def profile_all_read_only():
    """Run `smoke_test.py all` without write operations."""
    print("Starting profiling: smoke_test.py all (read-only)...")
    start_time = time.perf_counter()

    # We pass 'all' but NOT '--write'
    smoke_test.main(["all"])

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"\nTotal execution time: {duration:.4f} seconds")
    return duration


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()

    duration = profile_all_read_only()

    pr.disable()
    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20)  # Top 20 functions

    with open("profiling_results.txt", "w") as f:
        f.write(f"Total duration: {duration:.4f}s\n")
        f.write(s.getvalue())

    print("\nProfiling results saved to profiling_results.txt")
    print(s.getvalue())

