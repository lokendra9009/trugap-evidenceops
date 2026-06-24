from __future__ import annotations

from collections.abc import Sequence

from trugap_evidenceops.models import RuleResult, ScoreSummary


def score_results(results: Sequence[RuleResult]) -> ScoreSummary:
    total = len(results)
    passed = sum(1 for result in results if result.passed)
    failed = total - passed
    score = round((passed / total) * 100) if total else 0

    return ScoreSummary(
        total_checks=total,
        passed_checks=passed,
        failed_checks=failed,
        score=score,
    )
