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

EXTENSIONS = (".js", ".ts", ".py", ".html", ".jsx", ".tsx")

# Regex patterns to strip strings and comments (basic)
STRIP_STRINGS_REGEX = r"(\".*?\"|\'.*?\')"
SINGLE_LINE_COMMENT_REGEX = r"(#.*|//.*)"
MULTILINE_COMMENT_REGEX = r"(\/\*[\s\S]*?\*\/|\"\"\"[\s\S]*?\"\"\"|\'\'\'[\s\S]*?\'\'\')"

def clean_line(line):
    # Remove strings
    line = re.sub(STRIP_STRINGS_REGEX, '', line)
    # Remove single-line comments
    line = re.sub(SINGLE_LINE_COMMENT_REGEX, '', line)
    return line

def remove_multiline_comments(content):
    return re.sub(MULTILINE_COMMENT_REGEX, '', content)

def scan_file(filepath):
    issues = []
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        content = remove_multiline_comments(content)
        lines = content.splitlines()

        for lineno, line in enumerate(lines, 1):
            raw_line = line  # keep original for context
            line = clean_line(line)

            for symbol in BAD_SYMBOLS:
                if symbol in line:
                    issues.append(f"{filepath}:{lineno} => ❌ Bad symbol: '{symbol}' in: {raw_line.strip()}")

            for pattern in BAD_PATTERNS:
                if re.search(pattern, line):
                    issues.append(f"{filepath}:{lineno} => ⚠️  Pattern matched: '{pattern}' in: {raw_line.strip()}")

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
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"🔍 Running smart symbol check in '{target_dir}'...")
    issues = walk_dir(target_dir)
    if issues:
        print("\n".join(issues))
        print("❌ Symbol or formatting issues found.")
        sys.exit(1)
    else:
        print("✅ Code looks clean. You're good to go!")
