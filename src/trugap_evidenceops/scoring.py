from __future__ import annotations

from collections.abc import Sequence

from trugap_evidenceops.models import RuleCategory, RuleResult, ScoreSummary


def _percentage(part: int, whole: int) -> int:
    """Return ``part`` of ``whole`` as a whole-number percentage, or 0 when ``whole`` is 0."""
    return round((part / whole) * 100) if whole else 0


def score_results(results: Sequence[RuleResult]) -> ScoreSummary:
    """Summarise overall readiness and EvidenceOps readiness for a set of results.

    Overall readiness counts every result. Evidence readiness counts only the
    results whose category is ``RuleCategory.EVIDENCE_OPS``, so checks in other
    categories cannot raise or lower it.
    """
    total = len(results)
    passed = sum(1 for result in results if result.passed)
    failed = total - passed

    evidence_results = [
        result for result in results if result.category == RuleCategory.EVIDENCE_OPS
    ]
    evidence_total = len(evidence_results)
    evidence_ready = sum(1 for result in evidence_results if result.passed)

    return ScoreSummary(
        total_checks=total,
        passed_checks=passed,
        failed_checks=failed,
        score=_percentage(passed, total),
        evidence_checks=evidence_total,
        evidence_ready_checks=evidence_ready,
        evidence_readiness_score=_percentage(evidence_ready, evidence_total),
    )
