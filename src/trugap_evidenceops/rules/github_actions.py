from __future__ import annotations

import re
from pathlib import Path

from trugap_evidenceops.models import RuleCategory, RuleResult
from trugap_evidenceops.rules import first_existing, relative_path

WORKFLOW_SUFFIXES = {".yml", ".yaml"}


def check_github_workflows(repo: Path) -> RuleResult:
    path = repo / ".github" / "workflows"
    passed = path.is_dir()
    evidence = [relative_path(repo, path)] if path.is_dir() else []

    return RuleResult.from_check(
        id="github_workflows_exists",
        title=".github/workflows exists",
        category=RuleCategory.GITHUB_ACTIONS,
        passed=passed,
        description="Checks whether the repository has GitHub Actions workflow definitions.",
        evidence=evidence,
        recommendation="Add a .github/workflows directory for CI/CD evidence.",
    )


def check_dependabot_config(repo: Path) -> RuleResult:
    path = first_existing(
        repo,
        [
            ".github/dependabot.yml",
            ".github/dependabot.yaml",
            "dependabot.yml",
            "dependabot.yaml",
        ],
    )
    passed = path is not None and path.is_file()

    return RuleResult.from_check(
        id="dependabot_config_exists",
        title="Dependabot config exists",
        category=RuleCategory.GITHUB_ACTIONS,
        passed=passed,
        description="Checks whether dependency update automation is configured.",
        evidence=[relative_path(repo, path)] if path and path.is_file() else [],
        recommendation="Add .github/dependabot.yml for dependency update evidence.",
    )


def check_workflow_permissions(repo: Path) -> RuleResult:
    workflow_dir = repo / ".github" / "workflows"
    workflow_files = _workflow_files(workflow_dir)

    files_with_permissions = []
    for path in workflow_files:
        if _has_explicit_permissions(path.read_text(encoding="utf-8")):
            files_with_permissions.append(path)

    missing_permissions = sorted(set(workflow_files) - set(files_with_permissions))
    passed = bool(workflow_files) and not missing_permissions

    evidence = [relative_path(repo, path) for path in files_with_permissions]
    if missing_permissions:
        evidence.extend(
            f"missing permissions: {relative_path(repo, path)}" for path in missing_permissions
        )

    return RuleResult.from_check(
        id="workflow_permissions_declared",
        title="Workflow permissions are explicitly declared",
        category=RuleCategory.GITHUB_ACTIONS,
        passed=passed,
        description="Checks whether GitHub Actions workflows declare token permissions.",
        evidence=evidence,
        recommendation="Add an explicit permissions: block to each workflow file.",
    )


def _workflow_files(workflow_dir: Path) -> list[Path]:
    if not workflow_dir.is_dir():
        return []

    return sorted(
        path
        for path in workflow_dir.iterdir()
        if path.is_file() and path.suffix.lower() in WORKFLOW_SUFFIXES
    )


def _has_explicit_permissions(text: str) -> bool:
    for line in text.splitlines():
        line_without_comment = line.split("#", 1)[0].strip()
        if re.match(r"^permissions\s*:", line_without_comment):
            return True

    return False
