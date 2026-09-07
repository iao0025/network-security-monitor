import json
from pathlib import Path


def append_results(path, results):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as stream:
        for result in results:
            stream.write(json.dumps(result.to_dict(), sort_keys=True) + "\n")


def write_report(path, results):
    up = sum(result.status == "up" for result in results)
    average = round(sum(result.latency_ms for result in results) / len(results), 2) if results else 0
    report = {
        "summary": {"total": len(results), "up": up, "down": len(results) - up,
                    "average_latency_ms": average},
        "results": [result.to_dict() for result in results],
    }
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


