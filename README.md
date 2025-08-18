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

### Запуск теста с параметрами по умолчанию (100 запросов, 10 потоков)

```bash
python -m http_benchmarker.cli bench https://example.com

```
### Расширенный тест с кастомными параметрами

```bash
python -m http_benchmarker.cli bench https://api.example.com/data \
  --requests 500 \
  --concurrency 50 \
  --timeout 5
```

### POST запрос с JSON данными из файла

```bash
python -m http_benchmarker.cli bench https://api.example.com/data \
  --method POST \
  --json-file data.json
```

### PUT запрос с JSON данными из файла

```bash
python -m http_benchmarker.cli bench https://api.example.com/data \
  --method PUT \
  --json-file update.json \
  --requests 500 \
  --concurrency 50
```

### Save results to a report file:

```bash
# Save as text report
python -m http_benchmarker.cli bench https://api.example.com --save-report

# Save as JSON report
python -m http_benchmarker.cli bench https://api.example.com --save-report --json-report
```
# Report Files

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
 | -m, --method       | HTTP method (GET,POST,PUT)           | GET         |
 | --json-file        | Path to the JSON file with the       |             |
 |                    | request body                         | None        |
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



