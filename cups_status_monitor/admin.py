from flask import (
    Blueprint,
    render_template,
)

from cups_status_monitor.auth import login_required
from cups_status_monitor.db import get_db

"""
Source: https://flask.palletsprojects.com/en/stable/tutorial/views
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application, they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
"""
bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    return render_template("admin/dashboard.html")
