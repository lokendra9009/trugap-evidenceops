# Security Policy

## Supported versions

TruGap EvidenceOps Scanner is pre-1.0. Only the latest release on `main`
receives security fixes.

## Reporting a vulnerability

Please report vulnerabilities privately through GitHub's private vulnerability
reporting: open the **Security** tab of this repository and choose
**Report a vulnerability**. This opens a private advisory visible only to the
maintainers.

Do not open a public issue for a security report.

Please include:

- what the issue is and the impact you believe it has;
- the steps or input needed to reproduce it;
- the version or commit you tested.

You can expect an initial acknowledgement within 7 days. Because this project is
maintained on a best-effort basis, please do not expect a same-day response.

## Scope

The scanner reads files from a local directory you point it at and writes a
report. It makes no network calls and executes nothing it reads.

Findings that are in scope include path traversal outside the scanned directory,
writing outside the `--out` directory, crashes or resource exhaustion triggered
by a crafted repository, and any code execution triggered by scanned content.

Findings that are **not** in scope: the scanner reporting a check as failed for a
repository that you believe is compliant. That is a rule-accuracy issue, not a
vulnerability. Please open a normal issue for it.
