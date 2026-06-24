from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from trugap_evidenceops.models import RuleResult, ScanReport
from trugap_evidenceops.rules.evidence_ops import check_evidence_tracker
from trugap_evidenceops.rules.github_actions import (
    check_dependabot_config,
    check_github_workflows,
    check_workflow_permissions,
)
from trugap_evidenceops.rules.policies import check_policies_folder, check_security_md
from trugap_evidenceops.rules.secure_sdlc import (
    check_backup_recovery_runbook,
    check_incident_response_document,
)
from trugap_evidenceops.scoring import score_results

RuleCheck = Callable[[Path], RuleResult]

DEFAULT_RULES: tuple[RuleCheck, ...] = (
    check_security_md,
    check_github_workflows,
    check_dependabot_config,
    check_policies_folder,
    check_incident_response_document,
    check_backup_recovery_runbook,
    check_workflow_permissions,
    check_evidence_tracker,
)


def scan_repository(repo: str | Path) -> ScanReport:
    repo_path = Path(repo).expanduser().resolve()

    if not repo_path.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repo_path}")
    if not repo_path.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {repo_path}")

    results = [rule(repo_path) for rule in DEFAULT_RULES]

    return ScanReport(
        repo_path=str(repo_path),
        summary=score_results(results),
        results=results,
    )
