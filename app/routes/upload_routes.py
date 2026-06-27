from flask import (
    Blueprint,
    request,
    jsonify
)

from app.services.upload_service import (
    process_uploaded_files
)

upload_bp = Blueprint(
    "upload",
    __name__
)


@upload_bp.route(
    "/upload",
    methods=["POST"]
)
def upload():

    uploaded_files = (
        request.files.getlist(
            "files"
        )
    )

    if not uploaded_files:

        return jsonify({
            "status":
                "failed",

            "message":
                "No files uploaded"
        }), 400

    result = (
        process_uploaded_files(
            uploaded_files
        )
    )

    return jsonify(result)