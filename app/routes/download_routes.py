import pandas as pd

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)

from app.services.box_download_service import (
    download_excel_from_box,
)

from app.config.settings import (
    BOX_DOWNLOAD_FOLDER_PATH,
    BOX_DOWNLOAD_FILE_NAME,
)

download_bp = Blueprint(
    "download",
    __name__
)

DATE_COLUMNS = [
    "Created On",
    "Order Date",
    "Courier Pick Up",
    "Parts ETA Date",
    "ASP Received Date & Time",
    "Date & Time WO# Closed",
]


@download_bp.route("/download-page")
def download_page():
    """Render the download page with default config values pre-filled."""
    return render_template(
        "download.html",
        default_folder_path=BOX_DOWNLOAD_FOLDER_PATH,
        default_file_name=BOX_DOWNLOAD_FILE_NAME,
        headers=[],
        rows=[],
        total=0,
        file_name=None,
        error=None,
    )


@download_bp.route("/download-from-box", methods=["POST"])
def download_from_box():
    """
    Accept folder_path and file_name from the form,
    download the Excel from Box, parse it and return
    the table data back to the same page.
    """
    folder_path = request.form.get(
        "folder_path",
        BOX_DOWNLOAD_FOLDER_PATH
    ).strip()

    file_name = request.form.get(
        "file_name",
        BOX_DOWNLOAD_FILE_NAME
    ).strip()

    headers = []
    rows = []
    total = 0
    error = None
    downloaded_file_name = None

    try:
        result = download_excel_from_box(
            folder_path=folder_path,
            file_name=file_name,
        )

        downloaded_file_name = result["file_name"]
        local_path = result["local_path"]

        df = pd.read_excel(local_path)

        for col in DATE_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_datetime(
                    df[col],
                    errors="coerce"
                ).dt.strftime("%Y-%m-%d %H:%M")

        df = df.fillna("")

        headers = df.columns.tolist()
        rows = df.values.tolist()
        total = len(rows)

    except Exception as e:
        error = str(e)

    return render_template(
        "download.html",
        default_folder_path=folder_path,
        default_file_name=file_name,
        headers=headers,
        rows=rows,
        total=total,
        file_name=downloaded_file_name,
        error=error,
    )
