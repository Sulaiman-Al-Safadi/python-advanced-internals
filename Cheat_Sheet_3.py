"""
===============================================================================
                        SESSION 3: CHEAT_SHEET_3.py
===============================================================================
A quick-reference study sheet covering advanced standard library utilities,
modern file system handling, resource management, function argument freezing,
safe enumerations, fast binary search indexing, wildcard file pattern matching,
and high-level file/archive manipulation.

-------------------------------------------------------------------------------
TABLE OF CONTENTS
-------------------------------------------------------------------------------
1. pathlib.Path
2. contextlib.contextmanager
3. functools.partial
4. enum.Enum & enum.auto
5. bisect Module (bisect & insort)
6. fnmatch & glob Modules
7. shutil Module
===============================================================================
"""

# =============================================================================
# 1. pathlib.Path
# =============================================================================
# SIGNATURE:
#   Path(*pathsegments)
#    └── *pathsegments: Path strings or Path objects joined dynamically with '/'
#
# PURPOSE:
#   Provides an object-oriented interface for cross-platform file system paths,
#   replacing legacy os.path calls with clean syntax and built-in I/O methods.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Calling `.write_text()` on a path inside a non-existent parent directory
#      - Throws FileNotFoundError: Parent directory must exist on disk first.
#      - FIX: Always run `file_path.parent.mkdir(parents=True, exist_ok=True)`
#   ❌ Treating Path object as string in legacy libraries requiring raw strings
#      - FIX: Explicitly convert with `str(path_obj)` when required.
#
# COMPLEXITY: Time O(1) path creation | Space O(1)

from pathlib import Path

print("=== 1. pathlib.Path ===")

# EXAMPLE 1: Cross-platform path creation and metadata extraction
base_dir = Path("project_logs")                                              # Creates a base Path object for folder
file_path = base_dir / "app_config.txt"                                      # Dynamically joins path segments using '/' operator

print("Example 1 (Path Metadata Extraction):")
print(f"Full Path        : {file_path}")                                     # Output: project_logs/app_config.txt
print(f"File Name (Name) : {file_path.name}")                                # Output: app_config.txt (filename + extension)
print(f"File Name Only   : {file_path.stem}")                                # Output: app_config (filename without extension)
print(f"Extension        : {file_path.suffix}")                              # Output: .txt (file extension only)
print(f"Parent Directory : {file_path.parent}")                              # Output: project_logs (parent directory)

# EXAMPLE 2: Safe directory creation and direct file write/read without open()
file_path.parent.mkdir(parents=True, exist_ok=True)                          # Safely creates parent folders if missing on disk
file_path.write_text("API_KEY=123456\nSTATUS=active", encoding="utf-8")       # Writes string content directly into the file

print("\nExample 2 (Direct File Read & File System Checks):")
file_content = file_path.read_text(encoding="utf-8")                        # Reads entire text content directly without open()
print("File Content:\n" + file_content)
print(f"Is File Exists?  : {file_path.exists()}")                            # Checks if path exists on disk (True)
print(f"Is it a File?    : {file_path.is_file()}")                            # Confirms if path points to a file (True)


# =============================================================================
# 2. contextlib.contextmanager
# =============================================================================
# SIGNATURE:
#   @contextmanager
#   def generator_func(*args, **kwargs):
#       # 1. Setup code
#       yield [target_value]
#       # 2. Cleanup code (inside try...finally)
#
# PURPOSE:
#   Converts a generator function into a custom 'with' statement Context Manager
#   without writing a full class with __enter__ and __exit__ methods.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Omitting `try...finally` block around `yield`
#      - If an exception occurs inside the 'with' block, code after `yield` is skipped,
#        causing resource leaks (unclosed DB connections or locks).
#   ❌ Writing multiple `yield` statements inside the context manager function.
#      - Throws RuntimeError: generator didn't yield or yielded more than once.
#
# COMPLEXITY: Time O(1) overhead | Space O(1)

import time
from contextlib import contextmanager

print("\n=== 2. contextlib.contextmanager ===")

