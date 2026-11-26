from datetime import datetime


def format_timestamp(timestamp: datetime | None) -> str | None:
    """
    Format a datetime value as a string.

    The output format is:
        %a, %d %b %Y %H:%M:%S.%f

    Args:
        timestamp (datetime | None): The timestamp to format, or None.

    Returns:
        str | None: The formatted datetime string, or None if the input is None.

    Examples:
        >>> format_timestamp(datetime(2025, 1, 15, 14, 30, 45))
        'Wed, 15 Jan 2025 14:30:45.000000'

        >>> format_timestamp(None) is None
        True
    """

    return timestamp.strftime("%a, %d %b %Y %H:%M:%S.%f") if timestamp else None
