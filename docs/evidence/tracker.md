# Evidence Tracker

This is the evidence register for the TruGap EvidenceOps Scanner repository
itself. It records, for each check the scanner runs, where the supporting
evidence actually lives — or why no evidence exists.

It is maintained by hand. It is not generated, and it is not an auditor
assessment. TruGap does not perform a SOC 2 audit or provide assurance.

Last reviewed: 2026-08-31

## Repository facts these entries depend on

- The scanner is a local CLI. It has no deployed service, no database, no
  customer data, and no production environment.
- The project has no employees and no corporate entity behind it.
- Everything below is scoped to this repository only.

## Evidence register

| Check | Status | Evidence artifact | Notes |
| --- | --- | --- | --- |
| `security_md_exists` | Ready | `SECURITY.md` | Private disclosure via GitHub Security Advisories. |
| `github_workflows_exists` | Ready | `.github/workflows/ci.yml` | Runs Ruff and Pytest on every push to `main` and every PR. |
| `dependabot_config_exists` | Ready | `.github/dependabot.yml` | Weekly `uv` and `github-actions` update checks. |
| `workflow_permissions_declared` | Ready | `.github/workflows/ci.yml` | `permissions: contents: read` at workflow level. |
| `evidence_tracker_exists` | Ready | this file | Reviewed when checks or repository facts change. |
| `policies_folder_exists` | Not applicable | — | No organisation exists to hold policies. See below. |
| `incident_response_document_exists` | Not applicable | — | Disclosure handling is in `SECURITY.md`. See below. |
| `backup_recovery_runbook_exists` | Not applicable | — | Nothing to back up. See below. |

## Why three checks are deliberately left failing

These are recorded as gaps rather than closed with documents that would describe
controls nobody operates. Writing such documents is the exact failure mode this
scanner is meant to surface, so closing them that way would be dishonest.

**Policy folder.** SOC 2 policies describe how an organisation governs access,
change management, and vendors. There is no organisation here — no staff, no
access to grant, no vendors. A `docs/policies/` folder would contain templates
that govern nobody.

**Incident response document.** The relevant incident type for this project is a
reported vulnerability, and that process is documented in `SECURITY.md`
(reporting path, expected acknowledgement time, scope). A separate document
covering paging rotations, severity tiers, and customer notification would
describe a response capability that does not exist.

**Backup or recovery runbook.** The scanner holds no state. It reads a directory
and writes a report. The only asset is the Git repository, which is replicated on
GitHub and in every clone. There is no backup procedure to document and no
recovery objective to state.

## What this tells us about the scanner

All three gaps share a cause: the v0.1 rule set assumes the scanned repository
belongs to a SaaS company with staff, production infrastructure, and customer
data. Applied to a library or CLI, those checks measure something that is not
true of the target rather than something the target is missing.

The rules are not wrong for their intended audience. They are missing a notion of
repository context, and of a gap being explicitly accepted with a reason instead
of silently failing.

Tracked as future work; not implemented in v0.1.
