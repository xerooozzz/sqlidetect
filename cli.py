from rich.console import Console
from pathlib import Path
import os.path
import argparse
import re

# add anything you want to be global here
console = Console()
base_dir = Path(__file__).resolve().parent.parent


# Convert string headers to a dict Headers
def extract_headers(headers: str) -> dict:
    """
    >>> extract_headers('User-agent: YES')
    {'User-agent':'YES'}
    >>> extract_headers('User-agent: YES\nHacker: 3')
    {'User-agent':'YES','Hacker':'3'}
    """
    headers = headers.replace("\\n", "\n")
    sorted_headers = {}
    matches = re.findall(r"(.*):\s(.*)", headers)
    for match in matches:
        header = match[0]
        value = match[1]
        if value[-1] == ",":
            value = value[:-1]
        sorted_headers[header] = value
    return sorted_headers


def cli_opts() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A simple tool to detect SQL errors")
    parser.add_argument(
        "-f",
        "--file",
        help="File of the urls",
        required=False,
        type=lambda x: is_valid_file(parser, x),
    )
    parser.add_argument(
        "-w", "--workers", help="Number of threads", required=False, type=int, default=10
    )
    parser.add_argument("-p", "--proxy", help="Proxy host", required=False)
    parser.add_argument("-H","--header", help="Custom header", required=False)
    parser.add_argument(
        "-t", "--timeout", help="Connection timeout", required=False, default=10, type=int
    )
    parser.add_argument("-o", "--output", help="Output file", required=False)
    parser.add_argument("--stdin", help="Get URLS from stdin", action="store_true")
    return parser.parse_args()

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg  # return the file path


def print_logo():
    logo = "|S|Q|L|i| |D|e|t|e|c|t|o|r|"

    def print_lines():
        x = 0
        for _ in range(30):
            if x == 1:
                console.print("[yellow]-[/yellow]", style="bold", end="")
                x = 0
            else:
                console.print("[green]+[/green]", style="bold", end="")
                x = 1

    print_lines()
    console.print()
    for char in logo:
        if char == "|":
            console.print("[green]|[/green]", style="bold", end="")
        else:
            console.print(char, style="bold", end="")
    console.print()
    console.print(
        "[green bold]|[/green bold] Coded By: [yellow]Eslam Akl [blue]@eslam3kll[/blue][/yellow] & [yellow]Khaled Nassar [blue]@knassar702[/blue][/yellow]"
    )
    console.print("[green bold]|[/green bold] Version: [yellow]1.0.0[/yellow]")
    console.print(
        "[green bold]|[/green bold] Blog: [yellow]eslam3kl.medium.com[/yellow]"
    )
    print_lines()
    console.print()
