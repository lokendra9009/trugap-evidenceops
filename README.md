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

## Scanning this repository

We run the scanner against its own repository. At the time of writing it reports
five of eight checks passing, with evidence readiness at 100%.

Three checks are deliberately left failing rather than closed with placeholder
documents:

- **Policy folder** — there is no organisation here to hold policies.
- **Incident response document** — vulnerability handling is covered by `SECURITY.md`.
- **Backup or recovery runbook** — the scanner holds no state, so there is nothing
  to back up.

Closing those with generated templates would raise the score while describing
controls nobody operates, which is the failure mode this scanner exists to
surface. The reasoning for each is recorded in
[`docs/evidence/tracker.md`](docs/evidence/tracker.md).

All three share a cause worth stating plainly: the v0.1 rule set assumes the
scanned repository belongs to a SaaS company with staff, production
infrastructure, and customer data. Applied to a library or CLI, those checks
measure something that is not true of the target rather than something the target
is missing. Adding repository context, and a way to accept a gap with a recorded
reason, is future work.

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
