# TruGap EvidenceOps Scanner

TruGap EvidenceOps Scanner is a local-first CLI for scanning SaaS repositories
for basic SOC 2 engineering evidence readiness.

The v0.1 scanner only inspects files on disk. It does not call the GitHub API
and does not run external security scanners such as Gitleaks, Trivy, or Semgrep.

TruGap is a readiness and evidence scanner. It does not perform a SOC 2 audit,
does not provide independent assurance, and does not guarantee compliance.

## Readiness signals

Reports separate two signals, because having a control in place and being able to
show evidence that it operates are different problems:

- **Overall readiness** — the share of all checks in the scan that passed.
- **Evidence readiness** — the share of `evidence_ops` checks that passed.

Only checks categorised as `evidence_ops` count toward evidence readiness, so a
repository can score well on engineering controls while still having little
evidence tracked. When a scan runs no `evidence_ops` checks, evidence readiness
is reported as 0%.

Both numbers appear in `trugap-report.md` and in the `summary` object of
`trugap-evidence.json`.

## Install

This project uses Python 3.11+ and [uv](https://docs.astral.sh/uv/) for local
environment management.

```bash
uv sync
```

## Usage

Run a scan against the current repository:

```bash
uv run trugap scan --repo . --out ./trugap-report
```

The command writes:

- `./trugap-report/trugap-report.md`
- `./trugap-report/trugap-evidence.json`

## v0.1 Checks

The scanner currently checks for:

- `SECURITY.md`
- `.github/workflows`
- Dependabot configuration
- `docs/policies` or `policies`
- Incident response documentation
- Backup or recovery runbook
- Explicit `permissions:` declarations in GitHub Actions workflows
- Evidence tracker file

## Development

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Format code:

```bash
uv run ruff format .
```