# EXAMPLE 1: Execution Timer Context Manager
@contextmanager
def execution_timer(task_name):
    start_time = time.perf_counter()                                         # Record start time on context entry
    print(f"[START] Task '{task_name}' started...")
    try:
        yield                                                                # Transfers execution control to inside 'with' block
    finally:
        elapsed = time.perf_counter() - start_time                           # Calculate duration regardless of errors inside block
        print(f"[END] Task '{task_name}' finished in {elapsed:.4f} seconds.")

print("Example 1 (Timer Execution):")
with execution_timer("Data Processing"):
    total_sum = sum(i ** 2 for i in range(500000))                           # Simulated workload execution
    print(f"Computed sum: {total_sum}")


# EXAMPLE 2: Database Connection Resource Manager Passing Value
@contextmanager
def managed_db_connection(db_name):
    connection = {"status": "CONNECTED", "database": db_name}                # Setup: Acquire resource / open connection
    print(f"\n[DB] Connected to {db_name}")
    try:
        yield connection                                                     # Passes resource object to 'as' target in 'with'
    finally:
        connection["status"] = "DISCONNECTED"                                # Cleanup: Safely tear down resource on exit
        print(f"[DB] Disconnected from {db_name} (Status: {connection['status']})")

print("\nExample 2 (Resource Management):")
with managed_db_connection("analytics_db") as db:
    print(f"Executing query on DB '{db['database']}' with status '{db['status']}'")


# =============================================================================
# 3. functools.partial
# =============================================================================
# SIGNATURE:
#   partial(func, *args, **keywords)
#    ├── func: Target callable function to wrap.
#    └── *args, **keywords: Positional or keyword arguments to freeze in advance.
#
# PURPOSE:
#   Freezes a portion of a function's arguments to derive a simpler callable
#   function with fewer required arguments.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ⚠️ Argument Binding Order: Unnamed positional arguments freeze from left to right.
#   ⚠️ Mutable Default Binding: Passing a mutable object (like a list) binds its memory reference.
#
# COMPLEXITY: Time O(1) function wrapper creation | Space O(1)

from functools import partial

print("\n=== 3. functools.partial ===")

# EXAMPLE 1: Freezing Positional Arguments
def multiply(a, b, c):
    return a * b * c

double_and_triple = partial(multiply, 2, 3)                                  # Freezes a=2 and b=3 into new callable function

print("Example 1 (Freezing positional parameters):")
print(f"Result (2 * 3 * 5): {double_and_triple(5)}")                         # Passes only remaining parameter c=5 (Output: 30)


# EXAMPLE 2: Real-world Tax Calculator via Keyword Binding
def calculate_total_price(price, tax_rate):
    return price + (price * tax_rate)

apply_standard_vat = partial(calculate_total_price, tax_rate=0.15)          # Freezes tax_rate to 15% standard rate
apply_reduced_vat = partial(calculate_total_price, tax_rate=0.05)           # Freezes tax_rate to 5% reduced rate

print("\nExample 2 (Tax Calculator Application):")
print(f"Product 1 ($100 + 15% VAT): ${apply_standard_vat(100)}")            # Computes 100 + (100 * 0.15) -> Output: 115.0
print(f"Product 2 ($100 + 5% VAT) : ${apply_reduced_vat(100)}")             # Computes 100 + (100 * 0.05) -> Output: 105.0


# =============================================================================
# 4. enum.Enum & enum.auto
# =============================================================================
# SIGNATURE:
#   class EnumName(Enum):
#       MEMBER = auto() / value
#
# PURPOSE:
#   Defines a type-safe set of symbolic, immutable constants to replace raw
#   magic strings/numbers, preventing typos and providing IDE auto-completion.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Comparing Enum object directly to raw string: `OrderStatus.PENDING == "PENDING"`
#      - Evaluates to False! Compare against `.name` or use Enum object directly.
#   ❌ Attempting to modify Enum member values dynamically at runtime.
#      - Throws AttributeError: Cannot reassign Enum members (Immutable).
#
# COMPLEXITY: Time O(1) lookup | Space O(1)

from enum import Enum, auto

print("\n=== 4. enum.Enum & enum.auto ===")

