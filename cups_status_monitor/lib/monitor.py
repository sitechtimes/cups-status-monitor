import cups 
from dotenv import load_dotenv
import os

load_dotenv()

cups_ip = os.getenv('CUPS_IP', '127.0.0.1')

cups.setServer(cups_ip)

printer_data = {}

try:
    import cups
    conn = cups.Connection()
    printers = conn.getPrinters()

    if not printers:
        print("No printers found on this system.")
    else:
        for name, attrs in printers.items():
            if not attrs.get("printer-type") & cups.CUPS_PRINTER_CLASS:
                printer_data[name] = dict(attrs)

except Exception as error:
    print(error)

print(printer_data)