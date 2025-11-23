# datainsightx/cli.py

import argparse
import sys
import pandas as pd
from datainsightx.quality import (
    missing_value_report,
    duplicate_report,
    validate_schema,
)


def main():
    parser = argparse.ArgumentParser(
        prog="datainsightx",
        description="DataInsightX - Data quality assessment CLI tool",
    )

    parser.add_argument(
        "command",
        choices=["analyze", "quality"],
        help="Command to execute: analyze (all checks) or quality (data quality report only)",
    )

    parser.add_argument(
        "file",
        help="Path to the input CSV file",
    )

    args = parser.parse_args()

    # Load dataset
    try:
        df = pd.read_csv(args.file)
    except Exception as e:
        print(f"Error: Unable to load file. Details: {e}")
        sys.exit(1)

    # Run Quality Checks
    if args.command in ["analyze", "quality"]:
        print("\nRunning data quality checks...\n")

        # Missing values
        print("Missing Value Report:")
        mv_report = missing_value_report(df)
        if mv_report.empty:
            print("✓ No missing values detected.\n")
        else:
            print(mv_report, "\n")

        # Duplicate rows
        print("Duplicate Row Report:")
        dup_count = duplicate_report(df)
        if dup_count == 0:
            print("✓ No duplicate rows detected.\n")
        else:
            print(f"Found {dup_count} duplicate rows.\n")

        # Schema validation
        print("Schema Validation:")
        expected_schema = list(df.columns)  # Placeholder for future configuration
        schema_result = validate_schema(df, expected_schema)
        if schema_result is True:
            print("✓ Schema validation passed.\n")
        else:
            print("Schema mismatch detected:")
            print(schema_result, "\n")

        print("Data quality analysis completed.\n")
