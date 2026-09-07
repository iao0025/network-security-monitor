# Network Security Monitor

A configuration-driven Python tool that checks the availability and response time of explicitly authorized TCP, HTTP, and HTTPS services. It records timestamped JSON Lines logs and generates a machine-readable summary report for each monitoring cycle.

## Why I built it

I built this project to apply networking, defensive security, logging, and software-testing concepts in a practical tool. It checks only the individual hosts and ports supplied by the user; it does not discover hosts, scan port ranges, or exploit services.

## Features

- TCP connection checks for approved services
- HTTP and HTTPS health checks with certificate validation
- Response-time measurement in milliseconds
- UTC timestamps and structured JSON Lines history
- JSON reports with availability totals and average latency
- One-time or interval-based monitoring
- Configuration validation and a 100-target safety limit
- Automated tests using Python's standard library
- No third-party production dependencies

## Project structure

```text
network-security-monitor/
|-- config.example.json
|-- pyproject.toml
|-- src/netwatch/
|   |-- checks.py
|   |-- cli.py
|   |-- config.py
|   |-- models.py
|   `-- storage.py
`-- tests/
    `-- test_monitor.py
```

## Quick start

Requires Python 3.10 or newer.

```bash
python -m venv .venv
python -m pip install -e .
```

Edit `config.example.json` so it contains only systems you own or are authorized to monitor, then run:

```bash
netwatch --config config.example.json
```

To repeat checks every 30 seconds for five cycles:

```bash
netwatch --config config.example.json --interval 30 --cycles 5
```

Results are written to `logs/checks.jsonl` and `reports/latest.json`. Generated monitoring data is excluded from Git.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Responsible use

Use this tool only with systems you own or have explicit permission to monitor. The project intentionally accepts individual hosts and ports instead of subnets or port ranges.

## Future improvements

- Status-change alerts
- CSV report export
- Configurable latency thresholds
- Lightweight dashboard

## Author

Idowu Ayoola Olawoore


