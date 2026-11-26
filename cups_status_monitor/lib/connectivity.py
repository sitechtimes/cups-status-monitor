import asyncio
import socket
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class Endpoint:
    name: str
    port: int
    protocol: str = "TCP"


ENDPOINTS = [
    Endpoint("AppSocket", 9100),
    Endpoint("IPP", 631),
    Endpoint("IPPS", 443),
    Endpoint("HTTP", 80),
    Endpoint("HTTPS", 443),
    Endpoint("LPD", 515),
]
"""The possible endpoints to test."""


def extract_host(uri: str) -> str:
    """
    Extract the hostname from a URI string.

    Args:
        uri (str): The URI string to extract.

    Returns:
        str: The extracted hostname, or the stripped URI if no hostname was extracted.
    """

    return urlparse(uri).hostname or uri.strip()


def check_tcp(
    host: str,
    port: int,
    timeout: float = 2.0,
) -> bool:
    """
    Attempt a TCP socket connection to a given host and port.

    Args:
        host (str): The hostname to test.
        port (int): The port to test the connection on.
        timeout (float): The maximum time to wait before marking the connection as failed.

    Returns:
        bool: Whether or not the connection succeeded.
    """

    try:
        with socket.create_connection(
            (host, port),
            timeout=timeout,
        ):
            return True
    except OSError:
        return False


async def probe_endpoint(
    host: str,
    endpoint: Endpoint,
) -> tuple[str, bool]:
    """
    Check if the host is available on a given endpoint.

    Args:
        host (str): The hostname to check.
        endpoint (Endpoint): The endpoint to test.

    Returns:
        tuple[str, bool]: The name of the endpoint and the result of the test.
    """

    if endpoint.protocol == "TCP":
        result = await asyncio.to_thread(
            check_tcp,
            host,
            endpoint.port,
        )
        return endpoint.name, result

    raise ValueError(f"The provided protocol is not supported: {endpoint.protocol}.")


async def scan_connectivity(host: str) -> dict[str, bool]:
    """
    Test the connectivity of a given hostname on all supported endpoints.

    Args:
        host (str): The hostname to scan the connectivity of.

    Returns:
        dict[str, bool]: A map of each tested endpoint name to whether or not a TCP connection succeeded to that endpoint.
    """

    results = await asyncio.gather(
        *[probe_endpoint(host, endpoint) for endpoint in ENDPOINTS]
    )

    return dict(results)
