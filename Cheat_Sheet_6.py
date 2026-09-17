"""
===============================================================================
                        SESSION 6: CHEAT_SHEET_6.py
===============================================================================
A quick-reference study sheet covering automatic function memoization with 
functools.lru_cache, custom context managers using contextlib.contextmanager, 
and sub-generator delegation via yield from.

-------------------------------------------------------------------------------
TABLE OF FUNCTIONS & REASONING SUMMARY
-------------------------------------------------------------------------------
1. Function Memoization:
   - @lru_cache(maxsize=N)      : Caches function outputs to skip redundant computations (O(1) time).
   - func.cache_info()          : Retrieves cache execution stats (hits, misses, maxsize).

2. Context Management:
   - @contextmanager            : Converts a generator function into a custom 'with' block manager.
   - yield                      : Suspends execution between setup and teardown logic.

3. Generator Delegation:
   - yield from iterable        : Delegates iteration directly to a sub-generator/iterable.

===============================================================================
"""

# =============================================================================
# 1. Automatic Memoization (@lru_cache)
# =============================================================================
# PURPOSE:
#   Improves performance of pure functions by caching input/output mappings,
#   reducing time complexity to O(1) for repeated positional or named arguments.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Passing mutable/unhashable argument types (e.g., lists or dicts):
#      - Raises `TypeError: unhashable type`. Inputs must be immutable (int, str, tuple).
#
# COMPLEXITY: Time O(1) cached lookup | Space O(N) cache entries

import time
from functools import lru_cache

print("=== 1. Automatic Memoization (@lru_cache) ===")

@lru_cache(maxsize=32)
def heavy_computation(number: int) -> int:
    """Simulates a heavy calculation using memoization."""
    time.sleep(0.1)  # Simulated overhead
    return number * 100

# First Call (Miss - executes computation)
start = time.perf_counter()
res1 = heavy_computation(5)
t1 = time.perf_counter() - start

# Second Call (Hit - retrieved instantly from cache)
start = time.perf_counter()
res2 = heavy_computation(5)
t2 = time.perf_counter() - start

print(f"First Execution Time  : {t1:.6f}s | Result: {res1}")
print(f"Second Execution Time : {t2:.6f}s | Result: {res2}")
print(f"Cache Statistics      : {heavy_computation.cache_info()}")


# =============================================================================
# 2. Custom Context Managers (@contextmanager)
# =============================================================================
# PURPOSE:
#   Simplifies setup/teardown mechanics for resources using a clean 'with' block,
#   ensuring cleanup code runs safely via try/finally blocks.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Omitting the try/finally block:
#      - If an exception occurs inside the 'with' scope, teardown code after yield is skipped.
#
# COMPLEXITY: Time O(1) context frame overhead | Space O(1)

from contextlib import contextmanager

print("\n=== 2. Custom Context Managers (@contextmanager) ===")

@contextmanager
def execution_timer(task_name: str):
    """Measures total execution time of an enclosed block of code."""
    print(f"--- Starting task: {task_name} ---")
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        print(f"--- Finished task: {task_name} in {elapsed:.6f} seconds ---")

# Usage with a block of code
with execution_timer("Processing Elements"):
    total = sum(i * i for i in range(500_000))


# =============================================================================
# 3. Sub-Generator Delegation (yield from)
# =============================================================================
# PURPOSE:
#   Flattens data streams and delegates generator iteration to nested iterables 
#   cleanly without requiring manual inner 'for' loops.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Using `yield` instead of `yield from` on an iterable:
#      - Yielding an iterable directly emits the entire container object rather than items.
#
# COMPLEXITY: Time O(N) sequential stream yield | Space O(1) constant RAM

print("\n=== 3. Sub-Generator Delegation (yield from) ===")

def combine_skills():
    """Delegates iteration over multiple skill containers."""
    core_skills = ["Python", "Git"]
    advanced_skills = ["Decorators", "Generators"]
    
    yield from core_skills
    yield from advanced_skills

print("Aggregated Skills:")
for skill in combine_skills():
    print(f" - {skill}")


# =============================================================================
# END OF CHEAT_SHEET_6.py
# =============================================================================