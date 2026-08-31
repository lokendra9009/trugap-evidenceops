from __future__ import annotations

import json
from pathlib import Path

from jinja2 import Template

from trugap_evidenceops.models import ScanReport

REPORT_TEMPLATE = (
    "# TruGap EvidenceOps Scan Report\n\n"
    "Repository: `{{ report.repo_path }}`\n"
    "Generated: `{{ report.generated_at.isoformat() }}`\n\n"
    "## Summary\n\n"
    "Overall readiness: **{{ report.summary.score }}%**\n"
    "Evidence readiness: **{{ report.summary.evidence_readiness_score }}%**\n\n"
    "- Total checks: {{ report.summary.total_checks }}\n"
    "- Passed: {{ report.summary.passed_checks }}\n"
    "- Failed: {{ report.summary.failed_checks }}\n"
    "- Evidence checks: {{ report.summary.evidence_checks }}\n"
    "- Evidence ready: {{ report.summary.evidence_ready_checks }}\n\n"
    "Overall readiness covers every check in this scan. Evidence readiness covers only "
    "the EvidenceOps checks found by this local scanner. Both are scanner signals, not "
    "an auditor assessment.\n\n"
    "## Checks\n\n"
    "| Status | Check | Category | Evidence | Recommendation |\n"
    "| --- | --- | --- | --- | --- |\n"
    "{% for result in report.results -%}\n"
    "{% set status = 'PASS' if result.passed else 'FAIL' -%}\n"
    "{% set evidence = result.evidence | join('<br>') if result.evidence else '-' -%}\n"
    "| {{ status }} | {{ result.title }} | {{ result.category }} | "
    "{{ evidence }} | {{ result.recommendation }} |\n"
    "{% endfor %}\n"
)


def render_markdown(report: ScanReport) -> str:
    return Template(REPORT_TEMPLATE).render(report=report)


def write_report(report: ScanReport, out_dir: str | Path) -> tuple[Path, Path]:
    output_dir = Path(out_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    markdown_path = output_dir / "trugap-report.md"
    json_path = output_dir / "trugap-evidence.json"

    markdown_path.write_text(render_markdown(report), encoding="utf-8")
    json_path.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2) + "\n",
        encoding="utf-8",
    )

    return markdown_path, json_path
