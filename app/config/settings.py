import os

BASE_DIR = os.path.abspath(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

TEMPLATE_DIR = os.path.join(
    BASE_DIR,
    "templates"
)

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads"
)

EXCEL_DIR = os.path.join(
    UPLOAD_DIR,
    "excel"
)

IMAGE_DIR = os.path.join(
    UPLOAD_DIR,
    "images"
)

DOWNLOAD_DIR = os.path.join(
    BASE_DIR,
    "downloads"
)

USE_NGROK = False

# ── Box Configuration ──────────────────────────────────────────────────────
# Developer token expires every 60 minutes — refresh in the Box Developer Console.

BOX_TOKEN = "iIJDRmfJbFLurXt3z0dY5mEWps3bOrqm"

# Upload: root folder that receives uploaded files
BOX_UPLOAD_ROOT_FOLDER_ID = "0"
BOX_UPLOAD_FOLDER_NAME = "Lenovo Ticket Upload"

# Download: full path inside Box to the folder containing the target file
BOX_DOWNLOAD_FOLDER_PATH = "/Lenovo-Ticketing-System-Development/Lenovo-Apps/Download"

# Default Excel file name to download (can be overridden via the UI)
BOX_DOWNLOAD_FILE_NAME = "test-dashboard-file2.xlsx"
