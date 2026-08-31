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
    assert summary.evidence_checks == 0
    assert summary.evidence_ready_checks == 0
    assert summary.evidence_readiness_score == 0


def test_evidence_readiness_is_scored_separately_from_overall_readiness() -> None:
    results = [
        _result("policy_pass", True),
        _result("policy_fail", False),
        _result("evidence_pass", True, RuleCategory.EVIDENCE_OPS),
        _result("evidence_fail", False, RuleCategory.EVIDENCE_OPS),
    ]

    summary = score_results(results)

    assert summary.score == 50
    assert summary.evidence_checks == 2
    assert summary.evidence_ready_checks == 1
    assert summary.evidence_readiness_score == 50


def test_passing_non_evidence_checks_do_not_raise_evidence_readiness() -> None:
    results = [_result(f"policy_{index}", True) for index in range(5)]
    results += [_result(f"sdlc_{index}", True, RuleCategory.SECURE_SDLC) for index in range(5)]
    results.append(_result("evidence_fail", False, RuleCategory.EVIDENCE_OPS))

    summary = score_results(results)

    assert summary.score == 91
    assert summary.evidence_checks == 1
    assert summary.evidence_ready_checks == 0
    assert summary.evidence_readiness_score == 0


def test_evidence_readiness_is_full_when_every_evidence_check_passes() -> None:
    results = [
        _result("policy_fail", False),
        _result("evidence_one", True, RuleCategory.EVIDENCE_OPS),
        _result("evidence_two", True, RuleCategory.EVIDENCE_OPS),
    ]

    summary = score_results(results)

    assert summary.score == 67
    assert summary.evidence_checks == 2
    assert summary.evidence_ready_checks == 2
    assert summary.evidence_readiness_score == 100


def test_evidence_readiness_is_zero_when_no_evidence_checks_ran() -> None:
    results = [
        _result("policy_pass", True),
        _result("sdlc_pass", True, RuleCategory.SECURE_SDLC),
    ]

    summary = score_results(results)

    assert summary.score == 100
    assert summary.evidence_checks == 0
    assert summary.evidence_ready_checks == 0
    assert summary.evidence_readiness_score == 0


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
