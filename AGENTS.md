# Project Conventions

## Scope

TruGap EvidenceOps Scanner is a local-first SOC 2 evidence scanner for SaaS
repositories. v0.1 must stay simple, deterministic, and filesystem-only.

Do not add GitHub API calls, Gitleaks, Trivy, Semgrep, or other external scanners
until the project explicitly grows past the first local-only version.

## Python

- Use Python 3.11+.
- Use `uv` for environment and dependency management.
- Keep source code under `src/trugap_evidenceops`.
- Prefer small, typed functions with clear names.
- Use Pydantic models for scan results and report output.
- Keep rule checks easy to read and easy to test.

## CLI

- The public command is `trugap scan --repo . --out ./trugap-report`.
- Use Typer for command parsing.
- Use Rich for terminal output.
- Treat `--out` as an output directory.

## Tests and Quality

- Use Pytest for tests.
- Use Ruff for linting and formatting.
- Add or update tests when scanner behavior or scoring changes.
