from dataclasses import asdict

from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)

from cups_status_monitor.auth import login_required
from cups_status_monitor.lib.shared import Server
from cups_status_monitor.lib.utils import format_timestamp

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
        return jsonify(
            {
                "printers": [asdict(printer) for printer in printers],
                "printersLastUpdated": format_timestamp(Server.printers_last_updated),
            }
        )

    # populate it on first load
    if Server.printers_last_updated is None:
        await Server.refresh_printer_cache()

    # load the template if it was a GET request
    return render_template(
        "admin/printers.html",
        printers=Server.printers,
        printers_last_updated=format_timestamp(Server.printers_last_updated),
    )


@bp.route("/classes", methods=("GET", "POST"))
@login_required
async def classes():
    if request.method == "POST":
        classes = await Server.refresh_class_cache()
        return jsonify(
            {
                "classes": classes,
                "classesLastUpdated": format_timestamp(Server.classes_last_updated),
            }
        )

    # populate it on first load
    if Server.classes_last_updated is None:
        await Server.refresh_class_cache()

    return render_template(
        "admin/classes.html",
        classes=Server.classes,
        classes_last_updated=format_timestamp(Server.classes_last_updated),
    )
