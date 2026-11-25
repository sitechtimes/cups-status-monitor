from cups_status_monitor.lib.monitor import PrinterScanner
from cups_status_monitor.lib.pinger import diagnose_printer_by_ip, extract_host
from cups_status_monitor.lib.types import PrinterData


class Server:
    scanner = PrinterScanner()
    """The shared printer scanner instance."""
    printers: list[PrinterData] = []
    """The cached printer information shared between requests."""

    @classmethod
    def fetch_printer_data(cls) -> list[PrinterData]:
        return [
            {
                "name": printer.get("name", ""),
                "model": printer.get("attributes", {}).get(
                    "printer-make-and-model", ""
                ),
                "location": printer.get("attributes", {}).get("printer-location", ""),
                "state": any(
                    diagnose_printer_by_ip(
                        extract_host(
                            printer.get("attributes", {}).get("device-uri", "")
                        )
                    ).values()
                ),
            }
            for printer in cls.scanner.scan_printers()
        ]

    @classmethod
    def refresh_printer_cache(cls) -> list[PrinterData]:
        cls.printers = cls.fetch_printer_data()
        return cls.printers


# initialize the printers list on module load
Server.refresh_printer_cache()
