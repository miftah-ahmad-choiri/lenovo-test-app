import os

import pandas as pd

from flask import (
    Blueprint,
    render_template
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

# Path to the fixed Excel file inside the project
EXCEL_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "uploads",
    "excel",
    "test-dashboard-file.xlsx"
)

DATE_COLUMNS = [
    "Created On",
    "Order Date",
    "Courier Pick Up",
    "Parts ETA Date",
    "ASP Received Date & Time",
    "Date & Time WO# Closed",
]


@dashboard_bp.route("/dashboard")
def dashboard():

    df = pd.read_excel(
        EXCEL_FILE
    )

    # Format date columns to readable strings (drop time portion)
    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            ).dt.strftime("%Y-%m-%d %H:%M")

    # Replace NaT / NaN with empty string so Jinja renders cleanly
    df = df.fillna("")

    headers = df.columns.tolist()
    rows = df.values.tolist()

    return render_template(
        "dashboard.html",
        headers=headers,
        rows=rows,
        total=len(rows)
    )
