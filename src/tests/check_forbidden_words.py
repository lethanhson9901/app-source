# scripts/check_forbidden_words.py
#!/usr/bin/env python
"""Check for forbidden words in Python files."""
import re
import sys
from typing import List, Pattern

FORBIDDEN_PATTERNS: List[Pattern] = [
    re.compile(r"# FIXME\b"),
    re.compile(r"# TODO\b"),
    re.compile(r"print\("),  # Prevent print statements in production code
    re.compile(r"breakpoint\(\)"),  # Prevent debugger statements
]

def check_file(filename: str) -> List[str]:
    """Check a file for forbidden patterns."""
    errors = []
    with open(filename, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file, start=1):
            for pattern in FORBIDDEN_PATTERNS:
                if pattern.search(line):
                    errors.append(f"{filename}:{i}: Found forbidden pattern: {line.strip()}")
    return errors

def main() -> int:
    """Main function."""
    errors = []
    for filename in sys.argv[1:]:
        errors.extend(check_file(filename))
    
    if errors:
        print("\n".join(errors))
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
