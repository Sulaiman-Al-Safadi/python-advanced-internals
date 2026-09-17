"""
===============================================================================
                        SESSION 4: CHEAT_SHEET_4.py
===============================================================================
A quick-reference study sheet covering advanced datetime management, 
timezone handling, JSON data serialization, comprehensive Regular Expressions 
(Regex) pattern building, and safe CSV database file I/O operations.

-------------------------------------------------------------------------------
TABLE OF FUNCTIONS & REASONING SUMMARY
-------------------------------------------------------------------------------
1. datetime & zoneinfo:
   - datetime.now()             : Retrieves local system date & time object.
   - timedelta(days=N, ...)     : Performs date arithmetic (addition/subtraction).
   - strftime(format)           : Converts datetime object to formatted string (date -> str).
   - strptime(string, format)   : Parses string text into a datetime object (str -> date).
   - ZoneInfo("Continent/City") : Sets specific geographical timezone (Requires 'tzdata' on Windows).
   - timezone.utc               : Standard built-in UTC timezone fallback without external dependencies.

2. json Module:
   - json.dumps(obj, indent=4)  : Serializes Python dict/list to JSON formatted String.
   - json.loads(json_str)       : Deserializes JSON formatted String back into Python dict/list.
   - json.dump(obj, file_obj)   : Writes Python data directly to an open JSON file on disk.
   - json.load(file_obj)        : Reads open JSON file on disk directly into Python data structure.

3. re Module (Regex Mechanics & Pattern Building Guide):
   - re.findall(pattern, text)  : Extracts all non-overlapping matches into a list.
   - re.search(pattern, text)   : Searches entire string for the first match object.
   - re.sub(pattern, repl, text): Replaces pattern matches with replacement string.
   
   PATTERN BUILDING BLOCKS & SYMBOLS GUIDE:
   ---------------------------------------
   - \d : Any single digit (0-9)               | \D : Any NON-digit character
   - \w : Word character (a-z, A-Z, 0-9, _)    | \W : Any NON-word character (symbols, space)
   - \s : Any whitespace (space, tab, newline) | \S : Any NON-whitespace character
   - .  : Any single character except newline (\n)
   - [abc] : Custom set (matches 'a', 'b', or 'c' only)
   - [^abc]: Negated set (matches anything EXCEPT 'a', 'b', or 'c')
   - +  : 1 or more occurrences (Mandatory)
   - *  : 0 or more occurrences (Optional)
   - ?  : 0 or 1 occurrence (Optional)
   - {n}: Exactly 'n' repetitions
   - (?P<name>...): Named Capture Group (extracts matched values cleanly into dictionaries)

4. csv Module:
   - csv.DictWriter(file, fieldnames=...) : Writes dict rows to CSV matching header names.
   - csv.DictReader(file)                : Reads CSV rows directly as Python dictionaries.

===============================================================================
"""

# =============================================================================
# 1. datetime & zoneinfo
# =============================================================================
# PURPOSE:
#   Provides accurate date arithmetic, string formatting/parsing, and 
#   cross-platform timezone conversions.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Confusing strftime vs strptime:
#      - strftime (Format Time) converts date object -> string.
#      - strptime (Parse Time) converts string -> date object.
#   ⚠️ Comparing naive datetime (no timezone) with aware datetime (with timezone):
#      - Throws TypeError! Always compare dates with matching timezone awareness.
#   ⚠️ Windows ZoneInfo Missing Database:
#      - If ZoneInfo("Asia/Damascus") throws ZoneInfoNotFoundError on Windows,
#        run `pip install tzdata` once in VS Code Terminal to load global cities.
#
# COMPLEXITY: Time O(1) date operations | Space O(1)

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

print("=== 1. datetime & zoneinfo ===")

# EXAMPLE 1: Date Arithmetic, Formatting, and Parsing
now = datetime.now()                                                         # Fetches current local system datetime
future_date = now + timedelta(days=7, hours=3)                               # Adds 7 days and 3 hours to current time

date_text = "2026-08-29 14:30:00"
parsed_date = datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S")              # Converts text string into datetime object

