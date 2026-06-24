from __future__ import annotations

from trugap_evidenceops.models import RuleCategory, RuleResult
from trugap_evidenceops.scoring import score_results


def test_score_results_counts_passes_and_failures() -> None:
    results = [
        _result("one", True),
        _result("two", False),
        _result("three", True),
        _result("four", False),
    ]

    summary = score_results(results)

    assert summary.total_checks == 4
    assert summary.passed_checks == 2
    assert summary.failed_checks == 2
    assert summary.score == 50


def test_score_results_handles_empty_result_set() -> None:
    summary = score_results([])

    assert summary.total_checks == 0
    assert summary.passed_checks == 0
    assert summary.failed_checks == 0
    assert summary.score == 0


def _result(id: str, passed: bool) -> RuleResult:
    return RuleResult.from_check(
        id=id,
        title=id.title(),
        category=RuleCategory.POLICIES,
        passed=passed,
        description="Test result.",
        recommendation="No recommendation.",
    )
