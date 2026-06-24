from __future__ import annotations

from pathlib import Path

from trugap_evidenceops.models import RuleCategory, RuleResult
from trugap_evidenceops.rules import first_existing, relative_path


def check_security_md(repo: Path) -> RuleResult:
    path = first_existing(repo, ["SECURITY.md", "security.md"])
    passed = path is not None

    return RuleResult.from_check(
        id="security_md_exists",
        title="SECURITY.md exists",
        category=RuleCategory.POLICIES,
        passed=passed,
        description="Checks whether the repository has a security policy entry point.",
        evidence=[relative_path(repo, path)] if path else [],
        recommendation="Add SECURITY.md at the repository root.",
    )


def check_policies_folder(repo: Path) -> RuleResult:
    path = first_existing(repo, ["docs/policies", "policies"])
    passed = path is not None and path.is_dir()

    return RuleResult.from_check(
        id="policies_folder_exists",
        title="Policy folder exists",
        category=RuleCategory.POLICIES,
        passed=passed,
        description="Checks whether engineering and compliance policies are stored in the repo.",
        evidence=[relative_path(repo, path)] if path and path.is_dir() else [],
        recommendation="Add a docs/policies or policies directory for SOC 2 policy evidence.",
    )
