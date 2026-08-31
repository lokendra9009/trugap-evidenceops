from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from trugap_evidenceops.report import write_report
from trugap_evidenceops.scanner import scan_repository

app = typer.Typer(no_args_is_help=True, help="TruGap EvidenceOps local scanner.")
console = Console()


@app.callback()
def main() -> None:
    """Scan repositories for SOC 2 engineering evidence readiness."""


@app.command()
def scan(
    repo: Annotated[
        Path,
        typer.Option(
            "--repo",
            "-r",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
            help="Repository directory to scan.",
        ),
    ] = Path("."),
    out: Annotated[
        Path,
        typer.Option(
            "--out",
            "-o",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Directory where report files will be written.",
        ),
    ] = Path("./trugap-report"),
) -> None:
    """Run the local EvidenceOps scan."""
    try:
        report = scan_repository(repo)
        markdown_path, json_path = write_report(report, out)
    except Exception as exc:
        console.print(f"[bold red]Scan failed:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title="TruGap EvidenceOps Scan")
    table.add_column("Status", style="bold")
    table.add_column("Check")
    table.add_column("Evidence")

    for result in report.results:
        status = "[green]PASS[/green]" if result.passed else "[red]FAIL[/red]"
        evidence = "\n".join(result.evidence) if result.evidence else "-"
        table.add_row(status, result.title, evidence)

    console.print(table)
    console.print(
        f"[bold]Overall readiness:[/bold] {report.summary.score}% "
        f"({report.summary.passed_checks}/{report.summary.total_checks} checks passed)"
    )
    console.print(
        f"[bold]Evidence readiness:[/bold] {report.summary.evidence_readiness_score}% "
        f"({report.summary.evidence_ready_checks}/{report.summary.evidence_checks} "
        "EvidenceOps checks passed)"
    )
    console.print(f"[bold]Markdown:[/bold] {markdown_path}")
    console.print(f"[bold]JSON:[/bold] {json_path}")
