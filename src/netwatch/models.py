from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Target:
    name: str
    host: str
    port: int
    protocol: str = "tcp"
    path: str = "/"


@dataclass(frozen=True)
class CheckResult:
    target: str
    host: str
    port: int
    protocol: str
    status: str
    latency_ms: float
    checked_at: str
    detail: str = ""

    @classmethod
    def create(cls, target, status, latency_ms, detail=""):
        return cls(target.name, target.host, target.port, target.protocol, status,
                   round(latency_ms, 2), datetime.now(timezone.utc).isoformat(), detail)

    def to_dict(self):
        return asdict(self)


