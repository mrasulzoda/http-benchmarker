## 📜 License

This project uses the [Creative Commons Attribution-NonCommercial 4.0 International] license (LICENSE).

You can:
- ⬇️ Download and use the project
- 📝 Study and change the code
- ↔️ Distribute original and derivative works

Under the following conditions:
- 👤 **Attribution** — You must indicate the author and link to the license.
- 🚫 **Non-commercial use** — Commercial use is prohibited

[![CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)

# HTTP Benchmarker

A simple tool for load testing HTTP servers.

## Installation
```bash
git clone https://github.com/your-profile/http-benchmarker.git
cd http-benchmarker
pip install -r requirements.txt
```
## Launch example
```bash
python -m http_benchmarker.cli check https://httpbin.org/get
```
## Output example
```bash
🚀 Benchmarking GET https://httpbin.org/get
Requests: 3, Concurrency: 10, Timeout: 10s
2025-08-16 23:20:20,774 - INFO - Starting benchmark for https://httpbin.org/get

📊 Performance Summary
------------------------------------------------------------
Total time:         1.26s
Requests/sec:       2.39
Success rate:       100.00%

📊 Latency Metrics (ms)
------------------------------------------------------------
Average:  1122.79
Min:      1057.08
Max:      1253.70
p50:      1057.60
p90:      1214.48
p95:      1234.09
p99:      1249.78

📊 Status Codes
------------------------------------------------------------
200: 3 requests
```
