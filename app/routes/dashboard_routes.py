import os

from flask import (
    Blueprint,
    render_template
)
from flask_login import login_required, current_user

from app.config.settings import MASTER_FILE
from app.services.master_query_service import query_master_by_user

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    result = query_master_by_user(
        excel_path=MASTER_FILE,
        user_full_name=current_user.full_name
    )

    return render_template(
        "dashboard.html",
        headers=result["headers"],
        rows=result["rows"],
        total=result["total"],
        all_total=result["all_total"],
        asp_name=result["asp_name"],
        error=result.get("error")
    )
