#!/usr/bin/env python3
"""Convert Bandit JSON output to SARIF format."""

import json
import sys

from bandit_sarif_formatter.converter import convert


def main():
    try:
        with open("reports/bandit.json") as f:
            bandit_data = json.load(f)

        sarif_output = convert(bandit_data, "")

        with open("reports/bandit-results.sarif", "w") as f:
            json.dump(sarif_output, f, indent=2)

        print("Successfully converted to SARIF format")
        return 0
    except Exception as e:
        print(f"Error converting to SARIF: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
