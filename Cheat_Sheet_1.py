"""
===============================================================================
                       SESSION 1: CHEAT_SHEET_1.py
===============================================================================
A quick-reference study sheet covering Python's standard library data structures,
built-in helper functions, performance profiling, and personal learning traps.

-------------------------------------------------------------------------------
TABLE OF CONTENTS
-------------------------------------------------------------------------------
1. collections.defaultdict
2. collections.Counter
3. itertools.zip_longest & Built-in zip()
4. Built-in any() & all()
5. itertools.groupby
6. functools.lru_cache (Memoization)
7. itertools.chain
8. str.maketrans & str.translate
===============================================================================
"""

# =============================================================================
# 1. collections.defaultdict
# =============================================================================
# SIGNATURE:
#   defaultdict(default_factory)
#     └── default_factory: A function or class type (e.g., list, int, set) that 
#                          provides the initial value for a missing key.
#
# PURPOSE:
#   Avoids KeyError by automatically initializing non-existent keys.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Loop syntax error: `for word[0] in words:` (Invalid Python)
#   ❌ Method mismatch: Using `.add()` with `defaultdict(list)` causes AttributeError.
#      - `defaultdict(list)` requires `.append()`
#      - `defaultdict(set)` requires `.add()`
#
# COMPLEXITY: Time O(1) avg lookup/insertion | Space O(N)

from collections import defaultdict

print("=== 1. defaultdict ===")

# EXAMPLE 1: Grouping items using defaultdict(list)
# Goal: Group words by their first letter
words = ["apple", "banana", "avocado", "blue", "cherry"]
grouped_by_first_letter = defaultdict(list)

for word in words:
    grouped_by_first_letter[word[0]].append(word)

print("Example 1 (Grouping with list):")
print(dict(grouped_by_first_letter))
# Output: {'a': ['apple', 'avocado'], 'b': ['banana', 'blue'], 'c': ['cherry']}


# EXAMPLE 2: Counting occurrences using defaultdict(int)
# Goal: Count user actions in system logs without prior key checks
user_logs = [
    ("Ahmad", "login"),
    ("Sara", "login"),
    ("Ahmad", "view_page"),
    ("Sara", "logout"),
    ("Ahmad", "logout"),
]
action_counts = defaultdict(int)

for user, action in user_logs:
    action_counts[user] += 1

print("\nExample 2 (Counting with int):")
print(dict(action_counts))
# Output: {'Ahmad': 3, 'Sara': 2}


# =============================================================================
# 2. collections.Counter
# =============================================================================
# SIGNATURE:
#   Counter([iterable_or_mapping])
#     └── iterable_or_mapping: Any list, string, tuple, or dict to count elements from.
#
#   Counter.most_common([k])
#     └── k (optional): Integer specifying top 'k' most frequent elements.
#                       Returns a list of tuples: [('item', count)].
#
# PURPOSE:
#   Fast frequency counting and tracking.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Calling `.most_common()` directly on a list: `search_tags.most_common(1)`
#      - Throws AttributeError: 'list' object has no attribute 'most_common'
#   ✓ CORRECT: `Counter(search_tags).most_common(1)`
#
# COMPLEXITY: Time O(N) build, O(N log k) most_common | Space O(U) unique items

from collections import Counter

print("\n=== 2. Counter ===")

# EXAMPLE 1: Basic counting & finding the top 1 item
# Goal: Count search tag frequency and find the most searched tag
search_tags = ["python", "django", "python", "css", "python", "django", "html"]
tag_counts = Counter(search_tags)
top_search_tag = tag_counts.most_common(1)

print("Example 1 (Most common 1 item):")
print(top_search_tag)
# Output: [('python', 3)]


# EXAMPLE 2: Accessing specific counts & top 2 items
print("\nExample 2 (Accessing counts & top 2):")
print(f"Count of 'django': {tag_counts['django']}") # Output: 2
print(f"Top 2 tags: {tag_counts.most_common(2)}")   # Output: [('python', 3), ('django', 2)]


# =============================================================================
# 3. itertools.zip_longest & Built-in zip()
# =============================================================================
# SIGNATURE:
#   zip(*iterables)
#     └── *iterables: Two or more lists/tuples to pair up side-by-side.
#
#   zip_longest(*iterables, fillvalue=None)
#     ├── *iterables: Two or more lists/tuples.
#     └── fillvalue: Placeholder value used when shorter iterables run out.
#
# PURPOSE:
#   Combine multiple iterables without losing elements from shorter lists.
#
# COMPLEXITY: Time O(N) | Space O(1) lazy evaluation

