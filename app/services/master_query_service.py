"""
master_query_service.py
Reads the master Excel file (sheet "RD") and returns rows filtered
by the "Actual ASP" column matching the logged-in user's full_name.
"""
import os
import pandas as pd

# Sheet name inside master-file.xlsx
SHEET_NAME = "RD"

# Columns whose values are dates — formatted to YYYY-MM-DD for display
DATE_COLUMNS = [
    "Creation Date",
    "WH Ship      (LAPS)",
    "Courier POD",
    "Technician assign Date",
    "Fixed Date",
]

# Column used to filter rows against the current user's full_name
FILTER_COLUMN = "Actual ASP"


def query_master_by_user(excel_path: str, user_full_name: str) -> dict:
    """
    Load the master Excel file and return only the rows where
    ``Actual ASP`` matches *user_full_name* (case-insensitive strip).

    Returns
    -------
    dict with keys:
        headers  : list[str]   — column names
        rows     : list[list]  — filtered data rows
        total    : int         — number of matching rows
        all_total: int         — total rows in the sheet (before filter)
        asp_name : str         — the name used for filtering
    """
    if not os.path.isfile(excel_path):
        return {
            "error": f"Master file not found: {excel_path}",
            "headers": [],
            "rows": [],
            "total": 0,
            "all_total": 0,
            "asp_name": user_full_name,
        }

    # Read the sheet
    df = pd.read_excel(excel_path, sheet_name=SHEET_NAME)
    all_total = len(df)

    # Format date columns to readable strings (date only, no time)
    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = (
                pd.to_datetime(df[col], errors="coerce")
                .dt.strftime("%Y-%m-%d")
            )

    # Filter by Actual ASP — case-insensitive, strip whitespace
    if FILTER_COLUMN in df.columns:
        mask = (
            df[FILTER_COLUMN]
            .astype(str)
            .str.strip()
            .str.lower()
            == user_full_name.strip().lower()
        )
        df_filtered = df[mask].copy()
    else:
        # Column missing — return empty
        df_filtered = df.iloc[0:0].copy()

    # Replace NaT / NaN with empty string for clean Jinja rendering
    df_filtered = df_filtered.fillna("")

    return {
        "headers":   df_filtered.columns.tolist(),
        "rows":      df_filtered.values.tolist(),
        "total":     len(df_filtered),
        "all_total": all_total,
        "asp_name":  user_full_name,
    }
