import os

from app.config.settings import (
    EXCEL_DIR,
    IMAGE_DIR
)

from app.services.excel_service import (
    read_excel_info
)


def process_uploaded_files(
    uploaded_files
):

    results = []
    excel_info = []

    for file in uploaded_files:

        filename = (
            file.filename
        )

        lower_name = (
            filename.lower()
        )

        # Excel
        if lower_name.endswith(
            (
                ".xlsx",
                ".xls",
                ".csv"
            )
        ):

            dst = os.path.join(
                EXCEL_DIR,
                filename
            )

            file.save(dst)

            info = (
                read_excel_info(
                    dst
                )
            )

            excel_info.append({
                "file":
                    filename,

                **info
            })

            results.append(
                f"Excel saved: {filename}"
            )

        # Image
        elif lower_name.endswith(
            (
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".webp"
            )
        ):

            dst = os.path.join(
                IMAGE_DIR,
                filename
            )

            file.save(dst)

            results.append(
                f"Image saved: {filename}"
            )

        else:

            results.append(
                f"Unsupported: {filename}"
            )

    return {
        "status":
            "success",

        "results":
            results,

        "excel_info":
            excel_info
    }