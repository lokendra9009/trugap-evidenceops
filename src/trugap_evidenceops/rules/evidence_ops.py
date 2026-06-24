from __future__ import annotations

from pathlib import Path

from trugap_evidenceops.models import RuleCategory, RuleResult
from trugap_evidenceops.rules import find_data_file_by_terms, first_existing, relative_path


def check_evidence_tracker(repo: Path) -> RuleResult:
    path = first_existing(
        repo,
        [
            "evidence-tracker.md",
            "evidence-tracker.csv",
            "evidence-tracker.xlsx",
            "evidence_tracker.md",
            "evidence_tracker.csv",
            "evidence_tracker.xlsx",
            "docs/evidence-tracker.md",
            "docs/evidence/tracker.md",
            "docs/evidence/evidence-tracker.md",
            "compliance/evidence-tracker.md",
            "soc2/evidence-tracker.md",
        ],
    )
    if path is None:
        path = find_data_file_by_terms(
            repo,
            required_terms=["evidence"],
            any_terms=["tracker", "register", "inventory", "log"],
        )

    passed = path is not None and path.is_file()

    return RuleResult.from_check(
        id="evidence_tracker_exists",
        title="Evidence tracker file exists",
        category=RuleCategory.EVIDENCE_OPS,
        passed=passed,
        description="Checks whether the repository has a tracker for SOC 2 evidence operations.",
        evidence=[relative_path(repo, path)] if path and path.is_file() else [],
        recommendation=(
            "Add an evidence tracker, such as evidence-tracker.md or docs/evidence/tracker.md."
        ),
    )
