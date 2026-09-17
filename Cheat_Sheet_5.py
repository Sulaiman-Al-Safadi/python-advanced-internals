"""
===============================================================================
                        SESSION 5: CHEAT_SHEET_5.py
===============================================================================
A quick-reference study sheet covering advanced function signature bounds
(*args, **kwargs, positional-only '/', keyword-only '*'), memory-efficient 
generators & iterators (yield vs list), and custom performance profiler decorators.

-------------------------------------------------------------------------------
TABLE OF FUNCTIONS & REASONING SUMMARY
-------------------------------------------------------------------------------
1. Signature Enforcement & Flexible Arguments:
   - *args                     : Packs un-named positional arguments into a tuple.
   - **kwargs                  : Packs named keyword arguments into a dictionary.
   - / (Positional-Only Flag)  : Forces arguments before '/' to be passed positionally.
   - * (Keyword-Only Flag)     : Forces arguments after '*' to be passed as named keywords.

2. Iterators & Generators:
   - yield                     : Pauses function execution and streams items lazily O(1) RAM.
   - next(gen)                 : Manually retrieves the next sequential item from a generator stream.
   - (expr for i in iterable)  : Generator expression allocating zero bulk list memory.

3. Decorators & Performance Profiling:
   - @wraps(func)              : Preserves wrapped function identity, docstrings, and metadata.
   - time.perf_counter()       : High-resolution timer for accurate code benchmarking.

===============================================================================
"""

# =============================================================================
# 1. Signature Enforcement (*args, **kwargs, /, *)
# =============================================================================
# PURPOSE:
#   Enforces strict API calling conventions for functions, preventing subtle bugs,
#   improving execution speed, and enabling flexible positional/keyword arguments.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Passing positional args by name before `/`:
#      - Passing `first_name="Sulaiman"` when signature uses `(first_name, /)` 
#        raises `TypeError: got positional-only arguments passed as keyword arguments`.
#   ❌ Forgetting that `*args` packs into a Tuple, whereas `**kwargs` packs into a Dict.
#
# COMPLEXITY: Time O(1) invocation | Space O(N) packed argument tuple/dict

print("=== 1. Signature Enforcement & Flexible Arguments ===")

# EXAMPLE 1: Combining Positional-Only (/), *args, and Keyword-Only (*)
def format_user_data(first_name, last_name, /, *skills, is_active=True):
    """
    first_name, last_name : MUST be positional-only (before /)
    *skills               : Packs extra positional skills into a Tuple
    is_active             : MUST be keyword-only (after *)
    """
    full_name = f"{first_name} {last_name}"
    skills_list = list(skills)
    return {
        "full_name": full_name,
        "skills": skills_list,
        "is_active": is_active
    }

# Correct Invocation:
user_record = format_user_data("Sulaiman", "Al Safadi", "Python", "GitHub", is_active=True)

print("Example 1 (Strict Signature Output):")
print(f"Full Name   : {user_record['full_name']}")
print(f"Skills List : {user_record['skills']}")
print(f"Active      : {user_record['is_active']}")


# =============================================================================
# 2. Iterators & Generators (Memory Optimization)
# =============================================================================
# PURPOSE:
#   Processes continuous data streams or massive files lazily using `yield`, 
#   maintaining an O(1) constant memory overhead instead of loading lists to RAM.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Assuming Generators can be reused after exhaustion:
#      - Generators are single-pass streams! Once iterated, they raise StopIteration.
#   ❌ Attempting to print a generator directly without iterating:
#      - Printing a generator outputs `<generator object ...>` instead of values.
#
# COMPLEXITY: Generator Time O(N) stream processing | Space O(1) Constant RAM usage

print("\n=== 2. Iterators & Generators ===")

# EXAMPLE 1: File Log Simulator Generator Function
def read_large_file_simulator(total_lines: int):
    """Generates synthetic log lines on-demand using yield."""
    for line_num in range(1, total_lines + 1):
        yield f"Log Line {line_num}"

# Instantiating generator object
log_stream = read_large_file_simulator(5)

print("Example 1 (Lazy Generation via yield):")
print("First Fetched Item  :", next(log_stream))
print("Second Fetched Item :", next(log_stream))

print("\nRemaining Items via Loop:")
for line in log_stream:
    print(" ", line)

# EXAMPLE 2: Generator Expression (Single-line Lazy Iterator)
gen_expr = (f"Stream Item {i}" for i in range(1, 4))
print("\nExample 2 (Generator Expression):")
print(f"Direct Next Output : {next(gen_expr)}")


# =============================================================================
# 3. Decorators & Execution Profiling
# =============================================================================
# PURPOSE:
#   Wraps functions to add cross-cutting behavior (like execution timing)
#   without modifying the original function's code body.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Omitting `@wraps(func)` inside custom wrappers:
#      - Strips original function metadata, setting `func.__name__` to 'wrapper'.
#
# COMPLEXITY: Time O(1) wrapper overhead + func execution time | Space O(1)

import time
from functools import wraps

print("\n=== 3. Decorators & Execution Profiling ===")

# EXAMPLE 1: Custom Execution Profiler Decorator
def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time = time.perf_counter() - start_time
        print(f"[PROFILER] '{func.__name__}' executed in {elapsed_time:.6f} seconds.")
        return result
    return wrapper

@timer_decorator
def process_data_pipeline(limit: int):
    return sum(i * i for i in range(limit))

print("Example 1 (Custom Timer Decorator Output):")
total_result = process_data_pipeline(1_000_000)


# =============================================================================
# END OF CHEAT_SHEET_5.py
# =============================================================================