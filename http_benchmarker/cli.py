import click
import asyncio
from http_benchmarker.bench import run_benchmark
import sys
import platform
from click import style

if sys.version_info[0] == 3 and sys.stdout.encoding != 'UTF-8':
    try:
        sys.stdout = open(sys.stdout.fileno(), mode='w', 
                         encoding='utf-8', buffering=1)
    except:
        pass

if platform.system() == "Windows":
    SYMBOLS = {
        "rocket": "==>",
        "success": "[OK]",
        "error": "[ERROR]",
        "results": "==== RESULTS ====",
        "bar": "#"
    }
 
    try:
        import colorama
        colorama.init()
    except ImportError:
        pass
else:
    SYMBOLS = {
        "rocket": "=>",
        "success": "[OK]",
        "error": "[ERR]",
        "results": "[RES]",
        "bar": "█"
    }

@click.group()
def cli():
    """HTTP Benchmarking Tool"""
    pass

@cli.command()
@click.argument("url")
@click.option("-r", "--requests", default=100, help="Total number of requests")
@click.option("-c", "--concurrency", default=10, help="Concurrent connections")
@click.option("-t", "--timeout", default=10, help="Request timeout in seconds")
@click.option("-m", "--method", default="GET", help="HTTP method")
def bench(url, requests, concurrency, timeout, method):
    """Run HTTP benchmark test"""
    try:
        # Displaying information about the test
        click.echo(style(f"{SYMBOLS['rocket']} Benchmarking {method} {url}", fg="blue", bold=True))
        click.echo(style(f"Requests: {requests}, Concurrency: {concurrency}, Timeout: {timeout}s", fg="cyan"))
        
        # Runs the test
        results = asyncio.run(run_benchmark(
            url, 
            requests, 
            concurrency,
            method=method,
            timeout=timeout
        ))
        
        # Displaying the results
        click.echo(style(f"\n{SYMBOLS['results']} Performance Summary", fg="green", bold=True))
        click.echo(style("-" * 60, fg="yellow"))
        
        # Key metrics
        click.echo(style(f"{'Total time:':<20}", fg="cyan") + 
                  style(f"{results['total_time']:.2f}s", bold=True))
        click.echo(style(f"{'Requests/sec:':<20}", fg="cyan") + 
                  style(f"{results['rps']:.2f}", bold=True))
        
        # Success rate status with color 
        success_color = "green" if results['success_rate'] > 95 else "yellow" if results['success_rate'] > 80 else "red"
        click.echo(style(f"{'Success rate:':<20}", fg="cyan") + 
                  style(f"{results['success_rate']:.2f}%", fg=success_color, bold=True))
        
        # Delay statistics
        click.echo(style(f"\n{SYMBOLS['results']} Latency Metrics (ms)", fg="green", bold=True))
        click.echo(style("-" * 60, fg="yellow"))
        click.echo(style(f"{'Average:':<10}", fg="cyan") + style(f"{results['avg_latency']:.2f}", bold=True))
        click.echo(style(f"{'Min:':<10}", fg="cyan") + style(f"{results['min_latency']:.2f}", bold=True))
        click.echo(style(f"{'Max:':<10}", fg="cyan") + style(f"{results['max_latency']:.2f}", bold=True))
        click.echo(style(f"{'p50:':<10}", fg="cyan") + style(f"{results['p50']:.2f}", bold=True))
        click.echo(style(f"{'p90:':<10}", fg="cyan") + style(f"{results['p90']:.2f}", bold=True))
        click.echo(style(f"{'p95:':<10}", fg="cyan") + style(f"{results['p95']:.2f}", bold=True))
        click.echo(style(f"{'p99:':<10}", fg="cyan") + style(f"{results['p99']:.2f}", bold=True))
        
        # Status codes
        if results['status_codes']:
            click.echo(style(f"\n{SYMBOLS['results']} Status Codes", fg="green", bold=True))
            click.echo(style("-" * 60, fg="yellow"))
            for code, count in results['status_codes'].items():
                color = "green" if 200 <= code < 300 else "yellow" if 300 <= code < 400 else "red" if 400 <= code < 600 else "cyan"
                click.echo(style(f"{code}:", fg=color, bold=True) + f" {count} requests")
    
    except Exception as e:
        click.echo(style(f"\n{SYMBOLS['error']} Error: {str(e)}", fg="red", bold=True))

if __name__ == "__main__":
    cli()
