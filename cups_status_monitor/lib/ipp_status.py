from ippx import IppClient

from cups_status_monitor.lib.types import PrinterState, PrinterStatus


def map_state(state: object) -> PrinterState:
    value = str(getattr(state, "value", state)).lower()

    mapping = {
        "idle": PrinterState.IDLE,
        "processing": PrinterState.PRINTING,
        "printing": PrinterState.PRINTING,
        "stopped": PrinterState.STOPPED,
    }

    return mapping.get(value, PrinterState.UNKNOWN)


def get_ipp_status(uri: str) -> PrinterStatus:
    """
    Retrieve printer attributes using IPP.

    Args:
        uri: The printer's IPP URI.

    Returns:
        Dictionary containing printer information.
    """

    with IppClient(uri) as client:
        printer = client.get_printer_attributes()

        return PrinterStatus(
            state=map_state(printer.state),
            reachable=True,
            reasons=list(printer.state_reasons or []),
        )
