from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CheckStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"


class RuleCategory(StrEnum):
    POLICIES = "policies"
    GITHUB_ACTIONS = "github_actions"
    SECURE_SDLC = "secure_sdlc"
    EVIDENCE_OPS = "evidence_ops"


class RuleResult(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: str
    title: str
    category: RuleCategory
    status: CheckStatus
    passed: bool
    description: str
    evidence: list[str] = Field(default_factory=list)
    recommendation: str

    @classmethod
    def from_check(
        cls,
        *,
        id: str,
        title: str,
        category: RuleCategory,
        passed: bool,
        description: str,
        evidence: list[str] | None = None,
        recommendation: str,
    ) -> RuleResult:
        return cls(
            id=id,
            title=title,
            category=category,
            status=CheckStatus.PASS if passed else CheckStatus.FAIL,
            passed=passed,
            description=description,
            evidence=evidence or [],
            recommendation=recommendation,
        )


class ScoreSummary(BaseModel):
    total_checks: int
    passed_checks: int
    failed_checks: int
    score: int


class ScanReport(BaseModel):
    repo_path: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    summary: ScoreSummary
    results: list[RuleResult]