print("Example 1 (Date Calculations & Formatting):")
print(f"Formatted Current Time : {now.strftime('%Y-%m-%d %H:%M:%S')}")        # Formats date to readable YYYY-MM-DD text
print(f"Future Date (+7d 3h)   : {future_date.strftime('%Y-%m-%d')}")          # Displays calculated future date
print(f"Parsed Date Object     : {parsed_date}")                             # Output: 2026-08-29 14:30:00

# EXAMPLE 2: Cross-Platform Timezone Conversion
utc_time = parsed_date.replace(tzinfo=timezone.utc)                          # Explicitly sets UTC timezone using built-in module

try:
    damascus_time = utc_time.astimezone(ZoneInfo("Asia/Damascus"))          # Converts UTC time to Damascus local timezone
    print("\nExample 2 (Timezone Conversion):")
    print(f"UTC Time      : {utc_time}")                                      # Timezone-aware UTC object
    print(f"Damascus Time : {damascus_time}")                                  # Timezone-aware local city object
except Exception as e:
    print(f"\nExample 2 Fallback: Install 'tzdata' via pip to use city names. UTC Time: {utc_time}")


# =============================================================================
# 2. json Module
# =============================================================================
# PURPOSE:
#   Converts Python data structures (dicts, lists) to standard JSON format for APIs,
#   and reads/writes JSON files directly from disk safely.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Confusing dumps/loads (String) with dump/load (File):
#      - `dumps` and `loads` operating on Strings in memory (note the 's').
#      - `dump` and `load` operate directly on File objects opened with `open()`.
#   ❌ Omitting `ensure_ascii=False`:
#      - Non-English characters (e.g., Arabic text) get escaped as \u0623 if False is omitted.
#
# COMPLEXITY: Time O(N) data serialization | Space O(N) JSON output

import json
from pathlib import Path

print("\n=== 2. json Module ===")

user_profile = {
    "user_id": 1001,
    "name": "Samer",
    "is_active": True,
    "skills": ["Python", "Git", "Regex"],
    "location": {"city": "Damascus", "country": "Syria"}
}

# EXAMPLE 1: In-Memory Serialization & Deserialization (dumps & loads)
json_string = json.dumps(user_profile, indent=4, ensure_ascii=False)          # Serializes Python dict into formatted JSON string
parsed_profile = json.loads(json_string)                                     # Deserializes JSON string back into Python dictionary

print("Example 1 (In-Memory String Conversion):")
print("Formatted JSON String:\n" + json_string)
print(f"Extracted Skill from Dict: {parsed_profile['skills'][0]}")

# EXAMPLE 2: Direct Disk File Storage & Retrieval (dump & load)
json_file_path = Path("user_data.json")

with open(json_file_path, "w", encoding="utf-8") as file:
    json.dump(user_profile, file, indent=4, ensure_ascii=False)              # Writes JSON content directly to disk file

with open(json_file_path, "r", encoding="utf-8") as file:
    loaded_file_data = json.load(file)                                      # Reads JSON file directly into Python dictionary

print("\nExample 2 (File Storage Operations):")
print(f"Saved file to disk : {json_file_path.name}")
print(f"Read ID from file  : {loaded_file_data['user_id']}")


# =============================================================================
# 3. re Module (Regular Expressions)
# =============================================================================
# PURPOSE:
#   Provides powerful pattern matching for string validation, text extraction,
#   data masking, and structural parsing using regular expressions.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ❌ Writing pattern strings without raw prefix `r"..."`:
#      - Escape sequences like `\d` or `\n` get misinterpreted by Python string parser.
#   ❌ Using re.match() instead of re.search():
#      - re.match() ONLY checks the start of the string. re.search() scans full string.
#
# COMPLEXITY: Time O(N) pattern search | Space O(M) extracted groups

import re

print("\n=== 3. re Module ===")

sample_log = """
[2026-08-29] ERROR: Database connection failed on host 192.168.1.50
Contact: admin@company.com or security@company.org
Candidate Skills: Python, Git, Docker, Linux - Experience: 4 years
"""

# EXAMPLE 1: Extracting All Emails using re.findall
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
extracted_emails = re.findall(email_pattern, sample_log)                     # Scans text and extracts all matching emails into list

