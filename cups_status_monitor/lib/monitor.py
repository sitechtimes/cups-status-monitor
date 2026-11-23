import os

import cups
from dotenv import load_dotenv

load_dotenv()

cups_ip = os.getenv("CUPS_IP", "127.0.0.1")
cups.setServer(cups_ip)


class PrinterScanner:
    def __init__(self):
        self.connection = cups.Connection()
        self.printers: list[dict] = []
        self.classes: list[dict] = []

    def scan_printers(self) -> list[dict]:
        """
        Scans the CUPS server for connected printers.

        Returns:
            The discovered printers (excluding classes).

        Raises:
            IPPError: IPP problem.
        """

        self.printers = []

        discovered_printers: dict = self.connection.getPrinters()

        for printer_name, printer_attributes in discovered_printers.items():
            if not printer_attributes.get("printer-type") & cups.CUPS_PRINTER_CLASS:
                self.printers.append(
                    {"name": printer_name, "attributes": printer_attributes}
                )

        return self.printers

    def scan_classes(self) -> list[dict]:
        """
        Scan the CUPS server for added classes.

        Returns:
            The discovered classes with their printer members.

        Raises:
            IPPError: IPP problem.
        """

        self.classes = []

        discovered_classes: dict = self.connection.getClasses()

        for class_name, class_printers in discovered_classes.items():
            self.classes.append({"name": class_name, "printers": class_printers})

        return self.classes
