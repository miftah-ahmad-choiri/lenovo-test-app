from flask import (
    Blueprint,
    render_template,
    jsonify
)

home_bp = Blueprint(
    "home",
    __name__
)


@home_bp.route("/")
def home():

    return render_template(
        "home.html"
    )


@home_bp.route("/upload-page")
def upload_page():

    return render_template(
        "index.html"
    )


@home_bp.route("/health")
def health():

    return jsonify({
        "status":
            "backend_running"
    })