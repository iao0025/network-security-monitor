import json
from pathlib import Path

from .models import Target


def load_config(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    timeout = float(data.get("timeout_seconds", 2.0))
    if not 0.1 <= timeout <= 30:
        raise ValueError("timeout_seconds must be between 0.1 and 30")
    raw_targets = data.get("targets")
    if not isinstance(raw_targets, list) or not raw_targets:
        raise ValueError("config must contain at least one target")
    if len(raw_targets) > 100:
        raise ValueError("config supports at most 100 explicit targets")
    targets = []
    for item in raw_targets:
        protocol = str(item.get("protocol", "tcp")).lower()
        if protocol not in {"tcp", "http", "https"}:
            raise ValueError(f"unsupported protocol: {protocol}")
        host = str(item["host"]).strip()
        if not host or "/" in host:
            raise ValueError("targets must use an explicit hostname or IP address, not a subnet")
        port = int(item["port"])
        if not 1 <= port <= 65535:
            raise ValueError(f"invalid port: {port}")
        path_value = str(item.get("path", "/"))
        if not path_value.startswith("/"):
            raise ValueError("HTTP paths must begin with /")
        targets.append(Target(str(item.get("name") or f"{host}:{port}"), host, port, protocol, path_value))
    return targets, timeout


