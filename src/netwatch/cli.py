import argparse
import time

from .checks import check_target
from .config import load_config
from .storage import append_results, write_report


def run_once(config_path, log_path, report_path):
    targets, timeout = load_config(config_path)
    results = [check_target(target, timeout) for target in targets]
    append_results(log_path, results)
    report = write_report(report_path, results)
    for result in results:
        print(f"[{result.status.upper():4}] {result.target:<28} {result.latency_ms:>8.2f} ms  {result.detail}")
    summary = report["summary"]
    print(f"Summary: {summary['up']} up, {summary['down']} down")
    return 0 if summary["down"] == 0 else 1


def main():
    parser = argparse.ArgumentParser(description="Monitor explicitly configured TCP and HTTP services.")
    parser.add_argument("--config", default="config.example.json")
    parser.add_argument("--log", default="logs/checks.jsonl")
    parser.add_argument("--report", default="reports/latest.json")
    parser.add_argument("--interval", type=float, help="Repeat every N seconds")
    parser.add_argument("--cycles", type=int, default=1, help="Number of checks; 0 repeats until interrupted")
    args = parser.parse_args()
    if args.interval is not None and args.interval < 1:
        raise SystemExit("--interval must be at least 1 second")
    if args.cycles < 0:
        raise SystemExit("--cycles cannot be negative")
    completed = 0
    last_status = 0
    try:
        while args.cycles == 0 or completed < args.cycles:
            last_status = run_once(args.config, args.log, args.report)
            completed += 1
            if args.cycles == 1 or completed == args.cycles:
                break
            if args.interval is None:
                raise SystemExit("--interval is required when --cycles is not 1")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    raise SystemExit(last_status)


if __name__ == "__main__":
    main()


