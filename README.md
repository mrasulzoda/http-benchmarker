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
```
