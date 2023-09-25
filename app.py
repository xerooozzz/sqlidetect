# app.py
from pytest import console_main
import requests
import random
import re
import threading
import json
from pathlib import Path
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Column

requests.packages.urllib3.disable_warnings()  # Disable SSL warnings

class Scanner:
    def __init__(
        self,
        timeout: int = 10,
        headers: dict = {},
        proxies: dict = {},
        custom_payloads: list = [],
    ):
        self.found = []
        self.timeout = timeout
        self.proxies = proxies
        self.headers = headers
        self.user_agents = (
            Path(f"{base_dir}/user_agents.txt").read_text().splitlines()
        )
        self.sql_errors = (
            Path(f"{base_dir}/sql_errors.txt").read_text().splitlines()
        )
        self.payloads = Path(f"{base_dir}/payloads.txt").read_text().splitlines()
        self.custom_payloads = custom_payloads
        self._lock = threading.Lock()

    def start(self, targets_file: str, workers: int = 10):
        new_targets = self.read_targets_from_file(targets_file)

        with Progress(
            TextColumn(
                "[progress.percentage] Scanning {task.completed}/{task.total} | {task.percentage:>3.0f}% ",
                table_column=Column(ratio=1),
            ),
            BarColumn(bar_width=50, table_column=Column(ratio=2)),
            SpinnerColumn(),
            console=console,
        ) as progress:
            pb_counter = len(new_targets)
            task1 = progress.add_task("[green] Scanning ...", total=pb_counter)
            with ThreadPoolExecutor(max_workers=workers) as executor:
                for url in new_targets:
                    executor.submit(self.send, url, task1, progress)

    def send(self, url: str, task1, progress):
        user_agent = random.choice(self.user_agents)
        headers = {"User-Agent": user_agent}
        headers.update(self.headers)
        try:
            response = requests.get(
                url,
                headers=headers,
                verify=False,
                proxies=self.proxies,
                timeout=self.timeout,
            ).text
            for pattern in self.sql_errors + self.custom_payloads:
                pattern = pattern.strip()
                if re.findall(pattern, response):
                    with self._lock:
                        self.found.append((url, pattern))
                        console.print(
                            f"[yellow bold]>>> [/yellow bold] {url}  [red bold]{pattern}[/red bold]"
                        )
        except KeyboardInterrupt:
            exit()
        except:
            pass  # IGNORING THE ERRORS

    def read_targets_from_file(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                targets = [line.strip() for line in file if '?' in line]
            return targets
        except FileNotFoundError:
            console_main.print("[red]File not found. Please provide a valid file path.[/red]")
            exit()

    def write_report(self, output: str):
        with open(output, "w") as f:
            f.write(json.dumps(self.found))

# Rest of the code remains unchanged