# EXAMPLE 1: Defining type-safe status enumeration using auto()
class OrderStatus(Enum):
    PENDING = auto()                                                         # Automatically assigns integer value 1
    PROCESSING = auto()                                                      # Automatically assigns integer value 2
    SHIPPED = auto()                                                         # Automatically assigns integer value 3
    DELIVERED = auto()                                                       # Automatically assigns integer value 4

def process_order(order_id, status):
    if status == OrderStatus.SHIPPED:
        print(f"Order #{order_id} is currently shipped and in transit.")
    elif status == OrderStatus.DELIVERED:
        print(f"Order #{order_id} has been successfully delivered.")

current_order_status = OrderStatus.SHIPPED

print("Example 1 (Enum Name, Value & Comparison):")
print(f"Member Name : {current_order_status.name}")                          # Output: SHIPPED
print(f"Member Value: {current_order_status.value}")                         # Output: 3
process_order(505, current_order_status)


# EXAMPLE 2: Explicit value mapping for DB serialization / HTTP status codes
class HTTPStatus(Enum):
    OK = 200                                                                 # Explicit integer status mapping
    NOT_FOUND = 404
    SERVER_ERROR = 500

incoming_code = 404
status_instance = HTTPStatus(incoming_code)                                  # Reconstructs Enum object from numeric database/API value

print("\nExample 2 (Deserializing Value to Enum):")
print(f"Reconstructed Enum: {status_instance}")                              # Output: HTTPStatus.NOT_FOUND
print(f"Status Name       : {status_instance.name}")                         # Output: NOT_FOUND


# =============================================================================
# 5. bisect Module (bisect & insort)
# =============================================================================
# SIGNATURE:
#   bisect.bisect_right(a, x) / bisect.bisect_left(a, x)
#    ├── a: Target list (MUST BE SORTED).
#    └── x: Value to search insertion index for.
#
#   bisect.insort(a, x)
#    └── Inserts element 'x' directly into list 'a' in sorted position.
#
# PURPOSE:
#   Fast binary search operations on sorted sequences to find insertion points
#   or keep lists sorted in O(log N) search time without calling list.sort().
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ⚠️ Executing bisect functions on an UNSORTED list.
#      - Will not raise an Error, but returns totally incorrect index positions!
#
# COMPLEXITY: Time O(log N) search, O(N) list insertion | Space O(1)

import bisect

print("\n=== 5. bisect Module ===")

# EXAMPLE 1: Inserting into a sorted list while maintaining sorted order
sorted_prices = [10, 25, 50, 100, 150]                                       # Initial sorted list
new_item_price = 30

target_index = bisect.bisect(sorted_prices, new_item_price)                 # Finds correct insertion index without altering list
print("Example 1 (Binary Search Insertion Position):")
print(f"Insertion Index for ${new_item_price}: {target_index}")              # Output: 2

bisect.insort(sorted_prices, new_item_price)                                # Inserts value directly into sorted position
print(f"List after insort: {sorted_prices}")                                # Output: [10, 25, 30, 50, 100, 150]


# EXAMPLE 2: Fast Grade Bucket Classification using bisect_right
score_breakpoints = [60, 70, 80, 90]                                        # Score threshold boundaries
letter_grades = ["F", "D", "C", "B", "A"]                                   # Corresponding grade categories

def classify_score(score):
    grade_index = bisect.bisect_right(score_breakpoints, score)              # Locates bucket index via fast binary search
    return letter_grades[grade_index]

print("\nExample 2 (Bucket Classifier):")
print(f"Score 55 -> Grade: {classify_score(55)}")                            # Output: F (< 60)
print(f"Score 75 -> Grade: {classify_score(75)}")                            # Output: C (between 70 and 80)
print(f"Score 95 -> Grade: {classify_score(95)}")                            # Output: A (> 90)


