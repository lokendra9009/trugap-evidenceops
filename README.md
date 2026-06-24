# TruGap EvidenceOps Scanner

TruGap EvidenceOps Scanner is a local-first CLI for scanning SaaS repositories
for basic SOC 2 engineering evidence readiness.

The v0.1 scanner only inspects files on disk. It does not call the GitHub API
and does not run external security scanners such as Gitleaks, Trivy, or Semgrep.

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
