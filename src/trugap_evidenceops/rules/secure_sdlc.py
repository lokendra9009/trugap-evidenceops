from __future__ import annotations

from pathlib import Path

from trugap_evidenceops.models import RuleCategory, RuleResult
from trugap_evidenceops.rules import find_document_by_terms, first_existing, relative_path


def check_incident_response_document(repo: Path) -> RuleResult:
    path = first_existing(
        repo,
        [
            "INCIDENT_RESPONSE.md",
            "incident-response.md",
            "incident_response.md",
            "docs/incident-response.md",
            "docs/incident_response.md",
            "docs/policies/incident-response.md",
            "policies/incident-response.md",
            "runbooks/incident-response.md",
            "docs/runbooks/incident-response.md",
        ],
    )
    if path is None:
        path = find_document_by_terms(
            repo,
            required_terms=["incident"],
            any_terms=["response", "runbook"],
        )

    passed = path is not None and path.is_file()

    return RuleResult.from_check(
        id="incident_response_document_exists",
        title="Incident response document exists",
        category=RuleCategory.SECURE_SDLC,
        passed=passed,
        description="Checks whether incident response evidence is present in the repository.",
        evidence=[relative_path(repo, path)] if path and path.is_file() else [],
        recommendation=(
            "Add an incident response document, such as docs/policies/incident-response.md."
        ),
    )


def check_backup_recovery_runbook(repo: Path) -> RuleResult:
    path = first_existing(
        repo,
        [
            "backup-runbook.md",
            "recovery-runbook.md",
            "restore-runbook.md",
            "docs/runbooks/backup-runbook.md",
            "docs/runbooks/recovery-runbook.md",
            "docs/runbooks/restore-runbook.md",
            "runbooks/backup-runbook.md",
            "runbooks/recovery-runbook.md",
            "runbooks/restore-runbook.md",
            "docs/policies/backup-recovery.md",
            "policies/backup-recovery.md",
        ],
    )
    if path is None:
        path = find_document_by_terms(
            repo,
            required_terms=[],
            any_terms=["backup", "recovery", "restore", "disaster-recovery"],
        )

    passed = path is not None and path.is_file()

    return RuleResult.from_check(
        id="backup_recovery_runbook_exists",
        title="Backup or recovery runbook exists",
        category=RuleCategory.SECURE_SDLC,
        passed=passed,
        description="Checks whether backup, restore, or recovery runbook evidence is present.",
        evidence=[relative_path(repo, path)] if path and path.is_file() else [],
        recommendation="Add a backup or recovery runbook under docs/runbooks or runbooks.",
    )