from itertools import zip_longest

print("\n=== 3. zip vs zip_longest ===")

names = ["Ahmad", "Sara", "Omar"]
scores = [90, 85]  # 'Omar' is missing a score

# EXAMPLE 1: Standard built-in zip() (Truncates data at shortest list)
zipped_standard = list(zip(names, scores))
print("Example 1 (Standard zip - ignores Omar):")
print(zipped_standard)
# Output: [('Ahmad', 90), ('Sara', 85)]


# EXAMPLE 2: zip_longest with default fillvalue
# Goal: Build a product catalog dictionary where missing price defaults to 0
products = ["Laptop", "Mouse", "Keyboard", "Monitor"]
prices = [1000, 25, 50]

product_catalog = dict(zip_longest(products, prices, fillvalue=0))
print("\nExample 2 (zip_longest with fillvalue=0):")
print(product_catalog)
# Output: {'Laptop': 1000, 'Mouse': 25, 'Keyboard': 50, 'Monitor': 0}


# =============================================================================
# 4. Built-in any() & all()
# =============================================================================
# SIGNATURE:
#   all(iterable) / any(iterable)
#     └── iterable: A sequence/generator yielding boolean expressions.
#
# PURPOSE:
#   - `all()` -> Returns True if ALL elements evaluate to True.
#   - `any()` -> Returns True if AT LEAST ONE element evaluates to True.
#
# COMPLEXITY: Time O(N) worst-case (Short-circuits!) | Space O(1)

print("\n=== 4. any() & all() ===")

task_scores = [85, 90, 78, 92, 60]

# EXAMPLE 1: Checking condition across all items with all()
all_passed = all(score >= 50 for score in task_scores)
print("Example 1 (all - Are all scores >= 50?):", all_passed)
# Output: True


# EXAMPLE 2: Checking for at least one match with any()
has_excellence = any(score > 90 for score in task_scores)
print("Example 2 (any - Is there any score > 90?):", has_excellence)
# Output: True


# =============================================================================
# 5. itertools.groupby
# =============================================================================
# SIGNATURE:
#   groupby(iterable, key=None)
#     ├── iterable: A dataset (MUST BE SORTED by the grouping field first).
#     └── key: A function (e.g., `lambda x: x["field"]`) extracting the criteria.
#
# PURPOSE:
#   Groups consecutive elements sharing the same key value.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ⚠️ CRITICAL: Must sort data by key before grouping, or duplicates won't merge!
#   ⚠️ Parameter `group` is a single-use generator -> convert with `list(group)`.
#
# COMPLEXITY: Time O(N) iteration | Space O(1) via generator

from itertools import groupby

print("\n=== 5. itertools.groupby ===")

# EXAMPLE 1: Grouping employee dictionaries by Role
employees = [
    {"name": "Ahmad", "role": "Admin"},
    {"name": "Sara", "role": "Admin"},
    {"name": "Omar", "role": "User"},
    {"name": "Lina", "role": "User"},
]

print("Example 1 (Grouping employees by role):")
for role, group in groupby(employees, key=lambda x: x["role"]):
    names = [emp["name"] for emp in group]
    print(f"{role} -> {names}")
# Output:
# Admin -> ['Ahmad', 'Sara']
# User -> ['Omar', 'Lina']


# EXAMPLE 2: Grouping transaction records by Status
transactions = [
    {"id": 1, "status": "approved"},
    {"id": 2, "status": "approved"},
    {"id": 3, "status": "pending"},
    {"id": 4, "status": "rejected"},
]

print("\nExample 2 (Grouping transactions by status):")
for status, group in groupby(transactions, key=lambda x: x["status"]):
    transaction_ids = [item["id"] for item in group]
    print(f"Status '{status}': {transaction_ids}")


