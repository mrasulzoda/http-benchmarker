# HTTP Benchmarker

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Advanced HTTP load testing tool with real-time progress monitoring and detailed performance reports.

## Features

- ⚡ **Asynchronous requests** for high-concurrency testing
- 📊 **Comprehensive metrics**: RPS, latency percentiles, success rate
- 🚀 **Real-time progress** with TQDM integration
- 📝 **Detailed error reporting** with error grouping
- 💾 **Automatic report generation** (text/JSON)
- 📈 **Statistical analysis**: p50, p90, p95, p99 latency
- 🎨 **Color-coded terminal output**

## Installation

```bash
git clone https://github.com/your-profile/http-benchmarker.git
cd http-benchmarker
pip install -r requirements.txt
```

## Basic Usage

### Run benchmark with default parameters:

```bash
python -m http_benchmarker.cli bench https://example.com
```
### Advanced test with custom parameters:

```bash
python -m http_benchmarker.cli bench https://api.example.com/data \
  --requests 500 \
  --concurrency 50 \
  --timeout 5
```

### Save results to a report file:

```bash
# Save as text report
python -m http_benchmarker.cli bench https://example.com --save-report

# Save as JSON report
python -m http_benchmarker.cli bench https://example.com --save-report --json-report
```
### Output Example

```bash
=> Benchmarking GET https://httpbin.org/get
Requests: 100, Concurrency: 10, Timeout: 10s
2025-08-17 10:15:33,820 - INFO - Starting benchmark for https://httpbin.org/get
Sending requests: 100%|████████████████████| 100/100 [00:04<00:00, 20.57req/s]

[RES] Performance Summary
------------------------------------------------------------
Total time:         4.87s
Requests/sec:       20.54
Success rate:       100.00%

[RES] Latency Metrics (ms)
------------------------------------------------------------
Average:  2993.57
Min:      1133.80
Max:      4849.47
p50:      3062.11
p90:      4524.57
p95:      4743.53
p99:      4839.26

[RES] Status Codes
------------------------------------------------------------
200: 100 requests

[OK] Report saved to: reports/http_benchmark_20250817_101533.json
```
## Report Files

### Reports are automatically saved with timestamped filenames:

-  reports/http_benchmark_20250817_101533.txt
-  reports/http_benchmark_20250817_101533.json

## Command Options

| Option             | Description                          | Default     |
 |--------------------|--------------------------------------|-------------|
 | URL                | Target URL to test                   | Required    |
 | -r, --requests     | Total number of requests             | 100         |
 | -c, --concurrency  | Concurrent connections               | 10          |
 | -t, --timeout      | Request timeout (seconds)            | 10          |
 | -m, --method       | HTTP method                          | GET         |
 | --save-report      | Save results to file                 | False       |
 | --json-report      | Save in JSON format                  | False       |
 | --report-dir       | Reports directory                    | reports     |


# 📜 License

This project uses the Creative Commons Attribution-NonCommercial 4.0 International license.

You can:

    ⬇️ Download and use the project

    📝 Study and modify the code

    ↔️ Distribute original and derivative works

Under the following conditions:

    👤 Attribution — You must give appropriate credit and link to the license

    🚫 NonCommercial — You may not use the material for commercial purposes



