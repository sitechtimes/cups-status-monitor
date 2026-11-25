from typing import TypedDict

from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)

from cups_status_monitor.auth import login_required
from cups_status_monitor.lib.monitor import PrinterScanner
from cups_status_monitor.lib.pinger import diagnose_printer_by_ip, extract_host


class PrinterData(TypedDict):
    name: str
    model: str
    location: str
    state: bool


"""
Source: https://flask.palletsprojects.com/en/stable/tutorial/views
A Blueprint is a way to organize a group of related views and other code.
Rather than registering views and other code directly with an application, they are registered with a blueprint.
Then the blueprint is registered with the application when it is available in the factory function.
"""
bp = Blueprint("admin", __name__, url_prefix="/")

scanner = PrinterScanner()


def fetch_printer_data() -> list[PrinterData]:
    return [
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
        for printer in scanner.scan_printers()
    ]


discovered_printers: list[PrinterData] = fetch_printer_data()
"""Cached printer information shared between requests."""


def refresh_printer_cache() -> list[PrinterData]:
    global discovered_printers
    discovered_printers = fetch_printer_data()
    return discovered_printers


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("admin/dashboard.html")


@bp.route("/printers", methods=("GET", "POST"))
@login_required
def printers():
    if request.method == "POST":
        return jsonify({"printers": refresh_printer_cache()})

    # load the template if it was a GET request
    return render_template("admin/printers.html", printers=discovered_printers)