# =============================================================================
# 6. fnmatch & glob Modules
# =============================================================================
# SIGNATURE:
#   fnmatch.fnmatch(filename, pattern)
#    ├── filename (str): String filename to test.
#    └── pattern (str): Wildcard string (* matches all, ? matches 1 char).
#
#   glob.glob(pathname, recursive=False)
#    └── pathname: Path wildcard pattern (e.g., "**/*.py").
#
# PURPOSE:
#   Filters text filenames using shell wildcards (fnmatch) and searches disk
#   directories directly to retrieve matching file paths (glob).
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ⚠️ Forgetting `recursive=True` when using '**' wildcard in glob.
#      - If recursive=False, '**' will treat double asterisks as single directory level.
#
# COMPLEXITY: Time O(N) directory scan / string evaluation | Space O(M) matched files

import glob
from fnmatch import fnmatch

print("\n=== 6. fnmatch & glob ===")

# EXAMPLE 1: Filtering text filenames using fnmatch wildcards
file_list = ["data_2026.csv", "image_01.png", "data_2025.csv", "notes.txt", "image_02.jpg"]

print("Example 1 (Wildcard String Matching):")
for filename in file_list:
    if fnmatch(filename, "data_*.csv"):                                      # '*' matches any character sequence
        print(f"Matched CSV File: {filename}")                               # Prints data_2026.csv & data_2025.csv

for filename in file_list:
    if fnmatch(filename, "image_??.*"):                                      # '??' matches exactly 2 characters
        print(f"Matched Image File: {filename}")                             # Prints image_01.png & image_02.jpg


# EXAMPLE 2: Disk Directory Scanning with glob
print("\nExample 2 (Disk File Retrieval with glob):")
python_files = glob.glob("*.py")                                             # Searches current folder for .py files
print(f"Current directory Python files: {python_files}")

nested_txt_files = glob.glob("**/*.txt", recursive=True)                    # Deep search in current directory & subfolders
print(f"All subfolder text files: {nested_txt_files}")


# =============================================================================
# 7. shutil Module
# =============================================================================
# SIGNATURE:
#   shutil.copy2(src, dst) -> Preserves content + file metadata (timestamps).
#   shutil.copytree(src, dst, dirs_exist_ok=False) -> Copies full folder tree.
#   shutil.make_archive(base_name, format, root_dir) -> Creates ZIP/TAR archives.
#   shutil.rmtree(path) -> Recursively deletes directory and all contents.
#
# PURPOSE:
#   Executes high-level, bulk file system operations including recursive directory
#   copying, zip archiving, metadata preservation, and complete folder deletion.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Using `shutil.copy()` instead of `shutil.copy2()` for backups
#      - `copy()` loses file modification time and metadata. `copy2()` retains it.
#   ⚠️ DANGER: `shutil.rmtree()` permanently deletes directory tree without recycling bin!
#
# COMPLEXITY: Time O(N) file system I/O | Space O(N) copied/compressed data

import shutil

print("\n=== 7. shutil Module ===")

# Setup demo directories for safe execution
demo_source = Path("demo_app")
demo_source.mkdir(exist_ok=True)
(demo_source / "config.txt").write_text("APP_ENV=production", encoding="utf-8")

# EXAMPLE 1: Copying single file with metadata & copying entire folder tree
backup_folder = Path("demo_app_backup")

shutil.copy2(demo_source / "config.txt", demo_source / "config_backup.txt")   # Copies file while preserving creation/modification timestamps
shutil.copytree(demo_source, backup_folder, dirs_exist_ok=True)              # Copies whole directory recursively

print("Example 1 (File Copy & Directory Tree Backup):")
print(f"Directory tree successfully copied to: {backup_folder}")


# EXAMPLE 2: Creating ZIP Archive
archive_file = shutil.make_archive("demo_archive", "zip", root_dir=demo_source) # Compresses source directory into demo_archive.zip
print("\nExample 2 (ZIP Archive Creation):")
print(f"ZIP Archive generated at: {archive_file}")


# EXAMPLE 3: Recursive Directory Deletion
shutil.rmtree(backup_folder)                                                 # Recursively deletes backup directory and all contents
print("\nExample 3 (Clean Directory Tree Deletion):")
print(f"Directory '{backup_folder}' permanently removed.")


# =============================================================================
# END OF CHEAT_SHEET_3.py
# =============================================================================