# datainsightx/quality.py

import pandas as pd
from pandas.api import types as ptypes
from typing import Dict, Any


def missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a detailed report of missing values."""
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df)) * 100

    report = pd.DataFrame({
        "missing_values": missing_count,
        "percentage": missing_percent.round(2)
    })

    return report[report["missing_values"] > 0].sort_values(
        by="percentage", ascending=False
    )


def duplicate_report(df: pd.DataFrame, subset=None, keep="first") -> int:
    """Count duplicate rows in the dataset."""
    if subset is None:
        subset = df.columns.tolist()

    duplicates_mask = df.duplicated(subset=subset, keep=keep)
    return int(duplicates_mask.sum())


def validate_schema(df: pd.DataFrame, expected_schema: Dict[str, str]) -> Any:
    """
    Validate the DataFrame schema against expected columns and datatypes.

    Parameters:
        expected_schema: e.g. {"id": "int", "name": "str"}

    Returns:
        True if schema is valid, otherwise a DataFrame describing issues.
    """
    rows = []

    for col, expected_type in expected_schema.items():
        if col not in df.columns:
            rows.append({
                "column": col,
                "expected_type": expected_type,
                "actual_type": None,
                "status": "missing_column"
            })
            continue

        actual_series = df[col]
        actual_type_name = str(actual_series.dtype).lower()
        expected_type = expected_type.lower()

        if expected_type in ("int", "integer"):
            match = ptypes.is_integer_dtype(actual_series.dropna())
        elif expected_type in ("float", "double"):
            match = ptypes.is_float_dtype(actual_series.dropna())
        elif expected_type in ("str", "string", "object"):
            match = ptypes.is_object_dtype(actual_series.dropna())
        elif expected_type in ("bool", "boolean"):
            match = ptypes.is_bool_dtype(actual_series.dropna())
        elif expected_type in ("datetime", "datetime64"):
            match = ptypes.is_datetime64_any_dtype(actual_series.dropna())
        elif expected_type == "numeric":
            match = ptypes.is_numeric_dtype(actual_series.dropna())
        else:
            match = expected_type in actual_type_name

        rows.append({
            "column": col,
            "expected_type": expected_type,
            "actual_type": actual_type_name,
            "status": "ok" if match else "type_mismatch"
        })

    report = pd.DataFrame(rows)

    # If all ok, return True
    if report["status"].eq("ok").all():
        return True

    return report
