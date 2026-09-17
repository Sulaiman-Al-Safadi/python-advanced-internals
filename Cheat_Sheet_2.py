"""
===============================================================================
                       SESSION 2: CHEAT_SHEET_2.py
===============================================================================
A quick-reference study sheet covering Python's standard library data structures,
combinatorics, heap queues, double-ended queues, and personal learning traps.

-------------------------------------------------------------------------------
TABLE OF CONTENTS
-------------------------------------------------------------------------------
1. itertools.combinations & itertools.permutations
2. heapq (Priority Queue & K-Smallest/Largest)
3. collections.deque (Double-Ended Queue)
===============================================================================
"""

# =============================================================================
# 1. itertools.combinations & itertools.permutations
# =============================================================================
# SIGNATURE:
#   combinations(iterable, r)
#     ├── iterable: Sequence/list to generate elements from.
#     └── r: Integer specifying the size of each subgroup (REQUIRED).
#
#   permutations(iterable, r=None)
#     ├── iterable: Sequence/list to generate elements from.
#     └── r (optional): Size of subgroups. If None, defaults to full length.
#
# PURPOSE:
#   Generates mathematical combinations and permutations without nested loops.
#   - `combinations`: Order DOES NOT matter -> ('A', 'B') is same as ('B', 'A').
#   - `permutations`: Order DOES matter -> ('A', 'B') is different from ('B', 'A').
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Forgetting the `r` parameter in combinations: `combinations(items)` 
#      - Throws TypeError: combinations() takes exactly 2 arguments (1 given).
#   ⚠️ Memory overhead: Passing massive lists generates millions of tuples. 
#      Iterate over them lazily rather than wrapping immediately with `list()`.
#
# COMPLEXITY:
#   Time: O(N! / (r! * (N-r)!)) for combinations | O(N! / (N-r)!)` for permutations.
#   Space: O(1) lazy iteration footprint.

from itertools import combinations, permutations

print("=== 1. itertools.combinations & permutations ===")

# EXAMPLE 1: combinations (Matchmaking / Unordered pairs)
# Goal: Find all unique 2-player match combinations
teams = ["Ahmad", "Sara", "Omar"]
matches = list(combinations(teams, 2))

print("Example 1 (Combinations - Order does not matter):")
print(matches)
# Output: [('Ahmad', 'Sara'), ('Ahmad', 'Omar'), ('Sara', 'Omar')]


# EXAMPLE 2: permutations (Rankings / Ordered placements)
# Goal: Find all 1st and 2nd place podium permutations
runners = ["Ahmad", "Sara", "Omar"]
podium = list(permutations(runners, 2))

print("\nExample 2 (Permutations - Order matters):")
print(podium)
# Output: [('Ahmad', 'Sara'), ('Ahmad', 'Omar'), ('Sara', 'Ahmad'), 
#          ('Sara', 'Omar'), ('Omar', 'Ahmad'), ('Omar', 'Sara')]


# =============================================================================
# 2. heapq (Priority Queue / K-Selection)
# =============================================================================
# SIGNATURE:
#   heapq.heapify(iterable)
#     └── iterable: Converts list in-place into a heap (min element at index 0).
#
#   heapq.nsmallest(n, iterable, key=None)
#   heapq.nlargest(n, iterable, key=None)
#     ├── n: Number of elements to extract (e.g., top 3 or bottom 2).
#     ├── iterable: Input list or sequence.
#     └── key (optional): Lambda function to extract comparison criteria.
#
# PURPOSE:
#   Fast retrieval of smallest/largest elements without sorting the entire dataset.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Assuming `heapify()` fully sorts a list: `heapq.heapify(ages); print(ages)`
#      - Only guarantees the smallest item is at `[0]`; rest is tree-structured.
#   ❌ Printing `.sort()` result: `print(youngest.sort())`
#      - Returns `None` because `.sort()` modifies lists in-place.
#   ✓ CORRECT: `heapq.nsmallest()` returns a NEW sorted list directly: `print(youngest)`.
#
# COMPLEXITY:
#   Time: O(N log k) for nsmallest/nlargest vs O(N log N) for full list sort.
#   Space: O(k) memory footprint for extracted values.

import heapq

print("\n=== 2. heapq ===")

ages = [22, 45, 19, 33, 28, 50, 26]

# EXAMPLE 1: Extracting smallest/largest values directly
# Goal: Get 3 youngest applicant ages sorted automatically
youngest_3 = heapq.nsmallest(3, ages)
print("Example 1 (nsmallest 3 ages):")
print(youngest_3)
# Output: [19, 22, 26]


# EXAMPLE 2: Extracting items from dictionary lists using `key`
# Goal: Get the 2 cheapest products
products = [
    {"name": "Laptop", "price": 1000},
    {"name": "Mouse", "price": 25},
    {"name": "Monitor", "price": 300},
    {"name": "Keyboard", "price": 75}
]

cheapest_2 = heapq.nsmallest(2, products, key=lambda x: x["price"])
print("\nExample 2 (Cheapest 2 products):")
print(cheapest_2)
# Output: [{'name': 'Mouse', 'price': 25}, {'name': 'Keyboard', 'price': 75}]


# =============================================================================
# 3. collections.deque (Double-Ended Queue)
# =============================================================================
# SIGNATURE:
#   deque([iterable[, maxlen]])
#     ├── iterable (optional): Initial elements to fill the deque.
#     └── maxlen (optional): Max capacity. When full, adding new items automatically
#                            discards old items from the opposite end.
#
# PURPOSE:
#   Fast O(1) appends and pops from both left and right sides.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Performance Trap: Using `list.pop(0)` on standard lists forces O(N) memory shifts.
#   ✓ CORRECT: Use `deque.popleft()` for O(1) performance.
#   ⚠️ Slicing limitations: Deque does NOT support slicing (e.g., `dq[1:3]`) efficiently.
#
# COMPLEXITY:
#   Time: O(1) for append/appendleft and pop/popleft operations.
#   Space: O(N) where N is current element count (bounded by maxlen if set).

from collections import deque

print("\n=== 3. collections.deque ===")

# EXAMPLE 1: Double-ended operations (appendleft, popleft)
# Goal: Manage incoming server request pipeline
requests = deque(["Req_1", "Req_2", "Req_3"])

# Add high-priority request to the front (left)
requests.appendleft("Req_0")
print("Example 1 (Queue after appendleft):")
print(requests)
# Output: deque(['Req_0', 'Req_1', 'Req_2', 'Req_3'])

# Process/remove first item from left
first_req = requests.popleft()
print(f"Processed request: {first_req}")
print("Remaining queue:", list(requests))
# Output: Remaining queue: ['Req_1', 'Req_2', 'Req_3']


# EXAMPLE 2: Fixed-size circular buffer using `maxlen`
# Goal: Maintain recent action history (max 3 actions)
recent_actions = deque(maxlen=3)
recent_actions.append("Action_1")
recent_actions.append("Action_2")
recent_actions.append("Action_3")
recent_actions.append("Action_4")  # Pushes out "Action_1" automatically

print("\nExample 2 (Fixed capacity maxlen=3 history):")
print(list(recent_actions))
# Output: ['Action_2', 'Action_3', 'Action_4']


# =============================================================================
# END OF CHEAT_SHEET_2.py
# =============================================================================