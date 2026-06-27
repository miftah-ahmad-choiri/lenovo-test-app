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

USE_NGROK = False