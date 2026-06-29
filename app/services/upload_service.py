import os

from app.config.settings import (
    EXCEL_DIR,
    IMAGE_DIR
)

from app.services.excel_service import (
    read_excel_info
)

from app.services.box_service import (
    upload_file_to_box
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
                _upload_to_box_and_build_result(
                    dst,
                    filename,
                    "Excel"
                )
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
                _upload_to_box_and_build_result(
                    dst,
                    filename,
                    "Image"
                )
            )

        else:

            results.append({
                "file": filename,
                "status": "skipped",
                "message": f"Unsupported file type: {filename}"
            })

    return {
        "status":
            "success",

        "results":
            results,

        "excel_info":
            excel_info
    }


def _upload_to_box_and_build_result(
    local_path,
    filename,
    file_type
):
    """Save locally, push to Box, delete local copy, return result dict."""
    try:

        box_info = upload_file_to_box(
            local_path,
            filename
        )

        return {
            "file": filename,
            "type": file_type,
            "status": "success",
            "message": f"{file_type} uploaded to Box and removed locally",
            "box_file_id": box_info["box_file_id"],
            "box_file_name": box_info["box_file_name"],
        }

    except Exception as e:

        return {
            "file": filename,
            "type": file_type,
            "status": "error",
            "message": str(e),
        }
