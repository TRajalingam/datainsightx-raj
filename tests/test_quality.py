import pandas as pd
from pathlib import Path
from datainsightx.quality import missing_value_report


def test_missing_value_report():
    # Locate test dataset relative to this test file
    test_file_path = Path(__file__).parent / "sample_data" / "sales_data.csv"

    # Load dataset
    df = pd.read_csv(test_file_path)

    # Run the function
    report = missing_value_report(df)

    # Validate structure
    assert "Missing Values" in report.columns
    assert "Percentage" in report.columns

    # Validate missing count for specific column
    assert "Discount" in report.index
    missing_value = int(report.loc["Discount", "Missing Values"])
    assert missing_value == 1

    # Validate percentage range
    percent = report.loc["Discount", "Percentage"]
    assert 0 <= percent <= 100
