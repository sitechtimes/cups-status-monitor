import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from cups_status_monitor.db import get_db

"""
Source: https://flask.palletsprojects.com/en/stable/tutorial/views
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application, they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
"""
bp = Blueprint("admin", __name__, url_prefix="/admin")

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user" not in g or g.user is None:
            flash("You are not logged in.")
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

@bp.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    return render_template("admin/dashboard.html")