# =============================================================================
# 6. functools.lru_cache (Memoization)
# =============================================================================
# SIGNATURE:
#   @lru_cache(maxsize=128, typed=False)
#     ├── maxsize: Max number of cached results in RAM (None = unlimited).
#     └── typed: If True, arguments of different types cached separately (e.g., 3 vs 3.0).
#
# PURPOSE:
#   Caches function outputs in memory to bypass redundant computational execution.
#
# PITFALLS & KEY QUESTIONS ASKED:
#   💡 `maxsize=128`: Retains up to 128 unique entries, dropping the oldest (LRU).
#   ⚠️ Unhashable Arguments: Passing mutable types (e.g., lists/dicts) throws TypeError.
#
# COMPLEXITY: Time O(1) on cache hit | Space O(K) bounded by maxsize

from functools import lru_cache

print("\n=== 6. functools.lru_cache ===")

# EXAMPLE 1: Tax calculation caching
@lru_cache(maxsize=128)
def calculate_tax(price, tax_rate):
    print(f"  [EXEC] Calculating tax for price={price}, rate={tax_rate}...")
    return price * (1 + tax_rate)

print("Example 1 (Tax Calculator execution):")
print("First call:", calculate_tax(100, 0.15))   # Executes logic & prints log
print("Second call:", calculate_tax(100, 0.15))  # Instant return from RAM!


# EXAMPLE 2: User profile retrieval simulation
@lru_cache(maxsize=500)
def get_user_profile(user_id):
    print(f"  [DB QUERY] Fetching data for user_id={user_id}...")
    return {"id": user_id, "status": "active"}

print("\nExample 2 (User Profile DB Query simulation):")
print(get_user_profile(101))
print(get_user_profile(101)) # Returns cached result directly


# =============================================================================
# 7. itertools.chain
# =============================================================================
# SIGNATURE:
#   chain(*iterables)
#     └── *iterables: Multiple sequences passed directly: `chain(list1, list2)`.
#
#   chain.from_iterable(iterable)
#     └── iterable: A single nested list containing iterables: `chain.from_iterable(nested)`.
#
# PURPOSE:
#   Sequentially iterates through multiple datasets without extra memory copies.
#
# COMPLEXITY: Time O(N) | Space O(1) memory footprint

from itertools import chain

print("\n=== 7. itertools.chain ===")

# EXAMPLE 1: Combining multiple separate lists with chain()
branch_1 = [101, 102]
branch_2 = [201, 202, 203]
branch_3 = [301]

all_orders = list(chain(branch_1, branch_2, branch_3))
print("Example 1 (Combining separate branch lists):")
print(all_orders)
# Output: [101, 102, 201, 202, 203, 301]


# EXAMPLE 2: Flattening a single nested list with chain.from_iterable()
nested_groups = [["Ahmad", "Sara"], ["Omar", "Lina"], ["Hasan"]]
flat_users = list(chain.from_iterable(nested_groups))
print("\nExample 2 (Flattening nested lists):")
print(flat_users)
# Output: ['Ahmad', 'Sara', 'Omar', 'Lina', 'Hasan']


# =============================================================================
# 8. str.maketrans & str.translate
# =============================================================================
# SIGNATURE:
#   str.maketrans(from_chars, to_chars, delete_chars)
#     ├── from_chars (str): Characters to be replaced.
#     ├── to_chars (str): Replacement characters corresponding to `from_chars`.
#     └── delete_chars (str): Characters to be completely deleted from the output.
#
#   string.translate(table)
#     └── table: Translation table generated by `str.maketrans()`.
#
# PURPOSE:
#   Fast character replacement and deletion executed natively in C.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Calling context error: `to_remove.translate(to_remove)`
#      - Called `.translate()` on the dict instead of the string target.
#
# COMPLEXITY: Time O(N) | Space O(N)

print("\n=== 8. str.maketrans & translate ===")

# EXAMPLE 1: Replacing characters (Vowels to numbers)
text = "hello world"
vowel_table = str.maketrans("aeiou", "12345")
print("Example 1 (Character replacement):")
print(text.translate(vowel_table))
# Output: h2ll4 w4rld


# EXAMPLE 2: Deleting specific characters (Cleaning phone numbers)
phone_number = "+1 (555)-123-4567"
# Params 1 & 2 are empty strings; Param 3 defines chars to strip: " ()-"
deletion_table = str.maketrans("", "", " ()-")
clean_phone_number = phone_number.translate(deletion_table)

print("\nExample 2 (Stripping formatting characters):")
print(clean_phone_number)
# Output: +15551234567


# =============================================================================
# END OF CHEAT_SHEET_1.py
# =============================================================================