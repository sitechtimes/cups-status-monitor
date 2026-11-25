from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)

from cups_status_monitor.auth import login_required
from cups_status_monitor.lib.monitor import PrinterScanner
from cups_status_monitor.lib.pinger import diagnose_printer_by_ip, extract_host

"""
Source: https://flask.palletsprojects.com/en/stable/tutorial/views
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application, they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
"""
bp = Blueprint("admin", __name__, url_prefix="/")

scanner = PrinterScanner()
discovered_printers: list[dict] = []


def refresh_printer_data():
    global discovered_printers
    data = scanner.scan_printers()
    discovered_printers = [
        {
            "name": printer.get("name", ""),
            "model": printer.get("attributes", {}).get("printer-make-and-model", ""),
            "location": printer.get("attributes", {}).get("printer-location", ""),
            "state": any(
                diagnose_printer_by_ip(
                    extract_host(printer.get("attributes", {}).get("device-uri", ""))
                ).values()
            ),
        }
        for printer in data
    ]


refresh_printer_data()


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("admin/dashboard.html")


@bp.route("/printers", methods=("GET", "POST"))
@login_required
def printers():
    global discovered_printers

    if request.method == "GET":
        return render_template("admin/printers.html", printers=discovered_printers)
    elif request.method == "POST":
        refresh_printer_data()
        return jsonify({"printers": discovered_printers})
