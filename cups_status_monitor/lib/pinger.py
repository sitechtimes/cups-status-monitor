# create a function to ping the status of a printer,
# taking its ipp:// or http:// or smtp:// (or whatever protocol it uses, must support all of them)
# as an argument and returning the accurate real-time status of the printer
import socket


def check_printer_status(printer_ip):
    try:
        with socket.create_connection((host, port), timeout=timeout):
                return True
    except (socket.timeout, ConnectionRefusedError, OSError):
            return False

check_printer_status(printer_data)
