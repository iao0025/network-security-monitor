import socket
import ssl
import time
from http.client import HTTPConnection, HTTPSConnection

from .models import CheckResult


def check_target(target, timeout):
    started = time.perf_counter()
    try:
        if target.protocol == "tcp":
            with socket.create_connection((target.host, target.port), timeout=timeout):
                detail = "TCP connection established"
        else:
            connection_type = HTTPSConnection if target.protocol == "https" else HTTPConnection
            kwargs = {"timeout": timeout}
            if target.protocol == "https":
                kwargs["context"] = ssl.create_default_context()
            connection = connection_type(target.host, target.port, **kwargs)
            try:
                connection.request("HEAD", target.path, headers={"User-Agent": "netwatch/1.0"})
                response = connection.getresponse()
                detail = f"HTTP {response.status} {response.reason}"
            finally:
                connection.close()
        return CheckResult.create(target, "up", (time.perf_counter() - started) * 1000, detail)
    except (OSError, TimeoutError) as error:
        return CheckResult.create(target, "down", (time.perf_counter() - started) * 1000, str(error))


