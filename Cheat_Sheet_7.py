"""
===============================================================================
                        SESSION 7: CHEAT_SHEET_7.py
===============================================================================
A quick-reference study sheet covering memory optimization with __slots__, 
dynamic attribute interception via __getattr__ & __setattr__, and asynchronous 
stream processing using Async Generators with asyncio.

-------------------------------------------------------------------------------
TABLE OF FUNCTIONS & REASONING SUMMARY
-------------------------------------------------------------------------------
1. Low-Level Memory Optimization:
   - __slots__                  : Suppresses default __dict__ creation, reducing RAM overhead by ~50-70%.

2. Dynamic Attribute Interception:
   - __getattr__(self, name)    : Fallback handler executed ONLY when an attribute is missing.
   - __setattr__(self, name, val): Intercepts ALL attribute mutations to enforce rules or immutability.

3. Asynchronous Data Streams:
   - async def + yield          : Creates an Async Generator emitting data non-blockingly over time.
   - async for                  : Consumes items emitted by an asynchronous iterable inside an event loop.

===============================================================================
"""

# =============================================================================
# 1. Memory Optimization & Immutability (__slots__ & __setattr__)
# =============================================================================
# PURPOSE:
#   Optimizes instance memory layout by removing __dict__ and enforces strict 
#   attribute mutation rules (Immutability pattern).
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Checking `if name in self.__slots__` inside `__setattr__` during instance init:
#      - Raises AttributeError on the very first assignment in `__init__` before setting the value.
#   ✅ Use `if hasattr(self, name): raise AttributeError(...)` to allow initialization 
#      while preventing subsequent modifications.
#
# COMPLEXITY: Memory O(1) constant slots allocation | Access O(1) fast array indexing

print("=== 1. Memory Optimization & Immutability (__slots__ & __setattr__) ===")

class ImmutablePoint:
    __slots__ = ("_x", "_y", "_z")

    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z

    def __setattr__(self, name: str, value: float) -> None:
        """Intercepts assignments to prevent modifying existing properties."""
        if hasattr(self, name):
            raise AttributeError(f"Cannot modify immutable attribute '{name}'.")
        super().__setattr__(name, value)

point = ImmutablePoint(1.0, 2.0, 3.0)
print(f"Coordinates: x={point._x}, y={point._y}, z={point._z}")

# Attempting mutation will raise AttributeError:
# point._x = 10.0


# =============================================================================
# 2. Dynamic Attribute Fallbacks (__getattr__)
# =============================================================================
# PURPOSE:
#   Provides dynamic fallback behaviors or dynamic property proxying when an 
#   requested attribute does not exist on the object instance.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Confusing `__getattr__` with `__getattribute__`:
#      - `__getattribute__` runs on EVERY property access, whereas `__getattr__` 
#        runs ONLY when the attribute search fails.
#
# COMPLEXITY: Time O(1) missing lookup delegation | Space O(1)

print("\n=== 2. Dynamic Attribute Fallbacks (__getattr__) ===")

class DynamicConfigProxy:
    def __init__(self):
        self.environment = "Production"
        self._overrides = {"database_url": "db.internal.net", "port": 5432}

    def __getattr__(self, name: str):
        """Executed only if 'name' is not found in instance dict/slots."""
        if name in self._overrides:
            return self._overrides[name]
        raise AttributeError(f"Configuration parameter '{name}' is undefined.")

config = DynamicConfigProxy()
print(f"Environment  : {config.environment}")     # Normal lookup
print(f"Database URL : {config.database_url}")    # Dynamically intercepted via __getattr__
print(f"Port         : {config.port}")            # Dynamically intercepted via __getattr__


# =============================================================================
# 3. Asynchronous Generators (async def + yield & async for)
# =============================================================================
# PURPOSE:
#   Streams real-time data chunks asynchronously without blocking the event loop 
#   or buffering large payloads entirely in memory.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Consuming an async generator using standard `for` loop:
#      - Raises `TypeError: 'async generator' object is not iterable`. Must use `async for`.
#
# COMPLEXITY: Time O(N) stream yields with IO pauses | Space O(1) continuous streaming

import asyncio

print("\n=== 3. Asynchronous Generators (async def + yield & async for) ===")

async def async_data_stream(total_chunks: int):
    """Yields data chunks asynchronously with simulated network delays."""
    for chunk_id in range(1, total_chunks + 1):
        await asyncio.sleep(0.05)  # Non-blocking async delay
        yield f"Payload-Chunk-{chunk_id}"

async def main():
    print("Consuming async stream...")
    async for chunk in async_data_stream(3):
        print(f"Received -> {chunk}")

# Execute event loop
asyncio.run(main())


# =============================================================================
# END OF CHEAT_SHEET_7.py
# =============================================================================