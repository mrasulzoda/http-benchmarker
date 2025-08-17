import click
import asyncio
import sys
import platform
from click import style

try:
    from http_benchmarker.bench import run_benchmark
except ImportError:
    from bench import run_benchmark

SYMBOLS = {
    "rocket": "=>",
    "success": "[OK]",
    "error": "[ERR]",
    "results": "[RES]",
    "bar": "#"
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
        
        # Running the test
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
        
        # Key Metrics
        click.echo(style(f"{'Total time:':<20}", fg="cyan") + 
                  style(f"{results['total_time']:.2f}s", bold=True))
        click.echo(style(f"{'Requests/sec:':<20}", fg="cyan") + 
                  style(f"{results['rps']:.2f}", bold=True))
        
        # Success rate status
        success_rate = results['success_rate']
        success_color = "green" if success_rate > 95 else "yellow" if success_rate > 80 else "red"
        click.echo(style(f"{'Success rate:':<20}", fg="cyan") + 
                  style(f"{success_rate:.2f}%", fg=success_color, bold=True))
        
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
                try:
                    code_int = int(code)
                    color = "green" if 200 <= code_int < 300 else "yellow" if 300 <= code_int < 400 else "red" if 400 <= code_int < 600 else "cyan"
                except ValueError:
                    color = "red"
                click.echo(style(f"{code}:", fg=color, bold=True) + f" {count} requests")
        
        if results.get('errors'):
            click.echo(style(f"\n{SYMBOLS['error']} Errors Summary", fg="red", bold=True))
            click.echo(style("-" * 60, fg="yellow"))
            for error, count in results['errors'].items():
                click.echo(style(f"{error}:", fg="red") + f" {count} occurrences")
    
    except Exception as e:
        click.echo(style(f"\n{SYMBOLS['error']} Critical Error: {str(e)}", fg="red", bold=True))

if __name__ == "__main__":
    cli()
