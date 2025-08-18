import click
import asyncio
import sys
import platform
import os
import json
from datetime import datetime
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
    "bar": "█"
}

def generate_report_filename(format="txt"):
    """Generates a report file name based on the current date and time"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    return f"http_benchmark_{timestamp}.{format}"

def save_text_report(results, filename, symbols):
    """Saves a text report to a file"""
    with open(filename, 'w') as f:
        f.write(f"{symbols['results']} Performance Summary\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Total time:':<20} {results['total_time']:.2f}s\n")
        f.write(f"{'Requests/sec:':<20} {results['rps']:.2f}\n")
        f.write(f"{'Success rate:':<20} {results['success_rate']:.2f}%\n")
        
        f.write(f"\n{symbols['results']} Latency Metrics (ms)\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Average:':<10} {results['avg_latency']:.2f}\n")
        f.write(f"{'Min:':<10} {results['min_latency']:.2f}\n")
        f.write(f"{'Max:':<10} {results['max_latency']:.2f}\n")
        f.write(f"{'p50:':<10} {results['p50']:.2f}\n")
        f.write(f"{'p90:':<10} {results['p90']:.2f}\n")
        f.write(f"{'p95:':<10} {results['p95']:.2f}\n")
        f.write(f"{'p99:':<10} {results['p99']:.2f}\n")
        
        if results['status_codes']:
            f.write(f"\n{symbols['results']} Status Codes\n")
            f.write("-" * 60 + "\n")
            for code, count in results['status_codes'].items():
                f.write(f"{code}: {count} requests\n")
        
        if results.get('errors'):
            f.write(f"\n{symbols['error']} Errors Summary\n")
            f.write("-" * 60 + "\n")
            for error, count in results['errors'].items():
                f.write(f"{error}: {count} occurrences\n")
        
        f.write("\nReport generated at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def save_json_report(results, filename):
    report_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "tool_version": "1.0",
            "parameters": results.get("parameters", {})
        },
        "metrics": {
            k: v for k, v in results.items() 
            if k not in ['parameters', 'latencies', 'status_codes']
        },
        "detailed": {
            "status_codes": results['status_codes'],
            "errors": results.get('errors', {}),
            "latencies": results.get('latencies', [])
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(report_data, f, indent=2)
        
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
@click.option("--json-file", type=click.Path(exists=True), help="Path to JSON file for request body")
@click.option("--save-report", is_flag=True, help="Save results to a file")
@click.option("--report-dir", default="reports", help="Directory to save reports")
@click.option("--json-report", is_flag=True, help="Save report in JSON format")
def bench(url, requests, concurrency, timeout, method, json_file, save_report, report_dir, json_report):
    """Run HTTP benchmark test"""
    try:
        # Displaying information about the test
        click.echo(style(f"{SYMBOLS['rocket']} Benchmarking {method} {url}", fg="blue", bold=True))
        click.echo(style(f"Requests: {requests}, Concurrency: {concurrency}, Timeout: {timeout}s", fg="cyan"))
        
        # Read JSON file if provided
        json_data = None
        if json_file:
            try:
                with open(json_file, 'r') as f:
                    json_data = f.read()
                click.echo(style(f"Using JSON data from: {json_file}", fg="cyan"))
            except Exception as e:
                click.echo(style(f"{SYMBOLS['error']} Failed to read JSON file: {str(e)}", fg="red"))
                return
        
        # Running the test
        results = asyncio.run(run_benchmark(
            url, 
            requests, 
            concurrency,
            method=method,
            timeout=timeout,
            json_data=json_data
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
        
        # Saving a report
        if save_report:
            # Create a directory if it doesn't exist
            os.makedirs(report_dir, exist_ok=True)
            
            # Generating a file name
            filename = generate_report_filename("json" if json_report else "txt")
            filepath = os.path.join(report_dir, filename)
            
            # Save in the selected format
            if json_report:
                save_json_report(results, filepath)
            else:
                save_text_report(results, filepath, SYMBOLS)
            
            click.echo(style(f"\n{SYMBOLS['success']} Report saved to: ", fg="green") + style(filepath, bold=True))
    
    except Exception as e:
        click.echo(style(f"\n{SYMBOLS['error']} Critical Error: {str(e)}", fg="red", bold=True))

if __name__ == "__main__":
    cli()
