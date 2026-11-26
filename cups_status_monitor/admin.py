from dataclasses import asdict

from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)

from cups_status_monitor.auth import login_required
from cups_status_monitor.lib.shared import Server

"""
Source: https://flask.palletsprojects.com/en/stable/tutorial/views
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application, they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
"""
bp = Blueprint("admin", __name__, url_prefix="/")


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("admin/dashboard.html")


@bp.route("/printers", methods=("GET", "POST"))
@login_required
async def printers():
    if request.method == "POST":
        printers = await Server.refresh_printer_cache()
        return jsonify({"printers": [asdict(printer) for printer in printers]})

    # load the template if it was a GET request
    return render_template("admin/printers.html", printers=Server.printers)
