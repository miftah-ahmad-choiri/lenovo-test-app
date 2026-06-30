from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import Session

from app.database.db import engine, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Already authenticated users go straight to home
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))

    error = None

    if request.method == "POST":
        user_id  = request.form.get("user_id",  "").strip()
        password = request.form.get("password", "").strip()

        with Session(engine) as db_session:
            user = db_session.get(User, user_id)

        if user and user.password == password:
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home.home"))

        error = "Invalid user ID or password. Please try again."

    return render_template("login.html", error=error)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
