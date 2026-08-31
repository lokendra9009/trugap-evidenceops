from __future__ import annotations

from pathlib import Path

from trugap_evidenceops.scanner import scan_repository


def test_scanner_passes_when_expected_evidence_exists(tmp_path: Path) -> None:
    _write(tmp_path / "SECURITY.md", "# Security\n")
    _write(
        tmp_path / ".github" / "workflows" / "ci.yml",
        "name: CI\npermissions:\n  contents: read\njobs: {}\n",
    )
    _write(
        tmp_path / ".github" / "dependabot.yml",
        "version: 2\nupdates: []\n",
    )
    _write(tmp_path / "docs" / "policies" / "access-control.md", "# Access control\n")
    _write(tmp_path / "docs" / "policies" / "incident-response.md", "# Incident response\n")
    _write(tmp_path / "docs" / "runbooks" / "backup-runbook.md", "# Backup\n")
    _write(tmp_path / "evidence-tracker.md", "# Evidence tracker\n")

    report = scan_repository(tmp_path)

    assert report.summary.total_checks == 8
    assert report.summary.score == 100
    assert report.summary.evidence_checks == 1
    assert report.summary.evidence_readiness_score == 100
    assert all(result.passed for result in report.results)


def test_scanner_reports_missing_items_and_workflow_permissions(tmp_path: Path) -> None:
    _write(
        tmp_path / ".github" / "workflows" / "ci.yml",
        "name: CI\njobs:\n  test:\n    runs-on: ubuntu-latest\n",
    )

    report = scan_repository(tmp_path)
    results = {result.id: result for result in report.results}

    assert results["github_workflows_exists"].passed is True
    assert results["workflow_permissions_declared"].passed is False
    assert (
        "missing permissions: .github/workflows/ci.yml"
        in results["workflow_permissions_declared"].evidence
    )
    assert results["security_md_exists"].passed is False
    assert results["dependabot_config_exists"].passed is False
    assert report.summary.score == 12
    assert report.summary.evidence_checks == 1
    assert report.summary.evidence_ready_checks == 0
    assert report.summary.evidence_readiness_score == 0


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
