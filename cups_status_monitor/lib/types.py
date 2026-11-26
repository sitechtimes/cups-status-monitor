from dataclasses import dataclass, field
from enum import StrEnum


class PrinterState(StrEnum):
    IDLE = "Idle"
    PRINTING = "Printing"
    STOPPED = "Stopped"
    ERROR = "Error"
    UNKNOWN = "Unknown"
    UNREACHABLE = "Unreachable"


@dataclass
class PrinterStatus:
    state: PrinterState = PrinterState.UNKNOWN
    reachable: bool = False

    reasons: list[str] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)

    protocols: dict[str, bool] = field(default_factory=dict)

    # toner_levels: dict[str, int | None] = field(default_factory=dict)


@dataclass
class PrinterData:
    name: str
    model: str
    location: str
    uri: str
    status: PrinterStatus = field(default_factory=PrinterStatus)
