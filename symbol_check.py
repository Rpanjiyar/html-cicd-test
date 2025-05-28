import os
import sys
import re

BAD_SYMBOLS = [",", ";", "/", "]", "{"]
BAD_PATTERNS = [
    r";;",                  # double semicolons
    r"{\s*}",               # empty curly braces
    r"//.*[;]",             # semicolon in single-line comment
    r"[^\s]\[",             # missing space before [
    r"function\s*\(",       # JS-style function call (if used incorrectly)
]

# File types to scan
EXTENSIONS = (".js", ".ts", ".py", ".html", ".jsx", ".tsx")

def scan_file(filepath):
    issues = []
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for lineno, line in enumerate(lines, 1):
            for symbol in BAD_SYMBOLS:
                if symbol in line:
                    issues.append(f"{filepath}:{lineno} => ❌ Found bad symbol: '{symbol}'")

            for pattern in BAD_PATTERNS:
                if re.search(pattern, line):
                    issues.append(f"{filepath}:{lineno} => ⚠️  Pattern matched: '{pattern}'")

    return issues

def walk_dir(directory="."):
    all_issues = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(EXTENSIONS):
                filepath = os.path.join(root, file)
                all_issues.extend(scan_file(filepath))
    return all_issues

if __name__ == "__main__":
    print("🔍 Running smart symbol check...")
    issues = walk_dir(".")
    if issues:
        print("\n".join(issues))
        print("❌ Symbol or formatting issues found.")
        sys.exit(1)
    else:
        print("✅ Code looks clean. You're good to go!")
