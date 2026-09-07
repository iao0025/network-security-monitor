import json
import tempfile
import unittest
from pathlib import Path

from netwatch.config import load_config
from netwatch.models import CheckResult, Target
from netwatch.storage import append_results, write_report


class MonitorTests(unittest.TestCase):
    def test_loads_explicit_target(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps({"targets": [{"name": "Local", "host": "127.0.0.1", "port": 8000}]}))
            targets, timeout = load_config(path)
            self.assertEqual(targets[0].name, "Local")
            self.assertEqual(timeout, 2.0)

    def test_rejects_subnet_notation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps({"targets": [{"host": "192.168.1.0/24", "port": 80}]}))
            with self.assertRaisesRegex(ValueError, "not a subnet"):
                load_config(path)

    def test_rejects_invalid_port(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps({"targets": [{"host": "localhost", "port": 70000}]}))
            with self.assertRaisesRegex(ValueError, "invalid port"):
                load_config(path)

    def test_appends_json_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checks.jsonl"
            result = CheckResult.create(Target("Local", "127.0.0.1", 8000), "up", 12.345)
            append_results(path, [result])
            self.assertEqual(json.loads(path.read_text())["latency_ms"], 12.35)

    def test_report_summarizes_results(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Target("Local", "127.0.0.1", 8000)
            results = [CheckResult.create(target, "up", 10), CheckResult.create(target, "down", 20)]
            report = write_report(Path(directory) / "report.json", results)
            self.assertEqual(report["summary"]["up"], 1)
            self.assertEqual(report["summary"]["down"], 1)


if __name__ == "__main__":
    unittest.main()


