#!/usr/bin/env python3

import json
import sys
from pathlib import Path


def convert_severity(bandit_severity):
    """Convert Bandit severity levels to SARIF severity levels."""
    severity_map = {"LOW": "warning", "MEDIUM": "error", "HIGH": "critical"}
    return severity_map.get(bandit_severity, "note")


def convert_to_sarif(bandit_json):
    """Convert Bandit JSON report to SARIF format."""
    sarif_output = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Bandit",
                        "informationUri": "https://github.com/PyCQA/bandit",
                        "rules": [],
                    }
                },
                "results": [],
            }
        ],
    }

    # Track unique rules
    rules = {}

    for result in bandit_json.get("results", []):
        rule_id = f"B{result.get('test_id', '000')}"

        # Add rule if not already present
        if rule_id not in rules:
            rules[rule_id] = {
                "id": rule_id,
                "name": result.get("test_name", ""),
                "shortDescription": {"text": result.get("issue_text", "")},
                "fullDescription": {"text": result.get("test_name", "")},
                "defaultConfiguration": {
                    "level": convert_severity(result.get("issue_severity", "MEDIUM"))
                },
            }

        # Create result object
        sarif_result = {
            "ruleId": rule_id,
            "level": convert_severity(result.get("issue_severity", "MEDIUM")),
            "message": {"text": result.get("issue_text", "")},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": result.get("filename", ""),
                        },
                        "region": {"startLine": result.get("line_number", 1)},
                    }
                }
            ],
        }

        sarif_output["runs"][0]["results"].append(sarif_result)

    # Add collected rules to the output
    sarif_output["runs"][0]["tool"]["driver"]["rules"] = list(rules.values())

    return sarif_output


def main():
    """Main function to handle file I/O and conversion."""
    if len(sys.argv) != 3:
        print("Usage: bandit_sarif.py <input_json> <output_sarif>")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    try:
        with input_file.open() as f:
            bandit_data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    sarif_data = convert_to_sarif(bandit_data)

    try:
        with output_file.open("w") as f:
            json.dump(sarif_data, f, indent=2)
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
