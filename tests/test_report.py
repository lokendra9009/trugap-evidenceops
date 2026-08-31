from __future__ import annotations

import json
from pathlib import Path

from trugap_evidenceops.models import RuleCategory, RuleResult, ScanReport
from trugap_evidenceops.report import render_markdown, write_report
from trugap_evidenceops.scoring import score_results


def test_markdown_report_shows_overall_and_evidence_readiness() -> None:
    markdown = render_markdown(_report())

    assert "Overall readiness: **50%**" in markdown
    assert "Evidence readiness: **0%**" in markdown
    assert "- Evidence checks: 1" in markdown
    assert "- Evidence ready: 0" in markdown


def test_json_report_keeps_existing_fields_and_adds_evidence_fields(tmp_path: Path) -> None:
    _, json_path = write_report(_report(), tmp_path)

    summary = json.loads(json_path.read_text(encoding="utf-8"))["summary"]

    assert summary["total_checks"] == 4
    assert summary["passed_checks"] == 2
    assert summary["failed_checks"] == 2
    assert summary["score"] == 50
    assert summary["evidence_checks"] == 1
    assert summary["evidence_ready_checks"] == 0
    assert summary["evidence_readiness_score"] == 0


def _report() -> ScanReport:
    results = [
        _result("policy_pass", True),
        _result("policy_also_pass", True),
        _result("policy_fail", False),
        _result("evidence_fail", False, RuleCategory.EVIDENCE_OPS),
    ]

    return ScanReport(
        repo_path="/tmp/example-repo",
        summary=score_results(results),
        results=results,
    )


def _result(
    id: str,
    passed: bool,
    category: RuleCategory = RuleCategory.POLICIES,
) -> RuleResult:
    return RuleResult.from_check(
        id=id,
        title=id.title(),
        category=category,
        passed=passed,
        description="Test result.",
        recommendation="No recommendation.",
    )
