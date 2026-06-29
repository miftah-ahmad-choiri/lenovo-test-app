import os

from app.config.settings import (
    TEMPLATE_DIR,
    UPLOAD_DIR,
    EXCEL_DIR,
    IMAGE_DIR,
    DOWNLOAD_DIR
)


def create_directories():

    directories = [
        TEMPLATE_DIR,
        UPLOAD_DIR,
        EXCEL_DIR,
        IMAGE_DIR,
        DOWNLOAD_DIR
    ]

    for directory in directories:

        os.makedirs(
            directory,
            exist_ok=True
        )

    print("\nDirectories ready:")
    print("Templates:", TEMPLATE_DIR)
    print("Uploads:", UPLOAD_DIR)
    print("Excel:", EXCEL_DIR)
    print("Images:", IMAGE_DIR)
    print("Downloads:", DOWNLOAD_DIR)
