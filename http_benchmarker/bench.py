import aiohttp
import asyncio
import time
import numpy as np
import logging
import sys
from tqdm import tqdm  

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def fetch(session, url, method="GET", headers=None, timeout=10):
    """Выполняет один HTTP-запрос и возвращает результат"""
    start_time = time.monotonic()
    request_headers = headers or {
        "User-Agent": "HTTP Benchmarker/1.0"
    }
    
    try:
        async with session.request(
            method, 
            url, 
            headers=request_headers, 
            timeout=timeout
        ) as response:
            # Read the entire response body for accurate measurement
            await response.read()
            latency = (time.monotonic() - start_time) * 1000  # ms
            
            return {
                "status": response.status,
                "latency": latency,
                "success": 200 <= response.status < 400
            }
    except Exception as e:
        latency = (time.monotonic() - start_time) * 1000
        logger.error(f"Request failed: {str(e)}")
        return {
            "error": str(e),
            "latency": latency,
            "success": False
        }

async def run_benchmark(url, total_requests, concurrency, method="GET", headers=None, timeout=10):
    """The main function for performing load testing"""
    start_time = time.time()
    logger.info(f"Starting benchmark for {url}")
    
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Create a progress bar
        pbar = tqdm(
            total=total_requests, 
            desc="Sending requests", 
            unit="req",
            dynamic_ncols=True,   
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        )
        
        #  Create tasks with a callback to update the progress bar
        tasks = []
        for _ in range(total_requests):
            task = asyncio.create_task(fetch(session, url, method, headers, timeout))
            task.add_done_callback(lambda _: pbar.update(1))
            tasks.append(task)
        
        # Waiting for all tasks to be completed.
        results = await asyncio.gather(*tasks)
        pbar.close()
    
    total_time = time.time() - start_time
    
    # Collects statistics
    latencies = [r['latency'] for r in results if 'latency' in r]
    success_count = sum(1 for r in results if r.get('success', False))
    status_codes = {}
    
    for r in results:
        status = r.get('status', 'error')
        status_codes[status] = status_codes.get(status, 0) + 1
    
    # Calculating metrics
    metrics = {
        "total_time": total_time,
        "requests": total_requests,
        "success_count": success_count,
        "success_rate": (success_count / total_requests) * 100 if total_requests else 0,
        "rps": total_requests / total_time if total_time > 0 else 0,
        "status_codes": status_codes
    }
    
    # Add statistics on delays if there is data
    if latencies:
        arr = np.array(latencies)
        metrics.update({
            "min_latency": np.min(arr),
            "max_latency": np.max(arr),
            "avg_latency": np.mean(arr),
            "p50": np.percentile(arr, 50),
            "p90": np.percentile(arr, 90),
            "p95": np.percentile(arr, 95),
            "p99": np.percentile(arr, 99),
            "latencies": latencies
        })
    else:
        metrics.update({
            "min_latency": 0,
            "max_latency": 0,
            "avg_latency": 0,
            "p50": 0,
            "p90": 0,
            "p95": 0,
            "p99": 0
        })
    
    return metrics