print("Example 1 (Extracting All Email Matches):")
print(f"Found Emails: {extracted_emails}")

# EXAMPLE 2: Named Capture Groups (?P<name>...) with re.search
# Pattern breakdown:
# \[(?P<date>\d{4}-\d{2}-\d{2})\] -> Matches date inside square brackets
# \s+(?P<level>[A-Z]+):           -> Matches log level (ERROR/INFO) after spaces
# \s+(?P<message>.+?)             -> Non-greedily matches log message content
# \s+host\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) -> Matches host IP address
log_pattern = r"\[(?P<date>\d{4}-\d{2}-\d{2})\]\s+(?P<level>[A-Z]+):\s+(?P<message>.+?)\s+host\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})"

log_match = re.search(log_pattern, sample_log)

print("\nExample 2 (Named Capture Groups to Dictionary):")
if log_match:
    parsed_log_dict = log_match.groupdict()                                  # Converts named match groups directly into Python dict
    print(f"Parsed Dict : {parsed_log_dict}")
    print(f"Log Date    : {parsed_log_dict['date']}")
    print(f"Log Level   : {parsed_log_dict['level']}")
    print(f"Host IP     : {parsed_log_dict['ip']}")

# EXAMPLE 3: Parsing Comma-Separated Data & Masking (re.sub)
skills_pattern = r"Skills:\s*([^-\n]+)"                                      # Captures everything after 'Skills:' until '-' or newline
skills_match = re.search(skills_pattern, sample_log)

print("\nExample 3 (Comma-Separated Extraction & Masking):")
if skills_match:
    raw_skills = skills_match.group(1).strip()
    skills_list = [s.strip() for s in raw_skills.split(",")]                 # Cleanly splits comma-separated string into Python list
    print(f"Clean Skills List : {skills_list}")

masked_log = re.sub(r"\d{1,3}(?:\.\d{1,3}){3}", "XXX.XXX.X.X", sample_log)   # Masks IP addresses in text for privacy
print("Masked IP Text Sample:")
print(masked_log.strip().split("\n")[0])                                     # Prints first line with masked IP


# =============================================================================
# 4. csv Module
# =============================================================================
# PURPOSE:
#   Reads and writes CSV tabular spreadsheet data using dictionaries, avoiding
#   manual string splitting bugs when data contains commas.
#
# PITFALLS & MY WRONG ATTEMPTS:
#   ⚠️ Forgetting `newline=""` in open() on Windows:
#      - Python adds unwanted extra blank lines between rows on Windows platforms.
#   ⚠️ Assuming numeric types during CSV read:
#      - DictReader parses ALL values as strings. Always convert explicitly (int/float).
#
# COMPLEXITY: Time O(N) row processing | Space O(1) streaming file I/O

import csv

print("\n=== 4. csv Module ===")

csv_file_path = Path("employees_data.csv")

employees_list = [
    {"id": "101", "name": "Samer", "department": "IT", "salary": "1200"},
    {"id": "102", "name": "Ahmad", "department": "Sales", "salary": "950"},
    {"id": "103", "name": "Sara", "department": "IT", "salary": "1400"}
]

csv_headers = ["id", "name", "department", "salary"]

# EXAMPLE 1: Writing CSV File via DictWriter
with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()                                                     # Writes top header row matching dictionary keys
    writer.writerows(employees_list)                                         # Writes all dictionary objects as rows

print("Example 1 (CSV File Creation):")
print(f"Successfully generated CSV: {csv_file_path.name}")

# EXAMPLE 2: Reading CSV File via DictReader & Data Conversion
print("\nExample 2 (Reading & Parsing CSV Records):")
with open(csv_file_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)                                            # Iterates rows as dictionary mapping header -> value
    
    total_it_salary = 0
    for row in reader:
        salary_num = int(row["salary"])                                      # Explicit string to integer conversion
        print(f"ID: {row['id']} | Name: {row['name']} | Dept: {row['department']} | Salary: ${salary_num}")
        
        if row["department"] == "IT":
            total_it_salary += salary_num

    print(f"\nTotal IT Department Salary: ${total_it_salary}")


# =============================================================================
# END OF CHEAT_SHEET_4.py
# =============================================================================