import asyncio

from cups_status_monitor.lib.connectivity import (
    extract_host,
    scan_connectivity,
)
from cups_status_monitor.lib.ipp_status import get_ipp_status
from cups_status_monitor.lib.monitor import PrinterScanner
from cups_status_monitor.lib.types import PrinterData, PrinterState, PrinterStatus


class Server:
    scanner = PrinterScanner()
    """The shared printer scanner instance."""
    printers: list[PrinterData] = []
    """The cached printer information shared between requests."""

    @classmethod
    async def fetch_printer_data(cls) -> list[PrinterData]:
        discovered_printers = cls.scanner.scan_printers()

        async def collect(printer: dict) -> PrinterData:
            attributes = printer.get("attributes", {})

            uri = attributes.get("device-uri", "")
            host = extract_host(uri) if uri else ""

            status = PrinterStatus()

            # check if the printer can be reached via the network
            if host:
                try:
                    status.protocols = await scan_connectivity(host)
                    status.reachable = any(status.protocols.values())
                except Exception as exception:
                    status.messages.append(
                        f"Failed to verify printer connectivity: {exception}."
                    )

            # get status from IPP
            if status.reachable and uri:
                try:
                    ipp_status = await asyncio.to_thread(
                        get_ipp_status,
                        uri,
                    )

                    ipp_status.protocols = status.protocols
                    ipp_status.reachable = True

                    status = ipp_status
                except Exception as exception:
                    status.messages.append(
                        f"Failed to retrieve printer status over IPP: {exception}."
                    )
            elif not status.reachable:
                status.state = PrinterState.UNREACHABLE
                failed = [
                    name
                    for name, reachable in status.protocols.items()
                    if not reachable
                ]
                status.messages.append(
                    f"No response on the following endpoints: {', '.join(failed)}."
                )

            return PrinterData(
                name=printer.get("name", ""),
                model=attributes.get("printer-make-and-model", ""),
                location=attributes.get("printer-location", ""),
                uri=uri,
                status=status,
            )

        return await asyncio.gather(
            *(collect(printer) for printer in discovered_printers)
        )

    @classmethod
    async def refresh_printer_cache(cls) -> list[PrinterData]:
        cls.printers = await cls.fetch_printer_data()
        return cls.printers
