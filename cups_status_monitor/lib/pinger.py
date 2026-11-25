import socket
from enum import IntEnum
from urllib.parse import urlparse


class PrinterPort(IntEnum):
    APPSOCKET = 9100
    IPP = 631
    HTTP = 80
    HTTPS = 443


def extract_host(uri: str) -> str:
    return urlparse(uri).hostname or ""


def check_printer_port(host: str, port: int, timeout: int = 2) -> bool:
    """
    Tests a TCP connection to a specific printer port.

    Args:
        host (str): The printer host IP.
        port (int): The printer host port.
        timeout (int): The time limit of the connection attempt.

    Returns:
        bool: Whether or not the printer connection succeeded.
    """

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (TimeoutError, ConnectionRefusedError, OSError):
        return False


def diagnose_printer_by_ip(host: str) -> dict[str, bool]:
    """
    Checks multiple protocols/ports to determine if the printer is on, disconnected, or running into issues.

    Args:
        host (str): The printer host IP.

    Returns:
        dict[str, bool]: The port statuses of all printer protocols.
    """

    return {
        "APPSOCKET": check_printer_port(host, PrinterPort.APPSOCKET),
        "IPP": check_printer_port(host, PrinterPort.IPP),
        "HTTP": check_printer_port(host, PrinterPort.HTTP),
        "HTTPS": check_printer_port(host, PrinterPort.HTTPS),
    }
